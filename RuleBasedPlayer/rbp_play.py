import numpy as np

from jass.base.const import card_values
from jass.base.player_round import PlayerRound
import RuleBasedPlayer.rbp_score as score

MINIMUM_POINTS_FOR_TRUMP = 5

def play_card(rnd: PlayerRound) -> int:
    """
    Play Cards according to doc/RuleBasedPlayerDecision
    """
    if rnd.nr_tricks == 0:
        #it's the first round -> calculate score for each color based on trump
        score.calculate_score(rnd)

    #Actualize variables in score
    print("Player: {}, Tricks: {}, CurrentTrick: {}".format(rnd.player, rnd.nr_tricks+1, rnd.current_trick))
    print(score.calculate_highest_card_per_color(rnd))
    print(score.calculate_lowest_card_per_color(rnd))
    print(score.calculate_next_best_card(rnd))

    card_to_play = None

    if check_more_than_one_valid_card(rnd):
        if check_is_first_player(rnd):
            if check_has_perfect_card(rnd):
                card_to_play = play_perfect_win(rnd)
            else:
                if check_has_trump(rnd):
                    card_to_play = play_trump(rnd)
                else:
                    card_to_play = play_lowest_card_with_highest_score(rnd)
        else:
            if check_has_teammember_played(rnd):
                if check_perfect_card_from_teammember(rnd):
                    card_to_play = play_schmere_or_lowest_card(rnd)
                else:
                    if check_has_perfect_card(rnd):
                        card_to_play = play_perfect_win(rnd)
                    else:
                        if check_has_trump(rnd):
                            if check_enough_points(rnd):
                                card_to_play = play_trump(rnd)
                            else:
                                card_to_play = play_lowest_card_of_weakest_color(rnd)
                        else:
                            card_to_play = play_lowest_card_of_weakest_color(rnd)
            else:
                if check_has_perfect_card(rnd):
                    card_to_play = play_perfect_win(rnd)
                else:
                    if check_has_trump(rnd):
                        if check_enough_points(rnd):
                            card_to_play = play_trump(rnd)
                        else:
                            card_to_play = play_lowest_card_of_weakest_color(rnd)
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

            if color != rnd.trump and check_round_has_still_trumps(rnd):
                continue #not perfect card when still trumps...

            return True

    return False

def check_has_trump(rnd: PlayerRound) -> bool:
    if rnd.trump < 4:
        if score.LOWEST_CARD_PER_COLOR[rnd.trump] != -1:
            return True

    return False

def check_enough_points(rnd: PlayerRound) -> bool:
    points = 0
    for card_index in rnd.current_trick:
        if card_index != -1:
            points = points + card_values[rnd.trump][card_index]

    if points >= MINIMUM_POINTS_FOR_TRUMP:
        print("Enough points - play Trump! Points: {}".format(points))
        return True
    else:
        return False

def check_has_teammember_played(rnd: PlayerRound) -> bool:
    partner_card = rnd.current_trick[get_partner_index(rnd.player)]
    if partner_card == -1: #if card is -1 he has not played
        return False

    return True

def check_round_has_still_trumps(rnd: PlayerRound) -> bool:
    if score.CARDS_MISSING[(rnd.trump*9):(rnd.trump*9)+9].sum() != 9:
        return True
    return False

def check_perfect_card_from_teammember(rnd: PlayerRound) -> bool:
    partner_card = rnd.current_trick[get_partner_index(rnd.player)]
    color_of_card = int(partner_card / 9)
    card_index_partner = int(partner_card - (9 * color_of_card))

    if partner_card == -1:
        ValueError("Partner not played so far! Check if he played before!")
    if color_of_card < 0 or color_of_card > 3:
        ValueError("Partner has invalid Color!")
    if card_index_partner < 0 or card_index_partner > 8:
        ValueError("Partner has invalid Card!!")

    if rnd.trump < 4:
        #check if still trumps
        if check_round_has_still_trumps(rnd):
            #still trumps
            print("There are still trumps!")
            if color_of_card == rnd.trump:
                print("Partner played trump!")
                return check_perfect_card_trump(color_of_card, card_index_partner, rnd.current_trick)
            else:
                print("Partner not played trump, but there are still some...")
                return False #no perfect win when there are trumps
        else:
            return check_perfect_card_obe(color_of_card, card_index_partner, rnd.current_trick)

    if rnd.trump == 4:
        return check_perfect_card_obe(color_of_card, card_index_partner, rnd.current_trick)

    if rnd.trump == 5:
        return check_perfect_card_unde(color_of_card, card_index_partner, rnd.current_trick)

    raise ValueError("Perfect card check of Teammember failed!")

def check_perfect_card_trump(color: int, card_index: int, tick: np.array) -> bool:
    missing_cards = score.CARDS_MISSING[color*9:(color*9)+9]

    best_card = True

    for index in score.BEST_TRUMP_INDEXES:
        if missing_cards[index] == 1:
            #found first missing card
            if index == 3: #buur handling
                return False #no higher card than buur
            elif index == 5: #9 handling
                return (card_index == 3) #has to be buur to beat 9
            else:
                best_card = (card_index < index) #after buur and 9 lowest index wins (A to 6)

    if best_card:
        #check opponents
        for card_in_tick in tick:
            c = int(card_in_tick / 9)
            if c == color:
                #played same color
                opponent_card_index = card_in_tick - (9*c)
                best_card = (opponent_card_index > card_index)

    return best_card

def check_perfect_card_obe(color: int, card_index: int, tick: np.array) -> bool:
    missing_cards = score.CARDS_MISSING[color*9:(color*9)+9]

    best_card = True

    for index in score.BEST_OBE_INDEXES:
        if missing_cards[index] == 1:
            best_card = (card_index < index) #card has to have lower index

    if best_card:
        #check opponents
        for card_in_tick in tick:
            c = card_in_tick / 9
            if c == color:
                opponent_card_index = card_in_tick - (9*c)
                best_card = (opponent_card_index > card_index)

    return best_card

def check_perfect_card_unde(color: int, card_index: int, tick: np.array) -> bool:
    missing_cards = score.CARDS_MISSING[color*9:(color*9)+9]

    best_card = True

    for index in score.BEST_OBE_INDEXES[::1]:
        if missing_cards[index] == 1:
            best_card = (card_index > index) #card has to have higher index when unde

    if best_card:
        #check opponents
        for card_in_tick in tick:
            c = card_in_tick / 9
            if c == color:
                opponent_card_index = card_in_tick - (9*c)
                best_card = (opponent_card_index < card_index) #opponent needs lower index when unde

    return best_card

def play_perfect_win(rnd: PlayerRound) -> int:
    for color in range(0, 4):
        if(score.HIGHEST_CARD_PER_COLOR[color] == -1 or
            score.NEXT_BEST_CARD_PER_COLOR[color] == -1):
            continue

        if score.HIGHEST_CARD_PER_COLOR[color] == score.NEXT_BEST_CARD_PER_COLOR[color]:
            print("Playing perfect card: {}, playingTrump: {}, stillTrumps: {}".format(score.HIGHEST_CARD_PER_COLOR[color], (color == rnd.trump), check_round_has_still_trumps(rnd)))
            return score.HIGHEST_CARD_PER_COLOR[color]

    raise ValueError("Should never reach this line :/. Check for perfect win before calling!")
    return -1

def play_lowest_card_with_highest_score(rnd: PlayerRound) -> int:
    max_score = -10000 #start with high score
    color_to_play = -1
    color_index = 0

    for s in score.SCORE_PER_COLOR:
        if score.LOWEST_CARD_PER_COLOR[color_index] == -1:
            color_index = color_index + 1
            continue #no card in this color...continue...

        #check the score and set color to play
        if max_score < s:
            max_score = s
            color_to_play = color_index

        color_index = color_index + 1

    if(color_to_play < 0 or color_to_play > 3 or
        score.LOWEST_CARD_PER_COLOR[color_to_play] == -1):
        raise ValueError("Color to Play has to be within 0 and 3 and Card != -1!")

    print("Playing lowest card of Best Color! Color: {}, Card: {}, Scores: {}".format(color_to_play, score.LOWEST_CARD_PER_COLOR[color_to_play], score.SCORE_PER_COLOR))
    return score.LOWEST_CARD_PER_COLOR[color_to_play]

def play_schmere_or_lowest_card(rnd: PlayerRound) -> int:
    #TODO implement play_schmere_or_lowest_card
    return play_lowest_card_of_weakest_color(rnd)

def play_lowest_card_of_weakest_color(rnd: PlayerRound) -> int:
    min_score = 10000 #start with high score
    color_to_play = -1
    color_index = 0

    for s in score.SCORE_PER_COLOR:
        if score.LOWEST_CARD_PER_COLOR[color_index] == -1:
            color_index = color_index + 1
            print("No card of Color: {}".format(color_index))
            continue #no card in this color...continue...

        #check the score and set color to play
        if min_score > s:
            min_score = s
            color_to_play = color_index

        color_index = color_index + 1

    if(color_to_play < 0 or color_to_play > 3 or
        score.LOWEST_CARD_PER_COLOR[color_to_play] == -1):
        raise ValueError("Color to Play has to be within 0 and 3 and Card != -1!")

    print("Playing lowest card of Weakest Color! Color: {}, Card: {}, Scores: {}".format(color_to_play, score.LOWEST_CARD_PER_COLOR[color_to_play], score.SCORE_PER_COLOR))
    return score.LOWEST_CARD_PER_COLOR[color_to_play]

def play_last_valid_card(rnd: PlayerRound) -> int:
    for card in score.HIGHEST_CARD_PER_COLOR:
        if card != -1:
            return card

    raise ValueError("No valid card anymore!")
    return -1

def play_trump(rnd: PlayerRound) -> int:
    trump = score.HIGHEST_CARD_PER_COLOR[rnd.trump]
    if trump == -1:
        raise ValueError("Invalid Trump: Check first if trump is available!")

    print("Playing Trump! Trump: {}".format(trump))
    return trump

def get_partner_index(myindex: int) -> int:
    if myindex == 0:
        return 2
    if myindex == 1:
        return 3
    if myindex == 2:
        return 0
    if myindex == 3:
        return 1