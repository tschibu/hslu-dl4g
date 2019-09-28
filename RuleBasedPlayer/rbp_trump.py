import numpy as np

from jass.base.const import color_masks, card_values, PUSH, trump_strings_german_long
from jass.base.player_round import PlayerRound
from jass.player.player import Player

import RuleBasedPlayer.rbp_score as rbp_score

# Win Threshold: we want at least x score (otherwise we try to PUSH)
SCORE_TRESHOLD = -50

def select_by_best_score(rnd: PlayerRound) -> int:
    """
    Target is to maximize the score
    """
    score = -10000

    best_trump, score = rbp_score.get_best_trump_and_score(rnd.hand)

    #check obe
    score_obe = rbp_score.get_score_obe(rnd.hand)
    if score_obe > score:
        best_trump = 4 #obe is best trump now
        score = score_obe

    #check onde
    score_unde = rbp_score.get_score_onde(rnd.hand)
    if score_unde > score:
        best_trump = 5 #onde ist best trump now
        score = score_unde

    if rnd.forehand is None:
        #We could push if we want
        if score >= SCORE_TRESHOLD:
            print("Select Trump - Good Cards: {}, score: {}".format(trump_strings_german_long[best_trump], score))
            return best_trump
        else:
            print("Bad Cards, let's push...  score: {}".format(score))
            return PUSH #let's push if we have not enough score
    else:
        #We have to select :/
        print("Select Trump - We have to :( : {}, score: {}".format(trump_strings_german_long[best_trump], score))
        return best_trump
