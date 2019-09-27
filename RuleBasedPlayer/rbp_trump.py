import numpy as np

from jass.base.const import color_masks, card_values, PUSH, trump_strings_german_long
from jass.base.player_round import PlayerRound
from jass.player.player import Player

# Trump Index and Corrections
# ------------------------------A--K--Q--J-10--9--8--7--6
# ------------------------------0--1--2--3--4--5--6--7--8
BEST_TRUMP_INDEXES  = np.array([3, 5, 0, 1, 2, 4, 6, 7, 8])
START_SCORE = 9
SCORE_STEP = -1

#------------------D--H--S--C--Obe-Unde
SCORES = np.array([0, 0, 0, 0, 0, 0])

# Win Threshold: we want at least x wins (otherwise we try to PUSH)
WIN_TRESHOLD = 0

def select_by_best_score(rnd: PlayerRound) -> int:
    """
    Target is to maximize the score
    """
    wins = 0

    best_trump, wins = get_best_trump_and_wins(rnd.hand)

    #check obe
    wins_obe = get_wins_obe(rnd.hand)
    if wins_obe > wins:
        best_trump = 4 #obe is best trump now
        wins = wins_obe

    #check onde
    wins_unde = get_wins_onde(rnd.hand)
    if wins_unde > wins:
        best_trump = 5 #onde ist best trump now
        wins = wins_unde

    if rnd.forehand is None:
        #We could push if we want
        if wins >= WIN_TRESHOLD:
            print("Select Trump - Good Cards: {}, Wins: {}".format(trump_strings_german_long[best_trump], wins))
            return best_trump
        else:
            print("Bad Cards, let's push...  Wins: {}".format(wins))
            return PUSH #let's push if we have not enough wins
    else:
        #We have to select :/
        print("Select Trump - We have to :( : {}, Wins: {}".format(trump_strings_german_long[best_trump], wins))
        return best_trump

def get_best_trump_and_wins(hand: np.array) -> (int, int):
    best_trump = 0
    max_wins_trump = 0

    #check all different trumps (slice into array)
    for i in range(0, 4):
        wins = 0
        if i < 4:
            wins = get_wins_trump_single_color(hand[i*9:(i*9)+9])
            wins = wins + get_wins_obe(np.delete(hand, hand[i*9:(i*9)+9]))

            if wins > max_wins_trump:
                max_wins_trump = wins
                best_trump = i

            continue #next trump
        if i > 5:
            raise ValueError("Unsupported number of Trump types!")

        break #finished after last trump (obe / onde checked afterwards)

    return best_trump, max_wins_trump


def get_wins_trump_single_color(hand: np.array) -> int:
    if hand.size != 9:
        ValueError("get_wins_trump works only with one color: size = 8")

    score = 0
    score_value = START_SCORE
    for i in range(0, BEST_TRUMP_INDEXES.size):
        if hand[BEST_TRUMP_INDEXES[i]] == 1:
            score = score + score_value
        else:
            score = score - score_value

        score_value = score_value + SCORE_STEP

    return score

def get_wins_obe(hand: np.array) -> int:
    score = 0

    number_of_colors = int(hand.size / 9)
    for i in range(0, number_of_colors):
        score_value = START_SCORE

        cards_of_color = hand[i*9:(i*9)+9]
        for v in cards_of_color:
            if v == 1:
                score = score + score_value
            else:
                score = score - score_value

            score_value = score_value + SCORE_STEP

    return score

def get_wins_onde(hand: np.array) -> int:
    hand_reversed = np.flip(hand)
    return get_wins_obe(hand_reversed)

