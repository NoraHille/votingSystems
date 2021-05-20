# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

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
            pm[op.name] = dist;
            normalization_faktor += dist;
        #normaliza PM so it adds up to 1
        sum_of_preferences = 0
        for (op_name, dist) in pm.items():
            normalized_pref = dist/normalization_faktor
            pm[op_name] = normalized_pref
            sum_of_preferences += normalized_pref
        if(sum_of_preferences != 1):
            print("Something went wrong with the normalization, the normalized value is ", sum_of_preferences)
        print("The PM of an agent is: ", pm)
        return pm

    def computeDistance(self, option):
        dist = 0;
        for i in range(len(self.coordinates)):
            dist += pow(self.coordinates[i] - option.coordinates[i], 2)
        return math.sqrt(dist)


def common_PM(args):
    pass


class Election:
    def __init__(self, issue, agents):
        self.issue = issue
        self.agents = agents

    def computeResult(self):
        commom_PM = {}
        commom_PM.update((op_name, 0) for op_name, pref in self.agents[0].pm.items())
        for op in self.issue.options:
            for ag in self.agents:
                commom_PM[op.name] += ag.pm[op.name]

        print(common_PM)
        #normalize
        prefs = 0
        for (op_name, pref) in commom_PM.items():
            prefs += pref
        if prefs != len(self.agents):
            print("Something went wrong with the common PM.")
        commom_PM.update((op_name, pref/prefs) for op_name, pref in commom_PM.items())
        print("Normalized PM: ", commom_PM)



class Helper:
    dimensionNames: ["taxamount", "freedom", "environment", "schoolfunding"]

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


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.


    # op1 = Option([1,2])
    # op2 = Option([-1, 8])
    # op3 = Option([5, -4])
    #
    # issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
    # ag1 = Agent([1,1], issue1)
    # ag2 = Agent([5,1], issue1)

    election = initializeRandomElection(3,10,3)
    election.computeResult()


    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


#plot
    # x = [0, -3, 1, 1]
    # y = [0, 1, 0, 1]
    # # plot(x, y, '+')
    # # axis([-0.2, 1.2, -0.2, 1.2])
    #
    # plt.scatter([1, 2, -3, 4], [0, -3, 1, 1])
    # plt.ylabel('some numbers')
    # plt.show()
#tkinter
    # root = Tk()
    #
    # # Creating a Label Widget
    # myLabel = Label(root, text="Hello World!")
    # # Shoving it onto the screen
    # myLabel.pack()
    #
    # root.mainloop()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/



