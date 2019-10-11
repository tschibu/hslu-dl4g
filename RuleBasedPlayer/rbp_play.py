import numpy as np

from jass.base.const import card_values
from jass.base.player_round import PlayerRound
import RuleBasedPlayer.rbp_score as score

MINIMUM_POINTS_FOR_TRUMP = 7

class RbpPlay():
    def __init__(self):
        self.score_per_color = np.array([0, 0, 0, 0])
        self.lowest_card_per_color = np.array([-1, -1, -1, -1])
        self.highest_card_per_color = np.array([-1, -1, -1, -1])
        self.best_next_card_per_color = np.array([-1, -1, -1, -1])

    def play_card(self, rnd: PlayerRound) -> int:
        """
        Play Cards according to doc/RuleBasedPlayerDecision
        """
        #if rnd.nr_tricks == 0:
        #    #it's the first round -> calculate score for each color based on trump
        self.score_per_color = score.calculate_score(rnd)

        self.lowest_card_per_color = score.calculate_lowest_card_per_color(rnd)
        self.highest_card_per_color = score.calculate_highest_card_per_color(rnd)
        self.best_next_card_per_color = score.calculate_next_best_card(rnd)

        #Actualize variables in score
        print("Player: {}, Tricks: {}, CurrentTrick: {}, Trump: {}".format(rnd.player, rnd.nr_tricks+1, rnd.current_trick, rnd.trump))
        print("Highest   Cards: {}".format(self.highest_card_per_color))
        print("Lowest    Cards: {}".format(self.lowest_card_per_color))
        print("Next Best Cards: {}".format(self.best_next_card_per_color))

        card_to_play = None

        if self._check_more_than_one_valid_card(rnd):
            if self._check_is_first_player(rnd):
                if self._check_has_perfect_card(rnd):
                    card_to_play = self._play_perfect_win(rnd)
                else:
                    if self._check_has_trump(rnd):
                        card_to_play = self._play_trump(rnd)
                    else:
                        card_to_play = self._play_lowest_card_with_highest_score(rnd)
            else:
                if self._check_has_teammember_played(rnd):
                    if self._check_perfect_card_from_teammember(rnd):
                        card_to_play = self._play_schmere_or_lowest_card(rnd)
                    else:
                        if self._check_has_perfect_card(rnd):
                            card_to_play = self._play_perfect_win(rnd)
                        else:
                            if self._check_has_trump(rnd):
                                if self._check_enough_points(rnd):
                                    card_to_play = self._play_trump(rnd)
                                else:
                                    card_to_play = self._play_lowest_card_of_weakest_color(rnd)
                            else:
                                card_to_play = self._play_lowest_card_of_weakest_color(rnd)
                else:
                    if self._check_has_perfect_card(rnd):
                        card_to_play = self._play_perfect_win(rnd)
                    else:
                        if self._check_has_trump(rnd):
                            if self._check_enough_points(rnd):
                                card_to_play = self._play_trump(rnd)
                            else:
                                card_to_play = self._play_lowest_card_of_weakest_color(rnd)
                        else:
                            card_to_play = self._play_lowest_card_of_weakest_color(rnd)
        else:
            card_to_play = self._play_last_valid_card(rnd)

        if(card_to_play == None
            or card_to_play < 0
            or card_to_play > 35):

            raise ValueError("card_to_play not set properly! Value should be within 0 and 35")

        return card_to_play

    def _check_more_than_one_valid_card(self, rnd: PlayerRound) -> bool:
        return rnd.get_valid_cards().sum() > 1

    def _check_is_first_player(self, rnd: PlayerRound) -> bool:
        return rnd.current_trick.sum() == -4 #nobody played so far

    def _check_has_perfect_card(self, rnd: PlayerRound) -> bool:
        for color in range(0, 4):
            if(self.highest_card_per_color[color] == -1 or
                self.best_next_card_per_color[color] == -1):
                continue

            if(self.highest_card_per_color[color]
                == self.best_next_card_per_color[color]):

                if color != rnd.trump and self._check_round_has_still_trumps(rnd):
                    continue #not perfect card when still trumps...

                return True

        return False

    def _check_has_trump(self, rnd: PlayerRound) -> bool:
        """check if trump available and valid in current round"""
        if rnd.trump < 4:
            if self.lowest_card_per_color[rnd.trump] != -1:
                return True

        return False

    def _check_enough_points(self, rnd: PlayerRound) -> bool:
        points = 0
        for card_index in rnd.current_trick:
            if card_index != -1:
                points = points + card_values[rnd.trump][card_index]

        if points >= MINIMUM_POINTS_FOR_TRUMP:
            print("Enough points in trick. Points: {}".format(points))
            return True
        else:
            return False

    def _check_has_teammember_played(self, rnd: PlayerRound) -> bool:
        partner_card = rnd.current_trick[self._get_partner_index(rnd.player)]
        if partner_card == -1: #if card is -1 he has not played
            return False

        return True

    def _check_round_has_still_trumps(self, rnd: PlayerRound) -> bool:
        """check if missing card sum is 0 where the trump is"""
        if score.get_missing_cards()[(rnd.trump*9):(rnd.trump*9)+9].sum() != 0:
            return True
        return False

    def _check_perfect_card_from_teammember(self, rnd: PlayerRound) -> bool:
        partner_card = rnd.current_trick[self._get_partner_index(rnd.player)]
        color_of_card = int(partner_card / 9)
        card_index_partner = int(partner_card - (9 * color_of_card))

        if partner_card == -1:
            ValueError("Partner not played so far! Check if he played before!")
        if color_of_card < 0 or color_of_card > 3:
            ValueError("Partner has invalid Color!")
        if card_index_partner < 0 or card_index_partner > 8:
            ValueError("Partner has invalid Card!!")

        print("Current Trick Winner: {}".format(rnd.trick_winner))

        if rnd.trump < 4:
            #check if still trumps
            if self._check_round_has_still_trumps(rnd):
                #still trumps
                print("There are still trumps!")
                if color_of_card == rnd.trump:
                    print("Partner played trump!")
                    return self._check_perfect_card_trump(color_of_card, card_index_partner, rnd.current_trick)
                else:
                    print("Partner not played trump, but there are still some...")
                    return False #no perfect win when there are trumps
            else:
                return self._check_perfect_card_obe(color_of_card, card_index_partner, rnd.current_trick)

        if rnd.trump == 4:
            return self._check_perfect_card_obe(color_of_card, card_index_partner, rnd.current_trick)

        if rnd.trump == 5:
            return self._check_perfect_card_unde(color_of_card, card_index_partner, rnd.current_trick)

        raise ValueError("Perfect card check of Teammember failed!")

    def _check_perfect_card_trump(self, color: int, card_index: int, tick: np.array) -> bool:
        missing_cards = score.get_missing_cards[color*9:(color*9)+9]

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

    def _check_perfect_card_obe(self, color: int, card_index: int, tick: np.array) -> bool:
        missing_cards = score.get_missing_cards[color*9:(color*9)+9]

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

    def _check_perfect_card_unde(self, color: int, card_index: int, tick: np.array) -> bool:
        missing_cards = score.get_missing_cards[color*9:(color*9)+9]

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

    def _play_perfect_win(self, rnd: PlayerRound) -> int:
        for color in range(0, 4):
            if(self.highest_card_per_color[color] == -1 or
                self.best_next_card_per_color[color] == -1):
                continue

            if self.highest_card_per_color[color] == self.best_next_card_per_color[color]:
                if rnd.get_valid_cards()[self.highest_card_per_color[color]] != 1:
                    print("Perfect win is not a valid card at the moment :(")
                    continue

                print("Playing perfect card: {}, playingTrump: {}, stillTrumps: {}".format(self.highest_card_per_color[color], (color == rnd.trump), self.check_round_has_still_trumps(rnd)))
                return self.highest_card_per_color[color]

        raise ValueError("Should never reach this line :/. Check for perfect win before calling!")
        return -1

    #TODO: check this method!!
    def _play_lowest_card_with_highest_score(self, rnd: PlayerRound) -> int:
        max_score = -10000 #start with high score
        color_to_play = -1
        color_index = 0

        for s in self.score_per_color:
            if (self.lowest_card_per_color[color_index] == -1 or
                rnd.get_valid_cards()[self.lowest_card_per_color[color_index]] != 1):

                color_index = color_index + 1
                print("No card of Color or not valid at the moment: {}".format(color_index))
                continue #no card in this color or color not valid...continue...

            #check the score and set color to play
            if max_score < s:
                max_score = s
                color_to_play = color_index

            color_index = color_index + 1

        if(color_to_play < 0 or color_to_play > 3 or
            self.lowest_card_per_color[color_to_play] == -1):
            raise ValueError("Color to Play has to be within 0 and 3 and Card != -1!")

        print("Playing lowest card of Best Color! Color: {}, Card: {}, Scores: {}".format(color_to_play, self.lowest_card_per_color[color_to_play], self.score_per_color))
        return self.lowest_card_per_color[color_to_play]

    def _play_schmere_or_lowest_card(self, rnd: PlayerRound) -> int:
        #TODO implement play_schmere_or_lowest_card
        return self._play_lowest_card_of_weakest_color(rnd)

    def _play_lowest_card_of_weakest_color(self, rnd: PlayerRound) -> int:
        min_score = 10000 #start with high score
        color_to_play = -1
        color_index = 0

        for s in self.score_per_color:
            if self.lowest_card_per_color[color_index] == -1:

                color_index = color_index + 1
                print("No card of Color or not valid at the moment: {}".format(color_index))
                continue #no card in this color...continue...

            #check the score and set color to play
            if min_score > s:
                min_score = s
                color_to_play = color_index

            color_index = color_index + 1

        if(color_to_play < 0 or color_to_play > 3 or
            self.lowest_card_per_color[color_to_play] == -1):
            raise ValueError("Color to Play has to be within 0 and 3 and Card != -1!")

        print("Playing lowest card of Weakest Color! Color: {}, Card: {}, Scores: {}".format(color_to_play, self.lowest_card_per_color[color_to_play], self.score_per_color))
        return self.lowest_card_per_color[color_to_play]

    def _play_last_valid_card(self, rnd: PlayerRound) -> int:
        for card in self.highest_card_per_color:
            if card != -1 and rnd.get_valid_cards()[card] == 1:
                return card

        raise ValueError("No valid card anymore!")
        return -1

    def _play_trump(self, rnd: PlayerRound) -> int:
        #TODO check if highest or lowest trump
        trump = self.highest_card_per_color[rnd.trump]
        if trump == -1 or rnd.get_valid_cards()[self.highest_card_per_color[rnd.trump]] != 1:
            raise ValueError("Invalid Trump: Check first if trump is available!")

        print("Playing Trump! Trump: {}".format(trump))
        return trump

    def _get_partner_index(self, myindex: int) -> int:
        if myindex == 0:
            return 2
        if myindex == 1:
            return 3
        if myindex == 2:
            return 0
        if myindex == 3:
            return 1