import pygame
import random
from classes import colours
from classes import position


class TicTacToe:
    def __init__(self):
        pygame.init()
        # region 'Variables'
        display_height = 800
        display_width = 800
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption("Tic Tac Toe")

        self.PlayerCrossturn = True
        self.gameMode = "1V1"
        self.difficulty = "Easy"

        self.active = ['TL', 'TC', 'TR',
                       'ML', 'MC', 'MR',
                       'BL', 'BC', 'BR']  # List of each active grid piece

        self.GridData = {  # Dictionary that defines the positions of each grid square
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

        self.positions = ["T", "M", "B", "L", "C", "R"]

        self.Xsquare = []
        self.Osquare = []  # Initialising lists that define if a square is taken by X or O

        self.XWin = False
        self.OWin = False
        self.TurnCount = 0

        self.Closed = False
        self.Finished = False
        self.Clock = pygame.time.Clock()

        self.load()
        # region 'GameLoop'
        while not self.Closed:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.Closed = True  # If the user presses the colours.Colour.red X it closes the window

            self.mouse = pygame.mouse.get_pos()  # gets position of mouse and if its been clicked
            self.click = pygame.mouse.get_pressed()

            # region 'Buttons'
            x, y, w, h = 10, 10, 100, 50
            pygame.draw.rect(self.gameDisplay, colours.Colour.desatRed, (x, y, w, h))
            self.textinbox(15, 'Play Again', colours.Colour.white, (x + (w / 2)), (y + (h / 2)))
            if x + w > self.mouse[0] > x and y + h > self.mouse[1] > y:
                pygame.draw.rect(self.gameDisplay, colours.Colour.red, (x, y, w, h))
                self.textinbox(15, 'Play Again', colours.Colour.white, (x + (w / 2)), (y + (h / 2)))
                if self.click[0] == 1:
                    self.load()

            x2, y2, w2, h2, x3 = 450, 650, 300, 50, 50
            dx, dy, dw, dh, dx2 = 450, 725, 120, 25, 630
            if self.gameMode == "PlayerVComputer":
                pygame.draw.rect(self.gameDisplay, colours.Colour.grey, (x2, y2, w2, h2))
                self.textinbox(15, "Player V Computer", colours.Colour.black, (x2 + (w2 / 2)), (y2 + (h2 / 2)))

                if self.difficulty == "Hard":
                    self.button(dx, dy, dw, dh, colours.Colour.desatgreen, colours.Colour.darkgreen, "Easy", "Easy",
                                colours.Colour.black)  # Displays Easy Button to be selected
                    pygame.draw.rect(self.gameDisplay, colours.Colour.grey,
                                     (dx2, dy, dw, dh))  # Makes the Hard Button invalid
                    self.textinbox(15, "Hard", colours.Colour.black, (dx2 + (dw / 2)), (dy + (dh / 2)))

                elif self.difficulty == "Easy":
                    self.button(dx2, dy, dw, dh, colours.Colour.red, colours.Colour.desatRed, "Hard", "Hard",
                                colours.Colour.black)  # Displays Hard Button
                    pygame.draw.rect(self.gameDisplay, colours.Colour.grey,
                                     (dx, dy, dw, dh))  # Makes the Easy Button invalid
                    self.textinbox(15, "Easy", colours.Colour.black, (dx + (dw / 2)), (dy + (dh / 2)))

            else:
                self.button(x2, y2, w2, h2, colours.Colour.blue, colours.Colour.lightblue, "PlayerVComputer",
                            "Player V Computer",
                            colours.Colour.white)

            if self.gameMode == "1V1":
                pygame.draw.rect(self.gameDisplay, colours.Colour.grey, (x3, y2, w2, h2))
                self.textinbox(15, "1 V 1", colours.Colour.black, (x3 + (w2 / 2)), (y2 + (h2 / 2)))

                pygame.draw.rect(self.gameDisplay, colours.Colour.beige, (dx, dy, dw, dh))
                pygame.draw.rect(self.gameDisplay, colours.Colour.beige, (dx2, dy, dw, dh))
            else:
                self.button(x3, y2, w2, h2, colours.Colour.red, colours.Colour.desatRed, "1V1", "1 V 1",
                            colours.Colour.black)
            # endregion
            if not self.Finished:
                # Draws the rectangles for the buttons | Format (x1, y1, width, height, initial colour, highlighted colour, Name in active list)
                self.grid(position.Left, position.Top, position.Width, position.Height, colours.Colour.desatBlack,
                          colours.Colour.black, 'TL')
                self.grid(position.Centre, position.Top, position.Width, position.Height, colours.Colour.desatBlack,
                          colours.Colour.black, 'TC')  # Top Layer
                self.grid(position.Right, position.Top, position.Width, position.Height, colours.Colour.desatBlack,
                          colours.Colour.black, 'TR')

                self.grid(position.Left, position.Middle, position.Width, position.Height, colours.Colour.desatBlack,
                          colours.Colour.black, 'ML')
                self.grid(position.Centre, position.Middle, position.Width, position.Height, colours.Colour.desatBlack,
                          colours.Colour.black, 'MC')  # Middle Layer
                self.grid(position.Right, position.Middle, position.Width, position.Height, colours.Colour.desatBlack,
                          colours.Colour.black, 'MR')

                self.grid(position.Left, position.Bottom, position.Width, position.Height, colours.Colour.desatBlack,
                          colours.Colour.black, 'BL')
                self.grid(position.Centre, position.Bottom, position.Width, position.Height, colours.Colour.desatBlack,
                          colours.Colour.black, 'BC')  # Bottom Layer
                self.grid(position.Right, position.Bottom, position.Width, position.Height, colours.Colour.desatBlack,
                          colours.Colour.black, 'BR')

                if self.TurnCount >= 5:
                    self.checkX()
                    self.checkO()
                    self.checkDraw()

                if self.gameMode == "PlayerVComputer" and not self.Finished:
                    if not self.PlayerCrossturn and self.TurnCount < 9:
                        if self.difficulty == "Easy":
                            self.easyMove()
                        else:
                            self.bestMove()  # Gets the best possible O pick
                        self.active.remove(self.pick)
                        self.Osquare.append(self.pick)
                        self.naught(self.GridData[self.pick]["Xpos"], self.GridData[self.pick]["Ypos"], position.Width,
                                    position.Height)  # Turns the Pick into a O square
                        self.PlayerCrossturn = True
                        self.TurnCount += 1

            pygame.display.update()
            self.Clock.tick(60)

        # endregion
        pygame.quit()
        quit()

        # endregion

        # region 'Functions'

    def load(self):
        #global PlayerCrossturn, TurnCount, active, Xsquare, Osquare, Finished, XWin, OWin
        self.Finished = False
        self.XWin = False
        self.OWin = False
        self.PlayerCrossturn = True
        self.TurnCount = 0
        self.active = ['TL', 'TC', 'TR', 'ML', 'MC', 'MR', 'BL', 'BC', 'BR']
        self.Xsquare.clear()
        self.Osquare.clear()  # Resets the variables and lists for a new game

        self.gameDisplay.fill(colours.Colour.beige)  # Rebuilds the window
        self.textinbox(100, 'Tic Tac Toe', colours.Colour.black, 400, 50)

        pygame.draw.rect(self.gameDisplay, colours.Colour.desatBlack, (325, 200, 5, 400))  # Vertical Lines
        pygame.draw.rect(self.gameDisplay, colours.Colour.desatBlack, (475, 200, 5, 400))

        pygame.draw.rect(self.gameDisplay, colours.Colour.black, (200, 325, 400, 5))  # Horizontal Lines
        pygame.draw.rect(self.gameDisplay, colours.Colour.black, (200, 475, 400, 5))

        pygame.display.update()  # draws the board and refreshes the window

    def text_objects(self, text, font, colour):
        textSurface = font.render(text, True, colour)  # defines the colour of the text
        return textSurface, textSurface.get_rect()

    def textinbox(self, size, text, colour, width, height):
        textFont = pygame.font.SysFont("centurygothic", size)  # size and font of text
        textSurf, textRect = self.text_objects(text, textFont, colour)  # variables to run the text functions
        textRect.center = (width, height)  # finds the center of the surface so that text is centralised
        self.gameDisplay.blit(textSurf, textRect)

    def button(self, x, y, w, h, ic, ac, function, text, colour):
        #global gameMode, difficulty
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:  # if the cursor is hovering over the button
            pygame.draw.rect(self.gameDisplay, ac, (x, y, w, h))  # highlights the button
            self.textinbox(15, text, colour, (x + (w / 2)), (y + (h / 2)))
            if click[0] == 1:  # if right mouse button is pressed
                if function == "1V1" or function == "PlayerVComputer":
                    self.gameMode = function
                else:
                    self.difficulty = function
        else:
            pygame.draw.rect(self.gameDisplay, ic, (x, y, w, h))
            self.textinbox(15, text, colour, (x + (w / 2)), (y + (h / 2)))  # Draws button if cursor is NOT on button

    def grid(self, x, y, w, h, ic, ac, pos):  # Function for grid buttons specifically
        #global PlayerCrossturn, TurnCount, mouse, click

        if x + w > self.mouse[0] > x and y + h > self.mouse[1] > y and pos in self.active:
            pygame.draw.rect(self.gameDisplay, ac, (x, y, w, h))
            if self.click[0] == 1 and self.PlayerCrossturn:
                self.active.remove(pos)
                self.Xsquare.append(pos)
                self.cross(x, y, w, h)
                self.PlayerCrossturn = False
                self.TurnCount += 1

            elif self.click[0] == 1 and not self.PlayerCrossturn:
                self.active.remove(pos)
                self.Osquare.append(pos)
                self.naught(x, y, w, h)
                self.PlayerCrossturn = True
                self.TurnCount += 1

        elif pos in self.active:
            pygame.draw.rect(self.gameDisplay, ic, (x, y, w, h))

    def cross(self, x, y, w, h):
        pygame.draw.rect(self.gameDisplay, colours.Colour.desatgreen, (x, y, w, h))
        width = x + (w / 2)
        height = y + (h / 2)
        self.textinbox(50, 'X', colours.Colour.black, width, height)

    def naught(self, x, y, w, h):
        pygame.draw.rect(self.gameDisplay, colours.Colour.red, (x, y, w, h))
        width = x + (w / 2)
        height = y + (h / 2)
        self.textinbox(50, 'O', colours.Colour.black, width, height)

        # region 'Check for end'

    def checkX(self):
        #global XWin, Finished, positions
        for letter in self.positions:  # Loops through every letter in positions
            y = 0  # Resets y if 3 of the same letter isnt found
            for i in self.Xsquare:  # for every square in Xsquare
                if letter in i:  # If position of sqauare contains the letter
                    y += 1

            if y == 3:
                self.XWin = True

        if ('TL' in self.Xsquare and 'MC' in self.Xsquare and 'BR' in self.Xsquare) or (
                'TR' in self.Xsquare and 'MC' in self.Xsquare and 'BL' in self.Xsquare):  # Checks Diagonal Lines
            self.XWin = True

        if self.XWin:
            self.textinbox(40, 'X Wins', colours.Colour.black, 400, 150)
            self.Finished = True

    def checkO(self):
        #global OWin, Finished, positions
        for letter in self.positions:
            y = 0
            for i in self.Osquare:
                if letter in i:
                    y += 1

            if y == 3:
                self.OWin = True

        if ('TL' in self.Osquare and 'MC' in self.Osquare and 'BR' in self.Osquare) or (
                'TR' in self.Osquare and 'MC' in self.Osquare and 'BL' in self.Osquare):  # Checks Diagonal Lines
            self.OWin = True

        if self.OWin:
            self.textinbox(40, 'O Wins', colours.Colour.black, 400, 150)
            self.Finished = True

    def checkDraw(self):
        #global Finished
        if not self.XWin and not self.OWin:
            if self.TurnCount >= 9:
                self.textinbox(40, 'Draw', colours.Colour.black, 400, 150)
                self.Finished = True

        # endregion

        # region 'Finding the best move'

    def WinBlock(self):
        #global Xsquare, Osqaure, pick, active, posone, postwo, posthree
        positions = ["T", "M", "B", ["L", "C", "R"]]
        x = 0  # index number for positions list
        self.posone = ""
        self.postwo = ""  # Declares the search variables
        self.posthree = ""

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
                self.pick = None
                break

            if (posone in self.Osquare and postwo in self.Osquare and posthree in self.active) or (
                    posone in self.Xsquare and postwo in self.Xsquare and posthree in self.active):  # Checks if two of the positions are taken by X and if the third is still available
                self.pick = posthree  # Picks the third position to block the win
                break  # breaks the Loop as the best pick has been found
            elif (postwo in self.Osquare and posthree in self.Osquare and posone in self.active) or (
                    postwo in self.Xsquare and posthree in self.Xsquare and posone in self.active):
                self.pick = posone
                break
            elif (posthree in self.Osquare and posone in self.Osquare and postwo in self.active) or (
                    posthree in self.Xsquare and posone in self.Xsquare and postwo in self.active):
                self.pick = postwo
                break
            else:
                x += 1  # Increments the index number meaning the positions searched will change
                if x > 2:  # Resets the index number if search continues through to the next stage
                    x = 0

    def cornerPick(self):
        #global pick, active, Osquare
        corners = [["TL", "TR"], ["BR", "BL"]]
        for x in range(2):
            if corners[0][x] in self.Osquare and corners[1][x] in self.active:
                self.pick = corners[1][x]
            elif corners[1][x] in self.Osquare and corners[0][x] in self.active:
                self.pick = corners[0][x]

    def bestMove(self):
        #global pick, active
        self.WinBlock()
        if self.pick is None:
            if "MC" in self.active:
                pick = "MC"
            else:
                self.cornerPick()

        if self.pick is None:
            self.pick = random.choice(self.active)

    def easyMove(self):
        #global pick, active
        if "MC" in self.active:
            self.pick = "MC"
        else:
            self.pick = random.choice(self.active)

        # endregion
        # endregion


if __name__ == "__main__":
    TicTacToe()
