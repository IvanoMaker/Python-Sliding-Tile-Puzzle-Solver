# helper script used to generate all the valid permutations for the sliding tile puzzle (3x3)
import itertools

tiles = [1, 2, 3, 4, 5, 6, 7, 8, 0]          # tiles (0 is considered None)
perms = list(itertools.permutations(tiles))  # generate the permutations

# is solvable function for determining solvability
def is_solvable(perm):
    inv_count = 0                                                      # inversion count
    for i in range(len(perm)):                                         # iterate through the permutations two at a time
        for j in range(i + 1, len(perm)):
            if perm[i] != 0 and perm[j] != 0 and perm[i] > perm[j]:    # check in an inversion is found
                inv_count += 1                                         # increment if so
    return inv_count % 2 == 0                                          # a board is solvable if the inversion count is even

# reset perms to only contain solvable permutations
perms = [p for p in perms if is_solvable(p)]

# open 'permutations.txt' file and write the permutations to it
with open('permutations.txt', 'w') as f:
    for p in perms:
        str_lst = [str(x) for x in p]           # concatenate the elements of the permutation to a string
        f.write("".join(str_lst) + ":" + '\n')  # add placeholder ':'
