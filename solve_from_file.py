# play from file
# solve a random solvable 3x3 sliding tile puzzle by getting the list of moves needed to solve it from the "knowledge.txt" file
import pygame
import sys
import ast
from functions import *

# constants used mostly for pygame
TILE_SIZE = 100                   # size of each tile
GRID_SIZE = 3                     # 3x3 grid
WIDTH = TILE_SIZE * GRID_SIZE     # window width
HEIGHT = TILE_SIZE * GRID_SIZE    # window height

BG_COLOR = (18, 18, 18)         # background color
TILE_COLOR = (52, 138, 82)      # tile color
TEXT_COLOR = (255, 255, 255)    # text color

# direction vectors for tile movement: (di, dj) where di is row change, dj is col change
DIRECTION = {
    "up":(-1, 0),
    "down":(1, 0),
    "left":(0, -1),
    "right":(0, 1)
}

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

# encode board into a string for finding the solution in the file
# i.e. [[1, 2, 3], [4, 5, 6], [7, 8, None]] -> 123456780
def encode_board(board):
    string = ""
    for i in range(3):
        for j in range(3):
            if board[i][j] == None:
                string += '0'
            else:
                string += str(board[i][j])
    return string

# find the blank tile
def find_blank(board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] is None:
                return i, j
    return None

# apply move to the board
def apply_move(board, direction):
    di, dj = DIRECTION[direction]   # direction as in dx, dy
    i, j = find_blank(board)        # find blank tile
    ni, nj = i + di, j + dj         # calculate neighbor

    # Swap blank with neighbor
    if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
        board[i][j], board[ni][nj] = board[ni][nj], board[i][j]

# apply move to a specific tile
def apply_tile_move(board, tile, direction):
    di, dj = DIRECTION[direction]       # direction as in dx, dy
    pos = None                          # find tile position
    
    for i in range(GRID_SIZE):          # iterate through grid
        for j in range(GRID_SIZE):  
            if board[i][j] == tile:     # if the tile were looking for is found
                pos = (i, j)            # set the pos to the tile coordinates and break the loop
                break
        if pos:                         # break second loop if tile was found
            break
    
    ti, tj = pos                        # tile position unpacking
    ni, nj = ti + di, tj + dj           # get neighbor tile coordinates
    # legal tile move: destination inside grid and is blank
    if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE and board[ni][nj] is None:
        board[ti][tj], board[ni][nj] = board[ni][nj], board[ti][tj]
        return
    # fallback: if blank adjacent to tile, swap
    b = find_blank(board)                                                   # find blank
    if b:                                                                   # if blank found
        bi, bj = b                                                          # unpack coordinates
        if abs(bi - ti) + abs(bj - tj) == 1:                                # if the tiles are next to each other
            board[ti][tj], board[bi][bj] = board[bi][bj], board[ti][tj]     # swap tiles
            return

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
tile_set = random_solvable_board(GRID_SIZE)
clock = pygame.time.Clock()
step_index = 0
solved = False
encoded_board = encode_board(tile_set)
moves = []

# get the list of moves needed to solve the board state
with open('knowledge.txt', 'r') as f:                       # open the knowledge.txt file (see train.py for more info)
    for line in f:                                          # for each line in the file
        key, moves_str = line.strip().split(':', 1)         # unpack the state key and the moves list, we already know each entry is solvable
        if key == encoded_board:                            # if the key is found
            moves = ast.literal_eval(moves_str)             # add the needed moves to the moves array

# moves is a list of (tile, direction) tuples
directions = moves
step_index = 0
# main loop
while True:
    for event in pygame.event.get():      # check if the window is closed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if step_index < len(directions):      # if we are not done iterating through the steps
        mv = directions[step_index]       # set the current move
        # mv expected to be (tile, direction) or just direction string
        if isinstance(mv, tuple) and len(mv) >= 2:
            tile, direction = mv[0], mv[1]              # unpack tile and direction
            apply_tile_move(tile_set, tile, direction)  # move the tile
        else:  # fallback: treat mv as direction and move blank
            apply_move(tile_set, mv)
        step_index += 1                   # iterate steps

    draw_puzzle(tile_set)   # call the draw function
    pygame.display.flip()   # dispaly the updated pygame screen
    clock.tick(10)          # 10 FPS