#!/usr/bin/env python3
"""
3D Tic-Tac-Toe Game (4x4x4)
Converted from Java to Python with expanded board size
Uses minimax algorithm with alpha-beta pruning for AI

Enhanced with fancy Canvas-based icons for X and O pieces
"""

import tkinter as tk
from tkinter import ttk, Canvas
import random
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class OneMove:
    """Represents a single move on the board"""
    layer: int
    row: int
    column: int


class FancyIcon:
    """Creates fancy Canvas-based icons for X and O pieces"""

    @staticmethod
    def draw_x(canvas: Canvas, size: int = 40):
        """Draw a fancy X with gradient effect"""
        canvas.delete("all")
        padding = size * 0.2

        # Draw shadow for depth
        canvas.create_line(
            padding + 2, padding + 2,
            size - padding + 2, size - padding + 2,
            width=size * 0.15,
            fill='#888888',
            capstyle=tk.ROUND
        )
        canvas.create_line(
            size - padding + 2, padding + 2,
            padding + 2, size - padding + 2,
            width=size * 0.15,
            fill='#888888',
            capstyle=tk.ROUND
        )

        # Draw main X in blue gradient
        canvas.create_line(
            padding, padding,
            size - padding, size - padding,
            width=size * 0.15,
            fill='#2E86DE',
            capstyle=tk.ROUND,
            smooth=True
        )
        canvas.create_line(
            size - padding, padding,
            padding, size - padding,
            width=size * 0.15,
            fill='#54A0FF',
            capstyle=tk.ROUND,
            smooth=True
        )

        # Add highlights
        canvas.create_line(
            padding + 2, padding,
            size - padding - 2, size - padding,
            width=size * 0.05,
            fill='#74B9FF',
            capstyle=tk.ROUND
        )

    @staticmethod
    def draw_o(canvas: Canvas, size: int = 40):
        """Draw a fancy O with gradient effect"""
        canvas.delete("all")
        padding = size * 0.2

        # Draw shadow for depth
        canvas.create_oval(
            padding + 2, padding + 2,
            size - padding + 2, size - padding + 2,
            outline='#888888',
            width=size * 0.15
        )

        # Draw outer circle in red gradient
        canvas.create_oval(
            padding, padding,
            size - padding, size - padding,
            outline='#EE5A6F',
            width=size * 0.15
        )

        # Draw inner highlight circle
        inner_padding = size * 0.25
        canvas.create_oval(
            inner_padding, inner_padding,
            size - inner_padding, size - inner_padding,
            outline='#FF6B81',
            width=size * 0.08
        )

        # Add highlight arc for 3D effect
        canvas.create_arc(
            padding + 2, padding + 2,
            size - padding - 2, size - padding - 2,
            start=120,
            extent=60,
            outline='#FF9FF3',
            width=size * 0.05,
            style=tk.ARC
        )

    @staticmethod
    def draw_x_win(canvas: Canvas, size: int = 40):
        """Draw a fancy X in winning color (gold)"""
        canvas.delete("all")
        padding = size * 0.2

        # Draw shadow
        canvas.create_line(
            padding + 2, padding + 2,
            size - padding + 2, size - padding + 2,
            width=size * 0.18,
            fill='#DAA520',
            capstyle=tk.ROUND
        )
        canvas.create_line(
            size - padding + 2, padding + 2,
            padding + 2, size - padding + 2,
            width=size * 0.18,
            fill='#DAA520',
            capstyle=tk.ROUND
        )

        # Draw main X in gold
        canvas.create_line(
            padding, padding,
            size - padding, size - padding,
            width=size * 0.15,
            fill='#FFD700',
            capstyle=tk.ROUND
        )
        canvas.create_line(
            size - padding, padding,
            padding, size - padding,
            width=size * 0.15,
            fill='#FFD700',
            capstyle=tk.ROUND
        )

    @staticmethod
    def draw_o_win(canvas: Canvas, size: int = 40):
        """Draw a fancy O in winning color (gold)"""
        canvas.delete("all")
        padding = size * 0.2

        # Draw shadow
        canvas.create_oval(
            padding + 2, padding + 2,
            size - padding + 2, size - padding + 2,
            outline='#DAA520',
            width=size * 0.18
        )

        # Draw main O in gold
        canvas.create_oval(
            padding, padding,
            size - padding, size - padding,
            outline='#FFD700',
            width=size * 0.15
        )


class TTT3D:
    """Main game class for 3D Tic-Tac-Toe"""

    def __init__(self):
        # Game configuration
        self.BOARD_SIZE = 3  # 3x3x3 board
        self.LAYERS = 3
        self.WIN_LENGTH = 3  # Need 3 in a row to win

        # Game state
        self.config = [[[-1 for _ in range(self.BOARD_SIZE)]
                       for _ in range(self.BOARD_SIZE)]
                      for _ in range(self.LAYERS)]
        self.board_buttons = [[[None for _ in range(self.BOARD_SIZE)]
                               for _ in range(self.BOARD_SIZE)]
                              for _ in range(self.LAYERS)]
        self.board_canvases = [[[None for _ in range(self.BOARD_SIZE)]
                                for _ in range(self.BOARD_SIZE)]
                               for _ in range(self.LAYERS)]

        # Game settings
        self.human_first = True
        self.human_piece = 'X'
        self.computer_piece = 'O'
        self.difficulty = 2  # 1=Easy, 2=Medium, 3=Hard
        self.total_looks_ahead = 2
        self.look_ahead_counter = 0

        # Score tracking
        self.human_score = 0
        self.computer_score = 0
        self.win = False
        self.final_win = []
        self.final_win_buttons = []

        # Calculate all winning combinations for 4x4x4
        self.winning_combinations = self._generate_winning_combinations()

        # Create GUI
        self.root = tk.Tk()
        self.root.title("3D Tic-Tac-Toe (3x3x3)")
        self.root.geometry("650x500")
        self.root.resizable(False, False)

        self.setup_gui()

    def _generate_winning_combinations(self) -> List[List[int]]:
        """Generate all possible winning combinations for 3x3x3 board"""
        wins = []

        # Helper function to convert 3D coordinates to 1D index
        def coord_to_index(layer, row, col):
            return layer * 9 + row * 3 + col

        # 1. Rows on each layer
        for layer in range(3):
            for row in range(3):
                wins.append([coord_to_index(layer, row, col) for col in range(3)])

        # 2. Columns on each layer
        for layer in range(3):
            for col in range(3):
                wins.append([coord_to_index(layer, row, col) for row in range(3)])

        # 3. Diagonals on each layer
        for layer in range(3):
            # Main diagonal
            wins.append([coord_to_index(layer, i, i) for i in range(3)])
            # Anti-diagonal
            wins.append([coord_to_index(layer, i, 2-i) for i in range(3)])

        # 4. Vertical lines through layers
        for row in range(3):
            for col in range(3):
                wins.append([coord_to_index(layer, row, col) for layer in range(3)])

        # 5. Diagonal lines through layers (in vertical planes)
        # Front-to-back diagonals
        for col in range(3):
            # Descending
            wins.append([coord_to_index(i, i, col) for i in range(3)])
            # Ascending
            wins.append([coord_to_index(i, 2-i, col) for i in range(3)])

        # Left-to-right diagonals
        for row in range(3):
            # Descending
            wins.append([coord_to_index(i, row, i) for i in range(3)])
            # Ascending
            wins.append([coord_to_index(i, row, 2-i) for i in range(3)])

        # 6. Space diagonals (corner to corner)
        # Main space diagonals
        wins.append([coord_to_index(i, i, i) for i in range(3)])  # (0,0,0) to (2,2,2)
        wins.append([coord_to_index(i, i, 2-i) for i in range(3)])  # (0,0,2) to (2,2,0)
        wins.append([coord_to_index(i, 2-i, i) for i in range(3)])  # (0,2,0) to (2,0,2)
        wins.append([coord_to_index(i, 2-i, 2-i) for i in range(3)])  # (0,2,2) to (2,0,0)

        return wins

    def setup_gui(self):
        """Create the GUI layout"""
        # Top frame for title and score
        top_frame = tk.Frame(self.root, bg='white')
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        self.status_label = tk.Label(
            top_frame,
            text="Welcome to 3D Tic-Tac-Toe!",
            font=('Tahoma', 12),
            bg='white'
        )
        self.status_label.pack()

        self.score_label = tk.Label(
            top_frame,
            text=f"You: {self.human_score}   Me: {self.computer_score}",
            font=('Tahoma', 15, 'bold'),
            bg='white'
        )
        self.score_label.pack()

        # Main container
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left side - Game boards
        board_frame = tk.Frame(main_container)
        board_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create 3 layers of 3x3 boards
        for layer in range(3):
            layer_frame = tk.LabelFrame(
                board_frame,
                text=f"Layer {layer + 1}",
                font=('Tahoma', 10, 'bold'),
                padx=5,
                pady=5,
                bg='#f0f0f0'
            )
            layer_frame.grid(row=0, column=layer, padx=5, pady=5)

            # Create 3x3 grid for this layer
            for row in range(3):
                for col in range(3):
                    # Create a frame to hold the canvas
                    cell_frame = tk.Frame(layer_frame, bg='white', relief=tk.RAISED, bd=2)
                    cell_frame.grid(row=row, column=col, padx=2, pady=2)

                    # Create canvas for drawing fancy icons
                    canvas = Canvas(
                        cell_frame,
                        width=45,
                        height=45,
                        bg='white',
                        highlightthickness=1,
                        highlightbackground='#cccccc',
                        cursor='hand2'
                    )
                    canvas.pack()
                    self.board_canvases[layer][row][col] = canvas

                    # Bind click event directly to canvas
                    canvas.bind('<Button-1>', lambda event, l=layer, r=row, c=col: self.human_move(l, r, c))

                    # Store canvas reference in board_buttons for compatibility
                    self.board_buttons[layer][row][col] = canvas

        # Right side - Controls
        control_frame = tk.Frame(main_container, width=200)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        # New Game button
        tk.Button(
            control_frame,
            text="New Game",
            font=('Tahoma', 12),
            command=self.new_game,
            bg='lightblue',
            width=15
        ).pack(pady=10)

        # Piece selection
        piece_frame = tk.LabelFrame(control_frame, text="Your Piece", font=('Tahoma', 10))
        piece_frame.pack(fill=tk.X, pady=5)

        self.piece_var = tk.StringVar(value='X')
        tk.Radiobutton(
            piece_frame,
            text="X",
            variable=self.piece_var,
            value='X',
            command=self.change_piece
        ).pack(anchor=tk.W)
        tk.Radiobutton(
            piece_frame,
            text="O",
            variable=self.piece_var,
            value='O',
            command=self.change_piece
        ).pack(anchor=tk.W)

        # First move selection
        first_frame = tk.LabelFrame(control_frame, text="First Move", font=('Tahoma', 10))
        first_frame.pack(fill=tk.X, pady=5)

        self.first_var = tk.StringVar(value='Human')
        tk.Radiobutton(
            first_frame,
            text="Human First",
            variable=self.first_var,
            value='Human',
            command=self.change_first
        ).pack(anchor=tk.W)
        tk.Radiobutton(
            first_frame,
            text="CPU First",
            variable=self.first_var,
            value='CPU',
            command=self.change_first
        ).pack(anchor=tk.W)

        # Difficulty selection
        diff_frame = tk.LabelFrame(control_frame, text="Difficulty", font=('Tahoma', 10))
        diff_frame.pack(fill=tk.X, pady=5)

        self.diff_var = tk.StringVar(value='Medium')
        tk.Radiobutton(
            diff_frame,
            text="Easy",
            variable=self.diff_var,
            value='Easy',
            command=self.change_difficulty
        ).pack(anchor=tk.W)
        tk.Radiobutton(
            diff_frame,
            text="Medium",
            variable=self.diff_var,
            value='Medium',
            command=self.change_difficulty
        ).pack(anchor=tk.W)
        tk.Radiobutton(
            diff_frame,
            text="Hard",
            variable=self.diff_var,
            value='Hard',
            command=self.change_difficulty
        ).pack(anchor=tk.W)

        # Instructions
        instructions = tk.Label(
            control_frame,
            text="Get 3 in a row\nto win!",
            font=('Tahoma', 10),
            justify=tk.CENTER,
            fg='darkblue'
        )
        instructions.pack(pady=20)

    def change_piece(self):
        """Handle piece selection change"""
        self.human_piece = self.piece_var.get()
        self.computer_piece = 'O' if self.human_piece == 'X' else 'X'
        self.clear_board()
        self.status_label.config(text="Good luck!", fg='black')
        if not self.human_first:
            if self.difficulty == 3:
                self.computer_plays()
            else:
                self.computer_play_random()

    def change_first(self):
        """Handle first move selection change"""
        self.human_first = (self.first_var.get() == 'Human')
        self.clear_board()
        self.status_label.config(text="Good luck!", fg='black')
        if not self.human_first:
            if self.difficulty == 3:
                self.computer_plays()
            else:
                self.computer_play_random()

    def change_difficulty(self):
        """Handle difficulty selection change"""
        diff = self.diff_var.get()
        if diff == 'Easy':
            self.difficulty = 1
            self.total_looks_ahead = 1
        elif diff == 'Medium':
            self.difficulty = 2
            self.total_looks_ahead = 2
        else:  # Hard
            self.difficulty = 3
            self.total_looks_ahead = 6  # Full depth for 3x3x3 board

        self.clear_board()
        self.status_label.config(text="Good luck!", fg='black')
        if not self.human_first:
            if self.difficulty == 3:
                self.computer_plays()
            else:
                self.computer_play_random()

    def new_game(self):
        """Start a new game"""
        self.clear_board()
        self.status_label.config(text="Good luck!", fg='black')
        if not self.human_first:
            if self.difficulty == 3:
                self.computer_plays()
            else:
                self.computer_play_random()

    def clear_board(self):
        """Reset the game board"""
        self.win = False
        self.look_ahead_counter = 0
        self.final_win = []
        self.final_win_buttons = []

        for layer in range(3):
            for row in range(3):
                for col in range(3):
                    self.config[layer][row][col] = -1
                    # Clear the canvas
                    canvas = self.board_canvases[layer][row][col]
                    canvas.delete("all")
                    canvas.config(bg='white', cursor='hand2')

    def human_move(self, layer: int, row: int, col: int):
        """Handle human player move"""
        if self.config[layer][row][col] != -1 or self.win:
            return

        # Make the move
        self.config[layer][row][col] = 0 if self.human_piece == 'X' else 1

        # Draw fancy icon
        canvas = self.board_canvases[layer][row][col]
        canvas.config(bg='#f5f5f5', cursor='')
        if self.human_piece == 'X':
            FancyIcon.draw_x(canvas, 45)
        else:
            FancyIcon.draw_o(canvas, 45)

        # Check for win
        move = OneMove(layer, row, col)
        if self.check_win(0 if self.human_piece == 'X' else 1, move):
            self.status_label.config(
                text="You beat me! Press New Game to play again.",
                fg='red'
            )
            self.human_score += 1
            self.win = True
            self.disable_board()
            self.update_score()
        else:
            # Computer's turn
            self.root.after(100, self.computer_plays)

    def computer_play_random(self):
        """Computer makes a random move (used for easier difficulties when going first)"""
        empty_spaces = []
        for layer in range(3):
            for row in range(3):
                for col in range(3):
                    if self.config[layer][row][col] == -1:
                        empty_spaces.append((layer, row, col))

        if empty_spaces:
            layer, row, col = random.choice(empty_spaces)
            piece_value = 1 if self.computer_piece == 'X' else 0
            self.config[layer][row][col] = piece_value

            # Draw fancy icon
            canvas = self.board_canvases[layer][row][col]
            canvas.config(bg='#f5f5f5', cursor='')
            if self.computer_piece == 'X':
                FancyIcon.draw_x(canvas, 45)
            else:
                FancyIcon.draw_o(canvas, 45)

    def computer_plays(self):
        """Computer makes a move using minimax algorithm"""
        best_score = -10000
        best_move = None
        computer_value = 1 if self.computer_piece == 'X' else 0

        # Check all possible moves
        for layer in range(3):
            for row in range(3):
                for col in range(3):
                    if self.config[layer][row][col] == -1:
                        # Try this move
                        move = OneMove(layer, row, col)

                        # Check if this move wins immediately
                        if self.check_win(computer_value, move):
                            # Make the winning move
                            self.config[layer][row][col] = computer_value

                            # Draw fancy icon
                            canvas = self.board_canvases[layer][row][col]
                            canvas.config(bg='#f5f5f5', cursor='')
                            if self.computer_piece == 'X':
                                FancyIcon.draw_x(canvas, 45)
                            else:
                                FancyIcon.draw_o(canvas, 45)

                            self.status_label.config(
                                text="I win! Press New Game to play again.",
                                fg='red'
                            )
                            self.win = True
                            self.computer_score += 1
                            self.disable_board()
                            self.update_score()
                            return

                        # Evaluate this move
                        self.config[layer][row][col] = computer_value

                        if self.difficulty != 1:
                            h_value = self.look_ahead(
                                0 if self.human_piece == 'X' else 1,
                                -10000,
                                10000
                            )
                        else:
                            h_value = self.heuristic()

                        self.look_ahead_counter = 0

                        # Track best move
                        if h_value >= best_score:
                            best_score = h_value
                            best_move = (layer, row, col)

                        # Undo the move
                        self.config[layer][row][col] = -1

        # Make the best move
        if best_move and not self.win:
            layer, row, col = best_move
            computer_value = 1 if self.computer_piece == 'X' else 0
            self.config[layer][row][col] = computer_value

            # Draw fancy icon
            canvas = self.board_canvases[layer][row][col]
            canvas.config(bg='#f5f5f5', cursor='')
            if self.computer_piece == 'X':
                FancyIcon.draw_x(canvas, 45)
            else:
                FancyIcon.draw_o(canvas, 45)

    def look_ahead(self, player_value: int, alpha: int, beta: int) -> int:
        """Minimax algorithm with alpha-beta pruning"""
        if self.look_ahead_counter >= self.total_looks_ahead:
            return self.heuristic()

        self.look_ahead_counter += 1
        computer_value = 1 if self.computer_piece == 'X' else 0

        if player_value == computer_value:
            # Computer's turn (maximizing)
            for layer in range(3):
                for row in range(3):
                    for col in range(3):
                        if self.config[layer][row][col] == -1:
                            move = OneMove(layer, row, col)

                            if self.check_win(computer_value, move):
                                self.config[layer][row][col] = -1
                                return 1000

                            h_value = self.look_ahead(
                                0 if self.human_piece == 'X' else 1,
                                alpha,
                                beta
                            )

                            if h_value > alpha:
                                alpha = h_value

                            self.config[layer][row][col] = -1

                            if alpha >= beta:
                                return alpha

            return alpha
        else:
            # Human's turn (minimizing)
            for layer in range(3):
                for row in range(3):
                    for col in range(3):
                        if self.config[layer][row][col] == -1:
                            move = OneMove(layer, row, col)

                            if self.check_win(player_value, move):
                                self.config[layer][row][col] = -1
                                return -1000

                            h_value = self.look_ahead(computer_value, alpha, beta)

                            if h_value < beta:
                                beta = h_value

                            self.config[layer][row][col] = -1

                            if alpha >= beta:
                                return beta

            return beta

    def heuristic(self) -> int:
        """Calculate heuristic value of current board state"""
        computer_value = 1 if self.computer_piece == 'X' else 0
        human_value = 0 if self.human_piece == 'X' else 1

        return self.check_available(computer_value) - self.check_available(human_value)

    def check_win(self, player_value: int, move: OneMove) -> bool:
        """Check if the given move creates a winning condition"""
        # Temporarily place the piece
        original = self.config[move.layer][move.row][move.column]
        self.config[move.layer][move.row][move.column] = player_value

        # Create game board array
        game_board = [0] * 27
        index = 0
        for layer in range(3):
            for row in range(3):
                for col in range(3):
                    if self.config[layer][row][col] == player_value:
                        game_board[index] = 1
                    index += 1

        # Check all winning combinations
        for win_combo in self.winning_combinations:
            if all(game_board[pos] == 1 for pos in win_combo):
                self.final_win = win_combo
                # Restore original value
                if original != player_value:
                    self.config[move.layer][move.row][move.column] = original
                return True

        # Restore original value
        self.config[move.layer][move.row][move.column] = original
        return False

    def check_available(self, player_value: int) -> int:
        """Count available winning paths for the given player"""
        win_counter = 0

        # Create game board array
        game_board = [0] * 27
        index = 0
        for layer in range(3):
            for row in range(3):
                for col in range(3):
                    if (self.config[layer][row][col] == player_value or
                        self.config[layer][row][col] == -1):
                        game_board[index] = 1
                    index += 1

        # Check all winning combinations
        for win_combo in self.winning_combinations:
            if all(game_board[pos] == 1 for pos in win_combo):
                win_counter += 1

        return win_counter

    def disable_board(self):
        """Disable board after game ends and highlight winning combination"""
        if self.final_win:
            # Convert winning indices to button coordinates
            self.final_win_buttons = []
            for idx in self.final_win:
                layer = idx // 9
                remainder = idx % 9
                row = remainder // 3
                col = remainder % 3
                self.final_win_buttons.append((layer, row, col))

        # Disable all canvases and redraw winning pieces in gold
        for layer in range(3):
            for row in range(3):
                for col in range(3):
                    canvas = self.board_canvases[layer][row][col]
                    canvas.config(cursor='')

                    # Redraw winning pieces in gold
                    if (layer, row, col) in self.final_win_buttons:
                        piece_value = self.config[layer][row][col]
                        if piece_value == 0:  # X
                            FancyIcon.draw_x_win(canvas, 45)
                        elif piece_value == 1:  # O
                            FancyIcon.draw_o_win(canvas, 45)

    def update_score(self):
        """Update the score display"""
        self.score_label.config(
            text=f"You: {self.human_score}   Me: {self.computer_score}"
        )

    def run(self):
        """Start the GUI event loop"""
        self.root.mainloop()


if __name__ == "__main__":
    game = TTT3D()
    game.run()
