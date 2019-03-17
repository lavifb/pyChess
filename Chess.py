from Pieces import *

BOARD_WIDTH  = 8
BOARD_HEIGHT = 8

chess_glyphs = {
	'WK': '♔ ', 'WQ': '♕ ', 'WR': '♖ ', 'WB': '♗ ', 'WN': '♘ ', 'WP': '♙ ',
	'BK': '♚ ', 'BQ': '♛ ', 'BR': '♜ ', 'BB': '♝ ', 'BN': '♞ ', 'BP': '♟ ',
	'  ': '  '
}

class Chess:
	def __init__(self, glyhs=True):
		"""Initialize Chess Game

		Params:
		glyphs -- Use Unicode chess chars (default True)
		"""
		self.width  = BOARD_WIDTH
		self.height = BOARD_HEIGHT
		self.glyhs = glyhs
		self.pieces = ()
		self.turn = 0 # White goes first

	def setupBoard(self):
		"""Setup Chess Board to start game"""

		# White Pieces
		white = [Rook(0,0,True), Knight(0,1,True), Bishop(0,2,True), Queen(0,3,True),
				 King(0,4,True), Bishop(0,5,True), Knight(0,6,True), Rook(0,7,True),
				 Pawn(1,0,True), Pawn(1,1,True), Pawn(1,2,True), Pawn(1,3,True),
				 Pawn(1,4,True), Pawn(1,5,True), Pawn(1,6,True), Pawn(1,7,True)]

		# Black Pieces
		black = [Rook(7,0,False), Knight(7,1,False), Bishop(7,2,False), Queen(7,3,False),
				 King(7,4,False), Bishop(7,5,False), Knight(7,6,False), Rook(7,7,False),
				 Pawn(6,0,False), Pawn(6,1,False), Pawn(6,2,False), Pawn(6,3,False),
				 Pawn(6,4,False), Pawn(6,5,False), Pawn(6,6,False), Pawn(6,7,False)]

		self.pieces = (white, black)

	def movePiece(self, piece, end_pos, start_pos=None):
		if start_pos == None:
			possible_pieces_to_move = []

			for p in self.pieces[self.turn]:
				if (p.row, p.col) == end_pos:
					raise ValueError("Cannot capture your own piece on {}".format(end_pos))
				if p.piece == piece:
					if end_pos in p.moves():
						possible_pieces_to_move.append(p)

			if len(possible_pieces_to_move) > 1:
				raise ValueError("Multiple pieces '{}' found that can make move to {}".format(piece, end_pos))
			elif len(possible_pieces_to_move) < 1:
				raise ValueError("No piece '{}' found that can make move to {}".format(piece, end_pos))

			possible_pieces_to_move[0].row, possible_pieces_to_move[0].col = end_pos

		else:
			piece_to_move = None
			for p in self.pieces[self.turn]:
				if (p.row, p.col) == end_pos:
					raise ValueError("Cannot capture your own piece on {}".format(end_pos))
				if (p.row, p.col) == start_pos:
					piece_to_move = p

			print(piece_to_move)
			if piece_to_move == None or piece_to_move.piece != piece:
				raise ValueError("No piece '{}' found at position {}".format(piece, end_pos))

			if end_pos in piece_to_move.moves():
				piece_to_move.row, piece_to_move.col = end_pos
			else:
				raise ValueError("{} at {} cannot move to {}".format(piece, start_pos, end_pos))

		# TODO: Check for capture
		# TODO: Pawns

	def printBoard(self):
		"""Print board state to stdout"""
		board = [['  ']*self.width for i in range(self.height)]

		# White pieces
		for piece in self.pieces[0]:
			board[piece.row][piece.col] = repr(piece)
		# Black pieces
		for piece in self.pieces[1]:
			board[piece.row][piece.col] = repr(piece)

		sep_line = '   ╟──┼──┼──┼──┼──┼──┼──┼──╢'
		print('   ╔══╤══╤══╤══╤══╤══╤══╤══╗')
		for i, row in enumerate(board[::-1]):
			print('  {}║{}║'.format(8-i, '│'.join(map(lambda p: chess_glyphs[p], row))))
			if i < 7:
				print(sep_line)

		print('   ╚══╧══╧══╧══╧══╧══╧══╧══╝')
		print('    a  b  c  d  e  f  g  h ')
		print('')

chess = Chess()
chess.setupBoard()
chess.printBoard()
# chess.movePiece('N', (2,5), (0,6))
chess.movePiece('N', (2,5))
chess.printBoard()