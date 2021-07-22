import pygame
import random
from classes import colours
from classes import position

pygame.init()
# region 'Variables'
display_height = 800
display_width = 800
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Tic Tac Toe")

PlayerCrossturn = True
gameMode = "1V1"
difficulty = "Easy"

active = ['TL', 'TC', 'TR',
          'ML', 'MC', 'MR',
          'BL', 'BC', 'BR']  # List of each active grid piece

GridData = {  # Dictionary that defines the positions of each grid square
    "TL": {"Xpos": position.Left, "Ypos": position.Top},
    "TC": {"Xpos": position.Centre, "Ypos": position.Top},
    "TR": {"Xpos": position.Right, "Ypos": position.Top},

    "ML": {"Xpos": position.Left, "Ypos": position.Middle},
    "MC": {"Xpos": position.Centre, "Ypos": position.Middle},
    "MR": {"Xpos": position.Right, "Ypos": position.Middle},

    "BL": {"Xpos": position.Left, "Ypos": position.Bottom},
    "BC": {"Xpos": position.Centre, "Ypos": position.Bottom},
    "BR": {"Xpos": position.Right, "Ypos": position.Bottom}
}

positions = ["T", "M", "B", "L", "C", "R"]

Xsquare = []
Osquare = []  # Initialising lists that define if a square is taken by X or O

XWin = False
OWin = False
TurnCount = 0

Closed = False
Finished = False
Clock = pygame.time.Clock()


# endregion

# region 'Functions'


def load():
    global PlayerCrossturn, TurnCount, active, Xsquare, Osquare, Finished, XWin, OWin
    Finished = False
    XWin = False
    OWin = False
    PlayerCrossturn = True
    TurnCount = 0
    active = ['TL', 'TC', 'TR', 'ML', 'MC', 'MR', 'BL', 'BC', 'BR']
    Xsquare.clear()
    Osquare.clear()  # Resets the variables and lists for a new game

    gameDisplay.fill(colours.Colour.beige)  # Rebuilds the window
    textinbox(100, 'Tic Tac Toe', colours.Colour.black, 400, 50)

    pygame.draw.rect(gameDisplay, colours.Colour.desatBlack, (325, 200, 5, 400))  # Vertical Lines
    pygame.draw.rect(gameDisplay, colours.Colour.desatBlack, (475, 200, 5, 400))

    pygame.draw.rect(gameDisplay, colours.Colour.black, (200, 325, 400, 5))  # Horizontal Lines
    pygame.draw.rect(gameDisplay, colours.Colour.black, (200, 475, 400, 5))

    pygame.display.update()  # draws the board and refreshes the window


def text_objects(text, font, colour):
    textSurface = font.render(text, True, colour)  # defines the colour of the text
    return textSurface, textSurface.get_rect()


def textinbox(size, text, colour, width, height):
    textFont = pygame.font.SysFont("centurygothic", size)  # size and font of text
    textSurf, textRect = text_objects(text, textFont, colour)  # variables to run the text functions
    textRect.center = (width, height)  # finds the center of the surface so that text is centralised
    gameDisplay.blit(textSurf, textRect)


def button(x, y, w, h, ic, ac, function, text, colour):
    global gameMode, difficulty
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:  # if the cursor is hovering over the button
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))  # highlights the button
        textinbox(15, text, colour, (x + (w / 2)), (y + (h / 2)))
        if click[0] == 1:  # if right mouse button is pressed
            if function == "1V1" or function == "PlayerVComputer":
                gameMode = function
            else:
                difficulty = function
    else:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))
        textinbox(15, text, colour, (x + (w / 2)), (y + (h / 2)))  # Draws button if cursor is NOT on button


def grid(x, y, w, h, ic, ac, pos):  # Function for grid buttons specifically
    global PlayerCrossturn, TurnCount, mouse, click

    if x + w > mouse[0] > x and y + h > mouse[1] > y and pos in active:
        pygame.draw.rect(gameDisplay, ac, (x, y, w, h))
        if click[0] == 1 and PlayerCrossturn:
            active.remove(pos)
            Xsquare.append(pos)
            cross(x, y, w, h)
            PlayerCrossturn = False
            TurnCount += 1

        elif click[0] == 1 and not PlayerCrossturn:
            active.remove(pos)
            Osquare.append(pos)
            naught(x, y, w, h)
            PlayerCrossturn = True
            TurnCount += 1

    elif pos in active:
        pygame.draw.rect(gameDisplay, ic, (x, y, w, h))


def cross(x, y, w, h):
    pygame.draw.rect(gameDisplay, colours.Colour.desatgreen, (x, y, w, h))
    width = x + (w / 2)
    height = y + (h / 2)
    textinbox(50, 'X', colours.Colour.black, width, height)


def naught(x, y, w, h):
    pygame.draw.rect(gameDisplay, colours.Colour.red, (x, y, w, h))
    width = x + (w / 2)
    height = y + (h / 2)
    textinbox(50, 'O', colours.Colour.black, width, height)


# region 'Check for end'


def checkX():
    global XWin, Finished, positions
    for letter in positions:  # Loops through every letter in positions
        y = 0  # Resets y if 3 of the same letter isnt found
        for i in Xsquare:  # for every square in Xsquare
            if letter in i:  # If position of sqauare contains the letter
                y += 1

        if y == 3:
            XWin = True

    if ('TL' in Xsquare and 'MC' in Xsquare and 'BR' in Xsquare) or (
            'TR' in Xsquare and 'MC' in Xsquare and 'BL' in Xsquare):  # Checks Diagonal Lines
        XWin = True

    if XWin:
        textinbox(40, 'X Wins', colours.Colour.black, 400, 150)
        Finished = True


def checkO():
    global OWin, Finished, positions
    for letter in positions:
        y = 0
        for i in Osquare:
            if letter in i:
                y += 1

        if y == 3:
            OWin = True

    if ('TL' in Osquare and 'MC' in Osquare and 'BR' in Osquare) or (
            'TR' in Osquare and 'MC' in Osquare and 'BL' in Osquare):  # Checks Diagonal Lines
        OWin = True

    if OWin:
        textinbox(40, 'O Wins', colours.Colour.black, 400, 150)
        Finished = True


def checkDraw():
    global Finished
    if not XWin and not OWin:
        if TurnCount >= 9:
            textinbox(40, 'Draw', colours.Colour.black, 400, 150)
            Finished = True


# endregion

# region 'Finding the best move'


def WinBlock():
    global Xsquare, Osqaure, pick, active, posone, postwo, posthree
    positions = ["T", "M", "B", ["L", "C", "R"]]
    x = 0  # index number for positions list
    posone = ""
    postwo = ""  # Declares the search variables
    posthree = ""

    for timesLooped in range(9):  # loops for every possibility i.e. 3x vertical, 3x horizontal, 2x diagonal
        if timesLooped == 0 or timesLooped == 1 or timesLooped == 2:  # Searches Vertical
            posone = positions[x] + positions[3][0]
            postwo = positions[x] + positions[3][1]
            posthree = positions[x] + positions[3][2]
        elif timesLooped == 3 or timesLooped == 4 or timesLooped == 5:  # Searches Horizontal
            posone = positions[0] + positions[3][x]
            postwo = positions[1] + positions[3][x]
            posthree = positions[2] + positions[3][x]
        elif timesLooped == 6:  # Searches Top - Bottom Diagonal
            posone = "TL"
            postwo = "MC"
            posthree = "BR"
        elif timesLooped == 7:  # Searches Bottom - Top Diagonal
            posone = "TR"
            postwo = "MC"
            posthree = "BL"
        else:
            pick = None
            break

        if (posone in Osquare and postwo in Osquare and posthree in active) or (
                posone in Xsquare and postwo in Xsquare and posthree in active):  # Checks if two of the positions are taken by X and if the third is still available
            pick = posthree  # Picks the third position to block the win
            break  # breaks the Loop as the best pick has been found
        elif (postwo in Osquare and posthree in Osquare and posone in active) or (
                postwo in Xsquare and posthree in Xsquare and posone in active):
            pick = posone
            break
        elif (posthree in Osquare and posone in Osquare and postwo in active) or (
                posthree in Xsquare and posone in Xsquare and postwo in active):
            pick = postwo
            break
        else:
            x += 1  # Increments the index number meaning the positions searched will change
            if x > 2:  # Resets the index number if search continues through to the next stage
                x = 0


def cornerPick():
    global pick, active, Osquare
    corners = [["TL", "TR"], ["BR", "BL"]]
    for x in range(2):
        if corners[0][x] in Osquare and corners[1][x] in active:
            pick = corners[1][x]
        elif corners[1][x] in Osquare and corners[0][x] in active:
            pick = corners[0][x]


def bestMove():
    global pick, active
    WinBlock()
    if pick is None:
        if "MC" in active:
            pick = "MC"
        else:
            cornerPick()

    if pick is None:
        pick = random.choice(active)


def easyMove():
    global pick, active
    if "MC" in active:
        pick = "MC"
    else:
        pick = random.choice(active)


# endregion
# endregion
load()
# region 'GameLoop'
while not Closed:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            Closed = True  # If the user presses the colours.Colour.red X it closes the window

    mouse = pygame.mouse.get_pos()  # gets position of mouse and if its been clicked
    click = pygame.mouse.get_pressed()

    # region 'Buttons'
    x, y, w, h = 10, 10, 100, 50
    pygame.draw.rect(gameDisplay, colours.Colour.desatRed, (x, y, w, h))
    textinbox(15, 'Play Again', colours.Colour.white, (x + (w / 2)), (y + (h / 2)))
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, colours.Colour.red, (x, y, w, h))
        textinbox(15, 'Play Again', colours.Colour.white, (x + (w / 2)), (y + (h / 2)))
        if click[0] == 1:
            load()

    x2, y2, w2, h2, x3 = 450, 650, 300, 50, 50
    dx, dy, dw, dh, dx2 = 450, 725, 120, 25, 630
    if gameMode == "PlayerVComputer":
        pygame.draw.rect(gameDisplay, colours.Colour.grey, (x2, y2, w2, h2))
        textinbox(15, "Player V Computer", colours.Colour.black, (x2 + (w2 / 2)), (y2 + (h2 / 2)))

        if difficulty == "Hard":
            button(dx, dy, dw, dh, colours.Colour.desatgreen, colours.Colour.darkgreen, "Easy", "Easy",
                   colours.Colour.black)  # Displays Easy Button to be selected
            pygame.draw.rect(gameDisplay, colours.Colour.grey, (dx2, dy, dw, dh))  # Makes the Hard Button invalid
            textinbox(15, "Hard", colours.Colour.black, (dx2 + (dw / 2)), (dy + (dh / 2)))

        elif difficulty == "Easy":
            button(dx2, dy, dw, dh, colours.Colour.red, colours.Colour.desatRed, "Hard", "Hard",
                   colours.Colour.black)  # Displays Hard Button
            pygame.draw.rect(gameDisplay, colours.Colour.grey, (dx, dy, dw, dh))  # Makes the Easy Button invalid
            textinbox(15, "Easy", colours.Colour.black, (dx + (dw / 2)), (dy + (dh / 2)))

    else:
        button(x2, y2, w2, h2, colours.Colour.blue, colours.Colour.lightblue, "PlayerVComputer", "Player V Computer",
               colours.Colour.white)

    if gameMode == "1V1":
        pygame.draw.rect(gameDisplay, colours.Colour.grey, (x3, y2, w2, h2))
        textinbox(15, "1 V 1", colours.Colour.black, (x3 + (w2 / 2)), (y2 + (h2 / 2)))

        pygame.draw.rect(gameDisplay, colours.Colour.beige, (dx, dy, dw, dh))
        pygame.draw.rect(gameDisplay, colours.Colour.beige, (dx2, dy, dw, dh))
    else:
        button(x3, y2, w2, h2, colours.Colour.red, colours.Colour.desatRed, "1V1", "1 V 1", colours.Colour.black)
    # endregion
    if not Finished:
        # Draws the rectangles for the buttons | Format (x1, y1, width, height, initial colour, highlighted colour, Name in active list)
        grid(position.Left, position.Top, position.Width, position.Height, colours.Colour.desatBlack,
             colours.Colour.black, 'TL')
        grid(position.Centre, position.Top, position.Width, position.Height, colours.Colour.desatBlack,
             colours.Colour.black, 'TC')  # Top Layer
        grid(position.Right, position.Top, position.Width, position.Height, colours.Colour.desatBlack,
             colours.Colour.black, 'TR')

        grid(position.Left, position.Middle, position.Width, position.Height, colours.Colour.desatBlack,
             colours.Colour.black, 'ML')
        grid(position.Centre, position.Middle, position.Width, position.Height, colours.Colour.desatBlack,
             colours.Colour.black, 'MC')  # Middle Layer
        grid(position.Right, position.Middle, position.Width, position.Height, colours.Colour.desatBlack,
             colours.Colour.black, 'MR')

        grid(position.Left, position.Bottom, position.Width, position.Height, colours.Colour.desatBlack,
             colours.Colour.black, 'BL')
        grid(position.Centre, position.Bottom, position.Width, position.Height, colours.Colour.desatBlack,
             colours.Colour.black, 'BC')  # Bottom Layer
        grid(position.Right, position.Bottom, position.Width, position.Height, colours.Colour.desatBlack,
             colours.Colour.black, 'BR')

        if TurnCount >= 5:
            checkX()
            checkO()
            checkDraw()

        if gameMode == "PlayerVComputer" and not Finished:
            if not PlayerCrossturn and TurnCount < 9:
                if difficulty == "Easy":
                    easyMove()
                else:
                    bestMove()  # Gets the best possible O pick
                active.remove(pick)
                Osquare.append(pick)
                naught(GridData[pick]["Xpos"], GridData[pick]["Ypos"], position.Width,
                       position.Height)  # Turns the Pick into a O square
                PlayerCrossturn = True
                TurnCount += 1

    pygame.display.update()
    Clock.tick(60)

# endregion
pygame.quit()
quit()
