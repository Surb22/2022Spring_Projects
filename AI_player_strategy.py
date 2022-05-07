"""
Code for AI with some predefined strategies:
1) Look for any boxes where three edges are occupied
2) Mark an edge on box with maximum score
3) Do not form the last edge on box with zero score
4) Do not mark edge on box with two occupied edges
"""

from tkinter import *
import numpy as np
import itertools
import random


size_of_board = 600
number_of_dots = 4
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
manipulated = []

class Dots_and_Boxes():

    def __init__(self):
        self.window = Tk()
        self.window.title('Dots_and_Boxes')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.list_board = []
        self.randomNumbers = [2, -3, 6, 15, 0, 8, -4, 3, 5]
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.refresh_board()
        self.play_again()
        self.zero_position_row=[]
        self.zero_position_col =[]
        position_zero = np.argwhere(self.board_status == 0)
        self.zero_position_row.append((position_zero[0][1], position_zero[0][0]))
        self.zero_position_row.append((position_zero[0][1], position_zero[0][0] + 1))
        self.zero_position_col.append((position_zero[0][1], position_zero[0][0]))
        self.zero_position_col.append((position_zero[0][1] + 1, position_zero[0][0]))
        self.board_status_score = np.array(self.randomNumbers).reshape(number_of_dots - 1, number_of_dots - 1).T
        self.score_list = list(itertools.chain(*self.board_status_score.tolist()))


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


    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]
        val = 1
        if c < (number_of_dots - 1) and r < (number_of_dots - 1):
            self.board_status[c][r] += val
            if self.board_status[c][r]==4:
                score_formed = self.board_status_score[c][r]
                self.score_list.remove(score_formed)
            if self.board_status[c][r] == 4 and self.player1_turn:
                self.board_status[c][r] = -4
        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c - 1][r] += val
                if self.board_status[c - 1][r] == 4:
                    score_formed = self.board_status_score[c-1][r]
                    self.score_list.remove(score_formed)
                if self.board_status[c - 1][r] == 4 and self.player1_turn:
                    self.board_status[c - 1][r] = -4
        if type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r - 1] += val
                if self.board_status[c][r-1] == 4:
                    score_formed = self.board_status_score[c][r-1]
                    self.score_list.remove(score_formed)
                if self.board_status[c][r - 1] == 4 and self.player1_turn:
                    self.board_status[c][r - 1] = -4


    def is_gameover(self):
        return (self.row_status != 0).all() and (self.col_status != 0).all()


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
                player1_weighted_score = player1_weighted_score * self.board_status_score[index[0]][index[1]]
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
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True
        # score_text = 'Click to play again \n'
        # self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
        #                         text=score_text)


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
                start_x = distance_between_dots * i + distance_between_dots
                end_x = distance_between_dots * j + distance_between_dots
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
        self.score_player1_text = self.canvas.create_text(90, 20, font="cmr 15 bold", text=score_text_1,
                                                          fill=player1_color)

        self.canvas.delete(self.score_player2_text)
        score_text_2 = 'Player2' + ':' + str(player2_score)
        self.score_player2_text = self.canvas.create_text(90, 40, font="cmr 15 bold", text=score_text_2,
                                                          fill=player2_color)


    def shade_box(self, box, color):
        start_x = distance_between_dots / 2 + box[1] * distance_between_dots + edge_width / 2
        start_y = distance_between_dots / 2 + box[0] * distance_between_dots + edge_width / 2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')


    def fill_three_side_box(self, score_list):
        """
        This function searches if the board has a box where three edges are occupied and returns
        the position of the fourth edge else returns a null value.
        :param score_list: list of weightages associated with boxes on the board
        :return: a string specifying : row or col and a tuple containing indices of a 2D array
        """

        player1_score, player2_score = self.score_track()
        score = score_list
         # score list contains score of all the boxes which can be formed in next turn
        if player2_score >= 1 and max(score) > 0:
            selected_score = max(score)
        elif player2_score < 0 and min(score) < 0:
            selected_score = min(score)
        elif player1_score<0 and player2_score<0 and (0 in score):
            selected_score = 0
        else:
            type = ''
            picked_position = []
            return type, picked_position
        zero_score_position = np.argwhere(self.board_status_score == 0)
        max_score_position = np.argwhere(self.board_status_score == selected_score)
        check_zero = ((max_score_position[0][0], max_score_position[0][1]))
        if selected_score != 0 and ((check_zero in self.zero_position_row) or \
                                    (check_zero in self.zero_position_col))\
                    and  self.board_status[zero_score_position[0][0],zero_score_position[0][1]] == 3:
            if len(score)>1:
                score.remove(selected_score)
                return self.fill_three_side_box(score)
            else:
                type = ''
                picked_position = []
                return type, picked_position

        if not (self.is_grid_occupied((max_score_position[0][1], max_score_position[0][0]), "row")):
            type = "row"
            picked_position = (max_score_position[0][1], max_score_position[0][0])
            return type, picked_position
        elif not (self.is_grid_occupied((max_score_position[0][1], max_score_position[0][0] + 1), "row")):
            type = "row"
            picked_position = (max_score_position[0][1], max_score_position[0][0] + 1)
            return type, picked_position
        elif not (self.is_grid_occupied((max_score_position[0][1], max_score_position[0][0]), "col")):
            type = "col"
            picked_position = (max_score_position[0][1], max_score_position[0][0])
            return type, picked_position
        elif not (self.is_grid_occupied((max_score_position[0][1] + 1, max_score_position[0][0]), "col")):
            type = "col"
            picked_position = (max_score_position[0][1] + 1, max_score_position[0][0])
            return type, picked_position
        else:
            type = ''
            picked_position = []
            return type, picked_position


    def max_score_move(self,try_score):
        """
        This function checks for the weightage of all unoccupied boxes on th board and selects the box
        which maximizes the score of the player and returns the position of one of the edges of the box.
        :param try_score: list of weightage associated with unoccupied boxes
        :return: a string specifying : row or col and a tuple containing indices of a 2D array
        """
        player1_score, player2_score = self.score_track()
        negative_present= False
        positive_present = False
        zero_present = False
        for value in try_score:
            if value<0:
                negative_present = True
            if value>0:
                positive_present = True
            if value==0:
                zero_present = True
        if player2_score >= 1 and positive_present :
            max_score = max(try_score)
        elif player2_score < 0 and negative_present:
            max_score = min(try_score)
        elif player2_score<0 and player1_score<0 and zero_present:
            max_score = 0
        else:
            type = ''
            picked_position = []
            return type, picked_position
        max_score_position = np.argwhere(self.board_status_score == max_score)
        possible_choices_row = []
        possible_choices_col = []
        row_position1 = self.is_grid_occupied((max_score_position[0][1], max_score_position[0][0]), "row")
        row_position2 = self.is_grid_occupied((max_score_position[0][1], max_score_position[0][0] + 1), "row")
        col_position1 = self.is_grid_occupied((max_score_position[0][1], max_score_position[0][0]), "col")
        col_position2 = self.is_grid_occupied((max_score_position[0][1] + 1, max_score_position[0][0]), "col")
        if not row_position1:
            possible_choices_row.append((max_score_position[0][1], max_score_position[0][0]))
        if not row_position2:
            possible_choices_row.append((max_score_position[0][1], max_score_position[0][0] + 1))
        if not col_position1:
            possible_choices_col.append((max_score_position[0][1], max_score_position[0][0]))
        if not col_position2:
            possible_choices_col.append((max_score_position[0][1] + 1, max_score_position[0][0]))
        remove_list_row =[]
        remove_list_col =[]
        zero_score_position = np.argwhere(self.board_status_score == 0)
        if (player2_score>0 or player2_score<0 ) and  self.board_status[zero_score_position[0][0],zero_score_position[0][1]] == 3:
            for value in possible_choices_row:
                if value in self.zero_position_row:
                    remove_list_row.append(value)
                    possible_choices_row.remove(value)
            for value in possible_choices_col:
                if value in self.zero_position_col:
                    remove_list_col.append(value)
                    possible_choices_col.remove(value)
        if len(possible_choices_row) ==1 and len(possible_choices_col) ==2\
                or(len(possible_choices_row) == 2 and len(possible_choices_col) == 1)\
                or(len(possible_choices_row) == 2 and len(possible_choices_col) == 2):
            type = random.choice(["row", "col"])
            if type == "row":
                picked_position = random.choice(possible_choices_row)
            elif type == "col":
                picked_position = random.choice(possible_choices_col)
            return type, picked_position
        elif len(try_score)>1:
            try_score.remove(max_score)
            return self.max_score_move(try_score)
        else:
            type =''
            move=[]
            return type, move


    def valid_move(self):
        """
        This function generates a random move.
        :return: a string specifying : row or col and a tuple containing indices of a 2D array
        """
        score = random.choice(self.score_list)
        score_position = np.argwhere(self.board_status_score == score)
        if not self.is_grid_occupied((score_position[0][1], score_position[0][0]), "row"):
            type = "row"
            position = (score_position[0][1], score_position[0][0])
            return type,position
        if not self.is_grid_occupied((score_position[0][1], score_position[0][0] + 1), "row"):
            type = "row"
            position = (score_position[0][1], score_position[0][0] + 1)
            return type,position
        if not self.is_grid_occupied((score_position[0][1], score_position[0][0]), "col"):
            type = "col"
            position = (score_position[0][1], score_position[0][0])
            return type,position
        if not self.is_grid_occupied((score_position[0][1] + 1, score_position[0][0]), "col"):
            type = "col"
            position = (score_position[0][1] + 1, score_position[0][0])
            return type,position


    def generate_move_ai(self):
        """
        Generates a move for the player with strategy.
        :return: a string specifying : row or col and a tuple containing indices of a 2D array
        """
        if len(self.score_list) != 0:
            move = []
            possibility_1 = np.argwhere(self.board_status == 3)
            if len(possibility_1) > 0:
                score=[]
                list_of_possible_score = possibility_1
                for value in list_of_possible_score:
                    score.append(self.board_status_score[value[0], value[1]])
                type, move = self.fill_three_side_box(score)
            if len(move) == 0:
                try_score_list = self.score_list.copy()
                type,move = self.max_score_move(try_score_list)
            if len(move) == 0:
                type,move = self.valid_move()
            return type, move


    def mark_move(self, event, move):
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
                if not self.player1_turn:
                    self.get_move()
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


    def get_move(self):
        if len(self.score_list) == 0:
            self.display_gameover()
        else:
            type, move = self.generate_move_ai()
            move_list = []
            move_list.append(move)
            move_list.append(type)
            event = []
            self.mark_move(event, move_list)


    def click(self, event):
        move_list = []
        self.mark_move(event, move_list)
        if not self.player1_turn:
            self.get_move()


game_instance = Dots_and_Boxes()
game_instance.mainloop()