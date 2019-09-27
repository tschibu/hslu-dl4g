import numpy as np

from jass.base.player_round import PlayerRound
import RuleBasedPlayer.rbp_score as score

#---------------------------D--H--S--C
SCORE_PER_COLOR = np.array([0, 0, 0, 0])

def play_card(rnd: PlayerRound) -> int:
    """
    Play Cards according to doc/RuleBasedPlayerDecision
    """
    if rnd.nr_tricks == 0:
        #it's the first round -> calculate score for each color based on trump
        calculate_score(rnd)

    if check_more_than_one_valid_card(rnd):
        if check_is_first_player(rnd):
            if check_has_perfect_card(rnd):
                play_perfect_win(rnd)
            else:
                play_lowest_card_with_highest_score(rnd)
        else:
            if check_has_teammember_played(rnd):
                if check_perfect_card_from_teammember():
                    play_schmere_or_lowest_card()
                else:
                    if check_has_perfect_card(rnd):
                        play_perfect_win(rnd)
                    else:
                        play_lowest_card_of_weakest_color(rnd)
            else:
                if check_has_perfect_card(rnd):
                    play_perfect_win(rnd)
                else:
                    play_lowest_card_of_weakest_color(rnd)
    else:
        return play_last_valid_card(rnd)

def check_more_than_one_valid_card(rnd: PlayerRound) -> bool:
    return rnd.get_valid_cards().sum() > 1

def check_is_first_player(rnd: PlayerRound) -> bool:
    return rnd.current_trick.sum() == -4 #nobody played so far

def check_has_perfect_card(rnd: PlayerRound) -> bool:
    #TODO implement check_has_perfect_card
    return False

def check_has_teammember_played(rnd: PlayerRound) -> bool:
    return (np.count_nonzero(rnd.current_trick == -1) > 2)

def check_perfect_card_from_teammember(rnd: PlayerRound) -> bool:
    #TODO implement check_perfect_card_from_teammember
    return False

def play_perfect_win(rnd: PlayerRound) -> int:
    #TODO implement play_perfect_win
    return 0

def play_lowest_card_with_highest_score(rnd: PlayerRound) -> int:
    #TODO implement play_lowest_card_with_highest_score
    return 0

def play_schmere_or_lowest_card(rnd: PlayerRound) -> int:
    #TODO implement play_schmere_or_lowest_card
    return 0

def play_lowest_card_of_weakest_color(rnd: PlayerRound) -> int:
    #TODO implement play_lowest_card_of_weakest_color
    return 0

def play_last_valid_card(rnd: PlayerRound) -> int:
    return np.random.choice(np.flatnonzero(rnd.get_valid_cards()))

def calculate_score(rnd: PlayerRound) -> int:
    if rnd.trump == 0:
        #it's a D trump
        SCORE_PER_COLOR[0] = score.get_score_per_color_and_trump(rnd.hand, 0, 0)
        SCORE_PER_COLOR[1] = score.get_score_per_color_and_trump(rnd.hand, 1, 1)
        SCORE_PER_COLOR[2] = score.get_score_per_color_and_trump(rnd.hand, 2, 1)
        SCORE_PER_COLOR[3] = score.get_score_per_color_and_trump(rnd.hand, 3, 1)
    elif rnd.trump == 0:
        #it's a H trump
        SCORE_PER_COLOR[0] = score.get_score_per_color_and_trump(rnd.hand, 0, 1)
        SCORE_PER_COLOR[1] = score.get_score_per_color_and_trump(rnd.hand, 1, 0)
        SCORE_PER_COLOR[2] = score.get_score_per_color_and_trump(rnd.hand, 2, 1)
        SCORE_PER_COLOR[3] = score.get_score_per_color_and_trump(rnd.hand, 3, 1)
    elif rnd.trump == 0:
        #it's a S trump
        SCORE_PER_COLOR[0] = score.get_score_per_color_and_trump(rnd.hand, 0, 1)
        SCORE_PER_COLOR[1] = score.get_score_per_color_and_trump(rnd.hand, 1, 1)
        SCORE_PER_COLOR[2] = score.get_score_per_color_and_trump(rnd.hand, 2, 0)
        SCORE_PER_COLOR[3] = score.get_score_per_color_and_trump(rnd.hand, 3, 1)
    elif rnd.trump == 0:
        #it's a C trump
        SCORE_PER_COLOR[0] = score.get_score_per_color_and_trump(rnd.hand, 0, 1)
        SCORE_PER_COLOR[1] = score.get_score_per_color_and_trump(rnd.hand, 1, 1)
        SCORE_PER_COLOR[2] = score.get_score_per_color_and_trump(rnd.hand, 2, 1)
        SCORE_PER_COLOR[3] = score.get_score_per_color_and_trump(rnd.hand, 3, 0)
    elif rnd.trump == 4:
        #it's obe
        SCORE_PER_COLOR[0] = score.get_score_per_color_and_trump(rnd.hand, 0, 1)
        SCORE_PER_COLOR[1] = score.get_score_per_color_and_trump(rnd.hand, 1, 1)
        SCORE_PER_COLOR[2] = score.get_score_per_color_and_trump(rnd.hand, 2, 1)
        SCORE_PER_COLOR[3] = score.get_score_per_color_and_trump(rnd.hand, 3, 1)
    elif rnd.trump == 5:
        #it's unde
        SCORE_PER_COLOR[0] = score.get_score_per_color_and_trump(rnd.hand, 0, 2)
        SCORE_PER_COLOR[1] = score.get_score_per_color_and_trump(rnd.hand, 1, 2)
        SCORE_PER_COLOR[2] = score.get_score_per_color_and_trump(rnd.hand, 2, 2)
        SCORE_PER_COLOR[3] = score.get_score_per_color_and_trump(rnd.hand, 3, 2)