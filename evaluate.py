from board import Board
from move import Move
import helpers
import constants

PIECE_VALUES = {
     constants.PAWN: 1,
     constants.BISHOP: 3,
     constants.KNIGHT: 3,
     constants.ROOK: 5,
     constants.QUEEN: 9,
     constants.KING: 0,
     constants.EMPTY: 0,
}

def searchDepth(board: Board, depth: int):
    board.generatePossibleMoves()

    bestMove: Move = None
    bestEvaluation: int = -1000

    for nextBoard in board.possibleBoards:
        boardEval = 0
        if depth == 1:
            boardEval = - staticEvaluate(nextBoard)
        else:
            _, boardEval = searchDepth(nextBoard, depth - 1)
            boardEval *= -1
        print(f"evaluating {nextBoard.lastMove.getAlgebraicNotation()}, eval: {boardEval}")
        if bestMove == None or boardEval > bestEvaluation:
            bestMove = nextBoard.lastMove
            bestEvaluation = boardEval
    
    return (bestMove, bestEvaluation)

def staticEvaluate(board: Board):
    sideModifier = 1 if board.getNextMoveColor() == constants.WHITE else -1
    board.generatePossibleMoves()
    if len(board.possibleBoards) == 0:
        kingSquare = board.kingPositions[board.getNextMoveColor() | constants.KING]
        if board.isSquareAttacked(kingSquare, helpers.invertColor(board.getNextMoveColor())):
            return 1000 * sideModifier
        else:
            return 0
    
    evaluation = 0

    for row in range(8):
        for col in range(8):
            piece = board.getSquare((row,col))
            pieceModifier = 1 if piece.getColor() == constants.WHITE else -1
            evaluation += PIECE_VALUES[piece.getType()] * pieceModifier
    
    return evaluation * sideModifier
    
