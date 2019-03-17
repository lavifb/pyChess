import re
import copy

from Pieces import *

# glyphs for pretty chess piece output
chess_glyphs = {
	'WK': '♔ ', 'WQ': '♕ ', 'WR': '♖ ', 'WB': '♗ ', 'WN': '♘ ', 'WP': '♙ ',
	'BK': '♚ ', 'BQ': '♛ ', 'BR': '♜ ', 'BB': '♝ ', 'BN': '♞ ', 'BP': '♟ ',
	'  ': '  '
}

# conversion between chess notation and col index
col_conv = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}

EMPTY_SQUARE = '  '
ES = EMPTY_SQUARE

class Chess:
	def __init__(self, glyhs=True):
		"""Initialize Chess Game

		Params:
		glyphs -- Use Unicode chess chars (default True)
		"""
		self.width  = 8
		self.height = 8
		self.glyhs = glyhs
		self.board = [['  ']*self.width for i in range(self.height)]
		self.turn = 0 # White goes first

		# TODO: pawn promotion in regex
		self.move_re = re.compile(r'^([KQBNR]?)([abcdefgh][1-8])\s*(-\s*([abcdefgh][1-8]))?$')

	def setupBoard(self):
		"""Setup Chess Board to start game"""

		# Black Pieces
		self.board[7] = ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR']
		self.board[6] = ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP']

		# Empty squares
		for i in range(2,6):
			self.board[i] = [EMPTY_SQUARE]*8

		# White Pieces
		self.board[1] = ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP']
		self.board[0] = ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']

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
		else:
			print("'{}' is an invalid move".format(move))

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
		color = 'W' if self.turn == 0 else 'B'

		# TODO: Check for capture
		# check if end_pos is occupied
		if self.board[end_coords[0]][end_coords[1]] != EMPTY_SQUARE:
			raise ValueError("Cannot make move {}{} because the {} is occupied".format(piece, end_pos, end_pos))

		# if piece == 'N':
		possible_pieces_to_move = possiblePieceStarts(piece, end_coords, color, self.board)
		print(possible_pieces_to_move)

		if len(possible_pieces_to_move) > 1 and start_pos == None:
			raise ValueError("Multiple pieces found that can make move {}{}".format(piece, end_pos))
		elif len(possible_pieces_to_move) < 1:
			raise ValueError("No piece found that can make move {}{}".format(piece, end_pos))

		# move piece
		start_coords = possible_pieces_to_move[0]
		newBoard = copy.deepcopy(self.board)
		newBoard[start_coords[0]][start_coords[1]] = EMPTY_SQUARE
		newBoard[end_coords[0]][end_coords[1]] = color + piece

		# TODO: Moving Pawns
		# TODO: Castling
		self.board = newBoard

	def printBoard(self):
		"""Print board state to stdout"""
		sep_line = '   ╟──┼──┼──┼──┼──┼──┼──┼──╢'
		print('   ╔══╤══╤══╤══╤══╤══╤══╤══╗')
		for i, row in enumerate(self.board[::-1]):
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
			input_query = ''
			if chess.turn == 0:
				input_query = 'White to move > '
			else:
				input_query = 'Black to move > '

			moveInput = input(input_query)
			if moveInput == 'q':
				return
			chess.makeMove(moveInput.strip())

		except ValueError as err:
			print(err)
			# print('Error making a move. Please try again.')


gameLoop(chess)