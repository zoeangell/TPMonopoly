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
        #coordinates of jail just visiting
    canvas.create_rectangle(app.marginSide + app.boardWidth - app.innerMargin,
        app.marginTop, app.marginSide+ app.boardWidth, 
             app.marginTop + app.innerMargin,  outline = "black") #Go to jail coordinates
    drawBlocks(app, canvas)
 
def createBoardCoordinates(app):
    #Creating a 2D list of the blocks coordinates
    row1 = bottomRowCoordinates(app)
    app.boardCoordinates.append(row1)
    col1 = leftColCoordinates(app)
    app.boardCoordinates.append(col1)
    row2 = topRowCoordinates(app)
    app.boardCoordinates.append(row2)
    col2 = rightColCoordinates(app)
    app.baordCoordinates.append(col2)
    

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