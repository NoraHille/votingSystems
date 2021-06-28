# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
import math
import string
import random
import pandas as pd
from classes import Option, Issue
from agentBlock import AgentBlock
from agent import Agent
from Helper import Helper
from Election import Election, initializeRandomElection, makeElectionWithAgentBlocks, initializeElection
from strategicVoting import generateStrategicVoting, computePossibilityStratVote
from exampleElections import make_Election_1, make_small_Election, make_small_Election_1, make_circle_Election, make_spreaded_circle_Election, make_outlier_circle_Election, make_strat_Election_1, make_upperRightCoordsElec, make_Election_With_Extremes, make_Election_With_extreme_Extremes



def method():



    election = make_Election_With_extreme_Extremes()
    # election.make_result_graphic()
    election.print_election_plot(printMiddle=True)

    # election = initializeElection(5, 100, 2, centerPoints=[(0.9, (90,90)), (0.1, (-80, -30))])
    # election.make_result_graphic()



    # election = initializeElection(5, 100, 2, centerPoints=[(0.4, (5,5)), (0.3, (-30,-90)), (0.2, (-60,90)), (0.1, (80, -25))])
    # # election = initializeRandomElection(4, 500, 2)
    # # election.print_result_table()
    # # election.print_election_plot(colorWeighted=True, linear=False)
    #
    # election.make_result_graphic()



    # election.print_election_plot(show=True, colorPlurality=True)
    # plt.figure(dpi=2000)
    # election.print_result_table(show=False)



    # for kind in ["WR", "WAR", "AV", "RC", "PL", "WLR", "WALR"]:
    # for kind in ["WALR"]:
    #     generateStrategicVoting(kind=kind, numOptions=5, numAgents=2, iter=10000)


# Example for Arrows Theorem:
#     op1 = Option([-70,50]) #X A
#     op2 = Option([70, 50]) #Z B
#     op3 = Option([0, -50]) #Y C
#
#     issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
#
#     agents = []
#
#     for i in range(2): #(45):
#         agents.append(Agent([-62, 40], issue1)) #(A,C)
#     for i in range(3): #(35):
#         agents.append(Agent([10, -40], issue1)) #(C,B)
#     for i in range(2): #(20):
#         agents.append(Agent([10, 50], issue1)) #(B,A)
def difference_of_Weighted_VS():
    election = make_circle_Election()
    election.make_result_graphic()
    election.print_elec_table()
    election.print_elec_table(true=True)
    election.print_elec_table(linear=True)
    election.print_elec_table(trueLin=True)
    election.print_elec_table(dist=True)

    election = make_spreaded_circle_Election()
    election.make_result_graphic()
    election.print_elec_table()
    election.print_elec_table(true=True)
    election.print_elec_table(linear=True)
    election.print_elec_table(trueLin=True)
    election.print_elec_table(dist=True)

    election = make_outlier_circle_Election()
    election.make_result_graphic()
    election.print_elec_table()
    election.print_elec_table(true=True)
    election.print_elec_table(linear=True)
    election.print_elec_table(trueLin=True)
    election.print_elec_table(dist=True)


    # election = initializeRandomElection(5,100,2)
    # # election = Election(issue1, agents)
    # election.make_result_graphic()
    # election.print_elec_table()
#     print(agents[0].pm)
#     print(agents[20].pm)
#     print(agents[55].pm)


# Strategic Voting!
#     op1 = Option([10,20])
#     op2 = Option([-50, 80])
#     op3 = Option([50, -40])
#
#     issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
#     ag1 = Agent([-60,87], issue1)
#     ag2 = Agent([59,-47], issue1)
#     ag4 = Agent([-62,79], issue1)
#     ag3 = Agent([-10,10], issue1)
#
#     # election = initializeRandomElection(5,100,3)
#     election = Election(issue1, [ag1, ag2, ag3, ag4])
#     election.print_election_plot(colorPlurality=True)



    # print(computePossibilityStratVote(election, "WR"))




# Example with a critical result:
#     op1 = Option([1,2])
#     op2 = Option([-5, 8])
#     op3 = Option([5, -4])
#
#     issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
#     ag1 = Agent([-5,8], issue1)
#     ag2 = Agent([5,-4], issue1)
#
#     # election = initializeRandomElection(5,100,3)
#     election = Election(issue1, [ag1, ag2])
#     election.print_election_plot(colorWeighted=True)
#     el_result = election.computeResultPlurality()
#     el_result.printResults()

# # Example with a good result:
#     op1 = Option([20,-10])
#     op2 = Option([-5, 8])
#     op3 = Option([-5, 6])
#
#     issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
#     ag1 = Agent([10,-8], issue1)
#     ag2 = Agent([-5,7], issue1)
#     ag3 = Agent([-5, 6.5], issue1)
#     ag4 = Agent([-5, 8], issue1)
#     ag5 = Agent([-5, 8], issue1)
#     ag6 = Agent([-5, 8], issue1)
#
#     # election = initializeRandomElection(5,100,3)
#     election = Election(issue1, [ag1, ag2, ag3])
#     el_result_list = election.computeAllResults()
#     for el_result in el_result_list:
#         el_result.printResults()
#     election.print_result_table()






# plot
#     x = [0, -3, 1, 1]
#     y = [0, 1, 0, 1]
#     # plot(x, y, '+')
#     # axis([-0.2, 1.2, -0.2, 1.2])
#
#     plt.scatter([1, 2, -3, 4], [0, -3, 1, 1])
#     plt.ylabel('some numbers')
#     plt.show()

# table

#
# fig, ax =plt.subplots(1,1)
# data=[[1,2,3],
#       [5,6,7],
#       [8,9,10]]
# column_labels=["Plurality", "Weighted Ranking", "Weightes Approval Ranking"]
# df=pd.DataFrame(data,columns=column_labels)
# ax.axis('tight')
# ax.axis('off')
# ax.table(cellText=df.values,colLabels=df.columns,rowLabels=["A","B","C"],loc="center")
#
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


if __name__ == '__main__':
    method()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


