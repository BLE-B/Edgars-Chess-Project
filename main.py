from PyQt5 import QtGui, QtCore 
from PyQt5.QtWidgets import *
import pygame as p
import pygame_gui as p_gui
import sys, time
import pandas_model
import engine, chessAI, games, review, sf_13
from multiprocessing import Process, Queue



class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        
        self.setWindowTitle('Edgar\'s Chess Project')
        self.setWindowIcon(QtGui.QIcon('images/board.jpg'))
        self.setFixedSize(1030, 850)
        
        ##self.setCentralWidget(StartScreen())
        
        self.show_start_screen()
        
# =============================================================================
#         self.stacked_layout = QStackedLayout()
#         self.stacked_layout.addWidget(self.start_ui_widget)
#         
#         self.central_widget = QWidget()
#         self.central_widget.setLayout(self.stacked_layout)
#         self.setCentralWidget(self.central_widget)
# =============================================================================

    def show_start_screen(self):
        self.start = StartScreen()
        self.start.switch_window.connect(self.show_main_menu)
        self.start.show()
        
    def show_main_menu(self):
        self.main_menu = MainMenu()
        self.start.close()
        self.main_menu.show()
    

class StartScreen(QWidget):   
    switch_window = QtCore.pyqtSignal()
    
    def __init__(self, parent = None):
        super(StartScreen, self).__init__()

        self.setWindowTitle('Edgar\'s Chess Project')
        self.setWindowIcon(QtGui.QIcon('images/board.jpg'))

        #self.surface = surface
        self.LEFT = 200
        self.TOP = 100
        self.WIDTH = 1030
        self.HEIGHT = 850
        self.setFixedSize(1030, 850)
        
        self.start_ui()
        #self.game_selection_ui()
        #self.init_pygame(game)  
        
    def start_ui(self):
        #self.setLayout(QVBoxLayout())
        self.setLayout(QGridLayout())
        
        #logo widget
        image = QtGui.QPixmap('images\project.png')
        logo = QLabel(self)
        #logo.setGeometry(self.LEFT, self.TOP, self.WIDTH, self.HEIGHT)
        logo.setPixmap(image)
        logo.setAlignment(QtCore.Qt.AlignCenter)
        logo.setStyleSheet('margin-top: 100px;')


        #self.setLayout(QLayout())
        #self.layout().addWidget(start_label)
        
        #self.button = QAbstractButton(self)
        #self.button.setPixmap(image)
        #self.button.setGeometry(self.LEFT, self.TOP, self.WIDTH, self.HEIGHT)
        
        
        
        self.button_game_select = QPushButton(self)
        self.button_game_select.setText('START')
        #self.button_game_select.move(self.LEFT, (self.TOP + 200))                                      
        self.button_game_select.setStyleSheet('background-color: grey; \
                                              color: white; \
                                              border-style: outset; \
                                              border-width: 2px; \
                                              border-radius: 10px; \
                                              border-color: black; \
                                              font: 14px; \
                                              padding: 6px; \
                                              min-width: 10px; \
                                              ')                                              
                                              
        #self.button_game_select.clicked.connect(self.clear_layout)
        self.button_game_select.clicked.connect(self.switch)
        
        
        self.layout().addWidget(logo)
        self.layout().addWidget(self.button_game_select)
        
        
    def switch(self):
        self.switch_window.emit()



class MainMenu(QMainWindow):
    switch_window = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()


        self.setWindowTitle('Edgar\'s Chess Project')
        self.setWindowIcon(QtGui.QIcon('images/board.jpg'))


        self.LEFT = 200
        self.TOP = 100
        self.WIDTH = 1030
        self.HEIGHT = int(0.8 * self.WIDTH)
        self.setFixedSize(self.WIDTH, self.HEIGHT)




        # add all widgets
        self.btn_1 = QPushButton('Play', self)
        self.btn_1.setObjectName('m1_button')
        self.btn_2 = QPushButton('Review', self)
        self.btn_2.setObjectName('m2_button')
        self.btn_3 = QPushButton('Options', self)
        self.btn_3.setObjectName('m3_button')
        self.btn_4 = QPushButton('Credits', self)
        self.btn_4.setObjectName('m4_button')

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)


        self.btn_5 = QPushButton('Human vs. Human', clicked = lambda: self.init_pygame(True, True, False))
        self.btn_5.setObjectName('p1_button')
        self.btn_6 = QPushButton('Play Computer as White', clicked = lambda: self.init_pygame(True, False, False))
        self.btn_6.setObjectName('p2_button')
        self.btn_7 = QPushButton('Play Computer as Black', clicked = lambda: self.init_pygame(False, True, False))
        self.btn_7.setObjectName('p3_button')
        self.btn_8 = QPushButton('Watch Computer Game', clicked = lambda: self.init_pygame(False, False, False))
        self.btn_8.setObjectName('p4_button')

# =============================================================================
#         self.btn_5.clicked.connect(self.button1)
#         self.btn_6.clicked.connect(self.button2)
#         self.btn_7.clicked.connect(self.button3)
#         self.btn_8.clicked.connect(self.button4)
# =============================================================================


        # add tabs
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()

        self.initUI()

    def initUI(self):
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none;}''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # ----------------- 
    # buttons

    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)

    def button4(self):
        self.right_widget.setCurrentIndex(3)

    # ----------------- 
    # pages

    def ui1(self):
        main_layout = QVBoxLayout()
        play_label = QLabel('Play Game')
        play_label.setFont(QtGui.QFont(None, 30))
        main_layout.addWidget(play_label)
        main_layout.addStretch(1)
        main_layout.addWidget(QLabel('Please select from the following game options'))
        main_layout.addStretch(1)
        button_layout = QGridLayout() 
        button_layout.addWidget(self.btn_5, 0, 0)
        button_layout.addWidget(self.btn_6, 1, 0)
        button_layout.addWidget(self.btn_7, 1, 1)
        button_layout.addWidget(self.btn_8, 0, 1)
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        main_layout.addWidget(button_widget)
        main_layout.addStretch(50)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui2(self):
        main_layout = QVBoxLayout()
        game_selection_label = QLabel('Game Selection')
        game_selection_label.setFont(QtGui.QFont(None, 30))
        main_layout.addWidget(game_selection_label)
        main_layout.addWidget(ReviewMenu())
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui3(self):
        main_layout = QVBoxLayout()
        options_label = QLabel('Options')
        options_label.setFont(QtGui.QFont(None, 30))
        main_layout.addWidget(options_label)
        main_layout.addStretch(1)
        main_layout.addWidget(QLabel('Nah. Not really. Maybe some time in the future ;-)'))
        main_layout.addStretch(51)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui4(self):
        main_layout = QVBoxLayout()
        credit_label = QLabel('Credits')
        credit_label.setFont(QtGui.QFont(None, 30))
        main_layout.addWidget(credit_label)
        main_layout.addStretch(1)
        main_layout.addWidget(QLabel('Made by Edgar. Enjoy! :-)'))
        main_layout.addStretch(51)
        main = QWidget()
        main.setLayout(main_layout)
        return main
    
    
    def init_pygame(self, player_one, player_two, game_review):
        #p.init()
        self.game = Game(player_one, player_two, game_review)
# =============================================================================
#         self.timer = QtCore.QTimer()
#         self.timer.timeout.connect(self.pygame_loop)
#         self.timer.start(0)
#         
#     
#     def pygame_loop(self):
#         if self.game.main_game():
#             #self.close()
#             #p.display.quit()
#             pass
# =============================================================================


        
        
class ReviewMenu(QWidget):   
    
    switch_window = QtCore.pyqtSignal()
    
    def __init__(self, parent = None):
        super(ReviewMenu, self).__init__()

        self.setWindowTitle('Edgar\'s Chess Project')
        self.setWindowIcon(QtGui.QIcon('images/board.jpg'))

        self.LEFT = 300
        self.TOP = 200
        self.WIDTH = 1030
        self.HEIGHT = 850
        #self.setFixedSize(1030, 850)
        #self.setGeometry(self.LEFT, self.TOP, self.WIDTH, self.HEIGHT)
        
        self.game_selection_ui()
        #self.game_selection_ui()
        #self.init_pygame(game)                    
    
    def game_selection_ui(self):
        # layout
        self.setLayout(QGridLayout())
        main_layout_width = self.frameGeometry().width()
        main_layout_height = self.frameGeometry().height()
        
        # labels
        game_no_label = QLabel('Game number')
        game_no_label.setFont(QtGui.QFont(None, 30))
        #game_selection_label = QLabel('Game Selection')
        #game_selection_label.setFont(QtGui.QFont(None, 30))
        
        game_type_label = QLabel('Time type')
        game_type_label.setFont(QtGui.QFont('Arial', 10))
        game_termination_label = QLabel('Termination')
        game_termination_label.setFont(QtGui.QFont('Arial', 10))
        game_result_label = QLabel('Result')
        game_result_label.setFont(QtGui.QFont('Arial', 10))
        player_name_label = QLabel('Player Name')
        player_name_label.setFont(QtGui.QFont('Arial', 10))
        game_since_label = QLabel('Date since')
        game_since_label.setFont(QtGui.QFont('Arial', 10))
        game_until_label = QLabel('Date until')
        game_until_label.setFont(QtGui.QFont('Arial', 10))
        
        # entry boxes
        game_entry = QLineEdit(self)
        game_entry.setObjectName('game_selectah')
        game_entry.setPlaceholderText('Enter game number')
        game_entry.textChanged.connect(self.line_changed)
        game_entry.setEnabled(False)
        player_entry = QLineEdit(self)
        player_entry.setObjectName('player_selectah')
        player_entry.setText('Bee-Shop')
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        game_entry.setSizePolicy(sizePolicy)
        player_entry.setSizePolicy(sizePolicy)
        
        # combo boxes
        time_combo = QComboBox(self, editable = False)
        termination_combo = QComboBox(self, editable = False)
        result_combo = QComboBox(self, editable = False)
        game_keys = ['times', 'termination', 'result']
        game_values = [
            ['Blitz', 'Bullet', 'Correspondence', 'Rapid'],
            ['Checkmate', 'Draw', 'Resignation', 'Time'],
            ['White wins', 'Draw', 'Black wins']
            ] 
        game_dict = dict(zip(game_keys, game_values))
        for item in game_dict['times']:    
            time_combo.addItem(item)
        for item in game_dict['termination']:    
            termination_combo.addItem(item)
        for item in game_dict['result']:    
            result_combo.addItem(item)
        time_combo.setObjectName('time_selectah')
        termination_combo.setObjectName('termination_selectah')
        result_combo.setObjectName('result_selectah')
        
        # date boxes
        date_since_box = QDateEdit(self)
        #date_since_box.setGeometry(100, 100, 150, 40)
        date_since_box_preset = QtCore.QDate(2020, 1, 1)
        date_since_box.setDate(date_since_box_preset)
        
        date_until_box = QDateEdit(self)
        #date_until_box.setGeometry(100, 100, 150, 40)
        date_until_box_preset = QtCore.QDate(2020, 6, 1)
        date_until_box.setDate(date_until_box_preset)
        
        # spin boxes
        #game_spin = QSpinBox(self, value = 0, maximum = 100, 
        #        minimum = 0, singleStep = 1, prefix = 'Game #')
        
        # buttons
        api_games = 'txt_files/api_games.txt'
        all_games = 'txt_files/games.txt'
        load_all_data_button = QPushButton('Load All Games', clicked = lambda: press_it(all_games))
        load_api_data_button = QPushButton('Load API Games', clicked = lambda: press_it(api_games))
# =============================================================================
#         load_api_data_button.setStyleSheet('color: black; \
#                                               border-style: outset; \
#                                               border-width: 2px; \
#                                               border-radius: 1px; \
#                                               border-color: black; \
#                                               font: 14px; \
#                                               padding: 1px; \
#                                               min-width: 10px; \
#                                               ')
# =============================================================================
        self.start_review_button = QPushButton('Start Game Review', 
                clicked = lambda: self.init_pygame(True, True, True, self.game_df_list, game_entry.text()))
        self.start_review_button.setEnabled(False)
        
        # text boxes
        game_text = QTextEdit()
        #self.layout().addWidget(game_text)
        
        # table boxes
        game_table = QTableView()
        game_table.setFixedHeight(int(main_layout_height * 1.25))
        game_table.show()
    
        
        self.layout().addWidget(game_type_label, 0, 2)
        #game_type_label.setAlignment(QtCore.Qt.AlignRight)
        self.layout().addWidget(game_termination_label, 0, 3)
        self.layout().addWidget(game_result_label, 0, 4)
        self.layout().addWidget(player_name_label, 0, 5)
        self.layout().addWidget(game_since_label, 0, 0)
        self.layout().addWidget(game_until_label, 0, 1)

        #self.layout().addWidget(game_no_label)
        #self.layout().addWidget(game_selection_label, 0, 0, 1, 3)
        self.layout().addWidget(time_combo, 1, 2)
        self.layout().addWidget(termination_combo, 1, 3)
        self.layout().addWidget(result_combo, 1, 4)
        self.layout().addWidget(player_entry, 1, 5)
        self.layout().addWidget(date_since_box, 1, 0)
        self.layout().addWidget(date_until_box, 1, 1)
        
        self.layout().addWidget(load_api_data_button, 2, 0, 1, 1)
        self.layout().addWidget(load_all_data_button, 2, 1, 1, 1)
        self.layout().addWidget(game_table, 3, 0, 1, 6)
        #self.layout().addWidget(game_spin)
        self.layout().addWidget(game_entry, 4, 3, 1, 2)
        self.layout().addWidget(self.start_review_button, 4, 4, 1, 2)
        

        def press_it(game_file):
            game_entry.setEnabled(True)
            
            # labels
# =============================================================================
#             game_no_label.setText(f'Game no.: {my_entry.text()}, {game_spin.value()}')
#             game_no = my_entry.text(), game_spin.value()
#             print('game number:', game_no)
#             my_entry.setText('')
#             game_selection_label.setText(f'Time: {time_combo.currentText()}')
# =============================================================================
            
            # combo boxes
            time = time_combo.currentText()
            time_index = time_combo.currentIndex()
            termination = termination_combo.currentText()
            termination_index = termination_combo.currentIndex()
            result = result_combo.currentText()
            result_index = result_combo.currentIndex()
            self.game_selection_index = [time_index, termination_index, result_index]
            self.game_selection = [time, termination, result]
            print('game selection:', self.game_selection)
            self.player_selection = player_entry.text()
            print('player selection:', self.player_selection)
            
            # date boxes
            date_since = date_since_box.date().toPyDate()
            date_since = [date_since.day, date_since.month, date_since.year]
            date_until = date_until_box.date().toPyDate()
            date_until = [date_until.day, date_until.month, date_until.year]
            
            # text boxes
            games.get_lichess_games(date_since,
                                    date_until,
                                    self.game_selection[0].lower(),
                                    self.player_selection,
                                    300)
            self.game_df_list = games.create_game_df(game_file,
                                                     '[Ev',
                                                     self.game_selection[0],
                                                     self.game_selection[1],
                                                     self.game_selection[2])[1]
            #game_text.setPlainText(games.create_game_df('txt_files/api_games.txt', '[Ev')[1].to_string())
            game_table.setModel(pandas_model.pandasModel(self.game_df_list))
            
            # spin boxes
            #self.game = game_entry.text()
            
            return True, True, True, self.game_df_list, game_entry.text()

    
    def init_pygame(self, player_one, player_two, game_review, game_df_list, game_no):
        #p.init()
        self.game = Game(player_one, player_two, game_review, game_df_list, game_no)
# =============================================================================
#         self.timer = QtCore.QTimer()
#         self.timer.timeout.connect(self.pygame_loop)
#         self.timer.start(0)
#         
#     
#     def pygame_loop(self):
#         if self.game.main_game():
#             #self.close()
#             #p.display.quit()
#             pass
# =============================================================================
        
    
    def switch(self):
        self.switch_window.emit(self.line_edit.text())
        

    #@QtCore.pyqtSlot(str)                
    def line_changed(self, text):
        if text:
            self.start_review_button.setEnabled(True)
        else:
            self.start_review_button.setEnabled(False)
        



class Game(QWidget):
    def __init__(self, 
                 player_one = True, 
                 player_two = True, 
                 game_review = False, 
                 game_df_list = None, 
                 game_no = None):
        super().__init__()

        p.display.set_icon(p.image.load('images/board.jpg'))
        
        self.game_init(player_one, 
                       player_two, 
                       game_review, 
                       game_df_list, 
                       game_no)


    def game_init(self, 
                  player_one, 
                  player_two, 
                  game_review, 
                  game_df_list = None, 
                  game_no = None):

        self.BOARD_WIDTH = self.BOARD_HEIGHT = 960
        self.USER_INTERFACE_PANEL_WIDTH = 300
        self.MOVE_LOG_PANEL_WIDTH = self.BOARD_WIDTH + self.USER_INTERFACE_PANEL_WIDTH
        self.MOVE_LOG_PANEL_HEIGHT = 90
        self.USER_INTERFACE_PANEL_HEIGHT = self.BOARD_HEIGHT
        self.DIMENSION = 8
        self.SQ_SIZE = self.BOARD_HEIGHT // self.DIMENSION
        self.MAX_FPS = 30
        self.size = self.BOARD_WIDTH + self.USER_INTERFACE_PANEL_WIDTH + 10,\
                    self.BOARD_HEIGHT + self.MOVE_LOG_PANEL_HEIGHT + 5
        self.screen = p.display.set_mode((self.size))
        # DELETE THE PYGAME FRAME WHILE INITIALIZING THE SCREEN
        #self.screen = p.display.set_mode((self.size), p.NOFRAME)
        self.clock = p.time.Clock()
        self.font = p.font.SysFont(None, 20)
        self.Images = {}
        
        # Players: True for human player, False for AI player
        self.player_one = player_one
        self.player_two = player_two
        self.game_review = game_review
        self.game_df_list = game_df_list
        if game_no != None:
            self.game_no = int(game_no)
        
        self.gs = engine.GameState()
        self.valid_moves = self.gs.get_valid_moves()
        self.move_made = False
        self.animate = False # flag var for animation
        self.load_images()
        self.selected_square = () # tuple of selected square
        self.clicks = [] # list of two tuples with selected squares
        self.game_over = False
        self.AI_thinking = False
        self.AI_process = None
        self.eval = self.evaluation()
        self.move_undone = False
        self.move_log_font = p.font.SysFont('Arial', 14, False, False)
        
        if self.game_review:
            self.move_list, self.game, self.game_cap, self.game_variables, self.input_dict \
                = games.get_game(self.game_df_list, self.game_no)
            #print('input dict:', input_dict)
            self.result_dict = {'1-0': 'White wins.', '1/2-1/2': 'Draw.', '0-1': 'Black wins.'}
            self.move_count = 0
            p.display.set_caption(self.game_cap)
            self.player_one = True
            self.player_two = True
            self.white_to_move = True
        else:
            if self.player_one == False and self.player_two == False:
                p.display.set_caption('Computer chess game')
            elif self.player_one and self.player_two:
                p.display.set_caption('Human chess game')
            else:
                p.display.set_caption('Human playing the computer')
        
        # GUI stuff
        self.manager = p_gui.UIManager((self.size[0], self.size[1]), 'themes/base_theme.json')
        self.eval_button = p_gui.elements.UIButton(relative_rect=p.Rect((965, 460), (100, 40)),
                                             text='Show Eval',
                                             manager=self.manager)
        self.eval_text = p_gui.elements.UILabel(relative_rect=p.Rect((1065, 460), (200, 40)),
                                             text=str(self.eval),
                                             manager=self.manager)
        
        self.main_game()

    
    def main_game(self):
        self.screen.fill(p.Color('white'))
        
        while True:
            time_delta = self.clock.tick(self.MAX_FPS)
            self.is_human_turn = (self.gs.white_to_move and self.player_one) \
                or (not self.gs.white_to_move and self.player_two)
            for e in p.event.get():
                if e.type == p.QUIT:
                    p.display.quit()
                    #p.quit()
                    #sys.exit()
                    return False
                # GUI inputs
                if e.type == p.USEREVENT:
                     if e.user_type == p_gui.UI_BUTTON_PRESSED:
                         if e.ui_element == self.eval_button:
                             self.eval_text.set_text(str(self.evaluation()))
                # mouse inputs
                if e.type == p.MOUSEBUTTONDOWN:
                    if not self.game_over:
                        location = p.mouse.get_pos()
                        col = location[0] // self.SQ_SIZE
                        row = location[1] // self.SQ_SIZE
                        if self.selected_square == (row, col) or col >= 8:
                            self.selected_square = ()
                            self.clicks = []
                        else:
                            self.selected_square = (row, col)
                            self.clicks.append(self.selected_square)
                        if len(self.clicks) == 2 and self.is_human_turn:
                            move = engine.Move(self.clicks[0], self.clicks[1], self.gs.board)
                            for i in range(len(self.valid_moves)):
                                if move == self.valid_moves[i]:
                                    self.gs.make_move(self.valid_moves[i])
                                    self.move_made = True
                                    self.animate = True
                                    self.selected_square = ()
                                    self.clicks = []
                                    #print(move.get_chess_notation(self.gs.in_check(), self.gs.get_valid_moves()))
                                    #print(move.get_chess_notation())
                            if not self.move_made:
                                self.clicks = [self.selected_square]
                # key inputs
                elif e.type == p.KEYDOWN:
                    if e.key == p.K_ESCAPE:
                        p.display.quit()
                        #p.quit()
                        #sys.exit()
                        return False
                    if e.key == p.K_u: # pressing 'u' undoes the most recent move
                        self.gs.undo()
                        self.move_made = True
                        self.selected_square = ()
                        self.clicks = []
                        self.animate = False
                        self.game_over = False
                        if self.AI_thinking:
                            move_finder_process.terminate()
                            self.AI_thinking = False
                        self.move_undone = True
                        
                    if e.key == p.K_r: # pressing 'r' resets the board
                        self.gs = engine.GameState()
                        self.valid_moves = self.gs.get_valid_moves()
                        self.move_made = False
                        self.selected_square = ()
                        self.clicks = []
                        self.animate = False
                        self.game_over = False
                        if self.AI_thinking:
                            move_finder_process.terminate()
                            self.AI_thinking = False
                        self.move_undone = True
                    
                    if self.game_review and e.key == p.K_LEFT: # pressing left arrow undoes the most recent move in game review
                        self.gs.undo()
                        self.move_made = True
                        self.selected_square = ()
                        self.clicks = []
                        self.animate = False
                        self.game_over = False
                        if self.AI_thinking:
                            move_finder_process.terminate()
                            self.AI_thinking = False
                        self.move_undone = True
                        if self.move_count >= 1:
                            self.move_count -= 1
                            self.white_to_move = not self.white_to_move
                    
                    if self.game_review and e.key == p.K_RIGHT: # pressing right arrow makes the next move in game review
                        #move = engine.Move((6, 3), (4, 3), self.gs.board)
                        if self.move_count < len(self.move_list):
                            start, end, board, en_passant, castle, pawn_promo \
                                = review.review_move(self.move_list[self.move_count], 
                                                     self.gs.board, self.white_to_move)
                            #print('s, e, b:', start, end, self.gs.board, en_passant, castle, pawn_promo)
                            move = engine.Move(start, end, self.gs.board, en_passant, castle, pawn_promo)
                            self.gs.make_move(move)
                            self.white_to_move = not self.white_to_move
                            self.move_count += 1
                        else:
                            self.game_over = True
                            self.final_result = self.result_dict[self.game_variables['result']]
                self.manager.process_events(e)
                        
    
            # AI part
            if not self.game_over and not self.is_human_turn and not self.move_undone:
                if not self.AI_thinking:
                    self.AI_thinking = True
                    print('Thinking...')
                    return_queue = Queue() # pass data between threads
                    move_finder_process = Process(target=chessAI.find_best_move, \
                                                  args=(self.gs, self.valid_moves, return_queue))
                    move_finder_process.start()
                    
                if not move_finder_process.is_alive():
                    print('Done thinking.')
                    AI_move = return_queue.get()
                    if AI_move == None:
                        AI_move = chessAI.find_random_move(self.valid_moves)
                    self.gs.make_move(AI_move)
                    self.move_made = True
                    self.animate = True
                    self.AI_thinking = False
    
            if self.move_made:
                if self.animate:
                    self.animate_move(self.gs.move_log[-1], self.screen, 
                                      self.gs.board, self.clock)
                self.valid_moves = self.gs.get_valid_moves()
                self.move_made = False
                self.animate = False
                self.move_undone = False
                if self.player_one == self.player_two == True:
                    #print(self.evaluation())
                    pass
    
            if not self.game_over:
                self.draw_game_state(self.screen, self.gs, self.valid_moves, 
                                     self.selected_square, self.move_log_font, 
                                     self.game_review)
            else:
                if self.game_review:
                    self.draw_game_state(self.screen, self.gs, self.valid_moves, 
                                         self.selected_square, self.move_log_font, 
                                         self.game_review, self.final_result)
                else:
                    self.draw_game_state(self.screen, self.gs, self.valid_moves, 
                                         self.selected_square, self.move_log_font, 
                                         self.game_review)
    
            if self.gs.checkmate or self.gs.stalemate or self.gs.repetition:
                self.game_over = True
                if self.gs.stalemate:
                    text = 'Stalemate.'
                elif self.gs.repetition:
                    text = 'Remis.'
                else:
                    text = 'Black wins.' if self.gs.white_to_move else 'White wins.'
                self.draw_endgame_text(self.screen, text)
    
            self.clock.tick(self.MAX_FPS)
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            p.display.flip()
            #return False
    
    
    def evaluation(self):
        self.eval = sf_13.eval(self.gs.FENizer())
        return self.eval
        
    
    def load_images(self):
        pieces = ['bp', 'bR', 'bN', 'bB', 'bQ', 'bK', 'wp', 'wR', 'wN', 'wB', 'wQ', 'wK']
        for piece in pieces:
            self.Images[piece] = p.transform.scale(p.image.load('images/chess pieces/' + piece + '.png'), \
                                              (self.SQ_SIZE, self.SQ_SIZE))
    
    
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
        
    
    def draw_game_state(self, screen, gs, valid_moves, selected_square, 
                        move_log_font, game_review, text = None):
        self.draw_board(screen)
        self.highlight(screen, gs, valid_moves, selected_square)
        self.draw_pieces(screen, gs.board)
        self.draw_move_log(screen, gs, move_log_font)
        self.draw_endgame_text(screen, text)
    
    
    def draw_board(self, screen):
        global COLOURS
        COLOURS = [p.Color('white'), p.Color('grey')]
        COLOURS = [(240, 217, 181), (181, 136, 99)]
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                colour = COLOURS[((row + column) % 2)]
                p.draw.rect(screen, colour, p.Rect(column * self.SQ_SIZE,
                                row * self.SQ_SIZE, self.SQ_SIZE, self.SQ_SIZE))
    
    
    # original highlight
    def highlight(self, screen, gs, valid_moves, selected_square):
        if selected_square != ():
            r, c = selected_square
            if gs.board[r][c][0] == ('w' if gs.white_to_move else 'b'):
                s = p.Surface((self.SQ_SIZE, self.SQ_SIZE))
                s.set_alpha(100) # opaqueness (0 -> 255)
                s.fill(p.Color('blue'))
                screen.blit(s, (c * self.SQ_SIZE, r * self.SQ_SIZE))
                s.fill(p.Color('yellow'))
                for move in valid_moves:
                    if move.start_row == r and move.start_col == c:
                        screen.blit(s, (self.SQ_SIZE * move.end_col,
                                             self.SQ_SIZE * move.end_row))
            else:
                s = p.Surface((self.SQ_SIZE, self.SQ_SIZE))
                s.set_alpha(100)
                s.fill(p.Color('red'))
                screen.blit(s, (c * self.SQ_SIZE, r * self.SQ_SIZE))
    
    
    def draw_pieces(self, screen, board):
        for row in range(self.DIMENSION):
            for column in range(self.DIMENSION):
                piece = board[row][column]
                if piece != '--':
                    screen.blit(self.Images[piece], \
                                     p.Rect(column * self.SQ_SIZE, row * self.SQ_SIZE, 
                                            self.SQ_SIZE, self.SQ_SIZE))
    
    
    def draw_move_log(self, screen, gs, font):
        #move_log_rect = p.Rect(BOARD_WIDTH + 5, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
        move_log_rect = p.Rect(0, 
                               self.BOARD_HEIGHT + 5, 
                               self.MOVE_LOG_PANEL_WIDTH + 5, 
                               self.MOVE_LOG_PANEL_HEIGHT)
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
            
    
    def animate_move(self, move, screen, board, clock):
        global COLOURS
        animate_fps = 60
        d_r = move.end_row - move.start_row
        d_c = move.end_col - move.start_col
        frames_per_square = 5
        frame_count = (abs(d_r) + abs(d_c)) * frames_per_square
        for frame in range(frame_count + 1):
            r, c = (move.start_row + d_r * frame / frame_count, 
                    move.start_col + d_c * frame / frame_count)
            self.draw_board(screen)
            self.draw_pieces(screen, board)
            # fetch colour of the ending square and overwriting the piece during animation
            colour = COLOURS[(move.end_row + move.end_col) % 2]
            end_square = p.Rect(move.end_col * self.SQ_SIZE, 
                                move.end_row * self.SQ_SIZE, 
                                self.SQ_SIZE, 
                                self.SQ_SIZE)
            p.draw.rect(screen, colour, end_square)
            # redraw captured piece (in case there is one)
            if move.piece_captured != '--':
                if move.is_en_passant_move:
                    en_passant_row = move.end_row + 1 if move.piece_captured[0] == 'b' else move.end_row -1
                    end_square = p.Rect(move.end_col * self.SQ_SIZE, 
                                        en_passant_row * self.SQ_SIZE, 
                                        self.SQ_SIZE, 
                                        self.SQ_SIZE)
                screen.blit(self.Images[move.piece_captured], end_square)
            # draw moving piece
            if move.piece_moved != '--':
                screen.blit(self.Images[move.piece_moved], 
                                 p.Rect(c * self.SQ_SIZE, 
                                        r * self.SQ_SIZE, 
                                        self.SQ_SIZE, 
                                        self.SQ_SIZE))
            
            clock.tick(animate_fps) # framerate for animation
            self.manager.update(clock.tick(animate_fps))
            self.manager.draw_ui(screen)
            p.display.flip()
    
    
    def draw_endgame_text(self, screen, text):
        font = p.font.SysFont('Helvetica', 32, False, False)
        text_object = font.render(text, 0, p.Color('Grey'))
        text_location = p.Rect(0, 0, self.BOARD_WIDTH, self.BOARD_HEIGHT).\
                    move(self.BOARD_WIDTH/2 - text_object.get_width()/2, \
                    self.BOARD_HEIGHT/2 - text_object.get_height()/2)
                    # last part centers the text
        screen.blit(text_object, text_location)
        text_object = font.render(text, 0, p.Color('Red'))
        screen.blit(text_object, text_location.move(2, 2))
    
    
    
    
    
def main():
    p.init()
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(styleSheet)
    window = MainWindow()
    #window.show()
    window.raise_()
    app.exec_()


styleSheet = '''
QPushButton#m1_button, #m2_button, #m3_button, #m4_button,
            p1_button, p2_button, p3_button, p4_button {
            background-color: grey;
            color: white;
            border-style: outset;
            border-width: 1px;
            border-radius: 2px;
            border-color: black;
            font: 14px;
            padding: 6px;
            min-width: 10px;
            }

QPushButton#m1_button:hover, #m2_button:hover, #m3_button:hover, #m4_button:hover {
    color: black;
    }

QPushButton#m1_button:pressed, #m2_button:pressed, #m3_button:pressed, #m4_button:pressed {
    border-color: white;
    }
'''

    
if __name__ == '__main__':
    main()