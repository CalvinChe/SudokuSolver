class Grid:
    def __init__(self, grid):
        self.grid = grid
    
    def setNum(self, Num, row, col):
        self.grid[row][col] = Num

def printGrid(grid):
    for i in range(9): 
        for j in range(9): 
            print(grid[i][j], end = ' ')
            if ((j+1) % 3 == 0) & (j != 8):
                print('|', end = '')
        if (i+1)% 3 == 0:
            print()
        print()

def isValid(grid, num, x, y):
    #row
    if num in grid[x]:
        return False

    #column
    for row in grid:
        if row[y] == num:
            return False

    #boxes
    xBox = int(x/3) * 3
    yBox = int(y/3) * 3
    for row in range(3):
        for col in range(3):
            if grid[xBox+row][yBox+col] == num:
                return False
    
    return True

def step(x, y):
    y += 1
    if (y == 9):
        x += 1
        y = 0
    return x,y

def dokuHelper(grid, validNums, x, y):

    if (x == 9):
        return True
    
    #print((x, y))
    if (grid[x][y] == 0):
        for i in range(9):
            if(isValid(grid, validNums[i], x, y)):
                grid[x][y] = validNums[i]
                newX, newY = step(x, y)
                if (dokuHelper(grid, validNums, newX, newY)):
                    return True
        grid[x][y] = 0
    else:
        newX, newY = step(x,y)
        if (dokuHelper(grid, validNums, newX, newY)):
            return True

    return False

def dokuSolver(grid):
    printGrid(grid)
    validNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if(dokuHelper(grid, validNums, x=0, y=0)):
        printGrid(grid)
        #x = 1
    else:
        print("Solution does not exist")

if __name__ == "__main__":
    #grid = [[0 for i in range(9)] for j in range(9)]
    grid = [[4, 0, 0, 8, 0, 6, 0, 0, 5], [0, 0, 5, 9, 7, 4, 6, 0, 0], [0, 1, 0, 0, 0, 0, 0, 8, 0], [5, 4, 0, 7, 0, 1, 0, 6, 8], [0, 9, 0, 0, 0, 0, 0, 1, 0], [6, 2, 0, 5, 0, 8, 0, 7, 4], [0, 6, 0, 0, 0, 0, 0, 4, 0], [0, 0, 8, 6, 4, 2, 1, 0, 0], [1, 0, 0, 3, 0, 9, 0, 0, 6]]
    dokuSolver(grid)
    print(grid)