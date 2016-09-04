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

#path = '/home/stephen/2016_09_03_Sudoku_Evil'
path = '/home/stephen/2016_09_04_Sudoku_Evil'
puzzle = load_puzzle(path) 

#   Produce 3 sets from solved cells, 1 each for rows, columns, and boxes
#   Sets will be in lists, indexed by row, column, or box number
strip_set = lambda s: set(s) - {0}
row_sets = [ strip_set(row) for row in puzzle ] 
col_sets = [ strip_set([ row[i] for row in puzzle ])
             for i in range(9) ]

box_sets = dict()   # Need to access out of order
                    # Convert to list later
row_slices = [ (0,3), (3,6), (6,9) ] # col_nums that compose boxes on a row
row_boxes = lambda rnum: [3 * int(rnum/3) + i for i in range(3) ]
#   rnum = 0, 1, or 2 --> boxes 0, 1, and 2 for cols in row_slices
#   rnum = 3, 4, or 5 --> boxes 3, 4, and 5 for cols in row_slices
#   rnum = 6, 7, or 8 --> boxes 6, 7, and 8 for cols in row_slices
for row_num, row in enumerate(puzzle):
    boxes = row_boxes(row_num)
    for box, row_slice in zip(boxes, row_slices):
        update = set(row[slice(*row_slice)])
        if box in box_sets:
            box_sets[box].update(update) # set.update(), not dict.update()
        else:
            box_sets[box] = set(update)

bx_sets = list()
for box in range(9):
    bx_sets.append(box_sets[box])
    bx_sets[box].remove(0)

box_sets = bx_sets

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
        if len(cell_poss) is 1:
            puzzle[row_num][col_num] = cell_poss.pop()
