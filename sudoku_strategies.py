from collections import defaultdict
from itertools import product
import sudoku_utils as su


def calculate_possibles(puzzle):
    """ calculate_possibles(puzzle): Return a dictionary keyed on 
        cell tuples with sets containing possible solutions for 
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
                            - col_sets[col] \
                            - box_sets[su.box_num(row, col)]
    return result


def reduce_singletons(puzzle, possibles):
    """ reduce_singletons(puzzle, possibles): Return puzzle updates
        for new singletons in possibles."""

    result = dict()
    for cell in product(range(9), range(9)):
        if cell in possibles:
            cell_poss = list(possibles[cell])
            if len(cell_poss) is 1 and not puzzle[cell]:
                result[cell] = cell_poss[0]
    return result


def reduce_uniques(puzzle, possibles):
    """ reduce_uniques(puzzle, possibles): Return puzzle updates
        for solution of cells with values unique to rows, columns, 
        and boxes."""

    result = dict()
    def _uniquify_cells(cells):
        uniques = unique_in_cells(cells, possibles)
        if uniques:
            for cell in uniques:
                result[cell] = uniques[cell]
    
    for i in range(9):
        cell_groups = [ list(it) for it in (su.row_cells(i),
                                            su.col_cells(i),
                                            su.box_cells(i)) ]
        for cells in cell_groups:
            _uniquify_cells(cells)
    return result

    
def unique_in_cells(cells, possibles):
    """ unique_in_cells(cells, possibles):
        Find unique values in a group of cells.
        Returns a dictionary with the unique value(s), 
        keyed on the cell(s) with the value(s)."""

    if len(cells) < 2:
        return dict()
    uniques = dict()
    counts = poss_counts_in_cells(cells, possibles)
    if 1 in counts.values():
        uniq_digits = set([ digit for digit in counts
                              if counts[digit] is 1 ])
        for cell in cells:
            if cell in possibles \
                    and possibles[cell].intersection(uniq_digits):
                uniq_digit = possibles[cell].intersection(uniq_digits)
                uniques[cell] = uniq_digit.pop()
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