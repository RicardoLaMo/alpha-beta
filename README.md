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
