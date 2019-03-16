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
		glyphs -- Use unicode chess chars (default True)
		"""
		self.width  = BOARD_WIDTH
		self.height = BOARD_HEIGHT
		self.board = [['  ']*self.width for i in range(self.height)]
		self.glyhs = glyhs

	def setupBoard(self):
		"""Setup Chess Board to start game"""

		# Black Pieces
		self.board[7] = ['BR', 'BN', 'BB', 'BQ', 'BK', 'BB', 'BN', 'BR']
		self.board[6] = ['BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP', 'BP']

		# Empty squares
		for i in range(2,6):
			self.board[i] = ['  ', '  ', '  ', '  ', '  ', '  ', '  ', '  ']

		# White Pieces
		self.board[1] = ['WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP', 'WP']
		self.board[0] = ['WR', 'WN', 'WB', 'WQ', 'WK', 'WB', 'WN', 'WR']

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
chess.printBoard()
chess.setupBoard()
chess.printBoard()