import constants
from dataclasses import dataclass


@dataclass
class Move():
    originSquare: tuple
    targetSquare: tuple
    moveType: int = constants.REGULAR_MOVE
    promotionPiece: int = constants.EMPTY

    def getEnPassantCaptureSquare(self):
        return (self.originSquare[0], self.targetSquare[1])