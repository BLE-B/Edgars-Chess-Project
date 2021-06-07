'''

Again, big thanks to Eddie Sharick (see main.py) 

'''


import random


piece_scores = {'K': 0, 'Q': 9, 'R': 5, 'B': 3, 'N': 3, 'p': 1}

knight_score = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishop_score = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 3, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 3, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4]]

rook_score =   [[3, 4, 4, 4, 4, 4, 4, 3],
                [3, 3, 3, 3, 3, 3, 3, 3],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 1],
                [3, 4, 3, 3, 2, 3, 4, 3],
                [3, 4, 4, 4, 4, 4, 4, 3]]

queen_score =  [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

white_pawn_score = [[9, 9, 9, 9, 9, 9, 9, 9],
                    [4, 4, 4, 4, 4, 4, 4, 4],
                    [3, 3, 4, 4, 4, 4, 3, 3],
                    [2, 2, 3, 4, 4, 3, 2, 2],
                    [2, 2, 3, 4, 4, 3, 2, 2],
                    [1, 2, 2, 3, 3, 1, 2, 1],
                    [1, 1, 1, 0, 0, 2, 2, 2],
                    [0, 0, 0, 0, 0, 0, 0, 0]]

black_pawn_score = [[0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 0, 0, 2, 2, 2],
                    [1, 2, 2, 3, 3, 1, 2, 1],
                    [2, 2, 3, 4, 4, 3, 2, 2],
                    [2, 2, 3, 4, 4, 3, 2, 2],
                    [3, 3, 4, 4, 4, 4, 3, 3],
                    [4, 4, 4, 4, 4, 4, 4, 4],
                    [9, 9, 9, 9, 9, 9, 9, 9]]


piece_position_scores = {'N': knight_score, 'B': bishop_score, 'R': rook_score, \
                         'Q': queen_score, 'wp': white_pawn_score, 'bp': black_pawn_score}

CHECKMATE_SCORE = 9999
STALEMATE_SCORE = 0
DEPTH = 4




def find_random_move(valid_moves):
    return random.choice(valid_moves)

def find_best_move_without_recursion(gs, valid_moves):
    turn_multi = 1 if gs.white_to_move else -1
    opponents_min_max_score = CHECKMATE_SCORE
    opponents_max_score = 0
    best_player_move = None
    random.shuffle(valid_moves)
    for player_move in valid_moves:
        gs.make_move(player_move)
        opponents_moves = gs.get_valid_moves()
        if gs.stalemate:
            opponents_max_score = STALEMATE_SCORE
        elif gs.checkmate:
            opponents_max_score = -CHECKMATE_SCORE
        else:
            opponents_max_score = -CHECKMATE_SCORE
            for opponents_move in opponents_moves:
                gs.make_move(opponents_move)
                gs.get_valid_moves()
                if gs.checkmate:
                    score = CHECKMATE_SCORE
                elif gs.stalemate:
                    score = STALEMATE_SCORE
                score = -turn_multi * score_material(gs.board)
                if score > opponents_max_score:
                    opponents_max_score = score
                gs.undo()
        if opponents_max_score < opponents_min_max_score:
            opponents_min_max_score = opponents_max_score
            best_player_move = player_move
        gs.undo()
    return best_player_move


# helper method to make first recursive call
def find_best_move(gs, valid_moves, return_queue):
    global NEXT_MOVE, COUNTER
    NEXT_MOVE = None
    random.shuffle(valid_moves)
    COUNTER = 0
    #find_move_min_max(gs, valid_moves, DEPTH, gs.white_to_move)
    #find_move_nega_max(gs, valid_moves, DEPTH, 1 if gs.white_to_move else -1)
    find_move_nega_max_alpha_beta(gs, valid_moves, DEPTH, -CHECKMATE_SCORE, CHECKMATE_SCORE, 1 if gs.white_to_move else -1)
    #print(COUNTER)
    return_queue.put(NEXT_MOVE)


    # algorithm that finds max scores for white and min scores (negativ max) for black
def find_move_min_max(gs, valid_moves, depth, white_to_move):
    global NEXT_MOVE
    if depth == 0:
        return score_material(gs.board)

    if white_to_move:
        max_score = CHECKMATE_SCORE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_min_max(gs, next_moves, depth - 1, False)
            if score > max_score:
                max_score = score
                if depth == DEPTH:
                    NEXT_MOVE = move
            gs.undo()
        return max_score
    else:
        min_score = -CHECKMATE_SCORE
        for move in valid_moves:
            gs.make_move(move)
            next_moves = gs.get_valid_moves()
            score = find_move_min_max(gs, next_moves, depth - 1, True)
            if score < min_score:
                min_score = score
                if depth == DEPTH:
                    NEXT_MOVE = move
            gs.undo()
        return min_score


# algorithm that always finds max scores for both white and black (almost identical to MinMax-algorithm)
def find_move_nega_max(gs, valid_moves, depth, turn_multi):
    global NEXT_MOVE, COUNTER
    COUNTER += 1
    if depth == 0:
        return turn_multi * score_board(gs)
    max_score = -CHECKMATE_SCORE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_nega_max(gs, next_moves, depth - 1, -turn_multi)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                NEXT_MOVE = move
        gs.undo()
    return max_score


'''
NegaMax-algorithm with alpha beta pruning (discards evaluating positions where opponent gets huge advantage).
alpha and beta serve as threshold values
'''
def find_move_nega_max_alpha_beta(gs, valid_moves, depth, alpha, beta, turn_multi):
    global NEXT_MOVE, COUNTER
    COUNTER += 1
    if depth == 0:
        return turn_multi * score_board(gs)
    max_score = -CHECKMATE_SCORE
    for move in valid_moves:
        gs.make_move(move)
        next_moves = gs.get_valid_moves()
        score = -find_move_nega_max_alpha_beta(gs, next_moves, depth - 1, -beta, -alpha, -turn_multi)
        if score > max_score:
            max_score = score
# =============================================================================
#             if max_score == CHECKMATE_SCORE:
#                 NEXT_MOVE = move
# =============================================================================
            if depth == DEPTH:
                NEXT_MOVE = move
                print(move, score)
        gs.undo()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


# Positive score = white winning
def score_board(gs):
    if gs.checkmate:
        if gs.white_to_move:
            return -CHECKMATE_SCORE # white is checkmated
        else:
            return CHECKMATE_SCORE
    elif gs.stalemate:
        return STALEMATE_SCORE

    score = 0
    for row in range(len(gs.board)): # range 8
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != '--':
                piece_position_score = 0
                if square[1] != 'K': # no position scores for kings yet
                    if square[1] == 'p':
                        piece_position_score = piece_position_scores[square][row][col]
                    else:
                        piece_position_score = piece_position_scores[square[1]][row][col]
                if square[0] == 'w':
                    score += piece_scores[square[1]] + piece_position_score * .1
                elif square[0] == 'b':
                    score -= piece_scores[square[1]] + piece_position_score * .1

    return score



def score_material(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += piece_scores[square[1]]
            elif square[0] == 'b':
                score -= piece_scores[square[1]]

    return score
