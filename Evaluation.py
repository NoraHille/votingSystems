

import numpy as np
import matplotlib.pyplot as plt
from classes import ElectionResult
from Election import Election, initializeRandomElection, initializeElection
from agent import Agent
from Helper import Helper
from exampleElections import make_equal_elec, make_Election_1, make_Election_With_extreme_Extremes, make_small_extreme_Elec, make_small_Elec_with_2_options
import pandas as pd
import copy



evalKindDict = {"dist": "Distance to result", "sqdist": "Squared distance to result", "hap": "Happiness with result", "distw": "Distance to winner", "hww": "Weighted happiness with winner", "hw": "Happiness with winner"}
eval_list = ["dist", "sqdist", "rtdist",  "hw"] #for equality
# eval_list = ["dist", "sqdist", "rtdist",  "hw", "HR", "HRW","GRC", "GRCW"] # for quality
kind_list = ["PL", "AV", "RC", "WR", "WAR", "HR", "GRC"]


def method():
    print("HI")
    make_tie_normalized_Var_table(5, 100, 2, numElec=10000, makePlot=False, show=True, name="VarTable10000")




def make_tie_normalized_Quality_table(numOptions, numAgents, numDim, numElec= 1, ax = None, show = True, makePlot=False, name="qualityTable"):
    happDict_list, varDict_list, kinds_for_eval_list = computeHappAndVar(numOptions, numAgents, numDim, numElec= numElec, makePlot=False, noVar=True)

    """" This function makes a table evaluating all the voting systems in kind_list with all the evaluation methods defined in eval_list
    and divides the results by the result the tie voting system achieves (unless that would be a zero) """
    happiness = {}
    for eval in eval_list:
        happiness[eval] = [0] * len(happDict_list[0][eval])
        for hap in happDict_list:
            for i in range(len(hap[eval])):
                happiness[eval][i] += (hap[eval][i] / numElec)

    tieHapp = {}
    for eval in happiness.keys():
        tieHapp[eval] = happiness[eval][0]

    for eval in eval_list:
        if (tieHapp[eval] == 0):
            tieHapp[eval] = 1
        for i in range(len(happiness[eval])):


            happiness[eval][i] /= tieHapp[eval]


    column_labels = []
    data = []

    for eval_type in eval_list:
        column_labels.append(eval_type)
        data.append([round(num, 6) for num in happiness[eval_type]])


    makeTable(data, column_labels, kinds_for_eval_list, name, title="Quality measures", ax=None, show=show)


def make_tie_normalized_Var_table(numOptions, numAgents, numDim, numElec= 1, ax = None, show = True, makePlot=False, name="qualityTable"):
    happDict_list, varDict_list, kinds_for_eval_list = computeHappAndVar(numOptions, numAgents, numDim, numElec= numElec, makePlot=False, noHap=True)

    """" This function makes a table evaluating all the voting systems in kind_list with all the evaluation methods defined in eval_list
      and taking their variance and divides the results by the result the tie voting system achieves (unless that would be a zero) """

    variance = {}
    for eval in eval_list:

        variance[eval] = [0] * len(varDict_list[0][eval])
        for var in varDict_list:
            for i in range(len(var[eval])):
                variance[eval][i] += var[eval][i] / numElec

    tieVar= {}
    for eval in variance.keys():
        tieVar[eval] = variance[eval][0]

    for eval in eval_list:
        if (tieVar[eval] == 0):
            tieVar[eval] = 1
        for i in range(len(variance[eval])):


            variance[eval][i] /= tieVar[eval]


    column_labels = []
    data = []

    for eval_type in eval_list:

        column_labels.append("var("+ eval_type + ")")
        data.append([round(num, 5) for num in variance[eval_type]])

    makeTable(data, column_labels, kinds_for_eval_list, name, title="Imbalance measures", ax=None, show=show)




def makeWholeQualHapTable(numOptions, numAgents, numDim, numElec= 1, ax = None, show = True, makePlot=False, name="evalTable"):
    happDict_list, varDict_list, kinds_for_eval_list = computeHappAndVar(numOptions, numAgents, numDim, numElec=numElec,
                                                                         makePlot=False)
    happiness = {}
    variance = {}
    for eval in eval_list:
        happiness[eval] = [0] * len(happDict_list[0][eval])
        for hap in happDict_list:
            for i in range(len(hap[eval])):
                happiness[eval][i] += hap[eval][i]/numElec


        variance[eval] = [0] * len(varDict_list[0][eval])
        for var in varDict_list:
            for i in range(len(var[eval])):
                variance[eval][i] += var[eval][i]/numElec

    column_labels = []
    data = []

    if (ax == None):
        _, ax = plt.subplots(1, 1)



    for eval_type in eval_list:
        column_labels.append(eval_type)
        data.append([round(num, 3) for num in happiness[eval_type]])
        column_labels.append("var("+ eval_type + ")")
        data.append([round(num, 5) for num in variance[eval_type]])


    makeTable(data, column_labels, kinds_for_eval_list, name=name, title="Random Election with {} agents and {} options.".format(numAgents, numOptions),  ax=None, show=show)



def computeHappAndVar(numOptions, numAgents, numDim, numElec= 1, makePlot=False, noHap= False, noVar=False):

    kinds_for_eval_list = ["tie"]
    kinds_for_eval_list.extend(kind_list)

    happDict_list = []
    varDict_list = []

    for i in range(numElec):

        election = initializeElection(numOptions,numAgents,numDim)
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

                linear = False

                if(not noHap):
                    happiness[eval].append(computeHappinessWithResult(election, result, kind=eval,makePlot=makePlot, linear=linear))
                if(not noVar):
                    variance[eval].append(computeVarianceOfHappiness(election, result, kind=eval, linear=linear))

        happDict_list.append(happiness)
        varDict_list.append(variance)
    return happDict_list, varDict_list, kinds_for_eval_list


def makeTable(data, column_labels, kinds_for_eval_list, name, title="Table", ax=None, show=True):

    if (ax == None):
        _, ax = plt.subplots(1, 1)

    data = np.array(data).T.tolist()
    df = pd.DataFrame(data, columns=column_labels)
    ax.axis('tight')
    ax.axis('off')
    tab = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=kinds_for_eval_list,
                   loc="center")
    tab.auto_set_font_size(False)
    tab.set_fontsize(6)
    tab.scale(1.1, 1)
    plt.title(title)
    plt.savefig("{}.png".format(name), dpi=1000)
    if(show):
        plt.show()



def computeHappinessWithResult(election: Election, result: ElectionResult, kind="dist", makePlot=False, linear=False)-> float:


    if(kind=="GR" or kind=="GRC" or kind=="WR" or kind=="HR" or kind=="WAR"): #closeness to solution
        return closenessToSolution(election, result, kind=kind)
    if (kind=="GRW" or kind=="WRW" or kind=="GRCW" or kind=="HRW" or kind=="WARW"):  # closeness to solution winner
        return closenessToSolutionWinner(election, result, kind=kind[:-1])






    totalHappiness = 0
    agHappiness = 0

    agentNum = len(election.agents)*1.0
    if(makePlot):
        numberOfBars = 50
        lengthOfXAchsis = 1
        if(result.short_kind_of_eval == "RC"):
            lengthOfXAchsis=2
        spanOfABar = lengthOfXAchsis/numberOfBars
        curveDict = {}
        for i in np.linspace(0, lengthOfXAchsis - spanOfABar, num=numberOfBars):
            curveDict[i] = 0
    for agent in election.agents:
        if(kind =="dist"):
            agHappiness = distanceOfAgentToResult(agent, result, linear=linear)

        if (kind == "pw"):
            agHappiness = preferanceOfAgentOfWinner(agent, result, linear=linear)
        if (kind == "hw"):
            agHappiness = happinessOfAgentWithWinner(agent, result, linear=linear)
        if (kind == "sqdist"):
            agHappiness = squaredDistanceOfAgentToResult(agent, result, linear=linear)
        if (kind == "rtdist"):
            agHappiness = rootDistanceOfAgentToResult(agent, result, linear=linear)

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

        amountOfLabels = 3 #every amountIfLabel step there will be a Label

        plt.bar(nameList, valueList)
        plt.xticks(list(range(0,numberOfBars, amountOfLabels)), [name for num, name in enumerate(nameList) if num%amountOfLabels ==0], rotation=50)
        plt.tick_params(axis='both', which='major', labelsize=7)
        plt.title("distribution of "+ result.kind_of_eval)


        plt.savefig("distributionPlot{}.png".format(result.short_kind_of_eval), dpi=700)
        plt.show()

    return totalHappiness/agentNum

def computeVarianceOfHappiness(election: Election, result: ElectionResult, kind="dist", linear=False)-> float:

    mu = computeHappinessWithResult(election, result, kind=kind, linear=linear)


    variance = 0
    agentNum = len(election.agents) * 1.0

    for agent in election.agents:

        if (kind == "dist"):
            variance += (distanceOfAgentToResult(agent, result, linear=linear)-mu)**2
        if (kind == "hap"):
            variance += (happinessOfAgentWithResult(agent, result, linear=linear)-mu)**2
        if (kind == "hww"):
            variance += (happinessOfAgentWithWinnerWeighted(agent, result, linear=linear)-mu)**2
        if (kind == "hw"):
            variance += (happinessOfAgentWithWinner(agent, result, linear=linear)-mu)**2
        if (kind == "sqdist"):
            variance += (squaredDistanceOfAgentToResult(agent, result, linear=linear)-mu)**2
        if (kind == "rtdist"):
            variance += (rootDistanceOfAgentToResult(agent, result, linear=linear) - mu) ** 2
        if (kind == "distw"):
            variance += (distanceOfAgentToWinner(agent, result, linear=linear) - mu) ** 2


    return variance/agentNum


def closenessToSolution(elec: Election, result: ElectionResult, kind="HR"):
    res = elec.computeBallotResult(kind)
    totalDist = 0
    for opName, score in res.normalizedRanking.items():
        totalDist += abs(result.normalizedRanking[opName] - score)
    return totalDist

def closenessToSolutionWinner(elec: Election, result: ElectionResult, kind="HR"):
    res = elec.computeBallotResult(kind)
    if (Helper.getWinner(res.normalizedRanking) == Helper.getWinner(result.normalizedRanking)):
        return 1
    else:
        return 0


def happinessOfAgentWithResult(agent: Agent, result: ElectionResult, linear=False)-> float:
    HM = agent.hm

    happiness = 0
    for op_name in HM.keys():
        happiness += HM[op_name]*result.normalizedRanking[op_name]

    return happiness

def distanceOfAgentToResult(agent: Agent, result: ElectionResult, linear=False)-> float:
    PM = agent.pm
    if (linear):
        PM = agent.linearPM
    distance = 0
    for op_name in PM.keys():
        distance += abs(PM[op_name]-result.normalizedRanking[op_name])

    return distance

def rootDistanceOfAgentToResult(agent: Agent, result: ElectionResult, linear=False)-> float:
    PM = agent.pm
    if (linear):
        PM = agent.linearPM
    distance = 0
    for op_name in PM.keys():
        distance += (abs(PM[op_name]-result.normalizedRanking[op_name]))**0.5
    # print(distance)
    return distance

def squaredDistanceOfAgentToResult(agent: Agent, result: ElectionResult, linear=False)-> float:
    PM = agent.pm
    if (linear):
        PM = agent.linearPM
    distance = 0
    for op_name in PM.keys():
        distance += (PM[op_name]-result.normalizedRanking[op_name])**2
    # print(distance)

    return distance

def preferanceOfAgentOfWinner(agent: Agent, result: ElectionResult, linear=False)-> float:
    PM = agent.pm
    if (linear):
        PM = agent.linearPM
    winners = Helper.getWinner(result.normalizedRanking)
    happiness = 0
    for op_name in winners:
        happiness += PM[op_name]

    return happiness/len(winners)

def happinessOfAgentWithWinner(agent: Agent, result: ElectionResult, linear=False)-> float:
    HM = agent.hm
    winners = Helper.getWinner(result.normalizedRanking)
    happiness = 0
    for op_name in winners:
        happiness += HM[op_name]

    return happiness/len(winners)

def happinessOfAgentWithWinnerWeighted(agent: Agent, result: ElectionResult, linear=False)-> float:
    HM = agent.hm
    winners = Helper.getWinner(result.normalizedRanking)
    happiness = 0
    for op_name in winners:
        happiness += HM[op_name]*result.normalizedRanking[op_name]

    return happiness/len(winners)

def distanceOfAgentToWinner(agent: Agent, result: ElectionResult, linear=False)-> float:
    PM = agent.pm
    if (linear):
        PM = agent.linearPM
    winners = Helper.getWinner(result.normalizedRanking)
    distance = 0
    for op_name in winners:
        distance += abs(PM[op_name] - result.normalizedRanking[op_name])

    return distance/len(winners)


































if __name__ == '__main__':

    method()