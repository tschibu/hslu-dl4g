import numpy as np

from jass.base.const import color_masks, card_values, PUSH, trump_strings_german_long
from jass.base.player_round import PlayerRound
from jass.player.player import Player

# Trump Index and Corrections
# ------------------------------A--K--Q--J-10--9--8--7--6
# ------------------------------0--1--2--3--4--5--6--7--8
BEST_TRUMP_INDEXES  = np.array([3, 5, 0, 1, 2, 4, 6, 7, 8])
BEST_OBE_INDEXES    = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])

START_SCORE = 9
SCORE_STEP = -1

# Variables used during playing
#-------------------------------------D--H--S--C
SCORE_PER_COLOR           = np.array([0, 0, 0, 0])
LOWEST_CARD_PER_COLOR     = np.array([0, 0, 0, 0])
HIGHEST_CARD_PER_COLOR    = np.array([0, 0, 0, 0])
NEXT_BEST_CARD_PER_COLOR  = np.array([0, 0, 0, 0])

CARDS_PLAYED = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
CARDS_MISSING = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

PERFECT_WINS_FACTOR = 30

#Trump Selection
def get_best_trump_and_score(hand: np.array) -> (int, int):
    best_trump = 0
    max_score_trump = -10000

    #check all different trumps (slice into array)
    for i in range(0, 4):
        score = get_score_trump_single_color(hand[i*9:(i*9)+9])
        score = score + get_score_obe(np.delete(hand, hand[i*9:(i*9)+9]))

        if score > max_score_trump:
            max_score_trump = score
            best_trump = i

    return best_trump, max_score_trump

def get_score_trump_single_color(hand: np.array) -> int:
    if hand.size != 9:
        ValueError("get_score_trump works only with one color: size = 9")

    score = 0
    perfect_wins = 0
    count_perfect_wins = True

    score_value = START_SCORE
    for i in range(0, BEST_TRUMP_INDEXES.size):
        if hand[BEST_TRUMP_INDEXES[i]] == 1:
            score = score + score_value

            if count_perfect_wins:
                perfect_wins = perfect_wins + 1
        else:
            count_perfect_wins = False #stop counting perfect wins
            score = score - score_value

        score_value = score_value + SCORE_STEP

    score = score + (perfect_wins * PERFECT_WINS_FACTOR)

    return score

def get_score_obe(hand: np.array) -> int:
    score = 0
    perfect_wins = 0
    count_perfect_wins = True

    number_of_colors = int(hand.size / 9)
    for i in range(0, number_of_colors):
        score_value = START_SCORE

        cards_of_color = hand[i*9:(i*9)+9]
        for v in cards_of_color:
            if v == 1:
                score = score + score_value

                if count_perfect_wins:
                    perfect_wins = perfect_wins + 1
            else:
                count_perfect_wins = False #stop counting perfect wins
                score = score - score_value

            score_value = score_value + SCORE_STEP

    score = score + (perfect_wins * PERFECT_WINS_FACTOR)

    return score

def get_score_onde(hand: np.array) -> int:
    hand_reversed = np.flip(hand)
    return get_score_obe(hand_reversed)

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
                score = score - score_value

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
                score = score - score_value

            score_value = score_value + SCORE_STEP

        return (score + (perfect_wins * PERFECT_WINS_FACTOR))

    elif trumpType == 2:
        #check onde
        perfect_wins = 0
        count_perfect_wins = True

        for v in np.flip(cards_of_color):
            if v == 1:
                score = score + score_value

                if count_perfect_wins:
                    perfect_wins = perfect_wins + 1
            else:
                count_perfect_wins = False
                score = score - score_value

            score_value = score_value + SCORE_STEP

        return (score + (perfect_wins * PERFECT_WINS_FACTOR))

#Card calculations
def calculate_highest_card_per_color(rnd: PlayerRound) -> np.array:
    for c in range(0, 4):
        cards = rnd.hand[c*9:(c*9)+9]
        if c == rnd.trump:
            #check highest trump
            HIGHEST_CARD_PER_COLOR[c] = (c*9) + get_highest_trump(cards)
        elif rnd.trump == 5:
            #check highest unde
            HIGHEST_CARD_PER_COLOR[c] = (c*9) + get_highest_unde(cards)
        else:
            #check highest obe
            HIGHEST_CARD_PER_COLOR[c] = (c*9) + get_highest_obe(cards)

    return HIGHEST_CARD_PER_COLOR

def calculate_lowest_card_per_color(rnd: PlayerRound) -> np.array:
    for c in range(0, 4):
        cards = rnd.hand[c*9:(c*9)+9]
        if c == rnd.trump:
            #check lowest trump
            LOWEST_CARD_PER_COLOR[c] = (c*9) + get_lowest_trump(cards)
        elif rnd.trump == 5:
            #check lowest unde
            LOWEST_CARD_PER_COLOR[c] = (c*9) + get_lowest_unde(cards)
        else:
            #check lowest obe
            LOWEST_CARD_PER_COLOR[c] = (c*9) + get_lowest_obe(cards)

    return LOWEST_CARD_PER_COLOR

def get_highest_trump(cards_of_color: np.array) -> int:
    return __get_card_index_by_color(cards_of_color, BEST_TRUMP_INDEXES)

def get_lowest_trump(cards_of_color: np.array) -> int:
    return __get_card_index_by_color(cards_of_color, np.flip(BEST_TRUMP_INDEXES))

def get_highest_obe(cards_of_color: np.array) -> int:
    return __get_card_index_by_color(cards_of_color, BEST_OBE_INDEXES)

def get_lowest_obe(cards_of_color: np.array) -> int:
    return __get_card_index_by_color(cards_of_color, np.flip(BEST_OBE_INDEXES))

def get_highest_unde(cards_of_color: np.array) -> int:
    return get_lowest_obe(cards_of_color)

def get_lowest_unde(cards_of_color: np.array) -> int:
    return get_highest_obe(cards_of_color)

def __get_card_index_by_color(cards_of_color: np.array, index_order: np.array) -> int:
    """
    gets the index of a color by its index order (to find best or worst color)
    """
    for index in index_order:
        if cards_of_color[index] == 1:
            return index

    return -1 #no cards of this color anymore

#Score per card
def calculate_score(rnd: PlayerRound) -> int:
    if rnd.trump == 0:
        #it's a D trump
        SCORE_PER_COLOR[0] = get_score_per_color_and_trump(rnd.hand, 0, 0)
        SCORE_PER_COLOR[1] = get_score_per_color_and_trump(rnd.hand, 1, 1)
        SCORE_PER_COLOR[2] = get_score_per_color_and_trump(rnd.hand, 2, 1)
        SCORE_PER_COLOR[3] = get_score_per_color_and_trump(rnd.hand, 3, 1)
    elif rnd.trump == 1:
        #it's a H trump
        SCORE_PER_COLOR[0] = get_score_per_color_and_trump(rnd.hand, 0, 1)
        SCORE_PER_COLOR[1] = get_score_per_color_and_trump(rnd.hand, 1, 0)
        SCORE_PER_COLOR[2] = get_score_per_color_and_trump(rnd.hand, 2, 1)
        SCORE_PER_COLOR[3] = get_score_per_color_and_trump(rnd.hand, 3, 1)
    elif rnd.trump == 2:
        #it's a S trump
        SCORE_PER_COLOR[0] = get_score_per_color_and_trump(rnd.hand, 0, 1)
        SCORE_PER_COLOR[1] = get_score_per_color_and_trump(rnd.hand, 1, 1)
        SCORE_PER_COLOR[2] = get_score_per_color_and_trump(rnd.hand, 2, 0)
        SCORE_PER_COLOR[3] = get_score_per_color_and_trump(rnd.hand, 3, 1)
    elif rnd.trump == 3:
        #it's a C trump
        SCORE_PER_COLOR[0] = get_score_per_color_and_trump(rnd.hand, 0, 1)
        SCORE_PER_COLOR[1] = get_score_per_color_and_trump(rnd.hand, 1, 1)
        SCORE_PER_COLOR[2] = get_score_per_color_and_trump(rnd.hand, 2, 1)
        SCORE_PER_COLOR[3] = get_score_per_color_and_trump(rnd.hand, 3, 0)
    elif rnd.trump == 4:
        #it's obe
        SCORE_PER_COLOR[0] = get_score_per_color_and_trump(rnd.hand, 0, 1)
        SCORE_PER_COLOR[1] = get_score_per_color_and_trump(rnd.hand, 1, 1)
        SCORE_PER_COLOR[2] = get_score_per_color_and_trump(rnd.hand, 2, 1)
        SCORE_PER_COLOR[3] = get_score_per_color_and_trump(rnd.hand, 3, 1)
    elif rnd.trump == 5:
        #it's unde
        SCORE_PER_COLOR[0] = get_score_per_color_and_trump(rnd.hand, 0, 2)
        SCORE_PER_COLOR[1] = get_score_per_color_and_trump(rnd.hand, 1, 2)
        SCORE_PER_COLOR[2] = get_score_per_color_and_trump(rnd.hand, 2, 2)
        SCORE_PER_COLOR[3] = get_score_per_color_and_trump(rnd.hand, 3, 2)

#Next best card
def calculate_next_best_card(rnd: PlayerRound) -> np.array:
    __set_played_and_missing_cards(rnd.tricks)
    for c in range(0, 4):
        cards = CARDS_MISSING[c*9:(c*9)+9]
        if c == rnd.trump:
            #check highest trump
            NEXT_BEST_CARD_PER_COLOR[c] = (c*9) + get_highest_trump(cards)
        elif rnd.trump == 5:
            #check highest unde
            NEXT_BEST_CARD_PER_COLOR[c] = (c*9) + get_highest_unde(cards)
        else:
            #check highest obe
            NEXT_BEST_CARD_PER_COLOR[c] = (c*9) + get_highest_obe(cards)

    return NEXT_BEST_CARD_PER_COLOR

def __set_played_and_missing_cards(tricks: np.array):
    for trick in tricks:
        for card in trick:
            if card != -1:
                CARDS_PLAYED[card] = 1
                CARDS_MISSING[card] = 0
            else:
                CARDS_PLAYED[card] = 0
                CARDS_MISSING[card] = 1
