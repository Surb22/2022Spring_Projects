"""
Team members:
Shubhda Sharma - shubhda2
Surbhi Bhargava - surbhib2

Player1: AI based on MiniMax
Player2: AT based on predefined strategies
"""

import itertools
import random
from collections import deque
from copy import deepcopy
from tkinter import *
import numpy as np
from utility import playerAI


size_of_board = 600
number_of_dots = 6
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = '#7BC043'
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
player2_color = '#EE4035'
player2_color_light = '#EE7E77'
Green_color = '#7BC043'
dot_width = 0.25 * size_of_board / number_of_dots
edge_width = 0.1 * size_of_board / number_of_dots
distance_between_dots = size_of_board / (number_of_dots)


class Board:

    def __init__(self):
        self.window = Tk()
        self.window.title('Dots_and_Boxes')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.list_board = []
        self.score_list = []
        self.zero_position_row = []
        self.zero_position_col = []
        self.all_valid_moves = []
        self.aiplayer = playerAI()
        #self.randomNumbers = [3, -3, 4, 15, 0, 8, -6, 2, -5]
        self.randomNumbers = [3, -3, 4, 15, 0, 8, -6, 2, -5,9,10,-6,-4,-4,-9, 11, -12, 12, -2, 17, 22, 13, 14,15,-1]
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.refresh_board()
        self.play_again()
        #self.window.bind('<Return>', self.start_game())
        #self.start_game()

    def play_again(self):
        self.refresh_board()
        self.board_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))
        #self.board_status_score = np.array(self.randomNumbers).reshape(number_of_dots - 1, number_of_dots - 1).T
        self.row_status = np.zeros(shape=(number_of_dots, number_of_dots - 1))
        self.col_status = np.zeros(shape=(number_of_dots - 1, number_of_dots))
        # Input from user in form of clicks
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []
        self.flag = 0
        self.score_player1_text = []
        self.score_player2_text = []
        self.already_marked_boxes = []
        self.display_turn_text()
        self.alpha = -100000
        self.beta = 100000
        self.zero_position_row = []
        self.zero_position_col = []
        position_zero = np.argwhere(self.board_status == 0)
        self.zero_position_row.append((position_zero[0][1], position_zero[0][0]))
        self.zero_position_row.append((position_zero[0][1], position_zero[0][0] + 1))
        self.zero_position_col.append((position_zero[0][1], position_zero[0][0]))
        self.zero_position_col.append((position_zero[0][1] + 1, position_zero[0][0]))
        self.board_status_score = np.array(self.randomNumbers).reshape(number_of_dots - 1, number_of_dots - 1).T
        self.score_list = list(itertools.chain(*self.board_status_score.tolist()))
        #self.start_game()

    def click(self,event):
        self.start_game()

    def start_game(self):
        all_moves = self.get_all_valid_moves()
        while(len(all_moves)) > 0:
            if self.player1_turn:
                type, move = self.generate_move_ai_strategy()
                move_list = []
                move_list.append(move)
                move_list.append(type)
                event = []
                self.mark_move(event, move_list)
                self.refresh_board()
            else:
                event, move_list = self.get_move_ai()
                self.mark_move(event, move_list)


    def mainloop(self):
        self.window.mainloop()

    def is_grid_occupied(self, logical_position, type):
        r = logical_position[0]
        c = logical_position[1]
        occupied = True
        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False
        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False
        return occupied

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position - distance_between_dots / 4) // (distance_between_dots / 2)
        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0] - 1) // 2)
            c = int(position[1] // 2)
            logical_position = [r, c]
            type = 'row'

        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type

    def mark_box(self):
        boxes_p1 = np.argwhere(self.board_status == -4)

        for box in boxes_p1:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.flag = 10
                self.already_marked_boxes.append(list(box))
                color = player1_color_light
                self.shade_box(box, color)
        boxes_p2 = np.argwhere(self.board_status == 4)

        for box in boxes_p2:
            if list(box) not in self.already_marked_boxes and list(box) != []:
                self.flag = 10
                self.already_marked_boxes.append(list(box))
                color = player2_color_light
                self.shade_box(box, color)

    def is_gameover(self):
        return (self.row_status != 0).all() and (self.col_status != 0).all()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x + distance_between_dots
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y
        elif type == 'col':
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x

        if self.player1_turn:
           color = player1_color
        else:
           color = player2_color
        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=edge_width)

    def score_track(self):
        player1_score_positions = np.argwhere(self.board_status == -4)
        player1_weighted_score = 1
        if len(player1_score_positions) != 0:
            for index in player1_score_positions:
                player1_weighted_score = player1_weighted_score*self.board_status_score[index[0]][index[1]]

        player2_score_positions = np.argwhere(self.board_status == 4)
        player2_weighted_score = 1
        if len(player2_score_positions) != 0:
            for index in player2_score_positions:
                player2_weighted_score = player2_weighted_score * self.board_status_score[index[0]][index[1]]
        return player1_weighted_score, player2_weighted_score

    def display_gameover(self):
        player1_weighted_score, player2_weighted_score = self.score_track()
        if player1_weighted_score > player2_weighted_score:
            # Player 1 wins
            text = 'Winner: Player 1 '
            color = player1_color
        elif player2_weighted_score > player1_weighted_score:
            text = 'Winner: Player 2 '
            color = player2_color
        else:
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 : ' + str(player1_weighted_score) + '\n'
        score_text += 'Player 2 : ' + str(player2_weighted_score) + '\n'
        # score_text += 'Tie                    : ' + str(self.tie_score)
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

    def refresh_board(self):
        for i in range(number_of_dots):
            x = i * distance_between_dots + distance_between_dots / 2
            self.canvas.create_line(x, distance_between_dots / 2, x,
                                    size_of_board - distance_between_dots / 2,
                                    fill='gray', dash=(2, 2))
            self.canvas.create_line(distance_between_dots / 2, x,
                                    size_of_board - distance_between_dots / 2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(number_of_dots):
            for j in range(number_of_dots):
                start_x = i * distance_between_dots + distance_between_dots / 2
                end_x = j * distance_between_dots + distance_between_dots / 2
                self.canvas.create_oval(start_x - dot_width / 2, end_x - dot_width / 2, start_x + dot_width / 2,
                                        end_x + dot_width / 2, fill=dot_color,
                                        outline=dot_color)

        indx = -1
        for i in range(number_of_dots - 1):
            for j in range(number_of_dots - 1):
                indx = indx + 1
                start_x = distance_between_dots*i + distance_between_dots
                end_x = distance_between_dots*j + distance_between_dots
                self.canvas.create_text(start_x, end_x, font="cmr 30 bold", text=self.randomNumbers[indx], fill="red")

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = player1_color
        else:
            text += 'Player2'
            color = player2_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5 * len(text),
                                                       size_of_board - distance_between_dots / 8,
                                                       font="cmr 15 bold", text=text, fill=color)
        player1_score, player2_score = self.score_track()
        score_text_1 = 'Player1' + ':' + str(player1_score)

        self.canvas.delete(self.score_player1_text)
        self.score_player1_text = self.canvas.create_text(90,20, font="cmr 15 bold", text=score_text_1, fill=player1_color)

        self.canvas.delete(self.score_player2_text)
        score_text_2 = 'Player2' + ':' + str(player2_score)
        self.score_player2_text = self.canvas.create_text(90, 40, font="cmr 15 bold", text=score_text_2, fill=player2_color)

    def shade_box(self, box, color):
        start_x = distance_between_dots / 2 + box[1] * distance_between_dots + edge_width / 2
        start_y = distance_between_dots / 2 + box[0] * distance_between_dots + edge_width / 2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def mark_move(self,event, move):
        if not self.reset_board:
            if event:
                grid_position = [event.x, event.y]
                logical_positon, valid_input = self.convert_grid_to_logical_position(grid_position)
            else:
                logical_positon, valid_input = move[0], move[1]
            if valid_input and not self.is_grid_occupied(logical_positon, valid_input):
                self.update_board(valid_input, logical_positon)
                self.make_edge(valid_input, logical_positon)
                self.mark_box()
                self.refresh_board()
                if self.flag == 10:
                    self.flag = 0
                    self.player1_turn = self.player1_turn
                else:
                    self.flag = 0
                    self.player1_turn = not self.player1_turn
                if self.is_gameover():
                    self.display_gameover()
                else:
                    self.display_turn_text()
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False