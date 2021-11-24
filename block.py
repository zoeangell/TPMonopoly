#This is the file with the block class
from card import *
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
        #This sets the rent of a block. 
        if self.price != None and self.hotel != 0:
            return self.price + 4*self.price
        elif self.house > 0:
            return self.price + self.price*self.house
        else:
            return self.price*0.1
    
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
        #self.fillChanceDeck()
        self.cChest = []
        #self.fillcChestDeck()

    '''def fillcChestDeck(self):
        card1 = Card("Bank error in your favor. Collect $200", 200)
        card2 = Card("Doctor's fee. Pay $50", -50)
        card3 = Card("From sale from stock you get $50", 50)
        card4 = Card("Holiday fund matures. Receive $100.", 100)
        card5 = Card("Income tax refund. Collect $20.", 20)
        card6 = Card("It's your birthday. Collect $100 from each player", 10)
        card7 = Card("Life insurance matures. Collect $100", 100)
        card8 = Card("Pay hospital fees of $100.", -100)
        card9 = Card("Pay school fees of $50", -50)
        card10 = Card("You have won a beauty contest. Collect $10", 10)
        self.cChest.extend(card1, card2, card3, card4, card5, card6, card7,
            card8, card9, card10)'''

    '''def fillChanceDeck(self):
        card1 = Card("Advance to Boardwalk", None)
        card2 = Card("Advance to Go and collect $200", 200)
        card3 = Card("Advance to IL Ave.", None)
        card4 = Card("Bank pays you dividend of $50", 50)
        card5 = Card("Go back 3 spaces", None)
        card6 = Card("Make general repairs on all your property, $25 for each house and $100 for each hotel",
                None)
        card7 = Card("Advance to Reading Railroad", None)
        card8 = Card("Speeding fine $15", 15)
        card9 = Card("You have been elected Chairman of the Board. Pay $50 to each player", -50)
        card10 = Card("Your building loan matures. Collect $150", 150)'''


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

    def rent(self): 
        #The rent of a normal block adjusted for the presence of houses/hotels
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







    
    