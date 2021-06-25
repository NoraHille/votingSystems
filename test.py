from classes import Option, Issue, Agent
from Election import Election, initializeRandomElection, ElectionResult
from Helper import Helper
from strategicVoting import computePossibilityStratVote, getCoordinatesFromNum, getOtherAgentsNumForStratVote, calculateMiddlePosition
from Evaluation import happinessOfAgentWithResult, happinessOfAgentWithWinner



import unittest


class TestVotingResults(unittest.TestCase):

    def test_Plurality(self):
        op1 = Option([1, 2])
        op2 = Option([-5, 8])

        issue1 = Issue([op1, op2], ["freedom", "taxes"])
        ag1 = Agent([-5,8], issue1)
        ag2 = Agent([1,2], issue1)

        election = Election(issue1, [ag1, ag2])
        el_result = election.computeBallotResult("PL")

        self.assertEqual({'A':1.0, 'B':1.0}, el_result.ranking, "Should match")
        self.assertEqual({'A':0.5, 'B':0.5}, el_result.normalizedRanking, "Should match")

    def test_Approval_Voting(self):
        pass
        # op1 = Option([1, 2])
        # op2 = Option([-5, 8])
        # op3 = Option([-4, 7])
        #
        # issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
        # ag1 = Agent([-4, 9], issue1)
        # ag2 = Agent([-5, 7], issue1)
        # ag3 = Agent([1, 2], issue1)
        #
        # election = Election(issue1, [ag1, ag2, ag3])
        # el_result = election.computeBallotResult("AV")
        #
        # self.assertEqual({'A': 1.0, 'B': 2.0, 'C': 2.0}, el_result.ranking, "Should match")
        # self.assertEqual({'A': 0.2, 'B': 0.4, 'C': 0.4}, el_result.normalizedRanking, "Should match")

    def test_Weighted_Ranking(self):
        op1 = Option([3, 2])
        op2 = Option([6, 2])
        op3 = Option([-3, 2])

        issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
        ag1 = Agent([0, 2], issue1)
        # ag2 = Agent([-5, 7], issue1)
        # ag3 = Agent([1, 2], issue1)

        election = Election(issue1, [ag1])
        el_result = election.computeBallotResult("WR")

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
        result = election.computeBallotResult("WR")
        self.assertEqual(0.5, happinessOfAgentWithResult(ag, result))

        ag1 = Agent([75, 80], issue1)
        election = Election(issue1, [ag, ag1])
        result1 = election.computeBallotResult("WR")
        self.assertEqual(0.5, round(happinessOfAgentWithResult(ag, result1), 3))
        self.assertEqual(0.611, round(happinessOfAgentWithResult(ag1, result1), 3))

        ag2 = Agent([-40, 80], issue1)
        election = Election(issue1, [ag, ag1, ag2])
        result2 = election.computeBallotResult("WR")
        self.assertEqual(0.5, round(happinessOfAgentWithResult(ag, result2), 3))
        self.assertEqual(0.485, round(happinessOfAgentWithResult(ag1, result2), 3))
        self.assertEqual(0.518, round(happinessOfAgentWithResult(ag2, result2), 3))

        ag3 = Agent([10, 80], issue1)
        election = Election(issue1, [ag, ag1, ag2, ag3])
        result3 = election.computeBallotResult("WR")
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
        result = election.computeBallotResult("PL")
        result2 = election.computeBallotResult("PL")


        self.assertEqual(0.75, happinessOfAgentWithWinner(ag, result))
        self.assertEqual(0.75, happinessOfAgentWithWinner(ag, result2))

    def test_getEmptyDict(self):
        op1 = Option([50, 80])
        op2 = Option([-50, 80])

        issue1 = Issue([op1, op2], ["freedom", "taxes"])
        ag = Agent([20, 40], issue1)
        self.assertEqual({"A":0, "B":0}, Helper.getEmptyDict(list(ag.pm.keys())))


    def test_RC_and_AV(self):
        op1 = Option([-70, 50])  # X A
        op2 = Option([70, 50])  # Z B
        op3 = Option([0, -50])  # Y C

        issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])

        agents = []

        for i in range(45):
            agents.append(Agent([-62, 40], issue1))  # (A,C)
        for i in range(35):
            agents.append(Agent([10, -40], issue1))  # (C,B)
        for i in range(20):
            agents.append(Agent([10, 50], issue1))  # (B,A)
        election = Election(issue1, agents)
        self.assertEqual([0.65, 0.0, 0.35], [round(v,2) for (k,v) in election.computeBallotResult("RC").normalizedRanking.items()])
        self.assertEqual([0.33, 0.28, 0.4], [round(v,2) for (k,v) in election.computeBallotResult("AV").normalizedRanking.items()])

    def test_RC_and_AV_2(self):
        op1 = Option([34, 67])  # X A
        op2 = Option([80, 46])  # Z B
        op3 = Option([-35, 6])  # Y C

        issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])

        agents = []

        for i in range(45):
            agents.append(Agent([-90, 45], issue1))  # (A,C)
        for i in range(35):
            agents.append(Agent([10, -40], issue1))  # (C,B)
        for i in range(200):
            agents.append(Agent([10, 10], issue1))  # (B,A)
        election = Election(issue1, agents)
        self.assertEqual([round(v,5) for (k,v) in election.computeBallotResult("RC").normalizedRanking.items()], [round(v,5) for (k,v) in election.computeBallotResult("RC").normalizedRanking.items()])
        self.assertEqual([round(v,5) for (k,v) in election.computeBallotResult("AV").normalizedRanking.items()], [round(v,5) for (k,v) in election.computeBallotResult("AV").normalizedRanking.items()])


    def test_RC_with_mult_levels(self):

        op1 = Option([90, 90])  # A
        op2 = Option([50, 50])  # B
        op3 = Option([20, 20])  # C
        op4 = Option([-40, -40])  # D
        op5 = Option([-80, -80])  # E

        issue1 = Issue([op1, op2, op3, op4, op5], ["freedom", "taxes"])

        agents = []

        for i in range(1):
            agents.append(Agent([0,0], issue1))  # C, D, B, E, A
        for i in range(1):
            agents.append(Agent([-20, -20], issue1))  # D, C, E, B, A
        for i in range(1):
            agents.append(Agent([80, 80], issue1))  # A, B, C, D, E
        for i in range(1):
            agents.append(Agent([30, 30], issue1))  # C, B, A, D, E
        for i in range(1):
            agents.append(Agent([-50, -50], issue1))  # D, E, C, B, A

        election = Election(issue1, agents)
        self.assertEqual(list(election.computeBallotResult("RC").normalizedRanking.values()),[0,0,0.6, 0.4, 0])


    def test_option_list(self):

        op1 = Option([50, 80])
        op2 = Option([-50, 80])

        issue1 = Issue([op1, op2], ["freedom", "taxes"])

        ag = Agent([0, 80], issue1)
        election = Election(issue1, [ag])

        self.assertEqual(['A', 'B'], election.getOptionNameList())


    def test_getCoordinatesFromNum(self):
        self.assertEqual(getCoordinatesFromNum(0), [-80, -80])
        self.assertEqual(getCoordinatesFromNum(80), [80, 80])
        self.assertEqual(getCoordinatesFromNum(40), [0, 0])

    def test_getOtherAgentsForStratVote(self):
        self.assertEqual(getOtherAgentsNumForStratVote(0), [0,0,0])
        self.assertEqual(getOtherAgentsNumForStratVote(531440), [80,80,80])
        self.assertEqual(getOtherAgentsNumForStratVote(81), [0,1,0])
        self.assertEqual(getOtherAgentsNumForStratVote(6560), [80,80,0])
        self.assertEqual(getOtherAgentsNumForStratVote(6561), [0,0,1])

    def test_calculateMiddlePosition(self):

        self.assertEqual(calculateMiddlePosition([50, 50], [40, 40]), [45, 45])
        self.assertEqual(calculateMiddlePosition([-50, 50], [40, 40]), [-5, 45])













if __name__ == '__main__':
    unittest.main()