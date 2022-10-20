from termios import CLOCAL
import pygame
from sudokusolver import solve, valid
from sudokugenerator import generate_puzzle, remove

RED, BLACK, WHITE, GRAY, BLUE = (255, 0, 0), (0, 0, 0), (255, 255, 255), (128, 128, 128), (140, 150, 157)
WIDTH, HEIGHT = 900, 900
FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT + 50))
pygame.display.set_caption("Sudoku")



class Board():
    board = generate_puzzle() # Board that will store the initial puzzle
    selected = None # Last tile selected

    def __init__(self, width, height):
        self.width = width # Width of Board
        self.height = height # Height of Board
        self.tiles = [[Tile(self.board[i][j], i, j, width, height) for j in range(9)] for i in range(9)] # Creating each tile


    def draw_grid(self, window):
        gap = self.width/9
        pygame.draw.rect(window, BLACK, (0, 0, self.width, self.height), 4)
        
        # Drawing table
        for i in range(1, 9):
            if i % 3 == 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(window, BLACK, (0, i*gap), (self.width, i*gap),thick) 
            pygame.draw.line(window, BLACK, (i*gap, 0), (i*gap, self.lenght), thick)





class Tile():
    def __init__(self, value, row, column, width, height):
        self.row = row # Tile Row
        self.col = column # Tile column
        self.value = value # Tile value (0 = empty)
        self.temp = [] # Possibilities for the tile
        self.selected = False
        self.width = width # Width of Board
        self.height = height # Height of Board

    def draw(self, window):
        font = pygame.font.SysFont("monospace", 40)

        gap = self.width/9
        x = self.col * gap
        y = self.row * gap

        if self.selected:
            pygame.draw.rect(window, RED, (x, y, gap, gap), 3)

        if self.value ==


        





def main():
    run = True
    clock = pygame.time.Clock()
    WINDOW.fill((255, 255, 255))
    pygame.display.update()
    pygame.draw.rect(WINDOW, BLACK, (0, 0, WIDTH, HEIGHT), 4)
    gap = WIDTH/9
    for i in range(1, 9):
            if i % 3 == 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(WINDOW, BLACK, (0, i*gap), (WIDTH, i*gap),thick) 
            pygame.draw.line(WINDOW, BLACK, (i*gap, 0), (i*gap, HEIGHT), thick)



    pygame.display.update()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        

    pygame.quit()



if __name__ == "__main__":
    main()