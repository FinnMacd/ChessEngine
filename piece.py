from dataclasses import dataclass
import constants

@dataclass
class Piece():
    data: int

    def getType(self):
        return self.data & constants.PIECE_MASK

    def getColor(self):
        return self.data & constants.COLOR_MASK
    
    def __hash__(self):
        return hash(self.data)