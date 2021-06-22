

import numpy as np
from classes import ElectionResult
from Election import Election, initializeRandomElection
from agent import Agent
from Helper import Helper




def method():
    print("HI")
    makeAHappinessPlot()



def makeAHappinessPlot():

    election = initializeRandomElection(5,200,2)
    for eval in ["dist", "sqdist", "hap", "hww", "hw"]:
        print(eval)
        for kind in ["WR", "WAR", "AV", "RC", "PL", "WLR", "WALR"]:
            result = election.computeBallotResult(kind)

            print(kind, computeHappinessWithResult(election, result, kind=eval))
        print("-----------------------------")
    for kind in ["WR", "WAR", "AV", "RC", "PL", "WLR", "WALR"]:
        result = election.computeBallotResult(kind)
        print(kind, computeVarianceOfHappiness(election, result))



def computeHappinessWithResult(election: Election, result: ElectionResult, kind="dist")-> float:

    totalHappiness = 0

    for agent in election.agents:
        if(kind =="dist"):
            totalHappiness += distanceOfAgentToResult(agent, result)
        if (kind == "hap"):
            totalHappiness += happinessOfAgentWithResult(agent, result)
        if (kind == "hww"):
            totalHappiness += happinessOfAgentWithWinnerWeighted(agent, result)
        if (kind == "hw"):
            totalHappiness += happinessOfAgentWithWinner(agent, result)
        if (kind == "sqdist"):
            totalHappiness += squaredDistanceOfAgentToResult(agent, result)

    return totalHappiness

def computeVarianceOfHappiness(election: Election, result: ElectionResult)-> float:

    mu = computeHappinessWithResult(election, result)/len(election.agents)

    variance = 0

    for agent in election.agents:
        variance += (happinessOfAgentWithResult(agent, result)-mu)**2

    return variance



def happinessOfAgentWithResult(agent: Agent, result: ElectionResult)-> float:
    PM = agent.pm
    happiness = 0
    for op_name in PM.keys():
        happiness += PM[op_name]*result.normalizedRanking[op_name]

    return happiness

def distanceOfAgentToResult(agent: Agent, result: ElectionResult)-> float:
    PM = agent.pm
    distance = 0
    for op_name in PM.keys():
        distance += abs(PM[op_name]-result.normalizedRanking[op_name])

    return distance

def squaredDistanceOfAgentToResult(agent: Agent, result: ElectionResult)-> float:
    PM = agent.pm
    distance = 0
    for op_name in PM.keys():
        distance += (PM[op_name]-result.normalizedRanking[op_name])**2

    return distance

def happinessOfAgentWithWinner(agent: Agent, result: ElectionResult)-> float:
    PM = agent.pm
    winners = Helper.getWinner(result.normalizedRanking)
    happiness = 0
    for op_name in winners:
        happiness += PM[op_name]

    return happiness/len(winners)

def happinessOfAgentWithWinnerWeighted(agent: Agent, result: ElectionResult)-> float:
    PM = agent.pm
    winners = Helper.getWinner(result.normalizedRanking)
    happiness = 0
    for op_name in winners:
        happiness += PM[op_name]*result.normalizedRanking[op_name]

    return happiness/len(winners)

































if __name__ == '__main__':

    method()