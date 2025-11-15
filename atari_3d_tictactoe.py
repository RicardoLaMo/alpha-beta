#!/usr/bin/env python3
"""
Atari-Style 3D Tic-Tac-Toe Game (4x4x4)
Enhanced GUI inspired by the classic Atari game with modern improvements
Uses minimax algorithm with alpha-beta pruning for challenging AI
"""

import tkinter as tk
from tkinter import Canvas, font
import random
import math
from typing import List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Move:
    """Represents a single move on the board"""
    layer: int
    row: int
    col: int


class AtariTicTacToe3D:
    """Main game class for Atari-style 3D Tic-Tac-Toe"""

    def __init__(self):
        # Game configuration
        self.BOARD_SIZE = 4  # 4x4x4 board
        self.LAYERS = 4
        self.WIN_LENGTH = 4

        # Visual configuration
        self.CELL_SIZE = 40  # Size for isometric cells
        self.CELL_PADDING = 2
        self.ISO_ANGLE = 30  # Isometric angle in degrees
        self.LAYER_SPACING = 15  # Vertical spacing between layers

        # Atari-inspired color scheme
        self.BG_COLOR = '#1a1a2e'  # Dark blue-black
        self.LAYER_COLORS = ['#0f3460', '#16213e', '#1e3a5f', '#2d4a7c']  # Gradient blues
        self.CELL_OUTLINE = '#2a4a6c'  # Subtle cell outline
        self.GRID_COLOR = '#4ecca3'  # Bright cyan for grid
        self.X_COLOR = '#ee6c4d'  # Bright orange-red
        self.O_COLOR = '#4ecca3'  # Bright cyan
        self.HIGHLIGHT_COLOR = '#ffd700'  # Gold for wins
        self.HOVER_COLOR = '#555555'  # Gray hover (tkinter doesn't support alpha in hex colors)

        # Game state
        self.board = [[[-1 for _ in range(self.BOARD_SIZE)]
                       for _ in range(self.BOARD_SIZE)]
                      for _ in range(self.LAYERS)]

        # UI elements
        self.layer_canvases = []
        self.cell_items = [[[None for _ in range(self.BOARD_SIZE)]
                           for _ in range(self.BOARD_SIZE)]
                          for _ in range(self.LAYERS)]

        # Game settings
        self.human_first = True
        self.human_piece = 'X'  # X = 0, O = 1
        self.computer_piece = 'O'
        self.difficulty = 2  # 1=Easy, 2=Medium, 3=Hard
        self.max_depth = 3

        # Score tracking
        self.human_score = 0
        self.computer_score = 0
        self.tie_score = 0
        self.game_over = False
        self.winning_cells = []

        # Animation state
        self.animation_queue = []
        self.is_animating = False

        # Calculate winning combinations
        self.winning_combinations = self._generate_winning_combinations()

        # Create GUI
        self.root = tk.Tk()
        self.root.title("Atari 3D Tic-Tac-Toe (4×4×4)")
        self.root.configure(bg=self.BG_COLOR)
        self.root.resizable(False, False)

        self.setup_gui()

    def _generate_winning_combinations(self) -> List[List[Tuple[int, int, int]]]:
        """Generate all possible winning combinations for 4x4x4 board"""
        wins = []

        # 1. Rows on each layer
        for layer in range(4):
            for row in range(4):
                wins.append([(layer, row, col) for col in range(4)])

        # 2. Columns on each layer
        for layer in range(4):
            for col in range(4):
                wins.append([(layer, row, col) for row in range(4)])

        # 3. Diagonals on each layer
        for layer in range(4):
            wins.append([(layer, i, i) for i in range(4)])
            wins.append([(layer, i, 3-i) for i in range(4)])

        # 4. Vertical lines through layers
        for row in range(4):
            for col in range(4):
                wins.append([(layer, row, col) for layer in range(4)])

        # 5. Diagonal lines through layers
        for col in range(4):
            wins.append([(i, i, col) for i in range(4)])
            wins.append([(i, 3-i, col) for i in range(4)])

        for row in range(4):
            wins.append([(i, row, i) for i in range(4)])
            wins.append([(i, row, 3-i) for i in range(4)])

        # 6. Space diagonals (corner to corner)
        wins.append([(i, i, i) for i in range(4)])
        wins.append([(i, i, 3-i) for i in range(4)])
        wins.append([(i, 3-i, i) for i in range(4)])
        wins.append([(i, 3-i, 3-i) for i in range(4)])

        return wins

    def setup_gui(self):
        """Create the Atari-style GUI"""
        # Main container
        main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        main_frame.pack(padx=20, pady=20)

        # Title with retro font
        title_font = font.Font(family='Courier', size=24, weight='bold')
        title = tk.Label(
            main_frame,
            text="ATARI 3D TIC-TAC-TOE",
            font=title_font,
            bg=self.BG_COLOR,
            fg=self.GRID_COLOR
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Score display
        score_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        score_frame.grid(row=1, column=0, columnspan=2, pady=(0, 15))

        score_font = font.Font(family='Courier', size=14, weight='bold')
        self.score_label = tk.Label(
            score_frame,
            text=f"YOU: {self.human_score}  |  CPU: {self.computer_score}  |  TIES: {self.tie_score}",
            font=score_font,
            bg=self.BG_COLOR,
            fg='#ffffff'
        )
        self.score_label.pack()

        # Status message
        status_font = font.Font(family='Courier', size=12)
        self.status_label = tk.Label(
            score_frame,
            text="Click any cell to start!",
            font=status_font,
            bg=self.BG_COLOR,
            fg=self.X_COLOR
        )
        self.status_label.pack(pady=(5, 0))

        # Game boards container
        boards_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        boards_frame.grid(row=2, column=0, padx=(0, 20))

        # Create single isometric 3D view of all layers
        self.create_isometric_board(boards_frame)

        # Control panel
        control_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        control_frame.grid(row=2, column=1, sticky='n')

        self.create_controls(control_frame)

    def create_isometric_board(self, parent):
        """Create a single canvas with isometric 3D stacked layers"""
        # Calculate canvas size for isometric view
        canvas_width = 500
        canvas_height = 650

        main_canvas_frame = tk.Frame(parent, bg=self.BG_COLOR, relief=tk.RAISED, bd=3)
        main_canvas_frame.pack(padx=5, pady=5)

        # Create single canvas for all layers
        self.main_canvas = Canvas(
            main_canvas_frame,
            width=canvas_width,
            height=canvas_height,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.main_canvas.pack(padx=5, pady=5)

        # Store layer canvases list for compatibility (now just references the main canvas)
        self.layer_canvases = [self.main_canvas] * 4

        # Store cell coordinates for click detection
        self.cell_coords = {}

        # Draw all layers
        self.draw_all_layers()

        # Bind events to main canvas
        self.main_canvas.bind('<Button-1>', self.on_iso_click)
        self.main_canvas.bind('<Motion>', self.on_iso_mouse_move)
        self.main_canvas.bind('<Leave>', self.on_iso_mouse_leave)

    def get_iso_coords(self, layer, row, col):
        """Convert grid coordinates to isometric canvas coordinates"""
        # Base position for each layer (stacking from top to bottom)
        base_x = 180
        base_y = 50 + layer * 145  # Stack layers vertically with spacing

        # Isometric projection
        # For isometric view: x goes right, y goes down-right
        iso_x = col * (self.CELL_SIZE * 0.8) + row * 8
        iso_y = row * (self.CELL_SIZE * 0.4) + col * 4

        return base_x + iso_x, base_y + iso_y

    def draw_iso_cell(self, layer, row, col, tags='cell'):
        """Draw a single isometric cell with 3D depth"""
        # Get corner coordinates
        x, y = self.get_iso_coords(layer, row, col)

        # Cell dimensions
        w = self.CELL_SIZE * 0.8  # Width (horizontal)
        h = self.CELL_SIZE * 0.4  # Height (vertical)
        depth = 8  # Depth offset for 3D effect

        # Top face of the cell (parallelogram)
        top_face = [
            x, y,                    # Top left
            x + w, y,                # Top right
            x + w + depth, y + depth,  # Bottom right
            x + depth, y + depth,    # Bottom left
        ]

        # Draw the top face
        cell_color = self.LAYER_COLORS[layer]
        outline_color = self.CELL_OUTLINE

        # Draw top face
        cell_id = self.main_canvas.create_polygon(
            top_face,
            fill=cell_color,
            outline=outline_color,
            width=1,
            tags=(tags, f'layer{layer}', f'cell_{layer}_{row}_{col}', 'top_face')
        )

        # Draw right side face (if not last column)
        if col < 3 or row < 3:
            right_face = [
                x + w, y,
                x + w + depth, y + depth,
                x + w + depth, y + depth + h,
                x + w, y + h,
            ]
            self.main_canvas.create_polygon(
                right_face,
                fill=self.LAYER_COLORS[min(layer, 3)],
                outline=outline_color,
                width=1,
                tags=(tags, f'layer{layer}', f'cell_{layer}_{row}_{col}', 'side_face')
            )

        # Draw bottom side face
        if row < 3:
            bottom_face = [
                x + depth, y + depth,
                x + w + depth, y + depth,
                x + w + depth, y + depth + h,
                x + depth, y + depth + h,
            ]
            self.main_canvas.create_polygon(
                bottom_face,
                fill=self.LAYER_COLORS[min(layer, 3)],
                outline=outline_color,
                width=1,
                tags=(tags, f'layer{layer}', f'cell_{layer}_{row}_{col}', 'bottom_face')
            )

        # Store coordinates for click detection (use top face)
        self.cell_coords[(layer, row, col)] = (x, y, w, h, top_face)

        return cell_id

    def draw_layer_outline(self, layer):
        """Draw the outline/frame of a layer"""
        # Draw connecting lines between layers
        if layer < 3:  # Don't draw for bottom layer
            # Draw vertical connection lines at corners
            for row, col in [(0, 0), (0, 3), (3, 0), (3, 3)]:
                x1, y1 = self.get_iso_coords(layer, row, col)
                x2, y2 = self.get_iso_coords(layer + 1, row, col)

                self.main_canvas.create_line(
                    x1, y1, x2, y2,
                    fill=self.CELL_OUTLINE,
                    width=2,
                    tags=('layer_connection', f'layer{layer}')
                )

    def draw_all_layers(self):
        """Draw all 4 layers in isometric view"""
        # Draw from top layer to bottom for proper layering
        for layer in range(4):
            # Draw layer connections first
            self.draw_layer_outline(layer)

            # Draw all cells in this layer
            for row in range(4):
                for col in range(4):
                    self.draw_iso_cell(layer, row, col)

            # Add layer label
            base_x = 180
            base_y = 50 + layer * 145
            self.main_canvas.create_text(
                base_x - 80, base_y + 50,
                text=f"L{layer + 1}",
                fill=self.GRID_COLOR,
                font=('Courier', 12, 'bold'),
                tags='layer_label'
            )

    def create_layer_board(self, parent, layer: int, grid_row: int, grid_col: int):
        """Create a single layer board with Atari styling"""
        layer_frame = tk.Frame(
            parent,
            bg=self.LAYER_COLORS[layer],
            relief=tk.RAISED,
            bd=3
        )
        layer_frame.grid(row=grid_row, column=grid_col, padx=8, pady=8)

        # Layer label
        label_font = font.Font(family='Courier', size=11, weight='bold')
        label = tk.Label(
            layer_frame,
            text=f"LAYER {layer + 1}",
            font=label_font,
            bg=self.LAYER_COLORS[layer],
            fg=self.GRID_COLOR
        )
        label.pack(pady=(5, 3))

        # Create canvas for this layer
        canvas_size = (self.CELL_SIZE * 4) + (self.CELL_PADDING * 5)
        canvas = Canvas(
            layer_frame,
            width=canvas_size,
            height=canvas_size,
            bg=self.LAYER_COLORS[layer],
            highlightthickness=0
        )
        canvas.pack(padx=5, pady=(0, 5))
        self.layer_canvases.append(canvas)

        # Draw cell backgrounds
        self.draw_grid(canvas, layer)

        # Bind click events
        canvas.bind('<Button-1>', lambda e, l=layer: self.on_cell_click(e, l))
        canvas.bind('<Motion>', lambda e, l=layer: self.on_mouse_move(e, l))
        canvas.bind('<Leave>', lambda e, l=layer: self.on_mouse_leave(e, l))

    def draw_grid(self, canvas: Canvas, layer: int):
        """Draw cell outlines for visual separation (no grid lines)"""
        # Draw individual cell rectangles with subtle borders
        for row in range(4):
            for col in range(4):
                x1, y1, x2, y2 = self.get_cell_coords(row, col)
                # Draw cell background with subtle outline
                canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline=self.CELL_OUTLINE,
                    fill=self.LAYER_COLORS[layer],
                    width=1,
                    tags='cell_border'
                )

    def create_controls(self, parent):
        """Create the control panel"""
        button_font = font.Font(family='Courier', size=10, weight='bold')
        label_font = font.Font(family='Courier', size=9)

        # New Game button
        tk.Button(
            parent,
            text="NEW GAME",
            font=button_font,
            command=self.new_game,
            bg=self.GRID_COLOR,
            fg=self.BG_COLOR,
            activebackground=self.X_COLOR,
            width=15,
            height=2
        ).pack(pady=(0, 15))

        # Player piece selection
        piece_frame = tk.LabelFrame(
            parent,
            text="YOUR PIECE",
            font=label_font,
            bg=self.BG_COLOR,
            fg=self.GRID_COLOR,
            bd=2
        )
        piece_frame.pack(fill=tk.X, pady=(0, 10))

        self.piece_var = tk.StringVar(value='X')
        for piece in ['X', 'O']:
            color = self.X_COLOR if piece == 'X' else self.O_COLOR
            tk.Radiobutton(
                piece_frame,
                text=piece,
                variable=self.piece_var,
                value=piece,
                command=self.on_settings_change,
                bg=self.BG_COLOR,
                fg=color,
                selectcolor=self.LAYER_COLORS[2],
                font=button_font,
                activebackground=self.BG_COLOR,
                activeforeground=color
            ).pack(anchor=tk.W, padx=10, pady=2)

        # First move selection
        first_frame = tk.LabelFrame(
            parent,
            text="FIRST MOVE",
            font=label_font,
            bg=self.BG_COLOR,
            fg=self.GRID_COLOR,
            bd=2
        )
        first_frame.pack(fill=tk.X, pady=(0, 10))

        self.first_var = tk.StringVar(value='Human')
        for option in ['Human', 'Computer']:
            tk.Radiobutton(
                first_frame,
                text=option.upper(),
                variable=self.first_var,
                value=option,
                command=self.on_settings_change,
                bg=self.BG_COLOR,
                fg='#ffffff',
                selectcolor=self.LAYER_COLORS[2],
                font=label_font,
                activebackground=self.BG_COLOR
            ).pack(anchor=tk.W, padx=10, pady=2)

        # Difficulty selection
        diff_frame = tk.LabelFrame(
            parent,
            text="DIFFICULTY",
            font=label_font,
            bg=self.BG_COLOR,
            fg=self.GRID_COLOR,
            bd=2
        )
        diff_frame.pack(fill=tk.X, pady=(0, 10))

        self.diff_var = tk.StringVar(value='Medium')
        for diff in ['Easy', 'Medium', 'Hard']:
            tk.Radiobutton(
                diff_frame,
                text=diff.upper(),
                variable=self.diff_var,
                value=diff,
                command=self.on_difficulty_change,
                bg=self.BG_COLOR,
                fg='#ffffff',
                selectcolor=self.LAYER_COLORS[2],
                font=label_font,
                activebackground=self.BG_COLOR
            ).pack(anchor=tk.W, padx=10, pady=2)

        # Instructions
        instructions = tk.Label(
            parent,
            text="\nGet 4 in a row\nto WIN!\n\nRows, columns,\ndiagonals, or\nthrough layers!",
            font=label_font,
            bg=self.BG_COLOR,
            fg='#aaaaaa',
            justify=tk.LEFT
        )
        instructions.pack(pady=(20, 0))

    def get_cell_coords(self, row: int, col: int) -> Tuple[int, int, int, int]:
        """Get canvas coordinates for a cell (legacy support)"""
        x1 = self.CELL_PADDING + col * (self.CELL_SIZE + self.CELL_PADDING)
        y1 = self.CELL_PADDING + row * (self.CELL_SIZE + self.CELL_PADDING)
        x2 = x1 + self.CELL_SIZE
        y2 = y1 + self.CELL_SIZE
        return x1, y1, x2, y2

    def get_cell_from_pos(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """Get cell row and column from canvas position (legacy support)"""
        for row in range(4):
            for col in range(4):
                x1, y1, x2, y2 = self.get_cell_coords(row, col)
                if x1 <= x <= x2 and y1 <= y <= y2:
                    return row, col
        return None

    def point_in_parallelogram(self, px, py, points):
        """Check if point (px, py) is inside parallelogram defined by points"""
        # Use cross product method to check if point is inside polygon
        def sign(p1x, p1y, p2x, p2y, p3x, p3y):
            return (p1x - p3x) * (p2y - p3y) - (p2x - p3x) * (p1y - p3y)

        # Convert flat list to coordinate pairs
        coords = [(points[i], points[i+1]) for i in range(0, len(points), 2)]

        # Check if point is on same side of all edges
        num_vertices = len(coords)
        has_neg = False
        has_pos = False

        for i in range(num_vertices):
            v1 = coords[i]
            v2 = coords[(i + 1) % num_vertices]

            d = sign(px, py, v1[0], v1[1], v2[0], v2[1])

            if d < 0:
                has_neg = True
            if d > 0:
                has_pos = True

        return not (has_neg and has_pos)

    def get_cell_from_iso_pos(self, x: int, y: int) -> Optional[Tuple[int, int, int]]:
        """Get layer, row, col from isometric canvas position"""
        # Check all cells to find which one contains the click point
        for (layer, row, col), (cx, cy, w, h, points) in self.cell_coords.items():
            if self.point_in_parallelogram(x, y, points):
                return (layer, row, col)
        return None

    def on_iso_click(self, event):
        """Handle click on isometric view"""
        if self.game_over or self.is_animating:
            return

        cell = self.get_cell_from_iso_pos(event.x, event.y)
        if cell is None:
            return

        layer, row, col = cell
        if self.board[layer][row][col] != -1:
            return

        # Make human move
        self.make_move(layer, row, col, is_human=True)

    def on_iso_mouse_move(self, event):
        """Handle mouse hover on isometric view"""
        if self.game_over:
            return

        # Clear previous hover
        self.main_canvas.delete('hover')

        cell = self.get_cell_from_iso_pos(event.x, event.y)
        if cell is not None:
            layer, row, col = cell
            if self.board[layer][row][col] == -1:
                # Draw hover effect
                x, y, w, h, points = self.cell_coords[(layer, row, col)]
                self.main_canvas.create_polygon(
                    points,
                    fill=self.HOVER_COLOR,
                    outline='',
                    tags='hover'
                )

    def on_iso_mouse_leave(self, event):
        """Clear hover effect when mouse leaves canvas"""
        self.main_canvas.delete('hover')

    def draw_x(self, layer: int, row: int, col: int, color: str, animated: bool = True):
        """Draw an X in an isometric cell"""
        # Get center of the isometric cell
        cx, cy = self.get_iso_coords(layer, row, col)

        # Size of the X
        size = self.CELL_SIZE * 0.3

        # Draw X
        self.main_canvas.create_line(
            cx - size, cy - size/2,
            cx + size, cy + size/2,
            fill=color,
            width=4,
            capstyle=tk.ROUND,
            tags=('piece', f'piece_{layer}_{row}_{col}')
        )
        self.main_canvas.create_line(
            cx + size, cy - size/2,
            cx - size, cy + size/2,
            fill=color,
            width=4,
            capstyle=tk.ROUND,
            tags=('piece', f'piece_{layer}_{row}_{col}')
        )

    def draw_o(self, layer: int, row: int, col: int, color: str, animated: bool = True):
        """Draw an O in an isometric cell"""
        # Get center of the isometric cell
        cx, cy = self.get_iso_coords(layer, row, col)

        # Size of the O
        size = self.CELL_SIZE * 0.3

        # Draw O
        self.main_canvas.create_oval(
            cx - size, cy - size/2,
            cx + size, cy + size/2,
            outline=color,
            width=4,
            tags=('piece', f'piece_{layer}_{row}_{col}')
        )

    def animate_x(self, canvas: Canvas, x1: int, y1: int, x2: int, y2: int,
                  padding: int, color: str, step: int = 0):
        """Animate drawing an X"""
        steps = 10
        if step <= steps:
            progress = step / steps

            # Clear previous animation frame
            canvas.delete('anim_piece')

            # First diagonal
            if progress <= 0.5:
                prog = progress * 2
                canvas.create_line(
                    x1 + padding, y1 + padding,
                    x1 + padding + (x2 - x1 - 2*padding) * prog,
                    y1 + padding + (y2 - y1 - 2*padding) * prog,
                    fill=color,
                    width=6,
                    capstyle=tk.ROUND,
                    tags='anim_piece'
                )
            else:
                # Complete first diagonal
                canvas.create_line(
                    x1 + padding, y1 + padding,
                    x2 - padding, y2 - padding,
                    fill=color,
                    width=6,
                    capstyle=tk.ROUND,
                    tags='anim_piece'
                )
                # Second diagonal
                prog = (progress - 0.5) * 2
                canvas.create_line(
                    x2 - padding, y1 + padding,
                    x2 - padding - (x2 - x1 - 2*padding) * prog,
                    y1 + padding + (y2 - y1 - 2*padding) * prog,
                    fill=color,
                    width=6,
                    capstyle=tk.ROUND,
                    tags='anim_piece'
                )

            self.root.after(20, lambda: self.animate_x(canvas, x1, y1, x2, y2, padding, color, step + 1))
        else:
            # Final frame
            canvas.delete('anim_piece')
            canvas.create_line(
                x1 + padding, y1 + padding,
                x2 - padding, y2 - padding,
                fill=color,
                width=6,
                capstyle=tk.ROUND,
                tags='piece'
            )
            canvas.create_line(
                x2 - padding, y1 + padding,
                x1 + padding, y2 - padding,
                fill=color,
                width=6,
                capstyle=tk.ROUND,
                tags='piece'
            )
            self.is_animating = False

    def animate_o(self, canvas: Canvas, x1: int, y1: int, x2: int, y2: int,
                  padding: int, color: str, step: int = 0):
        """Animate drawing an O"""
        steps = 15
        if step <= steps:
            progress = step / steps
            extent = 360 * progress

            canvas.delete('anim_piece')
            canvas.create_arc(
                x1 + padding, y1 + padding,
                x2 - padding, y2 - padding,
                start=90,
                extent=extent,
                outline=color,
                width=6,
                style=tk.ARC,
                tags='anim_piece'
            )

            self.root.after(20, lambda: self.animate_o(canvas, x1, y1, x2, y2, padding, color, step + 1))
        else:
            # Final frame
            canvas.delete('anim_piece')
            canvas.create_oval(
                x1 + padding, y1 + padding,
                x2 - padding, y2 - padding,
                outline=color,
                width=6,
                tags='piece'
            )
            self.is_animating = False

    def on_cell_click(self, event, layer: int):
        """Handle cell click"""
        if self.game_over or self.is_animating:
            return

        cell = self.get_cell_from_pos(event.x, event.y)
        if cell is None:
            return

        row, col = cell
        if self.board[layer][row][col] != -1:
            return

        # Make human move
        self.make_move(layer, row, col, is_human=True)

    def on_mouse_move(self, event, layer: int):
        """Handle mouse hover effect"""
        if self.game_over:
            return

        cell = self.get_cell_from_pos(event.x, event.y)
        canvas = self.layer_canvases[layer]

        # Clear previous hover
        canvas.delete('hover')

        if cell is not None:
            row, col = cell
            if self.board[layer][row][col] == -1:
                x1, y1, x2, y2 = self.get_cell_coords(row, col)
                canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.HOVER_COLOR,
                    outline='',
                    tags='hover'
                )

    def on_mouse_leave(self, event, layer: int):
        """Clear hover effect when mouse leaves"""
        canvas = self.layer_canvases[layer]
        canvas.delete('hover')

    def make_move(self, layer: int, row: int, col: int, is_human: bool, animated: bool = True):
        """Make a move on the board"""
        if is_human:
            piece = self.human_piece
            piece_value = 0 if piece == 'X' else 1
            color = self.X_COLOR if piece == 'X' else self.O_COLOR
        else:
            piece = self.computer_piece
            piece_value = 0 if piece == 'X' else 1  # Fixed: X=0, O=1
            color = self.X_COLOR if piece == 'X' else self.O_COLOR

        # Update board state
        self.board[layer][row][col] = piece_value

        # Draw piece on isometric board
        if piece == 'X':
            self.draw_x(layer, row, col, color, animated)
        else:
            self.draw_o(layer, row, col, color, animated)

        # Check for win or tie
        move = Move(layer, row, col)
        if self.check_win(piece_value, move):
            self.handle_win(is_human)
        elif self.is_board_full():
            self.handle_tie()
        elif is_human and not self.game_over:
            # Computer's turn
            self.root.after(300 if animated else 0, self.computer_turn)

    def computer_turn(self):
        """Computer makes its move"""
        if self.game_over:
            return

        self.status_label.config(text="Computer is thinking...", fg=self.O_COLOR)
        self.root.update()

        # Find best move using minimax
        best_move = self.find_best_move()

        if best_move:
            layer, row, col = best_move
            self.status_label.config(text="Your turn!", fg=self.X_COLOR)
            self.make_move(layer, row, col, is_human=False)
        else:
            self.handle_tie()

    def find_best_move(self) -> Optional[Tuple[int, int, int]]:
        """Find the best move using minimax with alpha-beta pruning"""
        best_score = -float('inf')
        best_move = None
        computer_value = 0 if self.computer_piece == 'X' else 1  # Fixed: X=0, O=1

        # Get all empty cells
        moves = []
        for layer in range(4):
            for row in range(4):
                for col in range(4):
                    if self.board[layer][row][col] == -1:
                        moves.append((layer, row, col))

        # Shuffle for variety
        random.shuffle(moves)

        # Evaluate each move
        for layer, row, col in moves:
            # Try this move
            self.board[layer][row][col] = computer_value

            # Check if this wins immediately
            move = Move(layer, row, col)
            if self.check_win(computer_value, move):
                self.board[layer][row][col] = -1
                return (layer, row, col)

            # Evaluate using minimax
            if self.difficulty == 1:
                score = random.randint(-100, 100)
            else:
                depth = 2 if self.difficulty == 2 else self.max_depth
                score = self.minimax(depth, -float('inf'), float('inf'), False, computer_value)

            # Undo move
            self.board[layer][row][col] = -1

            if score > best_score:
                best_score = score
                best_move = (layer, row, col)

        return best_move

    def minimax(self, depth: int, alpha: float, beta: float, is_maximizing: bool,
                computer_value: int) -> float:
        """Minimax algorithm with alpha-beta pruning"""
        human_value = 1 - computer_value

        # Check terminal states
        if depth == 0 or self.is_board_full():
            return self.evaluate_board(computer_value)

        if is_maximizing:
            max_score = -float('inf')
            for layer in range(4):
                for row in range(4):
                    for col in range(4):
                        if self.board[layer][row][col] == -1:
                            self.board[layer][row][col] = computer_value

                            move = Move(layer, row, col)
                            if self.check_win(computer_value, move):
                                self.board[layer][row][col] = -1
                                return 1000

                            score = self.minimax(depth - 1, alpha, beta, False, computer_value)
                            self.board[layer][row][col] = -1

                            max_score = max(max_score, score)
                            alpha = max(alpha, score)
                            if beta <= alpha:
                                return max_score
            return max_score
        else:
            min_score = float('inf')
            for layer in range(4):
                for row in range(4):
                    for col in range(4):
                        if self.board[layer][row][col] == -1:
                            self.board[layer][row][col] = human_value

                            move = Move(layer, row, col)
                            if self.check_win(human_value, move):
                                self.board[layer][row][col] = -1
                                return -1000

                            score = self.minimax(depth - 1, alpha, beta, True, computer_value)
                            self.board[layer][row][col] = -1

                            min_score = min(min_score, score)
                            beta = min(beta, score)
                            if beta <= alpha:
                                return min_score
            return min_score

    def evaluate_board(self, computer_value: int) -> float:
        """Evaluate the board position"""
        human_value = 1 - computer_value
        score = 0

        # Count potential wins for each player
        for combo in self.winning_combinations:
            computer_count = 0
            human_count = 0
            empty_count = 0

            for layer, row, col in combo:
                val = self.board[layer][row][col]
                if val == computer_value:
                    computer_count += 1
                elif val == human_value:
                    human_count += 1
                else:
                    empty_count += 1

            # Score based on potential
            if computer_count > 0 and human_count == 0:
                score += computer_count ** 2
            elif human_count > 0 and computer_count == 0:
                score -= human_count ** 2

        return score

    def check_win(self, player_value: int, move: Move) -> bool:
        """Check if the move creates a win"""
        # Temporarily place piece
        original = self.board[move.layer][move.row][move.col]
        self.board[move.layer][move.row][move.col] = player_value

        # Check all winning combinations
        for combo in self.winning_combinations:
            if all(self.board[l][r][c] == player_value for l, r, c in combo):
                self.winning_cells = combo
                if original != player_value:
                    self.board[move.layer][move.row][move.col] = original
                return True

        # Restore original
        self.board[move.layer][move.row][move.col] = original
        return False

    def is_board_full(self) -> bool:
        """Check if the board is full"""
        for layer in range(4):
            for row in range(4):
                for col in range(4):
                    if self.board[layer][row][col] == -1:
                        return False
        return True

    def handle_win(self, human_won: bool):
        """Handle game win"""
        self.game_over = True

        if human_won:
            self.human_score += 1
            self.status_label.config(text="YOU WIN! 🎉", fg=self.HIGHLIGHT_COLOR)
        else:
            self.computer_score += 1
            self.status_label.config(text="COMPUTER WINS!", fg=self.HIGHLIGHT_COLOR)

        self.update_score()
        self.highlight_winning_cells()

    def handle_tie(self):
        """Handle tie game"""
        self.game_over = True
        self.tie_score += 1
        self.status_label.config(text="IT'S A TIE!", fg='#ffffff')
        self.update_score()

    def highlight_winning_cells(self):
        """Highlight the winning combination in isometric view"""
        for layer, row, col in self.winning_cells:
            # Get cell coordinates
            x, y, w, h, points = self.cell_coords[(layer, row, col)]

            # Draw highlight on the cell
            self.main_canvas.create_polygon(
                points,
                fill='',
                outline=self.HIGHLIGHT_COLOR,
                width=3,
                tags='win_highlight'
            )

            # Redraw piece in gold
            piece_value = self.board[layer][row][col]
            if piece_value == 0:  # X
                self.draw_x(layer, row, col, self.HIGHLIGHT_COLOR, animated=False)
            else:  # O
                self.draw_o(layer, row, col, self.HIGHLIGHT_COLOR, animated=False)

    def update_score(self):
        """Update score display"""
        self.score_label.config(
            text=f"YOU: {self.human_score}  |  CPU: {self.computer_score}  |  TIES: {self.tie_score}"
        )

    def clear_board(self):
        """Clear the board for a new game"""
        self.game_over = False
        self.winning_cells = []
        self.is_animating = False

        # Reset board state
        for layer in range(4):
            for row in range(4):
                for col in range(4):
                    self.board[layer][row][col] = -1

        # Clear main canvas and redraw isometric view
        self.main_canvas.delete('all')
        self.cell_coords = {}
        self.draw_all_layers()

    def new_game(self):
        """Start a new game"""
        self.clear_board()
        self.status_label.config(text="Your turn!", fg=self.X_COLOR)

        # If computer goes first
        if not self.human_first:
            self.status_label.config(text="Computer starts!", fg=self.O_COLOR)
            self.root.after(500, self.computer_turn)

    def on_settings_change(self):
        """Handle settings change"""
        self.human_piece = self.piece_var.get()
        self.computer_piece = 'O' if self.human_piece == 'X' else 'X'
        self.human_first = (self.first_var.get() == 'Human')
        self.new_game()

    def on_difficulty_change(self):
        """Handle difficulty change"""
        diff = self.diff_var.get()
        if diff == 'Easy':
            self.difficulty = 1
            self.max_depth = 1
        elif diff == 'Medium':
            self.difficulty = 2
            self.max_depth = 3
        else:  # Hard
            self.difficulty = 3
            self.max_depth = 4

        self.new_game()

    def run(self):
        """Start the game"""
        self.root.mainloop()


if __name__ == "__main__":
    game = AtariTicTacToe3D()
    game.run()
