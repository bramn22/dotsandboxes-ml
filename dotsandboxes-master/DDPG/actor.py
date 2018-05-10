from keras.models import Sequential
from keras.layers import Dense, Activation

class Actor:

    def __init__(self, state_dim, action_dim):
        self.model = Sequential()
        self.model.add(Dense(32, input_dim=state_dim))
        self.model.add(Dense(32))
        self.model.add(Dense(2))
        self.model.add(Activation('softmax'))

        self.weights = self.model.trainable_weights


