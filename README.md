# Edgar's Chess Project


This is a chess game including a state-of-the-art GUI, a lichess.org game selection interface and review mechanic as well as a simple computer opponent to play against - based on a NegaMax algorithm with alpha-beta-pruning and some tweaks regarding positional awareness on the board. General Adversarial Network (GAN)-based EdgarAI implementation to follow as soon as the model has been fully trained.

In order to run the program, run main.py in a python 3 environment with pygame, pyqt5, berserk and chess installed. You will notice that pyqt5 throws a couple of errors (at least when combined with Spyder 5) and all in all this environment is slightly tedious to set up in conda-based python 3.8. In order to train the EdgarAI GAN model, tensorflow 2.5 is required. It is also recommended to install CUDA and cudnn (for my Windows 10 64 machine CUDA 11.2.2 and cudnn 8.1.1 worked like a charm - however, GPU supported keras will require at least 6GB of GPU RAM for this model, potentially more). Either way, training the model may easily take up to 1.5 months (yes, MONTHS) on a regular laptop without dedicated GPU, so please do it at your own risk.

Finally, in order run the program properly, a distribution of stockfish is required. Simply copy the source code (https://github.com/official-stockfish/Stockfish/releases/tag/sf_13) into the main folder and/or adjust the sf_13.py-file accordingly (currently set to "stockfish_13/sf_13.exe"). For more information on this amazing chess engine, check out the official website at https://stockfishchess.org/.

I received quite a bit of help from Eddie Sharick (unknowingly) in his YouTube tutorial series on how to program a chess game in python (as mentioned in the respective files; check out his playlist here: https://youtube.com/playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_. Remember to copy the underscore at the end). Also, the pandas_model file is largely not my own work. Furthermore, the GAN model is largely based on a model created Victor S (https://towardsdatascience.com/magnusgan-using-gans-to-play-like-chess-masters-9dded439bc56), which in turn is based on the pix2pix GAN model (see https://github.com/phillipi/pix2pix). I had to tweak the data processing a bit in order to fit it to my data, but the model as such isn't mine.
