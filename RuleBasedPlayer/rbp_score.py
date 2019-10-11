import numpy as np

from jass.base.const import color_masks, card_values, PUSH, trump_strings_german_long
from jass.base.player_round import PlayerRound
from jass.player.player import Player

# Trump Index and Corrections
# ------------------------------A--K--Q--J-10--9--8--7--6
# ------------------------------0--1--2--3--4--5--6--7--8
BEST_TRUMP_INDEXES  = np.array([3, 5, 0, 1, 2, 4, 6, 7, 8])
BEST_OBE_INDEXES    = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])

START_SCORE = 1
SCORE_STEP = 0

# Variables used during playing
#-------------------------------------D--H--S--C
SCORE_PER_COLOR           = np.array([0, 0, 0, 0])
LOWEST_CARD_PER_COLOR     = np.array([0, 0, 0, 0])
HIGHEST_CARD_PER_COLOR    = np.array([0, 0, 0, 0])
NEXT_BEST_CARD_PER_COLOR  = np.array([0, 0, 0, 0])

CARDS_PLAYED    = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
CARDS_MISSING   = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

PERFECT_WINS_FACTOR = 1

#Score per card
def calculate_score(rnd: PlayerRound, trumpToCheck=None) -> int:
    """trump can be given to check specific trump on a round otherwise the rnd trump is taken"""
    trump = None
    if trumpToCheck is not None:
        trump = trumpToCheck
    else:
        trump = rnd.trump

    if trump == 0:
        #it's a D trump
        SCORE_PER_COLOR[0] = get_score_per_color_and_trump(rnd.get_valid_cards(), 0, 0)
        SCORE_PER_COLOR[1] = get_score_per_color_and_trump(rnd.get_valid_cards(), 1, 1)
        SCORE_PER_COLOR[2] = get_score_per_color_and_trump(rnd.get_valid_cards(), 2, 1)
        SCORE_PER_COLOR[3] = get_score_per_color_and_trump(rnd.get_valid_cards(), 3, 1)

    elif trump == 1:
        #it's a H trump
        SCORE_PER_COLOR[0] = get_score_per_color_and_trump(rnd.get_valid_cards(), 0, 1)
        SCORE_PER_COLOR[1] = get_score_per_color_and_trump(rnd.get_valid_cards(), 1, 0)
        SCORE_PER_COLOR[2] = get_score_per_color_and_trump(rnd.get_valid_cards(), 2, 1)
        SCORE_PER_COLOR[3] = get_score_per_color_and_trump(rnd.get_valid_cards(), 3, 1)

    elif trump == 2:
        #it's a S trump
        SCORE_PER_COLOR[0] = get_score_per_color_and_trump(rnd.get_valid_cards(), 0, 1)
        SCORE_PER_COLOR[1] = get_score_per_color_and_trump(rnd.get_valid_cards(), 1, 1)
        SCORE_PER_COLOR[2] = get_score_per_color_and_trump(rnd.get_valid_cards(), 2, 0)
        SCORE_PER_COLOR[3] = get_score_per_color_and_trump(rnd.get_valid_cards(), 3, 1)

    elif trump == 3:
        #it's a C trump
        SCORE_PER_COLOR[0] = get_score_per_color_and_trump(rnd.get_valid_cards(), 0, 1)
        SCORE_PER_COLOR[1] = get_score_per_color_and_trump(rnd.get_valid_cards(), 1, 1)
        SCORE_PER_COLOR[2] = get_score_per_color_and_trump(rnd.get_valid_cards(), 2, 1)
        SCORE_PER_COLOR[3] = get_score_per_color_and_trump(rnd.get_valid_cards(), 3, 0)

    elif trump == 4:
        #it's obe
        SCORE_PER_COLOR[0] = get_score_per_color_and_trump(rnd.get_valid_cards(), 0, 1)
        SCORE_PER_COLOR[1] = get_score_per_color_and_trump(rnd.get_valid_cards(), 1, 1)
        SCORE_PER_COLOR[2] = get_score_per_color_and_trump(rnd.get_valid_cards(), 2, 1)
        SCORE_PER_COLOR[3] = get_score_per_color_and_trump(rnd.get_valid_cards(), 3, 1)

    elif trump == 5:
        #it's unde
        SCORE_PER_COLOR[0] = get_score_per_color_and_trump(rnd.get_valid_cards(), 0, 2)
        SCORE_PER_COLOR[1] = get_score_per_color_and_trump(rnd.get_valid_cards(), 1, 2)
        SCORE_PER_COLOR[2] = get_score_per_color_and_trump(rnd.get_valid_cards(), 2, 2)
        SCORE_PER_COLOR[3] = get_score_per_color_and_trump(rnd.get_valid_cards(), 3, 2)

    else:
        raise ValueError("Wrong trump number! only works for 0 to 5 (D, H, S, C, Obe, Unde)")

    print("Calculate Score - Trump: {}, ScorePerColor: {}".format(trump_strings_german_long[trump], SCORE_PER_COLOR))
    return SCORE_PER_COLOR.sum()

#Trump Selection
def get_score_per_color_and_trump(hand: np.array, color: int, trumpType: int) -> int:
    """
    hand: one-dimensional array with 36 entries
    color: color index (0-3)
    trumpType: trump = 0, obe = 1, unde = 2
    """
    cards_of_color = hand[color*9:(color*9)+9]
    score = 0
    score_value = START_SCORE

    perfect_wins = 0
    count_perfect_wins = True

    if trumpType == 0:
        #check trump
        for i in range(0, BEST_TRUMP_INDEXES.size):
            if cards_of_color[BEST_TRUMP_INDEXES[i]] == 1:
                score = score + score_value

                if count_perfect_wins:
                    perfect_wins = perfect_wins + 1

            else:
                count_perfect_wins = False

            score_value = score_value + SCORE_STEP

        return (score + (perfect_wins * PERFECT_WINS_FACTOR))

    elif trumpType == 1:
        #check obe
        perfect_wins = 0
        count_perfect_wins = True

        for v in cards_of_color:
            if v == 1:
                score = score + score_value

                if count_perfect_wins:
                    perfect_wins = perfect_wins + 1

            else:
                count_perfect_wins = False

            score_value = score_value + SCORE_STEP

        return (score + (perfect_wins * PERFECT_WINS_FACTOR))

    elif trumpType == 2:
        #check onde
        perfect_wins = 0
        count_perfect_wins = True

        for v in cards_of_color[::-1]:
            if v == 1:
                score = score + score_value

                if count_perfect_wins:
                    perfect_wins = perfect_wins + 1

            else:
                count_perfect_wins = False

            score_value = score_value + SCORE_STEP

        return (score + (perfect_wins * PERFECT_WINS_FACTOR))

#Card calculations
def calculate_highest_card_per_color(rnd: PlayerRound) -> np.array:
    for c in range(0, 4):
        cards = rnd.get_valid_cards()[c*9:(c*9)+9]
        if c == rnd.trump:
            #check highest trump
            HIGHEST_CARD_PER_COLOR[c] = get_highest_trump(c, cards)
        elif rnd.trump == 5:
            #check highest unde
            HIGHEST_CARD_PER_COLOR[c] = get_highest_unde(c, cards)
        else:
            #check highest obe
            HIGHEST_CARD_PER_COLOR[c] = get_highest_obe(c, cards)

    return HIGHEST_CARD_PER_COLOR

def calculate_lowest_card_per_color(rnd: PlayerRound) -> np.array:
    for c in range(0, 4):
        cards = rnd.get_valid_cards()[c*9:(c*9)+9]
        if c == rnd.trump:
            #check lowest trump
            LOWEST_CARD_PER_COLOR[c] = get_lowest_trump(c, cards)
        elif rnd.trump == 5:
            #check lowest unde
            LOWEST_CARD_PER_COLOR[c] = get_lowest_unde(c, cards)
        else:
            #check lowest obe
            LOWEST_CARD_PER_COLOR[c] = get_lowest_obe(c, cards)

    return LOWEST_CARD_PER_COLOR

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
    for c in range(0, 4):
        cards = cards_missing[c*9:(c*9)+9]
        if c == rnd.trump:
            #check highest trump
            NEXT_BEST_CARD_PER_COLOR[c] = get_highest_trump(c, cards)
        elif rnd.trump == 5:
            #check highest unde
            NEXT_BEST_CARD_PER_COLOR[c] = get_highest_unde(c, cards)
        else:
            #check highest obe
            NEXT_BEST_CARD_PER_COLOR[c] = get_highest_obe(c, cards)

    return NEXT_BEST_CARD_PER_COLOR

def get_missing_cards(tricks: np.array):
    missing_cards = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    for trick in tricks:
        for card in trick:
            if card != -1:
                missing_cards[card] = 1

    # as we calculated first the played cards we switch 0 and 1
    missing_cards[missing_cards == 1] = -1
    missing_cards[missing_cards == 0] = 1
    missing_cards[missing_cards == -1] = 0

    return missing_cards
