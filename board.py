import helpers
import constants
import copy

class Board:

    # Create a function to parse the FEN position and return an 8x8 board
    def __init__(self, board, nextMoveColor, lastMove):
        self.board = copy.deepcopy(board)
        self.nextMoveColor = nextMoveColor
        self.selectedPiece = None
        self.possibleMoves = {}

    def getGameState(self):
        return 1
    
    def movePiece(self, pieceSquare, targetSquare):
        newBoard = Board(self.board, helpers.invertColor(self.nextMoveColor), 0)
        newBoard.board[targetSquare[0]][targetSquare[1]] = newBoard.board[pieceSquare[0]][pieceSquare[1]]
        newBoard.board[pieceSquare[0]][pieceSquare[1]] = 0
        return newBoard
    
    def generatePossibleMoves(self):
        moves = {}
        for row in range(8):
            for col in range(8):
                if self.getNextMoveColor() == helpers.pieceColor(self.board[row][col]) and helpers.pieceType(self.board[row][col]) != constants.EMPTY:
                    moves.update({(row, col) : self.getMoves((row, col))})
        self.possibleMoves = moves

    def getNextMoveColor(self):
        return self.nextMoveColor
    
    def isValidMove(self, pieceSquare, targetSquare):
        return pieceSquare in self.possibleMoves and targetSquare in self.possibleMoves[pieceSquare]
    
    def getBoard(self):
        return self.board
    
    def getSelectedPiece(self):
        return self.selectedPiece
    
    def getSelectedPieceMoves(self):
        return {} if self.selectedPiece == None else self.possibleMoves[self.selectedPiece]
    
    # Returns a bool for whether the specified square contains a piece of the given color
    # or if color is -1 returns whether the square is empty
    def containsPiece(self, color, square):
        if color != -1:
            return helpers.pieceColor(self.board[square[0]][square[1]]) == color and helpers.pieceType(self.board[square[0]][square[1]]) != constants.EMPTY
        else:
            return helpers.pieceType(self.board[square[0]][square[1]]) == constants.EMPTY
    
    def getMoves(self, pieceSquare):
        moves = {}
        piece = self.board[pieceSquare[0]][pieceSquare[1]]

        if helpers.pieceType(piece) == constants.EMPTY or helpers.pieceColor(piece) != self.getNextMoveColor():
            return moves
        
        if helpers.pieceType(piece) == constants.PAWN:
            yMovement = -1 if helpers.pieceColor(piece) == constants.WHITE else 1
            # handle forward movement
            move = (pieceSquare[0] + yMovement, pieceSquare[1])
            if helpers.inBounds(move) and self.containsPiece(-1, move):
                newBoard = self.movePiece(pieceSquare, move)
                if newBoard.getGameState() == 1:
                    moves[move] = newBoard
                # handle starting jump
                if pieceSquare[0] == helpers.getStartingPawnRank(helpers.pieceColor(piece)):
                    move = (pieceSquare[0] + yMovement*2, pieceSquare[1])
                    if helpers.inBounds(move) and self.containsPiece(-1, move):
                        newBoard = self.movePiece(pieceSquare, move)
                        if newBoard.getGameState() == 1:
                            moves[move] = newBoard
            # handle captures
            move = (pieceSquare[0] + yMovement, pieceSquare[1]-1)
            if helpers.inBounds(move) and self.containsPiece(helpers.invertColor(helpers.pieceColor(piece)), move):
                newBoard = self.movePiece(pieceSquare, move)
                if newBoard.getGameState() == 1:
                    moves[move] = newBoard
            move = (pieceSquare[0] + yMovement, pieceSquare[1]+1)
            if helpers.inBounds(move) and self.containsPiece(helpers.invertColor(helpers.pieceColor(piece)), move):
                newBoard = self.movePiece(pieceSquare, move)
                if newBoard.getGameState() == 1:
                    moves[move] = newBoard
        else:
            directions = []
            if helpers.pieceType(piece) in (constants.ROOK, constants.QUEEN, constants.KING):
                directions += [(0, 1), (0, -1), (1, 0), (-1, 0)]
            if helpers.pieceType(piece) in (constants.BISHOP, constants.QUEEN, constants.KING):
                directions += [(1, 1), (-1, -1), (1, -1), (-1, 1)]
            if helpers.pieceType(piece) == constants.KNIGHT:
                directions = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
            pieceRange = 7
            if helpers.pieceType(piece) in (constants.KING, constants.KNIGHT):
                pieceRange = 1
            for direction in directions:
                for i in range(1, pieceRange+1):
                    move = (pieceSquare[0] + i * direction[0], pieceSquare[1] + i * direction[1])
                    if not helpers.inBounds(move):
                        break
                    if self.containsPiece(-1, move):
                        newBoard = self.movePiece(pieceSquare, move)
                        if newBoard.getGameState() == 1:
                            moves[move] = newBoard
                    elif helpers.pieceColor(self.board[move[0]][move[1]]) != helpers.pieceColor(piece):
                        newBoard = self.movePiece(pieceSquare, move)
                        if newBoard.getGameState() == 1:
                            moves[move] = newBoard
                        break
                    else:
                        break
        
        return moves
