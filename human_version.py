# human version
# version of the sliding tile puzzle for people to solve
# you move tiles by clicking on them and then clicking the highlighted (empty) tile to move to
import pygame
import sys
from functions import *

# constants used mostly for pygame
TILE_SIZE = 100                   # size of each tile
GRID_SIZE = 3                     # 3x3 grid
WIDTH = TILE_SIZE * GRID_SIZE     # window width
HEIGHT = TILE_SIZE * GRID_SIZE    # window height

BG_COLOR = (18, 18, 18)           # background color
SELECTED_COLOR = (128, 128, 128)  # color for selected tile
TILE_COLOR = (52, 138, 82)        # tile color
TEXT_COLOR = (255, 255, 255)      # text color

# get possible moves for tile n
def get_moves(n):
    if n is not None and 1 <= n <= 9:       # input validation
        location = (None, None)             # empty location tuple
        moves = []                          # moves array

        for i in range(GRID_SIZE):          # iterate through tiles
            for j in range(GRID_SIZE):
                if tile_set[i][j] == n:     # if the tile is found
                    location = [i, j]       # update the location tuple
                    break                   # break
            if (location[0] is not None):   # stop unnecessary looping
                break

        if location[0] is not None:                                                   # if the tile was found
            for x in [-1, 1]:                                                         # check x neighbors
                new_x = location[0] + x                                               # refer to current neighbor
                if 0 <= new_x < GRID_SIZE and tile_set[new_x][location[1]] is None:   # if the neighbor is within bounds
                    moves.append((new_x, location[1]))                                # add it to the list of moves
            for y in [-1, 1]:                                                         # check y neighbors
                new_y = location[1] + y                                               # refer to current neighbor
                if 0 <= new_y < GRID_SIZE and tile_set[location[0]][new_y] is None:   # if the neighbor is within bounds
                    moves.append((location[0], new_y))                                # add it to the list of moves
        return moves                                                                  # return moves
    return []                                                                         # return an empty set if no moves were found

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sliding Puzzle")
font = pygame.font.SysFont(None, 48)

current_clicked = None                          # current clicked tile
available_moves = []                            # available moves
tile_set = random_solvable_board(GRID_SIZE)     # random solvable board
moves = 0                                       # set move counter to 0

# draw the puzzle on the screen
def draw_puzzle():
    screen.fill(BG_COLOR)
    # Draw tiles
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = tile_set[row][col]
            rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            if value is not None:
                pygame.draw.rect(screen, TILE_COLOR, rect)
                pygame.draw.rect(screen, BG_COLOR, rect, 2)

                text = font.render(str(value), True, TEXT_COLOR)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            else:
                # Highlight empty slot if it’s available
                if (row, col) in available_moves:
                    pygame.draw.rect(screen, SELECTED_COLOR, rect)
                    pygame.draw.rect(screen, BG_COLOR, rect, 2)

# move tile to destination
def move_tile(tile_value, dest_row, dest_col):
    global tile_set
    global moves
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if tile_set[i][j] == tile_value:
                tile_set[i][j], tile_set[dest_row][dest_col] = (
                    tile_set[dest_row][dest_col],
                    tile_set[i][j],
                )
                moves += 1
                return

# main loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            clicked_row = mouse_pos[1] // TILE_SIZE
            clicked_col = mouse_pos[0] // TILE_SIZE

            clicked_value = tile_set[clicked_row][clicked_col]

            if current_clicked is None:
                # First click → select a tile
                if clicked_value is not None:
                    current_clicked = clicked_value
                    available_moves = get_moves(current_clicked)
            else:
                # Second click → check if it’s a valid move
                if (clicked_row, clicked_col) in available_moves:
                    move_tile(current_clicked, clicked_row, clicked_col)

                # Reset selection regardless
                current_clicked = None
                available_moves = []
    if tile_set == [[1, 2, 3], [4, 5, 6], [7, 8, None]]:
        print("puzzle complete")
        print(f"moves: {moves}")
        break

    draw_puzzle()
    pygame.display.flip()
    clock.tick(10)
