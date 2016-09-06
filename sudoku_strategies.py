#from collections import defaultdict
import sudoku_utils as su

def reduce_singletons(puzzle, possibles):
    """ reduce_singletons(puzzle, possibles): Return puzzle updated
        with new singletons in possibles."""

    result = su.copy_puzzle(puzzle) 
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

    result = su.copy_puzzle(puzzle)
    for i in range(9):
        cells = su.row_cells(i)
        uniques = unique_in_cells(cells, puzzle, possibles)
        if uniques:
            for cell in uniques:
                row, col = cell
                result[row][col] = uniques[cell]
    return result

def unique_in_col(puzzle, possibles):
    """ unique_in_col(puzzle, possibles): Return puzzle updated
        with solutions for cells with possible values unique
        to a column."""

    result = su.copy_puzzle(puzzle)
    for i in range(9):
        cells = su.col_cells(i)
        uniques = unique_in_cells(cells, puzzle, possibles)
        if uniques:
            for cell in uniques:
                row, col = cell
                result[row][col] = uniques[cell]
    return result


def unique_in_box(puzzle, possibles):
    """ unique_in_box(puzzle, possibles): Return puzzle updated
        with solutions for cells with possible values unique
        to a column."""

    result = su.copy_puzzle(puzzle)
    for i in range(9):
        cells = su.box_cells(i)
        uniques = unique_in_cells(cells, puzzle, possibles)
        if uniques:
            for cell in uniques:
                row, col = cell
                result[row][col] = uniques[cell]
    return result


def unique_in_cells(cells, puzzle, possibles):
    """ unique_in_cells(cells, puzzle, possibles):
        Find unique values in a group of cells.
        Returns a dictionary with the unique
        value(s), keyed on the cell(s) to be solved."""

    if len(cells) < 2:
        return dict()

    cell_sets = dict()
    def _copy_cell_sets():
        copy = dict()
        for cell in cell_sets:
            copy[cell] = cell_sets[cell].copy()
        return copy

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



