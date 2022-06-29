import pygame
from network import Network

WIDTH = 600
HEIGHT = 650
WIN_SIZE = HEIGHT
CELL_SIZE = 200
win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("TicTacToe")
pygame.font.init()

picture_x = pygame.image.load("X.jpg")
picture_x = pygame.transform.scale(picture_x, (CELL_SIZE, CELL_SIZE))

picture_o = pygame.image.load("O.jpg")
picture_o = pygame.transform.scale(picture_o, (CELL_SIZE, CELL_SIZE))


def redraw_window(win, game, p):
    win.fill((255, 255, 255))
    font = pygame.font.Font(None, 20)

    reset_button = pygame.draw.rect(win, (128, 128, 128), (0, 0, 600, 50))

    reset_font = font.render(f"RESET", True, (0, 0, 0))
    reset_font_rect = reset_font.get_rect(center=(reset_button.centerx, reset_button.centery))
    win.blit(reset_font, reset_font_rect)

    for row_index, row in enumerate(game.board):
        for cell_index, cell in enumerate(row):
            if cell == "X":
                win.blit(picture_x, (CELL_SIZE*row_index, CELL_SIZE*cell_index+50))
            elif cell == "O":
                win.blit(picture_o, (CELL_SIZE*row_index, CELL_SIZE*cell_index+50))
            else:
                pygame.draw.rect(win, (255, 255, 255), (CELL_SIZE*row_index, CELL_SIZE*cell_index+50, 200, 200))

    for row_lines in range(3):
        for column_lines in range(3):
            pygame.draw.line(win, (0, 0, 0), (row_lines * CELL_SIZE, 50), (row_lines * CELL_SIZE, WIN_SIZE), 3)
            pygame.draw.line(win, (0, 0, 0), (0, column_lines * CELL_SIZE+50), (WIN_SIZE, column_lines * CELL_SIZE+50), 3)

    if not(game.connected()):
        font = pygame.font.SysFont("arial", 40)
        text = font.render("Waiting for Player...", True, (0, 0, 0))
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

    if game.winner == 2:
        font = pygame.font.SysFont("arial", 40)
        text = font.render("Tie Game!", True, (255, 0, 0))
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    elif game.winner == p:
        font = pygame.font.SysFont("arial", 40)
        text = font.render("You win!", True, (255, 0, 0))
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    elif game.winner != -1:
        font = pygame.font.SysFont("arial", 40)
        text = font.render("You lose...", True, (255, 0, 0))
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    network = Network()
    player = int(network.get_player_id())
    print("You are player: ", player)

    while run:
        clock.tick(60)
        try:
            game = network.send("get_board")
        except:
            run = False
            print("Couldn't get game")
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] >= 50:
                    row = pos[0]//CELL_SIZE
                    column = (pos[1]-50)//CELL_SIZE

                    if game.check_move(player) and not game.game_finished:
                        if player == 0:
                            data = f"{row}|{column}|X"

                        else:
                            data = f"{row}|{column}|O"
                        network.send(data)
                else:
                    network.send("reset")

        redraw_window(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((255, 255, 255))
        font = pygame.font.SysFont("arial", 40)
        text = font.render("Click to Play!", True, (0, 0, 0))
        win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    main()


while True:
    menu_screen()
