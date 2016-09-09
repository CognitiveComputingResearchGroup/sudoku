BOX_SLICES = [ (0,3), (3,6), (6,9) ] 
row_boxes = lambda row: [3 * int(row/3) + i for i in range(3) ]
box_num = lambda r, c: row_boxes(r)[int(c/3)] 


def row_cells(row):
    """ row_cells(row): Iterates over the cells that 
        form a row in a sudoku puzzle."""
    for col in range(9):
        yield (row, col)
        

def col_cells(col):
    """ col_cells(col): Iterates over the cells that 
        form a column in a sudoku puzzle."""
    for row in range(9):
        yield (row, col)


def box_cells(box): 
    """ box_cells(box): Iterates over the cells that 
        form a box in sudoku puzzle."""
    start_row, stop_row = BOX_SLICES[int(box/3)]
    start_col, stop_col = BOX_SLICES[box % 3]
    for row in range(start_row, stop_row):
        for col in range(start_col, stop_col):
            yield (row, col)


def get_row_sets(puzzle):
    """ get_row_sets(puzzle): Return a list of sets indexed by row number.
        Sets contain already solved numbers in a row."""
    puzzle_rows = [ [ puzzle[cell] for cell in row_cells(row) ] for row in range(9) ]
    return [set(puzzle_row) - {0} for puzzle_row in puzzle_rows ]


def get_col_sets(puzzle):
    """ get_col_sets(puzzle): Return a list of sets indexed by col number.
        Sets contain already solved numbers in a column."""
    puzzle_rows = [[puzzle[cell] for cell in row_cells(row)] for row in range(9)]
    return [ set([ puzzle_row[i] for puzzle_row in puzzle_rows ]) - {0} for i in range(9) ]


def get_box_sets(puzzle):
    """ get_box_sets(puzzle): Return a list of sets indexed by box number.
        Sets contain already solved numbers in a box."""
    box_sets = dict()
    puzzle_rows = [[puzzle[cell] for cell in row_cells(row)] for row in range(9)]
    for row, puzzle_row in enumerate(puzzle_rows):
        boxes = row_boxes(row)
        for box, row_slice in zip(boxes, BOX_SLICES):
            update = set(puzzle_row[slice(*row_slice)])
            if box in box_sets:
                box_sets[box].update(update) 
            else:
                box_sets[box] = set(update)
    result = list()
    for box in range(9):
        result.append(box_sets[box])
        if 0 in result[box]:
            result[box].remove(0)
    return result
 

def different_puzzles(puzzle1, puzzle2):
    """ different_puzzles(puzzle1, puzzle2): Return False if 
        puzzle1 and puzzle2 have all the same cell values, else 
        return True."""
    if len(puzzle1) is not len(puzzle2):
        return True
    for cell in puzzle1:
        if puzzle1[cell] is not puzzle2[cell]:
            return True
    return False


def unsolved(cells, puzzle):
    """ unsolved(cells, puzzle): Iterates over that subset of 
        cells for which the puzzle does not yet have solutions. """
    for cell in cells:
        if puzzle[cell]:
            continue
        yield cell


def puzzle_by_cell(puzzle):
    """ puzzle_by_cell(puzzle): Return a dictionary,
        keyed on cell tuples, as an alternative
        representation for a puzzle."""
    result = dict()
    for row, puzzle_row in enumerate(puzzle):
        for col in range(9):
            result[(row, col)] = puzzle_row[col]
    return result


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
    return puzzle_by_cell(puzzle)


def pretty(puzzle, possibles):
    """ pretty(puzzle, possibles): Pretty print the puzzle
        and the sets of possible values for unsolved cells."""
    def pretty_puzzle(puzzle):
        def _row_iter(row):
            for cell in [ (row, col) for col in range(9) ]:
                if puzzle[cell]:
                    yield str(puzzle[cell])
                else:
                    yield '-'
        result = []
        fmt = '| {} {} {} | {} {} {} | {} {} {} |'
        divider = '========' * 3 + '='
        for row in range(9):
            if not row % 3:
                result.append(divider)
            result.append(fmt.format(*tuple(_row_iter(row))))
        result.append(divider)
        return result
    
    def pretty_possibles(possibles):
        def _row_iter(row):
            for cl in [ (row, col) for col in range(9) ]:
                if cl in possibles:
                    yield ''.join(str(d) for d in sorted(possibles[cl]))
                else:
                    yield '---'
        result = []
        cell_fmt = '{:^6}|'
        box_fmt = 3 * cell_fmt + '|'
        fmt = '||' + 3 * box_fmt 
        divider = '=======' * 9 + '====='
        for row in range(9):
            if not row % 3:
                result.append(divider)
            cells = []
            for idx, s in enumerate(_row_iter(row)):
                cells.append(s)
            result.append(fmt.format(*tuple(cells)))
        result.append('=======' * 9)
        return result
    
    for line in pretty_puzzle(puzzle):
        print line
    for line in pretty_possibles(possibles):
        print line

