#include <stdlib.h>
#include <stdio.h>

struct Position{
    int X;
    int Y;
};

void get_coordinates(int index, int *x, int *y) {
    if (index < 1 || index > 9) {
        *x = -1;
        *y = -1;
        return;
    }

    *x = (index - 1) % 3;
    *y = (index - 1) / 3;
}

int get_index(int x, int y) {
    if (x < 0 || x > 2 || y < 0 || y > 2) {
        return -1;
    }

    return y * 3 + x + 1;
}

int inversionCount (int *board) {
    int flat[8];
    int j, count = 0;

    for (int i = 0; i < 9; i++) {
        if (board[i] != 0){
            flat[j] = board[i];
            j++;
        }
    }

    for (int k = 0; k < 8; k++) {
        for (int l = (k + 1); l < 8; l++) {
            if (flat[k] > flat[l]) {
                count++;
            }
        }
    }

    return count;
}

int isSolvable(int *board) {
    int invs = inversionCount(board);
    return (invs % 2 == 0);
}

int heuristicSum(int *board, int gridSize, struct Position *goal_positions) {
    int total = 0;
    int goal_x, goal_y, cur_x, cur_y;
    for (int i = 0; i < 9; i++) {
        get_coordinates(i, &goal_x, &goal_y);
        if (board[i] != 0){
            const struct Position pos = goal_positions[i];
            goal_x = pos.X;
            goal_y = pos.Y;

            total += abs(goal_x - cur_x) + abs(goal_y - cur_y);
        }
    }
    return total;
}

int linearConflicts(int *board, int gridSize, struct Position *goal_positions) {
    int conflicts, n = 0;
    int temp_n;

    for (int i = 0; i < gridSize; i++) {
        struct Position row_tiles[3];
        temp_n = 0;
        for (int j = 0; j < gridSize; j++) {
            n = board[get_index(i, j)];
            if (n != 0 && goal_positions[n].X == i) {
                struct Position temp = { .X = j, .Y = goal_positions[n].Y };
                row_tiles[temp_n] = temp;
                temp_n++;
            }
        }
        for (int a = 0; a < temp_n; a++) {
            for (int b = a + 1; b < temp_n; b++) {
                if (row_tiles[a].Y > row_tiles[b].Y) {
                    conflicts++;
                }
            }
        }
    }

    for (int i = 0; i < gridSize; i++) {
        struct Position col_tiles[3];
        temp_n = 0;
        for (int j = 0; j < gridSize; j++) {
            n = board[get_index(j, i)];
            if (n != 0 && goal_positions[n].X == i) {
                struct Position temp = { .X = j, .Y = goal_positions[n].X };
                col_tiles[temp_n] = temp;
                temp_n++;
            }
        }
        for (int a = 0; a < temp_n; a++) {
            for (int b = a + 1; b < temp_n; b++) {
                if (col_tiles[a].Y > col_tiles[b].Y) {
                    conflicts++;
                }
            }
        }
    }

    return conflicts;
}

int main() {

    const int GOAL_BOARD[9] = {1, 2, 3, 4, 5, 6, 7, 8, 0};

    struct Position GOAL_POSITIONS[9];

    {
        GOAL_POSITIONS[0].X = 2;
        GOAL_POSITIONS[0].Y = 2;
        GOAL_POSITIONS[1].X = 0;
        GOAL_POSITIONS[1].Y = 0;
        GOAL_POSITIONS[2].X = 1;
        GOAL_POSITIONS[2].Y = 0;
        GOAL_POSITIONS[3].X = 2;
        GOAL_POSITIONS[3].Y = 0;
        GOAL_POSITIONS[4].X = 0;
        GOAL_POSITIONS[4].Y = 1;
        GOAL_POSITIONS[5].X = 1;
        GOAL_POSITIONS[5].Y = 1;
        GOAL_POSITIONS[6].X = 2;
        GOAL_POSITIONS[6].Y = 1;
        GOAL_POSITIONS[7].X = 0;
        GOAL_POSITIONS[7].Y = 2;
        GOAL_POSITIONS[8].X = 1;
        GOAL_POSITIONS[8].Y = 2;
    }

    char input[10];

    printf("Puzzle states (boards) should be entered as a string of 9 numbers, with 0 representing the empty space and each other number being the tiles position. Assume the first place in the string is the top left section of the puzzle, and the last place is the bottom right.\n");
    printf("Enter board string: ");
    fgets(input, sizeof(input), stdin);

    printf("You entered: %s", input);

    return 0;
}