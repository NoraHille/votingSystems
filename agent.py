from Helper import Helper, dimensionSize
import numpy as np
import string
import random
import math
import copy

class Agent(object):
    def __init__(self, coordinates, issue):
        self.setIssue(issue)
        self.setCoordinates(coordinates)
        self.base = 1/len(issue.options)
        self.numApp = None

    def setCoordinates(self, coordinates):
        self.coordinates = coordinates  # coordinates is a list of real numbers, each number being associated with a dimension in the issue
        self.pm = self.create_normalized_distance_PM()
        self.hm = self.create_distance_PM()
        self.linearPM = self.create_linear_PM(self.issue)
        # self.truelinPM = self.create_true_linear_PM(self.issue)
        # self.truePM = self.create_true_PM(self.issue)
        # self.distPM = self.create_distance_PM(self.issue)

    def setPM(self, pm):
        self.pm = pm

    def setNumApp(self, num):
        if(num == None):
            self.numApp = None
            return
        if(abs(num)<= len(self.issue.options)):
            self.numApp = num
        else:
            print("wrong numApp length in setNumApp")

    def setIssue(self, issue):
        self.issue = issue

    def create_PM(self, issue):
        pm = {}
        normalization_faktor = 0;
        for op in issue.options:

            dist = self.computeDistance(op)
            print(op.name, ":", dist)
            if (dist == 0):
                dist = 0.0000000000000000000000001
            pref = pow(dist, -1)  # raise to the power of -1 to make agents prefer the option with the lowest distance
            pm[op.name] = pref;
            normalization_faktor += pref;

        # print("classHapp", pm)
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
    #
    # def create_true_PM(self, issue):
    #     pm = {}
    #     normalization_faktor = 0;
    #     for op in issue.options:
    #
    #         dist = self.computeDistance(op)
    #         if (dist == 0):
    #             dist = 0.0000000000000000000000001
    #         pref = pow(dist, -1)  # raise to the power of -1 to make agents prefer the option with the lowest distance
    #         pm[op.name] = pref;
    #
    #     return pm
    #
    # def create_true_linear_PM(self, issue):
    #     pm = {}
    #     sumOfDist = 0;
    #     for op in issue.options:
    #
    #         dist = self.computeDistance(op)
    #         if (dist == 0):
    #             dist = 0.0000000001
    #         pref = dist
    #         pm[op.name] = pref;
    #         sumOfDist += dist;
    #     # linearly invert
    #
    #     for (op_name, pref) in pm.items():
    #         inverted_pref = sumOfDist - pref
    #         pm[op_name] = inverted_pref
    #
    #     return pm

    def create_linear_PM(self, issue):
        pm = {}
        sumOfDist = 0;
        for op in issue.options:

            dist = self.computeDistance(op)
            if(dist> sumOfDist):
                sumOfDist = dist
            if (dist == 0):
                dist = 0.0000000001
            pref = dist
            pm[op.name] = pref;
        #sumOfDist += dist;
        # linearly invert

        sum_of_inv_preferences = 0
        for (op_name, pref) in pm.items():
            inverted_pref = sumOfDist - pref
            pm[op_name] = inverted_pref
            sum_of_inv_preferences += inverted_pref

        # print("linHapp", pm)

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


    def create_normalized_distance_PM(self):
        pm = self.create_distance_PM()
        normPM = Helper.normalizeDict(pm)
        return normPM

    def create_distance_PM(self):

        pm = {}
        for op in self.issue.options:

            dist = self.computeDistance(op)
            pref = dist
            pm[op.name] = pref;
        maxDist = math.sqrt(2*((2*dimensionSize)**2))
        for (op_name, pref) in pm.items():
            inverted_pref = (maxDist - pref)
            pm[op_name] = inverted_pref



        return pm


    def computeDistance(self, option):
        dist = 0;
        for i in range(len(self.coordinates)):
            dist += pow(self.coordinates[i] - option.coordinates[i], 2)
        return math.sqrt(dist)

    def computeDistancePoint(self, point):
        dist = 0;
        for i in range(len(self.coordinates)):
            dist += pow(self.coordinates[i] - point[i], 2)
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
        if (kind == "HR"):
            return self.getHappinessBallot()
        # if (kind == "HLR"):
        #     return self.getLinHappinessBallot()
        # if (kind == "Dist"):
        #     return self.getDistBallot()



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

        # if(self.numApp != None):
        #
        #     sortBallot = Helper.sortDictDescending(ballot)
        #
        #     if(self.numApp > 0):
        #         for num, (key, value) in enumerate(sortBallot.items()):
        #             if(self.numApp > num):
        #                 ballot[key] = 1
        #     if (self.numApp < 0):
        #         for num, (key, value) in enumerate(sortBallot.items()):
        #             if (len(ballot) + self.numApp <= num):
        #                 ballot[key] = 0


        if (self.numApp != None):
            sortPM = Helper.sortDictDescending(self.pm)
            ballot = Helper.getEmptyDict(list(self.pm.keys()))
            for num, (opName, score) in enumerate(sortPM.items()):
                if (num < self.numApp):
                    ballot[opName] = 1
            return ballot


        return ballot


    #we don't wont anyone to choose one option and not another one simply because they are
    # later in the alphabet

    def getApprovalBallot(self, fractionOfChosenOptions = None):

        sortPM = Helper.sortDictDescending(self.pm)
        ballot = Helper.getEmptyDict(list(self.pm.keys()))

        if(self.numApp != None):
            for num, (opName, score) in enumerate(sortPM.items()):
                if (num < self.numApp):
                    ballot[opName] = 1
            return ballot

        if(fractionOfChosenOptions):
            for num, (opName, score) in enumerate(sortPM.items()):
                if(num< len(sortPM.items())*fractionOfChosenOptions):
                    ballot[opName]= 1
            return ballot

        for (opName, score) in sortPM.items():
            if(score>self.base):
                ballot[opName] = 1

        return ballot

    def getHappinessBallot(self):


        return self.create_distance_PM()


    # def getHappinessBallot(self):
    #     return self.truePM
    #
    # def getLinHappinessBallot(self):
    #     return self.truelinPM
    #
    # def getDistBallot(self):
    #     return self.distPM



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


