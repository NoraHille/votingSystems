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


from agent import Agent

# Todo:
# - show absolute as well as relative values
# - investigate different approval voting scores
# - color landscape plot according to plurality score
# - Simulate strategic voting -> Come up with a score
# - Testing! You need to be CERTAIN everything is right!



class Issue(object):
    def __init__(self, options, dimensions):
        self.options = options  # options is a list of options
        self.dimensions = dimensions  # dimensions is a list of Strings

        for i in range(len(options)):
            options[i].setName(alphabet_list[i])
            if len(options[i].coordinates) != len(dimensions):
                print("options has wrong number of dimensions")
    def numDimensions(self):
        return len(self.dimensions)

    def getRandomAgents(self, numAgents):
        agents = []
        for i in range(numAgents):
            ag = Agent(makeRandomCoordinates(self.numDimensions()), self)
            agents.append(ag)
        return agents

    def getCenterPointAgents(self, centerPoints, numAgents):
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
            ag = Agent(makeAdjecentCoordinates(self.numDimensions(), centerPoints[currentIndex][1]), self)
            agents.append(ag)
        return agents


class Option(object):
    def __init__(self, coordinates):
        self.setCoordinates(
            coordinates)  # coordinates is a list of real numbers, each number being associated with a dimension in the issue

    def setName(self, name):
        self.name = name

    def setCoordinates(self, coordinates):
        self.coordinates = coordinates



class ElectionResult(object):
    def __init__(self, ranking, short_kind_of_eval):
        self.ranking = ranking
        self.normalizedRanking = Helper.normalizeDict(ranking)
        self.short_kind_of_eval = short_kind_of_eval
        self.kind_of_eval = kindDict[short_kind_of_eval]

    def printResults(self):
        print("Using {} the winning option is {} and these are the normalized results {}. Absolute results: {}".format(
            self.kind_of_eval,
            Helper.getWinner(
                self.normalizedRanking), self.normalizedRanking, self.ranking))




def makeAdjecentCoordinates(numDimension, point, standardDev=(float(dimensionSize)/5.0), low=-dimensionSize, high=dimensionSize):
    randomlist = []
    for i in range(numDimension):
        ok = False
        while (not ok):
            n = np.random.normal(point[i], scale=standardDev)
            if (n < high and n > low):
                randomlist.append(n)
                ok = True

    return randomlist


def makeRandomCoordinates(numDimension, low=-dimensionSize, high=dimensionSize):
    randomlist = []
    for i in range(numDimension):
        n = random.uniform(low, high)
        randomlist.append(n)
    return randomlist











# def printDict(text, dict):
#     print(text)
#     for key, value in dict.items():
#         print(key, ' : ', value)



