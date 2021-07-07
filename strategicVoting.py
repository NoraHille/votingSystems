

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
from exampleElections import make_small_Election_1, make_Election_1, make_strat_Election_1, make_strat_Election_2, make_app_strat_Election, make_small_Election_3



posDict = {0: -80, 1: -60, 2: -40, 3: -20, 4: 0, 5:20, 6:40, 7:60, 8:80}

#TODO
#Methode die für eine Wahl und ein System berechnet wie viele Agenten/Optionen Paare es gibt, die mit strategischem Wählen besser fahren als ohne
# -> Diese Zahl als Bruchteil der (A,O) Paare insgesamt kann verglichen werden.
# -> Jede der Zahlen mal die Glückssetigerung des A kann verglichen werden.









def method():
    print("HI")
    # generateStrategicChangeVoting(kind="RC", numOptions=5, numAgents=3, iter=1000)

    stratVotPosStats(rounds=100)









def stratVotPosStats(rounds=20):
    numAg = 4
    numOp = 5

    resultDict = {}
    for i in range(rounds):
        election = initializeRandomElection(numOp, numAg, 2)
        newDict = computeStratVotPosForAll(election)
        for (kind, dicti) in newDict.items():
            if( kind not in resultDict):
                resultDict[kind] = {"Over voters": 0, "Change voters": 0, "failed": 0, "didn't try": 0, "Changed": 0}
            for k, value in dicti.items():
                resultDict[kind][k] += value
    total = len(election.issue.options)*len(election.agents)*rounds
    for kind, dicti in resultDict.items():
        innerTotal = dicti["failed"] + dicti["Change voters"] + dicti["Over voters"] + dicti["didn't try"]
        if(innerTotal != total):
            print("total {} and innerTotal {} don't match in StatVotPosStats!".format(total, innerTotal))
        totalAttemps = dicti["failed"] + dicti["Change voters"] + dicti["Over voters"]
        attemptRate = totalAttemps/total
        if(totalAttemps == 0):
            failed = 0
            change = 0
            over = 0
        else:
            failed = dicti["failed"]/totalAttemps * 100
            change = dicti["Change voters"]/totalAttemps * 100
            over = dicti["Over voters"]/totalAttemps * 100

        print("In {} unhappy voters failed {} %, succeded {} %,  overvoted {} % (total {}) and changevoted {} % (total {}) of the time. Attemptrate = {}. Nr of attemps: {}. There were {} changes.".format(kind, failed, 100 - failed, over, dicti["Over voters"], change, dicti["Change voters"], attemptRate, totalAttemps,dicti["Changed"] ))





def computeStratVotPosForAll(election=None):
    if(election==None):
        election = initializeRandomElection(5, 4, 2)
    dicti= {}
    for kind in ["WR", "WAR", "WAR2", "AV", "AV2", "PL", "RC"]:
        stratPos = computePossibilityStratVote(election, kind=kind)
        dicti[kind] = stratPos
        # print(kind, stratPos)
    return dicti



def computePossibilityStratVote(election: Election, kind: str):
    isAV2 = False
    if (kind == "AV2"):
        isAV2 = True
        kind = "AV"
    isWAR2 = False
    if (kind == "WAR2"):
        isWAR2 = True
        kind = "WAR"

    result = election.computeBallotResult(kind)
    winners = Helper.getWinner(result.normalizedRanking)

    sucOverVotes = 0
    sucChangeVotes = 0
    failedStratVotes = 0
    contendet = 0
    changedSomething = 0

    for ag in election.agents:
        PM = ag.pm
        coordinates = ag.coordinates
        personalWinners = Helper.getWinner(PM)
        # if(any(win in winners for win in personalWinners)): # Agent is already happy with the result -> no strat vote necessary
        if(personalWinners == winners):
            contendet += len(election.issue.options)
            continue
        else:
            for num, op in enumerate(election.issue.options):
                if (isAV2 or isWAR2):

                    ag.setNumApp(num + 1)
                # if (kind == "WAR"):
                #     ag.setNumApp(num + 1)
                if(kind == "RC"):
                    fakePM = copy.deepcopy(PM)
                    fakePM[op.name] = 1
                    ag.setPM(fakePM)  # The agent pretends to have this option as their prefered choice

                else:
                    fakePM = Helper.getEmptyDict(list(PM.keys()))
                    fakePM[op.name] = 1
                    ag.setPM(fakePM) #The agent pretends to have this option as their prefered choice
                newResult = election.computeBallotResult(kind)
                newWinners = Helper.getWinner(newResult.normalizedRanking)
                # if (any(win in newWinners for win in personalWinners)): # The Agent successfully changed the outcome of the vote to one of their favorites
                if(op.name in newWinners and op.name not in winners):
                    changedSomething += 1

                # if (any(win in newWinners for win in personalWinners)): # The Agent successfully changed the outcome of the vote to one of their favorites
                #     sucOverVotes += 1
                #     continue
                if(resultImproved(PM, winners, newWinners)): #The Agent could improve their happiness with the result
                    if(op.name in personalWinners):
                        sucOverVotes += 1
                    else:
                        sucChangeVotes +=1
                    continue
                failedStratVotes +=1 #The Agent could not improve the result of the vote through strat voting
            ag.setCoordinates(coordinates) #We set the agent to the old coordinates
            ag.setNumApp(None)


    sumOfLogged = sucOverVotes + sucChangeVotes + failedStratVotes + contendet
    sumOfTuples = len(election.agents)* len(election.issue.options)

    if(sumOfLogged!= sumOfTuples):
        print("The number of logged votes doesn't match.")

    return {"Over voters": sucOverVotes, "Change voters":  sucChangeVotes, "failed": failedStratVotes, "didn't try":contendet, "Changed": changedSomething}



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
