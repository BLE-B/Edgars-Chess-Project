import os
os.getcwd()
#os.chdir('XXXXX')


'''
The following section creates two lists based on a pgn file. One list includes
all moves made per game in the file, whereas the other lists the players names.
Various lists have to be introduced because of the incremental characteristic
of chess.pgn's read_game function. Additional code was necesary in order to 
eliminate non-standard variants (i.e. chess960 games) from the game list.
'''
import chess.pgn
file = "txt_files/games.txt"
pgn = open(file)
games = []
sides = []
variant = []
drop_list = []
length = 5000

game_list = []
for i in range(length):
    game_list.append(chess.pgn.read_game(pgn))
game_list = list(filter(None, game_list))

# =============================================================================
# for i in range(length):
#     try:
#         if chess.pgn.read_game(pgn).mainline_moves():
#             games.append(chess.pgn.read_game(pgn).mainline_moves())
#             sides.append(chess.pgn.read_game(pgn).headers["White"])
#     except:
#         print(i,chess.pgn.read_game(pgn))
#         pass
# =============================================================================
    
pgn_moves = open(file)
pgn_sides = open(file)
pgn_variant = open(file)

games = []
for i in range(len(game_list)):
    try:
        games.append(chess.pgn.read_game(pgn_moves).mainline_moves())
        sides.append(chess.pgn.read_game(pgn_sides).headers["White"])
        variant.append(chess.pgn.read_game(pgn_variant).headers["Variant"])
    except:
        print('Sum Ting Wong')
        pass
    if variant[i] != 'Standard':
        #print('here here here', i, game_list[i])
        drop_list.append(i)
for counter, j in enumerate(drop_list):
    del games[j-counter]
    del sides[j-counter]
    del variant[j-counter]
    
 
#print(games)
#print('len games:', len(games))
#print('no of 960s:', variant.count('Chess960'))
#print('variant uniques:', set(variant))
#print(games[60])

'''
The following section filters out the selected user's moves within each game
in the game list 'games'. X represents the initial board state, whereas y
represents the following board state (or move that the player decided to play).
This allows for y (or the actual move) to be predicted using the board state x.
'''
X = []
y = []
counter2 = 0
for game in games:
    board = chess.Board()
    #print(board)
    #print(type(board))
    white = sides[counter2]
    if white == 'Bee-Shop':
        remainder = 0
    else:
        remainder = 1
    counter = 0
    for move in game:
        if counter % 2 == remainder:
            X.append(board.copy())
        #print(board)
        #print(white)
        board.push(move)
        if counter % 2 == remainder:
            y.append(board.copy())
        counter += 1
    counter2 += 1
    
'''
The chess dictionary below one-hot encodes each different piece on the chess
board, discriminating by colour. It introduces '.' as a representation of an
empty square.
'''    
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


'''
make_matrix uses a board's status (in binary form) to transform it into the 
epd format and uses its board notation part (0th element) to create a board
matrix based on the chess_dicts keys.
'''
def make_matrix(board): 
    epd = board.epd()
    foo = []  
    pieces = epd.split(" ", 1)[0]
    rows = pieces.split("/")
    for row in rows:
        foo2 = []  
        for thing in row:
            if thing.isdigit():
                for i in range(0, int(thing)):
                    foo2.append('.')
            else:
                foo2.append(thing)
        foo.append(foo2)
    return foo


'''
translate transforms the board matrix into lists of one-hot encoded chess
matrices.
'''
def translate(matrix, chess_dict):
    rows = []
    for row in matrix:
        terms = []
        for term in row:
            terms.append(chess_dict[term])
        rows.append(terms)
    return rows


import numpy as np
# len(X) = 18929 in test_big.txt
for i in range(len(X)):
    #print('Xi', X[i])
    X[i] = translate(make_matrix(X[i]), chess_dict)
for i in range(len(y)):
    y[i] = translate(make_matrix(y[i]), chess_dict)
X = np.array(X) # len(X) = 18929 in test_big.txt
y = np.array(y)
np.save('X', X)


'''
GAN setup below
'''
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


'''
define_discriminator creates the GAN's discriminator. First, it instantiates
two Keras tensors (via Input()) that can be used as input and output variables
in the model (here, it represents the two inputs). The function then defines
six Conv2D layers, each supported by LeakyReLU and a BatchNormalization.
Sigmoid is being used as activation for the output
'''
def define_discriminator():
    init = RandomNormal(stddev=0.02)
    in_src_image = Input(shape=image_shape) # image_shape = (8, 8, 13)
    in_target_image = Input(shape=image_shape)
    merged = concatenate([in_src_image, in_target_image])
    d = Conv2D(64, (4,4), strides=(2,2), padding='same', kernel_initializer=init)(merged)
    d = LeakyReLU(alpha=0.2)(d)
    d = Conv2D(128, (4,4), strides=(2,2), padding='same', kernel_initializer=init)(d)
    d = BatchNormalization()(d)
    d = LeakyReLU(alpha=0.2)(d)
    d = Conv2D(256, (4,4), strides=(2,2), padding='same', kernel_initializer=init)(d)
    d = BatchNormalization()(d)
    d = LeakyReLU(alpha=0.2)(d)
    d = Conv2D(512, (4,4), strides=(2,2), padding='same', kernel_initializer=init)(d)
    d = BatchNormalization()(d)
    d = LeakyReLU(alpha=0.2)(d)
    d = Conv2D(512, (4,4), padding='same', kernel_initializer=init)(d)
    d = BatchNormalization()(d)
    d = LeakyReLU(alpha=0.2)(d)
    d = Conv2D(1, (4,4), padding='same', kernel_initializer=init)(d)
    patch_out = Activation('sigmoid')(d)
    model = Model(inputs = [in_src_image, in_target_image], outputs = patch_out)
    opt = Adam(lr=0.0002, beta_1=0.5)
    model.compile(loss='binary_crossentropy', optimizer=opt, loss_weights=[0.5])
    return model


def define_encoder_block(layer_in, n_filters, batchnorm=True):
    init = RandomNormal(stddev=0.02)
    g = Conv2D(n_filters, (4,4), strides=(2,2), padding='same', kernel_initializer=init)(layer_in)
    if batchnorm:
        g = BatchNormalization()(g, training=True)
    g = LeakyReLU(alpha=0.2)(g)
    return g
 
def decoder_block(layer_in, skip_in, n_filters, dropout=True):
    init = RandomNormal(stddev=0.02)
    g = Conv2DTranspose(n_filters, (4,4), strides=(2,2), padding='same', kernel_initializer=init)(layer_in)
    g = BatchNormalization()(g, training=True)
    if dropout:
        g = Dropout(0.5)(g, training=True)
    g = concatenate([g, skip_in])
    g = Activation('relu')(g)
    return g


def define_generator(image_shape=(8,8,13)):
    init = RandomNormal(stddev=0.02)
    in_image = Input(shape=image_shape)
    e1 = define_encoder_block(in_image, 64, batchnorm=False)
    e2 = define_encoder_block(e1, 128)
    b = Conv2D(512, (4,4), strides=(2,2), padding='same', kernel_initializer=init)(e2)
    b = Activation('relu')(b)
    d6 = decoder_block(b, e2, 128, dropout=False)
    d7 = decoder_block(d6, e1, 64, dropout=False)
    g = Conv2DTranspose(13, (4,4), strides=(2,2), padding='same', kernel_initializer=init)(d7)
    out_image = Activation('softmax')(g)
    model = Model(in_image, out_image)
    return model


def define_gan(g_model, d_model, image_shape):
    d_model.trainable = False
    in_src = Input(shape=image_shape)
    gen_out = g_model(in_src)
    dis_out = d_model([in_src, gen_out])
    model = Model(in_src, [dis_out, gen_out])
    opt = Adam(lr=0.0002, beta_1=0.5)
    model.compile(loss=['binary_crossentropy', 'mae'], optimizer=opt, loss_weights=[1,100])
    return model


def generate_real_samples(dataset, n_samples, patch_shape):
    trainA, trainB = dataset # dataset = [X, y]
    ix = randint(0, trainA.shape[0], n_samples)
    X1, X2 = trainA[ix], trainB[ix]
    y = ones((n_samples, patch_shape, patch_shape, 1)) # output is always real
    return [X1, X2], y
 
def generate_fake_samples(g_model, samples, patch_shape):
    X = g_model.predict(samples)
    y = zeros((len(X), patch_shape, patch_shape, 1)) # output is always fake
    return X, y


def train(d_model, g_model, gan_model, dataset, n_epochs=100, n_batch=1):
#def train(d_model, g_model, gan_model, dataset, n_epochs=1, n_batch=1):
    n_patch = d_model.output_shape[1]
    trainA, trainB = dataset
    print('len train datasets:', len(trainA), len(trainB))
    bat_per_epo = int(len(trainA) / n_batch)
    print('bat_per_epo:', bat_per_epo)
    n_steps = bat_per_epo * n_epochs # 15100 for test.txt (4 games, 151 moves)
    print('n_steps:', n_steps)
    #for i in range(n_steps):
    for i in range(10):
        [X_realA, X_realB], y_real = generate_real_samples(dataset, n_batch, n_patch)
        X_fakeB, y_fake = generate_fake_samples(g_model, X_realA, n_patch)
        d_loss1 = d_model.train_on_batch([X_realA, X_realB], y_real) # discrimininator loss on real data
        d_loss2 = d_model.train_on_batch([X_realA, X_fakeB], y_fake) # discrimininator loss on fake data
        g_loss, _, _ = gan_model.train_on_batch(X_realA, [y_real, X_realB])
        print('>%d, d1[%.3f] d2[%.3f] g[%.3f]' % (i+1, d_loss1, d_loss2, g_loss))
        #print('>rA[%d], rB[%d], noB[%d]' % (X_realA, X_realB, X_fakeB))
        #print(X_realA, X_realB, X_fakeB)
# =============================================================================
#     if (i+1) % (bat_per_epo * 10) == 0:
#         clear_output()
# =============================================================================
        
        
image_shape = (8,8,13)
d_model = define_discriminator()
g_model = define_generator()
gan_model = define_gan(g_model, d_model, image_shape)

train(d_model, g_model, gan_model, [X,y])
Model.save(gan_model, 'models/gan_model')
#loaded_model = load_model('models/gan_model')

import random
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