import numpy as np

from jass.base.const import color_masks, card_values, PUSH, trump_strings_german_long
from jass.base.player_round import PlayerRound
from jass.player.player import Player

import RuleBasedPlayer.rbp_score as score

# Win Threshold: we want at least x wins (otherwise we try to PUSH)
WIN_TRESHOLD = 0

def select_by_best_score(rnd: PlayerRound) -> int:
    """
    Target is to maximize the score
    """
    wins = 0

    best_trump, wins = score.get_best_trump_and_wins(rnd.hand)

    #check obe
    wins_obe = score.get_wins_obe(rnd.hand)
    if wins_obe > wins:
        best_trump = 4 #obe is best trump now
        wins = wins_obe

    #check onde
    wins_unde = score.get_wins_onde(rnd.hand)
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
