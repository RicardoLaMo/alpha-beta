# Atari 3D Tic-Tac-Toe - Enhanced Version

## Overview

This enhanced version recreates the classic **Atari 4×4×4 3D Tic-Tac-Toe** game with modern improvements while maintaining the retro aesthetic. The game features a smart AI opponent using minimax with alpha-beta pruning.

## Key Improvements Over Reference Implementation

### 🎨 Visual Enhancements

1. **Classic Atari Color Scheme**
   - Dark blue-black background (#1a1a2e) for authentic retro feel
   - Bright cyan (#4ecca3) grid lines inspired by classic arcade games
   - Orange-red X pieces (#ee6c4d) and cyan O pieces (#4ecca3)
   - Gold highlighting (#ffd700) for winning combinations
   - Gradient layer backgrounds for depth perception

2. **Better Layer Visualization**
   - Each of 4 layers displayed in a clear 2×2 grid layout
   - Distinct background colors for each layer with gradient effect
   - Layer labels ("LAYER 1-4") in retro font
   - Raised borders with 3D effect for depth

3. **Smooth Animations**
   - Animated drawing of X pieces (diagonal lines draw sequentially)
   - Animated drawing of O pieces (arc sweeps 360 degrees)
   - Hover effects showing semi-transparent highlight on empty cells
   - Winning combinations highlighted in gold with border

4. **Retro Typography**
   - Courier font throughout for authentic computer terminal feel
   - Bold headings and clear hierarchy
   - High contrast text colors for readability

### 🎮 Gameplay Improvements

1. **Smart AI with Multiple Difficulty Levels**
   - **Easy**: Random moves with basic evaluation
   - **Medium**: Minimax search with depth 3
   - **Hard**: Deep minimax search with depth 4 and alpha-beta pruning

2. **Flexible Game Options**
   - Choose X or O pieces
   - Select who goes first (Human or Computer)
   - Adjust difficulty on the fly
   - Score tracking across multiple games (Wins/Losses/Ties)

3. **Enhanced User Experience**
   - Visual hover feedback when mousing over cells
   - Status messages indicating game state
   - Disabled cells after placement (no accidental clicks)
   - Clear winning line visualization

### 🏗️ Technical Improvements

1. **Clean Code Architecture**
   - Well-organized class structure
   - Type hints for better code clarity
   - Dataclass for Move representation
   - Separated concerns (game logic vs. UI)

2. **Optimized AI**
   - Alpha-beta pruning for faster move calculation
   - Configurable search depth
   - Immediate win detection
   - Board evaluation heuristics

3. **Complete Winning Combinations**
   - All 76 possible winning combinations for 4×4×4:
     - 16 rows (4 per layer × 4 layers)
     - 16 columns (4 per layer × 4 layers)
     - 8 layer diagonals (2 per layer × 4 layers)
     - 16 vertical lines through layers
     - 16 diagonal lines through vertical planes
     - 4 space diagonals (corner to corner)

## Visual Comparison

### Reference Implementation (sairghan)
- Basic ASCII text representation
- Simple terminal interface
- Limited visual feedback
- No animations
- Monochrome or basic colors

### This Enhanced Version
- Full graphical interface with retro styling
- Animated piece placement
- Hover effects and visual feedback
- Color-coded pieces and layers
- Professional game feel with score tracking
- Authentic Atari aesthetic

## How to Run

```bash
python3 atari_3d_tictactoe.py
```

**Requirements:**
- Python 3.6+
- tkinter (usually included with Python)

## Game Rules

1. The game is played on a 4×4×4 cube (4 layers of 4×4 grids)
2. Players take turns placing their piece (X or O)
3. **Win by getting 4 in a row** in any direction:
   - Horizontal row on a layer
   - Vertical column on a layer
   - Diagonal on a layer
   - Straight line through layers
   - Diagonal through layers
   - 3D diagonal (corner to corner)

## Controls

- **Click** any empty cell to place your piece
- **New Game** button to start fresh
- **Radio buttons** to change settings (piece, first move, difficulty)
- **Hover** over cells to see placement preview

## Features Inspired by Original Atari Game

1. **4×4×4 Grid Structure**: Same as the 1979 Atari release
2. **Layer-Based Visualization**: All 4 layers visible simultaneously
3. **Color Scheme**: Bright colors on dark background (classic arcade)
4. **Clean Grid Lines**: Bold cyan grid reminiscent of vector graphics
5. **Immediate Visual Feedback**: See results instantly
6. **Score Tracking**: Keep track of wins across multiple games

## AI Strategy

The computer opponent uses:
- **Minimax algorithm** for optimal move selection
- **Alpha-beta pruning** to reduce search space
- **Board evaluation** based on potential winning paths
- **Immediate win detection** for quick victories
- **Blocking logic** to prevent human wins

## Technical Specifications

- **Board Size**: 4×4×4 (64 total cells)
- **Winning Combinations**: 76 unique ways to win
- **Cell Size**: 60×60 pixels
- **Total Window Size**: ~700×700 pixels
- **Animation Speed**: ~20ms per frame
- **AI Search Depth**: 1-4 levels (based on difficulty)

## Credits

Enhanced version created as a modern recreation of the classic **Atari 3D Tic-Tac-Toe** game released in 1979 for the Atari 2600/5200 systems.

Improvements over reference implementation at: https://github.com/sairghan/3D-Tic-Tac-Toe-4x4x4
