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

    return 0;
}