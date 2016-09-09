# sudoku.py
# Steve Strain sfstrain@yahoo.com
#
# Unsolved cells are represented by 0
# 3 x 3 sub-units will be referred to as boxes
# Solution must have a number from 1-9 in each cell
# and no duplicates on rows, columns, or in boxes

import sudoku_utils as su
import sudoku_strategies as strat
from copy import deepcopy

#path = '/home/stephen/PythonStuff/sudoku_git/2016_09_03_Sudoku_Evil.txt'
path = '/home/stephen/PythonStuff/sudoku_git/2016_09_04_Sudoku_Evil.txt'
#path = '/home/stephen/PythonStuff/sudoku_git/2016_09_04_Websudoku_Easy.txt'
#path = '/home/stephen/PythonStuff/sudoku_git/2016_09_05_Websudoku_Medium.txt'
#path = '/home/stephen/PythonStuff/sudoku_git/2016_09_05_Websudoku_Medium_2.txt'
#path = '/home/stephen/PythonStuff/sudoku_git/2016_09_05_Websudoku_Hard.txt'
#path = '/home/stephen/PythonStuff/sudoku_git/puzzle.txt'


def update_puzzle(strategy, puzzle, possibles):
    updated = False
    updates = strategy(puzzle, possibles)
    if updates:
        updated = True
    for cell in updates:
        puzzle[cell] = updates[cell]
    return updated
          
        
puzzle = su.load_puzzle(path)
possibles = strat.calculate_possibles(puzzle)
strategies = [strat.reduce_singletons, strat.reduce_uniques]
previous, updated = dict(), dict()
su.pretty(puzzle, possibles)
while su.different_puzzles(puzzle, previous):
    previous = deepcopy(puzzle)
    for strategy in strategies:
        updated = update_puzzle(strategy, puzzle, possibles)
        if not updated:
            continue
        else: 
            possibles = strat.calculate_possibles(puzzle)
            print
            print '=====     ' + strategy.__name__ + '     ====='
            su.pretty(puzzle, possibles)
