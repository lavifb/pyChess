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

	def test_move_e3e4(self):
		"""
		Illegal e3-e4 chess move
		"""
		with self.assertRaises(ValueError):
			self.chess.makeMove('e3-e4')

		self.assertEqual(self.chess.board[1][4], 'WP')
		self.assertEqual(self.chess.board[3][4], EMPTY_SQUARE)

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
		self.chess.setSquare('b2', 'WP')
		self.chess.setSquare('c2', 'WP')
		self.chess.setSquare('c3', 'BP')
		self.chess.setSquare('d2', 'WP')
		self.chess.setSquare('d3', 'WP')

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

	# def test_en_passant(self):
	# 	"""
	# 	En passant
	# 	"""
	# 	self.chess.setSquare('a4', 'BP')
	# 	self.chess.makeMove('b4')
	# 	self.chess.makeMove('axb3')

	# 	self.assertEqual(self.chess.checkSquare('a4'), EMPTY_SQUARE)
	# 	self.assertEqual(self.chess.checkSquare('b4'), EMPTY_SQUARE)
	# 	self.assertEqual(self.chess.checkSquare('b3'), 'BP')

	# def test_no_en_passant(self):
	# 	"""
	# 	No en passant
	# 	"""
	# 	self.chess.setSquare('a4', 'BP')
	# 	self.chess.setSquare('g8', 'BK')

	# 	self.chess.makeMove('b4')
	# 	self.chess.makeMove('Kf7')
	# 	self.chess.makeMove('d4')
	# 	with self.assertRaises(ValueError):
	# 		self.chess.makeMove('axb3')

	# 	self.assertEqual(self.chess.checkSquare('a4'), 'BP')
	# 	self.assertEqual(self.chess.checkSquare('b4'), 'WP')
	# 	self.assertEqual(self.chess.checkSquare('b3'), EMPTY_SQUARE)


class KnightMovesTest(unittest.TestCase):
	def setUp(self):
		self.chess = Chess()
		self.chess.setSquare('g1', 'WN')
		self.chess.setSquare('h3', 'BB')
		self.chess.setSquare('d4', 'WP')

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

	def test_ambig_move1(self):
		"""
		Test ambiguous move
		"""

		self.chess.setSquare('e1', 'WN')
		with self.assertRaises(ValueError):
			self.chess.makeMove('Nf3')
		self.chess.makeMove('Ne1-f3')

		self.assertEqual(self.chess.checkSquare('g1'), 'WN')
		self.assertEqual(self.chess.checkSquare('e1'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('f3'), 'WN')

	def test_ambig_move2(self):
		"""
		Test ambiguous move
		"""

		self.chess.setSquare('e1', 'WN')
		with self.assertRaises(ValueError):
			self.chess.makeMove('Nf3')
		self.chess.makeMove('Ng1-f3')

		self.assertEqual(self.chess.checkSquare('e1'), 'WN')
		self.assertEqual(self.chess.checkSquare('g1'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('f3'), 'WN')


class QueenMovesTest(unittest.TestCase):
	"""
	Tests for Queen moves. Implicitly also tests rooks and bishop logic
	"""
	def setUp(self):
		self.chess = Chess()
		self.chess.setSquare('e3', 'WQ')

	def test_queen_moves(self):
		"""
		Test a bunch of valid and invalid queen moves
		"""
		self.chess.makeMove('Qe7')
		self.chess.turn = 0

		self.assertEqual(self.chess.checkSquare('e7'), 'WQ')
		self.assertEqual(self.chess.checkSquare('e3'), EMPTY_SQUARE)

		self.chess.makeMove('Qg5')
		self.chess.turn = 0
		with self.assertRaises(ValueError):
			self.chess.makeMove('Qg5')
		self.chess.makeMove('Qb5')
		self.chess.turn = 0
		self.chess.makeMove('Qf1')
		self.chess.turn = 0
		with self.assertRaises(ValueError):
			self.chess.makeMove('Qg5')
		with self.assertRaises(ValueError):
			self.chess.makeMove('Qg3')
		self.chess.makeMove('Qg2')

	def test_blocked_queen_moves(self):
		"""
		Test queen moves while blocked by pieces
		"""
		self.chess.setSquare('e4', 'WP')
		self.chess.setSquare('d4', 'BP')

		with self.assertRaises(ValueError):
			self.chess.makeMove('Qe7')

		with self.assertRaises(ValueError):
			self.chess.makeMove('Qxe7')

		with self.assertRaises(ValueError):
			self.chess.makeMove('Qe4')

		with self.assertRaises(ValueError):
			self.chess.makeMove('Qxe4')

		with self.assertRaises(ValueError):
			self.chess.makeMove('Qc5')

		with self.assertRaises(ValueError):
			self.chess.makeMove('Qxc5')

		with self.assertRaises(ValueError):
			self.chess.makeMove('Qd4')

		self.chess.makeMove('Qxd4')
		self.assertEqual(self.chess.checkSquare('d4'), 'WQ')
		self.assertEqual(self.chess.checkSquare('e3'), EMPTY_SQUARE)

class BishopRookMovesTest(unittest.TestCase):
	"""
	Tests for Bishop and Rook moves
	"""
	def setUp(self):
		self.chess = Chess()
		self.chess.setSquare('e3', 'WB')
		self.chess.setSquare('b7', 'BR')

	def test__moves(self):
		"""
		Test a bunch of valid and invalid bishop and rook moves
		"""
		self.chess.makeMove('Bc5')
		self.chess.makeMove('Rb6')
		with self.assertRaises(ValueError):
			self.chess.makeMove('Ba7')
		with self.assertRaises(ValueError):
			self.chess.makeMove('Ba5')
		self.chess.makeMove('Ba3')
		self.chess.makeMove('Rf6')
		self.chess.makeMove('Bb2')
		self.chess.makeMove('Rf8')

class CastlingTest(unittest.TestCase):
	"""
	Tests for Castling
	"""
	def setUp(self):
		self.chess = Chess()
		self.chess.setSquare('e1', 'WK')
		self.chess.setSquare('h1', 'WR')
		self.chess.setSquare('e8', 'BK')
		self.chess.setSquare('a8', 'BR')

	def test_castling(self):
		"""
		Test castling
		"""
		self.chess.makeMove('O-O')
		self.chess.makeMove('O-O-O')

		self.assertEqual(self.chess.checkSquare('e1'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('f1'), 'WR')
		self.assertEqual(self.chess.checkSquare('g1'), 'WK')
		self.assertEqual(self.chess.checkSquare('h1'), EMPTY_SQUARE)

		self.assertEqual(self.chess.checkSquare('e8'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('d8'), 'BR')
		self.assertEqual(self.chess.checkSquare('c8'), 'BK')
		self.assertEqual(self.chess.checkSquare('b8'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('a8'), EMPTY_SQUARE)

	def test_blocked_castle(self):
		"""
		Test blocked castling
		"""
		self.chess.setSquare('f1', 'WB')
		with self.assertRaises(ValueError):
			self.chess.makeMove('0-0')
		self.chess.makeMove('Be2')
		self.chess.makeMove('0-0-0')
		self.chess.makeMove('0-0')

	def test_moved_before_castle(self):
		"""
		Test illegal castling after moving pieces
		"""
		self.chess.setSquare('a1', 'WR')
		self.chess.makeMove('Rh2')
		self.chess.makeMove('Ke7')
		self.chess.makeMove('Rh1')
		self.chess.makeMove('Ke8')
		with self.assertRaises(ValueError):
			self.chess.makeMove('0-0')
		self.chess.makeMove('0-0-0')
		with self.assertRaises(ValueError):
			self.chess.makeMove('0-0-0')

	def test_castle_out_of_check(self):
		"""
		Test illegal castling out of check
		"""
		self.chess.setSquare('e4', 'BQ')
		with self.assertRaises(ValueError):
			self.chess.makeMove('0-0')
		with self.assertRaises(ValueError):
			self.chess.makeMove('Rf1')

	def test_castle_throught_check(self):
		"""
		Test illegal castling through check
		"""
		self.chess.setSquare('f4', 'BQ')
		with self.assertRaises(ValueError):
			self.chess.makeMove('0-0')
		self.chess.makeMove('Rf1')

class PawnPromotionTest(unittest.TestCase):
	def setUp(self):
		self.chess = Chess()
		self.chess.setSquare('e7', 'WP')
		self.chess.setSquare('e2', 'BP')
		self.chess.setSquare('f1', 'WN')

	def test_promotion(self):
		"""
		Pawn promotion
		"""
		with self.assertRaises(ValueError):
			self.chess.makeMove('e8')
		with self.assertRaises(ValueError):
			self.chess.makeMove('exf8')
		self.chess.makeMove('e8=N')
		with self.assertRaises(ValueError):
			self.chess.makeMove('exf1')
		with self.assertRaises(ValueError):
			self.chess.makeMove('exf1=K')
		self.chess.makeMove('exf1=Q')

		self.assertEqual(self.chess.checkSquare('e7'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('e8'), 'WN')
		self.assertEqual(self.chess.checkSquare('e2'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('e1'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('f1'), 'BQ')

	def test_not_promotion(self):
		"""
		Not promotios
		"""
		self.chess.setSquare('e8', 'BB')
		self.chess.setSquare('a2', 'WP')
		with self.assertRaises(ValueError):
			self.chess.makeMove('Ne3=R')
		with self.assertRaises(ValueError):
			self.chess.makeMove('e8=B')
		with self.assertRaises(ValueError):
			self.chess.makeMove('a4=Q')

class CheckTests(unittest.TestCase):
	def setUp(self):
		self.chess = Chess()
		self.chess.setSquare('e1', 'WK')
		self.chess.setSquare('f3', 'BN')
		self.chess.setSquare('c4', 'BB')
		self.chess.setSquare('d8', 'BR')
		self.chess.setSquare('a2', 'WP')

	def test_moving_in_check(self):
		"""
		No moving into check
		"""

		with self.assertRaises(ValueError):
			self.chess.makeMove('a3')
		with self.assertRaises(ValueError):
			self.chess.makeMove('Ke2')
		with self.assertRaises(ValueError):
			self.chess.makeMove('Kd1')
		self.chess.makeMove('Kf2')

		self.assertEqual(self.chess.checkSquare('e1'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('f2'), 'WK')

	def test_pinned_check(self):
		"""
		No moving pinned piece into check
		"""
		self.chess.setSquare('f3', 'WN')
		self.chess.setSquare('b4', 'BQ')
		self.chess.setSquare('d2', 'WR')

		with self.assertRaises(ValueError):
			self.chess.makeMove('Rd6')
		self.chess.makeMove('a3')

		self.assertEqual(self.chess.checkSquare('d6'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('d2'), 'WR')

	def test_pawn_check1(self):
		"""
		No allowing pawn checks
		"""
		self.chess.setSquare('f3', 'WN')
		self.chess.setSquare('f2', 'BP')
		self.chess.setSquare('e2', 'BP')

		with self.assertRaises(ValueError):
			self.chess.makeMove('a3')
		self.chess.makeMove('Kxf2')
		
		self.assertEqual(self.chess.checkSquare('e1'), EMPTY_SQUARE)
		self.assertEqual(self.chess.checkSquare('f2'), 'WK')

	def test_pawn_check2(self):
		"""
		King not in check in front of pawn
		"""
		self.chess.setSquare('f3', 'WN')
		self.chess.setSquare('e2', 'BP')

		self.chess.makeMove('a3')

	def test_block_check(self):
		"""
		Check should be able to be blocked
		"""

		self.chess.setSquare('f3', 'WN')
		self.chess.setSquare('b4', 'BQ')
		self.chess.setSquare('g5', 'WB')

		self.chess.makeMove('Bd2')

		
if __name__ == '__main__':
	unittest.main()