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

Examples of valid possible moves are `Nf3`, `e4`, `e2-e4`, `Qxd7`, `exd5`

### Features
- [x] Basic moving of pieces
- [x] Printing board state
- [x] Printing moves so far
- [x] Algebraic move Input
    - [x] Long algebraic input
    - [ ] Disambiguated algebraic input
    - [ ] Pawn promotion
- [x] Capturing
- [x] Pawns
    - [x] Pawn Capturing
    - [x] Pawn capture notation
    - [ ] Pawn promotion
    - [ ] En passant
- [x] Castling
    - [x] Not after moving King/Rook
    - [ ] Not through check
- [ ] Check checking
- [ ] Checkmate checking

## Unit Tests
Tests are found in `test.py`. Unit tests can be done by running

    python -m unittest test.py

or, for verbose output,

    python -m unittest -v test.py
