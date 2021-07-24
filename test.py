
from agentBlock import AgentBlock
from classes import Option, Issue, Agent
from Election import Election, initializeRandomElection, ElectionResult, makeElectionWithAgentBlocks, makeElectionFromLists
from Helper import Helper
from incompleteKnowledgeStratVoting import makeBallotForChangeVote



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



    def test_getEmptyDict(self):
        op1 = Option([50, 80])
        op2 = Option([-50, 80])

        issue1 = Issue([op1, op2], ["freedom", "taxes"])
        ag = Agent([20, 40], issue1)
        self.assertEqual({"A":0, "B":0}, Helper.getEmptyDict(list(ag.pm.keys())))



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
    def test_AV(self):
        op1 = Option([-70, 80])  # A
        op2 = Option([70, 80])  # B
        op3 = Option([20, -40])  # C

        issue1 = Issue([op1, op2, op3], ["freedom", "taxes"])
        agents = []
        agents.append(Agent([0, 80], issue1))
        agents.append(Agent([10, 80], issue1))
        agents.append(Agent([45, 20], issue1))
        agents.append(Agent([60, 80], issue1))
        el = Election(issue1, agents)
        self.assertEqual([2.0,4.0,1.0],
                         [round(v, 5) for (k, v) in el.computeBallotResult("AV").ranking.items()])

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


    def test_agentBlock(self):
        op1 = Option([-70, 80])  # A
        op2 = Option([70, 80])  # B
        op3 = Option([20, -80])  # C
        op4 = Option([50, -80])  # D

        issue1 = Issue([op1, op2, op3, op4], ["freedom", "taxes"])
        agent = Agent([50, -80], issue1)
        agentBlock = AgentBlock(agent, 20)
        election = makeElectionWithAgentBlocks(issue1, [agentBlock])
        res = election.computeBallotResult(kind="PL")
        winner1 = Helper.getWinner(res.normalizedRanking)
        agentBlock.changeCoordinates([-70, 80])
        res = election.computeBallotResult(kind="PL")
        winner2 = Helper.getWinner(res.normalizedRanking)

        self.assertEqual(['D'], winner1)
        self.assertEqual(['A'], winner2)



    def test_WAR_ballot(self):
        op1 = Option([1, 2])
        op2 = Option([-5, 8])

        issue1 = Issue([op1, op2], ["freedom", "taxes"])
        ag1 = Agent([-50, 80], issue1)


        warBallot = ag1.getWeightedApprovalBallot()

        self.assertEqual(1, warBallot[Helper.getWinner(warBallot)[0]])
        self.assertEqual(1, sum(list(ag1.pm.values())))



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
















if __name__ == '__main__':
    unittest.main()