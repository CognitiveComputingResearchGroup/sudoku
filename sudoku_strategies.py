from collections import defaultdict
from itertools import product
import sudoku_utils as su


def reduce_singletons(puzzle, possibles):
    """ reduce_singletons(puzzle, possibles): Return puzzle updated
        with new singletons in possibles."""

    result = su.copy_puzzle(puzzle)
    for cell in product(range(9), range(9)):
        if cell in possibles:
            cell_poss = list(possibles[cell])
            if len(cell_poss) is 1 and not result[cell]:
                result[cell] = cell_poss[0]
        else:
            result[cell] = puzzle[cell]
    return result


def reduce_uniques(puzzle, possibles):
    """ reduce_uniques(puzzle, possibles): Return puzzle 
        with values unique to rows, columns, and boxes solved."""

    result = su.copy_puzzle(puzzle)
    def _uniquify_cells(cells):
        uniques = unique_in_cells(cells, possibles)
        if uniques:
            for cell in uniques:
                result[cell] = uniques[cell]
    
    for i in range(9):
        cell_groups = [ list(it) for it in (su.row_cells(i), su.col_cells(i), su.box_cells(i)) ]
        for cells in cell_groups:
            _uniquify_cells(cells)
    return result

    
def unique_in_cells(cells, possibles):
    """ unique_in_cells(cells, possibles):
        Find unique values in a group of cells.
        Cells are referenced by (row, column) tuples.
        Returns a dictionary with the unique
        value(s), keyed on the cell(s) to be solved."""

    if len(cells) < 2:
        return dict()
    uniques = dict()
    counts = poss_counts_in_cells(cells, possibles)
    if 1 in counts.values():
        unique_digits = set([ digit for digit in counts if counts[digit] is 1 ])
        for cell in cells:
            if cell in possibles and possibles[cell].intersection(unique_digits):
                unique_digit = possibles[cell].intersection(unique_digits)
                uniques[cell] = unique_digit.pop()
    return uniques


def poss_counts_in_cells(cells, possibles):
    """ poss_counts_in_cells(cells, possibles):
        Counts the number of times values occur in
        a group of cells. Returns the results in 
        a dictionary keyed on those values."""

    result = defaultdict(int)
    for cell in cells:
        if cell not in possibles:
            continue
        for poss in possibles[cell]:
            result[poss] += 1
    return result


