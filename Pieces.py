def onBoard(row, col):
	if row > 7 or row < 0:
		return False
	if col > 7 or col < 0:
		return False

	return True


class ChessPiece:
	"""Superclass for individual chess pieces"""
	def __init__(self, row, col, white=True):
		self.white = white

		if not onBoard(row, col):
			raise ValueError("Piece {} cannot be placed on {}".format(self.piece, (row, col)))
		self.row = row
		self.col = col

		self.has_moved = False

	def __repr__(self):
		if self.white:
			return 'W' + self.piece
		else:
			return 'B' + self.piece

class Pawn(ChessPiece):
	def __init__(self, row, col, white=True):
		self.piece = 'P'
		super().__init__(row, col, white)

	def moves(self):
		possible_moves = []
		if self.white:
			possible_moves.append((self.row+1, self.col))
			if self.row == 1:
				possible_moves.append((self.row+2, self.col))
		else:
			possible_moves.append((self.row-1, self.col))
			if self.row == 6:
				possible_moves.append((self.row-2, self.col))
		
		return possible_moves

class Knight(ChessPiece):
	def __init__(self, row, col, white=True):
		self.piece = 'N'
		super().__init__(row, col, white)

	def moves(self):
		diffs = [(1,2), (1,-2), (2,1), (2,-1), (-1,2), (-1,-2), (-2,1), (-2,-1)]
		possible_moves = []

		for diff in diffs:
			end_row, end_col = self.row+diff[0], self.col+diff[1]
			if not onBoard(end_row, end_col):
				continue
			possible_moves.append((end_row, end_col))

		return possible_moves

class Bishop(ChessPiece):
	def __init__(self, row, col, white=True):
		self.piece = 'B'
		super().__init__(row, col, white)

	# TODO: Bishop moves
	def moves(self):
		return []

class Rook(ChessPiece):
	def __init__(self, row, col, white=True):
		self.piece = 'R'
		super().__init__(row, col, white)

	# TODO: Rook moves
	def moves(self):
		return []

class Queen(ChessPiece):
	def __init__(self, row, col, white=True):
		self.piece = 'Q'
		super().__init__(row, col, white)

	# TODO: Queen moves
	def moves(self):
		return []

class King(ChessPiece):
	def __init__(self, row, col, white=True):
		self.piece = 'K'
		super().__init__(row, col, white)

	def moves(self):
		diffs = [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]
		possible_moves = []

		for diff in diffs:
			end_row, end_col = self.row+diff[0], self.col+diff[1]
			if not onBoard(end_row, end_col):
				continue
			possible_moves.append((end_row, end_col))

		return possible_moves