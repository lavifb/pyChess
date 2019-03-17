import re
import copy

from consts import *
from Pieces import possiblePieceStarts

class Chess:
	def __init__(self, glyhs=True):
		"""Initialize Chess Game

		Params:
		glyphs -- Use Unicode chess chars (default True)
		"""
		self.width  = 8
		self.height = 8
		self.glyhs = glyhs
		self.board = [[EMPTY_SQUARE]*self.width for i in range(self.height)]
		self.turn = 0 # White goes first

		# TODO: pawn promotion in regex
		self.move_re = re.compile(r'^([KQBNR])?(?:([abcdefgh][1-8])?(:?[abcdefgh])?\s*([-x]))?\s*([abcdefgh][1-8])$')

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
			piece, start_pos, move_type, end_pos = match.group(1, 2, 4, 5)
			# If only end position is given
			# if end_pos == None:
			# 	end_pos = start_pos
			# 	start_pos = None

			# set pawn for empty piece
			if piece == None:
				piece = 'P'

			# check for capture
			capture = False
			if move_type == 'x':
				capture = True
				# TODO: pawn capture notation (use group 3)

			self.movePiece(piece, end_pos, start_pos, capture)
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


	def movePiece(self, piece, end_pos, start_pos=None, capture=False):
		end_coords = self.convertPosToCoords(end_pos)
		color = 'W' if self.turn == 0 else 'B'

		# check if end_pos is occupied
		if self.board[end_coords[0]][end_coords[1]][0][0] == color:
			raise ValueError("Cannot make move {}{} because {} is occupied by your own piece".format(piece, end_pos, end_pos))
		if not capture and self.board[end_coords[0]][end_coords[1]] != EMPTY_SQUARE:
			raise ValueError("Cannot make move {}{} because {} is occupied".format(piece, end_pos, end_pos))
		if capture and self.board[end_coords[0]][end_coords[1]] == EMPTY_SQUARE:
			raise ValueError("Cannot make capture {}x{} because {} is unoccupied".format(piece, end_pos, end_pos))

		possible_pieces_to_move = possiblePieceStarts(piece, end_coords, color, self.board)
		# print(possible_pieces_to_move)

		if len(possible_pieces_to_move) < 1:
			raise ValueError("No piece found that can make move {}{}".format(piece, end_pos))
		elif len(possible_pieces_to_move) > 1 and start_pos == None:
			raise ValueError("Multiple pieces found that can make move {}{}".format(piece, end_pos))

		start_coords = possible_pieces_to_move[0]
		if start_pos:
			start_coords = self.convertPosToCoords(start_pos)
			if start_coords not in possible_pieces_to_move:
				raise ValueError("No piece found that can make move from {}{} to {}".format(piece, start_pos, end_pos))


		# TODO: Castling

		# move piece
		newBoard = copy.deepcopy(self.board)
		newBoard[start_coords[0]][start_coords[1]] = EMPTY_SQUARE
		newBoard[end_coords[0]][end_coords[1]] = color + piece

		# TODO: check for check/checkmate

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
	print("Welcome to Chess!")
	print("Input 'q' to exit game")
	print("Unambiguous moves are accepted in algebraic chess notation\n\tEx: Nf3, e4, Rxa7")
	print("Moves are also accepted in long algebraic chess notation\n\tEx: Ng1-f3, e2-e4, Ra4xa7")
	print("\n")

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