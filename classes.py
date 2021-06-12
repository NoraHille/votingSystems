
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import pandas as pd
import math
import string
import random


# Todo:
# - show absolute as well as relative values
# - investigate different approval voting scores
# - color landscape plot according to plurality score
# - Simulate strategic voting -> Come up with a score
# - Testing! You need to be CERTAIN everything is right!

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

    def create_linear_PM(self, issue):
        pm = {}
        sumOfDist = 0;
        for op in issue.options:

            dist = self.computeDistance(op)
            if(dist == 0):
                dist = 0.0000000001
            pref = dist
            pm[op.name] = pref;
            sumOfDist += dist;
        #linearly invert


        sum_of_inv_preferences = 0
        for (op_name, pref) in pm.items():
            inverted_pref = sumOfDist - pref
            pm[op_name] = inverted_pref
            sum_of_inv_preferences += inverted_pref


        #normalize PM so it adds up to 1
        sum_of_preferences = 0
        for (op_name, pref) in pm.items():
            normalized_pref = pref/sum_of_inv_preferences
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
        self.ranking = ranking
        self.normalizedRanking = Helper.normalizeDict(ranking)
        self.kind_of_eval = kind_of_eval




    def printResults(self):
        print("Using {} the winning option is {} and these are the normalized results {}. Absolute results: {}".format(self.kind_of_eval,
                                                                                                 Helper.getWinner(
                                                                                                     self.normalizedRanking), self.normalizedRanking, self.ranking))


class Election:
    def __init__(self, issue, agents):
        self.issue = issue
        self.agents = agents

    def computeAllResults(self):
        result_list = []
        result_list.append(self.computeResultPlurality())
        result_list.append(self.computeResultRC())
        result_list.append(self.computeResultAV(cutOffScore=0))
        result_list.append(self.computeResultWR())
        result_list.append(self.computeResultWLR())
        result_list.append(self.computeResultWAR())
        result_list.append(self.computeResultWAR(linear=True))



        return result_list

    def print_election_plot(self, show=True):


        if(len(self.issue.dimensions) != 2):
            print("You tried to plot an election with more/less than 2 dimensions, namely ",len(self.issue.dimensions) )
            return



        op_x = []
        op_y = []
        op_names = []
        for op in self.issue.options:
            op_x.append(op.coordinates[0])
            op_y.append(op.coordinates[1])
            op_names.append(op.name)

        plt.scatter(op_x, op_y, color="red")

        ag_x = []
        ag_y = []
        for ag in self.agents:
            ag_x.append(ag.coordinates[0])
            ag_y.append(ag.coordinates[1])

        plt.scatter(ag_x, ag_y)

        for i, txt in enumerate(op_names):
            plt.annotate(txt, (op_x[i], op_y[i]))

        plt.xlim([-100, 100])
        plt.ylim([-100, 100])


        if(show):
            plt.show()


    def print_result_table(self, rounded= True):

        result_list = self.computeAllResults()

        column_labels = []
        data = []

        plt.figure(dpi=2000)

        fig, ax = plt.subplots(1, 1)
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
        tab = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=list(result_list[0].ranking.keys()), loc="center")
        tab.set_fontsize(40)

        #merging time



        # highlight winners
        for i, res in enumerate(result_list):
            print("new res ", i)

            for win in Helper.getWinner(res.normalizedRanking):

                # Highlight the cell to draw attention to it

                alphabet_string = string.ascii_uppercase
                alphabet_list = list(alphabet_string)
                print(win)
                the_cell = tab[alphabet_list.index(win)+1,i]
                # the_cell = tab[1, 2]
                the_cell.set_facecolor('palegreen')
                # the_cell.set_edgecolor('black')
                # the_cell.set_linewidth(2)
                the_text = the_cell.get_text()
                # the_text.set_weight('bold')
                # the_text.set_fontstyle('italic')
                # the_text.set_color(highlight_text_color)
                ax.add_patch(the_cell)


        plt.savefig("table.png", dpi = 300)



        plt.show()



    def computeResultWR(self): #Weighted Ranking
        # print("results of weighted ranking: ")
        common_PM = {}
        for op in self.issue.options:
            common_PM[op.name] = 0
            for ag in self.agents:
                common_PM[op.name] += ag.pm[op.name]

      #  print("added up PM: ")

        return ElectionResult(common_PM, "Weighted Ranking")

    def computeResultWLR(self):  # Weighted Linear Ranking
        common_lin_PM = {}
        for op in self.issue.options:
            common_lin_PM[op.name] = 0
            for ag in self.agents:
                common_lin_PM[op.name] += ag.linearPM[op.name]


        return ElectionResult(common_lin_PM, "Weighted Linear Ranking")

    def computeResultWAR(self, linear= FALSE ):  # Weighted Approval Ranking
       # print("results of weighted ranking: ")
        name = "Weighted Approval Ranking"
        if(linear):
            name = "Wei.App.Lin. Ranking"
        common_PM = {}
        for op in self.issue.options:
            common_PM[op.name] = 0
            for ag in self.agents:
                #scale the agents pm so that the highes option is set to exactly 1:
                highesScore = 0
                items = ag.pm.items()
                if(linear):
                    items = ag.linearPM.items()
                for (option, score) in items:
                    if(score > highesScore):
                        highesScore = score
                common_PM[op.name] += (ag.pm[op.name] * 1/highesScore)


        return ElectionResult(common_PM, name)


    def computeResultPlurality(self): #Plurality
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

    def computeResultRC(self): # Ranked Choice
        disregardedOptions = []
        while(True):
            voteScore = {}
            for op in self.issue.options:
                voteScore[op.name] = 0
            for ag in self.agents:
                # print("ag")
                winning_options = Helper.getWinner(ag.pm, disregardedOptions=disregardedOptions)
                for wo in winning_options:
                    voteScore[wo] += 1/len(winning_options)
                    # print(voteScore, "voteScore")

            voteScore = Helper.normalizeDict(voteScore)
            # print(voteScore)
            lowestScore = 0.9
            lowestOption = ""
            for (option, score) in voteScore.items():
                if(option not in disregardedOptions):
                    # print(option, " is not part of ", disregardedOptions)
                    if(score < lowestScore):
                        lowestOption = option
                        lowestScore = score

                    if(score > 0.5):
                        return ElectionResult(voteScore, "Ranked Choice")

            # print(lowestOption, " was the lowest option")
            disregardedOptions.append(lowestOption)

    def computeResultAV(self, percentOfOptionsToApproveOf = 0.5, cutOffScore= None):  # Approval Voting
        if(cutOffScore != None):
        #The cutOffScore must be given independant of the number of choices.
        # A cutoff score of 0 means that we approve an option as long as it scores better than the mean. 0 -> 1/5
        # A cut off score of 1 means we approve all options, one of -1 means we approve of none. 1-> 0; -1 -> 1
            length= len(self.issue.options)
            if(cutOffScore<0):
                cutOff = 1/length - cutOffScore*(length-1)/length
            else:
                cutOff = 1 / length - cutOffScore * 1/ length
            print(cutOff, cutOffScore)
            voteScore = {}
            for op in self.issue.options:
                voteScore[op.name] = 0
            for ag in self.agents:
                for (op, score) in ag.pm.items():
                    if(score >= cutOff):
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

    def getWinner(resultDict, disregardedOptions = []):
        bestOption = []
        # print(list(resultDict.keys())[0])
        for i in range(len(resultDict)):
            if (list(resultDict.keys())[i] not in disregardedOptions):
                bestOption.append(list(resultDict.keys())[i])
                break;
        for (option, result) in resultDict.items():
            if(option not in disregardedOptions):
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
        if(prefs == 0):
            return dict
        returnDict = {op_name : pref/prefs for op_name, pref in dict.items()}
        return returnDict

    def getApproved(diction, percentOfOprionsToApproveOf):
        sorted_dict = dict(sorted(diction.items(), key=lambda item: item[1], reverse=True))
        approved_options = []
        for i in range(int(len(diction)*percentOfOprionsToApproveOf)):
            approved_options.append(list(sorted_dict.keys())[i])
        return approved_options

def makeRandomCoordinates(numDimension, low=-100, high=100):
    randomlist = []
    for i in range(numDimension):
        n = random.uniform(low, high)
        randomlist.append(n)
    return randomlist

def makeAdjecentCoordinates(numDimension, point, standardDev=10, low=-100, high=100):
    randomlist = []
    for i in range(numDimension):
        ok= False
        while(not ok):
            n = np.random.normal(point[i], scale=standardDev)
            if(n<high and n>low):
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
            if(i>cp):
                currentIndex = num+1
        ag = Agent(makeAdjecentCoordinates(numDimensions, centerPoints[currentIndex][1]), issue)
        agents.append(ag)
    return agents

def initializeRandomElection(numOptions, numAgents, numDimensions):
    return initializeElection(numOptions, numAgents, numDimensions)


def initializeElection(numOptions, numAgents, numDimensions, centerPoints= None): #CenterPoints is a list of tuples with likelihoods and points (points are also tuple)
    options = []
    for i in range(numOptions):
        op = Option(makeRandomCoordinates(numDimensions))
        options.append(op)
    dimensions = []
    for i in range(numDimensions):
        dimensions.append("dim" + 'i')
    issue = Issue(options, dimensions)

    if(centerPoints != None):
        agents = getCenterPointAgents(centerPoints, numAgents, numDimensions, issue)

    else:
        agents = getRandomAgents(numAgents, numDimensions, issue)


    return Election(issue, agents)




def printDict(text, dict):
    print(text)
    for key, value in dict.items():
        print(key, ' : ', value)


def generateStrategicVoting(kind="WR", numOptions=5, numAgents=10):
    highestDifference = 0
    cutOffValue = 0.5
    rounds = 0
    while(True):
        election = initializeRandomElection(numOptions, numAgents, 2)

        for ag in election.agents:

            if(kind == "WR"):
                result = election.computeResultWR()
            if(kind == "WAR"):
                result = election.computeResultWAR()
            strategicAgent = ag
            initialCoordinates = strategicAgent.coordinates
            initialPM = strategicAgent.pm
            preferredOption = Helper.getWinner(strategicAgent.pm)[0]
            winningOption =  Helper.getWinner(result.normalizedRanking)[0]
            if(preferredOption == winningOption):
                break
            initialHappiness = result.normalizedRanking[preferredOption]


            optionsByName = [op.name for op in election.issue.options]
            newCoordinates = election.issue.options[optionsByName.index(preferredOption)].coordinates
            strategicAgent.setCoordinates(newCoordinates)
            newPM = strategicAgent.pm

            if (kind == "WR"):
                newResult = election.computeResultWR()
            if (kind == "WAR"):
                newResult = election.computeResultWAR()


            newHappiness = newResult.normalizedRanking[preferredOption]
            happinessIncrease = newHappiness - initialHappiness

            if(happinessIncrease>highestDifference):
                highestDifference = happinessIncrease




                data = []

                result.printResults()
                print("Agent has this initial PM", initialPM)
                data.append([round(num, 3) for num in list(initialPM.values())])
                data.append([round(num, 3) for num in list(result.normalizedRanking.values())])
                print(initialCoordinates, " -> ", strategicAgent.coordinates)
                newResult.printResults()
                print("Agent has this new PM", newPM)
                data.append([round(num, 3) for num in list(newPM.values())])
                data.append([round(num, 3) for num in list(newResult.normalizedRanking.values())])
                print("The happiness increased by ", happinessIncrease, "from ", initialHappiness, "to ", newHappiness)
                plt.subplot(2, 2, 2)  # row 1, col 2 index 2



                election.print_election_plot(show=False)
                # ax1.set_aspect('equal')
                strategicAgent.setCoordinates(initialCoordinates)
                plt.subplot(2, 2, 1)  # index 1


                if(kind == "WR"):
                    plt.title("Strategic Voting with Weighted Ranking", fontsize= 12)
                if (kind == "WAR"):
                    plt.title("Strategic Voting with Weighted Approval Ranking", fontsize= 12)

                election.print_election_plot(show=False)
                # ax2.set_aspect('equal')

                ax = plt.subplot(2, 1, 2, visible= True)  # index 3

                column_labels = ["Agents Pref", "Result", "Agents Vote", "Result"]


                data = np.array(data).T.tolist()
                print(data, "DATA")
                df = pd.DataFrame(data, columns=column_labels)

                ax.axis('tight')
                ax.axis('off')
                tab = ax.table(cellText=df.values, colLabels=df.columns, rowLabels=list(result.ranking.keys()),
                               loc="center")
                # plt.subplot(2, 2, 4, visible= False)  # index 4

                plt.show()

                print("________________________________________________________________________________________________ \n \n")
                if(highestDifference>cutOffValue):
                    break
            strategicAgent.setCoordinates(initialCoordinates)
        rounds +=1
        if(rounds > 1000):
            print("Breaking now, rounds are up")
            break




    print("Best increase was", highestDifference)



