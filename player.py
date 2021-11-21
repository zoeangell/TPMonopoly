#This is the player class
from block import *
class Player(object):
    def __init__(self, name, board, position, color):
        self.name = name
        self.board = board
        self.bankaccount = 1500
        self.position = position
        self.color = color
        
    def move(self, distance):
        x, y = self.position
        curblock = None
        totalBlocks = len(self.board) * len(self.board[0])
        #moves the player one space
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                bx0, by0, bx1, by1 = self.board[row][col].location
                #should work
                if x >= bx0 and y >= by0 and x <= bx1 and y <= by1:
                    curblock = 10*row + col 
                    print("hey")
        newblock = (curblock + distance)%totalBlocks
        return newblock
        #return (curblock, newblock)

    


