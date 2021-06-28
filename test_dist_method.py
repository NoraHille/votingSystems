from agentBlock import AgentBlock
from classes import Option, Issue, Agent
from Election import Election, initializeRandomElection, ElectionResult, makeElectionWithAgentBlocks
from Helper import Helper
from strategicVoting import computePossibilityStratVote, getCoordinatesFromNum, getOtherAgentsNumForStratVote, calculateMiddlePosition
from Evaluation import happinessOfAgentWithResult, happinessOfAgentWithWinner



import unittest


class TestDist(unittest.TestCase):

    def test_WAR_ballot(self):
        op1 = Option([1, 2])
        op2 = Option([-5, 8])

        issue1 = Issue([op1, op2], ["freedom", "taxes"])
        ag1 = Agent([-50, 80], issue1)


        warBallot = ag1.getWeightedApprovalBallot()

        self.assertEqual(1, warBallot[Helper.getWinner(warBallot)[0]])
        self.assertEqual(1, sum(list(ag1.pm.values())))

        self.assertNotEqual(warBallot, ag1.create_distance_PM(issue1))



