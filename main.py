import pygame
import time

import constants
from board import Board
from screen_manager import ScreenManager
import helpers
from evaluate import searchDepth

# Initialize Pygame
pygame.init()

board = Board(helpers.getBoardFromFEN(constants.START_POSITION), constants.WHITE, 0)
board.generatePossibleMoves()
renderer = ScreenManager()
renderer.render(board)

# Refresh the screen
pygame.display.flip()

def handleClick(row, col):
    global board
    piece = board.board[row][col]
    if board.selectedPiece is None:
        if piece.getType() != constants.EMPTY and piece.getColor() == board.getNextMoveColor():
            board.selectPiece((row, col))

    else:
        selectedPiece = board.selectedPiece
        board.selectPiece(None)
        if board.isValidMove(selectedPiece, (row, col)):
            board = board.getBoardFromMove(selectedPiece, (row, col))
            board.generatePossibleMoves()

            move, evaluation = searchDepth(board, 1)
            print(f"best move: {move.getAlgebraicNotation()}, evaluation: {evaluation}")


# Wait for the user to close the window
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is clicked on a piece
            for row in range(8):
                for col in range(8):
                    pieceRect = pygame.Rect(col * constants.SQUARE_SIZE, row * constants.SQUARE_SIZE, constants.SQUARE_SIZE, constants.SQUARE_SIZE)
                    if pieceRect.collidepoint(event.pos):
                        handleClick(row, col)
            renderer.render(board)
            pygame.display.flip()
    time.sleep(0.02)

# Quit Pygame
pygame.quit()