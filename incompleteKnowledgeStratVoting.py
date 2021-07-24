import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import copy
import math
from time import time



from classes import Option, Issue, Agent, dimensionSize, colormap, alphabet_list, makeRandomOptions, \
    makeRandomCoordinates
from Evaluation import  happinessOfAgentWithResult, distanceOfAgentToResult, distanceOfAgentToWinner, preferanceOfAgentOfWinner
from Helper import  Helper
from Election import Election, initializeRandomElection, initializeElection
from exampleElections import make_small_Election_1, make_Election_1, make_strat_Election_1, make_strat_Election_2, make_app_strat_Election, make_small_Election_3

posDict = {0: -80, 1: -60, 2: -40, 3: -20, 4: 0, 5:20, 6:40, 7:60, 8:80}





def method():
    print("HI")

    StatOnIncomKnowStratVote(10000)


# This method runs through a bunch of elections and sees if there is the possibilty to do strat vote within the coord system. If there isn't it sees if that changed when we allow any ballot.

def StatOnIncomKnowStratVote(rounds):

    """ This function initializes an election with 5 random options and one agent.
    It than tries to find the optimal position (within the grid) for that agent (the position that brings them the higest happiness).
    It does that by using the original position as well as all the positions on top of each of the options
    and always trying out the mean of the current two best positions next. After doing this with rounds elections
     it returns where the optimal positions were and whether any position that was not on an option could be improved by allowing the agent any ballot"""


    numOtherAgents = 3
    kinds = ["WR", "WAR"]
    winningOptionNum = Helper.getEmptyDict(kinds)
    anotherOptionNum = Helper.getEmptyDict(kinds)
    switchToOptionNum = Helper.getEmptyDict(kinds)
    origPosNum = Helper.getEmptyDict(kinds)
    otherPosNum = Helper.getEmptyDict(kinds)
    WinOrigNum = Helper.getEmptyDict(kinds)
    WinOpNum = Helper.getEmptyDict(kinds)
    OrigOpNum = Helper.getEmptyDict(kinds)
    OpOpNum = Helper.getEmptyDict(kinds)
    BallotChangeToWin = Helper.getEmptyDict(kinds)
    BallotChangeToOtherOp = Helper.getEmptyDict(kinds)




    for i in range(rounds):



        options = makeRandomOptions(2, 5)
        issue = Issue(options, ["dim1", "dim2"])


        agent = Agent(makeRandomCoordinates(2), issue)
        for kind in kinds:
            [bestCoord, origCorner1, secondBestCoord, origCorner2, baseDistance, bestDistance] = sampleUnknowingStrategic(agent, issue, numOtherAgents, kind=kind)

            opWasACorner = False
            origWasACorner = False
            winWasACorner = False
            OpOp = False
            posFound = False
            switchToOption = False
            if(bestCoord == agent.coordinates):
                origPosNum[kind] += 1

            else:
                for op in options:
                    if(bestCoord == op.coordinates):
                        if(op.name in Helper.getWinner(agent.pm)):
                            winningOptionNum[kind]+=1
                            switchToOption = True
                            posFound =True
                            break
                        else:
                            anotherOptionNum[kind] += 1
                            switchToOption = True
                            posFound = True
                            break
                    if (origCorner2 == op.coordinates or origCorner1 == op.coordinates):
                        if(op.name in Helper.getWinner(agent.pm)):
                            winWasACorner = True
                        else:
                            if(opWasACorner):
                                OpOp = True
                            else:
                                opWasACorner = True

                if (origCorner2 == agent.coordinates or origCorner1 == agent.coordinates):
                    origWasACorner = True
                if(not posFound):
                    if(opWasACorner and winWasACorner):
                        WinOpNum[kind]+=1
                    if(winWasACorner and origWasACorner):
                        WinOrigNum[kind]+=1
                    if(opWasACorner and origWasACorner):
                        OrigOpNum[kind]+=1
                    if(OpOp):
                        OpOpNum[kind] += 1
                    otherPosNum[kind] += 1
                    changed = False

            if(not switchToOption):
                for op in options:
                    ballot = makeBallotForChangeVote(agent, op.name, kind=kind)
                    dist = distanceWithBallotInRandomFilledElection(agent, issue, numOtherAgents, ballot, kind=kind)
                    if(dist < bestDistance):
                        bestDistance = dist
                        bestOp = op
                        changed = True

                if(changed):
                    if bestOp.name in Helper.getWinner(agent.pm)[0]:
                        BallotChangeToWin[kind] += 1
                    else:
                        BallotChangeToOtherOp[kind] += 1
            else:
                switchToOptionNum[kind] += 1







    for kind in kinds:
        print(kind, "switch to Option:", winningOptionNum[kind], anotherOptionNum[kind], switchToOptionNum[kind],
              "other pos: ", origPosNum[kind], otherPosNum[kind], "distribution of other posses: ", WinOrigNum[kind],
              OrigOpNum[kind], WinOpNum[kind], OpOpNum[kind], "ballot changes:", BallotChangeToWin[kind],
              BallotChangeToOtherOp[kind])

        print("-------------------------------------------------------------------------------------------------------------")

        print("In {} there were a total of {} switches exactly on top of an option. {} ({} %) of them to the winner and {} ({} %)to another one. {} ({} % of cases) remained at their original position, while {} ({} %) found a new Position. {} + {} + {} + {}".format(kind, switchToOptionNum[kind], winningOptionNum[kind], winningOptionNum[kind]/switchToOptionNum[kind] * 100, anotherOptionNum[kind], anotherOptionNum[kind]/switchToOptionNum[kind] * 100, origPosNum[kind], origPosNum[kind]/rounds* 100, otherPosNum[kind], otherPosNum[kind]/rounds* 100,WinOrigNum[kind], OrigOpNum[kind], WinOpNum[kind], OpOpNum[kind]))
        print("The new positions lay between the winner and orig {} % of time, between another option and orig {} % of the time, between the winner and another option {} % of the time and between two option {} % of the time.".format(WinOrigNum[kind]/otherPosNum[kind]* 100,OrigOpNum[kind]/otherPosNum[kind]* 100, WinOpNum[kind]/otherPosNum[kind]* 100, OpOpNum[kind]/otherPosNum[kind]* 100))
        print("Of the {} times the optimal position was not on an option, we could place the optimal position on the winner {} times ({} %) and on another option {} times ({} %) through ballot voting.".format(origPosNum[kind] + otherPosNum[kind],  BallotChangeToWin[kind],  BallotChangeToWin[kind]/(origPosNum[kind] + otherPosNum[kind])* 100, BallotChangeToOtherOp[kind],  BallotChangeToOtherOp[kind]/(origPosNum[kind] + otherPosNum[kind])* 100))

        print("-------------------------------------------------------------------------------------------------------------")

def makeBallotForChangeVote(agent, opName, kind="WR"):

    ballot = Helper.getEmptyDict(list(agent.pm.keys()))
    sortPM = Helper.sortDictDescending(agent.pm)
    for opname in sortPM.keys():
        if (opname == opName):
            ballot[opname] = 1
            break
        if(kind=="WAR"):
            ballot[opname] = 1

    return ballot


def distanceWithBallotInRandomFilledElection(agent: Agent, issue: Issue, numOtherAgents, ballot, kind="WR", doWholeResult=False):
    numRounds = 10000
    totalDistance = 0
    for i in range(numRounds):
        agents = issue.getRandomAgents(numOtherAgents)
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
            totalDistance += 1- preferanceOfAgentOfWinner(agent, result)
    totalDistance /= numRounds
    return totalDistance




def sampleUnknowingStrategic(agent: Agent, issue: Issue, numOtherAgents, kind="WR", doWholeResult=False, output=False):


    #set agent on a random extreme position
    #compute Happiness
    # if lower than normal position
    #break
    # if higher than normal position
    #set agent on midpoint between normal pos and extreme

    baseDistance = distanceWithPositionInRandomFilledElection(agent, issue, numOtherAgents, agent.coordinates, kind=kind, doWholeResult=doWholeResult)
    if(output):
        print("Basis: {}".format(baseDistance))

    bestDistance = baseDistance
    secondBestDistance = 0
    bestCoord = agent.coordinates
    secondBestCoord = agent.coordinates

    firstBreak = True

    origCorner1 = []
    origCorner2 = []


    breakCoord = [-1000, -1000]


    coordinatesToTry = [op.coordinates for op in issue.options]
    coordinatesToTry.append(breakCoord)

    counter = 20

    for coord in coordinatesToTry:
        counter -= 1

        if (output):
            print("rounds left: ", counter, coordinatesToTry)


        if(counter< 0):

            if (output):
                print("I will now end this, because my rounds are up.")
            break

        if(coord == breakCoord):
            if(firstBreak):
                origCorner1 = bestCoord
                origCorner2 = secondBestCoord
                firstBreak =False
            newCoords = calculateMiddlePosition(bestCoord, secondBestCoord)
            if (output):
                print("from {} and {} I make {}".format(bestCoord, secondBestCoord, newCoords))
            if(newCoords not in coordinatesToTry):
                coordinatesToTry.append(newCoords)
                coordinatesToTry.append(breakCoord)
            else:
                if (output):
                    print("I will now end this, because we have seen ", newCoords, "before!")
                break
            continue

        distance = distanceWithPositionInRandomFilledElection(agent, issue, numOtherAgents, coord, kind=kind)

        if(distance<bestDistance):
            if (output):
                print("{} is a better position and gives me {} distance".format(coord, distance))
            secondBestDistance = bestDistance
            secondBestCoord = bestCoord
            bestDistance = distance
            bestCoord = coord
        else:
            if(output):
                print("{} is not a better position and gives me {} distance".format(coord, distance))
            if (distance < secondBestDistance):
                if (output):
                    print("New second best!!!!!")
                secondBestDistance = distance
                secondBestCoord = coord

    return [bestCoord, origCorner1, secondBestCoord, origCorner2, baseDistance, bestDistance]




def calculateMiddlePosition(co1,co2):
    if(len(co1)!= len(co2)):
        print("calculateMiddlePosition: the two coordinates weren't the same length")
    middle = []
    for i in range(len(co1)):
        middle.append(min(co1[i],co2[i]) + (max(co1[i], co2[i]) - min(co1[i],co2[i]))/2)
    return middle




def distanceWithPositionInRandomFilledElection(agent: Agent, issue: Issue, numOtherAgents, position, kind="WR", doWholeResult=False):
    # numRounds = 81**numOtherAgents #We seperate the field into 81 distinct positions for the other agents.
    numRounds = 100
    totalDistance = 0
    for i in range(numRounds):
        # agents = getOtherAgentsForStratVote(i, issue)
        agents = issue.getRandomAgents(numOtherAgents)
        agentsVote = copy.deepcopy(agent)
        agentsVote.setCoordinates(position)
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
            totalDistance += 1- preferanceOfAgentOfWinner(agent, result)
    totalDistance /= numRounds
    return totalDistance

def getOtherAgentsForStratVote(round: int, issue):
    [firstpos, secpos, thirdpos] = getOtherAgentsNumForStratVote(round)

    return [Agent(getCoordinatesFromNum(firstpos), issue),Agent(getCoordinatesFromNum(secpos), issue),Agent(getCoordinatesFromNum(thirdpos), issue),]



def getOtherAgentsNumForStratVote(round: int):


    firstpos = round%81
    thirdpos = int(round/6561)
    secpos = int((round - thirdpos*6561)/81)

    return [firstpos, secpos, thirdpos]





def getCoordinatesFromNum(num: int):

    if(num >= 81 or num < 0):
        print("Number in getPositionsOfOtherAgents hat the wrong size.")
    firstnum = num%9
    secondnum = math.floor(num/9)

    return [posDict[firstnum], posDict[secondnum]]

def incompleteKnowledgeWith5ExampleElecs():

    results = []

    op1 = Option([50, 50])
    op2 = Option([-50, -80])
    op3 = Option([-60, -70])

    issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
    agent = Agent([40,40], issue1)

    results.append((1, "WR", sampleUnknowingStrategic(agent, issue1, 3)))
    results.append((1, "WAR",sampleUnknowingStrategic(agent, issue1, 3, kind="WAR")))
    results.append((1, "WR-whole", sampleUnknowingStrategic(agent, issue1, 3, doWholeResult=True)))
    results.append((1, "WAR-whole", sampleUnknowingStrategic(agent, issue1, 3, kind="WAR", doWholeResult=True)))
    election = Election(issue1, [agent])
    election.print_election_plot()

    op1 = Option([90, 90])
    op2 = Option([20, 20])
    op3 = Option([-90, -90])

    issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
    agent = Agent([80, 80], issue1)

    results.append((2, "WR", sampleUnknowingStrategic(agent, issue1, 3)))
    results.append((2, "WAR", sampleUnknowingStrategic(agent, issue1, 3, kind="WAR")))
    results.append((2, "WR-whole", sampleUnknowingStrategic(agent, issue1, 3, doWholeResult=True)))
    results.append((2, "WAR-whole", sampleUnknowingStrategic(agent, issue1, 3, kind="WAR", doWholeResult=True)))
    election = Election(issue1, [agent])
    election.print_election_plot()

    op1 = Option([90, 90])
    op2 = Option([20, 20])
    op3 = Option([-90, -90])

    issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
    agent = Agent([60, 60], issue1)

    results.append((3, "WR", sampleUnknowingStrategic(agent, issue1, 3)))
    results.append((3, "WAR", sampleUnknowingStrategic(agent, issue1, 3, kind="WAR")))
    results.append((3, "WR-whole", sampleUnknowingStrategic(agent, issue1, 3, doWholeResult=True)))
    results.append((3, "WAR-whole", sampleUnknowingStrategic(agent, issue1, 3, kind="WAR", doWholeResult=True)))
    election = Election(issue1, [agent])
    election.print_election_plot()

    op1 = Option([90, 90])
    op2 = Option([-20, -20])
    op3 = Option([70, 90])

    issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
    agent = Agent([60, 60], issue1)

    results.append((4, "WR", sampleUnknowingStrategic(agent, issue1, 3)))
    results.append((4, "WAR", sampleUnknowingStrategic(agent, issue1, 3, kind="WAR")))
    results.append((4, "WR-whole", sampleUnknowingStrategic(agent, issue1, 3, doWholeResult=True)))
    results.append((4, "WAR-whole", sampleUnknowingStrategic(agent, issue1, 3, kind="WAR", doWholeResult=True)))
    election = Election(issue1, [agent])
    election.print_election_plot()

    op1 = Option([90, 90])
    op2 = Option([-20, -20])
    op3 = Option([45, 90])

    issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
    agent = Agent([70, 90], issue1)

    results.append((5, "WR", sampleUnknowingStrategic(agent, issue1, 3)))
    results.append((5, "WAR", sampleUnknowingStrategic(agent, issue1, 3, kind="WAR")))
    results.append((5, "WR-whole", sampleUnknowingStrategic(agent, issue1, 3, doWholeResult=True)))
    results.append((5, "WAR-whole", sampleUnknowingStrategic(agent, issue1, 3, kind="WAR", doWholeResult=True)))
    election = Election(issue1, [agent])
    election.print_election_plot()


    for index, kind, res in results:
        print("Election {}, {}: bestCoord: {}, bestDistance: {}, sndBestCoord: {}, sndBestDist: {}, baseDist{}".format(index, kind,
            res[0], res[1], res[2], res[3], res[4]))






if __name__ == '__main__':

    method()