#This is the file with the block class. A block are the squares on the outside
#of the board that the players move on
from card import *
class Block(object):
    #General block class for the board
    def __init__(self, location, color, name, price):
        #Block constructor is being called
        self.location = location
        self.color = color
        self.name = name
        self.price = price
        self.house = 0
        self.hotel = 0
        self.ownership = None
    
    def rent(self):
        #This sets the rent of a block. 
        if self.price != None and self.hotel != 0:
            return self.price + 4*self.price
        elif self.house > 0:
            return self.price + self.price*self.house
        else:
            return self.price*0.1
    
    def __repr__(self):
        return self.name

class SpecialCards(Block):
    #Block subclass to handle community chest and chance
    def __init__(self, location, color, name, price):
        super().__init__(location, color, name, price)
        self.property = None
        self.ownership = None
       

    def __repr__(self):
        return self.name


class Railroad(Block):
    #The special class for railroad blocks
    def __init__(self, location, color, name, price):
        super().__init__(location, color, name, price)
        self.property = None

class Tax(Block):
    #Special block to handle luxury and income tax
    def __init__(self, location, color, name, price):
        super().__init__(location, color, name, price)
        self.property = None
        self.ownership = None

    def rent(self): 
        #The rent of a normal block adjusted for the presence of houses/hotels
        return self.price

class Utility(Block):
    #Special class for the utility blocks
    def __init__(self, location, color, name, price):
        super().__init__(location, color, name, price)
        self.property = None

class Corner(Block):
    #Special block for the "corners" ie GO, Free Parking...
    def __init__(self, location, color, name, price, gTJ):
        super().__init__(location, color, name, price)
        self.property = None
        self.ownership = None
        self.gTJ = gTJ
    
    def rent(self):
        #Overwrites the rent function in the block class
        return None








    
    