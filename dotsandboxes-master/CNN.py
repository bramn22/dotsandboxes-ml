import keras
from keras.models import Sequential
from keras.layers import Conv2D, Conv2DTranspose, Dense
from keras.layers import Activation
from keras import optimizers

class CNN:
    def __init__(self, board_size):
        self.model = Sequential()
        #self.model.add(Conv2D(32, (2, 2), input_shape=(3, 3, 2), padding="valid", activation=Activation('tanh')))
        #self.model.add(Conv2D(32, (2, 2), padding="valid"))
        #self.model.add(Conv2DTranspose(board_size, (2, 2)))
        self.model.add(Dense(50))
        sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        self.model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        print(self.model.summary())

    def predict(self):
        pass

    def optimize(self):
        pass