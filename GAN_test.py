from numpy import expand_dims
from numpy import zeros
from numpy import ones
from numpy import vstack
from numpy.random import randn
from numpy.random import randint
from keras.utils import plot_model
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D,Conv2DTranspose
from keras.layers.pooling import MaxPooling2D
from keras.layers.merge import concatenate
from keras.initializers import RandomNormal
from keras.layers import LeakyReLU
from keras.layers import BatchNormalization
from keras.layers import Activation,Reshape
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers import Dropout



chess_dict = {
    'p' : [1,0,0,0,0,0,0,0,0,0,0,0,0],
    'P' : [0,0,0,0,0,0,1,0,0,0,0,0,0],
    'n' : [0,1,0,0,0,0,0,0,0,0,0,0,0],
    'N' : [0,0,0,0,0,0,0,1,0,0,0,0,0],
    'b' : [0,0,1,0,0,0,0,0,0,0,0,0,0],
    'B' : [0,0,0,0,0,0,0,0,1,0,0,0,0],
    'r' : [0,0,0,1,0,0,0,0,0,0,0,0,0],
    'R' : [0,0,0,0,0,0,0,0,0,1,0,0,0],
    'q' : [0,0,0,0,1,0,0,0,0,0,0,0,0],
    'Q' : [0,0,0,0,0,0,0,0,0,0,1,0,0],
    'k' : [0,0,0,0,0,1,0,0,0,0,0,0,0],
    'K' : [0,0,0,0,0,0,0,0,0,0,0,1,0],
    '.' : [0,0,0,0,0,0,0,0,0,0,0,0,1],
}





import random
import numpy as np
from keras.models import load_model

X = np.load('X.npy')
gan_model = load_model('models/gan_model_500k')

flatten = lambda l: [item for sublist in l for item in sublist]
instance = random.randint(1,len(X)-1) # len(X) = 18929 in test_big.txt
print('len X:', len(X))
state = X[instance].reshape(1,8,8,13) # list of 8 matrices of 8x13 (zeros & ones; 13 different pieces)
action = gan_model.predict(state)[1] # list of 8 matrices of 8x13 (model output (tensors); the 13 numbers add to 100)


new_chess_dict = {}
for k, v in chess_dict.items():
    new_chess_dict[tuple(v)] = k
def retranslate(action):
    board = []
    flatten_action = flatten(flatten(action))
    print('len_flatten_action:', len(flatten_action)) # len(flatten_action) = 64
    for i in range(len(flatten_action)):
        new_set = np.zeros((13,))
        max_index = list(flatten_action[i]).index(max(flatten_action[i]))
        # each i list consists of 13 numbers, adding up to 1
        #print('list flatten action', list(flatten_action[i]))
        #print('max flatten', max(flatten_action[i]))
        new_set[max_index] = 1
        board.append(new_set)
        # len(board) = 64
    for i in range(len(board)):
        #pass
        #print(board[i])
        board[i] = new_chess_dict[tuple(board[i])]
        #board[i] = chess_dict[tuple(board[i])]
    board = np.array(board).reshape(8,8)
    print(board)


retranslate(state)
retranslate(action)