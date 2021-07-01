import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import copy
import math
from time import time



from classes import Option, Issue, Agent, dimensionSize, colormap, alphabet_list
from Evaluation import happinessOfAgentWithResult, distanceOfAgentToResult, distanceOfAgentToWinner, \
    preferanceOfAgentOfWinner
from Helper import  Helper
from Election import Election, initializeRandomElection, initializeElection
from exampleElections import make_small_Election_1, make_Election_1, make_strat_Election_1, make_strat_Election_2, make_app_strat_Election, make_small_Election_3
from incompleteKnowledgeStratVoting import distanceWithPositionInRandomFilledElection, getOtherAgentsForStratVote
from exampleElections import make_small_Elec_with_3_options

def method():
    print("HI")
    differentBallotsStratVote()

def differentBallotsStratVote():

    election = make_small_Elec_with_3_options()

    agent = election.agents[0]

    base_dist = distanceWithBallotInRandomFilledElection(agent, election.issue, 3, agent.pm)
    sortPM = Helper.sortDictDescending(agent.pm)
    newPM = Helper.getEmptyDict(list(agent.pm.keys()))
    newPM[list(sortPM.keys())[0]] = 1
    new_dist = distanceWithBallotInRandomFilledElection(agent, election.issue, 3, newPM)
    print(base_dist)
    print(new_dist)





def distanceWithBallotInAllPosFilledElection(agent: Agent, issue: Issue, numOtherAgents, ballot, kind="WR", doWholeResult=False):
    numRounds = 81**numOtherAgents #We seperate the field into 81 distinct positions for the other agents.
    totalDistance = 0
    for i in range(numRounds):
        agents = getOtherAgentsForStratVote(i, issue)
        agentsVote = copy.deepcopy(agent)
        agentsVote.setPM(ballot)
        agents.append(agentsVote)

        election = Election(issue, agents)

        # if(i%125 ==0):
        #     print(i)
        #     election.print_election_plot(highlightAgent=3)
        result = election.computeBallotResult(kind)
        # how much does the agent like the result?
        if(doWholeResult):
            totalDistance += distanceOfAgentToResult(agent, result)
        else:
            totalDistance += preferanceOfAgentOfWinner(agent, result)
    totalDistance /= numRounds
    return totalDistance





















if __name__ == '__main__':

    method()