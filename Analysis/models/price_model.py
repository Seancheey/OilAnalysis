"""Price Model

The task of our price model should be predicting future N days oil prices given previous M days of data.

"""

from keras import Sequential
from keras.layers import Dense, LSTM
from keras.optimizers import adam
from keras.losses import mse


class FeatureExtractionAutoEncoder(Sequential):

    def __init__(self, input_shape: int):
        super().__init__()

        # encoder
        self.add(Dense(input_shape, activation='relu', input_shape=(input_shape,)))
        self.add(Dense(20, activation='relu'))

        # bottleneck layer
        self.add(Dense(10, activation='relu'))

        # decoder
        self.add(Dense(20, activation='relu'))
        self.add(Dense(input_shape))

        self.compile(adam(lr=0.01), loss=mse)


class PredictorLSTM(Sequential):

    def __init__(self, input_shape: int, output_shape: int):
        super().__init__()
        self.add(LSTM(128, input_shape=(input_shape,), dropout=0.2, recurrent_dropout=0.2))
        self.add(Dense(output_shape))

        self.compile(adam(lr=0.01), loss=mse)
