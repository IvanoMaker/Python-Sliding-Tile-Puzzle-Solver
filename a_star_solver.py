# a* solver
# creates a random, solvable board and solves it using the a* algorithm
import pygame
import sys
from functions import *

# constants used mostly for pygame
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
solution = a_star_search(tile_set, GRID_SIZE, GOAL_POSITIONS, GOAL_BOARD)
clock = pygame.time.Clock()
step_index = 0
solved = False

# main loop
while True:
    for event in pygame.event.get():      # check if the window is closed
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
    
    draw_puzzle(tile_set)   # call the draw function
    pygame.display.flip()   # dispaly the updated pygame screen
    clock.tick(10)          # 10 FPS
