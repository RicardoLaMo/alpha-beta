#!/usr/bin/env python3
"""
Test script for 3D Tic-Tac-Toe to verify winning combinations
"""

from ttt3d_4x4x4 import TTT3D, OneMove

def test_winning_combinations():
    """Test that winning combinations are generated correctly"""
    game = TTT3D()

    # Destroy the GUI window for testing
    game.root.destroy()

    # Create a new instance without GUI for testing
    game = TTT3D.__new__(TTT3D)
    game.BOARD_SIZE = 4
    game.LAYERS = 4
    game.WIN_LENGTH = 4
    game.winning_combinations = game._generate_winning_combinations()

    print(f"Total winning combinations: {len(game.winning_combinations)}")

    # Expected combinations:
    # Rows: 4 rows × 4 layers = 16
    # Columns: 4 columns × 4 layers = 16
    # Layer diagonals: 2 diagonals × 4 layers = 8
    # Vertical: 4×4 = 16
    # Vertical plane diagonals: 4 columns × 2 + 4 rows × 2 = 16
    # Space diagonals: 4
    # Total = 16 + 16 + 8 + 16 + 16 + 4 = 76

    print("\nSample winning combinations:")
    print(f"First 5: {game.winning_combinations[:5]}")
    print(f"Last 5: {game.winning_combinations[-5:]}")

    # Verify each combination has 4 positions
    all_valid = all(len(combo) == 4 for combo in game.winning_combinations)
    print(f"\nAll combinations have 4 positions: {all_valid}")

    # Verify no duplicate combinations
    unique_combos = set(tuple(sorted(combo)) for combo in game.winning_combinations)
    print(f"No duplicates: {len(unique_combos) == len(game.winning_combinations)}")

    return game

def test_board_indices():
    """Test that board index conversion works correctly"""
    def coord_to_index(layer, row, col):
        return layer * 16 + row * 4 + col

    print("\n\nTesting board index conversion:")
    print(f"(0,0,0) -> {coord_to_index(0,0,0)} (expected: 0)")
    print(f"(0,0,3) -> {coord_to_index(0,0,3)} (expected: 3)")
    print(f"(0,3,3) -> {coord_to_index(0,3,3)} (expected: 15)")
    print(f"(1,0,0) -> {coord_to_index(1,0,0)} (expected: 16)")
    print(f"(3,3,3) -> {coord_to_index(3,3,3)} (expected: 63)")

if __name__ == "__main__":
    print("="*50)
    print("3D Tic-Tac-Toe (4x4x4) Test Suite")
    print("="*50)

    test_winning_combinations()
    test_board_indices()

    print("\n" + "="*50)
    print("Tests completed!")
    print("="*50)
