import pandas as pd
import numpy as np
import re
import berserk
from datetime import datetime


'''
THIS FILE CONTAINS THE FOLLOWING FUNCTIONS:
    1) create_game_df
        CREATE GAME DATAFRAME FROM *.txt-FILE (requires PGN format)
    2) get_game
        FETCHES A GAME TO REVIEW IN GAME
    3) get_lichess_games
        USES LICHESS API TO GET UP TO ALL GAMES PLAYED BY SPECIFIC PLAYER
        STORES INFORMATION IN 'txt_files/api_games.txt'

'''        
def create_game_df(file, search_string = '[Ev', time = 'Blitz', termination = 'Checkmate', result = 'White wins'):
    # open the file
    with open(file, 'r') as f:
        lines = (line.rstrip() for line in f) # get all lines
        lines = list(line for line in lines if \
                     line and \
                     line[0:7] != '[WhiteT' and \
                     line[0:7] != '[BlackT' and \
                     line[0:7] != '[WhiteR' and \
                     line[0:7] != '[BlackR') # no blank lines, titles or rating changes
        short_line = list(line[0:3] for line in lines) # initial 3 characters of each line
    
    # drop unnecessary content
    #for line in lines:
        
    '''
    CREATE GAME CHUNKS
        1) index_list represents the indices of all game starting lines.
        2) gap_list represents the differences between all starting lines.
        3) final_game adds the ultimate game in the list, missing from gap_list
    '''
    index_list = [x for x in range(len(lines)) if short_line[x] == search_string]
    final_game = len(lines) - index_list[-1]
    gap_list = [y - x for x, y in zip(index_list[:-1], index_list[1:])]
    gap_list.insert(-1, final_game)
    game_list = []
    i = 0
    for j in range(len(gap_list)):
        n = gap_list[j]
        game_list.append(lines[i:i+n])
        i = i + n
    print(len(game_list))
    # create dictionary and dataframe
    dict_main = {}
    for count, chunk in enumerate(game_list):
        dict_main[count + 1] = chunk
    df = pd.DataFrame().from_dict(dict_main, orient='index')
# =============================================================================
#     print(df.head(30))
#     drop_stuff = df[0][:]
#     print(drop_stuff)
#     
#     df[df[0] != '[Event \"C']
#     print(df.head(30))
# =============================================================================












# change this!
















    '''
    CHECK FOR MISSINGS
    - for x in range(df.shape[1]):
        print(x, df[x].isnull().sum())
    - print(df.iloc[769]) 
    - print(df.loc[df[15].isnull()][0])
        1) remove non-regular games (> 15 entries, i.e. columns)
        2) reindex dataframe
    '''
    if df.shape[1] > 15:
        df = df.loc[df[15].isnull()]
        df.dropna(axis = 1, inplace = True)
    df = df.reset_index(drop = True)

    # create column names
    column_names = []
    for x in range(0, len(df.columns)):
        column_names.append(df[x][1].lstrip('[').split()[0])
    df.columns = column_names
    df.rename(columns={'TimeControl': 'TC', '1.': 'Moves'}, inplace=True)

    '''
    DATA CLEANING
        1) remove column names from values
        2) remove non-standard variants
        3) reindex dataframe
    '''
    for col in df.columns:
        for x in range(0, len(df)):
            df[col][x] = df[col][x].lstrip('[').rstrip(']').split(' ', 1)[1].strip('"')
    variant_names = df[df['Variant'] != 'Standard'].index
    df.drop(variant_names, inplace = True)
    df = df.reset_index(drop = True)

    '''
    MORE DATA CLEANING
        1) introduce two new columns (time and length)
        2) repair move column
        3) add termination parameters
        4) single out time data
        5) single out event data
        6) fill game length column
    '''
    move_help = '1. '
    df = df.assign(Time = df['Event'])
    df = df.assign(Length = df['Moves'])
    for y in np.arange(0, len(df)):
        df['Moves'][y] = ''.join((move_help, df['Moves'][y]))
        if '#' in df['Moves'][y]:
            df['Termination'][y] = 'Checkmate'
        df['Termination'].loc[df['Result'] == '1/2-1/2'] = 'Draw'
        df['Termination'].loc[df['Termination'] == 'Normal'] = 'Resign'
        df['Termination'].loc[df['Termination'] == 'Time forfeit'] = 'Time'
        df['Time'][y] = df['Time'][y].split(' ', 2)[1]
        df['Event'][y] = df['Event'][y].split(' ', 1)[0]
        df['Length'][y] = max([int(e.strip('.')) for e in re.findall(r'\d+.', df['Moves'][y]) if e[-1] == '.'])
        df['Date'][y] = datetime.strptime(df['Date'][y], '%Y.%m.%d').strftime('%d.%m.%Y')
    
    #print([df[col].unique() for col in df.columns])
    # finally, turn index into game no for easier selection
    df.reset_index(inplace = True)
    df = df.rename(columns = {'index': 'Game'})
    
    # generate csv-file for neural network algorithm
    if file == 'txt_files/games.txt':
        pd.DataFrame.to_csv(df, 'txt_files/games.csv')
    
    result_list_int = ['1-0', '1/2-1/2', '0-1']
    result_list_str = ['White wins', 'Draw', 'Black wins']
    result_dict = dict(zip(result_list_str, result_list_int))
    df2 = df[(df['Termination'] == termination) \
             & (df['Result'] == result_dict[result])]
    df2_cols = ['Game', 'Date', 'White', 'Black', 'Result', 'Time', 'TC', 'Length', 'Termination', 'Moves']
    #df2_cols = ['Game', 'Date', 'White', 'Black', 'Result', 'TC', 'Length', 'Moves']
    df2_table = df2[df2_cols]
    
    return df, df2_table


def get_game(df, game = 1, time = 'Blitz', termination = 'Checkmate', result = '1-0'):
    df = df[df['Game'] == game]
    result = df['Result'][game]
    game_pgn = df['Moves'][game]
    if game_pgn[-3:] == '1-0' or game_pgn[-3:] == '0-1':
        clean_pgn = game_pgn[0:-4]
    else: # remis
        clean_pgn = game_pgn[0:-8]

    pgn_list = clean_pgn.split(' ')
    
    dict_keys = ['termination', 'time', 'result']
    dict_values = [termination, time, result]
    game_variables = dict(zip(dict_keys, dict_values))

    input_dict = {}
    for x in [x.capitalize() for x in dict_keys]:
        input_dict[x.lower()] = df[x].unique()

    move_list = []
    for count, ele in enumerate(pgn_list):
        if count % 3 != 0:
            if ele[-1] == '#':
                ele = ele[:-1]
                move_list.append(ele)
            elif ele[-1] == '+':
                ele = ele[:-1]
                move_list.append(ele)
            else:
                move_list.append(ele)

    return move_list, game, ('Reviewing game no. ' + str(game)), game_variables, input_dict


def get_lichess_games(since, until, perf_type, username, max = 300, color = None):
    start = int(berserk.utils.to_millis(datetime(since[2], since[1], since[0])))
    end = int(berserk.utils.to_millis(datetime(until[2], until[1], until[0])))
    with open('txt_files/api_token.txt', 'r') as f:
        token = f.readline()
    if username == 'Bee-Shop':
        session = berserk.TokenSession(token)
    else:
        session = ''
        max = max // 3
    client = berserk.Client(session = session, pgn_as_default = False)
    games = client.games.export_by_player(as_pgn = True, \
             username = username, since = start, until = end, rated = None, \
             perf_type = perf_type, color = color, analysed = None, \
             max = max, evals = None)
    with open('txt_files/api_games.txt', 'w') as output:
        for x in list(games):
            output.write(x + '\n')
            
             

if __name__ == '__main__':
    #get_lichess_games([19, 10, 2020], [19, 12, 2020], 'bullet', max = 100, username = 'Chess-Network')
    create_game_df('txt_files/test_big.txt', '[Ev')
    