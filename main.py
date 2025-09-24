import random
import pygame
import sys
from heap import BinaryHeap

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

# flatten board to tuple
def board_to_tuple(board):
    return tuple(tuple(row) for row in board)
# expand tuple back to board
def tuple_to_board(t):
    return [list(row) for row in t]

# Manhattan distance heuristic
def heuristic_sum(board):
    total = 0                       # total Manhattan distance
    for i in range(GRID_SIZE):      # rows
        for j in range(GRID_SIZE):  # columns
            n = board[i][j]         # tile number
            if n is not None:              # ignore blank
                goal_i, goal_j = GOAL_POSITIONS[n]         # goal position
                total += abs(goal_i - i) + abs(goal_j - j) # add distance
    return total #return total

# Linear conflict heuristic
def linear_conflict(board):
    conflicts = 0   # count of linear conflicts
    for i in range(GRID_SIZE):  # rows
        # collect tiles in their goal row
        row_tiles = []
        for j in range(GRID_SIZE):
            n = board[i][j]
            if n is not None and GOAL_POSITIONS[n][0] == i: # if the tile is in its goal row
                row_tiles.append((j, GOAL_POSITIONS[n][1])) # (current col, goal col)
        # count inversions in goal columns
        for a in range(len(row_tiles)):           # for each tile
            for b in range(a+1, len(row_tiles)):  # compare with subsequent tiles
                if row_tiles[a][1] > row_tiles[b][1]: # inversion found
                    conflicts += 1 # increment conflict count

    # columns
    # same logic as rows but for columns
    for j in range(GRID_SIZE):
        col_tiles = []
        for i in range(GRID_SIZE):
            n = board[i][j]
            if n is not None and GOAL_POSITIONS[n][1] == j:
                col_tiles.append((i, GOAL_POSITIONS[n][0]))
        for a in range(len(col_tiles)):
            for b in range(a+1, len(col_tiles)):
                if col_tiles[a][1] > col_tiles[b][1]:
                    conflicts += 1

    return conflicts

#Admissible heuristic: Manhattan distance + 2 * linear_conflict
def heuristic(board):
    return heuristic_sum(board) + 2 * linear_conflict(board)

# Helper functions for solvability and random board generation
def inversion_count(flat):
    flat = [n for n in flat if n is not None]
    count = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                count += 1
    return count

# return True if a board is solvable
def is_solvable(board):
    flat = [tile for row in board for tile in row]
    inv = inversion_count(flat)
    return inv % 2 == 0  # 3x3 grid: solvable if inversion count is even

# generate a random solvable 3x3 board
def random_solvable_board():
    flat = [1, 2, 3, 4, 5, 6, 7, 8, None]
    while True:
        random.shuffle(flat)
        board = [flat[i:i + GRID_SIZE] for i in range(0, GRID_SIZE ** 2, GRID_SIZE)]
        if is_solvable(board):
            return board

# generate all possible moves from current board state
def find_all_moves(board_t):
    board = tuple_to_board(board_t) # expand tuple back to board
    # Locate the blank
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] is None:
                blank_pos = (i, j)
                break
        else:
            continue
        break
    # Generate neighbors by sliding tiles into the blank
    neighbors = []                                      # list of neighbor board tuples
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:          # up, down, left, right
        x, y = blank_pos[0] + dx, blank_pos[1] + dy     # new position
        if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:   # if it is a valid position
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
            return reconstruct_path(came_from, current_t)
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

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sliding Puzzle")
font = pygame.font.SysFont(None, 48)

# draw the puzzle on the screen
def draw_puzzle(board):
    screen.fill(BG_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            val = board[i][j]
            if val is not None:
                rect = pygame.Rect(j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, TILE_COLOR, rect)
                pygame.draw.rect(screen, BG_COLOR, rect, 2)
                text = font.render(str(val), True, TEXT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

# Initialize puzzle and solve
tile_set = random_solvable_board()
solution = a_star_search(tile_set)
clock = pygame.time.Clock()
step_index = 0
solved = False

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Animate solution steps
    if solution is not None and step_index < len(solution):
        tile_set = solution[step_index]
        step_index += 1
    # print when solution is complete
    elif solution is not None and not solved:
        solved = True
        print('Solution length:', len(solution) - 1)

    draw_puzzle(tile_set)
    pygame.display.flip()
    clock.tick(10)