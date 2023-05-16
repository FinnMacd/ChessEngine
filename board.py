import helpers
import constants
import copy

# special moves
EN_PASSANT = 1
QUEEN_SIDE_CASTLE = 2
KING_SIDE_CASTLE = 3

# bit representations of whether each castling option is still available
CASTLE_WHITE_KING_SIDE = 1
CASTLE_WHITE_QUEEN_SIDE = 2
CASTLE_BLACK_KING_SIDE = 4
CASTLE_BLACK_QUEEN_SIDE = 8
CASTLE_ALL_OPTIONS = 15

class Board:

    def __init__(self, board, nextMoveColor, lastMove, castleOptions = CASTLE_ALL_OPTIONS, kingPositions = None):
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
                    moves = self.getMoves((row, col), True)
                    if targetSquare in moves:
                        # King is in check
                        return True
        
        # King is not in check
        return False

    def movePiece(self, pieceSquare, targetSquare, specialMove = 0):
        newBoard = Board(self.board, helpers.invertColor(self.nextMoveColor), (pieceSquare, targetSquare), self.castleOptions, self.kingPositions)
        piece = newBoard.board[pieceSquare[0]][pieceSquare[1]]
        newBoard.board[targetSquare[0]][targetSquare[1]] = newBoard.board[pieceSquare[0]][pieceSquare[1]]
        newBoard.board[pieceSquare[0]][pieceSquare[1]] = 0

        if specialMove == EN_PASSANT:
            newBoard.board[pieceSquare[0]][targetSquare[1]] = 0
        elif specialMove == QUEEN_SIDE_CASTLE:
            rookHome = (pieceSquare[0], 0)
            rookTarget = (pieceSquare[0], 3)
            newBoard.board[rookTarget[0]][rookTarget[1]] = newBoard.board[rookHome[0]][rookHome[1]]
            newBoard.board[rookHome[0]][rookHome[1]] = 0
        elif specialMove == KING_SIDE_CASTLE:
            rookHome = (pieceSquare[0], 7)
            rookTarget = (pieceSquare[0], 5)
            newBoard.board[rookTarget[0]][rookTarget[1]] = newBoard.board[rookHome[0]][rookHome[1]]
            newBoard.board[rookHome[0]][rookHome[1]] = 0
        if helpers.pieceType(piece) == constants.KING:
            newBoard.kingPositions[piece] = targetSquare

        # assess castling impact
        if pieceSquare == (0,0) or piece == constants.BLACK | constants.KING:
            newBoard.castleOptions &= (CASTLE_ALL_OPTIONS ^ CASTLE_BLACK_QUEEN_SIDE)
        if pieceSquare == (0,7) or piece == constants.BLACK | constants.KING:
            newBoard.castleOptions &= (CASTLE_ALL_OPTIONS ^ CASTLE_BLACK_KING_SIDE)
        if pieceSquare == (7,0) or piece == constants.WHITE | constants.KING:
            newBoard.castleOptions &= (CASTLE_ALL_OPTIONS ^ CASTLE_WHITE_QUEEN_SIDE)
        if pieceSquare == (7,7) or piece == constants.WHITE | constants.KING:
            newBoard.castleOptions &= (CASTLE_ALL_OPTIONS ^ CASTLE_WHITE_KING_SIDE)
        
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
    
    def getMove(self, pieceSquare, targetSquare):
        return self.possibleMoves[pieceSquare][targetSquare]
    
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
    
    def getMoves(self, pieceSquare, allowIllegalMoves = False):
        moves = {}
        piece = self.board[pieceSquare[0]][pieceSquare[1]]
        pieceColor = helpers.pieceColor(piece)
        pieceType = helpers.pieceType(piece)

        if pieceType == constants.EMPTY or pieceColor != self.getNextMoveColor():
            return moves
        
        if pieceType == constants.PAWN:
            yMovement = -1 if pieceColor == constants.WHITE else 1
            # handle forward movement
            move = (pieceSquare[0] + yMovement, pieceSquare[1])
            if helpers.inBounds(move) and self.containsPiece(-1, move):
                newBoard = self.movePiece(pieceSquare, move)
                if allowIllegalMoves or newBoard.getGameState() == 1:
                    moves[move] = newBoard
                # handle starting jump
                if pieceSquare[0] == helpers.getStartingPawnRank(pieceColor):
                    move = (pieceSquare[0] + yMovement*2, pieceSquare[1])
                    if helpers.inBounds(move) and self.containsPiece(-1, move):
                        newBoard = self.movePiece(pieceSquare, move)
                        if allowIllegalMoves or newBoard.getGameState() == 1:
                            moves[move] = newBoard
            # handle captures
            move = (pieceSquare[0] + yMovement, pieceSquare[1]-1)
            if helpers.inBounds(move) and self.containsPiece(helpers.invertColor(pieceColor), move):
                newBoard = self.movePiece(pieceSquare, move)
                if allowIllegalMoves or newBoard.getGameState() == 1:
                    moves[move] = newBoard
            move = (pieceSquare[0] + yMovement, pieceSquare[1]+1)
            if helpers.inBounds(move) and self.containsPiece(helpers.invertColor(pieceColor), move):
                newBoard = self.movePiece(pieceSquare, move)
                if allowIllegalMoves or newBoard.getGameState() == 1:
                    moves[move] = newBoard
            # check en passant
            if pieceSquare[0] == helpers.getStartingPawnRank(helpers.invertColor(pieceColor))-2*yMovement:
                if helpers.pieceType(self.getSquare(self.lastMove[1])) == constants.PAWN and \
                    self.lastMove[1][0] == pieceSquare[0] and abs(self.lastMove[1][1] - pieceSquare[1]) == 1 and \
                    self.lastMove[0][0] == helpers.getStartingPawnRank(helpers.invertColor(pieceColor)):
                    move = (pieceSquare[0] + yMovement, self.lastMove[1][1])
                    newBoard = self.movePiece(pieceSquare, move, EN_PASSANT)
                    if allowIllegalMoves or newBoard.getGameState() == 1:
                        moves[move] = newBoard

        else:
            directions = []
            if pieceType in (constants.ROOK, constants.QUEEN, constants.KING):
                directions += [(0, 1), (0, -1), (1, 0), (-1, 0)]
            if pieceType in (constants.BISHOP, constants.QUEEN, constants.KING):
                directions += [(1, 1), (-1, -1), (1, -1), (-1, 1)]
            if pieceType == constants.KNIGHT:
                directions = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
            pieceRange = 7
            if pieceType in (constants.KING, constants.KNIGHT):
                pieceRange = 1
            for direction in directions:
                for i in range(1, pieceRange+1):
                    move = (pieceSquare[0] + i * direction[0], pieceSquare[1] + i * direction[1])
                    if not helpers.inBounds(move):
                        break
                    if self.containsPiece(-1, move):
                        newBoard = self.movePiece(pieceSquare, move)
                        if allowIllegalMoves or newBoard.getGameState() == 1:
                            moves[move] = newBoard
                    elif helpers.pieceColor(self.board[move[0]][move[1]]) != pieceColor:
                        newBoard = self.movePiece(pieceSquare, move)
                        if allowIllegalMoves or newBoard.getGameState() == 1:
                            moves[move] = newBoard
                        break
                    else:
                        break
            # check castling
            if pieceType ==  constants.KING:
                queenSide, kingSide = self.getCastleOptionsForSide(pieceColor)
                queensRookSquare = (pieceSquare[0], 0)
                kingsRookSquare = (pieceSquare[0], 7)
                if queenSide and self.isLineOpen(queensRookSquare, pieceSquare):
                    move = (pieceSquare[0], pieceSquare[1] - 2)
                    newBoard = self.movePiece(pieceSquare, move, QUEEN_SIDE_CASTLE)
                    if allowIllegalMoves or newBoard.getGameState() == 1:
                        moves[move] = newBoard
                if kingSide and self.isLineOpen(kingsRookSquare, pieceSquare):
                    move = (pieceSquare[0], pieceSquare[1] - 2)
                    newBoard = self.movePiece(pieceSquare, move, KING_SIDE_CASTLE)
                    if allowIllegalMoves or newBoard.getGameState() == 1:
                        moves[move] = newBoard

        
        return moves
    
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

        direction = tuple(direction)
        currentSquare = ((firstSquare[0] + direction[0]), (firstSquare[1] + direction[1]))
        while currentSquare != secondSquare:
            if self.containsPiece(-1, currentSquare):
                return False
            currentSquare = ((currentSquare[0] + direction[0]), (currentSquare[1] + direction[1]))

        return True
    
    def getCastleOptionsForSide(self, color):
        queenSideBit = CASTLE_WHITE_QUEEN_SIDE
        kingSideBit = CASTLE_WHITE_KING_SIDE
        if color == constants.BLACK:
            queenSideBit = CASTLE_BLACK_QUEEN_SIDE
            kingSideBit = CASTLE_BLACK_KING_SIDE
        canCastleQueenSide = (self.castleOptions & queenSideBit) == queenSideBit
        canCastleKingSide = (self.castleOptions & kingSideBit) == kingSideBit
        return (canCastleQueenSide, canCastleKingSide)

