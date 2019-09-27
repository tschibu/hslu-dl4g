import numpy as np

from jass.base.player_round import PlayerRound

#------------------D--H--S--C--Obe--Unde
SCORE_PER_TRUMP = [0, 0, 0, 0, 0, 0]

def play_card(rnd: PlayerRound) -> int:
    """
    Play Cards according to doc/RuleBasedPlayerDecision
    """
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
    return False

def check_has_perfect_card(rnd: PlayerRound) -> bool:
    return False

def check_has_teammember_played(rnd: PlayerRound) -> bool:
    return False

def check_perfect_card_from_teammember(rnd: PlayerRound) -> bool:
    return False

def play_perfect_win(rnd: PlayerRound) -> int:
    return 0

def play_lowest_card_with_highest_score(rnd: PlayerRound) -> int:
    return 0

def play_schmere_or_lowest_card(rnd: PlayerRound) -> int:
    return 0

def play_lowest_card_of_weakest_color(rnd: PlayerRound) -> int:
    return 0

def play_last_valid_card(rnd: PlayerRound) -> int:
    return np.random.choice(np.flatnonzero(rnd.get_valid_cards()))