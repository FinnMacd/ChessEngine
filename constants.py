# Define piece codes
WHITE, BLACK, COLOR_MASK = 0, 16, 16
EMPTY, PAWN, ROOK, KNIGHT, BISHOP, QUEEN, KING, PIECE_MASK = 0, 1, 2, 3, 4, 5, 6, 7

START_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w'

# Set the dimensions of the screen and the size of each square on the board
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
SQUARE_SIZE = SCREEN_WIDTH // 8

# move type
REGULAR_MOVE = 0
EN_PASSANT = 1
QUEEN_SIDE_CASTLE = 2
KING_SIDE_CASTLE = 3

# bit representations of whether each castling option is still available
CASTLE_WHITE_KING_SIDE = 1
CASTLE_WHITE_QUEEN_SIDE = 2
CASTLE_BLACK_KING_SIDE = 4
CASTLE_BLACK_QUEEN_SIDE = 8
CASTLE_ALL_OPTIONS = 15
