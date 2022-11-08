'''
* server.py
* By: Octavio Augusto Aleman Esparza
* 11/07/2022
'''
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import RoombaModel

NUMBER_OF_CELLS = 10
SIZE_OF_CANVAS_X = 500
SIZE_OF_CANVAS_Y = 500 

simulation_params = { #Parameters given by the user recquired for the initialization of the model
    "number_of_vacuums" : UserSettableParameter( #Total allowed vacuums
        "slider",
        "Number of Roombas",
        1, #default
        1, #min
        10, #max
        1, #step
        description = "No. de agentes de limpieza (aspiradoras) a simular."
    ),
    "number_of_agents" : UserSettableParameter( #Total allowed dirt spots
        "slider",
        "Number of Dirty Spots",
        50, #default
        10, #min
        99, #max
        1, #step
        description = "No. de agentes (casillas con suciedad) a simular."
    ),
    "number_of_max_steps" : UserSettableParameter( #Total allowed Time
        "slider",
        "Max Time (in Steps as Seconds)",
        50, #default
        10, #min
        100, #max
        1, #step
        description = "Tiempo maximo de simulacion, dado por el no. maximo de pasos por agente."
    ),

    "width": NUMBER_OF_CELLS,
    "height": NUMBER_OF_CELLS,
}

def agent_portrayal(agent): #A color is assigned to each type of agent
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.5}

    if agent.value == 2:
        portrayal["Color"] = "black"
        portrayal["Layer"] = 2
    elif agent.value == 1:
        portrayal["Color"] = "brown"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.25
    else:
        portrayal["Color"] = "white"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.25
    return portrayal

grid = CanvasGrid(agent_portrayal, NUMBER_OF_CELLS, NUMBER_OF_CELLS, SIZE_OF_CANVAS_X, SIZE_OF_CANVAS_Y) #Init. of visual model

chart_currents = ChartModule(#Graph Dirty vs Cleaned Spots
    [
        {"Label": "Dirty Agents", "Color": "brown"},
        {"Label": "Clean Agents", "Color": "teal"},
    ],
    canvas_height=300,
    data_collector_name = "datacollector_currents"
)

chart_currents1 = ChartModule( #Graph Percentage of cleaned spots
    [
        {"Label": "Percentage Clean Agents (%)", "Color": "green"},
    ],
    canvas_height=300,
    data_collector_name = "datacollector_currents_percentage_clean"
)

server = ModularServer(RoombaModel,
                        [grid, RoombaModel.get_clean_percentage, RoombaModel.get_total_movements, chart_currents, chart_currents1],
                        "Roomba Model",
                        simulation_params)
server.port = 8522
server.launch()