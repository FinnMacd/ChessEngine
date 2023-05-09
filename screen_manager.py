import pygame
import helpers
import board
import constants

# Define the colors for the board squares
LIGHT_SQUARE_COLOR = (255, 206, 158)
DARK_SQUARE_COLOR = (209, 139, 71)

pieces = {}
# Load the chess piece images
def loadImages():
    for color in ['b', 'w']:
        for piece in ['p', 'r', 'n', 'b', 'q', 'k']:
            image_path = f'pieces/{color}{piece}.png'
            raw_image = pygame.image.load(image_path)
            raw_image.set_colorkey((255, 255, 255))
            scaled_image = pygame.transform.smoothscale(raw_image, (constants.SQUARE_SIZE*0.8, constants.SQUARE_SIZE*0.8))
            pieces[helpers.parsePiece(color == 'w', piece)] = scaled_image

class ScreenManager(object):
    def __init__(self):
        # Set up the window
        self.screen = pygame.display.set_mode([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT])

        # Set the caption for the window
        pygame.display.set_caption("Chess Board")

        loadImages()

    # Create a function to render the board
    def renderBoard(self, board):
        for row in range(8):
            for col in range(8):
                squareColor = LIGHT_SQUARE_COLOR if (row + col) % 2 == 0 else DARK_SQUARE_COLOR
                if board.getSelectedPiece() == (row, col):
                    squareColor = (0,0,0)
                if (row, col) in board.getSelectedPieceMoves():
                    squareColor = (255, 255, 255)
                pygame.draw.rect(self.screen, squareColor, (col * constants.SQUARE_SIZE, row * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE))

    # Create a function to render a piece on the board
    def renderPiece(self, piece, row, col):
        if piece & 7 == 0:
            return
        piece_image = pieces[piece]
        x = (col + 0.1) * constants.SQUARE_SIZE
        y = (row + 0.1) * constants.SQUARE_SIZE
        self.screen.blit(piece_image, (x, y))

    # Create a function to render the board based on a 8x8 array of pieces
    def renderPieces(self, board):
        for x, row in enumerate(board.getBoard()):
            for y, piece in enumerate(row):
                self.renderPiece(piece, x, y)

    def render(self, board):
        self.renderBoard(board)
        self.renderPieces(board)