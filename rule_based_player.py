import numpy as np

from jass.base.player_round import PlayerRound
from jass.player.player import Player
import RuleBasedPlayer.rbp_trump as rbp_trump

class RuleBasedPlayer(Player):
    """
    Rule Based implementation of a player to play Jass.
    """

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

        return rbp_trump.select_by_best_wins(rnd)

    def play_card(self, rnd: PlayerRound) -> int:
        """
        Player returns a card to play based on the given round information.

        Args:
            rnd: current round

        Returns:
            card to play, int encoded
        """
        # play random

        # get the valid cards to play
        valid_cards = rnd.get_valid_cards()

        # select a random card
        return np.random.choice(np.flatnonzero(valid_cards))
