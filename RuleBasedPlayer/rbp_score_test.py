import unittest

import numpy as np
import RuleBasedPlayer.rbp_score as score

#Trump Combinations ----------------A--K--Q--J-10--9--8--7--6
#Indexes----------------------------0--1--2--3--4--5--6--7--8
#Score Obe--------------------------9--8--7--6--5--4--3--2--1
#Score Unde-------------------------1--2--3--4--5--6--7--8--9
#Score Trump------------------------7--6--5--9--4--8--3--2--1
NO_TRUMP_ARRAY          = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
#Test one highest
J_TRUMP_ARRAY           = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0])
#Test two highest
J_9_TRUMP_ARRAY         = np.array([0, 0, 0, 1, 0, 1, 0, 0, 0])
#Test tree highest
J_9_A_TRUMP_ARRAY       = np.array([1, 0, 0, 1, 0, 1, 0, 0, 0])
#Test tree highest and another one
J_9_A_10_TRUMP_ARRAY    = np.array([1, 0, 0, 1, 1, 1, 0, 0, 0])
#Test 5 trump
A_10_8_7_6_TRUMP_ARRAY  = np.array([1, 0, 0, 0, 1, 0, 1, 1, 1])
#Test 4 trump
A_10_8_7_TRUMP_ARRAY    = np.array([1, 0, 0, 0, 1, 0, 1, 1, 0])
#Test 3 trump
A_10_8_TRUMP_ARRAY    = np.array([1, 0, 0, 0, 1, 0, 1, 0, 0])

#Obe Combinations
OBE_ONE_COLOR_GOOD  =   np.array([1, 1, 0, 0, 0, 1, 1, 1, 1])
OBE_ONE_COLOR_BAD   =   np.array([0, 1, 0, 0, 0, 1, 1, 1, 1])
#Unde Combinations
UNDE_ONE_COLOR_GOOD =   np.array([1, 1, 0, 0, 0, 0, 1, 1, 1])
UNDE_ONE_COLOR_BAD  =   np.array([1, 1, 0, 0, 0, 0, 1, 1, 0])

class RuleBasePlayerTest(unittest.TestCase):
    # Trump Tests

    def test_get_score_trump_when_no_trump(self):
        """We have no trump :("""
        self.assertTrue(0 == score.get_score_per_color_and_trump(NO_TRUMP_ARRAY, 0 , 0))

    def test_get_score_trump_when_only_J_trump(self):
        perfect_wins = 1
        self.assertTrue(1+(perfect_wins*score.PERFECT_WINS_FACTOR) ==
                        score.get_score_per_color_and_trump(J_TRUMP_ARRAY, 0, 0))

    def test_get_score_trump_when_J_9_trump(self):
        perfect_wins = 2
        self.assertTrue(2+(perfect_wins*score.PERFECT_WINS_FACTOR) ==
                        score.get_score_per_color_and_trump(J_9_TRUMP_ARRAY, 0, 0))

    def test_get_score_trump_when_J_9_A_trump(self):
        perfect_wins = 3
        self.assertTrue(3+(perfect_wins*score.PERFECT_WINS_FACTOR) ==
                        score.get_score_per_color_and_trump(J_9_A_TRUMP_ARRAY, 0, 0))

    def test_get_score_trump_when_J_9_A_10_trump(self):
        perfect_wins = 3
        self.assertTrue(4+(perfect_wins*score.PERFECT_WINS_FACTOR) ==
                        score.get_score_per_color_and_trump(J_9_A_10_TRUMP_ARRAY, 0, 0))

    def test_get_score_trump_when_A_10_8_7_6_trump(self):
        self.assertTrue(5 ==
                        score.get_score_per_color_and_trump(A_10_8_7_6_TRUMP_ARRAY, 0, 0))

    def test_get_score_trump_when_A_10_8_7_trump(self):
        self.assertTrue(4 ==
                        score.get_score_per_color_and_trump(A_10_8_7_TRUMP_ARRAY, 0, 0))

    def test_get_score_trump_when_A_10_8_trump(self):
        self.assertTrue(3 ==
                        score.get_score_per_color_and_trump(A_10_8_TRUMP_ARRAY, 0, 0))

    # Obe score Tests

    def test_get_score_obe_one_color_good(self):
        perfect_wins = 2
        self.assertTrue(6+(perfect_wins*score.PERFECT_WINS_FACTOR) ==
                        score.get_score_per_color_and_trump(OBE_ONE_COLOR_GOOD, 0, 1))

    def test_get_score_obe_one_color_bad(self):
        self.assertTrue(5 == score.get_score_per_color_and_trump(OBE_ONE_COLOR_BAD, 0, 1))

    # Unde score Tests

    def test_get_score_unde_one_color_good(self):
        perfect_wins = 3
        self.assertTrue(5+(perfect_wins*score.PERFECT_WINS_FACTOR) ==
                        score.get_score_per_color_and_trump(UNDE_ONE_COLOR_GOOD, 0, 2))

    def test_get_score_unde_one_color_bad(self):
        self.assertTrue(4 == score.get_score_per_color_and_trump(UNDE_ONE_COLOR_BAD, 0, 2))


if __name__ == 'main':
    unittest.main()