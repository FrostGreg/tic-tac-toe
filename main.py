import pygame
import random
from classes import colours
from classes import position


class TicTacToe:
    def __init__(self):
        pygame.init()
        display_height = 800
        display_width = 800
        self.game_display = pygame.display.set_mode((display_width, display_height))
        pygame.display.set_caption("Tic Tac Toe")

        self.is_cross_turn = True
        self.game_mode = "1V1"
        self.difficulty = "Easy"
        self.pick = ""

        self.active_grid = ['TL', 'TC', 'TR',
                            'ML', 'MC', 'MR',
                            'BL', 'BC', 'BR']  # List of each active_grid grid piece

        self.grid_positions = {  # Dictionary that defines the positions of each grid square
            "TL": {"x_pos": position.LEFT, "y_pos": position.TOP},
            "TC": {"x_pos": position.CENTRE, "y_pos": position.TOP},
            "TR": {"x_pos": position.RIGHT, "y_pos": position.TOP},

            "ML": {"x_pos": position.LEFT, "y_pos": position.MIDDLE},
            "MC": {"x_pos": position.CENTRE, "y_pos": position.MIDDLE},
            "MR": {"x_pos": position.RIGHT, "y_pos": position.MIDDLE},

            "BL": {"x_pos": position.LEFT, "y_pos": position.BOTTOM},
            "BC": {"x_pos": position.CENTRE, "y_pos": position.BOTTOM},
            "BR": {"x_pos": position.RIGHT, "y_pos": position.BOTTOM}
        }

        self.positions = ["T", "M", "B", "L", "C", "R"]

        self.x_square = []
        self.o_square = []  # Initialising lists that define if a square is taken by X or O

        self.x_win = False
        self.o_win = False
        self.turn_count = 0

        self.program_closed = False
        self.game_finished = False
        self.clock = pygame.time.Clock()

        self.setup()

        while not self.program_closed:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.program_closed = True  # If the user presses the colours.RED X it closes the window

            self.mouse = pygame.mouse.get_pos()  # gets position of mouse and if its been clicked
            self.click = pygame.mouse.get_pressed()

            x, y, w, h = 10, 10, 100, 50
            pygame.draw.rect(self.game_display, colours.DESATURATED_RD, (x, y, w, h))
            self.text_in_box(15, 'Play Again', colours.WHITE, (x + (w / 2)), (y + (h / 2)))
            if x + w > self.mouse[0] > x and y + h > self.mouse[1] > y:
                pygame.draw.rect(self.game_display, colours.RED, (x, y, w, h))
                self.text_in_box(15, 'Play Again', colours.WHITE, (x + (w / 2)), (y + (h / 2)))
                if self.click[0] == 1:
                    self.setup()

            x2, y2, w2, h2, x3 = 450, 650, 300, 50, 50
            dx, dy, dw, dh, dx2 = 450, 725, 120, 25, 630
            if self.game_mode == "PlayerVComputer":
                pygame.draw.rect(self.game_display, colours.GREY, (x2, y2, w2, h2))
                self.text_in_box(15, "Player V Computer", colours.BLACK, (x2 + (w2 / 2)), (y2 + (h2 / 2)))

                if self.difficulty == "Hard":
                    self.button(dx, dy, dw, dh, colours.DESATURATED_GRN, colours.GREEN, "Easy", "Easy",
                                colours.BLACK)  # Displays Easy Button to be selected
                    pygame.draw.rect(self.game_display, colours.GREY,
                                     (dx2, dy, dw, dh))  # Makes the Hard Button invalid
                    self.text_in_box(15, "Hard", colours.BLACK, (dx2 + (dw / 2)), (dy + (dh / 2)))

                elif self.difficulty == "Easy":
                    self.button(dx2, dy, dw, dh, colours.RED, colours.DESATURATED_RD, "Hard", "Hard",
                                colours.BLACK)  # Displays Hard Button
                    pygame.draw.rect(self.game_display, colours.GREY,
                                     (dx, dy, dw, dh))  # Makes the Easy Button invalid
                    self.text_in_box(15, "Easy", colours.BLACK, (dx + (dw / 2)), (dy + (dh / 2)))

            else:
                self.button(x2, y2, w2, h2, colours.BLUE, colours.LIGHT_BLU, "PlayerVComputer",
                            "Player V Computer",
                            colours.WHITE)

            if self.game_mode == "1V1":
                pygame.draw.rect(self.game_display, colours.GREY, (x3, y2, w2, h2))
                self.text_in_box(15, "1 V 1", colours.BLACK, (x3 + (w2 / 2)), (y2 + (h2 / 2)))

                pygame.draw.rect(self.game_display, colours.BEIGE, (dx, dy, dw, dh))
                pygame.draw.rect(self.game_display, colours.BEIGE, (dx2, dy, dw, dh))
            else:
                self.button(x3, y2, w2, h2, colours.RED, colours.DESATURATED_RD, "1V1", "1 V 1",
                            colours.BLACK)

            if not self.game_finished:
                # Draws the rectangles for the buttons | Format (x1, y1, width, height, initial colour,
                # highlighted colour, Name in active_grid list)
                self.grid(position.LEFT, position.TOP, position.WIDTH, position.HEIGHT, colours.DESATURATED_BLK,
                          colours.BLACK, 'TL')
                self.grid(position.CENTRE, position.TOP, position.WIDTH, position.HEIGHT, colours.DESATURATED_BLK,
                          colours.BLACK, 'TC')  # TOP Layer
                self.grid(position.RIGHT, position.TOP, position.WIDTH, position.HEIGHT, colours.DESATURATED_BLK,
                          colours.BLACK, 'TR')

                self.grid(position.LEFT, position.MIDDLE, position.WIDTH, position.HEIGHT, colours.DESATURATED_BLK,
                          colours.BLACK, 'ML')
                self.grid(position.CENTRE, position.MIDDLE, position.WIDTH, position.HEIGHT, colours.DESATURATED_BLK,
                          colours.BLACK, 'MC')  # MIDDLE Layer
                self.grid(position.RIGHT, position.MIDDLE, position.WIDTH, position.HEIGHT, colours.DESATURATED_BLK,
                          colours.BLACK, 'MR')

                self.grid(position.LEFT, position.BOTTOM, position.WIDTH, position.HEIGHT, colours.DESATURATED_BLK,
                          colours.BLACK, 'BL')
                self.grid(position.CENTRE, position.BOTTOM, position.WIDTH, position.HEIGHT, colours.DESATURATED_BLK,
                          colours.BLACK, 'BC')  # BOTTOM Layer
                self.grid(position.RIGHT, position.BOTTOM, position.WIDTH, position.HEIGHT, colours.DESATURATED_BLK,
                          colours.BLACK, 'BR')

                if self.turn_count >= 5:
                    self.has_player_won("X")
                    self.has_player_won("O")
                    self.is_draw()

                if self.game_mode == "PlayerVComputer" and not self.game_finished:
                    if not self.is_cross_turn and self.turn_count < 9:
                        if self.difficulty == "Easy":
                            self.easy_move()
                        else:
                            self.best_move()  # Gets the best possible O pick
                        self.active_grid.remove(self.pick)
                        self.o_square.append(self.pick)
                        self.activate(self.grid_positions[self.pick]["x_pos"], self.grid_positions[self.pick]["y_pos"],
                                      position.WIDTH,
                                      position.HEIGHT, "O", colours.RED)  # Turns the Pick into a O square
                        self.is_cross_turn = True
                        self.turn_count += 1

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        quit()

    def setup(self):
        self.game_finished = self.x_win = self.o_win = False
        self.is_cross_turn = True
        self.turn_count = 0
        self.active_grid = ['TL', 'TC', 'TR', 'ML', 'MC', 'MR', 'BL', 'BC', 'BR']
        self.x_square.clear()
        self.o_square.clear()  # Resets the variables and lists for a new game

        self.game_display.fill(colours.BEIGE)  # Rebuilds the window
        self.text_in_box(100, 'Tic Tac Toe', colours.BLACK, 400, 50)

        line_width = 5
        line_length = 400
        line_x = 325
        line_y = 200
        gap_size = 150

        # Vertical Lines
        pygame.draw.rect(self.game_display, colours.DESATURATED_BLK, (line_x, line_y, line_width, line_length))
        pygame.draw.rect(self.game_display, colours.DESATURATED_BLK,
                         (line_x + gap_size, line_y, line_width, line_length))
        # Horizontal Lines
        pygame.draw.rect(self.game_display, colours.BLACK, (line_y, line_x, line_length, line_width))
        pygame.draw.rect(self.game_display, colours.BLACK, (line_y, line_x + gap_size, line_length, line_width))

        pygame.display.update()  # draws the board and refreshes the window

    def text_objects(self, text, font, colour):
        text_surface = font.render(text, True, colour)  # defines the colour of the text
        return text_surface, text_surface.get_rect()

    def text_in_box(self, size, text, colour, width, height):
        text_font = pygame.font.SysFont("centurygothic", size)  # size and font of text
        text_surf, text_rect = self.text_objects(text, text_font, colour)  # variables to run the text functions
        text_rect.center = (width, height)  # finds the center of the surface so that text is centralised
        self.game_display.blit(text_surf, text_rect)

    def button(self, x, y, w, h, initial_clr, hover_clr, function, text, colour):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:  # if the cursor is hovering over the button
            pygame.draw.rect(self.game_display, hover_clr, (x, y, w, h))  # highlights the button
            self.text_in_box(15, text, colour, (x + (w / 2)), (y + (h / 2)))
            if click[0] == 1:  # if right mouse button is pressed
                if function == "1V1" or function == "PlayerVComputer":
                    self.game_mode = function
                else:
                    self.difficulty = function
        else:
            pygame.draw.rect(self.game_display, initial_clr, (x, y, w, h))
            self.text_in_box(15, text, colour, (x + (w / 2)), (y + (h / 2)))  # Draws button if cursor is NOT on button

    def grid(self, x, y, w, h, initial_clr, hover_clr, pos):  # Function for grid buttons specifically
        if x + w > self.mouse[0] > x and y + h > self.mouse[1] > y and pos in self.active_grid:
            pygame.draw.rect(self.game_display, hover_clr, (x, y, w, h))
            if self.click[0] == 1:
                self.active_grid.remove(pos)
                if self.is_cross_turn:
                    self.x_square.append(pos)
                    self.activate(x, y, w, h, "X", colours.DESATURATED_GRN)
                    self.is_cross_turn = False

                else:
                    self.o_square.append(pos)
                    self.activate(x, y, w, h, "O", colours.RED)
                    self.is_cross_turn = True
                self.turn_count += 1

        elif pos in self.active_grid:
            pygame.draw.rect(self.game_display, initial_clr, (x, y, w, h))

    def activate(self, x, y, w, h, char, clr):
        pygame.draw.rect(self.game_display, clr, (x, y, w, h))
        width = x + (w / 2)
        height = y + (h / 2)
        self.text_in_box(50, char, colours.BLACK, width, height)

    def has_player_won(self, player):
        win = False
        if player == "X":
            captured = self.x_square
        else:
            captured = self.o_square

        for letter in self.positions:
            y = 0
            for pos in captured:
                if letter in pos:
                    y += 1

                if y == 3:
                    win = True

            if ('TL' in captured and 'MC' in captured and 'BR' in captured) or (
                    'TR' in captured and 'MC' in captured and 'BL' in captured):  # Checks Diagonal Lines
                win = True

            if win:
                self.text_in_box(40, player + " Wins", colours.BLACK, 400, 150)
                if player == "X":
                    self.x_win = True
                else:
                    self.o_win = True
                self.game_finished = True

    def is_draw(self):
        if not self.x_win and not self.o_win:
            if self.turn_count >= 9:
                self.text_in_box(40, 'Draw', colours.BLACK, 400, 150)
                self.game_finished = True

    def block_win(self):
        positions = ["T", "M", "B", ["L", "C", "R"]]
        x = 0  # index number for positions list

        for timesLooped in range(9):  # loops for every possibility i.e. 3x vertical, 3x horizontal, 2x diagonal
            if 0 <= timesLooped < 3:  # Searches horizontal
                pos_one = positions[x] + positions[3][0]
                pos_two = positions[x] + positions[3][1]
                pos_three = positions[x] + positions[3][2]
            elif 3 <= timesLooped < 6:  # Searches Vertical
                pos_one = positions[0] + positions[3][x]
                pos_two = positions[1] + positions[3][x]
                pos_three = positions[2] + positions[3][x]
            elif timesLooped == 6:  # Searches TOP - BOTTOM Diagonal
                pos_one = "TL"
                pos_two = "MC"
                pos_three = "BR"
            elif timesLooped == 7:  # Searches BOTTOM - TOP Diagonal
                pos_one = "TR"
                pos_two = "MC"
                pos_three = "BL"
            else:
                self.pick = None
                break

            if (pos_one in self.o_square and pos_two in self.o_square and pos_three in self.active_grid) or (
                    pos_one in self.x_square and pos_two in self.x_square and pos_three in self.active_grid):
                # Checks if two of the positions are taken by X and if the third is still available
                self.pick = pos_three  # Picks the third position to block the win
                break  # breaks the Loop as the best pick has been found
            elif (pos_two in self.o_square and pos_three in self.o_square and pos_one in self.active_grid) or (
                    pos_two in self.x_square and pos_three in self.x_square and pos_one in self.active_grid):
                self.pick = pos_one
                break
            elif (pos_three in self.o_square and pos_one in self.o_square and pos_two in self.active_grid) or (
                    pos_three in self.x_square and pos_one in self.x_square and pos_two in self.active_grid):
                self.pick = pos_two
                break
            else:
                x += 1  # Increments the index number meaning the positions searched will change
                if x > 2:  # Resets the index number if search continues through to the next stage
                    x = 0

    def pick_corner(self):
        corners = [["TL", "TR"], ["BR", "BL"]]
        for x in range(2):
            if corners[0][x] in self.o_square and corners[1][x] in self.active_grid:
                self.pick = corners[1][x]
            elif corners[1][x] in self.o_square and corners[0][x] in self.active_grid:
                self.pick = corners[0][x]

    def best_move(self):
        self.block_win()
        if self.pick is None:
            if "MC" in self.active_grid:
                self.pick = "MC"
            else:
                self.pick_corner()

        if self.pick is None:
            self.pick = random.choice(self.active_grid)

    def easy_move(self):
        self.pick = random.choice(self.active_grid)


if __name__ == "__main__":
    TicTacToe()
