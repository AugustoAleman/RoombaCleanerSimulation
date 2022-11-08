'''
* model.py
* By: Octavio Augusto Aleman Esparza
* 11/07/2022
'''
from mesa import Model
from agent import RoombaAgent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

#Class that represents the Model's ambient
class RoombaModel(Model):

    def __init__(self, number_of_vacuums, number_of_agents, number_of_max_steps, width, height): #Initializer Method
        self.num_agents = number_of_agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        self.datacollector_currents = DataCollector( #Data collector for the Dirty vs Clean Agents Graph
            {
                "Dirty Agents": RoombaModel.current_dirty_agents,
                "Clean Agents": RoombaModel.current_clean_agents,
            }
        )

        self.datacollector_currents_percentage_clean = DataCollector( #Data collector for the Clean Percentage Graph
            {
                "Percentage Clean Agents (%)": RoombaModel.percentage_current_clean_agents,
            }
        )

        coor = [[0, 0]] #List of used coordinates

        for i in range(number_of_vacuums): #Initializing of vacuum cleaners
            a = RoombaAgent(i, self)
            self.schedule.add(a)

            self.grid.place_agent(a, (0, 0))
            
            coor.append([0, 0])
            self.grid.place_agent(a, (0, 0))

        for i in range(number_of_agents): #Initializing of dirt spots
            a = RoombaAgent(i + 10, self)
            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            curr = [x, y]

            while(True): #While a coordinate is already in use by another agent
                coorExists = False
                for j in range(len(coor)):
                    if(curr == coor[j]):
                        coorExists = True
                if(coorExists or curr == [0, 0]):
                    x = self.random.randrange(self.grid.width)
                    y = self.random.randrange(self.grid.height)
                    curr = [x, y]
                else:
                    break

            coor.append(curr)
            self.grid.place_agent(a, (x, y))

        #Global variables that are recquired by other methods
        global I
        global MAX_STEPS #Max. quantity of allowed steps
        global AGENTS  #Number of dirt and cleaned agents
        global VACUUMS #Number of vacuum agents
        I = 0

        MAX_STEPS = number_of_max_steps
        AGENTS = number_of_agents
        VACUUMS = number_of_vacuums

    
    def step(self):
        self.schedule.step()
        self.datacollector_currents.collect(self)
        self.datacollector_currents_percentage_clean.collect(self)
        global I
        global MAX_STEPS 
        
        if(RoombaModel.current_dirty_agents(self) < 1 or I == MAX_STEPS - 2): #If there aren't any more dirt spots or the max time has been reached.
            self.running = False #Stop Simulation

        I += 1
    
    @staticmethod
    def current_dirty_agents(model) -> int: #MEthod that returns amount of dirt spots
        return(sum([1 for agent in model.schedule.agents if agent.value == 1]))

    @staticmethod
    def current_clean_agents(model) -> int: #MEthod that returns amount of cleaned spots
        return(sum([1 for agent in model.schedule.agents if agent.value == 0]))

    @staticmethod
    def percentage_current_clean_agents(model) -> int: #MEthod that returns percentage of cleaned spots
        global AGENTS
        return(int((sum([1 for agent in model.schedule.agents if agent.value == 0])) * 100) / AGENTS)

    def get_clean_percentage(model):
        return f"Percentage of cleaned agents: {(int((sum([1 for agent in model.schedule.agents if agent.value == 0])) * 100) / AGENTS):.2f} %"

    def get_total_movements(model):
        return f"Total combined movements of Roomba Cleaners: {((I + 2) * VACUUMS) - VACUUMS}"

        #outlier
        #estocastico
        #% celdas limpias vs movimientos