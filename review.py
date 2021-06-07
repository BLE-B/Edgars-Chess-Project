import itertools
import engine


gs = engine.GameState()

ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4,
               '5': 3, '6': 2, '7': 1, '8': 0}
rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
               'e': 4, 'f': 5, 'g': 6, 'h': 7}
cols_to_files = {v: k for k, v in files_to_cols.items()}



def review_move(move, board, white_to_move):
    #print('white to move?', white_to_move)
       
    start_rank = int()
    start_file = ''
    end_file = move[-2]
    #print('end file:', end_file)
    end_rank = move[-1]
    #print('end rank:', end_rank)
    
    start_row = int()
    start_col = int()
    
    if move[0] != 'O' and 'Q' not in move[1:]:
        end_row = get_row_col(end_rank, end_file)[0]
        #print('end row:', end_row)
        end_col = get_row_col(end_rank, end_file)[1]
        #print('end col:', end_col)
        is_castle_move = False
        is_pawn_promotion = False
    elif move[0] == 'O':
        end_row = end_col = int()
        piece_moved = 'K'
        is_castle_move = True
        is_pawn_promotion = False
    elif 'Q' in move and 'Q' not in move[0]:
        if 'x' in move:
            end_rank = move[3]
            end_file = move[2]
        else:
            end_rank = move[1]
            end_file = move[0]
        end_row = get_row_col(end_rank, end_file)[0]
        end_col = get_row_col(end_rank, end_file)[1]
        is_castle_move = False
        is_pawn_promotion = True
    
    end_square = (end_row, end_col)
    #print('end square:', end_square)
    
    
    is_en_passant_move = False

    directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), \
                       (-1, 0), (0, -1), (1, 0), (0, 1))
    knight_moves = [x for x in itertools.permutations((1, 2, -1, -2), 2) \
           if (abs(x[0]) + abs(x[1])) == 3] # lists all 8 possible knight moves
    straights = [n for n in directions if (n[0] + n[1]) % 2 == 1]
    diags = [n for n in directions if (n[0] + n[1]) % 2 == 0]
    
    # helper variable for cases in which two pieces can access end square
    if move[1].isdigit():
        move_part_row = ranks_to_rows[move[1]]
        move_part_col = ''
    elif move[1] != 'x' and move[1] != '-':
        move_part_row = ''
        move_part_col = files_to_cols[move[1]]

    piece_captured = board[end_row][end_col]
    

    # pawns
    if move[0].islower() == True:
        piece_moved = 'p'
        start_file = move[-2]
        turn_multi = 1 if white_to_move else -1
    
        if 'Q' not in move:
            if len(move) == 2:
                if white_to_move:
                    # two step advance
                    if end_row == 4 and board[5][end_col] == '--':
                        start_rank = 2
                    else:
                        start_rank = int(move[-1]) - turn_multi * 1
                else:
                    #print('board square with pawn on c6:', board[2][end_col])
                    if end_row == 3 and board[2][end_col] == '--':
                        start_rank = 7
                    else:
                        start_rank = int(move[-1]) - turn_multi * 1
            # pawn captures
            elif len(move) == 4:
                start_file = move[0]
                start_rank = int(move[-1]) - turn_multi * 1
                #print('pawn capture start rank:', start_rank)
        else:
            # pawn promotion
            #if move[-1] == 'Q' or move[-2:] == 'Q#' or move[-2:] == 'Q+':
            start_file = move[0]
            start_rank = 7 if white_to_move else 2

    
# =============================================================================
#         # en passant
#         if move blablabla:
#             is_en_passant_move = True
# =============================================================================
        
        start_row = get_row_col(str(start_rank), start_file)[0]
        start_col = get_row_col(str(start_rank), start_file)[1]
        
        #print('start file:', start_file)
        #print('start rank:', start_rank)
    
        
        #print('find stuff:', find('wN', board))
    
    
    # other pieces
    if move[0].isupper() == True and move[0] != 'O':
        piece_moved = move[0]
        
        if piece_moved == 'Q':
            queen_locations = find('wQ', board) if white_to_move else find('bQ', board)
            start_row = find('wQ', board)[0][0] if white_to_move else find('bQ', board)[0][0]
            start_col = find('wQ', board)[0][1] if white_to_move else find('bQ', board)[0][1]
            piece_moved = 'wQ' if white_to_move else 'bQ'
            
            
            if len(move) == 4 and move[1] != 'x' or len(move) == 5:
                for ele in queen_locations:
                    for n in range(1, 8):
                        for di in directions:
                            parts = ele[0] + n*di[0], ele[1] + n*di[1]
                            if 0 <= parts[0] <= 7 and 0 <= parts[1] <= 7:
                                if (parts[0], parts[1]) == end_square:
                                    if move_part_row == ele[0] or move_part_col == ele[1]:
                                        start_row = ele[0]
                                        #print('row:', start_row)
                                        start_col = ele[1]
                                        #print('col:', start_col)
                                        piece_moved = 'wQ' if white_to_move else 'bQ' 
            # only one rook can access end square
            else:
                for ele in queen_locations:
                    for di in directions:
                        for n in range(1, 8):
                            parts = ele[0] + n*di[0], ele[1] + n*di[1]
                            if 0 <= parts[0] <= 7 and 0 <= parts[1] <= 7:
                                if board[parts[0]][parts[1]] == '--' or (parts[0], parts[1]) == end_square:
                                    if (parts[0], parts[1]) == end_square:
                                            start_row = ele[0]
                                            #print('row:', start_row)
                                            start_col = ele[1]
                                            #print('col:', start_col)
                                            piece_moved = 'wQ' if white_to_move else 'bQ'  
                                else: break   
            
            
        elif piece_moved == 'K':
            start_row = find('wK', board)[0][0] if white_to_move else find('bK', board)[0][0]
            start_col = find('wK', board)[0][1] if white_to_move else find('bK', board)[0][1]
            piece_moved = 'wK' if white_to_move else 'bK'
            
        elif piece_moved == 'N':
            knight_locations = find('wN', board) if white_to_move else find('bN', board)
            # both knights can access the end square
            if len(move) == 4 and move[1] != 'x' or len(move) == 5:
                for ele in knight_locations:
                    for knight_move in knight_moves:
                        parts = ele[0] + knight_move[0], ele[1] + knight_move[1]
                        if 0 <= parts[0] <= 7 and 0 <= parts[1] <= 7:
                            if (parts[0], parts[1]) == end_square:
                                if move_part_row == ele[0] or move_part_col == ele[1]:
                                    start_row = ele[0]
                                    #print('row:', start_row)
                                    start_col = ele[1]
                                    #print('col:', start_col)
                                    piece_moved = 'wN' if white_to_move else 'bN'
            # only one knight can access end square
            else:
                for ele in knight_locations:
                    for knight_move in knight_moves:
                        parts = ele[0] + knight_move[0], ele[1] + knight_move[1]
                        if 0 <= parts[0] <= 7 and 0 <= parts[1] <= 7:
                            if (parts[0], parts[1]) == end_square:
                                start_row = ele[0]
                                #print('row:', start_row)
                                start_col = ele[1]
                                #print('col:', start_col)
                                piece_moved = 'wN' if white_to_move else 'bN'
                
        elif piece_moved == 'B':
            bishop_locations = find('wB', board) if white_to_move else find('bB', board)
            for ele in bishop_locations:
                for n in range(1, 7):
                    for diag in diags:
                        parts = ele[0] + n*diag[0], ele[1] + n*diag[1]
                        if 0 <= (parts[0]) < 8 and 0 <= (parts[1]) < 8:
                            if (parts[0], parts[1]) == end_square:
                                start_row = ele[0]
                                #print('row:', start_row)
                                start_col = ele[1]
                                #print('col:', start_col)
                                piece_moved = 'wB' if white_to_move else 'bB'
            
        elif piece_moved == 'R':
            rook_locations = find('wR', board) if white_to_move else find('bR', board)
            # both rooks can access the same end square
            # this is not quite accurate, because it ignores moves such as Rxg7+
            # however, '+' and '#' are not implemented (yet), so it works
            if len(move) == 4 and move[1] != 'x' or len(move) == 5:
                for ele in rook_locations:
                    for n in range(1, 8):
                        for straight in straights:
                            parts = ele[0] + n*straight[0], ele[1] + n*straight[1]
                            if 0 <= parts[0] <= 7 and 0 <= parts[1] <= 7:
                                if (parts[0], parts[1]) == end_square:
                                    if move_part_row == ele[0] or move_part_col == ele[1]:
                                        start_row = ele[0]
                                        #print('row:', start_row)
                                        start_col = ele[1]
                                        #print('col:', start_col)
                                        piece_moved = 'wR' if white_to_move else 'bR' 
            # only one rook can access end square
            else:
                for ele in rook_locations:
                    for straight in straights:
                        for n in range(1, 8):
                            parts = ele[0] + n*straight[0], ele[1] + n*straight[1]
                            if 0 <= parts[0] <= 7 and 0 <= parts[1] <= 7:
                                if board[parts[0]][parts[1]] == '--' or (parts[0], parts[1]) == end_square:
                                    if (parts[0], parts[1]) == end_square:
                                            start_row = ele[0]
                                            #print('row:', start_row)
                                            start_col = ele[1]
                                            #print('col:', start_col)
                                            piece_moved = 'wR' if white_to_move else 'bR'  
                                else: break       

        
    # castle
    if move == 'O-O' or move == 'O-O-O':
        start_row = 7 if white_to_move else 0
        start_col = 4
        end_row = start_row
        end_col = 6 if move == 'O-O' else 2
        is_castle_move = True
        #print('castle stuff:', start_row, start_col, end_row, end_col)
        
    
# =============================================================================
#     print('move:', move, '\nPiece:', piece_moved, '\nCapture:', \
#           piece_captured, '\nEndsquare:', end_file+end_rank, \
#           '\nMoved piece:', piece_moved, '\nPrawn Pomotion:', is_pawn_promotion)
# =============================================================================
    

    start = (start_row, start_col)
    end = (end_row, end_col)
        
    #print(start, end, board)
    
    return start, end, board, is_en_passant_move, is_castle_move, is_pawn_promotion
        

# transform chess notation into python syntax
def get_row_col(r, c):
    return (ranks_to_rows[r], files_to_cols[c])
    

def find(target, board):
    lst = []
    for i, line in enumerate(board):
        for j, piece in enumerate(line):
            if piece == target:
                lst.append((i, j))            
    return lst

# =============================================================================
# wtm = True
# move_list = games.get_game(games.create_game_df('[Ev'))
# move_list = iter(move_list)
# print(review_move(next(move_list), gs.board, wtm))
# wtm = not wtm
# print(review_move(next(move_list), gs.board, wtm))
# wtm = not wtm
# print(review_move(next(move_list), gs.board, wtm))
# =============================================================================


if __name__ == '__main__':
    review_move()