import chess
import chess.engine

def eval(FEN):
    engine = chess.engine.SimpleEngine.popen_uci("stockfish_13/sf_13.exe")
    
# =============================================================================
#     board = chess.Board(FEN)
#     info = engine.analyse(board, chess.engine.Limit(time=0.1))
#     print("Score:", info["score"])
#     # Score: PovScore(Cp(+20), WHITE)
# =============================================================================
    
    board = chess.Board(FEN)
    info = engine.analyse(board, chess.engine.Limit(depth=12))
    #print("Score:", info["score"])
    # Score: PovScore(Mate(+1), WHITE)
    
    engine.quit()
    
    return info['score']
    

if __name__ == '__main__':
    eval("r1bqkbnr/p1pp1ppp/1pn5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 2 4")