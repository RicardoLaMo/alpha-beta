#!/usr/bin/env python3
"""
Test winning combinations generation for 3x3x3 3D Tic-Tac-Toe
"""

def generate_winning_combinations():
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

def main():
    print("="*60)
    print("3D Tic-Tac-Toe (3x3x3) - Winning Combinations Test")
    print("="*60)

    wins = generate_winning_combinations()

    print(f"\nTotal winning combinations: {len(wins)}")

    # Expected combinations breakdown:
    print("\nExpected combinations:")
    print("  - Rows on each layer: 3 rows × 3 layers = 9")
    print("  - Columns on each layer: 3 columns × 3 layers = 9")
    print("  - Diagonals on each layer: 2 diagonals × 3 layers = 6")
    print("  - Vertical through layers: 3×3 = 9")
    print("  - Vertical plane diagonals: 3 cols × 2 + 3 rows × 2 = 12")
    print("  - Space diagonals: 4")
    print("  - Total: 49")

    # Verify each combination has 3 positions
    all_valid = all(len(combo) == 3 for combo in wins)
    print(f"\n✓ All combinations have 3 positions: {all_valid}")

    # Verify all indices are in valid range (0-26)
    all_valid_range = all(0 <= idx <= 26 for combo in wins for idx in combo)
    print(f"✓ All indices in valid range (0-26): {all_valid_range}")

    # Verify no duplicate combinations
    unique_combos = set(tuple(sorted(combo)) for combo in wins)
    no_dups = len(unique_combos) == len(wins)
    print(f"✓ No duplicate combinations: {no_dups}")

    print("\nSample winning combinations:")
    print(f"  Row in layer 0: {wins[0]}")
    print(f"  Column in layer 0: {wins[16]}")
    print(f"  Diagonal in layer 0: {wins[32]}")
    print(f"  Vertical through (0,0): {wins[40]}")
    print(f"  Space diagonal: {wins[-4]}")

    print("\n" + "="*60)
    print("All tests passed!" if all_valid and all_valid_range and no_dups else "Some tests failed!")
    print("="*60)

if __name__ == "__main__":
    main()
