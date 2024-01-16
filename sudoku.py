import collections, random, copy

class Game:
    def __init__(self):
        self.generateGrid()
        self.base = copy.deepcopy(self.grid)
        self.printGrid()

    # Prints the grid out to the console.
    def printGrid(self):
        print("-" * 21)
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("- - -   - - -   - - -")
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("| ", end = "")
                
                if j == 8:
                    print(self.grid[i][j])
                else:
                    print(str(self.grid[i][j]) + " ", end = "")
        print("-" * 21)
        # print("\n")

    # adds num into the row and column of grid
    def inputCell(self, x, y, num):
        self.grid[x][y] = num
        self.printGrid()

    # Checks the full grid to see if the answer is valid.
    def validAnswer(self):
        row = collections.defaultdict(set)
        col = collections.defaultdict(set)
        box = collections.defaultdict(set)
        for i in range(9):
            for j in range(9):
                num = self.grid[i][j]

                if num == 0:
                    continue

                numBox = (i // 3, j // 3)
                if num in row[i] or num in col[j] or num in box[numBox]:
                    return False
                else:
                    row[i].add(num)
                    col[j].add(num)
                    box[numBox].add(num)
        
        return True

    # Checks if the number we place into the answer is valid.
    def isValid(self, row, col, num):
        self.grid[row][col] = 0
        for i in range(9):
            if self.grid[i][col] == num:
                return False
            if self.grid[row][i] == num:
                return False
            if self.grid[3 * (row // 3) + i // 3][3 * (col // 3) + i % 3] == num:
                return False
        self.grid[row][col] = num
        return True

    # Solves the Sudoku Grid Recursively.
    def solve(self, row, col):
        if row == 9:
            return True
        if col == 9:
            return self.solve(row + 1, 0)
        
        if self.grid[row][col] == 0:
            for i in range(1, 10):
                if self.isValid(row, col, i):
                    self.grid[row][col] = i
                    if self.solve(row, col + 1):
                        return True
                    else:
                        self.grid[row][col] = 0
            return False
        else:
            return self.solve(row, col + 1)

    # generates a new playable sudoku grid.
    def generateGrid(self):
        self.resetGrid()
        self.solve(0,0)
        self.swapNum()
        self.eraseRandomSquares(50)
        self.base = copy.deepcopy(self.grid)

    # creates a grid of all zeros.
    def resetGrid(self):
        self.grid = [[0] * 9 for _ in range(9)]

    # Helper function which generates a number map by shuffling an 
    # list of numbers and zipping them together.
    # returns a dictionary, the mapping of the numbers.
    def generateNumMap(self):
        nums = list(range(1,10))
        random.shuffle(nums)
        nums_map = dict(zip(range(1, 10), nums))
        return nums_map

    # Swap the numbers according to a generated map.
    def swapNum(self):
        map = self.generateNumMap()
        for i in range(9):
            for j in range(9):
                self.grid[i][j] = map[self.grid[i][j]]

    # removes random squares from the sudoku grid.
    def eraseRandomSquares(self, numSquares):
        currSquare = [(i,j) for j in range(9) for i in range(9)]
        for _ in range(min(len(currSquare), numSquares)):
            row, col = random.choice(currSquare)
            self.grid[row][col] = 0
            currSquare.remove((row, col))

if __name__ == "__main__":
    game = Game()
    game.solve(0,0)
    game.printGrid()