# 3D Tic-Tac-Toe with Alpha-Beta Pruning

A sophisticated implementation of 3D Tic-Tac-Toe (4x4x4 board with 64 positions) featuring an AI opponent powered by the Alpha-Beta pruning algorithm.

## Features

- **3D Gameplay**: 4x4x4 board with 64 total positions (4 levels, each 4x4)
- **76 Winning Lines**: All possible winning combinations including:
  - Horizontal lines within each level
  - Vertical lines within each level
  - Diagonal lines within each level
  - Vertical lines through all levels
  - Diagonal lines across vertical planes
  - 4 unique 3D space diagonals
- **AI Opponent**: Intelligent computer player using Alpha-Beta pruning
- **Multiple Difficulty Levels**:
  - **Easy**: AI searches 2 levels deep
  - **Difficult**: AI searches 4 levels deep
  - **Insane**: AI searches 6 levels deep
- **Single Player Mode**: Human vs AI

## How to Play

### Running the Game

```bash
python3 tictactoe_3d.py
```

### Game Rules

1. The board consists of 4 levels (z-axis: 0-3)
2. Each level is a 4x4 grid (y-axis: 0-3, x-axis: 0-3)
3. Players take turns placing their mark (X for player, O for AI)
4. Win by getting 4 marks in a row (horizontally, vertically, or diagonally in any direction)
5. The game ends in a draw if all 64 positions are filled with no winner

### Input Format

When it's your turn, you'll be prompted to enter:
- **Level**: 1-4 (which layer of the 3D board)
- **Row**: 0-3 (vertical position within the level)
- **Column**: 0-3 (horizontal position within the level)

## Algorithm Details

### Alpha-Beta Pruning

The AI uses the **Alpha-Beta pruning algorithm**, an optimization of the minimax algorithm that reduces the number of nodes evaluated in the game tree.

**Key Components:**

1. **Minimax Principle**:
   - AI (O) tries to minimize the score
   - Player (X) tries to maximize the score

2. **Alpha-Beta Pruning**:
   - Alpha: Best value that the maximizer can guarantee
   - Beta: Best value that the minimizer can guarantee
   - Prunes branches that cannot influence the final decision

3. **Scoring**:
   - +10: Player (X) wins
   - -10: AI (O) wins
   - 0: Draw or non-terminal state

4. **Depth Control**:
   - Limits search depth based on difficulty level
   - Balances computation time with AI intelligence

### Difficulty Levels Implementation

```python
difficulty_depths = {
    'easy': 2,       # Searches 2 moves ahead
    'difficult': 4,  # Searches 4 moves ahead
    'insane': 6      # Searches 6 moves ahead
}
```

### Alpha-Beta Minimax Algorithm Implementation

The core game engine uses the **Alpha-Beta Minimax algorithm** (`tictactoe_3d.py:147-194`), which is the heart of the AI's decision-making process.

#### Algorithm Method Signature

```python
def alpha_beta_minimax(self, depth, alpha, beta, player):
    """
    Args:
        depth: Maximum depth to search (2, 4, or 6 based on difficulty)
        alpha: Alpha value for pruning (best for maximizer)
        beta: Beta value for pruning (best for minimizer)
        player: Current player (1 for X, -1 for O)

    Returns:
        [z, y, x, score] - best move coordinates and its score
    """
```

#### How It Works

1. **Terminal Condition Check** (`tictactoe_3d.py:165-166`):
   ```python
   if depth == 0 or self.game_won() or self.board_full():
       return [z_pos, y_pos, x_pos, self.get_score()]
   ```
   - Stops searching when depth limit reached or game is over
   - Returns the score: +10 (player wins), -10 (AI wins), or 0 (draw)

2. **Recursive Search** (`tictactoe_3d.py:170-173`):
   ```python
   for cell in blanks:
       z, y, x = cell
       self.set_move(z, y, x, player)
       score = self.alpha_beta_minimax(depth - 1, alpha, beta, -player)
   ```
   - Tries each possible move
   - Recursively evaluates the resulting position
   - Alternates between players (player becomes -player)

3. **Minimax Evaluation** (`tictactoe_3d.py:175-182`):
   ```python
   if player == 1:  # Maximizing player (X)
       if score[3] > alpha:
           alpha = score[3]
           z_pos, y_pos, x_pos = z, y, x
   else:  # Minimizing player (O)
       if score[3] < beta:
           beta = score[3]
           z_pos, y_pos, x_pos = z, y, x
   ```
   - **Player (X)** tries to maximize the score (alpha)
   - **AI (O)** tries to minimize the score (beta)
   - Tracks the best move found so far

4. **Alpha-Beta Pruning** (`tictactoe_3d.py:188-189`):
   ```python
   if alpha >= beta:
       break
   ```
   - **Critical optimization**: Stops exploring branches that cannot affect the final decision
   - If the maximizer's best option (alpha) is already better than or equal to the minimizer's best option (beta), remaining moves in this branch are irrelevant
   - Dramatically reduces the number of positions evaluated without affecting the result

5. **Move Undo** (`tictactoe_3d.py:185`):
   ```python
   self.set_move(z, y, x, 0)
   ```
   - Restores the board to its previous state after evaluation
   - Allows trying all possible moves from the current position

#### AI Move Integration

The AI uses this algorithm when making moves (`tictactoe_3d.py:196-223`):

```python
def ai_move(self, difficulty='difficult'):
    # Get depth based on difficulty
    depth = self.difficulty_depths.get(difficulty, 4)

    # Call alpha-beta minimax with initial values
    result = self.alpha_beta_minimax(max_depth, -inf, inf, -1)

    # Make the move
    z, y, x = result[0], result[1], result[2]
    self.set_move(z, y, x, -1)
```

**Initial values**:
- `alpha = -infinity`: Maximizer starts with worst possible score
- `beta = +infinity`: Minimizer starts with worst possible score
- `player = -1`: AI (O) is the minimizing player

#### Performance Optimization

The implementation includes smart optimizations:

1. **Early-game randomization** (`tictactoe_3d.py:206-210`):
   - When board has 60+ empty positions, makes random moves
   - Avoids expensive computation on nearly empty boards
   - Speeds up game start without affecting quality

2. **Adaptive depth limiting** (`tictactoe_3d.py:216`):
   ```python
   max_depth = min(depth, len(blanks))
   ```
   - Limits search depth to number of remaining positions
   - Prevents unnecessary deep searches near game end

#### Algorithm Efficiency

The alpha-beta pruning optimization provides significant performance improvements:

- **Worst case**: O(b^d) - same as minimax (no pruning)
- **Best case**: O(b^(d/2)) - effectively doubles the search depth possible
- **Typical case**: Much closer to best case with good move ordering

Where `b` is the branching factor (possible moves) and `d` is the search depth.

For a 4x4x4 board:
- Up to 64 possible moves initially
- Alpha-beta pruning cuts off many branches
- Makes deeper search (depth 6) computationally feasible

## Technical Implementation

### Board Representation

The board is represented as a 3D list:
```python
board[z][y][x]
```
- `z`: Level (0-3)
- `y`: Row (0-3)
- `x`: Column (0-3)

Values:
- `0`: Empty
- `1`: Player (X)
- `-1`: AI (O)

### Winning Line Detection

The game checks all 76 possible winning lines:
- 16 horizontal rows (4 levels × 4 rows)
- 16 vertical columns (4 levels × 4 columns)
- 8 diagonals within levels (4 levels × 2 diagonals)
- 16 vertical lines through levels (4×4 positions)
- 8 diagonals in YZ planes (4 positions × 2 diagonals)
- 8 diagonals in XZ planes (4 positions × 2 diagonals)
- 4 3D space diagonals

## Files

- `tictactoe_3d.py`: Main game implementation with AI
- `Final Project Draft.ipynb`: Jupyter notebook with initial development
- `README.md`: This file

## Example Game Session

```
===========================================================
3D TIC-TAC-TOE with ALPHA-BETA PRUNING
4x4x4 Board (64 positions)
===========================================================

Select difficulty level:
1. Easy (AI searches 2 levels deep)
2. Difficult (AI searches 4 levels deep)
3. Insane (AI searches 6 levels deep)
Enter choice (1-3): 2

Difficulty set to: DIFFICULT

Who goes first?
1. You (X)
2. AI (O)
Enter choice (1-2): 1

You (X) go first!

[Board displays...]

Enter your move (X):
  Level (1-4): 1
  Row (0-3): 0
  Column (0-3): 0

[Game continues...]
```

## Performance Considerations

- **Early Game Optimization**: AI makes random moves when board is nearly empty (60+ empty positions)
- **Adaptive Depth**: Search depth is limited by the number of remaining empty positions
- **Pruning Efficiency**: Alpha-Beta pruning significantly reduces computation compared to pure minimax

## Future Enhancements

Potential improvements:
- Graphical user interface (GUI)
- Multiplayer mode (human vs human)
- Move history and undo functionality
- AI move hints for the player
- Save/load game state
- Performance statistics and move analysis

## Credits

Based on the classic Alpha-Beta pruning algorithm applied to 3D Tic-Tac-Toe.

## License

Open source - feel free to modify and distribute.
