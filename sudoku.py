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
    """load_puzzle(path): Loads puzzle from file path"""
    puzzle = list()
    # Format of puzzle encoding will be as example above
    with open(path) as f:
        lines = f.readlines()
        for row, line in enumerate(lines):
            puzzle.append([int(s) for s in list(line.strip())])
    return puzzle

def get_row_sets(puzzle):
    return [set(row) - {0} for row in puzzle]


def get_col_sets(puzzle):
    return [ set([ row[i] for row in puzzle ]) - {0} for i in range(9) ]


row_slices = [ (0,3), (3,6), (6,9) ] # column ranges in a row that compose boxes
row_boxes = lambda row: [3 * int(row/3) + i for i in range(3) ]
#   row = 0, 1, or 2 --> boxes 0, 1, and 2 for cols in row_slices
#   row = 3, 4, or 5 --> boxes 3, 4, and 5 for cols in row_slices
#   row = 6, 7, or 8 --> boxes 6, 7, and 8 for cols in row_slices

def get_box_sets(puzzle):
    box_sets = dict()
    for row_num, row in enumerate(puzzle):
        boxes = row_boxes(row_num)
        for box, row_slice in zip(boxes, row_slices):
            update = set(row[slice(*row_slice)])
            if box in box_sets:
                box_sets[box].update(update) # set.update(), not dict.update()
            else:
                box_sets[box] = set(update)
    
    result = list()
    for box in range(9):
        result.append(box_sets[box])
        result[box].remove(0)
    
    return result
 


def calculate_possibles(puzzle):
    #   Produce 3 sets from solved cells, 1 each for rows, columns, and boxes
    #   Sets will be in lists, indexed by row, column, or box number
    #strip_set = lambda s: set(s) - {0}
    #row_sets = [ strip_set(row) for row in puzzle ] 
    #col_sets = [ strip_set([ row[i] for row in puzzle ])
    #             for i in range(9) ]
    row_sets = get_row_sets(puzzle)
    col_sets = get_col_sets(puzzle)
    box_sets = get_box_sets(puzzle)
    
#    box_sets = dict()   # Need to access out of order
#                        # Convert to list later
#    row_slices = [ (0,3), (3,6), (6,9) ] # col_nums that compose boxes on a row
#    row_boxes = lambda rnum: [3 * int(rnum/3) + i for i in range(3) ]
#    #   rnum = 0, 1, or 2 --> boxes 0, 1, and 2 for cols in row_slices
#    #   rnum = 3, 4, or 5 --> boxes 3, 4, and 5 for cols in row_slices
#    #   rnum = 6, 7, or 8 --> boxes 6, 7, and 8 for cols in row_slices
#    for row_num, row in enumerate(puzzle):
#        boxes = row_boxes(row_num)
#        for box, row_slice in zip(boxes, row_slices):
#            update = set(row[slice(*row_slice)])
#            if box in box_sets:
#                box_sets[box].update(update) # set.update(), not dict.update()
#            else:
#                box_sets[box] = set(update)
#    
#    bx_sets = list()
#    for box in range(9):
#        bx_sets.append(box_sets[box])
#        bx_sets[box].remove(0)
#    
#    box_sets = bx_sets
    
    possibles = dict()
    box_num = lambda r, c: row_boxes(r)[int(c/3)]
    for row_num in range(9):
        possibles[row_num] = dict()
        for col_num in range(9):
            cell = puzzle[row_num][col_num] 
            if cell > 0:
                possibles[row_num][col_num] = {cell}
                continue
            cell_poss = set(range(1, 10)) - row_sets[row_num] \
                        - col_sets[col_num] \
                        - box_sets[box_num(row_num, col_num)]
            possibles[row_num][col_num] = cell_poss.copy()
            #if len(cell_poss) is 1:
                #puzzle[row_num][col_num] = cell_poss.pop()
    return possibles


def scan_possibles(puzzle, possibles):
    result = list() 
    for row_num in range(9):
        result.append(list(puzzle[row_num]))
        for col_num in range(9):
            cell_poss = possibles[row_num][col_num].copy()
            if len(cell_poss) is 1:
                result[row_num][col_num] = cell_poss.pop()
    return result


def different_puzzles(puzzle1, puzzle2):
    for row1, row2 in zip(puzzle1, puzzle2):
        for col in range(9):
            if row1[col] is not row2[col]:
                return True
    return False


def update_puzzle(func, puzzle, possibles):
    pass
    

#path = '/home/stephen/PythonStuff/sudoku/2016_09_03_Sudoku_Evil.txt'
path = '/home/stephen/PythonStuff/sudoku/2016_09_04_Sudoku_Evil.txt'
puzzle = load_puzzle(path) 
possibles = calculate_possibles(puzzle)
updated = scan_possibles(puzzle, possibles)
while different_puzzles(puzzle, updated):
    puzzle = updated
    possibles = calculate_possibles(puzzle)
    updated = scan_possibles(puzzle, possibles)
