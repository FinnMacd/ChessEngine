import constants

# Create a funciton to parse bool character input to the internal in piece representation
def parsePiece(isWhite, piece):
    color = constants.WHITE if isWhite else constants.BLACK
    switcher = {
        'p': constants.PAWN,
        'n': constants.KNIGHT,
        'b': constants.BISHOP,
        'r': constants.ROOK,
        'q': constants.QUEEN,
        'k': constants.KING
    }
    piece_type = switcher.get(piece.lower())
    return piece_type | color

def pieceType(piece):
    return piece & constants.PIECE_MASK

def pieceColor(piece):
    return piece & constants.COLOR_MASK

def inBounds(square):
    return square[0] >= 0 and square[1] >= 0 and square[0] < 8 and square[1] < 8

def invertColor(color):
    return color ^ constants.BLACK

def getStartingPawnRank(color):
    return 1 if color == constants.BLACK else 6

def getBoardFromFEN(fen):
    board = []
    rows = fen.split(' ')[0].split('/')
    for row in rows:
        board_row = []
        for char in row:
            if char.isdigit():
                for i in range(int(char)):
                    board_row.append(0)
            else:
                board_row.append(parsePiece(char.isupper(), char))
                
        board.append(board_row)
    return board
