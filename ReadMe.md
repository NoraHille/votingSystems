#Introduction 

In this project we can simulate elections and apply specific evaluation techniques to them. We can measure how good the result of the election through utilizing data about the happiness it leads to. 


#Functionality


##Elections 

In this project we can simulate elections, by defining agents (the voters) as well as options (the alternatives e.g. parties).
We start by defining an issue that has d different dimensions. Than we consider each agent and each options as a point within that d dimenional space. To create an election we now only need an issue as well as a list of options and agents. 

The class Election.py holds all the relevant data for the elections. 
In the file exampleElections.py you can find functions that return certain previously defined elections, with specific attributes. 


###Making Plots 

election.make_result_graphic() visualizes an election by coloring the agents according to where they would fall with Plurality and gives them ratio colors according to their vote in Weighted ranking (can be realized with election.print_election_plot()). It also provides you with a table that shows the score each option reached with each voting system (can be realized using election.print_result_table()).
election.print_elec_table() prints a table that shows the preference matrix of each agent (though only for elections with less than 5 agents). 



##Voting systems


We have implemented five different voting systems:
+ Plurality Voting (PL)
+ Approval Voting (AV)
+ Ranked Choice Voting (RC)
+ Weighted Ranking (WR)
+ Weighted Approval Ranking (WAR)

An election can be evaluated by a certain kind of voting system by calling election.computeBallotResult(kind). 
The function returns an ElectionResult object that contains the absolute as well as relatives scores each of the options has achieved. 
We also have to add an entry in Helper.kindDict, so that we can keep track of the abbreviation for that voting system. 

###Adding new voting systems
Additive voting systems can be easily added by writing a new case in the Agent.getBallot. For voting systems with more complicated evaluation stages (like Ranked Choice Voting) we must intercede in Election.computeBallotResult() and add a new case there. 



##Evaluation 

In Evaluation.py we can create tables that evaluate all the voting systems specified in kind_list with all the evaluation techniques listed in eval_list. 
For this we either call make_tie_normalized_Quality_table() for quality measures or make_tie_normalized_Var_table for equality measures. Both functions normalize the values by dividing them through the value a voting system that always returns a tie would achieve. 

###Adding new evaluation techniques 

To add a new evaluation technique we need to add a case for it in Evaluation.computeHappinessWithResult() and in Evaluation.computeVarianceOfHappiness().

##Strategic voting (complete knowledge)

In strategicVoting.py we have two major functionalities: 

###Create Examples 

With generateStrategicVoting() and generateStrategicChangeVoting() we can generate example elections where agents can manipulate the vote by changing their position in the grid. 
We also get a graphic visualizing this effect (they can be made using makeStratVotingPlot()).

###Tally Strategiv Votes 

stratVotPosStats() considers a specified number of elections and returns the percentage of agents that could use over voting, change voting or failed at strategic voting despite trying. The results are visualized in two pie plots (one with agents that were contented one without) per voting system. 

##Strategic voting (incomplete knowledge)

incompleteKnowledgeStratVoting.StatOnIncomKnowStratVote() initializes an election with 5 random options and one agent.
    It than tries to find the optimal position (within the grid) for that agent (the position that brings them the higest happiness).
    It does that by using the original position as well as all the positions on top of each of the options
    and always trying out the mean of the current two best positions next. After doing this with a specified number of elections
     it returns (to the console) where the optimal positions were and whether any position that was not on an option could be improved by allowing the agent any ballot. 


#Tests

Tests can be found and added in test.py. 