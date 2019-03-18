# pyChess
Simple command line chess game

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


Unit tests can be done by running

    python -m unittest test.py

or, for verbose output,

    python -m unittest -v test.py