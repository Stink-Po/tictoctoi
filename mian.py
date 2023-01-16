import sys
from ui import Game
import pygame

# pygame Setup
pygame.init()


def main():
    final = False
    # a variable  that check if we are in the welcome screen or not
    welcome = True
    # a variable check if we are in the end of a round or not
    end_round = False
    # init a game class it's showing the ui and controls all the other class (AI and GameBrain)
    game = Game()
    while True:

        if game.brain.running:

            if welcome:
                # showing welcome screen and ask user to choose the game mode
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_g:
                            game.brain.game_mode = "ai"
                            game.draw_lines()
                            welcome = False
                        elif event.key == pygame.K_p:
                            game.brain.game_mode = "pvp"
                            game.draw_lines()
                            welcome = False
                        elif event.key == pygame.K_n:
                            game.brain.ai.level = 0
                            game.brain.game_mode = "ai"
                            game.draw_lines()
                            welcome = False

            if not end_round:

                if not welcome:
                    # clear the screen from welcome text and draw a game board and waiting for
                    # user to click and fill the board with user choose also check iof game is over or not
                    for event in pygame.event.get():

                        if game.brain.is_full():
                            end_round = True
                        if game.brain.final_state()[0] != 0:
                            end_round = True
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            game.check_click(event)
                            pygame.display.update()

                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

        if end_round and not final:
            # showing the winner or Draw if draw and after a while showing a users current scores
            pygame.display.update()
            if game.brain.final_state()[0] != 0:
                game.draw_winner_status()
            pygame.display.update()
            game.draw_score()
            pygame.display.update()
            if not game.brain.check_final():

                if game.brain.player == 2:
                    game.ai_turn()
                    pygame.display.update()

            end_round = False
        if game.brain.check_final():
            # if any of users reach the 5 score in game there is a winner, and we show the winner
            final = True
            game.draw_final_score()
            for event in pygame.event.get():
                # after showing winner  asking from user want to play again or quit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        end_round = False
                        final = False
                        welcome = True
                        game.rest_game()
                        print(game.brain.running)
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


if __name__ == '__main__':
    main()
