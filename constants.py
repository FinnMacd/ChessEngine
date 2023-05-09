# Define piece codes
WHITE, BLACK, COLOR_MASK = 0, 16, 16
EMPTY, PAWN, ROOK, KNIGHT, BISHOP, QUEEN, KING, PIECE_MASK = 0, 1, 2, 3, 4, 5, 6, 7

START_POSITION = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w'

# Set the dimensions of the screen and the size of each square on the board
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
SQUARE_SIZE = SCREEN_WIDTH // 8
