import tkinter as tk
from sudoku import Game
from threading import Thread
import time

# Class for the GUI of the Sudoku Solver.
class SudokuGUI:
    def __init__(self, game):
        # initialize the game and the root window.
        self.game = game
        self.root = tk.Tk()
        self.root.title("Sudoku Solver")
        self.selectedButton = None
        self.selectionCoord = (0,0)
        self.root.bind('<Key>', self.keyEvent)
        
        # draw the grid.
        self.drawGrid()

        # draw the buttons.
        self.create_complete_button()
        self.create_solve_button()

    # Function to handle the click event on the cell.
    def onClick(self, event, coord):
        if self.selectedButton:
            self.selectedButton.config(highlightbackground='grey')
        self.selectedButton = event.widget
        self.selectionCoord = coord
        print(self.selectionCoord)
        self.selectedButton.config(highlightbackground='blue')

    # Function to create the solve button.
    def create_solve_button(self):
        solve_button = tk.Button(self.root, text="Solve", command=self.startSolveThread, height=3, width=15)
        solve_button.pack(side=tk.LEFT, pady=10)

    # Function to create the new button.
    def create_complete_button(self):
        complete_button = tk.Button(self.root, text="New", command=self.newPuzzle, height=3, width=15)
        complete_button.pack(side=tk.LEFT, padx=20, pady=10)


    # Function to handle the key event (1-9).
    def keyEvent(self, event):
        if self.selectedButton:
            num = event.char
            if num.isdigit() and 1 <= int(num) <= 9:
                x, y = self.selectionCoord
                self.updateCell(x, y, num)

    # Function to draw the grid.
    def drawGrid(self):
        # Create the base puzzle frame.
        puzzle = tk.Frame(self.root, bg='white')
        puzzle.pack()

        # Add the 3 * 3 big blocks
        blocks = [] 
        for i in range(3):
            row = []
            for j in range(3):
                frame = tk.Frame(puzzle, bd=1, highlightbackground='grey',
                                highlightcolor='grey', highlightthickness=2)
                frame.grid(row=i, column=j, sticky='nsew')
                row.append(frame)
            blocks.append(row)

        # Add the 9 * 9 individual cells
        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                # check value of the cell and if it is a base cell
                cellValue = self.game.grid[i][j]
                isBase = cellValue != 0

                # figure location of the cell in the 3 * 3 block
                cell = tk.Frame(blocks[i // 3][j // 3])
                cell.grid(row=(i % 3), column=(j % 3), sticky='nsew')
                cell.rowconfigure(0, minsize=65, weight=1)
                cell.columnconfigure(0, minsize=65, weight=1)
                
                # only add text to the cell if it is a base cell
                var = tk.StringVar()
                var.set(str(cellValue) if isBase else '')

                # create the button for the cell
                cellButton = tk.Button(cell, relief="ridge", 
                                    bg='white',
                                    textvariable=var,
                                    highlightbackground='grey',
                                    state=tk.DISABLED if isBase else tk.NORMAL,
                                    disabledforeground='blue',
                                    font = ('Arial', 25, 'bold'))
                cellButton.grid(sticky='nsew')
                
                # bind the click event to the cell if not base
                if not isBase:
                    cellButton.bind('<Button-1>', lambda event,
                                                coord = (i, j):
                                                self.onClick(event, coord))

                row.append(cellButton)
            self.cells.append(row)

    # Function to update the cell with the number.
    def updateCell(self, x, y, num):
        self.game.inputCell(x, y, int(num))

        if self.game.isValid(x, y, int(num)):
            textColour = 'green'
        else:
            textColour = 'red'
        cell = self.cells[x][y]
        var = tk.StringVar()
        if int(num) != 0:
            var.set(str(num))
        cell.config(textvariable=var)
        cell.config(foreground = textColour)

    # Function to check all the cells.
    def checkAll(self):
        for x in range(9):
            for y in range(9):
                if self.game.base[x][y] == 0 and self.game.grid[x][y] != 0:
                    self.updateCell(x, y, self.game.grid[x][y])

    # Function to create a new puzzle.
    def newPuzzle(self):
        self.game.generateGrid()
        for x in range(9):
            for y in range(9):
                self.cells[x][y].config(state=tk.NORMAL)
                num = self.game.grid[x][y]
                var = tk.StringVar()
                var.set(str(num) if num != 0 else '')
                self.cells[x][y].bind('<Button-1>', lambda event, cooord = (x, y): self.onClick(event, cooord))
                self.cells[x][y].config(textvariable=var)
                if self.game.grid[x][y] != 0:
                    self.cells[x][y].config(state=tk.DISABLED)
                    self.cells[x][y].unbind('<Button-1>')


    # Function to start a new thread and solve the puzzle visually.
    def startSolveThread(self):
        t = Thread(target= lambda: self.visualSolve(0,0), daemon=True)
        t.start()

    # Function to solve the puzzle visually.
    def visualSolve(self, row, col):
        self.game.grid = self.game.base
        self.checkAll()
        if row == 9:
            return True
        if col == 9:
            return self.visualSolve(row + 1, 0)
        
        if self.game.grid[row][col] == 0:
            for i in range(1, 10):
                self.updateCell(row, col, i)
                time.sleep(0.1)
                if self.game.isValid(row, col, i):
                    if self.visualSolve(row, col + 1):
                        return True
                    else:
                        self.updateCell(row, col, 0)
                        time.sleep(0.1)
            else:
                self.updateCell(row, col, 0)
                time.sleep(0.1)
            return False
        else:
            return self.visualSolve(row, col + 1)

# Main function to run the program.
def main():
    game = Game()
    gui = SudokuGUI(game)
    gui.root.mainloop()

if __name__ == "__main__":
    main()