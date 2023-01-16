import copy
import random


# if game mode is AI but is random mode( easy mode ) this function will choose for random AI
def rnd_choice(empty):
    empty_sqr = empty
    idx = random.randrange(0, len(empty_sqr))
    return empty_sqr[idx]


# AI function with minimax algorythm if game mode is AI and not in random mode
def minimax(board, maximizing):
    terminal = board.final_state()[0]
    full = board.is_full()
    case = terminal
    # player 1 wins
    if case == 1:
        return 1, None
    # player 2 wins
    if case == 2:
        return -1, None
    # draw
    elif full:
        return 0, None
    if maximizing:
        max_eval = -100
        best_move = None
        empty_sqr = board.get_empty_sqr()

        for (row, col) in empty_sqr:
            temp_board = copy.deepcopy(board)
            temp_board.mark(row, col, 1)

            ma_eval = minimax(temp_board, False)[0]
            if ma_eval > max_eval:
                max_eval = ma_eval
                best_move = (row, col)

        return max_eval, best_move

    elif not maximizing:
        min_eval = 100
        best_move = None
        empty_sqr = board.get_empty_sqr()

        for (row, col) in empty_sqr:
            temp_board = copy.deepcopy(board)
            temp_board.mark(row, col, board.player)
            mi_eval = minimax(temp_board, True)[0]
            if mi_eval < min_eval:
                min_eval = mi_eval
                best_move = (row, col)

        return min_eval, best_move


class AI:

    def __init__(self, player=2):
        self.level = 1
        self.player = player

    def eval(self, brain):
        if self.level == 0:
            # random choice
            empty = brain.get_empty_sqr()
            move = rnd_choice(empty)

        else:
            # minimax choice
            eval, move = minimax(board=brain, maximizing=False)

        return move  # return row and col
