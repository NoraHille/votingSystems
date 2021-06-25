from classes import Option, Issue, Agent
from Election import Election, initializeRandomElection, ElectionResult, makeIssue, makeRandomOptions
from Helper import Helper
from strategicVoting import computePossibilityStratVote
from Evaluation import happinessOfAgentWithResult, happinessOfAgentWithWinner


def method():
    print("HI")
    makeDimensionGraphic()



def makeDimensionGraphic():

    numDim = 5
    numOptions = 5
    numAgents = 100

    options = makeRandomOptions(numOptions, numDim)

    issue = makeIssue(options, numDim)
    agents = issue.getRandomAgents(numAgents)

    for i in range(numDim):
        print("Runde", i)
        for op in options:
            op.setCoordinates(op.coordinates[:numDim-i])
        newIssue = makeIssue(options, numDim-i)
        for ag in agents:
            ag.setCoordinates(ag.coordinates[:numDim-i])
            ag.setIssue(newIssue)
        election = Election(newIssue, agents)
        election.print_result_table("Dimension " + str(numDim-i))

        if(i == numDim-1):
            for op in options:
                print(op.coordinates)
            for ag in agents:
                print(ag.coordinates)


if __name__ == '__main__':
    method()