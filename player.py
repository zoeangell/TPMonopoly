#This is the player class
from block import *
import random
class Player(object):
    def __init__(self, name, board, position, color):
        self.name = name
        self.board = board
        self.bankaccount = 1500
        self.position = position
        self.land = []
        self.color = color
        
    def curBlock(self):
        #return curBlock as an int
        x, y = self.position
        print("x: ", x, "y: ", y)
        curblock = 0
        #totalBlocks = len(self.board) * len(self.board[0])
        #moves the player one space
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                bx0, by0, bx1, by1 = self.board[row][col].location
                #should work
                if x >= bx0 and y >= by0 and x <= bx1 and y <= by1:
                    curblock = 10*row + col 
                    print("hey")
        print("curblock: ", curblock)
        return curblock
        #newblock = (curblock + distance)%totalBlocks
        #return newblock
        #return (curblock, newblock)
    
    def getCurBlock(self, blockNum):
        row = blockNum // len(self.board[0])
        col = blockNum % len(self.board[0])
        return self.board[row][col]


    def roll(self):
        toss1 = random.randint(1,6)
        toss2 = random.randint(1,6)
        return ((toss1, toss2))

    def __repr__(self):
        return self.name

    def buyBlock(self, block):
        #Allows player to buy land
        self.bankaccount += block.price #plus because I made the prices -
        block.ownership = self.name
        self.land.append(block)

    def canBuy(self, block):
        if (isinstance(block, SpecialCards) or isinstance(block, Tax) or
            isinstance(block, Corner)): return False
        return True
    
    def payRent(self, block):
        #Pays the rent for a owned block
        self.bankaccount += block.rent()

    def isOwned(self, other, block):
        #Checks if the someone owns the block. If None then no rent and
        #it can be bought.
        if block.ownership == self.name: return True
        elif block.ownership == other.name: return False
        return None

    def payTax(self, block):
        self.bankaccount += block.rent()

    def payIncomeTax(self):
        #Pay 10% of your income
        self.bankaccount *= 0.9

    def payUtilityTax(self, block, roll, other):
        #Utilities have special rules for tax. This function handles that.
        count, tax = self.countUtilities(other), 0
        if count == 1:
            tax = 4*roll
        elif count == 2:
            tax = 10*roll
        self.bankaccount -= tax
        return tax

    def payRailroadTax(self, block, other):
        count, tax = self.countRailroads(other), 0
        if count == 1: tax = 25
        elif count == 2: tax = 50
        elif count == 3: tax = 100
        elif count == 4: tax = 200
        self.bankaccount -= tax
        return tax


    def countUtilities(self, other):
        count = 0
        for block in other.land:
            if isinstance(block, Utility): count +=1
        return count

    def countRailroads(self, other):
        count = 0
        for block in other.land:
            if isinstance(block, Railroad): count +=1
        return count


    


    


