from Chess import Chess

class ChessGame:
	def __init__(self):
		"""Initializes chess class and board"""
		self.chess = Chess()

	def startGame(self):
		"""Starts the interactive chess game and runs the game loop"""
		print("Welcome to Chess!")
		print("Input 'q' to exit game")
		print("Input 'm' to see moves made so far")
		print("Unambiguous moves are accepted in algebraic chess notation\n\tEx: Nf3, e4, Rxa7")
		print("Moves are also accepted in long algebraic chess notation\n\tEx: Ng1-f3, e2-e4, Ra4xa7")
		print("\n")

		self.chess.setupBoard()
		self.gameLoop()

	def gameLoop(self):
		"""Runs the game loop, asking for input and exiting on 'q' input"""
		while True:
			self.chess.printBoard()
			try:
				input_query = ''
				if self.chess.turn == 0:
					input_query = 'White to move > '
				else:
					input_query = 'Black to move > '

				moveInput = input(input_query)
				if moveInput == 'q':
					return
				elif moveInput == 'm':
					self.chess.printMoves()
					continue
				self.chess.makeMove(moveInput.strip())

			except ValueError as err:
				print(err)
				# print('Error making a move. Please try again.')


if __name__ == "__main__":
	game = ChessGame()
	game.startGame()