from cmu_112_graphics import *
import random
from block import *
from player import *

###CITATION:
#The commands app.getUserInput and app.showMessage come from:
#https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html
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
    app.newblock = None
    app.curPlayer = None
    app.otherPlayer = None
    app.endgame = False
    app.newGame = True
    app.passedGo = False
    app.newTurn = False
    app.colorDict = {}
    app.playerMoved = False
    app.blockActions, app.specialBA = False, True
    app.roll = None
    app.cChestCoordinates = None
    app.chanceCoordinates = None
    app.landedOnChance, app.landedOnCChest = False, False
    app.pickedCard = False
    createBoardCoordinates(app)
    createBoard(app)
    app.totalBlocks = len(app.board) * len(app.board[0])
    getCChestCoordinates(app)
    getChanceCoordinates(app)
    jailCoordinates(app)
    playMonopoly(app)

def keyPressed(app, event):
    #Need to fix the weird behavior on the corners
    if app.curPlayer != None:
        curblock = app.curPlayer.curBlock()
        #("curblock: ", curblock) 
        row = curblock // 10
        if curblock == app.newblock:
            app.playerMoved = True
        else:
            if ((event.key == "Left" and row == 0) or 
                (event.key == "Up" and row  == 1) or
                (event.key == "Right" and row == 2) or
                (event.key == "Down" and row ==3)):
                app.curPlayer.position = getCenterOfBlock(app, (curblock+1)%40, 
                app.curPlayer)

def timerFired(app):
    if(app.endgame):
        app.showMessage(f'Game over.')
    else:
        if app.newGame:
            startGame(app)
            app.newGame = False
        if(app.newTurn):
            updatePlayerPos(app)
            app.playerMoved = False
        if app.curPlayer.curBlock() == app.newblock:
            app.playerMoved = True
            if(app.passedGo): app.curPlayer.collect200()
            app.newTurn = False
        if(app.playerMoved and not app.blockActions):
            blockActions(app)
        if(app.blockActions and app.specialBA):
            switchPlayer(app)



def mousePressed(app, event):
    #Decides if the user clicked on the card piles in the center of the board
    #and if they should be allowed to pick a card.
    print("This function was called")
    if app.landedOnChance and not app.pickedCard:
        x0, y0, x1, y1 = app.chanceCoordinates
        if event.x >= x0 and event.x <= x1 and event.y >= y0 and event.y <= y1:
           app.pickedCard = True
           chanceAction(app)
    elif app.landedOnCChest and not app.pickedCard:
        x0, y0, x1, y1 = app.cChestCoordinates
        if event.x >= x0 and event.x <= x1 and event.y >= y0 and event.y <= y1:
           app.pickedCard = True
           cChestAction(app)


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
    drawPlayerBoard(app, canvas, app.player1)
    drawPlayerBoard(app, canvas, app.player2)
    drawPlayerInfo(app,canvas,app.player1,(app.marginSide, app.marginSide))
    drawPlayerInfo(app,canvas,app.player2,(app.marginSide,2*app.marginSide))
 
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
    #(app.boardCoordinates)

def getCChestCoordinates(app):
    #Sets the coordinates of the community chest card pile
    x0 = app.marginSide + 3*app.innerMargin/2
    x1 = x0 + 2*app.marginSide
    y0 = app.marginTop + 4*app.innerMargin/3
    y1 = y0 + app.innerMargin
    app.cChestCoordinates = (x0, y0, x1, y1)

def getChanceCoordinates(app):
    #Sets the coordinates of the chance card pile
    x1 = app.marginSide + app.innerBoardLength + app.innerMargin/2
    x0 = x1 - 2*app.marginSide
    y0 = app.marginTop + app.innerBoardLength - app.innerMargin/4
    y1 = y0 + app.innerMargin
    app.chanceCoordinates = (x0, y0, x1, y1)

def drawInnerBoard(app, canvas):
    #Draws the inside of the board meaning the monopoly and special cards
    x0 = app.marginSide + 3*app.innerMargin/2
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
    createColorDict(app)

def createColorDict(app):
    #Creates a dictionary mapping color to properties with that color
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            curblock = app.board[row][col]
            if curblock.color != None:
                #print(curblock.name)
                app.colorDict[curblock.color] = app.colorDict.get(curblock.color, 0)
                if app.colorDict[curblock.color] == 0:
                    app.colorDict[curblock.color] = [curblock]
                else:
                    app.colorDict[curblock.color].append(curblock)
    #print ("app.colorDict: ",app.colorDict)


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
            drawOwnership(app, canvas, curblock)
            drawHouse(app, canvas, curblock)
            drawHotel(app, canvas, curblock)
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

def drawOwnership(app, canvas, curblock):
    #This draws a little dot on the block showing ownership.
    x0, y0, x1, y1 = curblock.location
    margin2 = 5
    if curblock.ownership != None:
        #print("hey I own this property.")
        owner = curblock.ownership
        if owner == "Player 1":
            canvas.create_oval(x1 - 2*margin2, y1 - 3*margin2,
            x1 - margin2, y1 - 2*margin2, fill = app.player1.color, 
                outline = "black")  
        elif owner == "Player 2":
            canvas.create_oval(x1 - 2*margin2, y1 - 3*margin2,
            x1 - margin2, y1 - 2*margin2, fill = app.player2.color, 
                outline = "black") 

def drawHouse(app, canvas, curblock):
    x0, y0, x1, y1 = curblock.location
    centerY = (y0+y1)/2
    margin = 5
    owner = curblock.ownership
    if curblock.house > 0 and curblock.house < 4:
        for i in range(curblock.house):
            if owner == "Player 1":
                canvas.create_rectangle(x0 + margin*(1+i) + margin*i, centerY - margin, 
                    x0 + margin*(2+i) + margin*i, centerY + margin, fill = app.player1.color, 
                outline = "black")
            elif owner == "Player 2":
                canvas.create_rectangle(x0 + margin*(1+i) + margin*i, centerY - margin, 
                    x0 + margin*(2+i) + margin*i, centerY + margin, fill = app.player2.color, 
                outline = "black")

def drawHotel(app, canvas, curblock):
    x0, y0, x1, y1 = curblock.location
    centerY = (y0+y1)/2
    margin = 5
    owner = curblock.ownership
    if curblock.hotel > 0:
        if owner == "Player 1":
            canvas.create_rectangle(x0 + margin, centerY, x0 + 6*margin, 
                centerY - margin, fill = app.player1.color, 
                    outline = "black")
        elif owner == "Player 2":
            canvas.create_rectangle(x0 + margin, centerY, x0 + 6*margin, 
             centerY - margin, fill = app.player2.color, 
                outline = "black")
                                
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
            drawOwnership(app, canvas, curblock)
            drawHouse(app, canvas, curblock)
            drawHotel(app, canvas, curblock)
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

def getCenterOfBlock(app, blockNum, player):
    #Gives the position of the center of the block for the player to move to
    offset = 5
    cols = len(app.board[0])
    row = blockNum // cols
    col = blockNum % cols
    x0, y0, x1, y1 = app.board[row][col].location
    centerX = (x0 + x1)/2
    centerY = (y0 + y1)/2
    if player == None:
        return ((centerX - offset, centerY - offset))
    if "1" in player.name:
        return ((centerX - offset, centerY - offset))
    elif "2" in player.name:
        return ((centerX + offset, centerY + offset))

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
    offset = 5
    startPosition1 = getCenterOfBlock(app, 0, None)
    #(startPosition1)
    #test = getCenterOfBlock(app, 2, None)
    #print("test: ", test)
    startPosition2 = (startPosition1[0] + 2*offset, startPosition1[1] + 3*offset)
    app.player1 = Player("Player 1", app.board, startPosition1, "aquamarine")
    print("Player 1's starting jail position", app.player1.jail)
    app.player2 = Player("Player 2", app.board, startPosition2, "magenta")

def drawPlayerBoard(app, canvas, player):
    if player.jail:
        color = "black"
    else:
        color = player.color
    cx, cy = player.position
    radius = 5
    canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, 
        fill = color, outline = "black")

def drawPlayerInfo(app, canvas, player, position):
    x, y = position
    canvas.create_text(x, y, text = f'{player.name}:', font = "Arial 24 bold",
        fill = 'black')
    offset, radius = 80, 20
    cx = x + offset
    canvas.create_oval(cx - radius, y - radius, cx + radius, y + radius, 
        fill = player.color, outline = "black")
    canvas.create_text(cx + 2*offset, y, text = 
        f'Bank Account: ${(player.bankaccount)}',fill = "black", 
            font = "Arial 24 bold")
    

def movePlayer(app, player, distance):
    app.newblock = (player.curBlock() + distance) % app.totalBlocks
    app.passedGo = False
    checkPassGo(app, player.curBlock(), app.newblock)
    #print("newblock: ", app.newblock, "curblock: ", player.curBlock())

def checkPassGo(app, curblock, newblock):
    curRow = curblock // len(app.board[0])
    newRow = newblock // len(app.board[0])
    if curRow != 0 and newRow == 0:
        app.passedGo = True
#These are the functions for each step of player's turn
def updatePlayerPos(app):
    #Function for the game play algorithm
    #print("Current Player: ",app.curPlayer)
    #player1, player2 = app.players[0], app.players[1]
    app.showMessage(f"It's {app.curPlayer.name}'s turn.")
    print(app.curPlayer.jail)
    if app.curPlayer.jail:
        answer = app.getUserInput("Would you like to pay a $50 fine to get out of jail?")
        if answer != None and "yes" in answer.lower():
            app.curPlayer.payJailFine()
            app.showMessage("You are out of jail!")
            app.curPlayer.jail = False
            app.playerMoved = True
            app.newTurn = True
            
        else:
            roll = app.curPlayer.roll()
            if roll[0] == roll[1]: 
                app.showMessage("You rolled snake eyes! You are out of jail.")
                app.curPlayer.jail = False
                app.playerMoved = True
                app.newTurn = True
    else:
        roll = app.curPlayer.roll()
        rollTotal = roll[0] + roll[1]
        app.roll = rollTotal
        app.showMessage(f'You rolled {roll}. Use the arrow keys to move yourself {rollTotal} spaces.')
        #print("Current Player Before Move: ", app.curPlayer)
        movePlayer(app, app.curPlayer, rollTotal)
        app.newTurn = False

    #print("New Current Player: ", app.curPlayer)

       

def turnRoll(app, player1, player2):
    #The player who rolls a higher combined score gets to go first
    p1CombinedRoll, p2CombinedRoll = 0, 0
    while(p1CombinedRoll == p2CombinedRoll):
        player1roll = player1.roll()
        #print("player1roll ", player1roll )
        player2roll = player2.roll()
        #print("player2roll ", player2roll )
        p1CombinedRoll = player1roll[0] + player1roll[1]
        p2CombinedRoll = player2roll[0] + player2roll[1]
        if(p1CombinedRoll > p2CombinedRoll):
            app.curPlayer = player1
            app.otherPlayer = player2
        elif(p1CombinedRoll < p2CombinedRoll):
            app.curPlayer = player2
            app.otherPlayer = player1

def startGame(app):
    #turnRoll(app, app.player1, app.player2)
    app.newTurn = True
    #print("curPlayer: ", app.curPlayer)
    app.curPlayer = app.player1 #comment this to return to normal
    app.otherPlayer = app.player2 #comment this to return to normal
    app.showMessage(f'{app.curPlayer.name} rolled the higher score. They will go first.')
    
def cChestAction(app):
    #displays the cChest card and fulfills the message
    curblockNum = app.curPlayer.curBlock()
    curblock = app.curPlayer.getCurBlock(curblockNum)
    card = curblock.pickACard()
    app.showMessage(card.message)
    if "each player" in card.message and "Collect" in card.message:
        app.curPlayer.bankaccount += card.action
        app.otherPlayer.bankaccount -= card.action
    else:
        app.curPlayer.bankaccount += card.action
    app.specialBA = True
    

def chanceAction(app):
    #displays the chance card and fulfills the message
    pass

def blockActions(app):
    #This is where the player buys property and pays rent when applicable.
    curblockNum = app.curPlayer.curBlock()
    curblock = app.curPlayer.getCurBlock(curblockNum)
    #send player to Jail
    margin = 5
    if curblock.name == "Go To Jail":
        x0, y0, x1, y1 = app.inJail
        centerX = (x0 + x1)/2
        centerY = (y0 + y1)/2
        if app.curPlayer == app.player1:
            app.curPlayer.position = centerX - 5, centerY - 5
        else:
            app.curPlayer.position = centerX + 5, centerY + 5
        app.curPlayer.jail = True
        app.showMessage("You are now in jail!")
    #------------------------------------------------------------------
    if isinstance(curblock, SpecialCards):
        app.showMessage(f"You've landed on {curblock.name}. Click on the deck to pick a card.")
        if curblock.name == "Chance":
            app.landedOnChance = True
            app.pickedCard = False
        else:
            app.landedOnCChest = True
            app.pickedCard = False
        app.specialBA = False
    #--------------------------------------------------------
    if app.curPlayer.isOwned(app.otherPlayer, curblock) == None:
        if (app.curPlayer.canBuy(curblock)):
            answer = app.getUserInput(f"{curblock.name} is avaible for purchase. Would you like to buy the property? (Yes/No)")
            if answer != None and answer.lower() == "yes":
                app.curPlayer.buyBlock(curblock)
                app.showMessage(f'You now own {curblock.name}.')
    elif app.curPlayer.isOwned(app.otherPlayer, curblock ) == False:
        if isinstance(curblock, Utility):
            print("roll: ", app.roll)
            tax = app.curPlayer.payUtilityTax(curblock, app.roll, app.otherPlayer)
            app.showMessage(f'You paid ${tax} in tax.')
        elif isinstance(curblock, Railroad):
            tax = app.curPlayer.payRailroadTax(curblock, app.otherPlayer)
            app.showMessage(f'You paid ${tax} in tax.')
        else:
            app.curPlayer.payRent(curblock, app.otherPlayer)
            app.showMessage(f'You paid ${abs(curblock.rent())} in rent.')

    if isinstance(curblock, Tax):
        if curblock.name == "Income Tax":
            answer = app.getUserInput("You need to pay income tax. Would you like to pay 10% of your income or $200?")
            if answer == None or "10" in answer:
                app.curPlayer.payIncomeTax()
            else:
                app.curPlayer.payTax(curblock)
        else:
            app.curPlayer.payTax(curblock)
            app.showMessage(f'You paid ${abs(curblock.price)} in tax.')

    #testBuyHouses(app)
    #testBuyHotel(app) 
    #testRailroadTax(app)
    #testUtilityTax(app)
    buyOpponentsProperty(app)
    buyHouse(app)
    buyHotel(app)
    #if app.specialBA:
    app.blockActions = True

def buyOpponentsProperty(app):
    #Prompts the player with the opportunity to buy the other player's property
    flag = True
    #Write a new function property available
    opponentLand = app.curPlayer.opponentPropAvailable(app.otherPlayer)
    if len(opponentLand) != 0:
        message = app.getUserInput(f"Would you like buy any of {app.otherPlayer}'s property at twice the price?")
        if message != None and "yes" in message.lower():
            while(flag):
                blockName = app.getUserInput("Please enter the name of the property that you want to purchase. Hit cancel if you don't want to purchase any property.")
                if blockName == None: 
                    block = None
                    flag = False
                else:
                    block = app.curPlayer.getBlock(blockName)
                    if block == None:
                        app.showMessage("The name you entered wasn't valid.")
                    elif block.house != 0 or block.hotel != 0:
                        app.showMessage("You can't buy property has a house or hotel built on it.")
                    elif block not in opponentLand:
                        app.showMessage(f"{app.otherPlayer.name} doesn't own that property.")
                    else:
                        flag = False
            if block != None:
                if block in app.otherPlayer.land:
                    app.curPlayer.buyOpponentsProp(block, app.otherPlayer)
                    app.showMessage(f'You now own {block.name}.')
            print("curPlayer.land: ", app.curPlayer.land)
            print("other Player land: ", app.otherPlayer.land)

def buyHouse(app):
    #Let's the player buy a house
    houseOptions = []
    #print(app.board[0][1] in app.curPlayer.land)
    #print("curPlayer.land: ", app.curPlayer.land)
    for key in app.colorDict:
        land = app.colorDict[key]
        #print("land: ", land)
        flag, flag2 = True, True
        for prop in land:
            #print("prop: ", prop)
            if prop not in app.curPlayer.land or prop.hotel != 0: 
                flag = False
                break
            elif prop.house < 3:
                flag2 = False
        if flag and not flag2:
            houseOptions.append(key)
    #print("houseOptions: ", houseOptions)
    if houseOptions != []:
        answer = app.getUserInput(f"Do you want to buy a house in the {houseOptions} blocks? Enter yes/no")
        if answer != None and "yes" in answer.lower():
            flag = True
            while(flag):
                blockName = app.getUserInput("Please enter the name of the property that you want to buy a house on.")
                if blockName == None: 
                    break
                else:
                    block = app.curPlayer.getBlock(blockName)
                    if block == None or block.color not in houseOptions:
                        app.showMessage("The name you entered wasn't valid.")
                    elif block.house >= 3:
                        app.showMessage("You can't build any more houses on this property.")
                    else:
                        flag = False
            if not flag:
                app.curPlayer.buyHouse(block)
                app.showMessage(f'You now own a house on {block.name}')

    
def buyHotel(app):
    #This function lets a player buy a hotel if qualified
    hotelOptions = []
    #print("curPlayer.land: ", app.curPlayer.land)
    for key in app.colorDict:
        land = app.colorDict[key]
        #print("land: ", land)
        flag = True
        for prop in land:
            #print("prop: ", prop)
            if prop not in app.curPlayer.land or prop.house != 3: 
                flag = False
                break
        if flag:
            hotelOptions.append(key)
    if hotelOptions != []:
            answer = app.getUserInput(f"Do you want to buy a hotel in the {hotelOptions} blocks?")
            if answer != None and "yes" in answer.lower():
                flag = True
                while(flag):
                    blockName = app.getUserInput("Please enter the name of the property that you want to buy a hotel on.")
                    if blockName == None: 
                        break
                    else:
                        block = app.curPlayer.getBlock(blockName)
                        if block == None or block.color not in hotelOptions:
                            app.showMessage("The name you entered wasn't valid.")
                        elif block.hotel == 1:
                            app.showMessage("You can't build multiple hotels on the same property.")
                        else:
                            flag = False
                if not flag:
                    app.curPlayer.buyHotel(block)
                    app.showMessage(f'You now own a hotel on {block.name}')
    

def switchPlayer(app):
    #This switches the curPlayer when the turn is done
    #print(f'{app.curPlayer.name}: ', app.curPlayer.bankaccount)
    #print(f'{app.otherPlayer.name}: ', app.otherPlayer.bankaccount)
    if app.curPlayer.bankaccount <= 0:
        app.endgame = True
    if app.curPlayer == app.player1: 
        app.curPlayer = app.player2
        app.otherPlayer = app.player1
    else: 
        app.curPlayer = app.player1
        app.otherPlayer = app.player2
    app.newTurn = True
    app.blockActions = False


def testBuyHouses(app):
    #buying houses work
    app.curPlayer.land = []
    app.otherPlayer.land = []
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            curblock = app.board[row][col]
            if curblock.color != None:
                app.player2.land.append(curblock)
                curblock.ownership = app.player2.name

def testBuyHotel(app):
    #shows that buying hotels works
    testBuyHouses(app)
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            curblock = app.board[row][col]
            if curblock.color != None and curblock.hotel == 0:
                curblock.house = 3

#def testRailroadTax(app):
    #shows that the railroad tax is working
    #for row in range(len(app.board)):
        #for col in range(len(app.board[0])):
            #curblock = app.board[row][col]
            #if isinstance(curblock, Railroad):
                #curblock.ownership = app.player1.name
                #app.player1.land.append(curblock)
    #app.player1.land.pop()
    #app.player1.land.pop()

'''def testUtilityTax(app):
    for row in range(len(app.board)):
        for col in range(len(app.board[0])):
            curblock = app.board[row][col]
            if isinstance(curblock, Utility):
                curblock.ownership = app.player1.name
                app.player1.land.append(curblock)
    app.player1.land.pop()
    #app.player1.land.pop()'''

            

    



runApp(width=700, height=700)

    
    




    


                
  
    
                    


    


    
    
    










    


    
        
    

    

