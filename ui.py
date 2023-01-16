import pygame
from constent import *
from game_brain import GameBrain


class Game:

    def __init__(self):
        self.brain = GameBrain()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic Tac Toi")
        self.draw_welcome()

    # drawing the welcome screen
    def draw_welcome(self):
        self.screen.fill(BG_COLOR)
        word_height = None
        font = pygame.font.SysFont("FiraCode", 20)
        collection = [word.split(" ") for word in TEXT.splitlines()]
        space = font.size(" ")[0]
        pos = (20, 20)
        x, y = pos
        for lines in collection:

            for words in lines:
                word_surface = font.render(words, True, TEXT_CLOR)
                word_width, word_height = word_surface.get_size()

                if x + word_width >= HEIGHT:
                    x = pos[0]
                    y += word_height
                self.screen.blit(word_surface, (x, y))
                pygame.time.delay(200)
                pygame.display.update()
                x += word_width + space
            x = pos[0]
            y += word_height

    # drawing the game board
    def draw_lines(self):

        self.screen.fill(BG_COLOR)
        pygame.draw.line(self.screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (SQSIZE + SQSIZE, 0), (SQSIZE + SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (0, SQSIZE + SQSIZE), (WIDTH, SQSIZE + SQSIZE), LINE_WIDTH)

    # check screen for user click and reaction  to user
    def check_click(self, event):
        print(self.brain.ai.level)
        if self.brain.final_state()[0] != 0 or self.brain.is_full():
            return
        pos = event.pos
        player = self.brain.player
        if self.brain.game_mode == "pvp":
            row = pos[1] // SQSIZE
            col = pos[0] // SQSIZE
            if self.brain.empty_square(row, col):
                self.brain.mark(row, col, player=player)
                self.draw_fig(row, col)
                self.brain.change_player()
        elif self.brain.game_mode == "ai" and player == 1:
            if self.brain.final_state()[0] != 0 or self.brain.is_full():
                return
            row = pos[1] // SQSIZE
            col = pos[0] // SQSIZE
            if self.brain.empty_square(row, col):
                self.brain.mark(row, col, player=player)
                self.draw_fig(row, col)
                self.brain.change_player()
                self.ai_turn()

    # DRAW  crinkle or cross on the game board
    def draw_fig(self, row, col):

        player = self.brain.player
        if player == 1:
            # draw cross
            start_dis = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_dis = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(self.screen, CROSS_COLOR, start_dis, end_dis, CROSS_WIDTH)
            start_asd = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asd = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(self.screen, CROSS_COLOR, start_asd, end_asd, CROSS_WIDTH)

        elif player == 2:
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            # draw circle
            pygame.draw.circle(self.screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)

    # if game mode is AI this function drawing for AI user
    def ai_draw(self, row, col):
        center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
        pygame.draw.circle(self.screen, CIRCLE_COLOR, center, RADIUS, CIRCLE_WIDTH)
        self.brain.mark(row, col, player=2)
        pygame.display.update()

    # if is the AI turn to choose this function do it
    def ai_turn(self):
        if self.brain.final_state()[0] != 0 or self.brain.is_full():
            return
        row, col = self.brain.ai.eval(brain=self.brain)
        self.ai_draw(row, col)
        pygame.display.update()
        self.brain.change_player()

    # this function drawing win or draw and after that showing current scores
    def draw_score(self):
        font = pygame.font.SysFont("FiraCode", 40)
        self.screen.fill(BG_COLOR)
        winner = int(self.brain.final_state()[0])
        self.brain.add_score(winner)
        if winner == 0:
            winner = "Draw"
        elif winner == 1:
            winner = "Player one Win !"
        elif winner == 2 and self.brain.game_mode == "pvp":
            winner = "Player two Win !"
        elif winner == 2 and self.brain.game_mode == "ai":
            winner = "AI Win !"
        word_surface = font.render(winner, True, TEXT_CLOR)
        if winner == "Draw":
            self.screen.blit(word_surface, (250, 250))
        elif winner == "Player one Win !" or winner == "Player two Win !":
            self.screen.blit(word_surface, (100, 250))
        else:
            self.screen.blit(word_surface, (230, 250))
        pygame.display.update()
        pygame.time.delay(5000)
        self.screen.fill(BG_COLOR)
        if self.brain.game_mode == "pvp":
            scores = f'Player One : {self.brain.player_1_score}\n' \
                     f'Plater Two :{self.brain.player_2_score}'
            self.draw_player_score(scores)
            pygame.display.update()
        if self.brain.game_mode == "ai":
            scores = f'Player One :{self.brain.player_1_score}\n' \
                     f'AI : {self.brain.player_2_score}'
            self.draw_player_score(scores)
            pygame.display.update()

        pygame.time.delay(500)
        if self.brain.player_1_score < 5 and self.brain.player_2_score < 5:
            self.screen.fill(BG_COLOR)
            pygame.time.delay(500)
            self.brain.rest_board()
            self.brain.marked_sqr = 0
            pygame.display.update()
            self.draw_lines()
            print(self.brain.player)

    # showing user scores in draw score function
    def draw_player_score(self, score):
        font = pygame.font.SysFont("FiraCode", 30)
        space = font.size(" ")[0]
        scores = score
        collection = [word.split(" ") for word in scores.splitlines()]
        pos = (190, 250)
        word_height = None
        x, y = pos
        for lines in collection:

            for words in lines:

                word_surface = font.render(words, True, TEXT_CLOR)
                word_width, word_height = word_surface.get_size()

                if x + word_width >= HEIGHT:
                    x = pos[0]
                    y += word_height
                self.screen.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]
            y += word_height

    # this function show the final score of the game and after while ask user to chosee
    # if you want to play again or quit the game
    def draw_final_score(self):
        winner = self.brain.winner()
        final_text = f"player {winner} win Press 'R' if you want to play again or 'Q' for quit the game"
        self.screen.fill(BG_COLOR)
        pygame.time.delay(5000)
        font = pygame.font.SysFont("FiraCode", 30)
        space = font.size(" ")[0]
        final_collection = [word.split(" ") for word in final_text.splitlines()]
        pos = (200, 250)
        word_height = None
        x, y = pos
        for lines in final_collection:

            for words in lines:

                word_surface = font.render(words, True, TEXT_CLOR)
                word_width, word_height = word_surface.get_size()

                if x + word_width >= HEIGHT:
                    x = pos[0]
                    y += word_height
                self.screen.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]
            y += word_height

    # if user want to play again after the end of game this function will do it
    def rest_game(self):
        self.brain = GameBrain()
        Game()

    # draw a line if user win in a round
    def draw_winner_status(self):
        player = self.brain.final_state()[1]["player"]
        if player is None:
            return
        color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
        ipos = self.brain.final_state()[1]["ipos"]
        fpos = self.brain.final_state()[1]["fpos"]
        pygame.draw.line(self.screen, color, ipos, fpos, 10)
        pygame.display.update()
        pygame.time.delay(3000)
