
# sudoku.py
# Steve Strain sfstrain@yahoo.com
#
# Unsolved cells are represented by 0
# 3 x 3 sub-units will be referred to as boxes
# Solution must have a number from 1-9 in each cell
# and no duplicates on rows, columns, or in boxes

from itertools import product
import sudoku_utils as su
import sudoku_strategies as strat

def load_puzzle(path):
    """ load_puzzle(path): Return puzzle from file path.
        path should be text, 9 lines long, with exactly nine 
        digits on each line, and zeros for unsolved cells."""

    # TODO: try/except, validate_puzzle() before returning

    puzzle = list()
    with open(path) as f:
        lines = f.readlines()
        for row, line in enumerate(lines):
            puzzle.append([int(s) for s in list(line.strip())])
    return su.puzzle_by_cell(puzzle)


def calculate_possibles(puzzle):
    """ calculate_possibles(puzzle): Return a dictionary keyed on 
        row and column with sets containing possible solutions for 
        each cell."""

    row_sets = su.get_row_sets(puzzle)
    col_sets = su.get_col_sets(puzzle)
    box_sets = su.get_box_sets(puzzle)

    result = dict()
    for cell in product(range(9),range(9)):
        cell_content = puzzle[cell] 
        if cell_content > 0: 
            continue
        row, col = cell
        result[cell] = set(range(1, 10)) - row_sets[row] \
                            - col_sets[col] - box_sets[su.box_num(row, col)]
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
strategies = [strat.reduce_singletons, strat.reduce_uniques]
previous, updated = dict(), dict()
while su.different_puzzles(puzzle, previous):
    previous = su.copy_puzzle(puzzle)
    for strategy in strategies:
        updated = update_puzzle(strategy, puzzle, possibles)
        if not su.different_puzzles(puzzle, updated):
            continue
        else: 
            puzzle = updated
            possibles = calculate_possibles(puzzle)
