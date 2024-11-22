import mesa
import names
from utils import State, find_grid_dimensions, generate_traits
from agent import Agent

class Model(mesa.Model):
    def __init__(
        self, 
        population = 3,
        initial_infected = 1,
        max_interactions = 5,
        infection_rate = 0.1,
        seed=None
    ):
        super().__init__(seed=seed)

        # Model Constants
        self.population = population
        self.initial_infected = initial_infected
        self.max_interactions = max_interactions
        self.infection_rate = infection_rate
        self.time_to_heal = 6
        self.infection_severity = [0, 0, 1, 2, 2, 1]
        self.infection_visible = 4

        # Model State
        self.current_day = 1
        self.agents_visible = []
        self.agents_outside = []

        width, height = find_grid_dimensions(self.population)
        self.grid = mesa.space.SingleGrid(width, height, torus=True)
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Susceptible": lambda model: sum([1 for a in model.agents if a.state == State.SUSCEPTIBLE]),
                "Infected": lambda model: sum([1 for a in model.agents if a.state == State.INFECTED]),
                "Recovered": lambda model : sum([1 for a in model.agents if a.state == State.RECOVERED]),
            },
            agent_reporters={
                "Decision": "decision"
            },
        )

        for i in range(self.population):
            a = Agent(
                self,
                name = names.get_first_name(),
                age = self.random.randrange(18,65),
                traits = generate_traits(self.random),
                infected = i < self.initial_infected
            )
            self.grid.place_agent(a, (i%width, i//width))

        self.datacollector.collect(self)
    
    def step(self):
        self.agents.do("check_infection_visible")
        self.agents.do("decide_location")
        self.agents.shuffle_do("make_interactions")
        self.agents.do("end_day")
        self.datacollector.collect(self)
        self.agents_visible = []
        self.agents_outside = []
        self.current_day += 1