'''

Again, big thanks to Eddie Sharick (see main.py) 

'''


import itertools
import copy



class GameState():
    def __init__(self):
        self.board = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
            ]
        self.move_functions = {'p': self.get_pawn_moves, 'R': self.get_rook_moves, \
                               'N': self.get_knight_moves, 'B': self.get_bishop_moves, \
                               'Q': self.get_queen_moves, 'K': self.get_king_moves}
        self.white_to_move = True
        self.move_log = []
        self.FEN = ''
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.king_locations = {'w': (7, 4), 'b': (0 , 4)}
        self.in_check = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.repetition = False
        self.en_passant_possible = () # Square coordinates where EP is possible
        self.en_passant_possible_log = [self.en_passant_possible] # allows for en passant when multiple moves have been taken back
        self.current_castling_right = CastleRights(True, True, True, True)
        self.half_move_clock = 0
        self.total_moves = 0
        self.castle_rights_log = [CastleRights(self.current_castling_right.wks,
                                                self.current_castling_right.bks,
                                                self.current_castling_right.wqs,
                                                self.current_castling_right.bqs)]
        self.board_log = [self.board]
        # Introducing directions for viable moves
        self.directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), \
                           (-1, 0), (0, -1), (1, 0), (0, 1))
        self.knight_moves = [x for x in itertools.permutations((1, 2, -1, -2), 2) \
               if (abs(x[0]) + abs(x[1])) == 3] # lists all 8 possible knight moves
        self.straights = [n for n in self.directions if (n[0] + n[1]) % 2 == 1]
        self.diags = [n for n in self.directions if (n[0] + n[1]) % 2 == 0]


    def FENizer(self):
        piece_dict = {'bR': 'r', 'bN': 'n', 'bB': 'b', 'bQ': 'q', 'bK': 'k', 'bp': 'p',
                      'wR': 'R', 'wN': 'N', 'wB': 'B', 'wQ': 'Q', 'wK': 'K', 'wp': 'P'}
    
        FEN = []
        for count, rows in enumerate(self.board):
            empty_count = 0
            row_string = ''
            for count_ele, ele in enumerate(rows):
                for key in piece_dict:
                    if ele == key:
                        # IMPORTANT!!! USE BELOW FOR BOARD TRANSLATION!
                        #self.board[count][count_ele] = piece_dict[key]
                        pass
                if ele == '--':
                    empty_count += 1
                    empty_flag = True
                else:
                    if empty_count > 0:
                        row_string += str(empty_count)
                        empty_count = 0
                    row_string += piece_dict[ele]
                    empty_flag = False
            if empty_flag == True:
                row_string += str(empty_count)
            FEN.append(row_string)
    
        FEN = '/'.join(FEN)
        
        FEN += ' w' if self.white_to_move else ' b'
        
        castle_list = ['K', 'Q', 'k', 'q']
        castle_string = ''
        castle_rights = [self.current_castling_right.wks,
                         self.current_castling_right.wqs,
                         self.current_castling_right.bks,
                         self.current_castling_right.bqs]

        for count, ele in enumerate(castle_rights):
            if ele: castle_string += castle_list[count]
        if castle_string == '':
            castle_string += '-'
        
        FEN += ' ' + castle_string

        FEN += ' ' + self.get_rank_file(self.en_passant_possible[0], 
                                        self.en_passant_possible[1]) \
            if self.en_passant_possible != () else ' -'
        
        FEN += ' ' + str(self.half_move_clock)
        
        FEN += ' ' + str(self.total_moves)
        
        return FEN
     

    # make a move
    def make_move(self, move):
        if self.white_to_move:
            self.total_moves += 1
        self.board[move.start_row][move.start_col] = '--'
        self.board[move.end_row][move.end_col] = move.piece_moved
        self.move_log.append(move)
        #self.board_log.append(self.board)
        self.white_to_move = not self.white_to_move
        if move.piece_moved == 'wK':
            self.king_locations['w'] = (move.end_row, move.end_col)
        elif move.piece_moved == 'bK':
            self.king_locations['b'] = (move.end_row, move.end_col)

        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_col] = move.piece_moved[0] + 'Q'

        if move.is_en_passant_move:
            self.board[move.start_row][move.end_col] = '--'

        if move.piece_moved[1] == 'p' and abs(move.end_row - move.start_row) == 2:
            self.en_passant_possible = ((move.start_row + move.end_row) // 2, move.end_col)
        else:
            self.en_passant_possible = ()

        if move.is_castle_move: # moves the rook (king already moved)
            if move.end_col - move.start_col == 2: # kingside castle
                self.board[move.end_row][move.end_col - 1] \
                    = self.board[move.end_row][move.end_col + 1] # copy rook pos
                self.board[move.end_row][move.end_col + 1] = '--' # deletes old rook
            else:
                self.board[move.end_row][move.end_col + 1] \
                    = self.board[move.end_row][move.end_col - 2] # copy rook pos
                self.board[move.end_row][move.end_col - 2] = '--' # deletes old rook

        self.en_passant_possible_log.append(self.en_passant_possible)

        self.update_castle_rights(move)
        self.castle_rights_log.append(CastleRights(self.current_castling_right.wks, \
                                                    self.current_castling_right.bks, \
                                                    self.current_castling_right.wqs, \
                                                    self.current_castling_right.bqs))
        
        #print(self.FENizer())


    # undo move
    def undo(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_row][move.start_col] = move.piece_moved
            self.board[move.end_row][move.end_col] = move.piece_captured
            self.white_to_move = not self.white_to_move

            if move.piece_moved == 'wK':
                self.king_locations['w'] = (move.start_row, move.start_col)
            elif move.piece_moved == 'bK':
                self.king_locations['b'] = (move.start_row, move.start_col)

            # en passant
            if move.is_en_passant_move:
                self.board[move.end_row][move.end_col] = '--'
                self.board[move.start_row][move.end_col] = move.piece_captured
            self.en_passant_possible_log.pop()
            self.en_passant_possible = self.en_passant_possible_log[-1]

            # castling
            if move.is_castle_move:
                if move.end_col - move.start_col == 2: # kingside castle
                    self.board[move.end_row][move.end_col + 1] \
                        = self.board[move.end_row][move.end_col - 1] # copy rook pos
                    self.board[move.end_row][move.end_col - 1] = '--' # deletes castled rook
                else:
                    self.board[move.end_row][move.end_col - 2] \
                        = self.board[move.end_row][move.end_col + 1] # copy rook pos
                    self.board[move.end_row][move.end_col + 1] = '--' # deletes castled rook
            # castle rights
            self.castle_rights_log.pop()
            castle_rights_help = copy.deepcopy(self.castle_rights_log[-1])
            self.current_castling_right = castle_rights_help

            self.checkmate = False
            self.stalemate = False
            self.repetition = False


    # update castle rights during game
    def update_castle_rights(self, move):
        if move.piece_moved[1] == 'K':
            if move.piece_moved[0] == 'w':
                self.current_castling_right.wks = self.current_castling_right.wqs = False
            else: self.current_castling_right.bks = self.current_castling_right.bqs = False
        elif move.piece_moved[1] == 'R':
            if move.start_col == 0:
                if move.piece_moved[0] == 'w':
                    self.current_castling_right.wqs = False
                else: self.current_castling_right.bqs = False
            elif move.start_col == 7:
                if move.piece_moved[0] == 'w':
                    self.current_castling_right.wks = False
                else: self.current_castling_right.bks = False
        if move.piece_captured[1] == 'R':
            if move.end_col == 0:
                if move.piece_captured[0] == 'w':
                    self.current_castling_right.wqs = False
                else:
                    self.current_castling_right.bqs = False
            elif move.end_col == 7:
                if move.piece_captured[0] == 'w':
                    self.current_castling_right.wks = False
                else:
                    self.current_castling_right.bks = False


    # tracks the attacked squares
    def square_attacked(self, r, c): # checking for a specific square whether it is attacked or not
        self.white_to_move = not self.white_to_move # switch to opponent
        opp_moves = self.get_possible_moves()
        self.white_to_move = not self.white_to_move
        for moves in opp_moves:
            if moves.end_row == r and moves.end_col == c:
                return True
        return False


    # doesn't do much, I suppose
    def in_check(self):
        return self.square_attacked(self.king_locations['w'][0] if self.white_to_move \
                                    else self.king_locations['b'][0], \
                                    self.king_locations['w'][1] if self.white_to_move \
                                    else self.king_locations['b'][1])


    # this function gets all the actually valid moves
    def get_valid_moves(self):
        # actually valid moves (i.e. possible moves minus check in the following move)
        # includes a range of functions that are reversed within
        # gen moves, make moves, gen opponent moves, check for checks --> not valid
        temp_en_passant_possible = self.en_passant_possible
        temp_castle_rights = CastleRights(self.current_castling_right.wks, \
                                         self.current_castling_right.bks, \
                                         self.current_castling_right.wqs, \
                                         self.current_castling_right.bqs)
        moves = []
        
        
        #moves = self.get_possible_moves() # to be deleted
        
        
        self.in_check, self.pins, self.checks = self.check_for_pins_and_checks()
        # checks returns 1: checking_piece_row, 2: checking_piece_col, 3/4: checking directions
        king_row = self.king_locations['w'][0] if self.white_to_move else self.king_locations['b'][0]
        king_col = self.king_locations['w'][1] if self.white_to_move else self.king_locations['b'][1]
        if self.in_check:
            if len(self.checks) == 1: # 1 checking piece
                #print('Checks: ', self.checks)
                moves = self.get_possible_moves()
                check = self.checks[0]
                check_row = check[0]
                check_col = check[1]
                checking_piece = self.board[check_row][check_col]
                #print('Checking piece: ', checking_piece)
                valid_squares = [] # valid squares for pieces
                if checking_piece[1] == 'N':
                    # capture knight or nothing (move king)
                    valid_squares = [(check_row, check_col)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_row + check[2] * i, king_col + check[3] * i)
                        valid_squares.append(valid_square)
                        # if checking piece is captured, break
                        if valid_square[0] == check_row and valid_square[1] == check_col:
                            break
                for i in range(len(moves) -1, -1, -1):
                    if moves[i].piece_moved[1] != 'K':
                        if not (moves[i].end_row, moves[i].end_col) in valid_squares:
                            moves.remove(moves[i])
            else: # 2 checking pieces, king has to move
                self.get_king_moves(king_row, king_col, moves)
        else:
            moves = self.get_possible_moves()
            
        if self.white_to_move:
            self.get_castle_moves(self.king_locations['w'][0], self.king_locations['w'][1], moves)
        else:
            self.get_castle_moves(self.king_locations['b'][0], self.king_locations['b'][1], moves)
# =============================================================================
#         this code was being used for the simple, inefficient check check
#         for i in range(len(moves)-1, -1, -1): # iterates backwards through move list
#             self.make_move(moves[i])
#             self.white_to_move = not self.white_to_move
#             if self.in_check:
#                 moves.remove(moves[i])
#             self.white_to_move = not self.white_to_move
#             self.undo()
# =============================================================================
        if len(moves) == 0:
            if self.in_check:
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
            
        # repetition part
        if len(self.board_log) >= 5:
            if self.board_log[-1] == self.board_log[-3] == self.board_log[-5]:
                self.repetition = True
        else:
            self.repetition = False

        self.en_passant_possible = temp_en_passant_possible
        self.current_castling_right = temp_castle_rights

        return moves


    # this function simply adds all possible moves, ignoring their validity
    def get_possible_moves(self): # moves possible according to the general move patterns
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                #print(self.board)
                #print('turn:', turn, 'board:', self.board[r][c], 'castle rights:', self.current_castling_right)
                if (turn == 'w' and self.white_to_move) or (turn == 'b' and not self.white_to_move):
                    piece = self.board[r][c][1]
                    #print('r:', r, 'turn:', turn, 'white?', self.white_to_move, 'piece:', piece)
                    self.move_functions[piece](r, c, moves)
        return moves


    # checker for pins and checks
    def check_for_pins_and_checks(self):
        pins = []
        checks = []
        in_check = False
        enemy = 'b' if self.white_to_move else 'w'
        ally = 'w' if self.white_to_move else 'b'
        start_row = self.king_locations['w'][0] if self.white_to_move else self.king_locations['b'][0]
        start_col = self.king_locations['w'][1] if self.white_to_move else self.king_locations['b'][1]
        for j in range(len(self.directions)):
            d = self.directions[j]
            possible_pin = ()
            for i in range(1, 8):
                end_row = start_row + d[0] * i
                end_col = start_col + d[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally and end_piece[1] != 'K':
                        if possible_pin == ():
                            possible_pin = (end_row, end_col, d[0], d[1])
                        else: #second ally piece, so no pin possible
                            break
                    elif end_piece[0] == enemy:
                        piece_type = end_piece[1]
                        # 1) orthogonal rook check
                        # 2) diagonal bishop check
                        # 3) 1 square diagonal pawn check
                        # 4) any direction queen check
                        # 5) any direction king 'check'
                        if (0 <= j <= 3 and piece_type == 'B') or \
                            (4 <= j <= 7 and piece_type == 'R') or \
                            (i == 1 and piece_type == 'p' and ((enemy == 'w' and 2 <= j <= 3) or \
                                                         (enemy == 'b' and 0 <= j <= 1))) or \
                            (piece_type == 'Q') or (i == 1 and piece_type == 'K'):
                            if possible_pin == (): # no piece blocking --> check
                                in_check = True
                                checks.append((end_row, end_col, d[0], d[1]))
                                break
                            else: # piece blocking --> pin
                                pins.append(possible_pin)
                                break
                        else: # no checks
                            break
                else: # off board
                    break
        for m in self.knight_moves:
            end_row = start_row + m[0]
            end_col = start_col + m[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy and end_piece[1] == 'N':
                    in_check = True
                    checks.append((end_row, end_col, m[0], m[1]))
                    #print('Check!')
        return in_check, pins, checks


    '''
    Here come the moves!
    You better watch out!
    '''
    # all the pawn moves
    def get_pawn_moves(self, r, c, moves):
        #pass
# =============================================================================
#         # very simple pawn moves (commented out)
#         if self.board[r - 1 if self.white_to_move else r + 1][c] == '--':
#             moves.append(Move((r, c), (r - 1 if self.white_to_move else r + 1, c), self.board))
#             if r == 6 if self.white_to_move else r == 1 and self.board[r - 2][c] == '--':
#                 moves.append(Move((r, c), (r - 2, c), self.board))
# =============================================================================
        piece_pinned = False
        pin_direction = ()
        # check list of pinned pieces and whether current piece is in there
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:
            move_amount = -1
            start_row = 6
            enemy = 'b'
        else:
            move_amount = 1
            start_row = 1
            enemy = 'w'
        king_row, king_col = self.king_locations['w'] if self.white_to_move else self.king_locations['b']
        #print('pawn_r:', r, 'pawn_c:', r, 'move_amount:', move_amount)
        if self.board[r + move_amount][c] == '--':
            if not piece_pinned or pin_direction == (move_amount, 0):
                moves.append(Move((r, c), (r + move_amount, c), self.board))
                if r == start_row and self.board[r + (move_amount * 2)][c] == '--':
                    moves.append(Move((r, c), (r + (move_amount * 2), c), self.board))
        if c - 1 >= 0: # pawn captures to the left
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[r + move_amount][c - 1][0] == enemy:
                    moves.append(Move((r, c), (r + move_amount, c - 1), self.board))
                if (r + move_amount, c - 1) == self.en_passant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == r:
                        if king_col < c: # king is left of the pawn
                            # inside between king and pawn; outside between pawn and border
                            inside_range = range(king_col + 1, c - 1)
                            outside_range = range(c + 1, 8)
                        else:
                            inside_range = range(king_col - 1 , c, -1)
                            outside_range = range(c - 2, -1, -1)
                        for i in inside_range:
                            if self.board[r][i] != '--': # another piece beside en passant piece is blocking
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[r][i]
                            if square[0] == enemy and (square[1] == 'R' or square[1] == 'Q'):
                                attacking_piece = True
                            elif square != '--':
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((r, c), (r + move_amount, c - 1), self.board, is_en_passant_move = True))
        if c + 1 <= (len(self.board[0]) - 1): # pawn captures to the right
            if not piece_pinned or pin_direction == (move_amount, 1):
                if self.board[r + move_amount][c + 1][0] == enemy:
                    moves.append(Move((r, c), (r + move_amount, c + 1), self.board))
                if (r + move_amount, c + 1) == self.en_passant_possible:
                    attacking_piece = blocking_piece = False
                    if king_row == r:
                        if king_col < c: # king is left of the pawn
                            # inside between king and pawn; outside between pawn and border
                            inside_range = range(king_col + 1, c)
                            outside_range = range(c + 2, 8)
                        else:
                            inside_range = range(king_col - 1, c + 1, -1)
                            outside_range = range(c - 1, -1, -1)
                        for i in inside_range:
                            if self.board[r][i] != '--': # another piece beside en passant piece is blocking
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[r][i]
                            if square[0] == enemy and (square[1] == 'R' or square[1] == 'Q'):
                                attacking_piece = True
                            elif square != '--':
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((r, c), (r + move_amount, c + 1), self.board, is_en_passant_move = True))
# =============================================================================
#         # old malarkey
#         else:
#             if self.board[r + 1][c] == '--':
#                 if not piece_pinned or pin_direction == (1, 0):
#                     moves.append(Move((r, c), (r + 1, c), self.board))
#                     if r == 1 and self.board[r + 2][c] == '--':
#                         moves.append(Move((r, c), (r + 2, c), self.board))
#             if c - 1 >= 0: # pawn captures to the left
#                 if not piece_pinned or pin_direction == (1, -1):
#                     if self.board[r + 1][c - 1][0] == 'w':
#                         moves.append(Move((r, c), (r + 1, c - 1), self.board))
#                     elif (r + 1, c - 1) == self.en_passant_possible:
#                         moves.append(Move((r, c), (r + 1, c - 1), self.board, is_en_passant_move = True))
#             if c + 1 <= (len(self.board[0]) - 1): # pawn captures to the right
#                 if not piece_pinned or pin_direction == (1, 1):
#                     if self.board[r + 1][c + 1][0] == 'w':
#                         moves.append(Move((r, c), (r + 1, c + 1), self.board))
#                     elif (r + 1, c + 1) == self.en_passant_possible:
#                         moves.append(Move((r, c), (r + 1, c + 1), self.board, is_en_passant_move = True))
# =============================================================================

    # all the rook moves
    def get_rook_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][1] != 'Q':
                    self.pins.remove(self.pins[i])
                break

        enemy = 'b' if self.white_to_move else 'w'
        for s in self.straights:
            for n in range(1, 8):
                end_row = r + s[0] * n
                end_col = c + s[1] * n
                if 0 <= end_row < 8 and 0 <= end_col < 8: # board
                    # moves toward AND away from pin are allowed
                    if not piece_pinned or pin_direction == s or pin_direction == (-s[0], -s[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == '--':
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break # breaks once enemy piece is hit
                        else:
                            break # breaks once own piece is hit
                else:
                    break # breaks if off board

    # all the knight moves
    def get_knight_moves(self, r, c, moves):
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        enemy = 'b' if self.white_to_move else 'w'
        for k in self.knight_moves:
            end_row = r + k[0]
            end_col = c + k[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if not piece_pinned:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == enemy or end_piece == '--':
                        moves.append(Move((r, c), (end_row, end_col), self.board))

    # all the bishop moves
    def get_bishop_moves(self, r, c, moves):
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        enemy = 'b' if self.white_to_move else 'w'
        for d in self.diags:
            for n in range(1, 8):
                end_row = r + d[0] * n
                end_col = c + d[1] * n
                if 0 <= end_row < 8 and 0 <= end_col < 8: # board
                    if not piece_pinned or pin_direction == d or pin_direction == (-d[0], -d[1]):
                        end_piece = self.board[end_row][end_col]
                        if end_piece == '--':
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                        elif end_piece[0] == enemy:
                            moves.append(Move((r, c), (end_row, end_col), self.board))
                            break # breaks once enemy piece is hit
                        else:
                            break # breaks once own piece is hit
                else:
                    break # breaks if off board

    # all the queen moves
    def get_queen_moves(self, r, c, moves):
        self.get_bishop_moves(r, c, moves)
        self.get_rook_moves(r, c, moves)

    # all the king moves
    def get_king_moves(self, r, c, moves):
        #row_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        #col_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        enemy = 'b' if self.white_to_move else 'w'
        for i in range(8):
            end_row = r + self.directions[i][0]
            end_col = c + self.directions[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8: # board
                end_piece = self.board[end_row][end_col]
                if end_piece[0] == enemy or end_piece == '--':
                    if enemy == 'b':
                        self.king_locations['w'] = (end_row, end_col)
                    else:
                        self.king_locations['b'] = (end_row, end_col)
                    in_check, pins, checks = self.check_for_pins_and_checks()
                    if not in_check:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    if enemy == 'b':
                        self.king_locations['w'] = (r, c)
                    else:
                        self.king_locations['b'] = (r, c)

    # castle moves
    def get_castle_moves(self, r, c, moves):
        if self.square_attacked(r, c):
            return # no castling for you when in check!
        if (self.white_to_move and self.current_castling_right.wqs) or \
                (not self.white_to_move and self.current_castling_right.bqs):
            if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
                if not self.square_attacked(r, c-1) and not self.square_attacked(r, c-2):
                    moves.append(Move((r, c), (r, c-2), self.board, is_castle_move=True))
        if (self.white_to_move and self.current_castling_right.wks) or \
                (not self.white_to_move and self.current_castling_right.bks):
            if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
                if not self.square_attacked(r, c+1) and not self.square_attacked(r, c+2):
                    moves.append(Move((r, c), (r, c+2), self.board, is_castle_move=True))
    
    
    # first part allows for translation into chess notation
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4,
                   '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                   'e': 4, 'f': 5, 'g': 6, 'h': 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}
    # transform python syntax into chess notation
    def get_rank_file(self, r, c):
        #print('r:', r, 'c:', c)
        return self.cols_to_files[c] + self.rows_to_ranks[r]


# store castling rights
class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


# instantiates moves on the board
class Move():
    # first part allows for translation into chess notation
    ranks_to_rows = {'1': 7, '2': 6, '3': 5, '4': 4,
                   '5': 3, '6': 2, '7': 1, '8': 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_cols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                   'e': 4, 'f': 5, 'g': 6, 'h': 7}
    cols_to_files = {v: k for k, v in files_to_cols.items()}


    # init
    def __init__(self, start, end, board, is_en_passant_move = False, \
                 is_castle_move = False, is_pawn_promotion = False):
        self.start_row = start[0]
        self.start_col = start[1]
        self.end_row = end[0]
        self.end_col = end[1]

        self.piece_moved = board[self.start_row][self.start_col]
        self.piece_captured = board[self.end_row][self.end_col]

# =============================================================================
#         self.is_pawn_promotion = self.piece_moved[1] == 'p' and \
#             (self.end_row == 0 or self.end_row == 7)
# =============================================================================
        
        self.is_pawn_promotion = is_pawn_promotion
        self.is_pawn_promotion = (self.piece_moved == 'wp' and self.end_row == 0) \
            or (self.piece_moved == 'bp' and self.end_row == 7)

        self.is_en_passant_move = is_en_passant_move
        if self.is_en_passant_move:
            self.piece_captured = 'wp' if self.piece_moved == 'bp' else 'bp'

        self.is_castle_move = is_castle_move

        self.is_capture = self.piece_captured != '--'

        # hash moves for better identification
        self.move_ID = self.start_row * 1000 + self.start_col * 100 + self.end_row * 10 + self.end_col
        #print('moveID:', self.move_ID)

    # override equals method (__eq__), so that moves can be inserted via different means
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False


    # chess notation
    def get_chess_notation(self, in_check = False, checkmate = 0, repetition = False):
        #return self.get_rank_file(self.end_row, self.end_col)
        if self.piece_moved[1] == 'p':
            if not self.is_capture:
                if in_check:
                    if checkmate == []:
                        return self.get_rank_file(self.end_row, self.end_col) + '#'
                    else: return self.get_rank_file(self.end_row, self.end_col) + '+'
                elif self.piece_moved[0] == 'w' and int(self.get_rank_file(self.end_row, self.end_col)[1]) == 8:
                    return self.get_rank_file(self.end_row, self.end_col) + '=Q'
                elif self.piece_moved[0] == 'b' and int(self.get_rank_file(self.end_row, self.end_col)[1]) == 1:
                    return self.get_rank_file(self.end_row, self.end_col) + '=Q'
                else: return self.get_rank_file(self.end_row, self.end_col)
                return self.get_rank_file(self.end_row, self.end_col)
            else:
                if in_check:
                    if checkmate == []:
                        return self.get_rank_file(self.start_row, self.start_col)[0] + 'x' + self.get_rank_file(self.end_row, self.end_col) + '#'
                    else: return self.get_rank_file(self.start_row, self.start_col)[0] + 'x' + self.get_rank_file(self.end_row, self.end_col) + '+'
                elif self.piece_moved[0] == 'w' and int(self.get_rank_file(self.end_row, self.end_col)[1]) == 8:
                    return self.get_rank_file(self.start_row, self.start_col)[0] + 'x' + self.get_rank_file(self.end_row, self.end_col) + '=Q'
                elif self.piece_moved[0] == 'b' and int(self.get_rank_file(self.end_row, self.end_col)[1]) == 1:
                    return self.get_rank_file(self.start_row, self.start_col)[0] + 'x' + self.get_rank_file(self.end_row, self.end_col) + '=Q'
                else: return self.get_rank_file(self.start_row, self.start_col)[0] + 'x' + self.get_rank_file(self.end_row, self.end_col)
                return self.get_rank_file(self.start_row, self.start_col)[0] + 'x' + self.get_rank_file(self.end_row, self.end_col)
        else:
            if not self.is_capture:
                 if self.is_castle_move:
                     return 'O-O' if self.end_col == 6 else 'O-O-O'
                 if in_check:
                     if checkmate == []:
                         return self.piece_moved[1] + self.get_rank_file(self.end_row, self.end_col) + '#'
                     else: return self.piece_moved[1] + self.get_rank_file(self.end_row, self.end_col) + '+'
                 else: return self.piece_moved[1] + self.get_rank_file(self.end_row, self.end_col)
                 return self.piece_moved[1] + self.get_rank_file(self.end_row, self.end_col)
            else:
                if in_check:
                    if checkmate == []:
                        return self.piece_moved[1] + 'x' + self.get_rank_file(self.end_row, self.end_col) + '#'
                    else: return self.piece_moved[1] + 'x' + self.get_rank_file(self.end_row, self.end_col) + '+'
                else: return self.piece_moved[1] + 'x' + self.get_rank_file(self.end_row, self.end_col)
                return self.piece_moved[1] + 'x' + self.get_rank_file(self.end_row, self.end_col)


    # transform python syntax into chess notation
    def get_rank_file(self, r, c):
        #print('r:', r, 'c:', c)
        return self.cols_to_files[c] + self.rows_to_ranks[r]


    # override str method
    def __str__(self):
        if self.is_castle_move:
            return 'O-O' if self.end_col == 6 else 'O-O-O'

        end_square = self.get_rank_file(self.end_row, self.end_col)

        if self.piece_moved[1] == 'p':
            if self.is_capture:
                return self.cols_to_files[self.start_col] + 'x' + end_square
            else:
                return end_square

        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += 'x'        
# =============================================================================
#         if GameState.in_check() == (3, 4): # ?????
#             print('Check True') # ????
#             return move_string + end_square + '+' # ????
# =============================================================================
        return move_string + end_square


if __name__ == '__main__':
    GameState()