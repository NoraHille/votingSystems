from classes import Option, Issue, Agent, Election, initializeRandomElection, ElectionResult, happinessOfAgentWithResult, happinessOfAgentWithWinner
from strategicVoting import computePossibilityStratVote



import unittest


class TestVotingResults(unittest.TestCase):

    def test_Plurality(self):
        op1 = Option([1, 2])
        op2 = Option([-5, 8])

        issue1 = Issue([op1, op2], ["freedom", "taxes"])
        ag1 = Agent([-5,8], issue1)
        ag2 = Agent([1,2], issue1)

        election = Election(issue1, [ag1, ag2])
        el_result = election.computeResultPlurality()

        self.assertEqual({'A':1.0, 'B':1.0}, el_result.ranking, "Should match")
        self.assertEqual({'A':0.5, 'B':0.5}, el_result.normalizedRanking, "Should match")

    def test_Approval_Voting(self):
        op1 = Option([1, 2])
        op2 = Option([-5, 8])
        op3 = Option([-4, 7])

        issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
        ag1 = Agent([-4, 9], issue1)
        ag2 = Agent([-5, 7], issue1)
        ag3 = Agent([1, 2], issue1)

        election = Election(issue1, [ag1, ag2, ag3])
        el_result = election.computeResultAV(cutOffScore=0)

        self.assertEqual({'A': 1.0, 'B': 2.0, 'C': 2.0}, el_result.ranking, "Should match")
        self.assertEqual({'A': 0.2, 'B': 0.4, 'C': 0.4}, el_result.normalizedRanking, "Should match")

    def test_Weighted_Ranking(self):
        op1 = Option([3, 2])
        op2 = Option([6, 2])
        op3 = Option([-3, 2])

        issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
        ag1 = Agent([0, 2], issue1)
        # ag2 = Agent([-5, 7], issue1)
        # ag3 = Agent([1, 2], issue1)

        election = Election(issue1, [ag1])
        el_result = election.computeResultWR()

        # self.assertEqual({'A': 2.0, 'B': 1.0, 'C': 2.0}, el_result.ranking, "Should match")
        self.assertEqual({'A': 0.4, 'B': 0.2, 'C': 0.4}, el_result.normalizedRanking, "Should match")


    def test_threeBythreeTest(self):
        self.assertEqual(3, 3)

    def test_computePossibilityStratVote(self):
        op1 = Option([10, 20])
        op2 = Option([-50, 80])
        op3 = Option([50, -40])

        issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
        ag1 = Agent([-60, 87], issue1)
        ag2 = Agent([59, -47], issue1)
        ag3 = Agent([-62, 79], issue1)

        middle_ag_low = Agent([-10, -10], issue1)
        middle_ag_high = Agent([-10, 30], issue1)

        election = Election(issue1, [ag1, ag2, ag3, middle_ag_low])
        self.assertEqual([0,2,4,6], list(computePossibilityStratVote(election, "PL").values()))

        election2 = Election(issue1, [ag1, ag2, ag3, middle_ag_high])
        self.assertEqual([0, 1, 5, 6], list(computePossibilityStratVote(election2, "PL").values()))

    def test_Over_voters(self):
        op1 = Option([50, 80])
        op2 = Option([-50, 80])

        issue1 = Issue([op1, op2], ["freedom", "taxes"])

        ag1 = Agent([1, 80], issue1)
        ag2 = Agent([50, 80], issue1)
        ag3 = Agent([-50, 80], issue1)
        ag4 = Agent([-5, 80], issue1)

        election = Election(issue1, [ag1, ag2, ag3, ag4])
        self.assertEqual([1, 0, 3, 4], list(computePossibilityStratVote(election, "WR").values()))
        self.assertEqual([0, 0, 0, 8], list(computePossibilityStratVote(election, "PL").values()))

    def test_happinessOfAgentWithResult(self):
        op1 = Option([50, 80])
        op2 = Option([-50, 80])

        issue1 = Issue([op1, op2], ["freedom", "taxes"])

        ag = Agent([0, 80], issue1)
        election = Election(issue1, [ag])
        result = election.computeResultWR()
        print(result.normalizedRanking)
        self.assertEqual(0.5, happinessOfAgentWithResult(ag, result))

        ag1 = Agent([75, 80], issue1)
        election = Election(issue1, [ag, ag1])
        result1 = election.computeResultWR()
        print(result1.normalizedRanking)
        self.assertEqual(0.5, round(happinessOfAgentWithResult(ag, result1), 3))
        self.assertEqual(0.611, round(happinessOfAgentWithResult(ag1, result1), 3))

        ag2 = Agent([-40, 80], issue1)
        election = Election(issue1, [ag, ag1, ag2])
        result2 = election.computeResultWR()
        print(result2.normalizedRanking)
        self.assertEqual(0.5, round(happinessOfAgentWithResult(ag, result2), 3))
        self.assertEqual(0.485, round(happinessOfAgentWithResult(ag1, result2), 3))
        self.assertEqual(0.518, round(happinessOfAgentWithResult(ag2, result2), 3))

        ag3 = Agent([10, 80], issue1)
        election = Election(issue1, [ag, ag1, ag2, ag3])
        result3 = election.computeResultWR()
        print(result3.normalizedRanking)
        self.assertEqual(0.502, round(happinessOfAgentWithResult(ag3, result3), 3))

    def test_happinessOfAgentWithWinner(self):
        op1 = Option([50, 80])
        op2 = Option([-50, 80])

        issue1 = Issue([op1, op2], ["freedom", "taxes"])
        ag = Agent([-25, 80], issue1)
        ag1 = Agent([-45, 80], issue1)
        ag2 = Agent([-45, 80], issue1)
        ag3 = Agent([-45, 80], issue1)

        election = Election(issue1, [ag, ag1, ag2, ag3])
        result = election.computeResult("PL")
        result2 = election.computeResult("PL")


        self.assertEqual(0.75, happinessOfAgentWithWinner(ag, result))
        self.assertEqual(0.75, happinessOfAgentWithWinner(ag, result2))














if __name__ == '__main__':
    unittest.main()