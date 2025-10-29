"""
3D Tic-Tac-Toe Game (4x4x4) with Alpha-Beta Pruning AI
Single Player vs AI with Multiple Difficulty Levels

Difficulty Levels:
- Easy: Alpha-beta pruning 2 levels deep
- Difficult: Alpha-beta pruning 4 levels deep
- Insane: Alpha-beta pruning 6 levels deep
"""

from random import choice
from math import inf

class TicTacToe3D:
    """
    3D Tic-Tac-Toe game with 4x4x4 board (64 positions)
    """
    def __init__(self):
        # Board: 4 levels, each level is 4x4
        # board[z][y][x] where z is level (0-3), y is row (0-3), x is column (0-3)
        self.board = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
        self.difficulty_depths = {
            'easy': 2,
            'difficult': 4,
            'insane': 6
        }

    def clear_board(self):
        """Reset the board to empty state"""
        self.board = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]

    def display_board(self):
        """Display the 3D board in a 2D representation"""
        chars = {1: 'X', -1: 'O', 0: ' '}
        print("\n" + "="*60)
        print("3D TIC-TAC-TOE BOARD (4x4x4)")
        print("="*60)

        for z in range(4):
            print(f"\nLevel {z + 1}:")
            print("    0   1   2   3")
            print("  " + "-" * 17)
            for y in range(4):
                print(f"{y} ", end="")
                for x in range(4):
                    ch = chars[self.board[z][y][x]]
                    print(f"| {ch} ", end="")
                print("|")
                print("  " + "-" * 17)
        print("="*60 + "\n")

    def get_all_winning_lines(self):
        """
        Generate all possible winning lines in 4x4x4 3D tic-tac-toe
        There are 76 possible winning lines total
        """
        lines = []

        # 1. Rows within each level (4 levels * 4 rows = 16)
        for z in range(4):
            for y in range(4):
                lines.append([(z, y, x) for x in range(4)])

        # 2. Columns within each level (4 levels * 4 columns = 16)
        for z in range(4):
            for x in range(4):
                lines.append([(z, y, x) for y in range(4)])

        # 3. Diagonals within each level (4 levels * 2 diagonals = 8)
        for z in range(4):
            # Main diagonal
            lines.append([(z, i, i) for i in range(4)])
            # Anti-diagonal
            lines.append([(z, i, 3-i) for i in range(4)])

        # 4. Vertical lines through levels (4x4 = 16)
        for y in range(4):
            for x in range(4):
                lines.append([(z, y, x) for z in range(4)])

        # 5. Diagonals in vertical planes (YZ plane, 4 positions * 2 diagonals = 8)
        for x in range(4):
            # Main diagonal
            lines.append([(i, i, x) for i in range(4)])
            # Anti-diagonal
            lines.append([(i, 3-i, x) for i in range(4)])

        # 6. Diagonals in vertical planes (XZ plane, 4 positions * 2 diagonals = 8)
        for y in range(4):
            # Main diagonal
            lines.append([(i, y, i) for i in range(4)])
            # Anti-diagonal
            lines.append([(i, y, 3-i) for i in range(4)])

        # 7. 3D diagonals (4 space diagonals)
        # Main 3D diagonal
        lines.append([(i, i, i) for i in range(4)])
        # 3D diagonal (z, y, 3-x)
        lines.append([(i, i, 3-i) for i in range(4)])
        # 3D diagonal (z, 3-y, x)
        lines.append([(i, 3-i, i) for i in range(4)])
        # 3D diagonal (z, 3-y, 3-x)
        lines.append([(i, 3-i, 3-i) for i in range(4)])

        return lines

    def check_winner(self, player):
        """Check if the specified player has won"""
        lines = self.get_all_winning_lines()

        for line in lines:
            if all(self.board[z][y][x] == player for z, y, x in line):
                return True
        return False

    def game_won(self):
        """Check if game has been won by either player"""
        return self.check_winner(1) or self.check_winner(-1)

    def get_score(self):
        """Get the score for the current board state"""
        if self.check_winner(1):
            return 10
        elif self.check_winner(-1):
            return -10
        else:
            return 0

    def get_blanks(self):
        """Get all empty positions on the board"""
        blanks = []
        for z in range(4):
            for y in range(4):
                for x in range(4):
                    if self.board[z][y][x] == 0:
                        blanks.append((z, y, x))
        return blanks

    def board_full(self):
        """Check if the board is completely filled"""
        return len(self.get_blanks()) == 0

    def set_move(self, z, y, x, player):
        """Place a move on the board"""
        self.board[z][y][x] = player

    def alpha_beta_minimax(self, depth, alpha, beta, player):
        """
        Alpha-Beta Pruning algorithm for 3D Tic-Tac-Toe

        Args:
            depth: Maximum depth to search
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            player: Current player (1 for X, -1 for O)

        Returns:
            [z, y, x, score] - best move and its score
        """
        z_pos = -1
        y_pos = -1
        x_pos = -1

        # Terminal conditions
        if depth == 0 or self.game_won() or self.board_full():
            return [z_pos, y_pos, x_pos, self.get_score()]

        blanks = self.get_blanks()

        for cell in blanks:
            z, y, x = cell
            self.set_move(z, y, x, player)
            score = self.alpha_beta_minimax(depth - 1, alpha, beta, -player)

            if player == 1:  # Maximizing player (X)
                if score[3] > alpha:
                    alpha = score[3]
                    z_pos, y_pos, x_pos = z, y, x
            else:  # Minimizing player (O)
                if score[3] < beta:
                    beta = score[3]
                    z_pos, y_pos, x_pos = z, y, x

            # Undo move
            self.set_move(z, y, x, 0)

            # Alpha-beta pruning
            if alpha >= beta:
                break

        if player == 1:
            return [z_pos, y_pos, x_pos, alpha]
        else:
            return [z_pos, y_pos, x_pos, beta]

    def ai_move(self, difficulty='difficult'):
        """
        AI makes a move based on difficulty level

        Args:
            difficulty: 'easy' (depth 2), 'difficult' (depth 4), or 'insane' (depth 6)
        """
        blanks = self.get_blanks()

        # If board is empty or nearly empty, make a random move for efficiency
        if len(blanks) >= 60:
            z, y, x = choice(blanks)
            self.set_move(z, y, x, -1)
            print(f"AI (O) placed at Level {z+1}, Row {y}, Col {x}")
            return

        # Use alpha-beta pruning with appropriate depth
        depth = self.difficulty_depths.get(difficulty, 4)

        # Limit depth based on number of empty cells to avoid excessive computation
        max_depth = min(depth, len(blanks))

        print(f"AI thinking (Difficulty: {difficulty.upper()}, Depth: {max_depth})...")
        result = self.alpha_beta_minimax(max_depth, -inf, inf, -1)

        z, y, x = result[0], result[1], result[2]
        self.set_move(z, y, x, -1)
        print(f"AI (O) placed at Level {z+1}, Row {y}, Col {x}")

    def player_move(self):
        """Get and execute player's move"""
        valid_move = False

        while not valid_move:
            try:
                print("\nEnter your move (X):")
                level = int(input("  Level (1-4): ")) - 1
                row = int(input("  Row (0-3): "))
                col = int(input("  Column (0-3): "))

                if not (0 <= level <= 3 and 0 <= row <= 3 and 0 <= col <= 3):
                    print("Invalid input! All values must be in range.")
                    continue

                if (level, row, col) not in self.get_blanks():
                    print("That position is already taken! Try again.")
                    continue

                self.set_move(level, row, col, 1)
                valid_move = True

            except ValueError:
                print("Invalid input! Please enter numbers only.")
            except KeyboardInterrupt:
                print("\nGame interrupted!")
                return False

        return True

    def print_result(self):
        """Print the game result"""
        print("\n" + "="*60)
        if self.check_winner(1):
            print("CONGRATULATIONS! You (X) have won!")
        elif self.check_winner(-1):
            print("AI (O) has won! Better luck next time!")
        else:
            print("It's a DRAW!")
        print("="*60 + "\n")


def play_game():
    """Main game loop"""
    print("="*60)
    print("3D TIC-TAC-TOE with ALPHA-BETA PRUNING")
    print("4x4x4 Board (64 positions)")
    print("="*60)

    game = TicTacToe3D()

    # Select difficulty
    print("\nSelect difficulty level:")
    print("1. Easy (AI searches 2 levels deep)")
    print("2. Difficult (AI searches 4 levels deep)")
    print("3. Insane (AI searches 6 levels deep)")

    difficulty_map = {1: 'easy', 2: 'difficult', 3: 'insane'}
    difficulty = 'difficult'

    while True:
        try:
            choice_diff = int(input("Enter choice (1-3): "))
            if choice_diff in difficulty_map:
                difficulty = difficulty_map[choice_diff]
                break
            else:
                print("Invalid choice! Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input! Please enter a number.")

    print(f"\nDifficulty set to: {difficulty.upper()}")

    # Select who goes first
    print("\nWho goes first?")
    print("1. You (X)")
    print("2. AI (O)")

    current_player = 1
    while True:
        try:
            order = int(input("Enter choice (1-2): "))
            if order == 1:
                current_player = 1
                print("\nYou (X) go first!")
                break
            elif order == 2:
                current_player = -1
                print("\nAI (O) goes first!")
                break
            else:
                print("Invalid choice! Please enter 1 or 2.")
        except ValueError:
            print("Invalid input! Please enter a number.")

    # Game loop
    game.clear_board()
    game.display_board()

    while not (game.board_full() or game.game_won()):
        if current_player == 1:
            # Player's turn
            if not game.player_move():
                return
        else:
            # AI's turn
            game.ai_move(difficulty)

        game.display_board()

        # Switch player
        current_player *= -1

    # Print result
    game.print_result()

    # Ask to play again
    play_again = input("Play again? (y/n): ").lower()
    if play_again == 'y':
        play_game()


# Driver Code
if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nGame terminated by user. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()
