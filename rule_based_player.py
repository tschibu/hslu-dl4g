import numpy as np

from jass.base.const import color_masks
from jass.base.player_round import PlayerRound
from jass.player.player import Player
import RuleBasedPlayer.rbp_trump as rbp_trump
from RuleBasedPlayer.rbp_play import RbpPlay

class RuleBasedPlayer(Player):
    """
    Rule Based implementation of a player to play Jass.
    """
    def __init__(self):
        self.rbp_player = RbpPlay()

    def select_trump(self, rnd: PlayerRound) -> int:
        """
        Player chooses a trump based on the given round information.

        Args:
            rnd: current round

        Returns:
            selected trump
        """
        # select the trump with the largest number of cards
        print(rnd.hand)
        print(rnd.hand.shape)

        #TODO remove like random_choice selection
        #trump = 0
        #max_number_in_color = 0
        #for c in range(4):
        #    number_in_color = (rnd.hand * color_masks[c]).sum()
        #    if number_in_color > max_number_in_color:
        #        max_number_in_color = number_in_color
        #        trump = c
        #return trump

        return rbp_trump.select_by_best_score(rnd)

    def play_card(self, rnd: PlayerRound) -> int:
        """
        Player returns a card to play based on the given round information.

        Args:
            rnd: current round

        Returns:
            card to play, int encoded
        """

        #TODO remove like random_choice selection
        valid_cards = rnd.get_valid_cards()
        return np.random.choice(np.flatnonzero(valid_cards))

        #return self.rbp_player.play_card(rnd)
