'''

HUGE thanks to Eddie Sharick who with his tutorial series 
'Chess Engine in Python' (https://www.youtube.com/
playlist?list=PLBwF487qi8MGU81nDGaeNE1EnNEPYWKY_) on YouTube
helped me a lot in understanding how to set up a chess engine in Python.
The code in engine.py and chessAI.py (and, to some extent, main.py) is based
on his work. 

'''


import pygame as p
import sys
import pandas as pd
import engine, chessAI, games, review
from multiprocessing import Process, Queue



BOARD_WIDTH = BOARD_HEIGHT = 960
USER_INTERFACE_PANEL_WIDTH = 300
MOVE_LOG_PANEL_WIDTH = BOARD_WIDTH + USER_INTERFACE_PANEL_WIDTH
MOVE_LOG_PANEL_HEIGHT = 90
USER_INTERFACE_PANEL_HEIGHT = BOARD_HEIGHT
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT // DIMENSION
MAX_FPS = 30
Images = {}
chess_image = p.image.load('images/board.jpg')
p.display.set_icon(chess_image)
# =============================================================================
# move_list, game, game_cap, game_variables, input_dict \
#     = games.get_game()
# =============================================================================





def load_images():
    pieces = ['bp', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wp', 'wR', 'wN', 'wB', 'wQ', 'wK']
    for piece in pieces:
        Images[piece] = p.transform.scale(p.image.load('images/chess pieces/' + piece + '.png'), \
                                          (SQ_SIZE, SQ_SIZE))


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


# =============================================================================
# def main_menu():
#     while True:
#         p.display.set_caption('Edgar\'s Chess Project')
#         header_font = p.font.SysFont(None, 40)
#         screen.fill(p.Color('white'))
#         draw_text('main menu', header_font, p.Color('black'), screen, 20, 20)
#         
#         button_names = ['bt_human_game', 'bt_human_computer_game'\
#                        , 'bt_computer_human_game', 'bt_computer_game', 'bt_game_review']
#         
#         button_locations = [(40, 100, 275, 50), (40, 200, 275, 50)\
#                            , (40, 300, 275, 50), (40, 400, 275, 50), (40, 500, 275, 50)]
#         button_dict = dict(zip(button_names, button_locations))
#         
#         button_human_game = Button(button_locations[0], 'Human vs Human'\
#                                 , main_game, True, True, False)
#         button_human_computer_game = Button(button_locations[1], 'Human vs Computer'\
#                                 , main_game, True, False, False)
#         button_computer_human_game = Button(button_locations[2], 'Computer vs Human'\
#                                 , main_game, False, True, False)
#         button_computer_game = Button(button_locations[3], 'Computer vs Computer'\
#                                 , main_game, False, False, False)
#         button_game_review = Button(button_locations[4], 'Edgar\'s Game Review'\
#                                 , review_menu, True, True, True, colour = 'lightblue')
#         
#         button_list = [button_human_game, button_human_computer_game\
#                        , button_computer_human_game, button_computer_game, button_game_review]
# 
#         lighter_orange = (255, 165, 0) #RGB orange
#                 
#         for count, values in enumerate(button_dict.values()):
#             btnRect = p.Rect(values) # rect of button's image (a pygame.Surface)
#             pointer = p.mouse.get_pos() # (x, y) location of pointer in every frame
#             if btnRect.collidepoint(pointer): # if pointer is inside btnRect
#                 button_list[count].image.fill(lighter_orange) 
# 
#         for e in p.event.get():
#             if e.type == p.QUIT:
#                 p.quit()
#                 sys.exit()
#             if e.type == p.KEYDOWN:
#                 if e.key == p.K_ESCAPE:
#                     p.quit()
#                     sys.exit()
#             if e.type == p.MOUSEBUTTONDOWN:
#                 pass
#             for button in button_list:
#                 button.get_event(e)
#             
#         for button in button_list:
#             button.render(screen)
#  
#         p.display.flip()
#         clock.tick(60)
# =============================================================================


# =============================================================================
# def review_menu(player_one = True, player_two = True, game_review = True):
#     while True:
#         p.display.set_caption('Game Review Menu')
#         header_font = p.font.SysFont(None, 40)
#         base_font = p.font.Font(None, 32)
#         screen.fill(p.Color('white'))
#         draw_text('game review menu', header_font, p.Color('black'), screen, 20, 20)
#         draw_text('Time:', base_font, p.Color('black'), screen, 50, 100) 
#         draw_text('Termination:', base_font, p.Color('black'), screen, 50, 200) 
#         draw_text('Result:', base_font, p.Color('black'), screen, 50, 300) 
#         
# 
#         button_names = ['bt_time_bullet', 'bt_time_blitz', 'bt_time_rapid'\
#                        , 'bt_term_mate', 'bt_term_draw', 'bt_term_resign', 'bt_term_time'\
#                        , 'bt_result_white', 'bt_result_draw', 'bt_result_black'\
#                        , 'bt_submit']
#         
#         button_locations = [(200, 100, 150, 50), (400, 100, 150, 50), (600, 100, 150, 50)\
#                             , (200, 200, 150, 50), (400, 200, 150, 50), (600, 200, 150, 50), (800, 200, 150, 50)\
#                             , (200, 300, 150, 50), (400, 300, 150, 50), (600, 300, 150, 50)\
#                             , (300, 450, 200, 75)]
#         button_dict = dict(zip(button_names, button_locations))
#         
#         bt_time_bullet = Button(button_locations[0], 'Bullet'\
#                                 , None, False, False, True, colour = 'lightgrey', info = 'bullet')
#         bt_time_blitz = Button(button_locations[1], 'Blitz'\
#                                 , None, False, False, True, colour = 'lightgrey', info = 'blitz')
#         bt_time_rapid = Button(button_locations[2], 'Rapid'\
#                                 , None, False, False, True, colour = 'lightgrey', info = 'rapid')
#             
#         bt_term_mate = Button(button_locations[3], 'Checkmate'\
#                                 , None, False, False, True, colour = 'lightgrey', info = 'checkmate')
#         bt_term_draw = Button(button_locations[4], 'Draw'\
#                                 , None, False, False, True, colour = 'lightgrey', info = 'draw')
#         bt_term_resign = Button(button_locations[5], 'Resignation'\
#                                 , None, False, False, True, colour = 'lightgrey', info = 'resign')
#         bt_term_time = Button(button_locations[6], 'Time'\
#                                 , None, False, False, True, colour = 'lightgrey', info = 'time')
#             
#         bt_result_white = Button(button_locations[7], 'White wins'\
#                                 , None, False, False, True, colour = 'lightgrey', info = '1-0')
#         bt_result_draw = Button(button_locations[8], 'Draw'\
#                                 , None, False, False, True, colour = 'lightgrey', info = '1/2-1/2')
#         bt_result_black = Button(button_locations[9], 'Black wins'\
#                                 , None, False, False, True, colour = 'lightgrey', info = '0-1')
#         
#         bt_submit = Button(button_locations[10], 'SUBMIT'\
#                                 , choose_game_menu, False, False, True, colour = 'orange', font_size = 40, df = df2_table)
#         
#         button_list = [bt_time_bullet, bt_time_blitz, bt_time_rapid\
#                        , bt_term_mate, bt_term_draw, bt_term_resign, bt_term_time\
#                        , bt_result_white, bt_result_draw, bt_result_black\
#                        , bt_submit]
#             
#         for e in p.event.get():
#             if e.type == p.QUIT:
#                 main_menu()
#             if e.type == p.KEYDOWN:
#                 if e.key == p.K_ESCAPE:
#                     main_menu()
#             if e.type == p.MOUSEBUTTONDOWN:
#                 pass                          
#             if e.type == p.KEYDOWN:  
#                 pass
#             for button in button_list:
#                 button.get_event(e)
#                 button.click(e)
# 
# # =============================================================================
# #                 if e.type == p.MOUSEBUTTONDOWN:
# #                     if button.rect.collidepoint(p.mouse.get_pos()):
# #                         button.change_colour()
# #                         #button.colour = p.Color('darkgrey')
# #                         #button.image.fill(button.colour)
# # =============================================================================
#                 
#         for button in button_list:
#             button.render(screen)
#         
#         p.display.flip()
#         clock.tick(60)
# =============================================================================
        

# =============================================================================
# def choose_game_menu(df): 
#     input_rect = p.Rect(900, 600, 140, 32)
#     user_text = ''
#     
#     while True:
#         p.display.set_caption('Game Selection Menu')
#         header_font = p.font.SysFont(None, 40)
#         base_font = p.font.Font(None, 12)
#         game_font = p.font.Font(None, 30)
#         screen.fill(p.Color('white'))
#         
#         draw_text('Game?', game_font, p.Color('black'), screen, 900, 570)
#         
#         df_list_ind = df.index.tolist()
#         df_list = df.values.tolist()
#         
#         for x in range(len(df)): 
#             df_list[x].insert(0, df_list_ind[x])
#         
#         width = 20
#         x = 30
#         for i in range(len(df_list)):
#             game_table = font.render(("{}".format(str(df_list[i]).ljust(width))),
#                                        True, p.Color('black'))
#             screen.blit(game_table, (300, x))
#             x = x + 20
#         
#         #draw_text(df, base_font, p.Color('black'), screen, 20, 20)
#         
#         for e in p.event.get():
#             if e.type == p.QUIT:
#                 review_menu()
#             if e.type == p.KEYDOWN:
#                 if e.key == p.K_ESCAPE:
#                     review_menu()
#                 elif e.key == p.K_BACKSPACE:
#                     user_text = user_text[:-1]
#                 elif e.key == p.K_RETURN:
#                     main_game(True, True, True, int(user_text))
#                 else:
#                     user_text += e.unicode
#             if e.type == p.MOUSEBUTTONDOWN:
#                 if input_rect.collidepoint(e.pos):
#                     active = True
#                 else:
#                     active = False                            
#                 
# # =============================================================================
# #             for button in button_list:
# #                 button.get_event(e)
# #                 
# #         for button in button_list:
# #             button.render(screen)
# # =============================================================================
#         
#         p.draw.rect(screen, p.Color('lightgrey'), input_rect)      
#         text_surface = game_font.render(user_text, True, p.Color('black'))          
#         screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
#         input_rect.w = max(100, text_surface.get_width()+10)
#         
#         p.display.flip()
#         clock.tick(60)
# =============================================================================


def main_game(player_one, player_two, game_review, game_df_list = None, game_no = None):
    #player_one, player_two, game_review
    gs = engine.GameState()
    valid_moves = gs.get_valid_moves()
    move_made = False
    animate = False # flag var for animation
    load_images()
    #running = True
    selected_square = () # tuple of selected square
    clicks = [] # list of two tuples with selected squares
    game_over = False
    #player_one = True # True for human player, False for AI player
    #player_two = True
    AI_thinking = False
    AI_process = None
    move_undone = False
    if game_review:
        move_list, game, game_cap, game_variables, input_dict \
            = games.get_game(game_df_list, game_no)
        #print('input dict:', input_dict)
        result_dict = {'1-0': 'White wins.', '1/2-1/2': 'Draw.', '0-1': 'Black wins.'}
        #move_list = iter(move_list)
        move_count = 0
        p.display.set_caption(game_cap)
        player_one = True
        player_two = True
        white_to_move = True
    else:
        if player_one == False and player_two == False:
            p.display.set_caption('Computer chess game')
        elif player_one and player_two:
            p.display.set_caption('Human chess game')
        else:
            p.display.set_caption('Human playing the computer')

    #while running:
    while True:
        screen.fill(p.Color('white'))
        move_log_font = p.font.SysFont('Arial', 14, False, False)
        is_human_turn = (gs.white_to_move and player_one) or (not gs.white_to_move and player_two)
        for e in p.event.get():
            if e.type == p.QUIT:
                #pass
                #main_menu()
                p.quit()
                sys.exit()
                #running = False
            # mouse inputs
            elif e.type == p.MOUSEBUTTONDOWN:
                if not game_over:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if selected_square == (row, col) or col >= 8:
                        selected_square = ()
                        clicks = []
                    else:
                        selected_square = (row, col)
                        clicks.append(selected_square)
                    if len(clicks) == 2 and is_human_turn:
                        move = engine.Move(clicks[0], clicks[1], gs.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                gs.make_move(valid_moves[i])
                                move_made = True
                                animate = True
                                selected_square = ()
                                clicks = []
                                #print(move.get_chess_notation(gs.in_check(), gs.get_valid_moves()))
                                #print(move.get_chess_notation())
                        if not move_made:
                            clicks = [selected_square]
            # key inputs
            elif e.type == p.KEYDOWN:
                if e.key == p.K_ESCAPE:
                    #main_menu()
                    #pass
                    p.quit()
                    sys.exit()
                    
                if e.key == p.K_u: # pressing 'u' undoes the most recent move
                    gs.undo()
                    move_made = True
                    selected_square = ()
                    clicks = []
                    animate = False
                    game_over = False
                    if AI_thinking:
                        move_finder_process.terminate()
                        AI_thinking = False
                    move_undone = True
                    
                if e.key == p.K_r: # pressing 'r' resets the board
                    gs = engine.GameState()
                    valid_moves = gs.get_valid_moves()
                    move_made = False
                    selected_square = ()
                    clicks = []
                    animate = False
                    game_over = False
                    if AI_thinking:
                        move_finder_process.terminate()
                        AI_thinking = False
                    move_undone = True
                
                if game_review and e.key == p.K_LEFT: # pressing left arrow undoes the most recent move in game review
                    gs.undo()
                    move_made = True
                    selected_square = ()
                    clicks = []
                    animate = False
                    game_over = False
                    if AI_thinking:
                        move_finder_process.terminate()
                        AI_thinking = False
                    move_undone = True
                    if move_count >= 1:
                        move_count -= 1
                        white_to_move = not white_to_move
                
                if game_review and e.key == p.K_RIGHT: # pressing right arrow makes the next move in game review
                    #move = engine.Move((6, 3), (4, 3), gs.board)
                    if move_count < len(move_list):
                        start, end, board, en_passant, castle, pawn_promo = review.review_move(move_list[move_count], gs.board, white_to_move)
                        #print('s, e, b:', start, end, gs.board, en_passant, castle, pawn_promo)
                        move = engine.Move(start, end, gs.board, en_passant, castle, pawn_promo)
                        gs.make_move(move)
                        white_to_move = not white_to_move
                        move_count += 1
                    else:
                        game_over = True
                        final_result = result_dict[game_variables['result']]
                    

        # AI part
        if not game_over and not is_human_turn and not move_undone:
            if not AI_thinking:
                AI_thinking = True
                #print('Thinking...')
                return_queue = Queue() # pass data between threads
                move_finder_process = Process(target=chessAI.find_best_move, \
                                              args=(gs, valid_moves, return_queue))
                move_finder_process.start()
                
                # old approach without threading
                #AI_move = chessAI.find_random_move(valid_moves)
                #AI_move = chessAI.find_best_move(gs, valid_moves)
                
            if not move_finder_process.is_alive():
                #print('Done thinking.')
                AI_move = return_queue.get()
                if AI_move == None:
                    AI_move = chessAI.find_random_move(valid_moves)
                gs.make_move(AI_move)
                move_made = True
                animate = True
                AI_thinking = False

        if move_made:
            if animate:
                animate_move(gs.move_log[-1], screen, gs.board, clock)
            valid_moves = gs.get_valid_moves()
            move_made = False
            animate = False
            move_undone = False

        if not game_over:
            draw_game_state(screen, gs, valid_moves, selected_square, move_log_font, game_review)
        else:
            if game_review:
                draw_game_state(screen, gs, valid_moves, selected_square, move_log_font, game_review, final_result)
            else:
                draw_game_state(screen, gs, valid_moves, selected_square, move_log_font, game_review)

        if gs.checkmate or gs.stalemate or gs.repetition:
            game_over = True
            if gs.stalemate:
                text = 'Stalemate.'
            elif gs.repetition:
                text = 'Remis.'
            else:
                text = 'Black wins.' if gs.white_to_move else 'White wins.'
            draw_endgame_text(screen, text)

        clock.tick(MAX_FPS)
        p.display.flip()


def draw_game_state(screen, gs, valid_moves, selected_square, move_log_font, game_review, text = None):
    draw_board(screen)
    highlight(screen, gs, valid_moves, selected_square)
    draw_pieces(screen, gs.board)
    draw_move_log(screen, gs, move_log_font)
    #draw_user_interface(screen, move_log_font, game_review)
    draw_endgame_text(screen, text)


def draw_board(screen):
    global COLOURS
    COLOURS = [p.Color('white'), p.Color('grey')]
    COLOURS = [(240, 217, 181), (181, 136, 99)]
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            colour = COLOURS[((row + column) % 2)]
            p.draw.rect(screen, colour, p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


# original highlight
def highlight(screen, gs, valid_moves, selected_square):
    if selected_square != ():
        r, c = selected_square
        if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # opaqueness (0 -> 255)
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color('yellow'))
            for move in valid_moves:
                if move.start_row == r and move.start_col == c:
                    screen.blit(s, (SQ_SIZE * move.end_col, SQ_SIZE * move.end_row))
        else:
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color('red'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))


# highlight with mouse buttons (currently not implemented)
# =============================================================================
# def highlight(screen, gs, valid_moves, selected_square):
#     if selected_square != ():
#         r, c = selected_square
#         for e in p.event.get():
#         #if p.mouse.get_pressed()[0]:
#             if e.type == p.MOUSEBUTTONDOWN and e.button == 1:
#                 if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'):
#                     s = p.Surface((SQ_SIZE, SQ_SIZE))
#                     s.set_alpha(100) # opaqueness (0 -> 255)
#                     if p.mouse.get_pressed()[0]:
#                       s.fill(p.Color('blue'))
#                     else:
#                       s.fill(p.Color('green'))
#                     screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
#                     s.fill(p.Color('yellow'))
#                     for move in valid_moves:
#                         if move.start_row == r and move.start_col == c:
#                             screen.blit(s, (SQ_SIZE * move.end_col, SQ_SIZE * move.end_row))
#             elif e.type == p.MOUSEBUTTONDOWN and e.button == 2:
#                 s = p.Surface((SQ_SIZE, SQ_SIZE))
#                 s.set_alpha(100)
#                 s.fill(p.Color('red'))
#                 screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
# =============================================================================


def draw_pieces(screen, board):
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]
            if piece != '--':
                screen.blit(Images[piece], p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_move_log(screen, gs, font):
    #move_log_rect = p.Rect(BOARD_WIDTH + 5, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    move_log_rect = p.Rect(0, BOARD_HEIGHT + 5, MOVE_LOG_PANEL_WIDTH + 5, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color('lightgrey'), move_log_rect)
    move_log = gs.move_log
    move_texts = []
    for i in range(0, len(move_log), 2):
        #move_string = str(i//2 + 1) + '. ' + str(move_log[i]) + ' '
        move_string = str(i//2 + 1) + '. ' \
            + move_log[i].get_chess_notation() + ' '
        if i + 1 < len(move_log): # make sure black made a move
            #move_string += str(move_log[i + 1])
            move_string += move_log[i + 1].get_chess_notation()
        move_texts.append(move_string)

    moves_per_row = 18
    padding = 5
    line_spacing = 2
    text_Y = padding
    for i in range(0, len(move_texts), moves_per_row):
        text = ''
        for j in range(moves_per_row):
            if i + j < len(move_texts):
                text += move_texts[i + j] + '   '
        text_object = font.render(text, True, p.Color('black'))
        text_location = move_log_rect.move(padding, text_Y)
        screen.blit(text_object, text_location)
        text_Y += text_object.get_height() + line_spacing
        

# =============================================================================
# def draw_user_interface(screen, font, game_review):
#     user_interface_rect = p.Rect(BOARD_WIDTH + 5, 0, USER_INTERFACE_PANEL_WIDTH, USER_INTERFACE_PANEL_HEIGHT)
#     p.draw.rect(screen, p.Color('lightgrey'), user_interface_rect)
#     padding = 5
#     line_spacing = 2
#     text_Y = padding
#     
#     if game_review:
#         header = font.render('GAME SELECTION', True, p.Color('black'))
#         header_location = user_interface_rect.move(padding, text_Y)
#         screen.blit(header, header_location)
#         
#         text = []
#         input_dict_adj = dict((key, value) for key, value in input_dict.items() if key not in ['result'])
#         for x in input_dict_adj.keys():
#             text.append(font.render(x.capitalize() + ' types:   ' + str(input_dict_adj[x]), True, p.Color('black')))
#         #text_object = font.render(text, True, p.Color('black'))
#         for line in range(len(text)):
#             text_location = user_interface_rect.move(padding, text_Y + header.get_height() + line_spacing)
#             screen.blit(text[line], text_location)
#             text_Y += text[line].get_height() + line_spacing
# =============================================================================

def animate_move(move, screen, board, clock):
    global COLOURS
    d_r = move.end_row - move.start_row
    d_c = move.end_col - move.start_col
    frames_per_square = 5
    frame_count = (abs(d_r) + abs(d_c)) * frames_per_square
    for frame in range(frame_count + 1):
        r, c = (move.start_row + d_r * frame / frame_count, move.start_col + d_c * frame / frame_count)
        draw_board(screen)
        draw_pieces(screen, board)
        # fetch colour of the ending square and overwriting the piece during animation
        colour = COLOURS[(move.end_row + move.end_col) % 2]
        end_square = p.Rect(move.end_col * SQ_SIZE, move.end_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, colour, end_square)
        # redraw captured piece (in case there is one)
        if move.piece_captured != '--':
            if move.is_en_passant_move:
                en_passant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row -1
                end_square = p.Rect(move.end_col * SQ_SIZE, en_passant_row * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(Images[move.piece_captured], end_square)
        # draw moving piece
        if move.piece_moved != '--':
            screen.blit(Images[move.piece_moved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60) # framerate for animation


def draw_endgame_text(screen, text):
    font = p.font.SysFont('Helvetica', 32, False, False)
    text_object = font.render(text, 0, p.Color('Grey'))
    text_location = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - text_object.get_width()/2, \
                                                    BOARD_HEIGHT/2 - text_object.get_height()/2)
                                                    # last part centers the text
    screen.blit(text_object, text_location)
    text_object = font.render(text, 0, p.Color('Red'))
    screen.blit(text_object, text_location.move(2, 2))


def input_checker(question, entry_list):
    while True:
        entry = input(question)
        if entry in entry_list:
            return entry
            break
        else:
            print('Please try again.')


# =============================================================================
# class Button:
#     def __init__(self, rect, text, command, player_one, player_two, game_review\
#                  , colour = p.Color('red'), clicked_colour = p.Color('darkgrey')\
#                  , font = 20, df = None, info = None):
#         self.colour = colour
#         self.clicked_colour = clicked_colour
#         self.rect = p.Rect(rect)
#         self.image = p.Surface(self.rect.size)
#         self.image.fill(self.colour)
#         self.font = p.font.SysFont('Arial', font)
#         self.text = self.font.render(text, 1, p.Color('black'))
#         self.text_rect = self.text.get_rect()
#         self.text_rect.center = (rect[0]+rect[2]/2, rect[1]+rect[3]/2)
#         self.command = command
#         self.player_one = player_one
#         self.player_two = player_two
#         self.game_review = game_review
#         self.df = df
#         self.info = info
#     def render(self, screen):
#         screen.blit(self.image, self.rect)
#         screen.blit(self.text, self.text_rect)
#     def get_event(self, event):
#         if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
#             if self.rect.collidepoint(p.mouse.get_pos()):
#                 if self.command == choose_game_menu:
#                     self.command(self.df)
#                 elif self.command == None:
#                     pass
#                 else:
#                     self.command(self.player_one, self.player_two, self.game_review)
# =============================================================================







class Button:
    def __init__(self, rect, text, command, player_one, player_two, game_review\
                 , colour = p.Color('red'), clicked_colour = p.Color('darkgrey')\
                 , font_size = 20, df = None, info = None):
        self.colour = colour
        self.clicked_colour = clicked_colour
        self.command = command
        self.player_one = player_one
        self.player_two = player_two
        self.game_review = game_review
        self.df = df
        self.info = info
        self.rect = p.Rect(rect)
        self.font_size = font_size
        self.font = p.font.SysFont('Arial', font_size)
        self.text = text
        self.text_item = self.font.render(text, 1, p.Color('black'))
        self.text_rect = self.text_item.get_rect()
        self.text_rect.center = (rect[0]+rect[2]/2, rect[1]+rect[3]/2)
        self.active = False
        self.change()
    def render(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text_item, self.text_rect)
    def change(self):               
        self.image = p.Surface(self.rect.size)
        if self.active == True:
            self.image.fill(self.clicked_colour)
        else:
            self.image.fill(self.colour)
        
# =============================================================================
#     def get_event(self, event):
#         if event.type == p.MOUSEBUTTONDOWN and event.button == 1:
#             if self.rect.collidepoint(p.mouse.get_pos()):
#                 if self.command == choose_game_menu:
#                     self.command(self.df)
#                 elif self.command == None:
#                     pass
#                     #self.change(self.clicked_colour, self.rect, self.font_size, self.text)
#                 else:
#                     self.command(self.player_one, self.player_two, self.game_review)
# =============================================================================
    def click(self, event):
        x, y = p.mouse.get_pos()
        if event.type == p.MOUSEBUTTONDOWN:
            if p.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.active = not self.active
                    print('active:', self.active)
                    #self.change()




                            
                

if __name__ == '__main__':
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + USER_INTERFACE_PANEL_WIDTH + 10\
                             , BOARD_HEIGHT + MOVE_LOG_PANEL_HEIGHT + 5))
    clock = p.time.Clock()
    font = p.font.SysFont(None, 20)
    main_game(True, False, False)
