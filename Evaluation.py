

import numpy as np
from classes import ElectionResult, Election, happinessOfAgentWithResult, initializeRandomElection, happinessOfAgentWithWinner, happinessOfAgentWithWinnerWeighted



def method():
    print("HI")
    makeAHappinessPlot()



def makeAHappinessPlot():

    election = initializeRandomElection(5,200,2)
    for kind in ["WR", "WAR", "AV", "RC", "PL", "WLR", "WALR"]:
        result = election.computeResult(kind)
        print(kind, computeVarianceOfHappiness(election, result))


def computeHappinessWithResult(election: Election, result: ElectionResult)-> float:

    totalHappiness = 0

    for agent in election.agents:
        totalHappiness += happinessOfAgentWithResult(agent, result)

    return totalHappiness

def computeVarianceOfHappiness(election: Election, result: ElectionResult)-> float:

    mu = computeHappinessWithResult(election, result)/len(election.agents)

    variance = 0

    for agent in election.agents:
        variance += (happinessOfAgentWithResult(agent, result)-mu)**2

    return variance



































if __name__ == '__main__':

    method()