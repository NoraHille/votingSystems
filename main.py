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
from classes import Option, Issue, Agent, Election, initializeRandomElection, initializeElection



def print_hi(name):

    election = initializeElection(5, 100, 2, centerPoints=[(0.4, (5,5)), (0.3, (-30,-90)), (0.2, (-60,90)), (0.1, (80, -25))])
    election.print_result_table()
    election.print_election_plot()




    # Use a breakpoint in the code line below to debug your script.

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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# def genrateARandomElection(int countOfAgents, int countOfOptions):
