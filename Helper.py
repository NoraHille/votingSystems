import numpy as np
import string
import random
import math

colormap = np.array(['teal', 'purple', 'yellow', 'steelblue', 'green',  'pink', 'red', 'brown', 'gray'])
dimensionSize = 100
alphabet_string = string.ascii_uppercase + string.ascii_lowercase
alphabet_list = list(alphabet_string)
kindDict = {"WR": "Weighted Ranking", "WLR": "Weightes Linear Ranking", "AV": "Approval Voting", "PL": "Plurality Voting", "WAR": "Weighted Approval Ranking", "WALR": "Weighted Approval Linear Ranking", "RC": "Ranked Choice", "tie": "Base Tie", "GR": "Graphic", "GRP": "Graphic Punishing", "GRC": "Graphic Pun Cirl", "HR": "Happiness Ranking", "HLR": "lin Happiness Ranking", "Dist": "Distance"}




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

    def getLooser(resultDict, disregardedOptions=[]):
        worstOptions = []
        for i in range(len(resultDict)):
            if (list(resultDict.keys())[i] not in disregardedOptions):
                worstOptions.append(list(resultDict.keys())[i])
                break;
        for (optionName, score) in resultDict.items():
            if (optionName not in disregardedOptions):
                if (resultDict[worstOptions[0]] > score):
                    worstOptions = [optionName]
                if (resultDict[worstOptions[0]] == score and worstOptions[0] != optionName):
                    worstOptions.append(optionName)
        return worstOptions  # returns a list containing either the worst option or all options that tie for worst option



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
        for i in range(math.ceil(len(diction) * percentOfOprionsToApproveOf)):
            approved_options.append(list(sorted_dict.keys())[i])
        return approved_options

    def getEmptyDict(options):

        return dict(zip(options, [0] * len(options)))

    def sortDictDescending(diction):

        return dict(sorted(diction.items(), key=lambda item: item[1], reverse=True))


    def disregardLowestOption(self, PM):

        loosingScore = PM[Helper.getLooser(PM)[0]]
        for op, score in PM.items():
            PM[op] = score - loosingScore
        return Helper.normalizeDict(PM)
