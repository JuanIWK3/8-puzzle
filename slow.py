import time
import numpy as np
import sys

sys.setrecursionlimit(1000000)

# Define the goal state
goal = np.array([1, 2, 3, 4, 5, 6, 7, 8, 0]).reshape(3, 3)

# Define the neighbors (possible moves) esq, dir, baixo, cima
neighbors = [[-1, 0], [1, 0], [0, -1], [0, 1]]

# Set to keep track of already tried states
already_tried = set()


def get_inversions(game):
    inversions = 0
    game = game.flatten()
    for i in range(len(game)):
        for j in range(i + 1, len(game)):
            if game[i] > game[j] and game[i] != 0 and game[j] != 0:
                inversions += 1
    return inversions


def manhattan_distance(game):
    distance = 0
    for i in range(3):
        for j in range(3):
            if game[i][j] != 0:
                x, y = np.where(goal == game[i][j])
                distance += abs(i - x[0]) + abs(j - y[0])
    return distance


def game_to_string(game):
    return "".join(map(str, game.flatten()))


count = 0


def solve(game, print_steps=False):
    global count
    count += 1

    if print_steps:
        print(game)
        print("Manhattan distance:", manhattan_distance(game))
        print()

    # Convert board to string for immutability and set operations
    game_str = game_to_string(game)

    if np.array_equal(game, goal):
        print("Goal reached!")
        return True

    # Check if this state has been tried before
    if game_str in already_tried:
        return False

    # Mark this state as tried
    already_tried.add(game_str)

    # Find the position of the empty tile
    empty_pos = np.argwhere(game == 0)[0]
    i, j = empty_pos

    # Try all possible moves
    for neighbor in neighbors:
        x = i + neighbor[0]
        y = j + neighbor[1]
        if 0 <= x < 3 and 0 <= y < 3:
            # Swap the empty tile with the neighboring tile
            game[i][j], game[x][y] = game[x][y], game[i][j]
            if solve(game, print_steps=print_steps):
                return True
            # Revert the swap
            game[i][j], game[x][y] = game[x][y], game[i][j]

    return False


# Initial game state
unsolvable = [8, 1, 2, 0, 4, 3, 7, 6, 5]
solvable = [1, 8, 2, 0, 4, 3, 7, 6, 5]
easy = [1, 2, 3, 4, 5, 6, 7, 8, 0]
one_inversion = [1, 2, 3, 4, 5, 0, 7, 8, 6]


game = np.array(one_inversion).reshape(3, 3)

print("Initial state:")
print(game)
print()

start = time.time()

# Check if the game is solvable
if get_inversions(game) % 2 != 0:
    print("This game is not solvable")
    exit()

# Start solving
if not solve(game, print_steps=False):
    print("No solution found")

end = time.time()
print("Time taken:", end - start)
print(count)
