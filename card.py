#This file just contains the card class which is for the community chest
#and chance feature
class Card(object):
    def __init__(self, message, action):
        self.message = message
        self.action = action

    def __repr__(self):
        return self.message

