from cmu_112_graphics import *
import random
from block import *
from gameplay import *
from player import *

def appStarted(app):
    app.boardWidth = 500
    app.marginSide = 50
    app.marginTop = 150
    app.innerMargin = 75
    app.innerBoardLength = app.boardWidth - 2*app.innerMargin
    app.boardCoordinates = []
    app.board = []
    app.nBlocks = 9
    app.inJail = None
    app.justVisiting = None
    app.players = []
    createBoardCoordinates(app)
    createBoard(app)
    jailCoordinates(app)
    playMonopoly(app)


def redrawAll(app, canvas):
    drawBoard(app, canvas)

def drawBoard(app, canvas):
    #Draws the skeleton of the board
    canvas.create_rectangle(app.marginSide, app.marginTop, 
        app.marginSide+app.boardWidth, 
        app.marginTop+app.boardWidth, outline = "black") #outer board
    canvas.create_rectangle(app.marginSide + app.innerMargin, app.marginTop + 
        app.innerMargin,
        app.marginSide+app.boardWidth - app.innerMargin, 
        app.marginTop+app.boardWidth -
            app.innerMargin, outline = "black") #inner board
    canvas.create_rectangle(app.marginSide + app.boardWidth,
        app.marginTop+app.boardWidth, app.marginSide + app.boardWidth - app.innerMargin,
            app.marginTop+app.boardWidth - app.innerMargin, outline = "black") 
            #coordinates of the Go block
    canvas.create_rectangle(app.marginSide, app.marginTop, app.marginSide+app.innerMargin, 
        app.marginTop+app.innerMargin, outline = "black") #coordinates for free parking
    canvas.create_rectangle(app.marginSide, app.marginTop+app.boardWidth - app.innerMargin,
        app.marginSide + app.innerMargin, app.marginTop + app.boardWidth, outline = "black")
        #coordinates of jail just visiting/in jail coordinates
        #
    canvas.create_rectangle(app.marginSide + app.boardWidth - app.innerMargin,
        app.marginTop, app.marginSide+ app.boardWidth, 
             app.marginTop + app.innerMargin,  outline = "black") #Go to jail coordinates
    drawBlocks(app, canvas)
    drawInnerBoard(app, canvas)
    drawSpecialBlocks(app,canvas)
    drawSideBlockDesign(app, canvas)
    drawTopBlockDesign(app, canvas)
    drawPlayerBoard(app, canvas, app.players[0])
    drawPlayerBoard(app, canvas, app.players[1])
    drawPlayerInfo(app,canvas,app.players[0],(app.marginSide, app.marginSide))
    drawPlayerInfo(app,canvas,app.players[1],(app.marginSide,2*app.marginSide))
 
def createBoardCoordinates(app):
    #Creating a 2D list of the blocks coordinates
    row1 = bottomRowCoordinates(app)
    app.boardCoordinates.append(row1)
    col1 = leftColCoordinates(app)
    app.boardCoordinates.append(col1)
    row2 = topRowCoordinates(app)
    app.boardCoordinates.append(row2)
    col2 = rightColCoordinates(app)
    app.boardCoordinates.append(col2)
    print(app.boardCoordinates)

def drawInnerBoard(app, canvas):
    #Draws the inside of the board meaning the monopoly and special cards
    x0 = app.marginSide + 3*app.innerMargin/2
    #print("x0: ", x0)
    x1 = app.marginSide + app.innerBoardLength + app.innerMargin/2
    #print("x1: ", x1)
    y0 = (app.marginTop + 2*app.innerMargin + app.innerBoardLength/8 + 
        3*app.marginSide/4)
    y1 = y0 + (app.innerBoardLength/6)
    canvas.create_rectangle(x0, y0, x1, y1, fill = "red", outline = "black",
        width = 3)
    boxHeight = y1 - y0
    boxWidth = x1 - x0
    canvas.create_text((x0 + 1/2*boxWidth),#Drawing monopoply in center of board
        y0 + boxHeight/2, text="MONOPOLY", font =
        "Arial 28 bold", fill = "white")
    #Drawing community chest
    #x0 = 4*app.marginSide/3 + app.innerMargin
    x1 = x0 + 2*app.marginSide
    y0 = app.marginTop + 4*app.innerMargin/3
    y1 = y0 + app.innerMargin
    boxHeight = y1 - y0
    boxWidth = x1 - x0
    canvas.create_rectangle(x0, y0, x1, y1, fill = "cyan")
    canvas.create_text((x0 + 1/2*boxWidth),
        y0 + boxHeight/2, text="Community Chest", font =
        "Arial 10 bold", fill = "black")
    
    #Drawing Chance
    x1 = app.marginSide + app.innerBoardLength + app.innerMargin/2
    x0 = x1 - 2*app.marginSide
    y0 = app.marginTop + app.innerBoardLength - app.innerMargin/4
    y1 = y0 + app.innerMargin 
    canvas.create_rectangle(x0, y0, x1, y1, fill = "orange")
    canvas.create_text((x0 + 1/2*boxWidth),
        y0 + boxHeight/2, text="Chance", font =
        "Arial 10 bold", fill = "black")

def textLocation(x0, y0, x1, y1):
    boxWidth = x1-x0
    boxHeight = y1-y0
    return (boxWidth, boxHeight)

def drawSpecialBlocks(app, canvas):
    #The Go Block
    margin = 20
    x0 = app.marginSide + app.boardWidth
    y0 = app.marginTop+app.boardWidth
    x1 = app.marginSide + app.boardWidth - app.innerMargin
    y1 = app.marginTop+app.boardWidth - app.innerMargin
    boxWidth, boxHeight = textLocation(x0, y0, x1, y1)
    canvas.create_text((x0 + 1/2*boxWidth),
        y0 + boxHeight/2, text="GO", font =
        "Arial 30 bold", fill = "red")
    canvas.create_text((x0 + 1/2*boxWidth),
        y0 + boxHeight/2 - margin, text="Collect $200 as you pass", font =
        "Arial 5 bold", fill = "black")

    #The Jail Block
    x0 = app.marginSide
    y0 = app.marginTop + app.boardWidth - app.innerMargin
    x1 = app.marginSide + app.innerMargin
    y1 = app.marginTop + app.boardWidth
    boxWidth, boxHeight = textLocation(x0, y0, x1, y1)
    canvas.create_rectangle(x0, y0, x1, y1 - boxHeight/2, fill = "orange", 
        outline = "black")
    y1 = y1 - boxHeight/2
    canvas.create_text((x0 + 1/2*boxWidth),
        y0 + boxHeight/2 - margin, text="In Jail", font =
        "Arial 10 bold", fill = "black")
    y0 = y1
    y1 = app.marginTop + app.boardWidth
    canvas.create_text((x0 + 1/2*boxWidth),
        y0 + boxHeight/2 - margin, text="Just Visiting", font =
        "Arial 10 bold", fill = "black")
    #The Free Parking 
    x0 = app.marginSide
    y0 = app.marginTop
    x1 = app.marginSide + app.innerMargin
    y1 = app.marginTop+app.innerMargin
    boxWidth, boxHeight = textLocation(x0, y0, x1, y1)
    canvas.create_text((x0 + 1/2*boxWidth),
        y0 + boxHeight/2 - margin, text="Free", font =
        "Arial 15 bold", fill = "red")
    canvas.create_text((x0 + 1/2*boxWidth),
        y0 + boxHeight/2 + margin/2, text="Parking!", font =
        "Arial 15 bold", fill = "red")

    #Go to Jail
    x0 = app.marginSide + app.boardWidth - app.innerMargin
    y0 = app.marginTop
    x1 = app.marginSide+ app.boardWidth
    y1 = app.marginTop + app.innerMargin
    boxWidth, boxHeight = textLocation(x0, y0, x1, y1)
    canvas.create_text((x0 + 1/2*boxWidth),
        y0 + boxHeight/2 - margin, text="Go", font =
        "Arial 15 bold", fill = "blue")
    canvas.create_text((x0 + 1/2*boxWidth),
        y0 + boxHeight/2 + margin/2, text="To Jail!", font =
        "Arial 15 bold", fill = "blue")
    

##Need to write a function to send the in jail/visiting coordinates



def bottomRowCoordinates(app):
    #Gets the coordinates for the row of blocks at the bottom of the board
    row1 = []
    blockWidth = app.innerBoardLength/app.nBlocks
    startWidth = app.marginSide + app.boardWidth - app.innerMargin
    y1 = app.marginTop+app.boardWidth
    y0 = y1 - app.innerMargin
    for i in range(app.nBlocks):
        x0 = startWidth - (i+1)*blockWidth
        x1 = startWidth - (i)*blockWidth
        row1.append((x0, y0, x1, y1,))
    #print("length of row1", len(row1))
    return row1

def drawBlocks(app, canvas):
    #Drawing the blocks on the outside of the board
    row1 = bottomRowCoordinates(app)
    col1 = leftColCoordinates(app)
    row2 = topRowCoordinates(app)
    col2 = rightColCoordinates(app)
    #createBoardCoordinates(app)
    for (x0, y0, x1, y1) in row1:
        #print("x0: ", x0, "y0: ", y0, "x1: ", x1, "y1: ", y1)
        canvas.create_rectangle(x0, y0, x1, y1, outline = "black" )
    for (x0, y0, x1, y1) in col1:
        #print("x0: ", x0, "y0: ", y0, "x1: ", x1, "y1: ", y1)
        canvas.create_rectangle(x0, y0, x1, y1, outline = "black" )
    for (x0, y0, x1, y1) in row2:
        #print("x0: ", x0, "y0: ", y0, "x1: ", x1, "y1: ", y1)
        canvas.create_rectangle(x0, y0, x1, y1, outline = "black" )
    for (x0, y0, x1, y1) in col2:
        #print("x0: ", x0, "y0: ", y0, "x1: ", x1, "y1: ", y1)
        canvas.create_rectangle(x0, y0, x1, y1, outline = "black" )

def leftColCoordinates(app):
    #Gets the coordinates for the column of blocks on the left of the board
    col1 = []
    blockWidth = app.innerBoardLength/app.nBlocks
    startHeight = app.marginTop + app.boardWidth - app.innerMargin
    x0 = app.marginSide
    #canvas.create_line(x0, startHeight, x1, startHeight, outline = "purple")
    x1 = x0 + app.innerMargin
    #canvas.create_line(x0, startHeight, x1, startHeight, fill = "blue")
    for i in range(app.nBlocks):
        y0 = startHeight - (i+1)*blockWidth
        y1 = startHeight - (i)*blockWidth
        col1.append((x0, y0, x1 , y1))
    #print("length of col1: ", len(col1))
    return col1

def topRowCoordinates(app):
    #Gets the coordinates for the blocks on the top row of the board
    row2 = []
    blockWidth = app.innerBoardLength/app.nBlocks
    startWidth = app.marginSide + app.innerMargin
    y0 = app.marginTop
    y1 = y0 + app.innerMargin
    for i in range(app.nBlocks):
        x0 = startWidth + (i)*blockWidth
        x1 = startWidth + (i+1)*blockWidth
        row2.append((x0, y0, x1, y1))
    return row2

def rightColCoordinates(app):
    #Gets the coordinates for the blocks on the left column of the board
    col2 = []
    blockWidth = app.innerBoardLength/app.nBlocks
    startHeight = app.marginTop + app.innerMargin
    x0 = app.marginSide + app.innerMargin + app.innerBoardLength
    x1 = x0 + app.innerMargin

    for i in range(app.nBlocks):
        y0 = startHeight + (i)*blockWidth
        y1 = startHeight + (i+1)*blockWidth
        col2.append((x0, y0, x1, y1))
    return col2

###########Creating the Board##########################
#location, color, name, price
def createBoard(app):
    row1 = []
    goLocation = (app.marginSide + app.boardWidth, app.marginTop+app.boardWidth,
        app.marginSide + app.boardWidth - app.innerMargin,
            app.marginTop+app.boardWidth - app.innerMargin)
    go = Corner(goLocation, None, "GO", 200, False)
    medAve = Block(app.boardCoordinates[0][0], "purple", "Med Ave",
        -60)
    cChest1 = SpecialCards(app.boardCoordinates[0][1], None, "Community Chest",
        None)
    balticAve = Block(app.boardCoordinates[0][2], "purple", "Baltic Ave", -60)
    incomeTax = Tax(app.boardCoordinates[0][3], None, "Income Tax", -200)
    rail1 = Railroad(app.boardCoordinates[0][4], None, "Reading Railroad", -200)
    orientalAve = Block(app.boardCoordinates[0][5], "grey", "Oriental Ave",
        -100)
    chance1 = SpecialCards(app.boardCoordinates[0][6], None, "Chance",
        None)
    vermontAve = Block(app.boardCoordinates[0][7], "grey", "Vermont Ave", -100)
    ctAve = Block(app.boardCoordinates[0][8], "grey", "CT Ave", -120)
    row1.extend([go, medAve, cChest1, balticAve, incomeTax, rail1, orientalAve,
        chance1, vermontAve, ctAve])

    col1 = []

    jailLocation = (app.marginSide, app.marginTop+app.boardWidth - 
        app.innerMargin,app.marginSide + app.innerMargin, app.marginTop + 
            app.boardWidth)
    jail = Corner(jailLocation, None, "Jail", None, False)
    stCharles = Block(app.boardCoordinates[1][0], "pink", "St. Charles Place",
        -140)
    electric = Utility(app.boardCoordinates[1][1], None, "Electric Company",
        -150)
    statesAve = Block(app.boardCoordinates[1][2], "pink", "States Ave", -140)
    vaAve = Block(app.boardCoordinates[1][3], "pink", "VA Ave",
        -160)
    rail2 = Railroad(app.boardCoordinates[1][4], None, "PA Railroad", -200)
    stJames = Block(app.boardCoordinates[1][5], "orange", "St. James Ave", 
        -180)
    cChest2 = SpecialCards(app.boardCoordinates[1][6], None, "Community Chest",
        None)
    tnAve = Block(app.boardCoordinates[1][7], "orange", "TN Ave", -180)
    nyAve = Block(app.boardCoordinates[1][8], "orange", "NY Ave", -200)
    col1.extend([jail, stCharles, electric, statesAve, vaAve, rail2, stJames,
        cChest2, tnAve, nyAve])
    
    row2 = []
    parkingLocation = (app.marginSide, app.marginTop, app.marginSide+
        app.innerMargin, app.marginTop+app.innerMargin)
    parking = Corner(parkingLocation, None, "Free", None, False)
    kyAve = Block(app.boardCoordinates[2][0], "red", "KY Ave", -220)
    chance2 = SpecialCards(app.boardCoordinates[2][1], None, "Chance", None)
    inAve = Block(app.boardCoordinates[2][2], "red", "IN Ave", -220)
    ilAve = Block(app.boardCoordinates[2][3], "red", "IL Ave", -240)
    rail3 = Railroad(app.boardCoordinates[2][4], None, "B&0 Railroad", -200)
    atlanticAve = Block(app.boardCoordinates[2][5], "yellow", "Atlantic Ave",
        -260)
    ventinorAve = Block(app.boardCoordinates[2][6], "yellow", "Ventinor Ave",
        -260)
    waterWorks = Utility(app.boardCoordinates[2][7], None, "Water Works", -150)
    marvinGardens = Block(app.boardCoordinates[2][8], "yellow", 
        "Marvin Gardens", -280)
    row2.extend([parking, kyAve, chance2, inAve, ilAve, rail3, atlanticAve, 
        ventinorAve, waterWorks, marvinGardens])
    
    col2 = []
    goToJailLoc = (app.marginSide + app.boardWidth - app.innerMargin,
        app.marginTop, app.marginSide+ app.boardWidth, 
             app.marginTop + app.innerMargin)
    goToJail = Corner(goToJailLoc, None, "Go To Jail", None, True)
    pacificAve = Block(app.boardCoordinates[3][0], "green", "Pacific Ave", 
        -300)
    ncAve = Block(app.boardCoordinates[3][1], "green", "NC Ave", -300)
    cChest3 = SpecialCards(app.boardCoordinates[3][2], None, "Community Chest", 
        None)
    paAve = Block(app.boardCoordinates[3][3], "green", "PA Ave", -320)
    rail4 = Railroad(app.boardCoordinates[3][4], None, "Short Line", -200)
    chance3 = SpecialCards(app.boardCoordinates[3][5], None, "Chance", None)
    parkPlace = Block(app.boardCoordinates[3][6], "blue", "Park Place", -350)
    luxTax = Tax(app.boardCoordinates[3][7], None, "Luxury Tax", -75)
    boardwalk = Block(app.boardCoordinates[3][8], "blue", "Boardwalk", -400)
    col2.extend([goToJail, pacificAve, ncAve, cChest3, paAve, rail4, chance3,
        parkPlace, luxTax, boardwalk])

    app.board.extend([row1, col1, row2, col2])
    #print("len of board",len(app.board))

def drawSideBlockDesign(app, canvas):
    #Filling in the blocks on the outside of the board
    margin = 25
    margin2 = 5
    margin3 = 50
    margin4 = 30
    for row in range(len(app.board)):
         for col in range(1, len(app.board[0])):
            curblock = app.board[row][col]
            x0, y0, x1, y1 = curblock.location
            if(row % 2 == 1):
                    if(curblock.color != None):
                        yDiff = y1-y0
                        xCenter = (x0 + x1)/2
                        canvas.create_rectangle(x0, y0, x1, y0 + yDiff/6, fill = curblock.color,
                            outline = "black")
                        canvas.create_text(xCenter, y0 + yDiff - margin, 
                            text = f'{curblock.name}',
                            font = "Arial 8 bold", fill = "black")
                        canvas.create_text(xCenter, y0 + yDiff - margin2, 
                            text = f'Price: ${abs(curblock.price)}',
                            font = "Arial 8 bold", fill = "black")
                    if(isinstance(curblock, SpecialCards)):
                        yDiff = y1-y0
                        xCenter = (x0 + x1)/2
                        if curblock.name == "Chance":
                            canvas.create_text(xCenter, y0 + yDiff - (margin4), text = f'{curblock.name}',
                                font = "Arial 8 bold", fill = "black")
                            canvas.create_text(xCenter, y0 + yDiff - margin/2, text = "?",
                                font = "Arial 24 bold", fill = "orange")
                        else:
                            name = curblock.name.split()
                            canvas.create_text(xCenter, y0 + yDiff - (margin4), text = name[0],
                                font = "Arial 8 bold", fill = "black")
                            canvas.create_text(xCenter, y0 + yDiff - (margin-margin2), text = name[1],
                                font = "Arial 8 bold", fill = "black")
                    if(isinstance(curblock, Tax)):
                        yDiff = y1-y0
                        xCenter = (x0 + x1)/2
                        canvas.create_text(xCenter, y0 + yDiff - (margin4), text = f'{curblock.name}',
                                font = "Arial 8 bold", fill = "black")
                        canvas.create_text(xCenter, y0 + yDiff - margin2, 
                            text = f'Pay: ${abs(curblock.price)}',
                            font = "Arial 8 bold", fill = "black")
                    if(isinstance(curblock, Utility) or isinstance(curblock, Railroad)):
                        yDiff = y1-y0
                        xCenter = (x0 + x1)/2
                        canvas.create_text(xCenter, y0 + yDiff - (margin4), text = f'{curblock.name}',
                                font = "Arial 8 bold", fill = "black")
                        canvas.create_text(xCenter, y0 + yDiff - margin2, 
                            text = f'Price: ${abs(curblock.price)}',
                            font = "Arial 8 bold", fill = "black")

                    
                        
def drawTopBlockDesign(app, canvas):
    #Drawing the design on the rows of blocks
    margin = 25
    margin2 = 5
    margin3 = 50
    margin4 = 30
    for row in range(len(app.board)):
         for col in range(1, len(app.board[0])):
            curblock = app.board[row][col]
            x0, y0, x1, y1 = curblock.location
            if(row % 2 == 0):
                if(curblock.color != None):
                    yDiff = y1-y0
                    xCenter = (x0 + x1)/2
                    canvas.create_rectangle(x0, y0, x1, y0 + yDiff/6, fill = curblock.color,
                        outline = "black")
                    canvas.create_text(xCenter, y0 + margin, 
                            text = f'{curblock.name}',
                            font = "Arial 5 bold", fill = "black")
                    canvas.create_text(xCenter, y0 + yDiff - margin2, 
                            text = f'Price: ${abs(curblock.price)}',
                            font = "Arial 5 bold", fill = "black")
                if(isinstance(curblock, SpecialCards)):
                    yDiff = y1-y0
                    xCenter = (x0 + x1)/2
                    if curblock.name == "Chance":
                        canvas.create_text(xCenter, y0 + margin/2 , 
                            text = f'{curblock.name}',
                            font = "Arial 5 bold", fill = "black")
                        canvas.create_text(xCenter, 
                            y0 + yDiff - margin - margin2, text = "?",
                            font = "Arial 50 bold", fill = "orange")
                    else:
                        name = curblock.name.split()
                        canvas.create_text(xCenter, 
                            y0 + margin/2, text = name[0],
                            font = "Arial 5 bold", fill = "black")
                        canvas.create_text(xCenter, 
                            y0 + yDiff - (margin3) -margin2, text = name[1],
                                font = "Arial 5 bold", fill = "black")
                if(isinstance(curblock, Tax)):
                        yDiff = y1-y0
                        xCenter = (x0 + x1)/2
                        canvas.create_text(xCenter, y0 + margin/2, 
                            text = f'{curblock.name}',
                            font = "Arial 5 bold", fill = "black")
                        canvas.create_text(xCenter, y0 + yDiff - margin4 - margin2, 
                            text = "Pay: 10% or ",
                            font = "Arial 5 bold", fill = "black")
                        canvas.create_text(xCenter, y0 + yDiff - margin4 + margin2, 
                            text = f'${abs(curblock.price)}',
                            font = "Arial 5 bold", fill = "black")
                if(isinstance(curblock, Utility) or isinstance(curblock, Railroad)):
                        yDiff = y1-y0
                        xCenter = (x0 + x1)/2
                        if(isinstance(curblock, Railroad)):
                            name = curblock.name.split()
                            canvas.create_text(xCenter, y0 + margin/2, text = name[0],
                                font = "Arial 5 bold", fill = "black")
                            canvas.create_text(xCenter, y0 + margin/2 + margin2,
                                text = name[1],
                                font = "Arial 5 bold", fill = "black")
                        else:
                            canvas.create_text(xCenter, y0 + margin/2, text = f'{curblock.name}',
                                font = "Arial 5 bold", fill = "black")
                        canvas.create_text(xCenter, y0 + yDiff - margin2, 
                            text = f'Price: ${abs(curblock.price)}',
                            font = "Arial 5 bold", fill = "black")

def getCenterOfBlock(app, blockNum):
    #Gives the position of the center of the block for the player to move to
    cols = len(app.board[0])
    row = blockNum // cols
    col = blockNum % cols
    x0, y0, x1, y1 = app.board[row][col].location
    centerX = (x0 + x1)/2
    centerY = (y0 + y1)/2
    return ((centerX, centerY))

def getCenter(app, pos):
    x0, y0, x1, y1 = pos
    centerX = (x0 + x1)/2
    centerY = (y0 + y1)/2
    return ((centerX, centerY))

def jailCoordinates(app):
    #sets the coordinates of the in jail/just vising block
    x0, y0, x1, y1 = app.board[1][0].location
    centerY = (y0 + y1)/2
    app.inJail = (x0, y0, x1, centerY)
    app.justVisiting = (x0, centerY, x1, y1)

def playMonopoly(app):
    startPosition1 = getCenterOfBlock(app, 0)
    offset = 10
    startPosition2 = (startPosition1[0] + offset, startPosition1[1] + offset)
    player1 = Player("Player 1", app.board, startPosition1, "aquamarine")
    player2 = Player("Player 2", app.board, startPosition2, "magenta")
    app.players.extend([player1, player2])

def drawPlayerBoard(app, canvas, player):
    cx, cy = player.position
    radius = 5
    canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, 
        fill = player.color, outline = "black")

def drawPlayerInfo(app, canvas, player, position):
    x, y = position
    canvas.create_text(x, y, text = f'{player.name}:', font = "Arial 24 bold",
        fill = 'black')
    offset, radius = 80, 20
    cx = x + offset
    canvas.create_oval(cx - radius, y - radius, cx + radius, y + radius, 
        fill = player.color, outline = "black")
    canvas.create_text(cx + 2*offset, y, text = f'Bank Account: ${player.bankaccount}',
        fill = "black", font = "Arial 24 bold")
    




    


                
  
    
                    


    


    
    
    










    


    
        
    

    

runApp(width=700, height=700)