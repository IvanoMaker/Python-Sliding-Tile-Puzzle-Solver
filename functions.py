# functions file
# used to holding frequently used functions to prevent needlessly defining them everywhere
import random
from heap import BinaryHeap

# flatten board to tuple
def board_to_tuple(board):
    return tuple(tuple(row) for row in board)

# expand tuple back to board
def tuple_to_board(t):
    return [list(row) for row in t]

# Helper functions for solvability and random board generation
def inversion_count(flat):
    flat = [n for n in flat if n is not None]   # ignore the None in the board
    count = 0                                   # counter for inversions
    for i in range(len(flat)):                  # iterate through the tiles on the board in sets of 2
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:               # if the first tile is greater than the next
                count += 1                      # increase inversion count
    return count                                # return inversion count

# return True if a board is solvable
def is_solvable(board):
    flat = [tile for row in board for tile in row]  # flatten board completely
    inv = inversion_count(flat)                     # get inversion count
    return inv % 2 == 0                             # solvable if inversion count is even

# generate a random solvable 3x3 board
def random_solvable_board(grid_size):
    flat = [1, 2, 3, 4, 5, 6, 7, 8, None]           # set of tiles in order
    while True:                                     # keep shuffling until a solvable one is found
        random.shuffle(flat)                         
        board = [flat[i:i + grid_size] for i in range(0, grid_size ** 2, grid_size)]
        if is_solvable(board):                      # if the generated board is solvable
            return board                            # return board
        
# Manhattan distance heuristic
def heuristic_sum(board, grid_size, goal_position):
    total = 0                                                # total Manhattan distance
    for i in range(grid_size):                               # rows
        for j in range(grid_size):                           # columns
            n = board[i][j]                                  # get tile number
            if n is not None:                                # ignore if blank
                goal_i, goal_j = goal_position[n]            # unpack goal position
                total += abs(goal_i - i) + abs(goal_j - j)   # add distance
    return total                                             # return total

# Linear conflict heuristic
def linear_conflict(board, grid_size, goal_positions):
    conflicts = 0                                                # count of linear conflicts
    for i in range(grid_size):                                   # rows
        row_tiles = []                                           # row tiles array
        for j in range(grid_size):                               # columns
            n = board[i][j]                                      # get tile number
            if n is not None and goal_positions[n][0] == i:      # if the tile isn't None and is in its goal row
                row_tiles.append((j, goal_positions[n][1]))      # add (current col, goal col) to the row tiles array
        # count inversions in goal columns
        for a in range(len(row_tiles)):                          # for each tile
            for b in range(a+1, len(row_tiles)):                 # compare with subsequent tiles
                if row_tiles[a][1] > row_tiles[b][1]:            # inversion found
                    conflicts += 1                               # increment conflict count

    # columns
    # same logic as rows but for columns
    for j in range(grid_size):
        col_tiles = []
        for i in range(grid_size):
            n = board[i][j]
            if n is not None and goal_positions[n][1] == j:
                col_tiles.append((i, goal_positions[n][0]))
        for a in range(len(col_tiles)):
            for b in range(a+1, len(col_tiles)):
                if col_tiles[a][1] > col_tiles[b][1]:
                    conflicts += 1

    return conflicts                                             # return total conflic count

#Admissible heuristic: Manhattan distance + 2 * linear_conflict
def heuristic(board, grid_size, goal_positions):
    return heuristic_sum(board, grid_size, goal_positions) + 2 * linear_conflict(board, grid_size, goal_positions)

# generate all possible moves from current board state
def find_all_moves(board_t, grid_size):
    board = tuple_to_board(board_t) # expand tuple back to board
    # Locate the blank
    for i in range(grid_size):
        for j in range(grid_size):
            if board[i][j] is None:
                blank_pos = (i, j)
                break
            else:
                continue
    # Generate neighbors by sliding tiles into the blank
    neighbors = []                                      # list of neighbor board tuples
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:          # up, down, left, right
        x, y = blank_pos[0] + dx, blank_pos[1] + dy     # new position
        if 0 <= x < grid_size and 0 <= y < grid_size:   # if it is a valid position
            # Swap blank and tile
            board[blank_pos[0]][blank_pos[1]], board[x][y] = board[x][y], None
            neighbors.append(board_to_tuple(board))
            # Swap back
            board[blank_pos[0]][blank_pos[1]], board[x][y] = None, board[blank_pos[0]][blank_pos[1]]
    return neighbors # return list of neighbor board tuples

def reconstruct_path(came_from, current_t):
    path = [tuple_to_board(current_t)]
    while current_t in came_from:
        current_t = came_from[current_t]
        path.append(tuple_to_board(current_t))
    path.reverse()
    return path

# A* search algorithm
def a_star_search(start_board, grid_size, goal_positions, goal_board):
    start_t = board_to_tuple(start_board) # flatten start board to tuple
    goal_t = board_to_tuple(goal_board)   # flatten goal board to tuple
    # Perform A* and return the solution path as a list of boards (or None).
    open_heap = BinaryHeap()                         # priority queue for open set
    open_heap.push(heuristic(start_board, grid_size, goal_positions), start_t)  # push start node with its f-score
    
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
            return reconstruct_path(came_from, current_t)
        # mark current as evaluated
        closed.add(current_t)
        # explore neighbors
        for neighbor_t in find_all_moves(current_t, grid_size):
            if neighbor_t in closed:      # skip already evaluated
                continue
            tentative_g = current_g + 1                                  # cost from start to neighbor
            if tentative_g < g_score.get(neighbor_t, float('inf')):      # better path found
                came_from[neighbor_t] = current_t                        # record best path
                g_score[neighbor_t] = tentative_g                        # update g-score     
                f = tentative_g + heuristic(tuple_to_board(neighbor_t), grid_size, goal_positions)  # compute f-score
                open_heap.push(f, neighbor_t)                            # add neighbor to open set      
    # no solution found
    return None
