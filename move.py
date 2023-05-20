import constants
from dataclasses import dataclass

piece_symbols = {
    constants.EMPTY: '',
    constants.PAWN: '',
    constants.ROOK: 'R',
    constants.KNIGHT: 'N',
    constants.BISHOP: 'B',
    constants.QUEEN: 'Q',
    constants.KING: 'K'
}

file_map = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}
rank_map = {0: '8', 1: '7', 2: '6', 3: '5', 4: '4', 5: '3', 6: '2', 7: '1'}

@dataclass
class Move():
    movePiece: int
    originSquare: tuple
    targetSquare: tuple
    isCapture: bool = False
    moveType: int = constants.REGULAR_MOVE
    promotionPiece: int = constants.EMPTY

    def getEnPassantCaptureSquare(self):
        return (self.originSquare[0], self.targetSquare[1])
    
    def getAlgebraicNotation(move):
        if move.moveType == constants.QUEEN_SIDE_CASTLE:
            return "O-O-O"
        elif move.moveType == constants.KING_SIDE_CASTLE:
            return "O-O"

        origin_piece = piece_symbols[move.movePiece.getType()]
        target_file = file_map[move.targetSquare[1]]
        target_rank = rank_map[move.targetSquare[0]]

        algebraic_notation = origin_piece
        if move.isCapture:
            algebraic_notation += 'x'
        algebraic_notation += target_file + target_rank

        if move.moveType == constants.PROMOTION:
            promotion_piece = piece_symbols[move.promotionPiece]
            algebraic_notation += promotion_piece

        return algebraic_notation