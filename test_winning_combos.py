#!/usr/bin/env python3
"""
Test winning combinations generation for 4x4x4 3D Tic-Tac-Toe
"""

def generate_winning_combinations():
    """Generate all possible winning combinations for 4x4x4 board"""
    wins = []

    # Helper function to convert 3D coordinates to 1D index
    def coord_to_index(layer, row, col):
        return layer * 16 + row * 4 + col

    # 1. Rows on each layer
    for layer in range(4):
        for row in range(4):
            wins.append([coord_to_index(layer, row, col) for col in range(4)])

    # 2. Columns on each layer
    for layer in range(4):
        for col in range(4):
            wins.append([coord_to_index(layer, row, col) for row in range(4)])

    # 3. Diagonals on each layer
    for layer in range(4):
        # Main diagonal
        wins.append([coord_to_index(layer, i, i) for i in range(4)])
        # Anti-diagonal
        wins.append([coord_to_index(layer, i, 3-i) for i in range(4)])

    # 4. Vertical lines through layers
    for row in range(4):
        for col in range(4):
            wins.append([coord_to_index(layer, row, col) for layer in range(4)])

    # 5. Diagonal lines through layers (in vertical planes)
    # Front-to-back diagonals
    for col in range(4):
        # Descending
        wins.append([coord_to_index(i, i, col) for i in range(4)])
        # Ascending
        wins.append([coord_to_index(i, 3-i, col) for i in range(4)])

    # Left-to-right diagonals
    for row in range(4):
        # Descending
        wins.append([coord_to_index(i, row, i) for i in range(4)])
        # Ascending
        wins.append([coord_to_index(i, row, 3-i) for i in range(4)])

    # 6. Space diagonals (corner to corner)
    # Main space diagonals
    wins.append([coord_to_index(i, i, i) for i in range(4)])  # (0,0,0) to (3,3,3)
    wins.append([coord_to_index(i, i, 3-i) for i in range(4)])  # (0,0,3) to (3,3,0)
    wins.append([coord_to_index(i, 3-i, i) for i in range(4)])  # (0,3,0) to (3,0,3)
    wins.append([coord_to_index(i, 3-i, 3-i) for i in range(4)])  # (0,3,3) to (3,0,0)

    return wins

def main():
    print("="*60)
    print("3D Tic-Tac-Toe (4x4x4) - Winning Combinations Test")
    print("="*60)

    wins = generate_winning_combinations()

    print(f"\nTotal winning combinations: {len(wins)}")

    # Expected combinations breakdown:
    print("\nExpected combinations:")
    print("  - Rows on each layer: 4 rows × 4 layers = 16")
    print("  - Columns on each layer: 4 columns × 4 layers = 16")
    print("  - Diagonals on each layer: 2 diagonals × 4 layers = 8")
    print("  - Vertical through layers: 4×4 = 16")
    print("  - Vertical plane diagonals: 4 cols × 2 + 4 rows × 2 = 16")
    print("  - Space diagonals: 4")
    print("  - Total: 76")

    # Verify each combination has 4 positions
    all_valid = all(len(combo) == 4 for combo in wins)
    print(f"\n✓ All combinations have 4 positions: {all_valid}")

    # Verify all indices are in valid range (0-63)
    all_valid_range = all(0 <= idx <= 63 for combo in wins for idx in combo)
    print(f"✓ All indices in valid range (0-63): {all_valid_range}")

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
