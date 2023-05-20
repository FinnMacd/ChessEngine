import helpers
import constants
from move import Move

def getMoves(board, pieceSquare, allowIllegalMoves = False):
    moves = {}
    piece = board.getSquare(pieceSquare)

    if piece.getType() == constants.EMPTY or (piece.getColor() != board.getNextMoveColor() and not allowIllegalMoves):
        return moves
    
    if piece.getType() == constants.PAWN:
        handlePawnMovement(moves, board, pieceSquare, allowIllegalMoves)
    else:
        handlePieceMovement(moves, board, pieceSquare, allowIllegalMoves)
    
    return moves

def handlePawnMovement(moves, board, pieceSquare, allowIllegalMoves):
    piece = board.getSquare(pieceSquare)

    yMovement = -1 if piece.getColor() == constants.WHITE else 1
    # handle forward movement
    targetSquare = (pieceSquare[0] + yMovement, pieceSquare[1])
    if helpers.inBounds(targetSquare) and board.getSquare(targetSquare).getType() == constants.EMPTY:
        # check for promotion
        if pieceSquare[0] == helpers.getStartingPawnRank(helpers.invertColor(piece.getColor())):
            handlePromotion(moves, board, pieceSquare, targetSquare, allowIllegalMoves)
        else:
            addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves)
            # handle starting jump
            if pieceSquare[0] == helpers.getStartingPawnRank(piece.getColor()):
                targetSquare = (pieceSquare[0] + yMovement*2, pieceSquare[1])
                if helpers.inBounds(targetSquare) and board.getSquare(targetSquare).getType() == constants.EMPTY:
                    addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves)

    # handle captures
    targetSquare = (pieceSquare[0] + yMovement, pieceSquare[1]-1)
    
    if helpers.inBounds(targetSquare):
        targetPiece = board.getSquare(targetSquare)
        if targetPiece.getType() != constants.EMPTY and targetPiece.getColor() != piece.getColor():
            if pieceSquare[0] == helpers.getStartingPawnRank(helpers.invertColor(piece.getColor())):
                handlePromotion(moves, board, pieceSquare, targetSquare, allowIllegalMoves)
            else:
                addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves)
    targetSquare = (pieceSquare[0] + yMovement, pieceSquare[1]+1)
    if helpers.inBounds(targetSquare):
        targetPiece = board.getSquare(targetSquare)
        if targetPiece.getType() != constants.EMPTY and targetPiece.getColor() != piece.getColor():
            if pieceSquare[0] == helpers.getStartingPawnRank(helpers.invertColor(piece.getColor())):
                handlePromotion(moves, board, pieceSquare, targetSquare, allowIllegalMoves)
            else:
                addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves)

    # check en passant
    if pieceSquare[0] == helpers.getStartingPawnRank(helpers.invertColor(piece.getColor()))-2*yMovement:
        if helpers.piece.getType()(board.getSquare(board.lastMove.targetSquare)) == constants.PAWN and \
            board.lastMove.targetSquare[0] == pieceSquare[0] and abs(board.lastMove.targetSquare[1] - pieceSquare[1]) == 1 and \
            board.lastMove.originSquare[0] == helpers.getStartingPawnRank(helpers.invertColor(piece.getColor())):
            targetSquare = (pieceSquare[0] + yMovement, board.lastMove.targetSquare[1])
            addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves, constants.EN_PASSANT)

def handlePromotion(moves, board, pieceSquare, targetSquare, allowIllegalMoves):
    promotionPieces = [constants.KNIGHT, constants.BISHOP, constants.ROOK, constants.QUEEN]
    for promotionPiece in promotionPieces:
        addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves, constants.PROMOTION, promotionPiece)
    
def handlePieceMovement(moves, board, pieceSquare, allowIllegalMoves):
    piece = board.getSquare(pieceSquare)

    directions = []
    if piece.getType() in (constants.ROOK, constants.QUEEN, constants.KING):
        directions += [(0, 1), (0, -1), (1, 0), (-1, 0)]
    if piece.getType() in (constants.BISHOP, constants.QUEEN, constants.KING):
        directions += [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    if piece.getType() == constants.KNIGHT:
        directions = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]

    pieceRange = 7
    if piece.getType() in (constants.KING, constants.KNIGHT):
        pieceRange = 1
    for direction in directions:
        for i in range(1, pieceRange+1):
            targetSquare = (pieceSquare[0] + i * direction[0], pieceSquare[1] + i * direction[1])
            if not helpers.inBounds(targetSquare):
                break
            if board.getSquare(targetSquare).getType() == constants.EMPTY:
                addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves)
            elif board.getSquare(targetSquare).getColor() != piece.getColor():
                addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves)
                break
            else:
                break

    # check castling
    if piece.getType() == constants.KING:
        handleCastling(moves, board, pieceSquare, allowIllegalMoves)

def handleCastling(moves, board, pieceSquare, allowIllegalMoves):
    if allowIllegalMoves:
        return 
    piece = board.getSquare(pieceSquare)

    queenSide, kingSide = board.getCastleOptionsForSide(piece.getColor())
    queensRookSquare = (pieceSquare[0], 0)
    kingsRookSquare = (pieceSquare[0], 7)
    if (queenSide or kingSide) and board.isSquareAttacked(pieceSquare, piece.getColor()):
        return
    if queenSide and board.isLineOpen(queensRookSquare, pieceSquare) and \
            not board.isSquareAttacked((pieceSquare[0], pieceSquare[1] - 1), piece.getColor()):
        targetSquare = (pieceSquare[0], pieceSquare[1] - 2)
        addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves, constants.QUEEN_SIDE_CASTLE)
    if kingSide and board.isLineOpen(kingsRookSquare, pieceSquare) and \
            not board.isSquareAttacked((pieceSquare[0], pieceSquare[1] + 1), piece.getColor()):
        targetSquare = (pieceSquare[0], pieceSquare[1] + 2)
        addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves, constants.KING_SIDE_CASTLE)

def addMove(moves, board, pieceSquare, targetSquare, allowIllegalMoves, moveType = constants.REGULAR_MOVE, promotionPiece = constants.EMPTY):
    piece = board.getSquare(pieceSquare)
    newBoard = board.movePiece(Move(piece, pieceSquare, targetSquare, moveType, promotionPiece))
    if allowIllegalMoves or newBoard.getGameState() != constants.INVALID_STATE:
        moves[targetSquare] = newBoard

def doesPieceAttackSquare(board, pieceSquare, piece, targetSquare, attackingColor):
    row, col = pieceSquare

    if piece.getType() == constants.PAWN:
        attackingDirection = -1 if attackingColor == constants.WHITE else 1
        attackingSquares = {(row + attackingDirection, col + 1), (row + attackingDirection, col - 1)}
        return targetSquare in attackingSquares
    
    if piece.getType() == constants.KNIGHT:
        attackingSquares = {(row + 2, col + 1), (row + 2, col - 1), 
                            (row - 2, col + 1), (row - 2, col - 1), 
                            (row + 1, col + 2), (row + 1, col - 2), 
                            (row - 1, col + 2), (row - 1, col - 2)}
        return targetSquare in attackingSquares
    
    if piece.getType() == constants.KING:
        return int(abs(row - targetSquare[0])) <= 1 and int(abs(col - targetSquare[1])) <= 1
    
    if piece.getType() == constants.ROOK or piece.getType() == constants.QUEEN:
        if row == targetSquare[0] and board.isLineOpen((row, col), targetSquare):
            return True
        if col == targetSquare[1] and board.isLineOpen((row, col), targetSquare):
            return True
    
    if piece.getType() == constants.BISHOP or piece.getType() == constants.QUEEN:
        rDiff = int(abs(row - targetSquare[0]))
        cDiff = int(abs(col - targetSquare[1]))
        if rDiff == cDiff and board.isLineOpen((row, col), targetSquare):
            return True
    
    return False
