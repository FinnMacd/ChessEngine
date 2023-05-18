import helpers
import constants
from move import Move

def getMoves(board, pieceSquare, allowIllegalMoves = False):
    moves = {}
    piece = board.getSquare(pieceSquare)
    pieceColor = helpers.pieceColor(piece)
    pieceType = helpers.pieceType(piece)

    if pieceType == constants.EMPTY or (pieceColor != board.getNextMoveColor() and not allowIllegalMoves):
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
    targetSquare = (pieceSquare[0] + yMovement, pieceSquare[1])
    if helpers.inBounds(targetSquare) and not board.containsPiece(-1, targetSquare):
        # check for promotion
        if pieceSquare[0] == helpers.getStartingPawnRank(helpers.invertColor(pieceColor)):
            handlePromotion(moves, board, pieceSquare, targetSquare, allowIllegalMoves)
        else:
            addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves)
            # handle starting jump
            if pieceSquare[0] == helpers.getStartingPawnRank(pieceColor):
                targetSquare = (pieceSquare[0] + yMovement*2, pieceSquare[1])
                if helpers.inBounds(targetSquare) and not board.containsPiece(-1, targetSquare):
                    addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves)

    # handle captures
    targetSquare = (pieceSquare[0] + yMovement, pieceSquare[1]-1)
    if helpers.inBounds(targetSquare) and board.containsPiece(helpers.invertColor(pieceColor), targetSquare):
        if pieceSquare[0] == helpers.getStartingPawnRank(helpers.invertColor(pieceColor)):
            handlePromotion(moves, board, pieceSquare, targetSquare, allowIllegalMoves)
        else:
            addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves)
    targetSquare = (pieceSquare[0] + yMovement, pieceSquare[1]+1)
    if helpers.inBounds(targetSquare) and board.containsPiece(helpers.invertColor(pieceColor), targetSquare):
        if pieceSquare[0] == helpers.getStartingPawnRank(helpers.invertColor(pieceColor)):
            handlePromotion(moves, board, pieceSquare, targetSquare, allowIllegalMoves)
        else:
            addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves)

    # check en passant
    if pieceSquare[0] == helpers.getStartingPawnRank(helpers.invertColor(pieceColor))-2*yMovement:
        if helpers.pieceType(board.getSquare(board.lastMove.targetSquare)) == constants.PAWN and \
            board.lastMove.targetSquare[0] == pieceSquare[0] and abs(board.lastMove.targetSquare[1] - pieceSquare[1]) == 1 and \
            board.lastMove.originSquare[0] == helpers.getStartingPawnRank(helpers.invertColor(pieceColor)):
            targetSquare = (pieceSquare[0] + yMovement, board.lastMove.targetSquare[1])
            addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves, constants.EN_PASSANT)

def handlePromotion(moves, board, pieceSquare, targetSquare, allowIllegalMoves):
    promotionPieces = [constants.KNIGHT, constants.BISHOP, constants.ROOK, constants.QUEEN]
    for promotionPiece in promotionPieces:
        addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves, constants.PROMOTION, promotionPiece)
    
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
            targetSquare = (pieceSquare[0] + i * direction[0], pieceSquare[1] + i * direction[1])
            if not helpers.inBounds(targetSquare):
                break
            if not board.containsPiece(-1, targetSquare):
                addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves)
            elif helpers.pieceColor(board.board[targetSquare[0]][targetSquare[1]]) != pieceColor:
                addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves)
                break
            else:
                break

    # check castling
    if pieceType == constants.KING:
        handleCastling(moves, board, pieceSquare, allowIllegalMoves)

def handleCastling(moves, board, pieceSquare, allowIllegalMoves):
    if allowIllegalMoves:
        return 
    piece = board.getSquare(pieceSquare)
    pieceColor = helpers.pieceColor(piece)

    queenSide, kingSide = board.getCastleOptionsForSide(pieceColor)
    queensRookSquare = (pieceSquare[0], 0)
    kingsRookSquare = (pieceSquare[0], 7)
    if (queenSide or kingSide) and board.isSquareAttacked(pieceSquare, pieceColor):
        return
    if queenSide and board.isLineOpen(queensRookSquare, pieceSquare) and \
            not board.isSquareAttacked((pieceSquare[0], pieceSquare[1] - 1), pieceColor):
        targetSquare = (pieceSquare[0], pieceSquare[1] - 2)
        addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves, constants.QUEEN_SIDE_CASTLE)
    if kingSide and board.isLineOpen(kingsRookSquare, pieceSquare) and \
            not board.isSquareAttacked((pieceSquare[0], pieceSquare[1] + 1), pieceColor):
        targetSquare = (pieceSquare[0], pieceSquare[1] + 2)
        addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves, constants.KING_SIDE_CASTLE)

def addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves, moveType = constants.REGULAR_MOVE, promotionPiece = constants.EMPTY):
    newBoard = board.movePiece(Move(pieceSquare, targetSquare, moveType, promotionPiece))
    if allowIllegalMoves or newBoard.getGameState() == 1:
        moves[targetSquare] = newBoard
