from consts import EMPTY_SQUARE

def onBoard(row, col):
	"""Checks if row, col are valid coords on the chess board"""
	if row > 7 or row < 0:
		return False
	if col > 7 or col < 0:
		return False

	return True

def possiblePawnStarts(end_coords, color, board):
	# TODO: en passant
	if color == 'W':
		# Cant move pawns to 1st or 2nd rank
		if end_coords[0] == 0 or end_coords[0] == 1:
			return []

		# Pawn is capturing
		if board[end_coords[0]][end_coords[1]] != EMPTY_SQUARE:
			possible_start_coords = []
			start_row, start_col = end_coords[0]-1, end_coords[1]-1
			if onBoard(start_row,start_col) and board[start_row][start_col] == 'WP':
				possible_start_coords.append((start_row, start_col))
			start_row, start_col = end_coords[0]-1, end_coords[1]+1
			if onBoard(start_row,start_col) and board[start_row][start_col] == 'WP':
				possible_start_coords.append((start_row, start_col))

			return possible_start_coords

		# Pawn is not capturing
		else:
			start_row, start_col = end_coords[0]-1, end_coords[1]
			if board[start_row][start_col] == 'WP':
				return [(start_row, start_col)]
			# Pawns can move 2 from the 2nd rank only if they are not blocked
			elif end_coords[0] == 3 and board[start_row][start_col] == EMPTY_SQUARE:
				start_row, start_col = 1, end_coords[1]
				if board[start_row][start_col] == 'WP':
					return [(start_row, start_col)]

	elif color == 'B':
		# Cant move pawns to 7th or 8th rank
		if end_coords[0] == 7 or end_coords[0] == 6:
			return []

		# Pawn is capturing
		if board[end_coords[0]][end_coords[1]] != EMPTY_SQUARE:
			possible_start_coords = []
			start_row, start_col = end_coords[0]+1, end_coords[1]-1
			if onBoard(start_row,start_col) and board[start_row][start_col] == 'BP':
				possible_start_coords.append((start_row, start_col))
			start_row, start_col = end_coords[0]+1, end_coords[1]+1
			if onBoard(start_row,start_col) and board[start_row][start_col] == 'BP':
				possible_start_coords.append((start_row, start_col))

			return possible_start_coords

		# Pawn is not capturing
		else:
			start_row, start_col = end_coords[0]+1, end_coords[1]
			if board[start_row][start_col] == 'BP':
				return [(start_row, start_col)]
			# Pawns can move 2 from the 7th rank only if they are not blocked
			elif end_coords[0] == 4 and board[start_row][start_col] == EMPTY_SQUARE:
				start_row, start_col = 6, end_coords[1]
				if board[start_row][start_col] == 'BP':
					return [(start_row, start_col)]

	return []

def definedDistancePiece(diffs, end_coords, piece, board):
	"""Logic for defined distance pieces: Kinght, King
	
	Params:
	diffs -- list of 2-tuples giving possible moves in coord difference form
	end_coords -- final coords of move
	piece -- 2 char string giving color and piece type
	board -- board on which to make move

	Retruns: list of possible starting positions for this move
	"""
	possible_start_coords = []
	for diff in diffs:
		start_row, start_col = end_coords[0]+diff[0], end_coords[1]+diff[1]
		if not onBoard(start_row, start_col):
			continue

		if board[start_row][start_col] == piece:
			possible_start_coords.append((start_row, start_col))

	return possible_start_coords

def possibleKinghtStarts(end_coords, color, board):
	diffs = [(1,2), (1,-2), (2,1), (2,-1), (-1,2), (-1,-2), (-2,1), (-2,-1)]
	return definedDistancePiece(diffs, end_coords, color+'N', board)

def possibleKingStarts(end_coords, color, board):
	diffs = [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]
	return definedDistancePiece(diffs, end_coords, color+'K', board)

def longDistancePiece(dirs, end_coords, piece, board):
	"""Logic for long distance pieces: Queen, Rook, Bishop.
	This works by moving in a dir one square at atime until you hit a piece or the end of the board.
	
	Params:
	dirs -- list of 2-tuples giving possible move directions in coord difference form
	end_coords -- final coords of move
	piece -- 2 char string giving color and piece type
	board -- board on which to make move

	Retruns: list of possible starting positions for this move
	"""
	possible_start_coords = []

	for diff in dirs:
		start_row, start_col = end_coords[0]+diff[0], end_coords[1]+diff[1]
		while onBoard(start_row, start_col) and board[start_row][start_col] == EMPTY_SQUARE:
			start_row, start_col = start_row+diff[0], start_col+diff[1]
		if onBoard(start_row, start_col) and board[start_row][start_col] == piece:
			possible_start_coords.append((start_row, start_col))

	return possible_start_coords

def possibleBishopStarts(end_coords, color, board):
	dirs = [(1,1), (1,-1), (-1,1), (-1,-1)]
	return longDistancePiece(dirs, end_coords, color+'B', board)

def possibleRookStarts(end_coords, color, board):
	dirs = [(1,0), (0,1), (-1,0), (0,-1)]
	return longDistancePiece(dirs, end_coords, color+'R', board)

def possibleQueenStarts(end_coords, color, board):
	dirs = [(1,1), (1,-1), (-1,1), (-1,-1), (1,0), (0,1), (-1,0), (0,-1)]
	return longDistancePiece(dirs, end_coords, color+'Q', board)

def possiblePieceStarts(piece, end_coords, color, board):
	"""Gets the possible starting positions of pieces that can move to end_coords.

	Params:
	piece -- Piece making move from ['','N','B','R','Q','K']
	end_coords -- coords in board of the end of the desired move
	color -- color of moving piece from ['W','B']
	board -- current board position

	Returns: list of possible starting coords
	"""

	if piece == 'P':
		return possiblePawnStarts(end_coords, color, board)
	elif piece == 'N':
		return possibleKinghtStarts(end_coords, color, board)
	elif piece == 'B':
		return possibleBishopStarts(end_coords, color, board)
	elif piece == 'R':
		return possibleRookStarts(end_coords, color, board)
	elif piece == 'Q':
		return possibleQueenStarts(end_coords, color, board)
	elif piece == 'K':
		return possibleKingStarts(end_coords, color, board)
	else:
		raise ValueError("Invalid piece '{}' given".format(piece))