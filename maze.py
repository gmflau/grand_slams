# Author: aqeelanwar
# Created: 12 March,2020, 7:06 PM
# Email: aqeel.anwar@gatech.edu

from tkinter import *
from PIL import Image
import numpy as np

size_of_board = 600
maze_size = 5
image_size = int(size_of_board / maze_size * 0.8)
image_offset = int(size_of_board / maze_size * 0.2) // 2
print("image_offset => " + str(image_offset))

symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'


class Maze():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Maze Game')
        self.canvas = Canvas(self.window, width=size_of_board,
            height=size_of_board, background="#299961")
        self.canvas.pack()
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        # Initialize images
        rf_file = "images/RF-60x60-01.png"
        image = Image.open(rf_file)
        image = image.resize((image_size, image_size), Image.ANTIALIAS)
        image.save(rf_file)
        self.rf_image = PhotoImage(file = rf_file)

        rn_file = "images/RN-150x150-01.png"
        image = Image.open(rn_file)
        image = image.resize((image_size, image_size), Image.ANTIALIAS)
        image.save(rn_file)
        self.rn_image = PhotoImage(file = rn_file)

        tennis_file = "images/tennis-ball.png"
        image = Image.open(tennis_file)
        image = image.resize((image_size, image_size), Image.ANTIALIAS)
        image.save(tennis_file)
        self.tennis_image = PhotoImage(file = tennis_file)

        wim_file = "images/wim-logo.png"
        image = Image.open(wim_file)
        image = image.resize((image_size, image_size), Image.ANTIALIAS)
        image.save(wim_file)
        self.wim_image = PhotoImage(file = wim_file)

        fo_file = "images/french-open.png"
        image = Image.open(fo_file)
        image = image.resize((image_size, image_size), Image.ANTIALIAS)
        image.save(fo_file)
        self.fo_image = PhotoImage(file = fo_file)

        ao_file = "images/ao-logo.png"
        image = Image.open(ao_file)
        image = image.resize((image_size, image_size), Image.ANTIALIAS)
        image.save(ao_file)
        self.ao_image = PhotoImage(file = ao_file)

        us_file = "images/us-open.png"
        image = Image.open(us_file)
        image = image.resize((image_size, image_size), Image.ANTIALIAS)
        image.save(us_file)
        self.us_image = PhotoImage(file = us_file)

        # Initialize maze
        self.initialize_board(maze_size)
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(maze_size, maze_size))

        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0


    def mainloop(self, size):
        self.initialize_values(size)
        self.window.mainloop()

    def initialize_board(self, size):
        for i in range(size):
            self.canvas.create_line((i + 1) * size_of_board / size, 0, (i + 1) * size_of_board / size, size_of_board,
                fill="#FAFCFB")

        for i in range(size):
            self.canvas.create_line(0, (i + 1) * size_of_board / size, size_of_board, (i + 1) * size_of_board / size,
                fill="#FAFCFB")



    def initialize_values(self, size):
        # Set Federer at the center
        center_position = [ size_of_board // 2 , size_of_board // 2 ]
        print(center_position)
        logical_position = self.convert_grid_to_logical_position(center_position)
        print("logical position of center => " + str(logical_position))
#        self.draw_slam(logical_position, self.rf_image)
        print("initialize_values")
        for i in range(maze_size):
            for j in range(maze_size):
                self.draw_slam([i,j], self.tennis_image)

        self.draw_slam([2, 2], self.rf_image)
        self.draw_slam([0, 0], self.wim_image)
        self.draw_slam([4, 1], self.fo_image)
        self.draw_slam([1, 4], self.us_image)
        self.draw_slam([4, 4], self.ao_image)


    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def draw_slam(self, logical_position, slam_image):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        image = self.canvas.create_image((grid_position[0],
            grid_position[1]), anchor=NW, image=slam_image)

    def draw_O(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        image = self.canvas.create_image((grid_position[0],
            grid_position[1]), anchor=NW, image=self.rf_image)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        image = self.canvas.create_image((grid_position[0],
            grid_position[1]), anchor=NW, image=self.rn_image)


    def display_gameover(self):

        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")

        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O): ' + str(self.O_score) + '\n'
        score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / maze_size) * logical_position + image_offset

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / maze_size), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):

        r, c = np.where(self.board_status == 0)
        tie = False
        if len(r) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return gameover





    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_X_turns = not self.player_X_turns
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not self.player_X_turns

            # Check if game is concluded
            if self.is_gameover():
                self.display_gameover()
                # print('Done')
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


game_instance = Maze()
game_instance.mainloop(maze_size)
