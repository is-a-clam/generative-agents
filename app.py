from mesa.visualization import SolaraViz, Slider, make_plot_component, make_space_component
from utils import State
from model import Model

def agent_portrayal(agent):
    node_color_dict = {
        State.INFECTED: "tab:red",
        State.SUSCEPTIBLE: "tab:green",
        State.RECOVERED: "tab:gray",
    }
    return {"color": node_color_dict[agent.state], "size": 10}

def post_process_lineplot(ax):
    ax.set_ylim(ymin=0)
    ax.set_ylabel("# people")
    ax.legend(bbox_to_anchor=(1.05, 1.0), loc="upper left")

model_params = {
    "population": Slider(
        label="Population",
        value=3,
        min=1,
        max=100,
        step=1,
    ),
    "initial_infected": Slider(
        label="Initial infected",
        value=1,
        min=1,
        max=100,
        step=1,
    ),
    "max_interactions": Slider(
        label="Contact Rate",
        value=5,
        min=1,
        max=10,
        step=1,
    ),
    "infection_rate": Slider(
        label="Infection Rate",
        value=0.1,
        min=0.1,
        max=1.0,
        step=0.05,
    ),
}

model = Model()
AgentPlot = make_space_component(agent_portrayal)
SIRPlot = make_plot_component(
    {"Susceptible": "tab:green", "Infected": "tab:red", "Recovered": "tab:gray"},
    post_process=post_process_lineplot,
)

page = SolaraViz(
    model=model,
    components=[AgentPlot, SIRPlot],
    model_params=model_params,
    name="Epidemic Modelling with Generative Agents",
)

