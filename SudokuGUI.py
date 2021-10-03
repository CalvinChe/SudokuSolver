import os, sys
import pygame as pg
from pygame.locals import *

# Global Variables
WIDTH = 800
HEIGHT = 900
FRAME_RATE = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (211, 211, 211)
BLUE = (0, 0, 255)
EFONT = None

# Global Functions
def displayText(text, size, coord, surface, centered=False, colour=BLACK):
    font = pg.font.Font(EFONT, size)
    t = font.render(text, True, colour)
    tA = t.get_rect()
    if centered:
        tA.centerx = coord[0]
        tA.centery = coord[1]
    else:
        tA.left = coord[0]
        tA.top = coord[1]
    surface.blit(t, tA)

class Square():    
    def __init__(self, x, y, num,locked=False):
        self.x = x
        self.y = y
        self.num = (num)
        self.locked = locked

    def setNum(self, num):
        self.num = num

class Grid():
    line_width = 2
    margin = 10
    leftMargin = WIDTH // margin
    topMargin = HEIGHT // margin // 2
    squareLength = WIDTH - leftMargin*2
    blockLength = squareLength // 9
    blockCentre = blockLength // 2
    rightMargin = leftMargin + squareLength
    bottomMargin = topMargin + squareLength

    def __init__(self):
        self.grid = []
        self.x = 0
        self.y = 0
        self.xPos = 0
        self.yPos = 0
        self.selected = False

    # import a grid
    def newGame(self, grid):
        for x in range(9):
            self.grid.append([])
            for y in range(9):
                if grid[x][y] != 0:
                    self.grid[x].append(Square(x, y, grid[x][y], True))
                else:
                    self.grid[x].append(Square(x,y, grid[x][y]))

    # Draw the Grid on the background
    def drawGridLine(self, background):
        for x in range(10):
            # Bold every third line for clarity
            if x % 3 == 0:
                line_width = 4
            else:
                line_width = 2
            
            # Distance from Start to the next line
            distance = self.blockLength * x
            
            # Draw Column Lines
            cLine = self.leftMargin + distance
            pg.draw.line(background, BLACK, (cLine, self.topMargin), (cLine, self.bottomMargin), line_width)
            
            # Draw Vertical Lines
            vLine = self.topMargin + distance
            pg.draw.line(background, BLACK, (self.leftMargin, vLine), (self.rightMargin, vLine), line_width)

    # display sudoku numbers onto grid
    def update(self, screen):
        # Shows which grid the user has selected
        if self.selected:
            pg.draw.rect(screen, (255, 0, 0), (self.xPos, self.yPos, self.blockLength, self.blockLength), 6)
        
        for x in range(9):
            for y in range(9):
                if self.grid and self.grid[x][y].num != 0:
                    xS = self.leftMargin + self.blockCentre + self.blockLength * self.grid[x][y].x + self.line_width
                    yS = self.topMargin + self.blockCentre + self.blockLength * self.grid[x][y].y + self.line_width
                    if self.grid[x][y].locked:
                        displayText(str(self.grid[x][y].num), 40, (xS, yS), screen, True, BLUE)
                    else:
                        displayText(str(self.grid[x][y].num), 40, (xS, yS), screen, True)

    # Select specific grid to add a number
    def selectGrid(self, pos, screen):
        if self.leftMargin < pos[0] < self.rightMargin - 5 and self.topMargin < pos[1] < self.bottomMargin - 5:
            self.x = (pos[0] - self.leftMargin) // self.blockLength
            self.y = (pos[1] - self.topMargin) // self.blockLength
            if not self.grid[self.x][self.y].locked:
                self.xPos = self.x * self.blockLength + self.leftMargin
                self.yPos = self.y * self.blockLength + self.topMargin
                self.selected = True
            else:
                self.selected = False

    def deselectGrid(self):
        self.selected = False

    # change number in Grid
    def addNumber(self, key):
        if self.selected:
            if key == pg.K_1:
                self.grid[self.x][self.y].setNum(1)
            elif key == pg.K_2:
                self.grid[self.x][self.y].setNum(2)
            elif key == pg.K_3:
                self.grid[self.x][self.y].setNum(3)
            elif key == pg.K_4:
                self.grid[self.x][self.y].setNum(4)
            elif key == pg.K_5:
                self.grid[self.x][self.y].setNum(5)
            elif key == pg.K_6:
                self.grid[self.x][self.y].setNum(6)
            elif key == pg.K_7:
                self.grid[self.x][self.y].setNum(7)
            elif key == pg.K_8:
                self.grid[self.x][self.y].setNum(8)
            elif key == pg.K_9:
                self.grid[self.x][self.y].setNum(9)
            else:
                self.grid[self.x][self.y].setNum(0)
        if key == pg.K_r:
            self.cleanGrid()
        elif key == pg.K_s:
            self.dokuSolver()

    def step(self, x, y):
        y += 1
        if (y == 9):
            x += 1
            y = 0
        return x,y
    
    # recursive method for backtracking
    def dokuHelper(self, validNums, x, y):
        if (x == 9):
            return True
        
        if (self.grid[x][y].num == 0):
            for i in range(9):
                if(isValid(self.grid, validNums[i], x, y)):
                    self.grid[x][y].setNum(validNums[i])
                    newX, newY = self.step(x, y)
                    if (self.dokuHelper(validNums, newX, newY)):
                        return True
            self.grid[x][y].num = 0
        else:
            newX, newY = self.step(x,y)
            if (self.dokuHelper(validNums, newX, newY)):
                return True

        return False
    
    # Solve the sudoku grid through backtracking
    def dokuSolver(self):
        validNums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.cleanGrid()
        if(self.dokuHelper(validNums, x=0, y=0)):
            print("done")
        else:
            print("Solution does not exist")

    def cleanGrid(self):
        for x in range(9):
            for y in range(9):
                if self.grid[x][y].locked != True:
                    self.grid[x][y].setNum(0)

# Create a duration timer
class Timer:
    
    # Create a timer starting at 0:00
    def __init__(self, screen):
        self.frame_count = 0
        self.total_seconds = 0
        self.minutes = 0
        self.seconds = 0
        self.timing = True
        displayText('{0:02}:{1:02}'.format(self.minutes, self.seconds), 40, (WIDTH - 150, HEIGHT - 50), screen)
    
    # Increment the timer every 60(FRAME_RATE) frames
    def update(self, screen):
        if self.timing:
            self.total_seconds = self.frame_count // FRAME_RATE
            self.minutes = self.total_seconds // 60
            self.seconds = self.total_seconds % 60
            self.frame_count += 1
        displayText('{0:02}:{1:02}'.format(self.minutes, self.seconds), 40, (WIDTH - 150, HEIGHT - 50), screen)

    def stop(self):
        self.timing = False
    
    def reset(self):
        self.frame_count = 0
        self.total_seconds = 0
        self.minutes = 0
        self.seconds = 0

    def start(self):
        self.timing = True

# Check validity of number in grid.
def isValid(grid, num, x, y):
    #check row
    for square in grid[x]:
        if square.num == num and square.y != y:
            return False

    #check column
    for square in grid:
        if square[y].num == num and square[y].x != x:
            return False

    #check boxes
    xBox = int(x/3) * 3
    yBox = int(y/3) * 3
    for row in range(3):
        for col in range(3):
            if grid[xBox+row][yBox+col].num == num  and grid[xBox+row][yBox+col].x != x and grid[xBox+row][yBox+col].y != y:
                return False
        
    return True

# Check if player has won!
def victory(grid):
    for x in range(9):
        for y in range(9):
            if not grid[x][y].num:
                return False
            if not isValid(grid, grid[x][y].num, x, y):
                return False
    return True

def infoText(screen):
    textSize = 30
    displayText("Press s to solve Grid", textSize, (10 ,HEIGHT - textSize), screen)
    displayText("Press r to reset Grid", textSize, (10 ,HEIGHT - textSize * 2), screen)
        


def main():

    # Initialize the game.
    pg.init()
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    pg.display.set_caption("Sudoku")

    # Set Background Colour
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill(GREY)
    
    # Display The Background
    screen.blit(background, (0,0))
    pg.display.flip()

    # Init Game objects
    clock = pg.time.Clock()
    timer = Timer(screen)
    grid = Grid()
    pg.display.update()
    
    # Draw a Grid To Background
    grid.drawGridLine(background)

    infoText(background)

    grid.newGame([[4, 0, 0, 8, 0, 6, 0, 0, 5], [0, 0, 5, 9, 7, 4, 6, 0, 0], [0, 1, 0, 0, 0, 0, 0, 8, 0], [5, 4, 0, 7, 0, 1, 0, 6, 8], [0, 9, 0, 0, 0, 0, 0, 1, 0], [6, 2, 0, 5, 0, 8, 0, 7, 4], [0, 6, 0, 0, 0, 0, 0, 4, 0], [0, 0, 8, 6, 4, 2, 1, 0, 0], [1, 0, 0, 3, 0, 9, 0, 0, 6]])

    # Game Loop
    running = True
    while running:
        clock.tick(FRAME_RATE)
        
        #Handle Input Events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if event.button == 1:
                    grid.selectGrid(pos, screen)
                elif event.button == 3:
                    grid.deselectGrid()
            elif event.type == pg.KEYDOWN:
                key = event.key
                grid.addNumber(event.key)
                if victory(grid.grid):
                    timer.stop()
                    print("VICTORY")

        

        # Draw New Frame
        screen.blit(background, (0,0))
        timer.update(screen)
        grid.update(screen)

        pg.display.update()
    
    pg.quit()

if __name__ == "__main__":
    main()