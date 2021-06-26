

import numpy as np
import matplotlib.pyplot as plt
from classes import ElectionResult
from Election import Election, initializeRandomElection, initializeElection
from agent import Agent
from Helper import Helper
from exampleElections import make_equal_elec
import pandas as pd


evalKindDict = {"dist": "Distance to result", "sqdist": "Squared distance to result", "hap": "Happiness with result", "distw": "Distance to winner", "hww": "Weighted happiness with winner", "hw": "Happiness with winner"}
eval_list = ["hw"]
# eval_list = ["dist", "sqdist", "rtdist", "hap", "distw", "hww", "hw"]
kind_list = ["AV"]
# kind_list = ["WR", "WAR", "AV", "RC", "PL"]


def method():
    print("HI")
    makeAHappinessTable(5, 1000, 2, numElec=1, makePlot=True, show=False)



def makeAHappinessTable(numOptions, numAgents, numDim, numElec= 1, ax = None, show = True, makePlot=False ):



    kinds_for_eval_list = ["tie"]
    kinds_for_eval_list.extend(kind_list)

    happDict_list = []
    varDict_list = []

    for i in range(numElec):
        # election = initializeElection(numOptions,numAgents,numDim, centerPoints=[(0.4, (5,5)), (0.3, (-30,-90)), (0.2, (-60,90)), (0.1, (80, -25))])
        election = initializeElection(numOptions,numAgents,numDim)
        # election = make_equal_elec(numOptions, numAgents, numDim)
        happiness = {}
        variance = {}

        for eval in eval_list:
            happiness[eval] = []
            variance[eval] = []
            for kind in kinds_for_eval_list:

                if(kind=="tie"):
                    result_dict = Helper.getEmptyDict(election.getOptionNameList())
                    for op_name in election.getOptionNameList():
                        result_dict[op_name] = 1.0/(len(election.getOptionNameList())*1.0)
                    result = ElectionResult(result_dict, kind)

                else:
                    result = election.computeBallotResult(kind)


                happiness[eval].append(computeHappinessWithResult(election, result, kind=eval,makePlot=makePlot))
                # variance[eval].append(computeVarianceOfHappiness(election, result, kind=eval))

        happDict_list.append(happiness)
        varDict_list.append(variance)

    happiness = {}
    variance = {}
    for eval in eval_list:
        happiness[eval] = [0] * len(happDict_list[0][eval])
        for hap in happDict_list:
            for i in range(len(hap[eval])):
                happiness[eval][i] += hap[eval][i]/numElec

        # for i in range(len(happiness[eval])):
        #     happiness[eval][i] /= numElec


        variance[eval] = [0] * len(varDict_list[0][eval])
        for var in varDict_list:
            for i in range(len(var[eval])):
                variance[eval][i] += var[eval][i]/numElec

        # for i in range(len(variance[eval])):
        #     variance[eval][i] /= numElec





    column_labels = []
    data = []

    if (ax == None):
        _, ax = plt.subplots(1, 1)



    for eval_type in eval_list:
        column_labels.append(eval_type)
        data.append([round(num, 3) for num in happiness[eval_type]])
        column_labels.append("var("+ eval_type + ")")
        data.append([round(num, 5) for num in variance[eval_type]])

    data = np.array(data).T.tolist()
    df = pd.DataFrame(data, columns=column_labels)
    ax.axis('tight')
    ax.axis('off')
    tab = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=kinds_for_eval_list,
                   loc="center")
    tab.auto_set_font_size(False)
    tab.set_fontsize(6)
    tab.scale(1.1, 1)
    plt.title("Random Election with {} agents and {} options.".format(numAgents, numOptions))
    plt.savefig("happinessTableVeryLong2.png", dpi=700)
    if(show):
        plt.show()


def computeHappinessWithResult(election: Election, result: ElectionResult, kind="dist", makePlot=False)-> float:

    totalHappiness = 0
    agHappiness = 0

    agentNum = len(election.agents)*1.0
    if(makePlot):
        numberOfBars = 30
        spanOfABar = 1/numberOfBars
        curveDict = {}
        for i in np.linspace(0, 1 - spanOfABar, num=numberOfBars):
            curveDict[i] = 0

    for agent in election.agents:
        if(kind =="dist"):
            agHappiness = distanceOfAgentToResult(agent, result)
        if (kind == "hap"):
            agHappiness = happinessOfAgentWithResult(agent, result)
        if (kind == "hww"):
            agHappiness = happinessOfAgentWithWinnerWeighted(agent, result)
        if (kind == "hw"):
            agHappiness = happinessOfAgentWithWinner(agent, result)
        if (kind == "sqdist"):
            agHappiness = squaredDistanceOfAgentToResult(agent, result)
        if (kind == "rtdist"):
            agHappiness = rootDistanceOfAgentToResult(agent, result)
        if (kind == "distw"):
            agHappiness = distanceOfAgentToWinner(agent, result)
        totalHappiness += agHappiness
        if(makePlot):
            for num in list(curveDict.keys()):
                if(agHappiness<num+ spanOfABar):
                    curveDict[num] += 1
                    break


    if(makePlot):
        nameList =[]
        valueList = []
        for key, value in curveDict.items():
            name = str(round(key, 2)) + "-" + str(round(key+ spanOfABar, 2))
            nameList.append(name)
            valueList.append(value)

        amountOfLabels = 1 #every amountIfLabel step there will be a Label

        plt.bar(nameList, valueList)
        plt.xticks(list(range(0,numberOfBars, amountOfLabels)), [name for num, name in enumerate(nameList) if num%amountOfLabels ==0], rotation=50)
        plt.tick_params(axis='both', which='major', labelsize=7)
        print(nameList, valueList)
        plt.show()

    return totalHappiness/agentNum

def computeVarianceOfHappiness(election: Election, result: ElectionResult, kind="dist")-> float:

    mu = computeHappinessWithResult(election, result, kind=kind)/len(election.agents)

    variance = 0
    agentNum = len(election.agents) * 1.0

    for agent in election.agents:

        if (kind == "dist"):
            variance += (distanceOfAgentToResult(agent, result)-mu)**2
        if (kind == "hap"):
            variance += (happinessOfAgentWithResult(agent, result)-mu)**2
        if (kind == "hww"):
            variance += (happinessOfAgentWithWinnerWeighted(agent, result)-mu)**2
        if (kind == "hw"):
            variance += (happinessOfAgentWithWinner(agent, result)-mu)**2
        if (kind == "sqdist"):
            variance += (squaredDistanceOfAgentToResult(agent, result)-mu)**2
        if (kind == "rtdist"):
            variance += (rootDistanceOfAgentToResult(agent, result) - mu) ** 2
        if (kind == "distw"):
            variance += (distanceOfAgentToWinner(agent, result) - mu) ** 2

    return variance/agentNum



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

def rootDistanceOfAgentToResult(agent: Agent, result: ElectionResult)-> float:
    PM = agent.pm
    distance = 0
    for op_name in PM.keys():
        distance += (abs(PM[op_name]-result.normalizedRanking[op_name]))**0.5

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

def distanceOfAgentToWinner(agent: Agent, result: ElectionResult)-> float:
    PM = agent.pm
    winners = Helper.getWinner(result.normalizedRanking)
    distance = 0
    for op_name in winners:
        distance += abs(PM[op_name] - result.normalizedRanking[op_name])

    return distance/len(winners)


































if __name__ == '__main__':

    method()