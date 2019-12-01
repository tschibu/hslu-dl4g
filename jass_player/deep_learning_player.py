import numpy as np
import tensorflow as tf

from jass.base.const import color_masks
from jass.base.player_round import PlayerRound
from jass.player.player import Player
from tensorflow.keras.models import load_model


class DeepLearningPlayer(Player):
    """
    Deep learning implementation of a player to play Jass.
    """

    def __init__(self):
        self.trumpModel = load_model('models/trumpV1.H5')
        # self.trumpModel._make_predict_function()

    def select_trump(self, rnd: PlayerRound) -> int:
        """
        Player chooses a trump based on the given round information.

        Args:
            rnd: current round

        Returns:
            selected trump
        """
        # select the trump with the largest number of cards
        if rnd.forehand is None:
            forehand = 0
        else:
            forehand = 1
        arr = np.array([np.append(rnd.hand, forehand)])

        trump = self.trumpModel.predict(arr)
        return np.argmax(trump)

    def play_card(self, rnd: PlayerRound) -> int:
        """
        Player returns a card to play based on the given round information.

        Args:
            rnd: current round

        Returns:
            card to play, int encoded
        """

        # get the valid cards to play
        valid_cards = rnd.get_valid_cards()

        # select a random card
        return np.random.choice(np.flatnonzero(valid_cards))
