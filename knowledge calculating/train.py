import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from heap import BinaryHeap
from functions import tuple_to_board, board_to_tuple, heuristic, find_all_moves, reconstruct_path

TILE_SIZE = 100
GRID_SIZE = 3
WIDTH = TILE_SIZE * GRID_SIZE
HEIGHT = TILE_SIZE * GRID_SIZE

BG_COLOR = (18, 18, 18)         # background color
TILE_COLOR = (52, 138, 82)      # tile color
TEXT_COLOR = (255, 255, 255)    # text color

# Define goal state
GOAL_BOARD = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, None]
]

# Precompute goal positions for heuristic calculations
GOAL_POSITIONS = {1: (0, 0), 2: (0, 1), 3: (0, 2),
                  4: (1, 0), 5: (1, 1), 6: (1, 2),
                  7: (2, 0), 8: (2, 1), None: (2, 2)}

# get the move done to get from board_a to board_b
def get_move_between(board_a, board_b):
    # find blank positions
    a_blank = None
    b_blank = None
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board_a[i][j] is None:
                a_blank = (i, j)
            if board_b[i][j] is None:
                b_blank = (i, j)
    # the moved tile is the one that occupies the opposite blank position
    # i.e., the tile that moved into the blank in board_b was adjacent to a_blank in board_a
    # find the tile that changed position
    moved_tile = None
    moved_from = None
    moved_to = None
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board_a[i][j] != board_b[i][j]:
                # record first differing tile position in a and b
                if board_a[i][j] is not None:
                    moved_from = (i, j)
                    moved_tile = board_a[i][j]
                if board_b[i][j] is not None:
                    moved_to = (i, j)
    # if we couldn't detect via diffs, fall back to blank positions
    if moved_tile is None and a_blank and b_blank:
        # tile moved from b_blank to a_blank or vice versa
        # The tile that moved occupies a_blank in board_b
        moved_to = a_blank
        moved_from = b_blank
        moved_tile = board_b[moved_to[0]][moved_to[1]]

    if moved_tile is None or moved_from is None or moved_to is None:
        return (None, None)

    di = moved_to[0] - moved_from[0]
    dj = moved_to[1] - moved_from[1]
    if di == -1 and dj == 0:
        direction = 'up'
    elif di == 1 and dj == 0:
        direction = 'down'
    elif di == 0 and dj == -1:
        direction = 'left'
    elif di == 0 and dj == 1:
        direction = 'right'
    else:
        direction = None
    return (moved_tile, direction)

# A* search algorithm
# different than what is in the functions file as it counts the specific moves used here.
def a_star_search(start_board):
    start_t = board_to_tuple(start_board) # flatten start board to tuple
    goal_t = board_to_tuple(GOAL_BOARD)   # flatten goal board to tuple
    # Perform A* and return the solution path as a list of boards (or None).
    open_heap = BinaryHeap()                         # priority queue for open set
    open_heap.push(heuristic(start_board), start_t)  # push start node with its f-score
    
    came_from = {}                       # to reconstruct path
    g_score = {start_t: 0}               # cost from start to current node
    closed = set()                       # closed set of evaluated nodes

    # main loop
    while len(open_heap) > 0:
        _, current_t = open_heap.pop()
        # if we popped a stale entry, skip
        if current_t in closed:
            continue
        # current_board = tuple_to_board(current_t)
        current_g = g_score.get(current_t, float('inf'))
        # goal check
        if current_t == goal_t:
            # reconstruct board path
            board_path = reconstruct_path(came_from, current_t)
            # build moves list (tile, direction) between consecutive boards
            moves = []
            for a, b in zip(board_path, board_path[1:]):
                moves.append(get_move_between(a, b))
            return board_path, moves
        # mark current as evaluated
        closed.add(current_t)
        # explore neighbors
        for neighbor_t in find_all_moves(current_t):
            if neighbor_t in closed:      # skip already evaluated
                continue
            tentative_g = current_g + 1                                  # cost from start to neighbor
            if tentative_g < g_score.get(neighbor_t, float('inf')):      # better path found
                came_from[neighbor_t] = current_t                        # record best path
                g_score[neighbor_t] = tentative_g                        # update g-score     
                f = tentative_g + heuristic(tuple_to_board(neighbor_t))  # compute f-score
                open_heap.push(f, neighbor_t)                            # add neighbor to open set      
    # no solution found
    return None

tracker = 0             # track position in the file
total_knowledge = []    # list of files to write to file

with open('permutations.txt', 'r') as f:
    for line in f:                                                   # for line in the files
        key = line.split(':')[0]                                     # get the key from the line
        board = [                                                    # reconstruct the board from the encoded tile set
            [int(c) if c != "0" else None for c in key[j:j+3]]
            for j in range(0, 9, 3)
        ]

        board_path, moves = a_star_search(board)     # perform a*, store the board_path and the moves.
        total_knowledge.append(f"{key}:{moves}")     # add the like to the file

        tracker += 1                     # increment the tracker
        if (tracker % 1000 == 0):        # print a status update every 1000 boards solved
            print(f"{tracker} / 181440")

with open('knowledge.txt', 'w') as f:   # upload the knowledge to the text file
    for line in total_knowledge:
        f.write(line + "\n")