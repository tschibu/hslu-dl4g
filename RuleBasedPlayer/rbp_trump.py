import numpy as np

from jass.base.const import color_masks, card_values, card_strings, PUSH, trump_strings_german_long
from jass.base.player_round import PlayerRound
from jass.player.player import Player

import RuleBasedPlayer.rbp_score as rbp_score

# Win Threshold: we want at least x score (otherwise we try to PUSH)
SCORE_TRESHOLD = (10 + rbp_score.PERFECT_WINS_FACTOR ) * 5  #minimum 5 perfect wins

def select_by_best_score(rnd: PlayerRound) -> int:
    """
    Target is to maximize the score
    """
    best_trump = None
    score = -10000

    for trump in range(0, 6):
        tmp_score = rbp_score.calculate_score(rnd, trumpToCheck=trump)

        if tmp_score > score:
            score = tmp_score
            best_trump = trump

    if rnd.forehand is None:
        #We could push if we want
        if score >= SCORE_TRESHOLD:
            print("Select Trump - Good Cards: {}, score: {}, cards: {}".format(trump_strings_german_long[best_trump], score, get_hand_str(rnd)))
            return best_trump
        else:
            print("Bad Cards, let's push...  score: {}, cards: {}".format(score, get_hand_str(rnd)))
            return PUSH #let's push if we have not enough score
    else:
        #We have to select :/
        print("Select Trump - We have to :( : {}, score: {}, cards: {}".format(trump_strings_german_long[best_trump], score, get_hand_str(rnd)))
        return best_trump

def get_hand_str(rnd: PlayerRound) -> str:
    hand_str = ""
    for i in range(0, 36):
        if rnd.hand[i] == 1:
            if hand_str != "":
                hand_str = hand_str + ", "

            hand_str = hand_str + card_strings[i]

    return hand_str