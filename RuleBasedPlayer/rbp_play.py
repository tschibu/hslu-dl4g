import numpy as np

from jass.base.player_round import PlayerRound
import RuleBasedPlayer.rbp_score as score


def play_card(rnd: PlayerRound) -> int:
    """
    Play Cards according to doc/RuleBasedPlayerDecision
    """
    if rnd.nr_tricks == 0:
        #it's the first round -> calculate score for each color based on trump
        score.calculate_score(rnd)

    #Actualize variables in score
    score.calculate_highest_card_per_color(rnd)
    score.calculate_lowest_card_per_color(rnd)
    score.calculate_next_best_card(rnd)

    card_to_play = None

    if check_more_than_one_valid_card(rnd):
        if check_is_first_player(rnd):
            if check_has_perfect_card(rnd):
                card_to_play = play_perfect_win(rnd)
            else:
                card_to_play = play_lowest_card_with_highest_score(rnd)
        else:
            if check_has_teammember_played(rnd):
                if check_perfect_card_from_teammember(rnd):
                    card_to_play = play_schmere_or_lowest_card()
                else:
                    if check_has_perfect_card(rnd):
                        card_to_play = play_perfect_win(rnd)
                    else:
                        card_to_play = play_lowest_card_of_weakest_color(rnd)
            else:
                if check_has_perfect_card(rnd):
                    card_to_play = play_perfect_win(rnd)
                else:
                    card_to_play = play_lowest_card_of_weakest_color(rnd)
    else:
        card_to_play = play_last_valid_card(rnd)

    if(card_to_play == None
        or card_to_play < 0
        or card_to_play > 35):

        ValueError("card_to_play not set properly! Value should be within 0 and 35")

    return card_to_play

def check_more_than_one_valid_card(rnd: PlayerRound) -> bool:
    return rnd.get_valid_cards().sum() > 1

def check_is_first_player(rnd: PlayerRound) -> bool:
    return rnd.current_trick.sum() == -4 #nobody played so far

def check_has_perfect_card(rnd: PlayerRound) -> bool:
    for color in range(0, 4):
        if(score.HIGHEST_CARD_PER_COLOR[color] == -1 or
            score.NEXT_BEST_CARD_PER_COLOR[color] == -1):
            continue

        if(score.HIGHEST_CARD_PER_COLOR[color]
            == score.NEXT_BEST_CARD_PER_COLOR[color]):

            #TODO is it a perfect card when there is still a trump?

            return True

    return False

def check_has_teammember_played(rnd: PlayerRound) -> bool:
    return (np.count_nonzero(rnd.current_trick == -1) > 2)

def check_perfect_card_from_teammember(rnd: PlayerRound) -> bool:
    #TODO implement check_perfect_card_from_teammember
    return False

def play_perfect_win(rnd: PlayerRound) -> int:
    for color in range(0, 4):
        if(score.HIGHEST_CARD_PER_COLOR[color] == -1 or
            score.NEXT_BEST_CARD_PER_COLOR[color] == -1):
            continue

        if score.HIGHEST_CARD_PER_COLOR[color] == score.NEXT_BEST_CARD_PER_COLOR[color]:
            return score.HIGHEST_CARD_PER_COLOR[color]

    raise ValueError("Should never reach this line :/. Check for perfect win before calling!")
    return -1

def play_lowest_card_with_highest_score(rnd: PlayerRound) -> int:
    #TODO implement play_lowest_card_with_highest_score
    return score.LOWEST_CARD_PER_COLOR.min()

def play_schmere_or_lowest_card(rnd: PlayerRound) -> int:
    #TODO implement play_schmere_or_lowest_card
    return score.LOWEST_CARD_PER_COLOR.min()

def play_lowest_card_of_weakest_color(rnd: PlayerRound) -> int:
    #TODO implement play_lowest_card_of_weakest_color
    return score.LOWEST_CARD_PER_COLOR.min()

def play_last_valid_card(rnd: PlayerRound) -> int:
    return np.random.choice(np.flatnonzero(rnd.get_valid_cards()))
