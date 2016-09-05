#
# sudoku.py
# Steve Strain sfstrain@yahoo.com
#
# Unsolved cells are represented by 0
# 3 x 3 sub-units will be referred to as boxes
# Solution must have a number from 1-9 in each cell
# and no duplicates on rows, columns, or in boxes

from collections import defaultdict

puzzle = [[ 0, 0, 2,  0, 0, 7,  0, 0, 9 ],
          [ 0, 8, 0,  0, 2, 0,  0, 5, 0 ],
          [ 7, 0, 0,  1, 0, 0,  4, 0, 0 ],

          [ 5, 0, 0,  8, 0, 0,  6, 0, 0 ],
          [ 0, 9, 0,  0, 3, 0,  0, 1, 0 ],
          [ 0, 0, 4,  0, 0, 6,  0, 0, 8 ],

          [ 0, 0, 7,  0, 0, 4,  0, 0, 5 ],
          [ 0, 1, 0,  0, 5, 0,  0, 4, 0 ],
          [ 8, 0, 0,  6, 0, 0,  2, 0, 0 ]]

   
# row_slices -- column ranges in a row that compose boxes
row_slices = [ (0,3), (3,6), (6,9) ] 


row_boxes = lambda row: [3 * int(row/3) + i for i in range(3) ]
#   row_boxes -- returns list of box numbers spanned by a row
#   Used with row_slices as follows:
#   row = 0, 1, or 2 --> boxes 0, 1, and 2 for cols in row_slices
#   row = 3, 4, or 5 --> boxes 3, 4, and 5 for cols in row_slices
#   row = 6, 7, or 8 --> boxes 6, 7, and 8 for cols in row_slices


# box_num(r,c): Returns the box number for a cell
box_num = lambda r, c: row_boxes(r)[int(c/3)] 


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


def copy_puzzle(puzzle):
    """ copy_puzzle(puzzle): Return deep copy of puzzle
        to avoid side effects in function calls."""

    result = list()
    for row in puzzle:
        result.append(list(row))
    return result


def different_puzzles(puzzle1, puzzle2):
    """ different_puzzles(puzzle1, puzzle2): Return False if 
        puzzle1 and puzzle2 have all the same cell values, else 
        return True."""

    if len(puzzle1) is not len(puzzle2):
        return True
    for row1, row2 in zip(puzzle1, puzzle2):
        if any([ v1 is not v2 for v1, v2 in zip(row1, row2) ]):
            return True
    return False


def get_row_sets(puzzle):
    """ get_row_sets(puzzle): Return a list of sets indexed by row number.
        Sets contain already solved numbers in a row."""

    return [set(row) - {0} for row in puzzle]


def get_col_sets(puzzle):
    """ get_col_sets(puzzle): Return a list of sets indexed by col number.
        Sets contain already solved numbers in a column."""

    return [ set([ row[i] for row in puzzle ]) - {0} for i in range(9) ]


def get_box_sets(puzzle):
    """ get_box_sets(puzzle): Return a list of sets indexed by box number.
        Sets contain already solved numbers in a box."""

    # box_sets: dict needed for updating; convert to list afterwards
    box_sets = dict() 
    for row_num, row in enumerate(puzzle):
        boxes = row_boxes(row_num)
        for box, row_slice in zip(boxes, row_slices):
        # Iterate over the appropriate boxes and slices for this row,
        # updating sets with as needed with already solved numbers
            update = set(row[slice(*row_slice)])
            if box in box_sets:
                box_sets[box].update(update) 
                # set.update(), not dict.update()
            else:
                box_sets[box] = set(update)
    
    result = list()
    for box in range(9):
        result.append(box_sets[box])
        if 0 in result[box]:
            result[box].remove(0)
    
    return result
 

def calculate_possibles(puzzle):
    """ calculate_possibles(puzzle): Return a dictionary keyed on 
        row and column with sets containing possible solutions for 
        each cell."""

    row_sets = get_row_sets(puzzle)
    col_sets = get_col_sets(puzzle)
    box_sets = get_box_sets(puzzle)
    
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
                        - box_sets[box_num(row_num, col_num)]
            result[row_num][col_num] = cell_poss.copy()
    return result


def reduce_singletons(puzzle, possibles):
    """ reduce_singletons(puzzle, possibles): Return puzzle updated
        with new singletons in possibles."""

    result = copy_puzzle(puzzle) 
    for row_num in range(9):
        for col_num in range(9):
            cell_poss = possibles[row_num][col_num].copy()
            # copy() prevents pop() below from mutating possibles
            if len(cell_poss) is 1 and not result[row_num][col_num]:
            # If singleton and the cell is not already solved...
                result[row_num][col_num] = cell_poss.pop()
    return result


def unique_in_row(puzzle, possibles):
    """ unique_on_row(puzzle, possibles): Return puzzle updated
        with solutions for cells with possible values unique 
        to a row."""

    result = copy_puzzle(puzzle)
    for i in range(9):
        pass        

def unique_in_col(puzzle, possibles):
    """ unique_on_row(puzzle, possibles): Return puzzle updated
        with solutions for cells with values unique to a column."""

    result = copy_puzzle(puzzle)
    for col in range(9):
        counts = defaultdict(int)
        for row in range(9):
            if not puzzle[row][col]: # If this is an unsolved cell...
                cell_poss = list(possibles[row][col])
                while len(cell_poss):
                    counts[cell_poss.pop()] += 1
        singletons = [ counts[k] is 1 for k in counts ]
        if any(singletons):
            for k in counts:
                if counts[k] is 1:
                    for row in range(9):
                        if not puzzle[row][col]   \
                        and k in possibles[row][col]:
                            result[row][col] = k
    return result


def unique_in_cells(cells, puzzle, possibles):
    """ unique_in_cells(cells, puzzle, possibles):
        Find unique values in a group of cells
        (row, column, or box). Returns a dictionary
        with the unique value(s), keyed on the cell(s) 
        to be solved."""

    if len(cells) < 9:
        return dict()

    def _copy_cell_sets():
        copy = dict()
        for cell in cell_sets:
            copy[cell] = cell_sets[cell].copy()
        return copy

    cell_sets = dict()
    for cell in cells:
        row, col = cell
        if puzzle[row][col]:
            continue
        cell_sets[cell] = possibles[row][col].copy()
    unique = dict()
    for cell in cell_sets:
        cs_copy = _copy_cell_sets()
        cell_set = cs_copy.pop(cell)
        for k in cs_copy:
            cell_set = cell_set - cs_copy[k]
            if not len(cell_set):
                break
        if len(cell_set):
            unique[cell] = cell_set.pop()
            # TODO: If cell_set is not now empty, 
            #       throw an exception
    return unique


def update_puzzle(strategy, puzzle, possibles):
    return strategy(puzzle, possibles)
    

#path = '/home/stephen/PythonStuff/sudoku/2016_09_03_Sudoku_Evil.txt'
path = '/home/stephen/PythonStuff/sudoku/2016_09_04_Sudoku_Evil.txt'
#path = '/home/stephen/PythonStuff/sudoku/2016_09_04_Websudoku_Easy.txt'
puzzle = load_puzzle(path) 
possibles = calculate_possibles(puzzle)
strategies = [reduce_singletons, unique_in_col]
previous, updated = list(), list()
while different_puzzles(puzzle, previous):
    previous = copy_puzzle(puzzle)
    for strategy in strategies:
        updated = update_puzzle(strategy, puzzle, possibles)
        if not different_puzzles(puzzle, updated):
            continue
        else: 
            puzzle = updated
            possibles = calculate_possibles(puzzle)
