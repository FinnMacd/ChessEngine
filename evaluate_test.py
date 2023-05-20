from board import Board
from evaluate import searchDepth, staticEvaluate
import constants
import helpers
import move

fen = "rnb1r1k1/pp3ppp/5q2/3n4/2pP4/2P2NB1/PP2Q1PP/RN3K1R b - - 4 13"

board = Board(helpers.getBoardFromFEN(fen), constants.WHITE, move.Move(0, (0,0), (0,0)), 0)

print(staticEvaluate(board))

move, evaluation = searchDepth(board, 2)
print(f"best move: {move.getAlgebraicNotation()}, evaluation: {evaluation}")