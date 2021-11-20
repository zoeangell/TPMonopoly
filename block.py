#This is the file with the block class
class Block(object):
    #General block class for the board
    def __init__(self, location, color, name, price):
        self.location = location
        self.color = color
        self.name = name
        self.price = price
        self.property = []
        self.ownership = None
    
    #create a function to add a property

    #create a function to change ownership

class SpecialCards(Block):
    #Block subclass to handle community chest and chance
    def __init__(self, location, color, name, price):
        super().__init__(location, color, name, price)
        self.property = None
        self.ownership = None
        self.chanceDeck = []
        #self.usedChance = [] just return cards to the bottom of the pile
        self.cChest = []
        #self.usedcChest = []

class Railroad(Block):
    def __init__(self, location, color, name, price):
        super().__init__(location, color, name, price)
        self.property = None
        #write a rent function

class Tax(Block):
    def __init__(self, location, color, name, price):
        super().__init__(location, color, name, price)
        self.property = None
        self.ownership = None

    def getRent(self): #might need to change this for the 10% rule for income tax
        return self.price
class Utility(Block):
    def __init__(self, location, color, name, price):
        super().__init__(location, color, name, price)
        self.property = None

class Corner(Block):
    def __init__(self, location, color, name, price, gTJ):
        super().__init__(location, color, name, price)
        self.property = None
        self.ownership = None
        self.gTJ = gTJ

    #Write a rent function






    
    