import numpy as np


class playerAI:
    def __init__(self):
        self.size_of_board = 600
        self.number_of_dots = 6
        self.player1_starts = True
        self.randomNumbers = [3, -3, 4, 5, 0, 8, -6, 2, -5,9,10,-6,-4,-4,-9, 11, 1, 6, -2, 7, -8, -9, -10,-1,-1]
        self.board_status = np.zeros(shape=(self.number_of_dots - 1, self.number_of_dots - 1))
        self.board_status_score = np.array(self.randomNumbers).reshape(self.number_of_dots - 1, self.number_of_dots - 1).T
        self.row_status = np.zeros(shape=(self.number_of_dots, self.number_of_dots - 1))
        self.col_status = np.zeros(shape=(self.number_of_dots - 1, self.number_of_dots))
        self.flag = 0
        # Input from user in form of clicks
        self.player1_starts = not self.player1_starts
        self.player1_turn = not self.player1_starts
        self.reset_board = False

    def update_board_ai(self, type, logical_position, max_min):
        r = logical_position[0]
        c = logical_position[1]
        val = 1
        if c < (self.number_of_dots - 1) and r < (self.number_of_dots - 1):
            self.board_status[c][r] += val
            if self.board_status[c][r] == 4:
                score_formed = self.board_status_score[c][r]
                self.score_list.remove(score_formed)
            if self.board_status[c][r] == 4 and not max_min:
                self.board_status[c][r] = -4
        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c - 1][r] += val
                if self.board_status[c - 1][r] == 4:
                    score_formed = self.board_status_score[c - 1][r]
                    self.score_list.remove(score_formed)
                if self.board_status[c - 1][r] == 4 and not max_min:
                    self.board_status[c - 1][r] = -4
        if type == 'col':
            self.col_status[c][r] = 1

            if r >= 1:
                self.board_status[c][r - 1] += val
                if self.board_status[c][r - 1] == 4:
                    score_formed = self.board_status_score[c][r - 1]
                    self.score_list.remove(score_formed)
                if self.board_status[c][r - 1] == 4 and not max_min:
                    self.board_status[c][r - 1] = -4

    def score_track_ai(self):
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


