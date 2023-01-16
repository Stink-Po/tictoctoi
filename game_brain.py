from constent import *
import numpy
from ai import AI


class GameBrain:

    def __init__(self):
        self.squares = numpy.zeros((ROW, COL))
        self.ai = AI()
        self.player = 1
        self.game_mode = "pvp"
        self.running = True
        self.empty_sqr = self.squares
        self.marked_sqr = 0
        self.player_1_score = 0
        self.player_2_score = 0
        self.final_game = False

    def final_state(self):
        # return 0 is there is no win yet
        # return 1 if player 1 win
        # return 2 if player 2 win
        # return local dict it hase a winner player and (x,y) of the winner status in board

        # vertical wins
        for col in range(COL):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                local_dict = {
                    "ipos": (col * SQSIZE + SQSIZE // 2, 20),
                    "fpos": (col * SQSIZE + SQSIZE // 2, WIDTH - 20),
                    "player": int(self.squares[0][col])
                }
                return self.squares[0][col], local_dict

        # horizontal wins
        for row in range(ROW):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                local_dict = {
                    "ipos": (20, row * SQSIZE + SQSIZE // 2),
                    "fpos": (WIDTH - 20, row * SQSIZE + SQSIZE // 2),
                    "player": int(self.squares[row][0])
                }
                return self.squares[row][0], local_dict

        # des winds
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            local_dict = {
                "ipos": (20, 20),
                "fpos": (WIDTH - 20, HEIGHT - 20),
                "player": int(self.squares[1][1])
            }
            return self.squares[1][1], local_dict

        # asc win
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            local_dict = {
                "ipos": (20, HEIGHT - 20),
                "fpos": (WIDTH - 20, 20),
                "player": int(self.squares[1][1])
            }
            return self.squares[1][1], local_dict

        return 0, None

    def mark(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqr += 1

    def empty_square(self, row, col):
        return self.squares[row][col] == 0

    # change the current player
    def change_player(self):
        self.player = self.player % 2 + 1

    # return True if board is full and false if not full
    def is_full(self):
        if self.marked_sqr == 9:
            return True
        else:
            return False

    # return true if the marked square is empty
    def is_empty(self):
        return self.marked_sqr == 0

    # return all the empty squares in board
    def get_empty_sqr(self):
        empty_sqr = []
        for row in range(ROW):
            for col in range(COL):
                if self.empty_square(row, col):
                    empty_sqr.append((row, col))

        return empty_sqr

    # change game mode from pvp to AI
    def change_mode(self):
        self.game_mode = "ai"

    # add a score to winner player
    def add_score(self, player):
        if player == 1:
            self.player_1_score += 1
        elif player == 2:
            self.player_2_score += 1

    # check if we are in the end of game or not
    def check_final(self):
        if self.player_1_score == 5:
            self.final_game = True
            self.running = False
            return self.final_game
        elif self.player_2_score == 5:
            self.final_game = True
            self.running = False
            return self.final_game

    # after each round this function rest the board
    def rest_board(self):
        self.squares = numpy.zeros((ROW, COL))

    # return winner3
    def winner(self):
        if self.final_game:
            if self.player_1_score > self.player_2_score:
                return 1
            elif self.player_2_score > self.player_1_score:
                return 2
