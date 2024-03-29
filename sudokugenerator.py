from random import shuffle, randint
from sudokusolver import valid, solve, find_empty

def generate_solution(bo):
    possibilities = [i for i in range(1, 10)]
    for k in range(81):
        row=k//9
        col=k%9
        if bo[row][col] == 0:
            shuffle(possibilities)
            for i in possibilities:
                if(valid(bo, i, (row, col))):
                    bo[row][col] = i
                    if not find_empty(bo):
                        return True
                    else:
                        if(generate_solution(bo)):
                            return True
                
            break

    bo[row][col] = 0 
    return False



def remove(bo):
    count = 81

    while count >18:
        i = randint(0, 8)
        j = randint(0, 8)
        if(bo[i][j] != 0):
            bo[i][j] = 0
            count -= 1


def generate_puzzle():
    bo = [[0 for i in range(9)] for i in range(9)]
    generate_solution(bo)
    remove(bo)
    return bo 


