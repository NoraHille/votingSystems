from classes import Option, Issue, Agent, Election, initializeRandomElection, ElectionResult



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

if __name__ == '__main__':
    unittest.main()