from Helper import Helper
import numpy as np
import string
import random
import math
import copy


class AgentBlock(object):

    def __init__(self, agent, agentNum):
        self.agents = []
        for i in range(agentNum):
            self.agents.append(copy.deepcopy(agent))
        self.agent = agent
        self.agentNum = agentNum

    def changeCoordinates(self, newCoordinates):

        if(len(newCoordinates) != len(self.agent.coordinates)):
            print("wrong coordinates!")
        else:
            for ag in self.agents:
                ag.setCoordinates(newCoordinates)


