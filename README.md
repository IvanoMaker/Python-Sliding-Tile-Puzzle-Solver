# Python Sliding Tile Puzzle Solver

This Python repository contains the structure for a sliding tile puzzle, as well as the code required to solve the maze.
When the `main.py` file is ran, it will open a pygame window for the visual representation of the puzzle. The puzzle will then be solved immedietly by the program.
The number of moves it took to solve the puzzle will be printed in the console.

| ![alt text](res/puzzle_gif.gif) |
|:--:|
| *A.1 The puzzle being solved* |

### `heap.py`
This file contains a class definition for the heap data structure used by A*.

### `functions.py`
This file contains a variety of helper functions used throughout the other files.  
These include the A* algorithm itself, functions for encoding and decoding the tile data,  
and functions to make sure the game state is solvable before attempting to solve it.

### `knowledge.zip`
This is the compressed `knowledge.txt` file.  
It contains the complete game knowledge of the sliding tile puzzle.  

- Each line has two parts: the **key** and the **moves**.  
- The key is the encoded string for the board state.  
- The moves are a list of the moves required to solve the puzzle in that configuration.  
- Moves are structured like `(n, 'direction')`, where `n` is one of the numbers between 1 and 8,  
  and `direction` is either `up`, `down`, `left`, or `right`.  

This file contains **181,440** lines, which is exactly half of $9!$ (the total number of permutations of 9 tiles, including the empty one).
