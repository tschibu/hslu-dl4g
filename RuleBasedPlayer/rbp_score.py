import numpy as np

from jass.base.const import color_masks, card_values, PUSH, trump_strings_german_long
from jass.base.player_round import PlayerRound
from jass.player.player import Player

# Trump Index and Corrections
# ------------------------------A--K--Q--J-10--9--8--7--6
# ------------------------------0--1--2--3--4--5--6--7--8
BEST_TRUMP_INDEXES  = np.array([3, 5, 0, 1, 2, 4, 6, 7, 8]) #TODO: Hyperparameter
BEST_OBE_INDEXES    = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8]) #TODO: Hyperparameter
BEST_UNDE_INDEXES   = np.array([8, 7, 6, 5, 4, 3, 2, 1, 0]) #TODO: Hyperparameter

START_SCORE = 9 #TODO: Hyperparameter
SCORE_STEP = (START_SCORE / 9) * -1 #linear curve

#PERFECT_WINS_FACTOR = 9 #TODO: Hyperparameter


def calculate_score(rnd: PlayerRound, trumpToCheck=None) -> np.array:
    """trump can be given to check specific trump on a round otherwise the rnd trump is taken
        return an array with four elemnts which each containing the score of one color """
    trump = None
    if trumpToCheck is not None:
        trump = trumpToCheck
    else:
        trump = rnd.trump

    score_per_color = np.array([0, 0, 0, 0])

    if trump == 0:
        #it's a D: Schellen trump
        score_per_color[0] = get_score_per_color_and_trump(0, rnd.get_valid_cards(), trump, 0)
        score_per_color[1] = get_score_per_color_and_trump(1, rnd.get_valid_cards(), trump, 1)
        score_per_color[2] = get_score_per_color_and_trump(2, rnd.get_valid_cards(), trump, 1)
        score_per_color[3] = get_score_per_color_and_trump(3, rnd.get_valid_cards(), trump, 1)

    elif trump == 1:
        #it's a H: Rosen trump
        score_per_color[0] = get_score_per_color_and_trump(0, rnd.get_valid_cards(), trump, 1)
        score_per_color[1] = get_score_per_color_and_trump(1, rnd.get_valid_cards(), trump, 0)
        score_per_color[2] = get_score_per_color_and_trump(2, rnd.get_valid_cards(), trump, 1)
        score_per_color[3] = get_score_per_color_and_trump(3, rnd.get_valid_cards(), trump, 1)

    elif trump == 2:
        #it's a S: Schilten trump
        score_per_color[0] = get_score_per_color_and_trump(0, rnd.get_valid_cards(), trump, 1)
        score_per_color[1] = get_score_per_color_and_trump(1, rnd.get_valid_cards(), trump, 1)
        score_per_color[2] = get_score_per_color_and_trump(2, rnd.get_valid_cards(), trump, 0)
        score_per_color[3] = get_score_per_color_and_trump(3, rnd.get_valid_cards(), trump, 1)

    elif trump == 3:
        #it's a C: Eichel trump
        score_per_color[0] = get_score_per_color_and_trump(0, rnd.get_valid_cards(), trump, 1)
        score_per_color[1] = get_score_per_color_and_trump(1, rnd.get_valid_cards(), trump, 1)
        score_per_color[2] = get_score_per_color_and_trump(2, rnd.get_valid_cards(), trump, 1)
        score_per_color[3] = get_score_per_color_and_trump(3, rnd.get_valid_cards(), trump, 0)

    elif trump == 4:
        #it's O: Obe
        #score_per_color[0] = get_score_per_color_and_trump(0, rnd.get_valid_cards(), trump, 1)
        #score_per_color[1] = get_score_per_color_and_trump(1, rnd.get_valid_cards(), trump, 1)
        #score_per_color[2] = get_score_per_color_and_trump(2, rnd.get_valid_cards(), trump, 1)
        #score_per_color[3] = get_score_per_color_and_trump(3, rnd.get_valid_cards(), trump, 1)
        pass

    elif trump == 5:
        #it's U: Une-Ufe
        #score_per_color[0] = get_score_per_color_and_trump(0, rnd.get_valid_cards(), trump, 2)
        #score_per_color[1] = get_score_per_color_and_trump(1, rnd.get_valid_cards(), trump, 2)
        #score_per_color[2] = get_score_per_color_and_trump(2, rnd.get_valid_cards(), trump, 2)
        #score_per_color[3] = get_score_per_color_and_trump(3, rnd.get_valid_cards(), trump, 2)
        pass

    else:
        raise ValueError("Wrong trump number! only works for 0 to 5 (D, H, S, C, Obe, Unde)")

    print("Calculate Score - Trump: {}, ScorePerColor: {}".format(trump_strings_german_long[trump], score_per_color))
    return score_per_color

def calculate_score_of_card(current_score: int, score_to_add: int, count_perfect_wins: bool, trump_card=False) -> int:
    if trump_card:
        current_score = current_score + score_to_add

    if count_perfect_wins:
        current_score = (current_score - score_to_add) + START_SCORE

    return current_score


#Trump Selection
def get_score_per_color_and_trump(color: int, hand: np.array, trump: int, trumpToCheck: int) -> int:
    """
    hand: one-dimensional array with 36 entries
    color: color index (0-3)
    trumpType: trump = 0, obe = 1, unde = 2
    """
    cards_of_color = hand[color*9:(color*9)+9]

    score = 0
    score_to_add = START_SCORE

    count_perfect_wins = True

    if trumpToCheck == 0:
        #check trump
        for i in range(0, BEST_TRUMP_INDEXES.size):
            if cards_of_color[BEST_TRUMP_INDEXES[i]] == 1:
                score = calculate_score_of_card(score, score_to_add, count_perfect_wins, trump<4)
            else:
                count_perfect_wins = False

            score_to_add = score_to_add + SCORE_STEP

        return score

    elif trumpToCheck == 1:
        #check obe
        for i in range(0, BEST_OBE_INDEXES.size):
            if cards_of_color[BEST_OBE_INDEXES[i]] == 1:
                score = calculate_score_of_card(score, score_to_add, count_perfect_wins, trump==5)
            else:
                count_perfect_wins = False

            score_to_add = score_to_add + SCORE_STEP

        return score

    elif trumpToCheck == 2:
        #check onde
        for i in range(0, BEST_UNDE_INDEXES.size):
            if cards_of_color[BEST_UNDE_INDEXES[i]] == 1:
                score = calculate_score_of_card(score, score_to_add, count_perfect_wins, trump==6)
            else:
                count_perfect_wins = False

            score_to_add = score_to_add + SCORE_STEP

        return score

    raise ValueError("Invalid trumpType: {}".format(trumpToCheck))

#Card calculations
def calculate_highest_card_per_color(rnd: PlayerRound) -> np.array:
    highest_card_per_color = np.array([-1, -1, -1, -1])

    for c in range(0, 4):
        cards = rnd.get_valid_cards()[c*9:(c*9)+9]

        if c == rnd.trump:
            #check highest trump
            highest_card_per_color[c] = get_highest_trump(c, cards)
        elif rnd.trump == 5:
            #check highest unde
            highest_card_per_color[c] = get_highest_unde(c, cards)
        else:
            #check highest obe
            highest_card_per_color[c] = get_highest_obe(c, cards)

    return highest_card_per_color

def calculate_lowest_card_per_color(rnd: PlayerRound) -> np.array:
    lowest_card_per_color = np.array([-1, -1, -1, -1])

    for c in range(0, 4):
        cards = rnd.get_valid_cards()[c*9:(c*9)+9]

        if c == rnd.trump:
            #check lowest trump
            lowest_card_per_color[c] = get_lowest_trump(c, cards)
        elif rnd.trump == 5:
            #check lowest unde
            lowest_card_per_color[c] = get_lowest_unde(c, cards)
        else:
            #check lowest obe
            lowest_card_per_color[c] = get_lowest_obe(c, cards)

    return lowest_card_per_color

def get_highest_trump(color_index: int, cards_of_color: np.array) -> int:
    return __get_card_index_by_color(color_index, cards_of_color, BEST_TRUMP_INDEXES)

def get_lowest_trump(color_index: int, cards_of_color: np.array) -> int:
    return __get_card_index_by_color(color_index, cards_of_color, BEST_TRUMP_INDEXES[::1])

def get_highest_obe(color_index: int, cards_of_color: np.array) -> int:
    return __get_card_index_by_color(color_index, cards_of_color, BEST_OBE_INDEXES)

def get_lowest_obe(color_index: int, cards_of_color: np.array) -> int:
    return __get_card_index_by_color(color_index, cards_of_color, BEST_OBE_INDEXES[::1])

def get_highest_unde(color_index: int, cards_of_color: np.array) -> int:
    return get_lowest_obe(color_index, cards_of_color)

def get_lowest_unde(color_index: int, cards_of_color: np.array) -> int:
    return get_highest_obe(color_index, cards_of_color)

def __get_card_index_by_color(color_index: int, cards_of_color: np.array, index_order: np.array) -> int:
    """
    gets the index of a color by its index order (to find best or worst color)
    """
    if color_index < 0 or color_index > 3:
        ValueError("color_index has to be within 0 and 3")

    for index in index_order:
        if cards_of_color[index] == 1:
            return index + (color_index * 9)

    return -1 #no cards of this color anymore

#Next best card
def calculate_next_best_card(rnd: PlayerRound) -> np.array:
    cards_missing = get_missing_cards(rnd.tricks)
    print("Missing Cards: {}".format(cards_missing))

    next_best_card_per_color = np.array([-1, -1, -1, -1])

    for c in range(0, 4):
        cards = cards_missing[c*9:(c*9)+9]
        if c == rnd.trump:
            #check highest trump
            next_best_card_per_color[c] = get_highest_trump(c, cards)
        elif rnd.trump == 5:
            #check highest unde
            next_best_card_per_color[c] = get_highest_unde(c, cards)
        else:
            #check highest obe
            next_best_card_per_color[c] = get_highest_obe(c, cards)

    return next_best_card_per_color

def get_missing_cards(tricks: np.array):
    missing_cards = np.array([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])

    for trick in tricks:
        for card in trick:
            if card != -1:
                missing_cards[card] = 0

    return missing_cards
