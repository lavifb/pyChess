# pyChess
Simple command line chess game

     ╔══╤══╤══╤══╤══╤══╤══╤══╗
    8║♜ │♞ │♝ │♛ │♚ │♝ │♞ │♜ ║
     ╟──┼──┼──┼──┼──┼──┼──┼──╢
    7║♟ │♟ │♟ │♟ │♟ │♟ │♟ │♟ ║
     ╟──┼──┼──┼──┼──┼──┼──┼──╢
    6║  │  │  │  │  │  │  │  ║
     ╟──┼──┼──┼──┼──┼──┼──┼──╢
    5║  │  │  │  │  │  │  │  ║
     ╟──┼──┼──┼──┼──┼──┼──┼──╢
    4║  │  │  │  │  │  │  │  ║
     ╟──┼──┼──┼──┼──┼──┼──┼──╢
    3║  │  │  │  │  │  │  │  ║
     ╟──┼──┼──┼──┼──┼──┼──┼──╢
    2║♙ │♙ │♙ │♙ │♙ │♙ │♙ │♙ ║
     ╟──┼──┼──┼──┼──┼──┼──┼──╢
    1║♖ │♘ │♗ │♕ │♔ │♗ │♘ │♖ ║
     ╚══╧══╧══╧══╧══╧══╧══╧══╝
     a  b  c  d  e  f  g  h

Run the game by using

    python playChess.py

Input `q` to quit and `m` to see the moves so far.

The game accepts moves in long algebraic chess notation and standard algebraic chess notation fo unambiguous moves.

Examples of valid move inputs are `Nf3`, `e4`, `e2-e4`, `Qxd7`, `exd5`, `f8=Q`

The board is shown using Unicode Chess glyphs. If they render weird, try using a different font or rendering without glyphs using the `g` input.

### Features
- [x] Basic moving of pieces
    - [x] King
    - [x] Queen
    - [x] Bishop
    - [x] Rook
    - [x] Knight
    - [x] Pawns
- [x] Printing board state
- [x] Printing moves so far
- [x] Algebraic move Input
    - [x] Long algebraic input
    - [x] Pawn promotion
    - [ ] Disambiguated algebraic input
- [x] Capturing
- [x] Pawns
    - [x] Pawn Capturing
    - [x] Pawn capture notation
    - [x] Pawn promotion
    - [ ] En passant
- [x] Castling
    - [x] Not after moving King/Rook
- [x] Checks
	- [x] No moving into check
	- [x] No staying in check
	- [ ] No castling through check
- [ ] Checkmates

## Unit Tests
Tests are found in `test.py`. Unit tests can be done by running

    python -m unittest test.py

or, for verbose output,

    python -m unittest -v test.py
