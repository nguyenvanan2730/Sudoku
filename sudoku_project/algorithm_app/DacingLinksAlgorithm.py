class DancingLinksSudokuSolver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.solutions = []

    def solve(self):
        # Create a sparse matrix for the puzzle
        matrix = self.create_matrix()

        # Create a doubly-linked list for the matrix
        head = self.create_linked_list(matrix)

        # Search for solutions using backtracking
        self.search(head, [])

        return self.solutions

    def create_matrix(self):
        # Create a matrix with 4 rows for each cell in the puzzle:
        # one for the row constraint, one for the column constraint,
        # one for the box constraint, and one for the cell value
        matrix = [[0] * 324 for _ in range(729)]

        # Fill in the matrix with the constraints and cell values
        for i in range(9):
            for j in range(9):
                value = self.puzzle[i][j]

                if value:
                    # The cell has a value, so we only need to fill in
                    # the row, column, and box constraints
                    row = i * 9 + value - 1
                    col = j * 9 + value - 1
                    box = (i // 3) * 3 + (j // 3) * 27 + value - 1

                    matrix[row][i * 9 + j] = 1
                    matrix[col + 81][i * 9 + j] = 1
                    matrix[box + 162][i * 9 + j] = 1
                else:
                    # The cell is empty, so we need to fill in all
                    # possible values for the cell
                    for value in range(1, 10):
                        row = i * 9 + value - 1
                        col = j * 9 + value - 1
                        box = (i // 3) * 3 + (j // 3) * 27 + value - 1

                        matrix[row][i * 9 + j] = 1
                        matrix[col + 81][i * 9 + j] = 1
                        matrix[box + 162][i * 9 + j] = 1
                        matrix[243 + i * 9 + j][i * 9 + j] = 1

        return matrix

    def create_linked_list(self, matrix):
        # Create a dummy node for the head of the linked list
        head = Node(-1, -1, None, None, None, None)

        # Create a node for each column in the matrix
        cols = [Node(i, 0, head, None, None, None) for i in range(324)]
        head.right = cols[0]
        head.left = cols[-1]
        cols[0].left = head
        cols[-1].right = head

        # Create a node for each row in the matrix
        for i in range(729):
            prev = None
            left = cols[-1]

            for j in range(324):
                if matrix[i][j]:
                    node = Node(j, i, cols[j], None, prev, left)

                    if prev:
                        prev.down = node
                    else:
                        #vanan wrong colum
                        cols[j].up =1


class Node:
    def __init__(self, col, row, right, left, up, down):
        self.col = col
        self.row = row
        self.right = right
        self.left = left
        self.up = up
        self.down = down
