import unittest
from Chess import Chess
from consts import EMPTY_SQUARE

class SimpleInputsTest(unittest.TestCase):
	def setUp(self):
		self.chess = Chess()
		self.chess.setupBoard()

	def test_move_e4(self):
		"""
		Simple e4 chess move
		"""
		self.chess.makeMove('e4')

		self.assertEqual(self.chess.board[1][4], EMPTY_SQUARE)
		self.assertEqual(self.chess.board[3][4], 'WP')

	def test_taking_turns(self):
		"""
		Turns change only after legal moves
		"""
		self.chess.makeMove('e4')
		self.assertEqual(self.chess.turn, 1)
		self.chess.makeMove('e5')
		self.assertEqual(self.chess.turn, 0)
		with self.assertRaises(ValueError):
			self.chess.makeMove('e5')
		self.assertEqual(self.chess.turn, 0)

	def test_move_e2e4(self):
		"""
		Simple e2-e4 chess move
		"""
		self.chess.makeMove('e2-e4')

		self.assertEqual(self.chess.board[1][4], EMPTY_SQUARE)
		self.assertEqual(self.chess.board[3][4], 'WP')

	def test_move_Nf3(self):
		"""
		Simple Nf3 chess move
		"""
		self.chess.makeMove('Nf3')

		self.assertEqual(self.chess.board[3][4], EMPTY_SQUARE)
		self.assertEqual(self.chess.board[1][4], 'WP')
		self.assertEqual(self.chess.board[0][6], EMPTY_SQUARE)
		self.assertEqual(self.chess.board[2][5], 'WN')

	def test_bad_input(self):
		"""
		Bad input chess move
		"""
		with self.assertRaises(ValueError):
			self.chess.makeMove('nf4')

		self.assertEqual(self.chess.board[3][4], EMPTY_SQUARE)
		self.assertEqual(self.chess.board[1][4], 'WP')
		self.assertEqual(self.chess.board[0][6], 'WN')
		self.assertEqual(self.chess.board[0][1], 'WN')

	def test_illegal_move_input(self):
		"""
		Bad e5 chess move
		"""
		with self.assertRaises(ValueError):
			self.chess.makeMove('e5')

		self.assertEqual(self.chess.board[3][4], EMPTY_SQUARE)
		self.assertEqual(self.chess.board[1][4], 'WP')

	def test_pos_conv(self):
		"""
		Position to array coord conversion
		"""
		self.assertEqual(self.chess.convertPosToCoords('a4'), (3,0))
		self.assertEqual(self.chess.convertPosToCoords('g5'), (4,6))


class PawnMovesTest(unittest.TestCase):
	def setUp(self):
		self.chess = Chess()
		self.chess.placeOnSquare('b2', 'WP')
		self.chess.placeOnSquare('c2', 'WP')
		self.chess.placeOnSquare('c3', 'BP')
		self.chess.placeOnSquare('d2', 'WP')
		self.chess.placeOnSquare('d3', 'WP')

	def test_illegal_hop1(self):
		"""
		Illegal pawn hopping over other color
		"""
		with self.assertRaises(ValueError):
			self.chess.makeMove('c4')

		self.assertEqual(self.chess.checkSquare('c2'), 'WP')
		self.assertEqual(self.chess.checkSquare('c3'), 'BP')
		self.assertEqual(self.chess.checkSquare('d2'), 'WP')
		self.assertEqual(self.chess.checkSquare('d3'), 'WP')
		self.assertEqual(self.chess.checkSquare('c4'), EMPTY_SQUARE)

	def test_illegal_hop2(self):
		"""
		Illegal pawn hopping over same color
		"""
		with self.assertRaises(ValueError):
			self.chess.makeMove('d2-d4')

		self.assertEqual(self.chess.checkSquare('c2'), 'WP')
		self.assertEqual(self.chess.checkSquare('c3'), 'BP')
		self.assertEqual(self.chess.checkSquare('d2'), 'WP')
		self.assertEqual(self.chess.checkSquare('d3'), 'WP')
		self.assertEqual(self.chess.checkSquare('d4'), EMPTY_SQUARE)

	def test_move_correct_pawn(self):
		"""
		Move correct pawn of doubled pawns
		"""
		self.chess.makeMove('d4')

		self.assertEqual(self.chess.checkSquare('c2'), 'WP')
		self.assertEqual(self.chess.checkSquare('c3'), 'BP')
		self.assertEqual(self.chess.checkSquare('d2'), 'WP')
		self.assertEqual(self.chess.checkSquare('d4'), 'WP')
		self.assertEqual(self.chess.checkSquare('d3'), EMPTY_SQUARE)

	def test_move_illegal_capture_input1(self):
		"""
		Illegal capture input
		"""
		with self.assertRaises(ValueError):
			self.chess.makeMove('c3')

		self.assertEqual(self.chess.checkSquare('c2'), 'WP')
		self.assertEqual(self.chess.checkSquare('c3'), 'BP')
		self.assertEqual(self.chess.checkSquare('d2'), 'WP')
		self.assertEqual(self.chess.checkSquare('d3'), 'WP')

	def test_move_illegal_capture_input2(self):
		"""
		Illegal capture input
		"""
		with self.assertRaises(ValueError):
			self.chess.makeMove('axc3')

		self.assertEqual(self.chess.checkSquare('c2'), 'WP')
		self.assertEqual(self.chess.checkSquare('c3'), 'BP')
		self.assertEqual(self.chess.checkSquare('d2'), 'WP')
		self.assertEqual(self.chess.checkSquare('d3'), 'WP')

	def test_move_capture_input1(self):
		"""
		Capture input dxc3
		"""
		self.chess.makeMove('dxc3')

		self.assertEqual(self.chess.checkSquare('b2'), 'WP')
		self.assertEqual(self.chess.checkSquare('c2'), 'WP')
		self.assertEqual(self.chess.checkSquare('c3'), 'WP')
		self.assertEqual(self.chess.checkSquare('d2'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('d3'), 'WP')

	def test_move_capture_input2(self):
		"""
		Capture input bxc3
		"""
		self.chess.makeMove('bxc3')

		self.assertEqual(self.chess.checkSquare('b2'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('c2'), 'WP')
		self.assertEqual(self.chess.checkSquare('c3'), 'WP')
		self.assertEqual(self.chess.checkSquare('d2'), 'WP')
		self.assertEqual(self.chess.checkSquare('d3'), 'WP')


class KnightMovesTest(unittest.TestCase):
	def setUp(self):
		self.chess = Chess()
		self.chess.placeOnSquare('g1', 'WN')
		self.chess.placeOnSquare('h3', 'BB')
		self.chess.placeOnSquare('d4', 'WP')

	def test_move1(self):
		"""
		Move knight
		"""
		self.chess.makeMove('Nf3')

		self.assertEqual(self.chess.checkSquare('g1'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('f3'), 'WN')

	def test_move_to_occupied(self):
		"""
		Cant move knight to occupied
		"""
		with self.assertRaises(ValueError):
			self.chess.makeMove('Nh3')

		self.assertEqual(self.chess.checkSquare('h3'), 'BB')
		self.assertEqual(self.chess.checkSquare('g1'), 'WN')

	def test_capture(self):
		"""
		Knight captures occupied
		"""
		self.chess.makeMove('Nxh3')

		self.assertEqual(self.chess.checkSquare('g1'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('h3'), 'WN')

	def test_bad_capture(self):
		"""
		Knight doesnt capture own piece occupied
		"""

		self.chess.makeMove('Ne2')
		self.chess.makeMove('Bg4')
		with self.assertRaises(ValueError):
			self.chess.makeMove('Nd4')
		with self.assertRaises(ValueError):
			self.chess.makeMove('Nxd4')

		self.assertEqual(self.chess.checkSquare('g1'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('e2'), 'WN')
		self.assertEqual(self.chess.checkSquare('d4'), 'WP')

		self.chess.makeMove('d5')
		self.assertEqual(self.chess.checkSquare('d4'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('d5'), 'WP')

if __name__ == '__main__':
	unittest.main()