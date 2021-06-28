import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import pandas as pd
import math
import string
import random
import copy
from time import time
from Helper import Helper, colormap, dimensionSize, alphabet_string, alphabet_list, kindDict

from classes import ElectionResult, Option, Issue, makeRandomCoordinates
from agent import Agent



class Election:
    def __init__(self, issue, agents, agentBlocks= None):
        self.issue = issue
        self.agents = agents
        self.agentBlocks = agentBlocks







    def computeAllResults(self):
        result_list = []
        # result_list.append(self.computeResultPlurality())
        # result_list.append(self.computeResultRC())
        # result_list.append(self.computeResultAV(cutOffScore=0))
        # result_list.append(self.computeResultWR())
        # result_list.append(self.computeResultWLR())
        # result_list.append(self.computeResultWAR())
        # result_list.append(self.computeResultWAR(linear=True))

        for kind in ["PL", "RC", "AV", "WR", "WAR", "WLR", "GR", "GRP", "HR", "HLR", "Dist"]:
            result_list.append(self.computeBallotResult(kind=kind))

        return result_list

    def getOptionNameList(self):
        return list(self.agents[0].pm.keys())

    def print_election_plot(self, show=True, highlightAgent: int=None, colorPlurality=False, colorWeighted=False, linear=False, scale=1, printMiddle=False):

        if (len(self.issue.dimensions) != 2):
            print("You tried to plot an election with more/less than 2 dimensions, namely ", len(self.issue.dimensions))
            return

        ag_x = []
        ag_y = []
        agentCat = []
        for ag in self.agents:
            # if (len(Helper.getWinner(ag.pm)) > 1):
            #     print("an agent is torn between multiple options!")
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

        if(printMiddle):
            mc = self.computeMiddleCoordOfAgents()
            x = mc[0]
            y = mc[1]
            plt.scatter(x, y, s=40, color="black")

            mc, points = self.computeGraphicWithOutlierPunishing(retPoints=True)
            x = mc[0]
            y = mc[1]
            plt.scatter(x, y, s=20, color="gray")
            for p in points:
                plt.scatter(p[0], p[1], s=10, color="red")

            mc, points = self.computeGraphicWithOutlierPunishingCircle(retPoints=True)
            x = mc[0]
            y = mc[1]
            plt.scatter(x, y, s=20, color="darkgreen")
            for p in points:
                plt.scatter(p[0], p[1], s=10, color="green")

        for i, txt in enumerate(op_names):
            plt.annotate(txt, xy=(op_x[i], op_y[i]), xytext=(op_x[i]-2*scale, op_y[i]-2*scale))

        plt.xlim([-dimensionSize, dimensionSize])
        plt.ylim([-dimensionSize, dimensionSize])

        # plt.savefig("elecPlot{}.png".format(int(time())), dpi=300)

        if (show):
            plt.show()



    def print_elec_table(self, linear= False, trueLin=False, true=False, dist=False):


        if(len(self.agents) > 5):
            print("Too many agents to fit into table")
            return

        column_labels = []
        data = []
        _, ax = plt.subplots(1, 1)
        for i, ag in enumerate(self.agents):
            PM = ag.pm
            if (true):
                PM = ag.truePM
            if(linear):
                PM = ag.linearPM
            if(trueLin):
                PM = ag.truelinPM
            if (dist):
                PM = ag.distPM
            column_labels.append("ag" + str(i))
            data.append([round(num, 3) for num in list(PM.values())])
        data = np.array(data).T.tolist()
        df = pd.DataFrame(data, columns=column_labels)
        ax.axis('tight')
        ax.axis('off')
        tab = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=list(self.agents[0].pm.keys()),
                       loc="center")
        tab.auto_set_font_size(False)
        tab.set_fontsize(6)
        tab.scale(1.1, 1)

        plt.savefig("elecTable.png", dpi=300)
        plt.show()






    def print_result_table(self, title= "", rounded=True, show=True, ax=None):

        result_list = self.computeAllResults()

        column_labels = []
        data = []




        if(ax == None):
            _, ax = plt.subplots(1, 1)
        for res in result_list:
            column_labels.append(res.short_kind_of_eval)
            # data.append([round(num, 3) for num in list(res.ranking.values())])
            data.append([round(num, 3) for num in list(res.normalizedRanking.values())])
        #     data.append([round(abs, 3) + "(" + round(rel, 3) + ")" for num, rel in zip(list(res.ranking.values()), list(res.normalizedRanking.values()))])
        data = np.array(data).T.tolist()
        # print(data)
        df = pd.DataFrame(data, columns=column_labels)
        ax.axis('tight')
        ax.axis('off')
        # print(list(result_list[0].ranking.keys()))
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
            # print("new res ", i)

            for win in Helper.getWinner(res.normalizedRanking):
                # Highlight the cell to draw attention to it

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

        # plt.savefig("table.png", dpi=300)

        if (show):
            plt.title(title)
            plt.show()

        return ax



    def make_result_graphic(self):

        ax1 = plt.subplot(2, 2, 1)
        self.print_election_plot(colorPlurality=True, show=False, scale=2)
        ax1.set_aspect('equal')

        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)
        ax2 = plt.subplot(2,2,2)
        self.print_election_plot(colorWeighted=True, show=False, scale =2)
        ax2.set_aspect('equal')
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)

        self.print_result_table(show=False, ax=plt.subplot(2,1,2))
        plt.savefig("elecGraphic.png", dpi=1000, bbox_inches='tight')

        plt.show()


    def computeBallotResult(self, kind="WR"):

        if(kind == "RC"):
            return self.computeBallotResultRC()
        if(kind == "GR"):
            return self.computeGraphic()
        if (kind == "GRP"):
            return self.computeGraphicWithOutlierPunishing()
        return self.computeAdditiveResults(kind)

    def computeAdditiveResults(self, kind="WR"):
        result = Helper.getEmptyDict(list(self.agents[0].pm.keys()))
        for ag in self.agents:
            for opName, score in ag.getBallot(kind=kind).items():
                result[opName] += score
        return ElectionResult(result, kind)

    def computeMiddleCoordOfAgents(self):

        middleCords = [0] * len(self.issue.dimensions)
        for i in range(len(self.issue.dimensions)):
            for ag in self.agents:
                middleCords[i] += ag.coordinates[i] / len(self.agents)
        return middleCords

    def computeGraphic(self):
        middleCords = self.computeMiddleCoordOfAgents()

        agent = Agent(middleCords, self.issue)
        return ElectionResult(agent.pm, "GR")

    def computeGraphicWithOutlierPunishing(self, retPoints=False):
        middleCoords = self.computeMiddleCoordOfAgents()
        newPoints = []
        for ag in self.agents:
            dist = ag.computeDistancePoint(middleCoords)
            rtdist = dist**0.5
            vecFromMidToAgWithLength1 = [(ag.coordinates[i] - middleCoords[i])/dist for i in range(len(middleCoords))]
            newPoint = [middleCoords[i] + vecFromMidToAgWithLength1[i]*rtdist for i in range(len(middleCoords))]
            newPoints.append(newPoint)

        trueMiddleCords = [0] * len(self.issue.dimensions)
        for i in range(len(self.issue.dimensions)):
            for newPoint in newPoints:
                trueMiddleCords[i] += newPoint[i] / len(newPoints)
        agent = Agent(trueMiddleCords, self.issue)

        if (retPoints):
            return trueMiddleCords, newPoints
        return ElectionResult(agent.linearPM, "GRP")

    def computeGraphicWithOutlierPunishingCircle(self,  retPoints=False):
        middleCoords = self.computeMiddleCoordOfAgents()
        totalDist = 0
        newPoints = []
        for ag in self.agents:
            totalDist += ag.computeDistancePoint(middleCoords)
        meanDist = totalDist/len(self.agents)
        for ag in self.agents:
            dist = ag.computeDistancePoint(middleCoords)
            vecFromMidToAgWithLength1 = [(ag.coordinates[i] - middleCoords[i]) / dist for i in range(len(middleCoords))]
            newPoint = [middleCoords[i] + vecFromMidToAgWithLength1[i]*meanDist for i in range(len(middleCoords))]
            newPoints.append(newPoint)

        trueMiddleCords = [0] * len(self.issue.dimensions)
        for i in range(len(self.issue.dimensions)):
            for newPoint in newPoints:
                trueMiddleCords[i] += newPoint[i] / len(newPoints)
        agent = Agent(trueMiddleCords, self.issue)
        if(retPoints):
            return trueMiddleCords, newPoints
        return ElectionResult(agent.pm, "GRPC")






    def computeBallotResultRC(self):

        noWinner = True
        lostOptions = []
        while(noWinner):
            result = Helper.getEmptyDict(list(self.agents[0].pm.keys()))
            for ag in self.agents:
                if(ag.getRankedChoicePick(lostOptions) == None):
                    pass
                result[ag.getRankedChoicePick(lostOptions)] += 1
            winners = Helper.getWinner(result)
            normResult = Helper.normalizeDict(result)
            if(normResult[winners[0]] > 0.5):
                return ElectionResult(result, "RC")
            looser = Helper.getLooser(result, disregardedOptions=lostOptions)
            if(len(looser)>1):
                if(len(looser)==len(result)): # There is no winner and there won't be one
                    return ElectionResult(result, "RC")
                lostOptions.extend(looser)
                if (len(lostOptions) == len(result)):  # There is no winner and there won't be one
                    return ElectionResult(result, "RC")
                # print("We have a tie in RC!")
            else:
                lostOptions.append(looser[0])
            if (len(lostOptions) == len(result)):  # There is no winner and there won't be one
                print("Something went wrong in computeBallotResultRC")
                return ElectionResult(result, "RC")










            #Old methods for computing results:


    # def computeResult(self, kind="WR"):
    #
    #     if (kind == "WR"):
    #         return self.computeResultWR()
    #     if (kind == "WAR"):
    #         return self.computeResultWAR()
    #     if (kind == "AV"):
    #         return self.computeResultAV()
    #     if (kind == "RC"):
    #         return self.computeResultRC()
    #     if (kind == "PL"):
    #         return self.computeResultPlurality()
    #     if (kind == "WLR"):
    #         return self.computeResultWLR()
    #     if (kind == "WALR"):
    #         return self.computeResultWAR(linear=True)
    #
    # def computeResultWR(self):  # Weighted Ranking
    #     common_PM = {}
    #     for op in self.issue.options:
    #         common_PM[op.name] = 0
    #         for ag in self.agents:
    #             common_PM[op.name] += ag.pm[op.name]
    #
    #     return ElectionResult(common_PM, "WR")
    #
    # def computeResultWLR(self):  # Weighted Linear Ranking
    #     common_lin_PM = {}
    #     for op in self.issue.options:
    #         common_lin_PM[op.name] = 0
    #         for ag in self.agents:
    #             common_lin_PM[op.name] += ag.linearPM[op.name]
    #
    #     return ElectionResult(common_lin_PM, "WLR")
    #
    # def computeResultWAR(self, linear=FALSE):  # Weighted Approval Ranking
    #     # print("results of weighted ranking: ")
    #     shortName = "WAR"
    #     if (linear):
    #         shortName = "WALR"
    #     common_PM = {}
    #     for op in self.issue.options:
    #         common_PM[op.name] = 0
    #         for ag in self.agents:
    #             # scale the agents pm so that the highes option is set to exactly 1:
    #             highestScore = 0
    #             items = ag.pm.items()
    #             if (linear):
    #                 items = ag.linearPM.items()
    #             for (option, score) in items:
    #                 if (score > highestScore):
    #                     highestScore = score
    #             if (linear):
    #                 common_PM[op.name] += (ag.linearPM[op.name] * 1 / highestScore)
    #             else:
    #                 common_PM[op.name] += (ag.pm[op.name] * 1 / highestScore)
    #
    #     return ElectionResult(common_PM, shortName)
    #
    # def computeResultPlurality(self):  # Plurality
    #     voteScore = {}
    #     for op in self.issue.options:
    #         voteScore[op.name] = 0
    #     for ag in self.agents:
    #         winning_options = Helper.getWinner(ag.pm)
    #         for wo in winning_options:
    #             voteScore[wo] += 1 / len(winning_options)  # even though its not at all how Plurality
    #         # voting works in real life it most closely resembles the result of real Plurality voting,
    #         # where each voter would make a semi random choice about what option to choose
    #     return ElectionResult(voteScore, "PL")
    #
    # def computeResultRC(self):  # Ranked Choice
    #     disregardedOptions = []
    #     while (True):
    #         voteScore = {}
    #         for op in self.issue.options:
    #             voteScore[op.name] = 0
    #         for ag in self.agents:
    #             # print("ag")
    #             winning_options = Helper.getWinner(ag.pm, disregardedOptions=disregardedOptions)
    #             for wo in winning_options:
    #                 voteScore[wo] += 1 / len(winning_options)
    #                 # print(voteScore, "voteScore")
    #
    #         voteScore = Helper.normalizeDict(voteScore)
    #         # print(voteScore)
    #         lowestScore = 0.9
    #         lowestOption = ""
    #         for (option, score) in voteScore.items():
    #             if (option not in disregardedOptions):
    #                 # print(option, " is not part of ", disregardedOptions)
    #                 if (score < lowestScore):
    #                     lowestOption = option
    #                     lowestScore = score
    #
    #                 if (score > 0.5):
    #                     return ElectionResult(voteScore, "RC")
    #
    #         # print(lowestOption, " was the lowest option")
    #         disregardedOptions.append(lowestOption)
    #
    # def computeResultAV(self, percentOfOptionsToApproveOf=0.5, cutOffScore=None):  # Approval Voting
    #     if (cutOffScore != None):
    #         # The cutOffScore must be given independant of the number of choices.
    #         # A cutoff score of 0 means that we approve an option as long as it scores better than the mean. 0 -> 1/5
    #         # A cut off score of 1 means we approve all options, one of -1 means we approve of none. 1-> 0; -1 -> 1
    #         length = len(self.issue.options)
    #         if (cutOffScore < 0):
    #             cutOff = 1 / length - cutOffScore * (length - 1) / length
    #         else:
    #             cutOff = 1 / length - cutOffScore * 1 / length
    #         print(cutOff, cutOffScore)
    #         voteScore = {}
    #         for op in self.issue.options:
    #             voteScore[op.name] = 0
    #         for ag in self.agents:
    #             for (opName, score) in ag.pm.items():
    #                 if (score >= cutOff):
    #                     voteScore[opName] += 1
    #         return ElectionResult(voteScore, "AV")
    #
    #
    #
    #
    #     else:
    #         voteScore = {}
    #         for op in self.issue.options:
    #             voteScore[op.name] = 0
    #         for ag in self.agents:
    #             approved_options = Helper.getApproved(ag.pm, percentOfOptionsToApproveOf)
    #             for ao in approved_options:
    #                 voteScore[ao] += 1
    #         return ElectionResult(voteScore, "AV")
    #


def initializeRandomElection(numOptions, numAgents, numDimensions):
    return initializeElection(numOptions, numAgents, numDimensions)

def initializeElection(numOptions, numAgents, numDimensions,
                       centerPoints=None):  # CenterPoints is a list of tuples with likelihoods and points (points are also tuple)

    issue = makeIssue(makeRandomOptions(numOptions, numDimensions), numDimensions)

    if (centerPoints != None):
        agents = issue.getCenterPointAgents(centerPoints, numAgents)

    else:
        agents = issue.getRandomAgents(numAgents)

    return Election(issue, agents)

def makeRandomOptions(numOptions, numDimensions):
    options = []
    for i in range(numOptions):
        op = Option(makeRandomCoordinates(numDimensions))
        options.append(op)

    return options

def makeIssue(options, numDimensions):

    dimensions = []
    for i in range(numDimensions):
        dimensions.append("dim" + 'i')
    issue = Issue(options, dimensions)
    return issue

def makeElectionWithAgentBlocks(issue, agentBlocks):
    agents = []
    for ab in agentBlocks:
        agents.extend(ab.agents)
    return Election(issue, agents, agentBlocks)
