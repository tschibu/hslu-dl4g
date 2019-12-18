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
        self.trumpModel = load_model('models/trump_prediction_model_V10.h5') #'models/trumpV1.H5')....
        self.playCardModel = load_model('models/card_prediction_model_V0.h5')

    def select_trump(self, rnd: PlayerRound) -> int:
        """
        Player chooses a trump based on the given round information.

        Args:
            rnd: current round

        Returns:
            selected trump
        """
        # select the trump with the largest number of cards
        #if rnd.forehand is None:
        #    forehand = 0
        #else:
        #    forehand = 1
        #arr = np.array([np.append(rnd.hand, forehand)])

        trump_weights = self.trumpModel.predict(np.array([rnd.hand]))[0]
        trump_selected = int(np.argmax(trump_weights))
        if trump_selected == 6 and rnd.forehand is None: #want to push and possible
            #print(f'Can Push -> Forehand: {rnd.forehand}')
            return self._assert_if_wrong_trump(int(10), rnd) #Push

        elif trump_selected == 6:
            best_without_pushing = int(np.argmax(trump_weights[0:5]))
            #print(f'Cannot Push anymore -> Best without Push: {best_without_pushing}, Possible Trumps: {trump_weights[0:5]}')
            return self._assert_if_wrong_trump(best_without_pushing, rnd)

        #print(f'Select Trump: {trump_selected}')
        return self._assert_if_wrong_trump(trump_selected, rnd)

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
        player = self._one_hot(rnd.player, 4)
        trump = self._one_hot(rnd.trump, 6)
        current_trick = self._get_current_trick(rnd.tricks)
        arr = np.array([np.append(valid_cards, current_trick)])
        arr = np.array([np.append(arr, player)])
        arr = np.array([np.append(arr, trump)])
        card_to_play = int(np.argmax(self.playCardModel.predict(arr)))

        if valid_cards[card_to_play] == 1: #valid card
            return card_to_play
        else:
            return int(np.nonzero(valid_cards == 1)[0][0])

    def _one_hot(self, number, size):
        """
        One hot encoding for a single value. Output is float array of size size
        Args:
            number: number to one hot encode
            size: length of the returned array
        Returns:
            array filled with 0.0 where index != number and 1.0 where index == number
        """
        result = np.zeros(size, dtype=np.int)
        result[number] = 1
        return result

    def _get_current_trick(self, tricks: np.array):
        current_trick = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        for trick in tricks:
            for card in trick:
                if card != -1:
                    current_trick[card] = 1

        return current_trick

    def _assert_if_wrong_trump(self, trump, rnd):
        need_to_select = rnd.forehand is not None

        if not isinstance(trump, int):
            print("Trump not Int!")
        elif (trump < 0 or trump > 5) and need_to_select:
            print(f'Should select! Trump not in Range {trump}')
        elif (trump < 0 or trump > 5) and trump != 10:
            print(f'Trump not 0-5 or 10: Trump: {trump}')

        return trump
