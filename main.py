from cmu_112_graphics import *
import random

def appStarted(app):
    app.boardWidth = 500
    app.marginSide = 50
    app.marginTop = 150
    app.innerMargin = 75
    app.innerBoardLength = app.boardWidth - 2*app.innerMargin
    app.boardCoordinates = []
    app.nBlocks = 9
    
def keyPressed(app, event):
    if (event.key == "Space"):
        leftColCoordinates(app)

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
    getInJail(app, x0, y0, x1, y1)
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
    

#def getInJail(app, x0, y0, x1, y1):
    #return ()






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









    


    
        
    

    

runApp(width=700, height=700)