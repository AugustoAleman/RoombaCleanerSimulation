'''
* agent.py
* By: Octavio Augusto Aleman Esparza
* 11/07/2022
'''
from mesa import Agent

#Class that contains the model's Agents
#Vacuum cleaners and Dirt Spots are represented by the same type of agent, although they differ on tasks
class RoombaAgent(Agent):

    #Class initializer
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        if self.unique_id < 10:
            self.value = 2 #If agent is Roomba
        else:
            self.value = 1 #If agent is dirt spot

    def step(self) -> None:
        if self.unique_id < 10: #Only cleaner agents are able to move
            self.clean() #Call to clean() method

    def clean(self): #Method that checks wether a box is dirty
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1: #If a box contains an agent in addition to one cleaner
            other = cellmates[0]
            if(other.value == 1): #If said agent is a dirt spot that hasn't been cleaned
                other.value = 0

        self.move() #Move the cleaner wether a box has been cleaned or not

    def move(self) -> None: #Method that moves a cleaner to some neighbouring box
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
