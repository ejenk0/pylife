import numpy as np
import pygame
import math

boardsize = 20
cellsize = math.floor(900/boardsize)
# cellpadd = math.floor(cellsize/10)
cellpadd = 1
# cellrounding = math.floor(cellsize/5)
cellrounding = 0
board = np.array([[0]*boardsize]*boardsize)
framerate = 4

# GLIDER
board[1, 2], board[2, 2], board[3, 2], board[3, 1], board[2, 0] = 1, 1, 1, 1, 1

# BLINKER
# board[1, 2], board[2, 2], board[3, 2] = 1, 1, 1

pygame.init()
win = pygame.display.set_mode(((boardsize+1)*cellpadd + boardsize*cellsize, (boardsize+1)*cellpadd + boardsize*cellsize))
font = pygame.font.Font('freesansbold.ttf', 32)
clock = pygame.time.Clock()


def draw(board):
    win.fill((50, 50, 50))
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            pygame.draw.rect(win, (cell*255, cell*255, cell*255), ((r+1) * cellpadd + (r*cellsize), (c+1) * cellpadd + (c*cellsize), cellsize, cellsize), border_radius=cellrounding)


def step(board):
    newboard = np.array([[0]*boardsize]*boardsize)
    for r, row in enumerate(board):
        for c, cell in enumerate(row):
            neighbours = 0
            if c-1 >= 0:
                left = (r, c-1)
            else:
                left = (r, boardsize-1)

            if c+1 < boardsize:
                right = (r, c+1)
            else:
                right = (r, 0)

            if r-1 >= 0:
                up = (r-1, c)
            else:
                up = (boardsize-1, c)

            if r+1 < boardsize:
                down = (r+1, c)
            else:
                down = (0, c)

            for i in [left, right, up, down, (up[0], left[1]), (up[0], right[1]), (down[0], left[1]), (down[0], right[1])]:
                if board[i[0], i[1]]:
                    neighbours += 1

            # CONWAY'S RULES
                # Any live cell with two or three live neighbours survives.
                # Any dead cell with three live neighbours becomes a live cell.
                # All other live cells die in the next generation. Similarly, all other dead cells stay dead.

            # SURVIVAL
            if cell and (neighbours == 2 or neighbours == 3):
                newboard[r, c] = 1

            # DEATH
            elif cell and not (neighbours == 2 or neighbours == 3):
                newboard[r, c] = 0

            # BIRTH
            elif not cell and neighbours == 3:
                newboard[r, c] = 1
    return newboard


def clicked(board):
    mp = pygame.mouse.get_pos()
    cellpos = (math.floor(mp[0] / (cellsize+cellpadd)), math.floor(mp[1] / (cellsize+cellpadd)))
    board[cellpos[0], cellpos[1]] = not board[cellpos[0], cellpos[1]]
    return board


playing = True
running = False
gen = 0
gensincestop = 0
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                playing = False
            if event.key == pygame.K_r:
                board = np.array([[0]*boardsize]*boardsize)
                gen = 0
            if event.key == pygame.K_SPACE:
                running = not running
                if running:
                    gensincestop = 0
            if event.key == pygame.K_RETURN or event.key == pygame.K_RIGHT:
                gen += 1
                board = step(board)
            if event.key == pygame.K_UP:
                framerate += 1
            if event.key == pygame.K_DOWN:
                framerate -= 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            board = clicked(board)
    draw(board)
    text = font.render(str(gen), True, (231, 234, 58))
    textRect = text.get_rect()
    textRect.topleft = (2, 2)
    win.blit(text, textRect)
    text = font.render(str(gensincestop), True, (82, 234, 79))
    textRect = text.get_rect()
    textRect.topright = (win.get_width() - 2, 2)
    win.blit(text, textRect)
    pygame.display.flip()
    if running:
        board = step(board)
        gen += 1
        gensincestop += 1
        clock.tick(framerate)


pygame.quit()
quit()
