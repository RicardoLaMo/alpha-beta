# 3D Tic-Tac-Toe (4x4x4)

## Overview

This is a Python implementation of 3D Tic-Tac-Toe with a 4x4x4 board, converted from the original Java version. The game features an AI opponent that uses the minimax algorithm with alpha-beta pruning.

## Features

- **4x4x4 Game Board**: Four layers, each with a 4x4 grid (64 total spaces)
- **Fancy Canvas Icons**: Beautiful X and O pieces with gradients, shadows, and 3D effects
  - Blue gradient X pieces with highlights
  - Red/pink gradient O pieces with depth
  - Gold-colored winning pieces for celebration
- **AI Opponent**: Intelligent computer player using minimax with alpha-beta pruning
- **Three Difficulty Levels**:
  - **Easy**: 1 move lookahead
  - **Medium**: 2 moves lookahead
  - **Hard**: 4 moves lookahead (very challenging!)
- **Customizable Settings**:
  - Choose your piece (X or O)
  - Choose who goes first (Human or Computer)
  - Adjust difficulty level
- **Score Tracking**: Keeps track of wins for both players
- **Win Highlighting**: Winning combinations are highlighted in gold

## Requirements

- Python 3.6+
- tkinter (usually comes with Python)

## Installation

No installation required! Just make sure you have Python 3 installed with tkinter support.

To check if tkinter is available:
```bash
python3 -c "import tkinter"
```

If you get an error, you may need to install tkinter:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **macOS**: tkinter should be included with Python
- **Windows**: tkinter should be included with Python

## Running the Game

```bash
python3 ttt3d_4x4x4.py
```

## How to Play

1. **Objective**: Get 4 of your pieces in a row (horizontally, vertically, or diagonally) across any dimension

2. **Winning Combinations** (76 total):
   - Rows within a single layer
   - Columns within a single layer
   - Diagonals within a single layer
   - Vertical lines through layers
   - Diagonal lines through layers
   - 4 main space diagonals (corner to corner)

3. **Game Controls**:
   - Click any empty space to make your move
   - Use the control panel on the right to:
     - Start a new game
     - Select your piece (X or O)
     - Choose who goes first
     - Adjust difficulty level

4. **Tips**:
   - Think in 3D! Consider moves across all layers
   - Watch for the computer setting up multi-layer threats
   - On hard difficulty, the computer is very aggressive
   - Try "Easy" or "Medium" difficulty first to learn the game

## Game Board Layout

The game displays 4 layers arranged in a 2x2 grid:

```
Layer 1 | Layer 2
--------|--------
Layer 3 | Layer 4
```

Each layer is a 4x4 grid. Think of these as stacked on top of each other.

## Technical Details

### Visual Design

The game features enhanced visual design with Canvas-based rendering:

- **FancyIcon Class**: Custom drawing system for game pieces
  - `draw_x()`: Blue gradient X with shadow effects
  - `draw_o()`: Red/pink gradient O with 3D highlights
  - `draw_x_win()`: Gold X for winning combinations
  - `draw_o_win()`: Gold O for winning combinations

- **Color Scheme**:
  - X pieces: Blue (#2E86DE, #54A0FF, #74B9FF)
  - O pieces: Red/Pink (#EE5A6F, #FF6B81, #FF9FF3)
  - Winning pieces: Gold (#FFD700, #DAA520)
  - Shadows: Gray (#888888) for depth perception

### Winning Combinations

The game has 76 possible winning combinations:
- 16 rows (4 per layer × 4 layers)
- 16 columns (4 per layer × 4 layers)
- 8 layer diagonals (2 per layer × 4 layers)
- 16 vertical lines (through all 4 layers)
- 16 vertical plane diagonals
- 4 space diagonals (corner to corner through all dimensions)

### AI Algorithm

The computer uses a **minimax algorithm with alpha-beta pruning**:

- **Minimax**: Explores possible future moves to find the best choice
- **Alpha-Beta Pruning**: Optimizes the search by eliminating branches that won't affect the final decision
  - Alpha (α): Best value for maximizer (computer)
  - Beta (β): Best value for minimizer (human)
  - Pruning occurs when α >= β
  - Reduces search space by ~94-99.6% depending on depth
- **Heuristic Function**: Evaluates board positions by counting available winning paths

**Implementation Details**: See `ALPHA_BETA_VERIFICATION.md` for complete verification of the alpha-beta pruning implementation.

### Difficulty Levels

- **Easy**: Looks 1 move ahead, uses random moves when going first
- **Medium**: Looks 2 moves ahead, uses random moves when going first
- **Hard**: Looks 4 moves ahead, uses strategic opening moves

Note: Due to the larger board size (64 vs 27 spaces), the lookahead depth is reduced compared to the original 3x3x3 game to maintain reasonable performance.

## Differences from Original Java Version

1. **Board Size**: Expanded from 3x3x3 (27 spaces) to 4x4x4 (64 spaces)
2. **Winning Condition**: Changed from 3-in-a-row to 4-in-a-row
3. **GUI Framework**: Converted from Java Swing to Python tkinter
4. **Visual Design**: Enhanced with Canvas-based fancy icons (gradients, shadows, 3D effects)
5. **Layout**: Simplified board visualization using a 2x2 grid of layers
6. **Lookahead Depth**: Reduced on hard difficulty (4 vs 6) due to larger search space
7. **Win Highlighting**: Changed from red lines to gold-colored pieces

## Testing

### Verify Winning Combinations
Run the test suite to verify all 76 winning combinations are correct:

```bash
python3 test_winning_combos.py
```

### Test Fancy Icons
Display all icon variations in a test window:

```bash
python3 test_fancy_icons.py
```

This will show:
- Regular X (blue gradient)
- Regular O (red gradient)
- Winning X (gold)
- Winning O (gold)

## Known Limitations

- No 3D perspective drawing of the boards (uses simple 2x2 layer layout instead)
- On hard difficulty, the AI can take a few seconds to compute moves
- Requires tkinter for GUI (usually included with Python)

## Credits

Original Java implementation by Devigili (2012)
Python conversion and 4x4x4 expansion (2025)

## License

This is an educational project. Feel free to modify and use as you wish.
