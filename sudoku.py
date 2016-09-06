
# sudoku.py
# Steve Strain sfstrain@yahoo.com
#
# Unsolved cells are represented by 0
# 3 x 3 sub-units will be referred to as boxes
# Solution must have a number from 1-9 in each cell
# and no duplicates on rows, columns, or in boxes

import sudoku_utils as su
import sudoku_strategies as strat

puzzle = [[ 0, 0, 2,  0, 0, 7,  0, 0, 9 ],
          [ 0, 8, 0,  0, 2, 0,  0, 5, 0 ],
          [ 7, 0, 0,  1, 0, 0,  4, 0, 0 ],

          [ 5, 0, 0,  8, 0, 0,  6, 0, 0 ],
          [ 0, 9, 0,  0, 3, 0,  0, 1, 0 ],
          [ 0, 0, 4,  0, 0, 6,  0, 0, 8 ],

          [ 0, 0, 7,  0, 0, 4,  0, 0, 5 ],
          [ 0, 1, 0,  0, 5, 0,  0, 4, 0 ],
          [ 8, 0, 0,  6, 0, 0,  2, 0, 0 ]]

   
def load_puzzle(path):
    """ load_puzzle(path): Return puzzle from file path.
        path should be text, 9 lines long, with exactly nine 
        digits on each line, and zeros for unsolved cells."""

    # TODO: try/except, validate_puzzle() before returning

    puzzle = list()
    # Encoding of returned puzzle will be as in example above
    with open(path) as f:
        lines = f.readlines()
        for row, line in enumerate(lines):
            puzzle.append([int(s) for s in list(line.strip())])
    return puzzle


def calculate_possibles(puzzle):
    """ calculate_possibles(puzzle): Return a dictionary keyed on 
        row and column with sets containing possible solutions for 
        each cell."""

    row_sets = su.get_row_sets(puzzle)
    col_sets = su.get_col_sets(puzzle)
    box_sets = su.get_box_sets(puzzle)
    
    result = dict()
    for row_num in range(9):
        result[row_num] = dict()
        for col_num in range(9):
            cell = puzzle[row_num][col_num] 
            if cell > 0: # If cell is solved...
                result[row_num][col_num] = {cell}
                continue
            # Use set differences to determine possible solutions for cell
            # Remove all numbers in the same row, column, and box
            cell_poss = set(range(1, 10)) - row_sets[row_num] \
                        - col_sets[col_num] \
                        - box_sets[su.box_num(row_num, col_num)]
            result[row_num][col_num] = cell_poss.copy()
    return result


def update_puzzle(strategy, puzzle, possibles):
    return strategy(puzzle, possibles)
    

#path = '/home/stephen/PythonStuff/sudoku_git/2016_09_03_Sudoku_Evil.txt'
#path = '/home/stephen/PythonStuff/sudoku_git/2016_09_04_Sudoku_Evil.txt'
#path = '/home/stephen/PythonStuff/sudoku_git/2016_09_04_Websudoku_Easy.txt'
#path = '/home/stephen/PythonStuff/sudoku_git/2016_09_05_Websudoku_Medium.txt'
#path = '/home/stephen/PythonStuff/sudoku_git/2016_09_05_Websudoku_Medium_2.txt'
path = '/home/stephen/PythonStuff/sudoku_git/2016_09_05_Websudoku_Hard.txt'
puzzle = load_puzzle(path) 
possibles = calculate_possibles(puzzle)
strategies = [strat.reduce_singletons, strat.unique_in_col, strat.unique_in_row]
previous, updated = list(), list()
while su.different_puzzles(puzzle, previous):
    previous = su.copy_puzzle(puzzle)
    for strategy in strategies:
        updated = update_puzzle(strategy, puzzle, possibles)
        if not su.different_puzzles(puzzle, updated):
            continue
        else: 
            puzzle = updated
            possibles = calculate_possibles(puzzle)
