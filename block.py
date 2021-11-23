#This is the file with the block class
class Block(object):
    #General block class for the board
    def __init__(self, location, color, name, price):
        self.location = location
        self.color = color
        self.name = name
        self.price = price
        self.house = 0
        self.hotel = 0
        self.ownership = None
    
    def rent(self):
        #This sets the rent of a block. The rent without any properties is 10% of price
        if self.price != None:
            return 0.1 * (self.price)
    
    #create a function to add a property
    def __repr__(self):
        return self.name

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

    def rent(self): #might need to change this for the 10% rule for income tax
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
    
    def rent(self):
        return None

    #Write a rent function







    
    