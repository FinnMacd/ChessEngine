import helpers
import constants
import copy
from movement import getMoves

class Board:

    def __init__(self, board, nextMoveColor, lastMove, castleOptions = constants.CASTLE_ALL_OPTIONS, kingPositions = None):
        self.board = copy.deepcopy(board)
        self.nextMoveColor = nextMoveColor
        self.selectedPiece = None
        self.possibleMoves = {}
        self.lastMove = lastMove
        self.castleOptions = castleOptions
        if kingPositions != None:
            self.kingPositions = copy.deepcopy(kingPositions)
        else:
            self.kingPositions = {}
            for row in range(8):
                for col in range(8):
                    piece = self.board[row][col]
                    if helpers.pieceType(piece) == constants.KING:
                        self.kingPositions[piece] = (row, col)

    def getGameState(self):
        kingColor = helpers.invertColor(self.getNextMoveColor())
        if self.isSquareAttacked(self.kingPositions[constants.KING | kingColor], kingColor):
            return -1
        return 1
    
    def isSquareAttacked(self, targetSquare, color):
        # Iterate through all opponent's pieces
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if helpers.pieceType(piece) != constants.EMPTY and helpers.pieceColor(piece) == helpers.invertColor(color):
                    moves = getMoves(self, (row, col), True)
                    if targetSquare in moves:
                        # King is in check
                        return True
        
        # King is not in check
        return False

    def movePiece(self, pieceSquare, targetSquare, moveType):
        newBoard = Board(self.board, helpers.invertColor(self.nextMoveColor), (pieceSquare, targetSquare), self.castleOptions, self.kingPositions)
        piece = newBoard.board[pieceSquare[0]][pieceSquare[1]]
        newBoard.board[targetSquare[0]][targetSquare[1]] = newBoard.board[pieceSquare[0]][pieceSquare[1]]
        newBoard.board[pieceSquare[0]][pieceSquare[1]] = 0

        if moveType == constants.EN_PASSANT:
            newBoard.board[pieceSquare[0]][targetSquare[1]] = 0
        elif moveType == constants.QUEEN_SIDE_CASTLE:
            rookHome = (pieceSquare[0], 0)
            rookTarget = (pieceSquare[0], 3)
            newBoard.board[rookTarget[0]][rookTarget[1]] = newBoard.board[rookHome[0]][rookHome[1]]
            newBoard.board[rookHome[0]][rookHome[1]] = 0
        elif moveType == constants.KING_SIDE_CASTLE:
            rookHome = (pieceSquare[0], 7)
            rookTarget = (pieceSquare[0], 5)
            newBoard.board[rookTarget[0]][rookTarget[1]] = newBoard.board[rookHome[0]][rookHome[1]]
            newBoard.board[rookHome[0]][rookHome[1]] = 0
        if helpers.pieceType(piece) == constants.KING:
            newBoard.kingPositions[piece] = targetSquare

        # assess castling impact
        if pieceSquare == (0,0) or piece == constants.BLACK | constants.KING:
            newBoard.castleOptions &= (constants.CASTLE_ALL_OPTIONS ^ constants.CASTLE_BLACK_QUEEN_SIDE)
        if pieceSquare == (0,7) or piece == constants.BLACK | constants.KING:
            newBoard.castleOptions &= (constants.CASTLE_ALL_OPTIONS ^ constants.CASTLE_BLACK_KING_SIDE)
        if pieceSquare == (7,0) or piece == constants.WHITE | constants.KING:
            newBoard.castleOptions &= (constants.CASTLE_ALL_OPTIONS ^ constants.CASTLE_WHITE_QUEEN_SIDE)
        if pieceSquare == (7,7) or piece == constants.WHITE | constants.KING:
            newBoard.castleOptions &= (constants.CASTLE_ALL_OPTIONS ^ constants.CASTLE_WHITE_KING_SIDE)
        
        return newBoard
    
    def generatePossibleMoves(self):
        moves = {None:[]}
        for row in range(8):
            for col in range(8):
                if self.getNextMoveColor() == helpers.pieceColor(self.board[row][col]) and helpers.pieceType(self.board[row][col]) != constants.EMPTY:
                    moves.update({(row, col) : getMoves(self, (row, col))})
        self.possibleMoves = moves

    def getNextMoveColor(self):
        return self.nextMoveColor
    
    def isValidMove(self, pieceSquare, targetSquare):
        return pieceSquare in self.possibleMoves and targetSquare in self.possibleMoves[pieceSquare]
    
    def getBoardFromMove(self, pieceSquare, targetSquare):
        return self.possibleMoves[pieceSquare][targetSquare]
    
    def selectPiece(self, pieceSquare):
        self.selectedPiece = pieceSquare
        self.selectedPieceMoves = self.possibleMoves[pieceSquare]
    
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
            return helpers.pieceType(self.board[square[0]][square[1]]) != constants.EMPTY
    
    def getSquare(self, targetSquare):
        return self.board[targetSquare[0]][targetSquare[1]]
    
    def isLineOpen(self, firstSquare, secondSquare):
        if firstSquare == secondSquare:
            return True
        ydiff =  secondSquare[0] - firstSquare[0]
        xdiff =  secondSquare[1] - firstSquare[1]
        if ydiff != 0 and xdiff != 0 and abs(ydiff) != abs(xdiff):
            return False
        direction = [0, 0]
        if ydiff != 0:
            direction[0] = int(ydiff/abs(ydiff))
        if xdiff != 0:
            direction[1] = int(xdiff/abs(xdiff))

        currentSquare = ((firstSquare[0] + direction[0]), (firstSquare[1] + direction[1]))
        while currentSquare != secondSquare:
            if self.containsPiece(-1, currentSquare):
                return False
            currentSquare = ((currentSquare[0] + direction[0]), (currentSquare[1] + direction[1]))

        return True
    
    def getCastleOptionsForSide(self, color):
        queenSideBit = constants.CASTLE_WHITE_QUEEN_SIDE
        kingSideBit = constants.CASTLE_WHITE_KING_SIDE
        if color == constants.BLACK:
            queenSideBit = constants.CASTLE_BLACK_QUEEN_SIDE
            kingSideBit = constants.CASTLE_BLACK_KING_SIDE
        canCastleQueenSide = (self.castleOptions & queenSideBit) == queenSideBit
        canCastleKingSide = (self.castleOptions & kingSideBit) == kingSideBit
        return (canCastleQueenSide, canCastleKingSide)

