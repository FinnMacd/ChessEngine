import board
import helpers
import constants

def getMoves(board, pieceSquare, allowIllegalMoves = False):
    moves = {}
    piece = board.getSquare(pieceSquare)
    pieceColor = helpers.pieceColor(piece)
    pieceType = helpers.pieceType(piece)

    if pieceType == constants.EMPTY or pieceColor != board.getNextMoveColor():
        return moves
    
    if pieceType == constants.PAWN:
        handlePawnMovement(moves, board, pieceSquare, allowIllegalMoves)
    else:
        handlePieceMovement(moves, board, pieceSquare, allowIllegalMoves)
    
    return moves

def handlePawnMovement(moves, board, pieceSquare, allowIllegalMoves):
    piece = board.getSquare(pieceSquare)
    pieceColor = helpers.pieceColor(piece)

    yMovement = -1 if pieceColor == constants.WHITE else 1
    # handle forward movement
    move = (pieceSquare[0] + yMovement, pieceSquare[1])
    if helpers.inBounds(move) and not board.containsPiece(-1, move):
        addMove(pieceSquare, move, moves, board, allowIllegalMoves)
        # handle starting jump
        if pieceSquare[0] == helpers.getStartingPawnRank(pieceColor):
            move = (pieceSquare[0] + yMovement*2, pieceSquare[1])
            if helpers.inBounds(move) and not board.containsPiece(-1, move):
                addMove(pieceSquare, move, moves, board, allowIllegalMoves)

    # handle captures
    move = (pieceSquare[0] + yMovement, pieceSquare[1]-1)
    if helpers.inBounds(move) and board.containsPiece(helpers.invertColor(pieceColor), move):
        addMove(pieceSquare, move, moves, board, allowIllegalMoves)
    move = (pieceSquare[0] + yMovement, pieceSquare[1]+1)
    if helpers.inBounds(move) and board.containsPiece(helpers.invertColor(pieceColor), move):
        addMove(pieceSquare, move, moves, board, allowIllegalMoves)

    # check en passant
    if pieceSquare[0] == helpers.getStartingPawnRank(helpers.invertColor(pieceColor))-2*yMovement:
        if helpers.pieceType(board.getSquare(board.lastMove[1])) == constants.PAWN and \
            board.lastMove[1][0] == pieceSquare[0] and abs(board.lastMove[1][1] - pieceSquare[1]) == 1 and \
            board.lastMove[0][0] == helpers.getStartingPawnRank(helpers.invertColor(pieceColor)):
            move = (pieceSquare[0] + yMovement, board.lastMove[1][1])
            addMove(pieceSquare, move, moves, board, allowIllegalMoves, constants.EN_PASSANT)
    
def handlePieceMovement(moves, board, pieceSquare, allowIllegalMoves):
    piece = board.getSquare(pieceSquare)
    pieceColor = helpers.pieceColor(piece)
    pieceType = helpers.pieceType(piece)

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
            if not board.containsPiece(-1, move):
                addMove(pieceSquare, move, moves, board, allowIllegalMoves)
            elif helpers.pieceColor(board.board[move[0]][move[1]]) != pieceColor:
                addMove(pieceSquare, move, moves, board, allowIllegalMoves)
                break
            else:
                break
            
    # check castling
    if pieceType == constants.KING:
        queenSide, kingSide = board.getCastleOptionsForSide(pieceColor)
        queensRookSquare = (pieceSquare[0], 0)
        kingsRookSquare = (pieceSquare[0], 7)
        if queenSide and board.isLineOpen(queensRookSquare, pieceSquare):
            move = (pieceSquare[0], pieceSquare[1] - 2)
            addMove(pieceSquare, move, moves, board, allowIllegalMoves, constants.QUEEN_SIDE_CASTLE)
        if kingSide and board.isLineOpen(kingsRookSquare, pieceSquare):
            move = (pieceSquare[0], pieceSquare[1] + 2)
            addMove(pieceSquare, move, moves, board, allowIllegalMoves, constants.KING_SIDE_CASTLE)
    
def addMove(pieceSquare, targetSquare, moves, board, allowIllegalMoves, moveType = constants.REGULAR_MOVE):
    newBoard = board.movePiece(pieceSquare, targetSquare, moveType)
    if allowIllegalMoves or newBoard.getGameState() == 1:
        moves[targetSquare] = newBoard
