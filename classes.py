
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import math
import string
import random


class Issue(object):
    def __init__(self, options, dimensions):
        self.options = options # options is a list of options
        self.dimensions = dimensions # dimensions is a list of Strings
        alphabet_string = string.ascii_uppercase
        alphabet_list = list(alphabet_string)
        for i in range(len(options)):
            options[i].setName(alphabet_list[i])
            if len(options[i].coordinates) != len(dimensions):
                print("options has wrong number of dimensions")



class Option(object):
    def __init__(self, coordinates):
        self.coordinates = coordinates #coordinates is a list of real numbers, each number being associated with a dimension in the issue
    def setName(self, name):
        self.name = name

class Agent(object):
    def __init__(self, coordinates, issue):
        self.coordinates = coordinates #coordinates is a list of real numbers, each number being associated with a dimension in the issue
        self.pm = self.create_PM(issue)
    def create_PM(self, issue):
        pm = {}
        normalization_faktor = 0;
        for op in issue.options:

            dist = self.computeDistance(op)
            if(dist == 0):
                dist = 0.0000000001
            pref = pow(dist, -1)#raise to the power of -1 to make agents prefer the option with the lowest distance
            pm[op.name] = pref;
            normalization_faktor += pref;
        #normalize PM so it adds up to 1
        sum_of_preferences = 0
        for (op_name, pref) in pm.items():
            normalized_pref = pref/normalization_faktor
            pm[op_name] = normalized_pref
            sum_of_preferences += normalized_pref
        if(sum_of_preferences != 1):
            print("Something went wrong with the normalization, the normalized value is ", sum_of_preferences)
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
        self.normalizedRanking = Helper.normalizeDict(ranking)
        self.kind_of_eval = kind_of_eval




    def printResults(self):
        print("Using {} the winning option is {} and these are the normalized results {}".format(self.kind_of_eval,
                                                                                                 Helper.getWinner(
                                                                                                     self.normalizedRanking), self.normalizedRanking))


class Election:
    def __init__(self, issue, agents):
        self.issue = issue
        self.agents = agents



    def computeResultWR(self):
        print("results of weighted ranking: ")
        common_PM = {}
        for op in self.issue.options:
            common_PM[op.name] = 0
            for ag in self.agents:
                common_PM[op.name] += ag.pm[op.name]

      #  print("added up PM: ")

        return ElectionResult(common_PM, "Weighted Ranking")

    def computeResultPlurality(self):
        voteScore = {}
        for op in self.issue.options:
            voteScore[op.name] = 0
        for ag in self.agents:
            winning_options = Helper.getWinner(ag.pm)
            for wo in winning_options:
                voteScore[wo] += 1/len(winning_options)  #even though its not at all how Plurality
            # voting works in real life it most closely resembles the result of real Plurality voting,
            # where each voter would make a semi random choice about what option to choose
        return ElectionResult(voteScore, "Plurality")




class Helper:
    dimensionNames: ["taxamount", "freedom", "environment", "schoolfunding"]

    def getWinner(resultDict):
        bestOption = []
        # print(list(resultDict.keys())[0])
        bestOption.append(list(resultDict.keys())[0])
        for (option, result) in resultDict.items():
            if (resultDict[bestOption[0]] < result):
                bestOption[0] = option
            if (resultDict[bestOption[0]] == result and bestOption[0] != option):
                bestOption.append(option)
        return bestOption  # returns a list containing either the best option or all options that tie for best option

    def normalizeDict(dict):
        prefs = 0
        for (op_name, pref) in dict.items():
            prefs += pref
        # if prefs != len(self.agents):
        #     print("Something went wrong with the normalization. Values added up to: ", prefs)
        returnDict = {op_name : pref/prefs for op_name, pref in dict.items()}
        return returnDict

def makeRandomCoordinates(numDimension, low=-100, high=100):
    randomlist = []
    for i in range(numDimension):
        n = random.uniform(low, high)
        randomlist.append(n)
    return randomlist


def initializeRandomElection(numOptions, numAgents, numDimensions):
    options = []
    for i in range(numOptions):
        op = Option(makeRandomCoordinates(numDimensions))
        options.append(op)
    dimensions = []
    for i in range(numDimensions):
        dimensions.append("dim"+ 'i')
    issue = Issue(options, dimensions)
    agents = []
    for i in range(numAgents):
        ag = Agent(makeRandomCoordinates(numDimensions), issue)
        agents.append(ag)
    return Election(issue, agents)

def printDict(text, dict):
    print(text)
    for key, value in dict.items():
        print(key, ' : ', value)