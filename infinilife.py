# Instead of using an array to kepp the data for all cells
# (which means that the board is limited  to positive integers only)
# we will keep a list of all LIVE cells, labelled by
# their tuple coords. (x, y)

# We can then draw any area of the infiboard we like

# CONTROLS

# MOUSE
# SCROLLWHEEL - zoom +/-
# RMB & drag - pan
# LMB - kill/create cell

# KEYBOARD
# - - zoom out
# = - zoom in
# ARROW KEYS - pan
# PGUP/PGDN - +/- running framerate

# FUNCTION
# SPACEBAR - pause/play
# RETURN - step
# h - hide hud
# r - reset
# q - quit

import pygame
import math

# "THE ACORN"
livecells = [(0, 0), (1, 0), (1, -2), (3, -1), (4, 0), (5, 0), (6, 0)]

# BLANK
# livecells = []

# CUSTOMISE #

# framerate when auto-genning
framerate = 10

# pixel width of square screen
screensize = 800

# number of cells shown in width
viewsize = 20

# pixel padding between each cell
cellpadding = 1

# cells to pan on button press
panspeed = 2

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 32)


# CALCULATED #

# cell coordiante to show in top left
viewtopleft = (round(0-viewsize/2), round(0-viewsize/2))


def recalculate():
    global cellsize
    # pixel width of a cell
    cellsize = ((screensize - cellpadding) / viewsize) - cellpadding
    global cellroundedness
    # pixel roundedness of each cell
    cellroundedness = math.floor(cellsize / 6)


recalculate()

win = pygame.display.set_mode((screensize, screensize))
pygame.display.set_caption("Conway's Game of Life")

# Stuff it, let's just use globals


def draw():
    if running or viewsize > 50:
        win.fill((0, 0, 0))
        for (x, y) in livecells:
            pygame.draw.rect(win, (255, 255, 255), ((x-viewtopleft[0])*(cellsize+cellpadding)+cellpadding, (y-viewtopleft[1])
                                                    * (cellsize+cellpadding)+cellpadding, cellsize, cellsize), border_radius=cellroundedness)
    else:
        win.fill((63, 63, 63))
        for x in range(viewtopleft[0], viewtopleft[0] + viewsize):
            for y in range(viewtopleft[1], viewtopleft[1] + viewsize):
                if (x, y) in livecells:
                    colour = (255, 255, 255)
                else:
                    colour = (0, 0, 0)
                pygame.draw.rect(win, colour, ((x-viewtopleft[0])*(cellsize+cellpadding)+cellpadding, (y-viewtopleft[1])
                                               * (cellsize+cellpadding)+cellpadding, cellsize, cellsize), border_radius=cellroundedness)


def clicked():
    mp = pygame.mouse.get_pos()
    cellpos = (math.floor(mp[0] / (cellsize+cellpadding)) + viewtopleft[0], math.floor(mp[1] / (cellsize+cellpadding) + viewtopleft[1]))
    global livecells
    if cellpos in livecells:
        livecells.remove(cellpos)
    else:
        livecells.append(cellpos)


def getneighbours(coords):
    return [(coords[0], coords[1]+1), (coords[0]+1, coords[1]+1), (coords[0]+1, coords[1]), (coords[0]+1,
                                                                                             coords[1]-1), (coords[0], coords[1]-1), (coords[0]-1, coords[1]-1), (coords[0]-1, coords[1]), (coords[0]-1, coords[1]+1)]


def checkcell(coords, newlivecells):
    neighbours = getneighbours(coords)
    neighbourcount = 0
    for i in neighbours:
        if i in livecells:
            neighbourcount += 1

    if coords in livecells and (neighbourcount > 3 or neighbourcount < 2):
        # DIE
        newlivecells.remove(coords)

        return newlivecells
    elif not (coords in livecells) and neighbourcount == 3:
        # BIRTH
        newlivecells.append(coords)

        return newlivecells
    else:
        # SURVIVE
        return newlivecells


def step():
    global livecells
    newlivecells = livecells.copy()
    alreadychecked = []
    # To ensure no cells that could possibly be important are missed we will
    # check every cell around every live cell. (Ignoring ones we have already checked)

    for cell in livecells:
        if not cell in alreadychecked:
            newlivecells = checkcell(cell, newlivecells)
            alreadychecked.append(cell)
        for i in getneighbours(cell):
            if not i in alreadychecked:
                alreadychecked.append(i)
                newlivecells = checkcell(i, newlivecells)
    livecells = newlivecells.copy()


clock = pygame.time.Clock()

playing = True
running = False
hud = True
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
                livecells = []
                gen = 0
            if event.key == pygame.K_SPACE:
                running = not running
                if running:
                    gensincestop = 0
            if event.key == pygame.K_RETURN:
                gen += 1
                step()

            if event.key == pygame.K_RIGHT:
                viewtopleft = (viewtopleft[0] + panspeed, viewtopleft[1])
            if event.key == pygame.K_LEFT:
                viewtopleft = (viewtopleft[0] - panspeed, viewtopleft[1])
            if event.key == pygame.K_UP:
                viewtopleft = (viewtopleft[0], viewtopleft[1] - panspeed)
            if event.key == pygame.K_DOWN:
                viewtopleft = (viewtopleft[0], viewtopleft[1] + panspeed)

            if event.key == pygame.K_MINUS:
                viewsize += 2
                viewtopleft = (viewtopleft[0] - 1, viewtopleft[1] - 1)
                recalculate()
            if event.key == pygame.K_EQUALS:
                if viewsize > 8:
                    viewsize -= 2
                    viewtopleft = (viewtopleft[0] + 1, viewtopleft[1] + 1)
                    recalculate()

            if event.key == pygame.K_PAGEUP:
                framerate += 1
            if event.key == pygame.K_PAGEDOWN:
                framerate = max(1, framerate - 1)

            if event.key == pygame.K_h:
                hud = not hud
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0 and viewsize > 8:
                viewsize -= event.y * 2
                viewtopleft = (viewtopleft[0] + event.y, viewtopleft[1] + event.y)
                recalculate()
            elif event.y < 0:
                viewsize -= event.y * 2
                viewtopleft = (viewtopleft[0] + event.y, viewtopleft[1] + event.y)
                recalculate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked()
            if event.button == 3:
                startingmmousepos = pygame.mouse.get_pos()
                startingview = viewtopleft
    if pygame.mouse.get_pressed(num_buttons=3)[2]:
        mp = pygame.mouse.get_pos()
        viewtopleft = (startingview[0] - math.floor((mp[0]-startingmmousepos[0]) / (cellsize+cellpadding)), startingview[1] - math.floor((mp[1]-startingmmousepos[1]) / (cellsize+cellpadding)))
    if running:
        step()
        gen += 1
        gensincestop += 1
        clock.tick(framerate)
    draw()
    if hud:
        text = font.render(str(gen), True, (231, 234, 58))
        textRect = text.get_rect()
        textRect.topleft = (2, 2)
        win.blit(text, textRect)
        text = font.render(str(gensincestop), True, (82, 234, 79))
        textRect = text.get_rect()
        textRect.topright = (win.get_width() - 2, 2)
        win.blit(text, textRect)
        text = font.render(str((round(viewtopleft[0] + viewsize/2), round(viewtopleft[1] + viewsize/2))), True, (31, 207, 226))
        textRect = text.get_rect()
        textRect.bottomleft = (2, screensize - 2)
        win.blit(text, textRect)
        text = font.render("FPS:" + str(framerate), True, (31, 207, 226))
        textRect = text.get_rect()
        textRect.bottomright = (screensize - 2, screensize - 2)
        win.blit(text, textRect)
        text = font.render("SCALE:" + str(viewsize), True, (31, 207, 226))
        textRect = text.get_rect()
        textRect.bottomright = (screensize - 2, screensize - 40)
        win.blit(text, textRect)
    pygame.display.flip()
