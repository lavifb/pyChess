import re
import copy

from consts import *
from Pieces import possiblePieceStarts

class Chess:
	def __init__(self, glyphs=True):
		"""Initialize Chess Game

		Params:
		glyphs -- Use Unicode chess chars (default True)
		"""
		self.width  = 8
		self.height = 8
		self.glyphs = glyphs
		self.board = [[EMPTY_SQUARE]*self.width for i in range(self.height)]
		self.turn = 0 # White goes first
		self.moves = [[],[]] # records moves made so far

		# Holds whether you can still castle king and queen side for each player
		# player can castle king  if self.castle[self.turn][0]
		# player can castle queen if self.castle[self.turn][1]
		self.castle = [[True, True], [True, True]]

		self.move_re = re.compile(r'^([KQBNR])?(?:([abcdefgh][1-8])?(:?[abcdefgh])?\s*([-x]))?\s*([abcdefgh][1-8])(?:=([QBNR]))?$')

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

		if move in ['O-O', '0-0']:
			self.moveCastle('king')
		elif move in ['O-O-O', '0-0-0']:
			self.moveCastle('queen')
		else:
			match = self.move_re.match(move)
			if match:
				piece, start_pos, pawn_pos, move_type, end_pos, promotion = match.group(1, 2, 3, 4, 5, 6)

				# set pawn for empty piece
				if piece == None:
					piece = 'P'

				# check for capture
				capture = False
				if move_type == 'x':
					capture = True
					if piece == 'P':
						if pawn_pos == None and start_pos == None:
							raise ValueError("'{}' is an invalid move".format(move))
							return
						if start_pos == None:
							# mark that rank is not given
							start_pos = 'X'+pawn_pos

				self.movePiece(piece, end_pos, start_pos, capture, promotion)
			else:
				raise ValueError("'{}' is an invalid move".format(move))
		
		# record move
		self.moves[self.turn].append(move)
		# change turns
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

	def checkSquare(self, pos):
		"""Returns string denoting the current occupant of the chess square

		Params:
		pos -- Chess position in chess notation (not checked for valid inputs)

		Returns: string with current piece in square or EMPTY_SQUARE const if empty

		Ex:
		In the starting position, checkSquare('e1') -> 'WK' and checkSquare('e4') -> '  '
		"""

		coords = self.convertPosToCoords(pos)
		return self.board[coords[0]][coords[1]]

	def setSquare(self, pos, piece):
		"""Places piece on given square

		Params:
		pos -- Chess position in chess notation (not checked for valid inputs)
		piece -- Chess piece given by 2 char string color+type
			color in ['W','B']
			type in ['K','Q','R','B','N','P']

		Ex:
		To place white knight on b2 call setSquare('b2', 'WN')
		"""

		if len(piece) != 2:
			raise ValueError("'{}' is not a valid 2 char string piece input".format(piece))
		if piece[0] not in ['W','B']:
			raise ValueError('{} is not a valid color'.format(piece[0]))
		if piece[1] not in ['K','Q','R','B','N','P']:
			raise ValueError('{} is not a valid piece type'.format(piece[1]))

		coords = self.convertPosToCoords(pos)
		self.board[coords[0]][coords[1]] = piece

	def movePiece(self, piece, end_pos, start_pos=None, capture=False, promotion=None):
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

		# Pawn notation is weird. This covers notation like 'exd4'
		if piece == 'P' and capture and start_pos[0] == 'X':
			# rank not given
			start_col = col_conv[start_pos[1]]
			start_coords = None
			for poss_start in possible_pieces_to_move:
				if poss_start[1] == start_col:
					start_coords = poss_start
			if start_coords == None:
				raise ValueError("No pawn found that can make move {}x{}".format(start_pos[0], end_pos))

		else:
			if start_pos:
				start_coords = self.convertPosToCoords(start_pos)
				if start_coords not in possible_pieces_to_move:
					raise ValueError("No piece found that can make move from {}{} to {}".format(piece, start_pos, end_pos))
			
		# Pawn promotion
		if piece == 'P' and (self.turn == 0 and end_coords[0] == 7) or (self.turn == 1 and end_coords[0] == 0):
			if promotion:
				piece = promotion
			else:
				raise ValueError("Cannot move to {} without promotion".format(piece, end_pos))
		else:
			if promotion:
				raise ValueError("Cannot promote with this move")



		# move piece
		newBoard = copy.deepcopy(self.board)
		newBoard[start_coords[0]][start_coords[1]] = EMPTY_SQUARE
		newBoard[end_coords[0]][end_coords[1]] = color + piece

		if self.checkForCheck(newBoard):
			raise ValueError("Cannot make move to a position in check")
		# TODO: check for checkmate

		# handle castling rules
		castle_row = 0 if self.turn == 0 else 7
		if piece == 'K':
			self.castle[self.turn] = [False, False]
		elif piece == 'R' and start_coords == (castle_row, 0):
			self.castle[self.turn][1] = False
		elif piece == 'R' and start_coords == (castle_row, 7):
			self.castle[self.turn][0] = False

		self.board = newBoard

	def moveCastle(self, side='king'):
		"""Performs Castling for current player if allowed

		Params:
		side -- Side to castle on ['king','queen']

		"""

		# TODO: castle out of check
		# TODO: castle through check

		row = 0 if self.turn == 0 else 7
		color = 'W' if self.turn == 0 else 'B'

		if side=='king':
			if (self.board[row][4], self.board[row][5], self.board[row][6], self.board[row][7]) \
				!= (color+'K', EMPTY_SQUARE, EMPTY_SQUARE, color+'R'):
				raise ValueError("Pieces are not in place to castle king side")
			if not self.castle[self.turn][0]:
				raise ValueError("Castling king side no longer allowed")

			# Castle
			self.board[row][4], self.board[row][5], self.board[row][6], self.board[row][7] \
				= EMPTY_SQUARE, color+'R', color+'K', EMPTY_SQUARE

			self.castle[self.turn] = [False, False]

		if side=='queen':
			if (self.board[row][4], self.board[row][3], self.board[row][2], self.board[row][1], self.board[row][0]) \
				!= (color+'K', EMPTY_SQUARE, EMPTY_SQUARE, EMPTY_SQUARE, color+'R'):
				raise ValueError("Pieces are not in place to castle queen side")
			if not self.castle[self.turn][1]:
				raise ValueError("Castling queen side no longer allowed")

			# Castle
			self.board[row][4], self.board[row][3], self.board[row][2], self.board[row][1], self.board[row][0] \
				= EMPTY_SQUARE, color+'R', color+'K', EMPTY_SQUARE, EMPTY_SQUARE

			self.castle[self.turn] = [False, False]

	def findKing(self, board):
		color = 'W' if self.turn == 0 else 'B'
		king_coords = None
		for row in range(len(board)):
			for col in range(len(board[row])):
				if board[row][col] == color+'K':
					king_coords = (row,col)
					return king_coords

		return None

	def checkForCheck(self, board):
		opposing_color = 'W' if self.turn == 1 else 'B'
		king_coords = self.findKing(board)
		if king_coords == None:
			return False
		for piece in ['Q','R','B','N','P']:
			possible_pieces_to_move = possiblePieceStarts(piece, king_coords, opposing_color, board)
			if possible_pieces_to_move:
				return True

		return False

	def printBoard(self):
		"""Print board state to stdout"""
		sep_line = '   ╟──┼──┼──┼──┼──┼──┼──┼──╢'
		print('   ╔══╤══╤══╤══╤══╤══╤══╤══╗')
		for i, row in enumerate(self.board[::-1]):
			print('  {}║{}║'.format(8-i, '│'.join(map(lambda p: chess_glyphs[p] if self.glyphs else p, row))))
			if i < 7:
				print(sep_line)

		print('   ╚══╧══╧══╧══╧══╧══╧══╧══╝')
		print('    a  b  c  d  e  f  g  h ')
		print('')

	def printMoves(self):
		"""Prints moves made to stdout"""
		print('\n')
		print('  WHITE  │  BLACK  ')
		print('═════════╪═════════')
		for wm, bm in zip(*self.moves):
			print("{:9}│{:9}".format(wm, bm))
		# if black has one less move
		if len(self.moves[0]) > len(self.moves[1]):
			print("{:9}│".format(self.moves[0][-1]))

		print('\n')