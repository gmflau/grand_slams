# Author: Abraham Lau
# Created: 20 April, 2020
# Email: abejolau@gmail.com
#
# Copyright 2020

from tkinter import *
from PIL import Image
import numpy as np

size_of_board = 600
maze_size = 5
image_size = int(size_of_board / maze_size * 0.8)
image_offset = int(size_of_board / maze_size * 0.2) // 2



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
                fill="#FAFCFB", width=3)

        for i in range(size):
            self.canvas.create_line(0, (i + 1) * size_of_board / size, size_of_board, (i + 1) * size_of_board / size,
                fill="#FAFCFB", width=3)



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
        pass

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


    def is_grid_occupied():
        return False

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

        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


game_instance = Maze()
game_instance.mainloop(maze_size)
