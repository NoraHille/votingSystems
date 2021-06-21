from Helper import Helper
import numpy as np
import string
import random
import math
import copy

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
                dist = 0.0000000000000000000000001
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

    def getBallot(self, kind="WR"):

        if(kind== "WR"):
            return self.pm
        if (kind == "WAR"):
            return self.getWeightedApprovalBallot()
        if (kind == "WALR"):
            return self.getWeightedApprovalBallot(linear=True)
        if (kind == "WLR"):
            return self.linearPM
        if (kind == "PL"):
            return self.getPluralityBallot()
        if (kind == "RC"):
            return self.getRankedChoiceBallot()
        if (kind == "AV"):
            return self.getApprovalBallot()



    def getPluralityBallot(self):
        winners = Helper.getWinner(self.pm)
        ballot = Helper.getEmptyDict(list(self.pm.keys()))
        for win in winners:
            ballot[win] = 1/len(winners)

        return ballot

    def getWeightedApprovalBallot(self, linear=False):
        PM = self.pm
        if(linear):
            PM = self.linearPM
        winner = Helper.getWinner(PM)[0]
        highestScore = PM[winner]
        ballot = copy.deepcopy(PM)
        for opName, score in ballot.items():
            ballot[opName] = score/highestScore
        if(ballot[winner] != 1):
            print("something went wrong with the approval ballot")
        return ballot


    #we don't wont anyone to choose one option and not another one simply because they are
    # later in the alphabet

    def getApprovalBallot(self, fractionOfChosenOptions = 0.5):

        sortPM = Helper.sortDictDescending(self.pm)
        ballot = Helper.getEmptyDict(list(self.pm.keys()))
        for num, (opName, score) in enumerate(sortPM.items()):
            if(num< len(sortPM.items())*fractionOfChosenOptions):
                ballot[opName]= 1
            # else:
            #     if(score == list(ballot.values())[-1]):
            #         ballot[opName] = 1
        return ballot

    def getRankedChoiceBallot(self):
        ballot = {}
        for num, (opName, score) in enumerate(Helper.sortDictDescending(self.pm).items()):

            ballot[opName] = num+1
        return ballot

    def getRankedChoicePick(self, lostOptions):
        ballot = self.getRankedChoiceBallot()
        for opName, score in ballot.items():
            if(opName not in lostOptions):
                return opName

