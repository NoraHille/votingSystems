import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import pandas as pd
import math
import string
import random
import copy
from time import time

# Todo:
# - show absolute as well as relative values
# - investigate different approval voting scores
# - color landscape plot according to plurality score
# - Simulate strategic voting -> Come up with a score
# - Testing! You need to be CERTAIN everything is right!


colormap = np.array(['teal', 'purple', 'yellow', 'steelblue', 'green',  'pink', 'red', 'brown', 'gray'])
dimensionSize = 100
alphabet_string = string.ascii_uppercase
alphabet_list = list(alphabet_string)


class Issue(object):
    def __init__(self, options, dimensions):
        self.options = options  # options is a list of options
        self.dimensions = dimensions  # dimensions is a list of Strings

        for i in range(len(options)):
            options[i].setName(alphabet_list[i])
            if len(options[i].coordinates) != len(dimensions):
                print("options has wrong number of dimensions")


class Option(object):
    def __init__(self, coordinates):
        self.setCoordinates(
            coordinates)  # coordinates is a list of real numbers, each number being associated with a dimension in the issue

    def setName(self, name):
        self.name = name

    def setCoordinates(self, coordinates):
        self.coordinates = coordinates


class Agent(object):
    def __init__(self, coordinates, issue):
        self.issue = issue
        self.setCoordinates(coordinates)

    def setCoordinates(self, coordinates):
        self.coordinates = coordinates  # coordinates is a list of real numbers, each number being associated with a dimension in the issue
        self.pm = self.create_PM(self.issue)
        self.linearPM = self.create_linear_PM(self.issue)

    def create_PM(self, issue):
        pm = {}
        normalization_faktor = 0;
        for op in issue.options:

            dist = self.computeDistance(op)
            if (dist == 0):
                dist = 0.0000000001
            pref = pow(dist, -1)  # raise to the power of -1 to make agents prefer the option with the lowest distance
            pm[op.name] = pref;
            normalization_faktor += pref;
        # normalize PM so it adds up to 1
        sum_of_preferences = 0
        for (op_name, pref) in pm.items():
            normalized_pref = pref / normalization_faktor
            pm[op_name] = normalized_pref
            sum_of_preferences += normalized_pref
        # if(sum_of_preferences != 1):
        # print("Something went wrong with the normalization, the normalized value is ", sum_of_preferences)
        # print("The PM of an agent is: ", pm)
        return pm

    def create_linear_PM(self, issue):
        pm = {}
        sumOfDist = 0;
        for op in issue.options:

            dist = self.computeDistance(op)
            if (dist == 0):
                dist = 0.0000000001
            pref = dist
            pm[op.name] = pref;
            sumOfDist += dist;
        # linearly invert

        sum_of_inv_preferences = 0
        for (op_name, pref) in pm.items():
            inverted_pref = sumOfDist - pref
            pm[op_name] = inverted_pref
            sum_of_inv_preferences += inverted_pref

        # normalize PM so it adds up to 1
        sum_of_preferences = 0
        for (op_name, pref) in pm.items():
            normalized_pref = pref / sum_of_inv_preferences
            pm[op_name] = normalized_pref
            sum_of_preferences += normalized_pref
        # if(sum_of_preferences != 1):
        # print("Something went wrong with the normalization, the normalized value is ", sum_of_preferences)
        # print("The PM of an agent is: ", pm)
        return pm

    def computeDistance(self, option):
        dist = 0;
        for i in range(len(self.coordinates)):
            dist += pow(self.coordinates[i] - option.coordinates[i], 2)
        return math.sqrt(dist)


def common_PM(args):
    pass


class ElectionResult(object):
    def __init__(self, ranking, kind_of_eval):
        self.ranking = ranking
        self.normalizedRanking = Helper.normalizeDict(ranking)
        self.kind_of_eval = kind_of_eval

    def printResults(self):
        print("Using {} the winning option is {} and these are the normalized results {}. Absolute results: {}".format(
            self.kind_of_eval,
            Helper.getWinner(
                self.normalizedRanking), self.normalizedRanking, self.ranking))


class Election:
    def __init__(self, issue, agents):
        self.issue = issue
        self.agents = agents

    def computeAllResults(self):
        result_list = []
        # result_list.append(self.computeResultPlurality())
        # result_list.append(self.computeResultRC())
        # result_list.append(self.computeResultAV(cutOffScore=0))
        # result_list.append(self.computeResultWR())
        # result_list.append(self.computeResultWLR())
        # result_list.append(self.computeResultWAR())
        # result_list.append(self.computeResultWAR(linear=True))

        for kind in ["PL", "RC", "AV", "WR", "WLR", "WAR", "WALR"]:
            result_list.append(self.computeResult(kind=kind))

        return result_list

    def print_election_plot(self, show=True, highlightAgent=None, colorPlurality=False, colorWeighted=False, linear=False, scale=1):

        if (len(self.issue.dimensions) != 2):
            print("You tried to plot an election with more/less than 2 dimensions, namely ", len(self.issue.dimensions))
            return

        ag_x = []
        ag_y = []
        agentCat = []
        for ag in self.agents:
            if (len(Helper.getWinner(ag.pm)) > 1):
                print("an agent is torn between multiple options!")
            choice = Helper.getWinner(ag.pm)[0]
            optionNameList = [op.name for op in self.issue.options]
            choiceID = optionNameList.index(choice)
            agentCat.append(choiceID)
            ag_x.append(ag.coordinates[0])
            ag_y.append(ag.coordinates[1])

        if (not colorPlurality and not colorWeighted):
            plt.scatter(ag_x, ag_y)
        else:
            if (colorPlurality):
                plt.scatter(ag_x, ag_y, s=10, c=colormap[agentCat])

            else:

                optionNameList = [op.name for op in self.issue.options]
                sizer = 50*1.0/(scale)
                exp = 2

                for ag in self.agents:
                    if (linear):
                        sorted_dict = dict(sorted(ag.linearPM.items(), key=lambda item: item[1], reverse=True))
                        sorted_dict_rev = dict(sorted(ag.linearPM.items(), key=lambda item: item[1], reverse=False))
                        # sizer= 8
                        # exp = 10
                    else:
                        sorted_dict = dict(sorted(ag.pm.items(), key=lambda item: item[1], reverse=True))
                        sorted_dict_rev = dict(sorted(ag.pm.items(), key=lambda item: item[1], reverse=False))

                    size = 0
                    for op, score in sorted_dict_rev.items():
                        sadd = (sizer * score) ** exp

                        size += sadd

                    for op, score in sorted_dict.items():
                        optionID = optionNameList.index(op)

                        plt.scatter(ag.coordinates[0], ag.coordinates[1], s=size, c=colormap[optionID])
                        size -= (sizer * score) ** exp

                # # first define the ratios
                # r1 = 0.9  # 20%
                # r2 = r1 + 0.05  # 40%
                #
                # # define some sizes of the scatter marker
                # sizes = [60, 80, 120]
                #
                # # calculate the points of the first pie marker
                # #
                # # these are just the origin (0,0) +
                # # some points on a circle cos,sin
                #
                #
                # x = [0] + np.cos(np.linspace(0, 2 * math.pi * r1, 10)).tolist()
                # y = [0] + np.sin(np.linspace(0, 2 * math.pi * r1, 10)).tolist()
                # xy1 = list(zip(x, y))
                # plt.scatter(ag_x, ag_y, s=100, marker=xy1, c='green')
                #
                # # ...
                # x = [0] + np.cos(np.linspace(2 * math.pi * r1, 2 * math.pi * r2, 10)).tolist()
                # y = [0] + np.sin(np.linspace(2 * math.pi * r1, 2 * math.pi * r2, 10)).tolist()
                # xy2 = list(zip(x, y))
                # plt.scatter(ag_x, ag_y, s=100, marker=xy2, c='red')
                #
                # x = [0] + np.cos(np.linspace(2 * math.pi * r2, 2 * math.pi, 10)).tolist()
                # y = [0] + np.sin(np.linspace(2 * math.pi * r2, 2 * math.pi, 10)).tolist()
                # xy3 = list(zip(x, y))
                # plt.scatter(ag_x, ag_y, s=100, marker=xy3, c='blue')

        op_x = []
        op_y = []
        op_names = []
        for op in self.issue.options:
            op_x.append(op.coordinates[0])
            op_y.append(op.coordinates[1])
            op_names.append(op.name)

        optionCat = np.array(range(len(self.issue.options)))

        if (not colorPlurality and not colorWeighted):
            plt.scatter(op_x, op_y, color="red")
        else:
            plt.scatter(op_x, op_y, marker='D',edgecolors='black', s=200, c=colormap[optionCat])







        if (highlightAgent != None):
            x = self.agents[highlightAgent].coordinates[0]
            y = self.agents[highlightAgent].coordinates[1]
            plt.scatter(x, y, s=10, color="darkblue")

        for i, txt in enumerate(op_names):
            plt.annotate(txt, xy=(op_x[i], op_y[i]), xytext=(op_x[i]-2*scale, op_y[i]-2*scale))

        plt.xlim([-dimensionSize, dimensionSize])
        plt.ylim([-dimensionSize, dimensionSize])

        if (show):
            plt.show()

    def print_result_table(self, rounded=True, show=True, ax=None):

        result_list = self.computeAllResults()

        column_labels = []
        data = []

        # plt.figure(dpi=2000)

        if(ax == None):
            _, ax = plt.subplots(1, 1)
        for res in result_list:
            column_labels.append(res.kind_of_eval)
            # data.append([round(num, 3) for num in list(res.ranking.values())])
            data.append([round(num, 3) for num in list(res.normalizedRanking.values())])
        #     data.append([round(abs, 3) + "(" + round(rel, 3) + ")" for num, rel in zip(list(res.ranking.values()), list(res.normalizedRanking.values()))])
        data = np.array(data).T.tolist()
        print(data)
        df = pd.DataFrame(data, columns=column_labels)
        ax.axis('tight')
        ax.axis('off')
        print(list(result_list[0].ranking.keys()))
        tab = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=list(result_list[0].ranking.keys()),
                       loc="center")
        tab.auto_set_font_size(False)
        tab.set_fontsize(6)
        tab.scale(1.1, 1)


        #color options

        for i in range(len(self.issue.options)):
            the_cell = tab[i+1, -1]
            the_cell.set_facecolor(colormap[i])
            ax.add_patch(the_cell)


        # highlight winners
        for i, res in enumerate(result_list):
            print("new res ", i)

            for win in Helper.getWinner(res.normalizedRanking):
                # Highlight the cell to draw attention to it

                print(win)
                the_cell = tab[alphabet_list.index(win) + 1, i]
                # the_cell = tab[1, 2]
                the_cell.set_facecolor('palegreen')
                # the_cell.set_edgecolor('black')
                # the_cell.set_linewidth(2)
                the_text = the_cell.get_text()
                # the_text.set_weight('bold')
                # the_text.set_fontstyle('italic')
                # the_text.set_color(highlight_text_color)
                ax.add_patch(the_cell)

        plt.savefig("table.png", dpi=300)

        return ax

        if(show):
            plt.show()

    def make_result_graphic(self):

        plt.subplot(2, 2, 1)
        self.print_election_plot(colorPlurality=True, show=False, scale=2)
        plt.xticks(fontsize=6)
        plt.yticks(fontsize=6)
        plt.subplot(2,2,2)
        self.print_election_plot(colorWeighted=True, show=False, scale =2)
        plt.xticks(fontsize=6)
        plt.yticks(fontsize=6)

        self.print_result_table(show=False, ax=plt.subplot(2,1,2))
        plt.savefig("elecGraphic.png", dpi=1000, bbox_inches='tight')

        plt.show()


    def computeResult(self, kind="WR"):

        if (kind == "WR"):
            return self.computeResultWR()
        if (kind == "WAR"):
            return self.computeResultWAR()
        if (kind == "AV"):
            return self.computeResultAV()
        if (kind == "RC"):
            return self.computeResultRC()
        if (kind == "PL"):
            return self.computeResultPlurality()
        if (kind == "WLR"):
            return self.computeResultWLR()
        if (kind == "WALR"):
            return self.computeResultWAR(linear=True)

    def computeResultWR(self):  # Weighted Ranking
        common_PM = {}
        for op in self.issue.options:
            common_PM[op.name] = 0
            for ag in self.agents:
                common_PM[op.name] += ag.pm[op.name]

        return ElectionResult(common_PM, "Weighted")

    def computeResultWLR(self):  # Weighted Linear Ranking
        common_lin_PM = {}
        for op in self.issue.options:
            common_lin_PM[op.name] = 0
            for ag in self.agents:
                common_lin_PM[op.name] += ag.linearPM[op.name]

        return ElectionResult(common_lin_PM, "Weighted lin. ")

    def computeResultWAR(self, linear=FALSE):  # Weighted Approval Ranking
        # print("results of weighted ranking: ")
        name = "Weighted App"
        if (linear):
            name = "WAL"
        common_PM = {}
        for op in self.issue.options:
            common_PM[op.name] = 0
            for ag in self.agents:
                # scale the agents pm so that the highes option is set to exactly 1:
                highestScore = 0
                items = ag.pm.items()
                if (linear):
                    items = ag.linearPM.items()
                for (option, score) in items:
                    if (score > highestScore):
                        highestScore = score
                if (linear):
                    common_PM[op.name] += (ag.linearPM[op.name] * 1 / highestScore)
                else:
                    common_PM[op.name] += (ag.pm[op.name] * 1 / highestScore)

        return ElectionResult(common_PM, name)

    def computeResultPlurality(self):  # Plurality
        voteScore = {}
        for op in self.issue.options:
            voteScore[op.name] = 0
        for ag in self.agents:
            winning_options = Helper.getWinner(ag.pm)
            for wo in winning_options:
                voteScore[wo] += 1 / len(winning_options)  # even though its not at all how Plurality
            # voting works in real life it most closely resembles the result of real Plurality voting,
            # where each voter would make a semi random choice about what option to choose
        return ElectionResult(voteScore, "Plurality")

    def computeResultRC(self):  # Ranked Choice
        disregardedOptions = []
        while (True):
            voteScore = {}
            for op in self.issue.options:
                voteScore[op.name] = 0
            for ag in self.agents:
                # print("ag")
                winning_options = Helper.getWinner(ag.pm, disregardedOptions=disregardedOptions)
                for wo in winning_options:
                    voteScore[wo] += 1 / len(winning_options)
                    # print(voteScore, "voteScore")

            voteScore = Helper.normalizeDict(voteScore)
            # print(voteScore)
            lowestScore = 0.9
            lowestOption = ""
            for (option, score) in voteScore.items():
                if (option not in disregardedOptions):
                    # print(option, " is not part of ", disregardedOptions)
                    if (score < lowestScore):
                        lowestOption = option
                        lowestScore = score

                    if (score > 0.5):
                        return ElectionResult(voteScore, "Ranked Choice")

            # print(lowestOption, " was the lowest option")
            disregardedOptions.append(lowestOption)

    def computeResultAV(self, percentOfOptionsToApproveOf=0.5, cutOffScore=None):  # Approval Voting
        if (cutOffScore != None):
            # The cutOffScore must be given independant of the number of choices.
            # A cutoff score of 0 means that we approve an option as long as it scores better than the mean. 0 -> 1/5
            # A cut off score of 1 means we approve all options, one of -1 means we approve of none. 1-> 0; -1 -> 1
            length = len(self.issue.options)
            if (cutOffScore < 0):
                cutOff = 1 / length - cutOffScore * (length - 1) / length
            else:
                cutOff = 1 / length - cutOffScore * 1 / length
            print(cutOff, cutOffScore)
            voteScore = {}
            for op in self.issue.options:
                voteScore[op.name] = 0
            for ag in self.agents:
                for (op, score) in ag.pm.items():
                    if (score >= cutOff):
                        voteScore[op] += 1
            return ElectionResult(voteScore, "Approval Voting")




        else:
            voteScore = {}
            for op in self.issue.options:
                voteScore[op.name] = 0
            for ag in self.agents:
                approved_options = Helper.getApproved(ag.pm, percentOfOptionsToApproveOf)
                for ao in approved_options:
                    voteScore[ao] += 1
            return ElectionResult(voteScore, "Approval Voting")


class Helper:
    dimensionNames: ["taxamount", "freedom", "environment", "schoolfunding"]

    def getWinner(resultDict, disregardedOptions=[]):
        bestOption = []
        # print(list(resultDict.keys())[0])
        for i in range(len(resultDict)):
            if (list(resultDict.keys())[i] not in disregardedOptions):
                bestOption.append(list(resultDict.keys())[i])
                break;
        for (option, result) in resultDict.items():
            if (option not in disregardedOptions):
                if (resultDict[bestOption[0]] < result):
                    bestOption = [option]
                if (resultDict[bestOption[0]] == result and bestOption[0] != option):
                    bestOption.append(option)
        return bestOption  # returns a list containing either the best option or all options that tie for best option

    def normalizeDict(dict):
        prefs = 0
        for (op_name, pref) in dict.items():
            prefs += pref
        # if prefs != len(self.agents):
        #     print("Something went wrong with the normalization. Values added up to: ", prefs)
        if (prefs == 0):
            return dict
        returnDict = {op_name: pref / prefs for op_name, pref in dict.items()}
        return returnDict

    def getApproved(diction, percentOfOprionsToApproveOf):
        sorted_dict = dict(sorted(diction.items(), key=lambda item: item[1], reverse=True))
        approved_options = []
        for i in range(int(len(diction) * percentOfOprionsToApproveOf)):
            approved_options.append(list(sorted_dict.keys())[i])
        return approved_options


def makeRandomCoordinates(numDimension, low=-dimensionSize, high=dimensionSize):
    randomlist = []
    for i in range(numDimension):
        n = random.uniform(low, high)
        randomlist.append(n)
    return randomlist


def makeAdjecentCoordinates(numDimension, point, standardDev=(float(dimensionSize)/10.0), low=-dimensionSize, high=dimensionSize):
    randomlist = []
    for i in range(numDimension):
        ok = False
        while (not ok):
            n = np.random.normal(point[i], scale=standardDev)
            if (n < high and n > low):
                randomlist.append(n)
                ok = True

    return randomlist


def getRandomAgents(numAgents, numDimensions, issue):
    agents = []
    for i in range(numAgents):
        ag = Agent(makeRandomCoordinates(numDimensions), issue)
        agents.append(ag)
    return agents


def getCenterPointAgents(centerPoints, numAgents, numDimensions, issue):
    listOfChangePoints = []
    agents = []
    changePoint = 0
    for (rate, cp) in centerPoints:
        changePoint += rate * numAgents
        listOfChangePoints.append(changePoint)

    print(listOfChangePoints)
    for i in range(numAgents):
        currentIndex = 0
        for num, cp in enumerate(listOfChangePoints):
            if (i > cp):
                currentIndex = num + 1
        ag = Agent(makeAdjecentCoordinates(numDimensions, centerPoints[currentIndex][1]), issue)
        agents.append(ag)
    return agents


def initializeRandomElection(numOptions, numAgents, numDimensions):
    return initializeElection(numOptions, numAgents, numDimensions)


def initializeElection(numOptions, numAgents, numDimensions,
                       centerPoints=None):  # CenterPoints is a list of tuples with likelihoods and points (points are also tuple)
    options = []
    for i in range(numOptions):
        op = Option(makeRandomCoordinates(numDimensions))
        options.append(op)
    dimensions = []
    for i in range(numDimensions):
        dimensions.append("dim" + 'i')
    issue = Issue(options, dimensions)

    if (centerPoints != None):
        agents = getCenterPointAgents(centerPoints, numAgents, numDimensions, issue)

    else:
        agents = getRandomAgents(numAgents, numDimensions, issue)

    return Election(issue, agents)


def printDict(text, dict):
    print(text)
    for key, value in dict.items():
        print(key, ' : ', value)


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

        for ag in election.agents:

            # ag = election.agents[0]

            result = election.computeResult(kind=kind)
            strategicAgent = ag
            initialCoordinates = strategicAgent.coordinates
            initialPM = strategicAgent.pm
            preferredOption = Helper.getWinner(strategicAgent.pm)[0]
            winningOption = Helper.getWinner(result.normalizedRanking)[0]
            if (preferredOption == winningOption):
                election = copy.deepcopy(bestElection)
                continue
            initialHappiness = result.normalizedRanking[preferredOption]

            optionsByName = [op.name for op in election.issue.options]
            newCoordinates = election.issue.options[optionsByName.index(preferredOption)].coordinates
            strategicAgent.setCoordinates(newCoordinates)
            newPM = strategicAgent.pm

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
                        winningOption, preferredOption, optionsByName):
    # result.printResults()
    # print("Agent has this initial PM", initialPM)
    # print(initialCoordinates, " -> ", strategicAgent.coordinates)
    # print("Agent has this new PM", newPM)
    # newResult.printResults()

    strategicAgent = election.agents[strategicAgentID]

    data = []
    data.append([round(num, 3) for num in list(initialPM.values())])
    data.append([round(num, 3) for num in list(result.normalizedRanking.values())])
    data.append([round(num, 3) for num in list(newPM.values())])
    data.append([round(num, 3) for num in list(newResult.normalizedRanking.values())])
    data.append([round(res2 - res1, 3) for (res1, res2) in zip(data[1], data[3])])
    plt.subplot(2, 2, 2)  # row 1, col 2 index 2 (because the agent we were given is already cheating)

    election.print_election_plot(show=False, highlightAgent=election.agents.index(strategicAgent))
    strategicAgent.setCoordinates(initialCoordinates)
    plt.subplot(2, 2, 1)  # index 1

    plt.title("Strategic Voting with {}".format(result.kind_of_eval), fontsize=11)

    election.print_election_plot(show=False, highlightAgent=election.agents.index(strategicAgent))

    ax = plt.subplot(2, 1, 2, visible=True)  # index 3

    column_labels = ["Agents Pref", "Result", "Agents Vote", "Result", "Diff"]

    data = np.array(data).T.tolist()
    df = pd.DataFrame(data, columns=column_labels)

    ax.axis('tight')
    ax.axis('off')
    tab = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=list(result.ranking.keys()),
                   loc="center")

    # Let's add some nice colors!

    for i in range(len(column_labels)):

        pref_cell = tab[optionsByName.index(preferredOption) + 1, i]
        if (i < 2):  # we only need this for the first two cols
            win_cell = tab[optionsByName.index(winningOption) + 1, i]
            win_cell.set_facecolor('red')
            ax.add_patch(win_cell)
        pref_cell.set_facecolor('palegreen')
        ax.add_patch(pref_cell)

    plt.savefig("strat{}{}.png".format(kind, int(time())), dpi=300)

    plt.show()
