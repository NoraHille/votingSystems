from agentBlock import AgentBlock
from classes import Option, Issue, Agent
from Election import Election, initializeRandomElection, ElectionResult, makeElectionWithAgentBlocks, makeElectionFromLists
from Helper import Helper
from incompleteKnowledgeStratVoting import makeBallotForChangeVote
from strategicVoting import computePossibilityStratVote
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

    def test_is_dist_uneffected_by_scale(self):
        el = makeElectionFromLists([[10,30], [70, 50], [80, -20]], [[80, 40], [90,20], [20, -60]])
        smallEl = makeElectionFromLists([[1,3], [7, 5], [8, -2]], [[8, 4], [9,2], [2, -6]])
        self.assertNotEqual(el.computeBallotResult("WR").normalizedRanking, smallEl.computeBallotResult("WR").normalizedRanking)

    def test_makeBallotForChangeVote(self):
        op1 = Option([1, 2])
        op2 = Option([-50, 80])
        op3 = Option([-40, 70])

        issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
        ag1 = Agent([-50, 80], issue1)

        ballot = makeBallotForChangeVote(ag1, op3.name, kind="WAR")

        self.assertEqual(list(ballot.values()), [0,1,1])

        ballot = makeBallotForChangeVote(ag1, op3.name, kind="WR")

        self.assertEqual(list(ballot.values()), [0, 0, 1])






