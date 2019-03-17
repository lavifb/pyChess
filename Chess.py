import re

from Pieces import *

# glyphs for pretty chess piece output
chess_glyphs = {
	'WK': '♔ ', 'WQ': '♕ ', 'WR': '♖ ', 'WB': '♗ ', 'WN': '♘ ', 'WP': '♙ ',
	'BK': '♚ ', 'BQ': '♛ ', 'BR': '♜ ', 'BB': '♝ ', 'BN': '♞ ', 'BP': '♟ ',
	'  ': '  '
}

# conversion between chess notation and col index
col_conv = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}

class Chess:
	def __init__(self, glyhs=True):
		"""Initialize Chess Game

		Params:
		glyphs -- Use Unicode chess chars (default True)
		"""
		self.width  = 8
		self.height = 8
		self.glyhs = glyhs
		self.pieces = ()
		self.turn = 0 # White goes first

		# TODO: pawn promotion in regex
		self.move_re = re.compile(r'^([KQBNR]?)([abcdefgh][1-8])\s*(-\s*([abcdefgh][1-8]))?$')

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

	def makeMove(self, move):
		"""Makes chess move on board

		Moves are accepted in algebraic chess notation without move ambiguity.
		Moves are also accepted in long algebraic notation which also includes the starting position.

		Params:
		move -- String in algebraic chess notation
		"""

		# TODO: check for castling
		match = self.move_re.match(move)
		if match:
			piece, start_pos, end_pos = match.group(1, 2, 4)
			# If only end position is given
			if end_pos == None:
				end_pos = start_pos
				start_pos = None

			# set pawn for empty piece
			if piece == '':
				piece = 'P'

			self.movePiece(piece, end_pos, start_pos)
			self.turn = 1-self.turn

	def convertPosToCoords(self, pos):
		"""Convert position notation from board notation to (row, col).

		Ex: 
		f3 converts to (2,5)

		Note: No valid position notation checking is done here
		
		Params:
		pos -- chess square in chess notation

		Returns: coords of given square as zero-indexed (row, col)
		"""

		col = col_conv[pos[0]]
		row = int(pos[1]) - 1

		return (row, col)


	def movePiece(self, piece, end_pos, start_pos=None):
		end_coords = self.convertPosToCoords(end_pos)

		if start_pos == None:
			possible_pieces_to_move = []

			for p in self.pieces[self.turn]:
				if (p.row, p.col) == end_coords:
					raise ValueError("Cannot capture your own piece on {}".format(end_pos))
				if p.piece == piece:
					if end_coords in p.moves():
						possible_pieces_to_move.append(p)

			if len(possible_pieces_to_move) > 1:
				raise ValueError("Multiple pieces {} found that can make move to {}".format(piece, end_pos))
			elif len(possible_pieces_to_move) < 1:
				raise ValueError("No piece {} found that can make move to {}".format(piece, end_pos))

			possible_pieces_to_move[0].row, possible_pieces_to_move[0].col = end_coords
			possible_pieces_to_move[0].has_moved = True

		else:
			start_coords = self.convertPosToCoords(start_pos)
			piece_to_move = None
			for p in self.pieces[self.turn]:
				if (p.row, p.col) == end_coords:
					raise ValueError("Cannot capture your own piece on {}".format(end_pos))
				if (p.row, p.col) == start_coords:
					piece_to_move = p

			print(piece_to_move, piece_to_move.row, piece_to_move.col, piece_to_move.moves())
			if piece_to_move == None or piece_to_move.piece != piece:
				raise ValueError("No piece {} found at position {}".format(piece, end_pos))

			if end_coords in piece_to_move.moves():
				piece_to_move.row, piece_to_move.col = end_coords
				piece_to_move.has_moved = True
			else:
				raise ValueError("{} at {} cannot move to {}".format(piece, start_pos, end_pos))

		# TODO: Check for capture
		# TODO: Moving Pawns
		# TODO: Castling

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

def gameLoop(chess):
	while True:
		chess.printBoard()
		try:
			moveInput = input('    > ')
			if moveInput == 'q':
				return
			chess.makeMove(moveInput.strip())

		except ValueError as err:
			print(err)
			# print('Error making a move. Please try again.')


gameLoop(chess)