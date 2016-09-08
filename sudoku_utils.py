# BOX_SLICES -- column ranges in a row that compose boxes, or
#               (also) row ranges in a column that compose boxes
BOX_SLICES = [ (0,3), (3,6), (6,9) ] 


row_boxes = lambda row: [3 * int(row/3) + i for i in range(3) ]
#   row_boxes -- returns list of box numbers spanned by a row
#   Used with BOX_SLICES as follows:
#   row = 0, 1, or 2 --> boxes 0, 1, and 2 for cols in BOX_SLICES
#   row = 3, 4, or 5 --> boxes 3, 4, and 5 for cols in BOX_SLICES
#   row = 6, 7, or 8 --> boxes 6, 7, and 8 for cols in BOX_SLICES


# box_num(r,c): Returns the box number for a cell
box_num = lambda r, c: row_boxes(r)[int(c/3)] 


def row_cells(row):
    """ row_cells(row): Return a set a tuples giving the cells
        that form a row in puzzle."""

    return set((row,col) for col in range(9))
        

def col_cells(col):
    """ col_cells(col): Return a set a tuples giving the cells
        that form a column in puzzle."""

    return set((row, col) for row in range(9))


def box_cells(box): 
    """ box_cells(box): Return a set a tuples giving the cells
        that form a box in puzzle."""

    start_row, stop_row = BOX_SLICES[int(box/3)]
    start_col, stop_col = BOX_SLICES[box % 3]
    return set((row, col) for row in range(start_row, stop_row)
                    for col in range(start_col, stop_col))


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
        for box, row_slice in zip(boxes, BOX_SLICES):
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


def unsolved(cells, puzzle):
    """ unsolved(cells, puzzle): Returns that subset of cells
        for which the puzzle does not yet have solutions. """

    result = set()
    for cell in cells:
        row, col = cell
        if puzzle[row][col]:
            continue
        result.add(cell)
    return result


def puzzle_by_cell(puzzle):
    """ puzzle_by_cell(puzzle): Return a dictionary,
        keyed on cell tuples, as an alternative
        representation for a puzzle."""

    result = dict()
    for row, puzzle_row in enumerate(puzzle):
        for col in range(9):
            result[(row, col)] = puzzle_row[col]
    return result
