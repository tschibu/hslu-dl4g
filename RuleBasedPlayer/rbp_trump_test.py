import unittest

import numpy as np
import RuleBasedPlayer.rbp_trump as rbp

#Trump Combinations ----------------A--K--Q--J-10--9--8--7--6
#-----------------------------------0--1--2--3--4--5--6--7--8
NO_TRUMP_ARRAY          = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
#Test one highest
J_TRUMP_ARRAY           = np.array([0, 0, 0, 1, 0, 0, 0, 0, 0])
#Test two highest
J_9_TRUMP_ARRAY         = np.array([0, 0, 0, 1, 0, 1, 0, 0, 0])
#Test tree highest
J_9_A_TRUMP_ARRAY       = np.array([1, 0, 0, 1, 0, 1, 0, 0, 0])
#Test tree highest and another one (will be ignored because of gap)
J_9_A_10_TRUMP_ARRAY    = np.array([1, 0, 0, 1, 1, 1, 0, 0, 0])
#Test 5 trump, will result in 2 win because of formula (see above)
A_10_8_7_6_TRUMP_ARRAY  = np.array([1, 0, 0, 0, 1, 0, 1, 1, 1])
#Test 4 trump, will result in 1 win because of formula (see above)
A_10_8_7_TRUMP_ARRAY    = np.array([1, 0, 0, 0, 1, 0, 1, 1, 0])
#Test 3 trump, will result in 0 win because of formula (see above)
A_10_8_TRUMP_ARRAY    = np.array([0, 0, 0, 0, 1, 0, 1, 0, 0])

#Obe Combinations
OBE_ONE_COLOR_GOOD  =   np.array([1, 1, 0, 0, 0, 1, 1, 1, 1])
OBE_TWO_COLOR_GOOD  =   np.array([1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1])
OBE_ONE_COLOR_BAD   =   np.array([0, 1, 0, 0, 0, 1, 1, 1, 1])
OBE_TWO_COLOR_BAD   =   np.array([0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1])
#Unde Combinations
UNDE_ONE_COLOR_GOOD =   np.array([1, 1, 0, 0, 0, 0, 1, 1, 1])
UNDE_TWO_COLOR_GOOD =   np.array([1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1])
UNDE_ONE_COLOR_BAD  =   np.array([1, 1, 0, 0, 0, 0, 1, 1, 0])
UNDE_TWO_COLOR_BAD  =   np.array([1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0])

class RuleBasePlayerTest(unittest.TestCase):
    # Trump Tests

    def test_get_wins_trump_when_no_trump(self):
        """We have no trump :("""
        self.assertTrue(0 == rbp.get_wins_trump_single_color(NO_TRUMP_ARRAY))

    def test_get_wins_trump_when_only_J_trump(self):
        self.assertTrue(1 == rbp.get_wins_trump_single_color(J_TRUMP_ARRAY))

    def test_get_wins_trump_when_J_9_trump(self):
        self.assertTrue(2 == rbp.get_wins_trump_single_color(J_9_TRUMP_ARRAY))

    def test_get_wins_trump_when_J_9_A_trump(self):
        self.assertTrue(3 == rbp.get_wins_trump_single_color(J_9_A_TRUMP_ARRAY))

    def test_get_wins_trump_when_J_9_A_10_trump(self):
        self.assertTrue(3 == rbp.get_wins_trump_single_color(J_9_A_10_TRUMP_ARRAY))

    def test_get_wins_trump_when_A_10_8_7_6_trump(self):
        self.assertTrue(3 == rbp.get_wins_trump_single_color(A_10_8_7_6_TRUMP_ARRAY))

    def test_get_wins_trump_when_A_10_8_7_trump(self):
        self.assertTrue(2 == rbp.get_wins_trump_single_color(A_10_8_7_TRUMP_ARRAY))

    def test_get_wins_trump_when_A_10_8_trump(self):
        self.assertTrue(0 == rbp.get_wins_trump_single_color(A_10_8_TRUMP_ARRAY))

    # Obe Wins Tests

    def test_get_wins_obe_one_color_good(self):
        self.assertTrue(2 == rbp.get_wins_obe(OBE_ONE_COLOR_GOOD))

    def test_get_wins_obe_two_color_good(self):
        self.assertTrue(4 == rbp.get_wins_obe(OBE_TWO_COLOR_GOOD))

    def test_get_wins_obe_one_color_bad(self):
        self.assertTrue(0 == rbp.get_wins_obe(OBE_ONE_COLOR_BAD))

    def test_get_wins_obe_two_color_bad(self):
        self.assertTrue(0 == rbp.get_wins_obe(OBE_TWO_COLOR_BAD))

    # Unde Wins Tests

    def test_get_wins_unde_one_color_good(self):
        self.assertTrue(3 == rbp.get_wins_onde(UNDE_ONE_COLOR_GOOD))

    def test_get_wins_unde_two_color_good(self):
        self.assertTrue(6 == rbp.get_wins_onde(UNDE_TWO_COLOR_GOOD))

    def test_get_wins_unde_one_color_bad(self):
        self.assertTrue(0 == rbp.get_wins_onde(UNDE_ONE_COLOR_BAD))

    def test_get_wins_unde_two_color_bad(self):
        self.assertTrue(0 == rbp.get_wins_onde(UNDE_TWO_COLOR_BAD))


if __name__ == 'main':
    unittest.main()