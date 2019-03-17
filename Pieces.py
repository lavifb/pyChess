class ChessPiece:
	"""Superclass for individual chess pieces"""
	def __init__(self, r, c, white=True):
		self.white = white

		if r > 7 or r < 0:
			raise ValueError("Piece '{}' cannot be placed on row {}".format(self.piece, r))
		if c > 7 or c < 0:
			raise ValueError("Piece '{}' cannot be placed on col {}".format(self.piece, c))

		self.row = r
		self.col = c

	def __repr__(self):
		if self.white:
			return 'W' + self.piece
		else:
			return 'B' + self.piece

class Pawn(ChessPiece):
	def __init__(self, r, c, white=True):
		self.piece = 'P'
		super().__init__(r, c, white)

	# TODO: Pawn moves
	def moves(self):
		return []

class Knight(ChessPiece):
	def __init__(self, r, c, white=True):
		self.piece = 'N'
		super().__init__(r, c, white)

	def moves(self):
		diffs = [(1,2), (1,-2), (2,1), (2,-1), (-1,2), (-1,-2), (-2,1), (-2,-1)]
		possible_moves = []

		for diff in diffs:
			end_row, end_col = self.row+diff[0], self.col+diff[1]
			if end_row > 7 and end_row < 0:
				continue
			if end_col > 7 and end_col < 0:
				continue
			possible_moves.append((end_row, end_col))

		return possible_moves

class Bishop(ChessPiece):
	def __init__(self, r, c, white=True):
		self.piece = 'B'
		super().__init__(r, c, white)

	# TODO: Bishop moves
	def moves(self):
		return []

class Rook(ChessPiece):
	def __init__(self, r, c, white=True):
		self.piece = 'R'
		super().__init__(r, c, white)

	# TODO: Rook moves
	def moves(self):
		return []

class Queen(ChessPiece):
	def __init__(self, r, c, white=True):
		self.piece = 'Q'
		super().__init__(r, c, white)

	# TODO: Queen moves
	def moves(self):
		return []

class King(ChessPiece):
	def __init__(self, r, c, white=True):
		self.piece = 'K'
		super().__init__(r, c, white)

	def moves(self):
		diffs = [(1,1), (1,0), (1,-1), (0,1), (0,-1), (-1,1), (-1,0), (-1,-1)]
		possible_moves = []

		for diff in diffs:
			end_row, end_col = self.row+diff[0], self.col+diff[1]
			if end_row > 7 and end_row < 0:
				continue
			if end_col > 7 and end_col < 0:
				continue
			possible_moves.append((end_row, end_col))

		return possible_moves