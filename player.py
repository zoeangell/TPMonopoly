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
        self.jail = False
        self.color = color
        
    def curBlock(self):
        #return curBlock as an int
        x, y = self.position
        #print("x: ", x, "y: ", y)
        curblock = 0
        #totalBlocks = len(self.board) * len(self.board[0])
        #moves the player one space
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                bx0, by0, bx1, by1 = self.board[row][col].location
                #should work
                if x >= bx0 and y >= by0 and x <= bx1 and y <= by1:
                    curblock = 10*row + col 
                    #print("hey")
        #print("curblock: ", curblock)
        return curblock
        #newblock = (curblock + distance)%totalBlocks
        #return newblock
        #return (curblock, newblock)
    
    def getCurBlock(self, blockNum):
        #gets the current block object based on the blockNumber in the board
        row = blockNum // len(self.board[0])
        col = blockNum % len(self.board[0])
        return self.board[row][col]

    def findBlock(self, word):
        #finds the block based on part of the name
        matches = 0
        block = None
        blockNum = None
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                if word in self.board[row][col].name:
                    block = self.board[row][col]
                    blockNum = row*len(self.board[0]) + col
                    matches += 1
        if matches == 1:
            return block, blockNum
        return None, None



    def roll(self):
        toss1 = random.randint(1,6)
        toss2 = random.randint(1,6)
        return ((toss1, toss2)) #uncomment this to return to normal
        #return((1, 1)) #comment this to return to normal

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
    
    def payRent(self, block, other):
        #Pays the rent for a owned block
        self.bankaccount += block.rent()
        other.bankaccount += abs(block.rent())

    def isOwned(self, other, block):
        #Checks if the someone owns the block. If None then no rent and
        #it can be bought.
        if block.ownership == self.name: return True
        elif block.ownership == other.name: return False
        return None

    def payTax(self, block):
        #Pays basic rent of a block
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
        other.bankaccount += tax
        return tax

    def payRailroadTax(self, block, other):
        #Tax for a railroad depends on the number of railroads that the other
        #player owns. This calculates that.
        count, tax = self.countRailroads(other), 0
        if count == 1: tax = 25
        elif count == 2: tax = 50
        elif count == 3: tax = 100
        elif count == 4: tax = 200
        self.bankaccount -= tax
        other.bankaccount += tax
        return tax


    def countUtilities(self, other):
        #Counts the number of utilities that the other player owns
        count = 0
        for block in other.land:
            if isinstance(block, Utility): count +=1
            print(count)
        #print("Utility Num is: ", count)
        return count

    def countRailroads(self, other):
        #Counts the number of railroads that the other player owns
        count = 0
        for block in other.land:
            if isinstance(block, Railroad): count +=1
        return count

    def getBlock(self, blockName):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                curName = self.board[row][col].name
                if curName in blockName:
                    return self.board[row][col]
        return None

    def buyOpponentsProp(self, block, other):
        #Let's a player buy the other player's property at twice the price.
        #When this happens, originally price of property is returned to original
        #owner
        self.land.append(block)
        price = 2*block.price
        self.bankaccount += price
        other.bankaccount -= block.price
        other.land.remove(block)
        block.ownership = self.name

    def buyHouse(self, block):
        #allows the player to buy a house
        blockNum = self.blockNum(block)
        row = blockNum // len(self.board[0])
        price = (row+1) * 50
        self.bankaccount -= price
        block.house += 1

    def buyHotel(self, block):
        #Allows the player to buy a hotel
        blockNum = self.blockNum(block)
        row = blockNum // len(self.board[0])
        price = (row+1) * 50
        self.bankaccount -= price
        block.house = 0
        block.hotel += 1

    def blockNum(self, block):
        #This returns the number of the block
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                curblock = self.board[row][col]
                if curblock.name == block.name:
                    blockNum = row*len(self.board[0]) + col
        return blockNum

    def opponentPropAvailable(self, other):
        #Find the opponent's land that don't have houses/hotels on them
        availableLand = []
        for block in other.land:
            if block.house > 0 or block.hotel > 0:
                continue
            else:
                availableLand.append(block)
        return availableLand
    
    def collect200(self):
        #Player gets $200 after passing GO
        self.bankaccount += 200

    def payJailFine(self):
        #The jail fine to get out of jail
        self.bankaccount -= 50

    def totalHouses(self):
        #Total houses that a player owns
        totalHouses = 0
        for prop in self.land:
            totalHouses += prop.house
        print("totalHouses: ", totalHouses)
        return totalHouses

    def totalHotels(self):
        #Total hotels that a player owns
        totalHotels = 0
        for prop in self.land:
            totalHotels += prop.hotel
        print("totalHotels: ", totalHotels)
        return totalHotels






    


    


