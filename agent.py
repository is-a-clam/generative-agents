from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_ollama.llms import OllamaLLM
from pydantic import BaseModel, Field
from textwrap import dedent
from utils import State
import mesa

# Typing
from typing import Self

# Debug
from utils import chain_print

class ReasonedBool(BaseModel):
    response: bool = Field(description="answer")
    reasoning: str = Field(description="reasoning for answer")

class Agent(mesa.Agent):
    def __init__(self, model, name: str, age: int, traits: list[str], infected: bool):
        super().__init__(model)
        # Agent Constants
        self.name = name
        self.age = age
        self.traits = traits

        # Agent LLM 
        self.decision_chain = self.initialise_chain()

        # Agent State
        self.home = True
        self.infected_day = 0 if infected else None
        self.interactions: list[Self] = []
        self.decision: ReasonedBool = None

    @property
    def days_infected(self):
        return self.model.current_day - self.infected_day
    
    @property
    def state(self):
        if self.infected_day is None:
            return State.SUSCEPTIBLE
        if self.days_infected <= self.model.time_to_heal:
            return State.INFECTED
        return State.RECOVERED

    def initialise_chain(self):
        llm = OllamaLLM(model="llama3-groq-tool-use")
        parser = PydanticOutputParser(pydantic_object=ReasonedBool)
        prompt = ChatPromptTemplate(
            messages=[
                ("system", dedent('''\
                    Your name is {name}. You are {age} years old. You lives in the town of Fort Halloway. You like the town and have friends who also live here. You have a job and go to the office for work everyday.
            
                    Your traits are given below:
                    {traits}
                                    
                    Your relevant memories are below:
                    {self_eval}
                    {environment_eval}
                    
                    {format_instructions}
                ''')),
                ("human", "{query}")
            ],
            input_variables=["self_eval", "environment_eval", "query"],
            partial_variables={
                "name": self.name,
                "age": self.age,
                "traits": ", ".join(self.traits),
                "format_instructions": parser.get_format_instructions(),
            }
        )
        return prompt | llm | parser | chain_print
    
    def check_infection_visible(self):
        if self.state == State.INFECTED and self.days_infected == self.model.infection_visible:
            self.model.agents_visible.append(self)

    def evaluate_self(self):
        conditions = [
            "You feel normal.",
            "You have a light cough.",
            "You have a fever and a cough.",
        ]

        if not self.state == State.INFECTED:
            return conditions[0]
        
        return conditions[self.model.infection_severity[self.days_infected-1]]

    def evaluate_environment(self):
        return dedent(f'''\
            You know about the Catasat virus spreading across the country. It is an infectious disease that spreads from human to human contact via an airborne virus. The deadliness of the virus is unknown. Scientists are warning about a potential epidemic.
            
            You check the newspaper and find that {len(self.model.agents_visible)/self.model.population:.1%} of Fort Halloway's population caught new infections of the Catasat virus yesterday.

            Staying at home will reduce your chance of contracting the virus. Leaving home will allow you to go to the office to work.
        ''')

    def decide_location(self):
        output: ReasonedBool = self.decision_chain.invoke({
            "self_eval": self.evaluate_self(),
            "environment_eval": self.evaluate_environment(),
            "query": "Should you stay at home all day and why?",
        })
        self.decision = output
        if not output.response:
            self.home = False
            self.model.agents_outside.append(self)
        
    def make_interactions(self):
        if self.home:
            return

        potential_interactions = [a for a in self.model.agents_outside if a is not self and a not in self.interactions]
        
        while len(self.interactions) < self.model.max_interactions and len(potential_interactions) > 0:
            other = self.random.choice(potential_interactions)
            self.interact(other)
            potential_interactions.remove(other)
        
    def interact(self, other: Self):
        self.interactions.append(other)
        other.interactions.append(self)

        if self.state == State.INFECTED and other.state == State.SUSCEPTIBLE:
            if self.random.random() < self.model.infection_rate:
                other.infected_day = self.model.current_day
        elif self.state == State.SUSCEPTIBLE and other.state == State.INFECTED:
            if self.random.random() < self.model.infection_rate:
                self.infected_day = self.model.current_day
    
    def end_day(self):
        self.interactions = []