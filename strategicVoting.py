

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import copy
import math
from time import time



from classes import Option, Issue, Agent, dimensionSize, colormap, alphabet_list
from Evaluation import  happinessOfAgentWithResult, distanceOfAgentToResult, distanceOfAgentToWinner
from Helper import  Helper
from Election import Election, initializeRandomElection, initializeElection
from exampleElections import make_small_Election_1, make_Election_1, make_strat_Election_1, make_strat_Election_2, make_app_strat_Election



posDict = {0: -80, 1: -60, 2: -40, 3: -20, 4: 0, 5:20, 6:40, 7:60, 8:80}

#TODO
#Methode die für eine Wahl und ein System berechnet wie viele Agenten/Optionen Paare es gibt, die mit strategischem Wählen besser fahren als ohne
# -> Diese Zahl als Bruchteil der (A,O) Paare insgesamt kann verglichen werden.
# -> Jede der Zahlen mal die Glückssetigerung des A kann verglichen werden.









def method():
    print("HI")
    # generateStrategicChangeVoting(kind="RC", numOptions=5, numAgents=3, iter=1000)

    stratVotPosStats()






# Change voting with Plurality leads to sooooo many ties it is really annoying


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

def sampleUnknowingStrategic(agent: Agent, issue: Issue, numOtherAgents, kind="WR", doWholeResult=False):


    #set agent on a random extreme position
    #compute Happiness
    # if lower than normal position
    #break
    # if higher than normal position
    #set agent on midpoint between normal pos and extreme

    baseDistance = distanceWithPositionInRandomFilledElection(agent, issue, numOtherAgents, agent.coordinates, kind=kind, doWholeResult=doWholeResult)
    print("Basis: {}".format(baseDistance))

    bestDistance = baseDistance
    secondBestDistance = 0
    bestCoord = agent.coordinates
    secondBestCoord = agent.coordinates


    breakCoord = [-1000, -1000]


    coordinatesToTry = [op.coordinates for op in issue.options]
    coordinatesToTry.append(breakCoord)

    counter = 20

    for coord in coordinatesToTry:
        counter -= 1

        print("rounds left: ", counter, coordinatesToTry)


        if(counter< 0):
            print("I will now end this, because my rounds are up.")
            break

        if(coord == breakCoord):
            newCoords = calculateMiddlePosition(bestCoord, secondBestCoord)
            print("from {} and {} I make {}".format(bestCoord, secondBestCoord, newCoords))
            if(newCoords not in coordinatesToTry):
                coordinatesToTry.append(newCoords)
                coordinatesToTry.append(breakCoord)
            else:
                print("I will now end this, because we have seen ", newCoords, "before!")
                break
            continue




        distance = distanceWithPositionInRandomFilledElection(agent, issue, numOtherAgents, coord, kind=kind)
        if(distance<bestDistance):
            print("{} is a better position and gives me {} distance".format(coord, distance))
        else:
            print("{} is not a better position and gives me {} distance".format(coord, distance))
        if(distance<bestDistance):
            secondBestDistance = bestDistance
            secondBestCoord = bestCoord
            bestDistance = distance
            bestCoord = coord
        else:
            if (distance < secondBestDistance):
                print("New second best!!!!!")
                secondBestDistance = distance
                secondBestCoord = coord

    return [bestCoord, bestDistance, secondBestCoord, secondBestDistance, baseDistance]




def calculateMiddlePosition(co1,co2):
    if(len(co1)!= len(co2)):
        print("calculateMiddlePosition: the two coordinates weren't the same length")
    middle = []
    for i in range(len(co1)):
        middle.append(min(co1[i],co2[i]) + (max(co1[i], co2[i]) - min(co1[i],co2[i]))/2)
    return middle




def distanceWithPositionInRandomFilledElection(agent: Agent, issue: Issue, numOtherAgents, position, kind="WR", doWholeResult=False):
    numRounds = 81**numOtherAgents #We seperate the field into 81 distinct positions for the other agents.
    totalDistance = 0
    for i in range(numRounds):
        agents = getOtherAgentsForStratVote(i, issue)
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
            totalDistance += distanceOfAgentToWinner(agent, result)
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

def stratVotPosStats(rounds=1000):
    numAg = 20
    numOp = 5

    resultDict = {}
    for i in range(rounds):
        election = initializeRandomElection(numOp, numAg, 2)
        newDict = computeStratVotPosForAll(election)
        for (kind, dicti) in newDict.items():
            if( kind not in resultDict):
                resultDict[kind] = {"Over voters": 0, "Change voters": 0, "failed": 0, "didn't try": 0}
            for k, value in dicti.items():
                resultDict[kind][k] += value
    total = numOp*numAg*rounds
    for kind, dicti in resultDict.items():
        innerTotal = dicti["failed"] + dicti["Change voters"] + dicti["Over voters"] + dicti["didn't try"]
        if(innerTotal != total):
            print("total {} and innerTotal {} don't match in StatVotPosStats!".format(total, innerTotal))
        totalAttemps = dicti["failed"] + dicti["Change voters"] + dicti["Over voters"]
        attemptRate = totalAttemps/total
        failed = dicti["failed"]/totalAttemps * 100
        change = dicti["Change voters"]/totalAttemps * 100
        over = dicti["Over voters"]/totalAttemps * 100

        print("In {} unhappy voters failed {} %, overvoted {} % and changevoted {} % of the time. Attemptrate = {}. Nr of attemps: {}".format(kind, failed, over, change, attemptRate, totalAttemps))





def computeStratVotPosForAll(election=None):
    if(election==None):
        election = initializeRandomElection(5, 4, 2)
    dicti= {}
    for kind in ["AV", "WR", "WAR", "RC", "PL"]:
        # for kind in ["WR"]:
        stratPos = computePossibilityStratVote(election, kind=kind)
            # if (stratPos['Over voters:'] > 0 or goOn == False):
        dicti[kind] = stratPos
        # print(kind, stratPos)
    return dicti



def computePossibilityStratVote(election: Election, kind: str):
    result = election.computeBallotResult(kind)
    winners = Helper.getWinner(result.normalizedRanking)

    sucOverVotes = 0
    sucChangeVotes = 0
    failedStratVotes = 0
    contendet = 0

    for ag in election.agents:
        PM = ag.pm
        coordinates = ag.coordinates
        personalWinners = Helper.getWinner(PM)
        if(any(win in winners for win in personalWinners)): # Agent is already happy with the result -> no strat vote necessary
            contendet += len(election.issue.options)
            continue
        else:
            for num, op in enumerate(election.issue.options):
                if (kind == "AV"):
                    ag.setNumApp(num + 1)
                else:
                    ag.setCoordinates(op.coordinates) #The agent pretends to have this option as their prefered choice
                newResult = election.computeBallotResult(kind)
                newWinners = Helper.getWinner(newResult.normalizedRanking)
                if (any(win in newWinners for win in personalWinners)): # The Agent successfully changed the outcome of the vote to one of their favorites
                    sucOverVotes += 1
                    continue
                if(resultImproved(PM, winners, newWinners)): #The Agent could improve their happiness with the result
                    sucChangeVotes +=1
                    continue
                failedStratVotes +=1 #The Agent could not improve the result of the vote through strat voting
            ag.setCoordinates(coordinates) #We set the agent to the old coordinates
            ag.setNumApp(None)

    sumOfLogged = sucOverVotes + sucChangeVotes + failedStratVotes + contendet
    sumOfTuples = len(election.agents)* len(election.issue.options)

    if(sumOfLogged!= sumOfTuples):
        print("The number of logged votes doesn't match.")

    return {"Over voters": sucOverVotes, "Change voters":  sucChangeVotes, "failed": failedStratVotes, "didn't try":contendet}



def resultImproved(PM: dict, oldW: dict, newW: dict):


    oldHappiness = 0
    newHappiness = 0

    for win in oldW:
        oldHappiness += PM[win]
    oldHappiness = oldHappiness/len(oldW)
    for win in newW:
        newHappiness += PM[win]
    newHappiness = newHappiness/len(newW)

    return oldHappiness < newHappiness








def generateStrategicChangeVoting(kind="WR", numOptions=5, numAgents=10, iter=10000):
    highestDifference = 0
    rounds = 0
    incNum = 0
    election = initializeRandomElection(numOptions, numAgents, 2)
    bestElection = copy.deepcopy(election)

    if (numAgents == 2):
        initialValue = 0.3;
    else:
        initialValue = 1.0 / (numAgents ** 2)

    while (True):

        if (highestDifference <= initialValue):
            election = initializeRandomElection(numOptions, numAgents, 2)


        strategicAgent = election.agents[0]
        PM = strategicAgent.pm
        if (kind == "WLR" or kind == "WALR"):
            PM = strategicAgent.linearPM


        # ag = election.agents[0]

        result = election.computeResult(kind=kind)

        for opName in [op.name for op in election.issue.options]:
            initialCoordinates = strategicAgent.coordinates
            initialPM = PM

            preferredOption = opName
            personalFavorite = Helper.getWinner(PM)[0]

            if (len(Helper.getWinner(result.normalizedRanking)) > 1): #if we have a tie, we don't really want it!
                election = copy.deepcopy(bestElection)
                continue

            winningOption = Helper.getWinner(result.normalizedRanking)[0]
            if(preferredOption == personalFavorite):
                continue
            if (preferredOption == winningOption):
                continue
            if (PM[preferredOption] <= PM[winningOption]):
                continue
            initialHappiness = PM[winningOption]
            optionsByName = [o.name for o in election.issue.options]
            newCoordinates = election.issue.options[optionsByName.index(preferredOption)].coordinates
            strategicAgent.setCoordinates(newCoordinates)

            newPM = strategicAgent.pm
            if (kind == "WLR" or kind == "WALR"):
                newPM = strategicAgent.linearPM

            newResult = election.computeResult(kind=kind)
            newWinner = Helper.getWinner(newResult.normalizedRanking)[0]

            newHappiness = PM[newWinner]
            happinessIncrease = newHappiness - initialHappiness

            if (happinessIncrease > highestDifference):
                print("better time ", incNum)
                incNum += 1
                highestDifference = happinessIncrease

                bestResult = copy.deepcopy(result)
                bestInitialCoordinates = initialCoordinates
                bestInitialPM = initialPM
                bestNewResult = copy.deepcopy(newResult)
                bestNewPM = newPM
                bestElection = copy.deepcopy(election)
                bestStrategicAgentID = election.agents.index(strategicAgent)
                bestWinOp = winningOption
                bestNewWin = newWinner
                # makeStratVotingPlot(kind, bestResult, bestNewResult, bestInitialPM, bestNewPM, bestInitialCoordinates,  bestStrategicAgentID, bestElection, bestWinOp, bestPrefOp, optionsByName)

            strategicAgent.setCoordinates(initialCoordinates)

            randAgentID = random.randint(0, len(election.agents) - 1)
            newX = max(
                min(np.random.normal(election.agents[randAgentID].coordinates[0], scale=(float(dimensionSize) / 10.0)),
                    dimensionSize), -dimensionSize)
            newY = max(
                min(np.random.normal(election.agents[randAgentID].coordinates[1], scale=(float(dimensionSize) / 10.0)),
                    dimensionSize), -dimensionSize)
            election.agents[randAgentID].setCoordinates([newX, newY])

            randOptionID = random.randint(0, len(election.issue.options) - 1)
            newOX = max(min(np.random.normal(election.issue.options[randOptionID].coordinates[0],
                                             scale=(float(dimensionSize) / 10.0)), dimensionSize), -dimensionSize)
            newOY = max(min(np.random.normal(election.issue.options[randOptionID].coordinates[1],
                                             scale=(float(dimensionSize) / 10.0)), dimensionSize), -dimensionSize)
            election.issue.options[randOptionID].setCoordinates([newOX, newOY])

        rounds += 1
        print(rounds)
        if (rounds > iter):
            break

    if (highestDifference > 0):
        makeStratVotingPlot(kind, bestResult, bestNewResult, bestInitialPM, bestNewPM, bestInitialCoordinates,
                            bestStrategicAgentID, bestElection, bestWinOp, bestNewWin, optionsByName, stratKind= "Change")
    print("Best increase was", highestDifference)


def generateStrategicVoting(kind="WR", numOptions=5, numAgents=10, iter=10000):
    highestDifference = 0
    rounds = 0
    incNum = 0
    election = initializeRandomElection(numOptions, numAgents, 2)
    bestElection = copy.deepcopy(election)

    if (numAgents == 2):
        initialValue = 0.3;
    else:
        initialValue = 1.0 / (numAgents ** 2)

    while (True):

        if (highestDifference <= initialValue):
            election = initializeRandomElection(numOptions, numAgents, 2)


        # ag = election.agents[0]

        result = election.computeResult(kind=kind)
        strategicAgent = election.agents[0]
        PM = strategicAgent.pm
        if (kind == "WLR" or kind == "WALR"):
            PM = strategicAgent.linearPM

        initialCoordinates = strategicAgent.coordinates

        initialPM = PM

        preferredOption = Helper.getWinner(PM)[0]

        if (len(Helper.getWinner(result.normalizedRanking)) > 1):
            election = copy.deepcopy(bestElection)
            continue
        winningOption = Helper.getWinner(result.normalizedRanking)[0]
        if (preferredOption == winningOption):
            continue
        initialHappiness = result.normalizedRanking[preferredOption]

        optionsByName = [op.name for op in election.issue.options]
        newCoordinates = election.issue.options[optionsByName.index(preferredOption)].coordinates
        strategicAgent.setCoordinates(newCoordinates)
        newPM = strategicAgent.pm
        if (kind == "WLR" or kind == "WALR"):
            newPM = strategicAgent.linearPM

        newResult = election.computeResult(kind=kind)

        newHappiness = newResult.normalizedRanking[preferredOption]
        happinessIncrease = newHappiness - initialHappiness

        if (happinessIncrease > highestDifference):
            print("better time ", incNum)
            incNum += 1
            highestDifference = happinessIncrease

            bestResult = copy.deepcopy(result)
            bestInitialCoordinates = initialCoordinates
            bestInitialPM = initialPM
            bestNewResult = copy.deepcopy(newResult)
            bestNewPM = newPM
            bestElection = copy.deepcopy(election)
            bestStrategicAgentID = election.agents.index(strategicAgent)
            bestWinOp = winningOption
            bestPrefOp = preferredOption
            # makeStratVotingPlot(kind, bestResult, bestNewResult, bestInitialPM, bestNewPM, bestInitialCoordinates,  bestStrategicAgentID, bestElection, bestWinOp, bestPrefOp, optionsByName)

        strategicAgent.setCoordinates(initialCoordinates)

        randAgentID = random.randint(0, len(election.agents) - 1)
        newX = max(min(np.random.normal(election.agents[randAgentID].coordinates[0], scale=(float(dimensionSize)/10.0)), dimensionSize), -dimensionSize)
        newY = max(min(np.random.normal(election.agents[randAgentID].coordinates[1], scale=(float(dimensionSize)/10.0)), dimensionSize), -dimensionSize)
        election.agents[randAgentID].setCoordinates([newX, newY])

        randOptionID = random.randint(0, len(election.issue.options) - 1)
        newOX = max(min(np.random.normal(election.issue.options[randOptionID].coordinates[0], scale=(float(dimensionSize)/10.0)), dimensionSize), -dimensionSize)
        newOY = max(min(np.random.normal(election.issue.options[randOptionID].coordinates[1], scale=(float(dimensionSize)/10.0)), dimensionSize), -dimensionSize)
        election.issue.options[randOptionID].setCoordinates([newOX, newOY])

        rounds += 1
        print(rounds)
        if (rounds > iter):
            break

    if (highestDifference > 0):
        makeStratVotingPlot(kind, bestResult, bestNewResult, bestInitialPM, bestNewPM, bestInitialCoordinates,
                            bestStrategicAgentID, bestElection, bestWinOp, bestPrefOp, optionsByName)
    print("Best increase was", highestDifference)


def makeStratVotingPlot(kind, result, newResult, initialPM, newPM, initialCoordinates, strategicAgentID, election,
                        winningOption, preferredOption, optionsByName, stratKind=""):
    strategicAgent = election.agents[strategicAgentID]

    result.printResults()
    print("Agent has this initial PM", initialPM)
    print(initialCoordinates, " -> ", strategicAgent.coordinates)
    print("Agent has this new PM", newPM)
    newResult.printResults()


    data = []
    data.append([round(num, 3) for num in list(initialPM.values())])
    if(kind == "RC"):
        data.append([list(dict(sorted(initialPM.items(), key=lambda item: item[1], reverse=True)).keys()).index(opName) + 1 for opName in initialPM.keys()])
    data.append([round(num, 3) for num in list(result.normalizedRanking.values())])
    data.append([round(num, 3) for num in list(newPM.values())])
    if(kind == "RC"):
        data[3] = [list(dict(sorted(newPM.items(), key=lambda item: item[1], reverse=True)).keys()).index(opName) + 1 for opName in newPM.keys()]
    data.append([round(num, 3) for num in list(newResult.normalizedRanking.values())])
    indexOfInitialVote = 1
    if (kind == "RC"):
        indexOfInitialVote = 2
    indexOfStratVote = -1
    data.append([round(res2 - res1, 3) for (res1, res2) in zip(data[indexOfInitialVote], data[indexOfStratVote])])
    plt.subplot(2, 2, 2)  # row 1, col 2 index 2 (because the agent we were given is already cheating)
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=6)

    election.print_election_plot(show=False, highlightAgent=election.agents.index(strategicAgent))
    strategicAgent.setCoordinates(initialCoordinates)
    plt.subplot(2, 2, 1)  # index 1
    plt.xticks(fontsize=6)
    plt.yticks(fontsize=6)

    plt.title("Strategic {} Voting with {}".format(stratKind, result.kind_of_eval), fontsize=11, loc="left", y=1.1)

    election.print_election_plot(show=False, highlightAgent=election.agents.index(strategicAgent))

    ax = plt.subplot(2, 1, 2, visible=True)  # index 3

    column_labels = ["Agents Pref", "Result", "Agents Vote", "Result", "Diff"]
    if(kind=="RC"):
        column_labels = ["Agents Pref", "Vote", "Result", "Agents Vote", "Result", "Diff"]

    data = np.array(data).T.tolist()
    df = pd.DataFrame(data, columns=column_labels)

    ax.axis('tight')
    ax.axis('off')
    tab = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=list(result.ranking.keys()),
                   loc="center")

    # Let's add some nice colors!

    indexOfActualPref = optionsByName.index(Helper.getWinner(initialPM)[0])

    ac_pref_cell = tab[indexOfActualPref+1, 0]
    print(indexOfActualPref, Helper.getWinner(initialPM)[0])
    ac_pref_cell.set_facecolor('green')
    ax.add_patch(ac_pref_cell)


    print("preffered Option: ", preferredOption)

    for i in range(len(column_labels)):

        pref_cell = tab[optionsByName.index(preferredOption) + 1, i]
        if (i < 2):  # we only need this for the first two cols
            win_cell = tab[optionsByName.index(winningOption) + 1, i]
            win_cell.set_facecolor('red')
            ax.add_patch(win_cell)
        pref_cell.set_facecolor('palegreen')
        ax.add_patch(pref_cell)

    plt.savefig("strat{}{}{}.png".format(stratKind, kind, int(time())), dpi=300)

    plt.show()

    election.print_elec_table()


if __name__ == '__main__':

    method()
