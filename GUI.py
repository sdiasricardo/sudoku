import pygame
from sudokusolver import solve, valid
from sudokugenerator import generate_puzzle, remove
import time
pygame.font.init()


RED, BLACK, WHITE, GRAY, BLUE = (255, 0, 0), (0, 0, 0), (255, 255, 255), (128, 128, 128), (140, 150, 157)
WIDTH, HEIGHT = 900, 900
FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT + 50))
pygame.display.set_caption("Sudoku")

def mat(mat):
    for i in mat:
        for j in i:
            print(j, end=' ')
        print()   


def check(mat1, mat2):
    for i in range(9):
        for j in range(9):
            if(mat1[i][j] != mat2[i][j]):
                return (i, j)

class Board():
    board = generate_puzzle() # Board that will store the initial puzzle
    selected = None # Last tile selected

    def __init__(self, width, height):
        self.width = width # Width of Board
        self.height = height # Height of Board
        self.tiles = [[Tile(self.board[i][j], i, j) for j in range(9)] for i in range(9)] # Creating each tile
        self.empty = 63


    def draw_grid(self, window):
        WINDOW.fill((255, 255, 255))
        gap = self.width/9
        pygame.draw.rect(window, BLACK, (0, 0, self.width, self.height), 4)
        
        # Drawing table
        for i in range(1, 9):
            if i % 3 == 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(window, BLACK, (0, i*gap), (self.width, i*gap),thick) 
            pygame.draw.line(window, BLACK, (i*gap, 0), (i*gap, self.height), thick)
        
        # Draing each tile
        for i in range(9):
            for j in range(9):
                self.tiles[i][j].draw(window, self.width)
        
        pygame.display.update()


    # Getting row and column from mouse click
    def click(self, pos):
        if(pos[1] < self.height and pos[0] < self.width):
            gap = self.width/9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        return None

    
    def select(self, x, y):
        if(self.selected != None):
            self.tiles[self.selected[0]][self.selected[1]].selected = False
        
        
        self.tiles[x][y].selected = True
        self.selected = (x, y)


    def trySolution(self, val, x, y):
        if self.board[x][y] != 0:
            return True
        if(valid(self.board, val, (x, y))):
            copy = []

            for i in range(9):
                aux = []
                for j in range(9):
                    aux.append(self.board[i][j])
                copy.append(aux)
            
            copy[x][y] = val
            if(solve(copy)):
                self.board[x][y] = val
                self.tiles[x][y].value = val
                self.tiles[x][y].temp.clear()
                return True
            return False
        
        return False







class Tile():
    def __init__(self, value, row, column):
        self.row = row # Tile Row
        self.col = column # Tile column
        self.value = value # Tile value (0 = empty)
        self.temp = [] # Possibilities for the tile
        self.selected = False
    

    def draw(self, window, width):
        # Defining each tile gap and coordinate (coordinates are set to be on top left coorner)
        gap = width/9
        x = self.col * gap
        y = self.row * gap

        if self.selected:
            pygame.draw.rect(window, RED, (x, y, gap, gap), 3)

        # Drawing the final value, if it exists
        if self.value == 0:
            fnt = pygame.font.SysFont("comicsans", 40)
            for i in self.temp:
                lin = (i-1)%3
                col = (i-1)// 3
                text = fnt.render(str(i), 1, GRAY)
                WINDOW.blit(text, (x + ((2*lin + 1)*gap/6 - text.get_width()/2), y + ((2*col + 1)*gap/6 - text.get_height()/2)))
        
        # Drawing possibilities sketch
        else:
            fnt = pygame.font.SysFont("comicsans", 90)
            text = fnt.render(str(self.value), 1, BLACK)
            WINDOW.blit(text, (x + (gap/2 - text.get_width()/2), y + (gap/2 - text.get_height()/2)))
    

    def setValue(self, value):
        self.value = value


    # Adding or removing possibilities (sketch)
    def addTemp(self, value):
        if len(self.temp) > 0:
            for i in range(len(self.temp)):
                if self.temp[i] > value:
                    self.temp.insert(i, value)
                    break
                elif self.temp[i] == value:
                    self.temp.remove(value)
                    break
                elif i == len(self.temp) - 1:
                    self.temp.append(value)
                    break
        else:
            self.temp.append(value)






def main():
    run = True
    clock = pygame.time.Clock()
    WINDOW.fill(WHITE)
    pygame.display.update()
    gap = WIDTH/9

    bo = Board(900, 900)
    bo.draw_grid(WINDOW)

    pygame.display.update()
    strikes = 0
    end = False
    while run:
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            num = None

            if event.type == pygame.QUIT:
                run = False

            if not end:
                # Key pressed
                if event.type == pygame.KEYDOWN:
                    if keys[pygame.K_1]:
                        num = 1
                    elif keys[pygame.K_2]:
                        num = 2
                    elif keys[pygame.K_3]:
                        num = 3
                    elif keys[pygame.K_4]:
                        num = 4
                    elif keys[pygame.K_5]:
                        num = 5
                    elif keys[pygame.K_6]:
                        num = 6
                    elif keys[pygame.K_7]:
                        num = 7
                    elif keys[pygame.K_8]:
                        num = 8
                    elif keys[pygame.K_9]:
                        num = 9

                    # Shift + number
                    if keys[pygame.K_LSHIFT] and num != None and bo.selected:
                        bo.tiles[bo.selected[0]][bo.selected[1]].addTemp(num)
                        num = None
                    
                    # Only number
                    elif num != None and bo.selected:
                        if bo.trySolution(num, bo.selected[0], bo.selected[1]):
                            if(bo.tiles[bo.selected[0]][bo.selected[1]].value != 0):
                                if bo.empty == 1:
                                    # Ganhou
                                    fnt = pygame.font.SysFont("comicsans", 120)
                                    text = fnt.render("You won!", 1, BLACK)
                                    WINDOW.fill(WHITE)
                                    WINDOW.blit(text, ((bo.width/2 - text.get_width()/2), (bo.height/2 - text.get_height()/2)))
                                    pygame.display.update()
                                    end = True
                                else:
                                    bo.empty -= 1
                        
                        else:
                            if strikes <= 2:
                                strikes += 1
                            else:
                                fnt = pygame.font.SysFont("comicsans", 120)
                                text = fnt.render("You lost!", 1, BLACK)
                                WINDOW.fill(WHITE)
                                WINDOW.blit(text, ((bo.width/2 - text.get_width()/2), (bo.height/2 - text.get_height()/2)))
                                pygame.display.update()
                                end = True
                        

                if not end:
                    # Mouse click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        clicked = bo.click(pos)

                        if clicked:
                            bo.select(clicked[0], clicked[1])
                            num = None
                    


                    
                    fnt = pygame.font.SysFont("comicsans", 50)
                    
                    # Draw Grid
                    bo.draw_grid(WINDOW)
                    
                    # Draw Strikes
                    text1 = text = fnt.render("Errors: ", 1, BLACK)
                    WINDOW.blit(text, (20, HEIGHT + 25 - text1.get_height()/2))
                    text = fnt.render("X "*strikes, 1, RED)
                    WINDOW.blit(text, (20 + text1.get_width(), HEIGHT + 25 - text.get_height()/2))
            
                    pygame.display.update()


                
                 

    pygame.quit()



if __name__ == "__main__":
    main()