import pygame
from pygame.locals import *
import os

dir = os.path.dirname(__file__)


winWidth = 601
winHeight = 601
BACKGROUND_COLOR = (0, 0, 255)
TEXT_COLOR = (255, 255, 0)


def display_text(text, pos, size=30, color=TEXT_COLOR):
    """displays text on the screen

    Args:
        text (string): text to displat
        pos (tuple): pos of text to display
        size (int, optional): size of font. Defaults to 30.
        color (tuple, optional): color of font. Defaults to TEXT_COLOR.

    Returns:
        None
    """
    myFont = pygame.font.SysFont('Comic Sans MS', size)
    textsurface = myFont.render(text, False, color)
    win.blit(textsurface, (pos[0], pos[1]))


def welcomeScreen():
    """displays welcome screen on the screen
    """

    # making the mouse invisible
    pygame.mouse.set_visible(False)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_RETURN:  # start game
                return
            else:
                win.fill(BACKGROUND_COLOR)
                display_text(
                    "TIC TAC TOE", (winWidth*0.15, winHeight*0.15), 60)
                display_text("Press 'ENTER' to start",
                             (winWidth*0.05, winHeight*0.5), 50)
                pygame.display.update()


def redrawGameWindow(blitting_positions, image, winner_declared):
    """function used to blit elements on the screen

    Args:
        blitting_positions (list): data
    """

    # blitting board on the screen
    win.blit(IMAGES['board'], (0, 0))

    if not winner_declared:
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]

        X = mouseX-IMAGES[image].get_width()//2
        Y = mouseY-IMAGES[image].get_height()//2
        win.blit(IMAGES[image], (X, Y))

    # blitting cross or circles
    for i in range(0, len(blitting_positions)):
        if blitting_positions[i][1] != '':
            win.blit(IMAGES[blitting_positions[i][1]],
                     (blitting_positions[i][2][0], blitting_positions[i][2][1]))

    pygame.display.update()


def getWinner(blitting_positions):
    """function used to check the winner

    Args:
        blitting_positions (list): data

    Returns:
        'x': if X is winner
        'o': if O is winner
        'draw': if it is draw
         None: if no winner
    """

    combo_X = []
    combo_O = []
    winX = False
    winO = False
    draw_possible = True
    win_combos = [
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        (1, 4, 7),
        (2, 5, 8),
        (3, 6, 9),
        (1, 5, 9),
        (3, 5, 7)
    ]

    for i in range(0, len(blitting_positions)):
        if blitting_positions[i][3] == 0:
            if blitting_positions[i][1] == 'x':
                combo_X.append(blitting_positions[i][0])
            elif blitting_positions[i][1] == 'o':
                combo_O.append(blitting_positions[i][0])

    # checking whether X is the winner
    for i in range(0, len(win_combos)):
        if all(elem in combo_X for elem in win_combos[i]):
            winX = True
            break

    if winX:
        return 'x'

    # checking whether O is the winner
    for i in range(0, len(win_combos)):
        if all(elem in combo_O for elem in win_combos[i]):
            winO = True
            break

    if winO:
        return 'o'

    for i in range(0, len(blitting_positions)):
        # if all buttons are pressed and still no one wins , its a draw
        if blitting_positions[i][3] == 0:
            pass
        else:
            draw_possible = False
            break

    # if neither X wins nor O wins ... checking for draw
    if draw_possible:
        if winX == False and winO == False:
            return 'draw'

    return None


def mainGame():
    """main game function
    """

    # blitting_positions= [ number , image , [X , Y] , pos_active ]
    blitting_positions = []
    image = 'x'
    winner = ''

    winner_found = False

    # adding number of block , cross or circle ,[ pos X , pos Y], position active to blitting_positions
    for i in range(0, 9):
        blitting_positions.append([i+1, '', [], 1])

    # adding X and Y values to blitting_positions

    blitting_positions[0][2] = [50, 50]
    blitting_positions[1][2] = [240, 50]
    blitting_positions[2][2] = [430, 50]
    blitting_positions[3][2] = [50, 240]
    blitting_positions[4][2] = [240, 240]
    blitting_positions[5][2] = [430, 240]
    blitting_positions[6][2] = [50, 430]
    blitting_positions[7][2] = [240, 430]
    blitting_positions[8][2] = [430, 430]

    while True:
        redrawGameWindow(blitting_positions, image, winner_found)

        if winner_found:
            pygame.time.delay(500)
            return winner

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]
                width_image = IMAGES['x'].get_width()

                for i in range(0, len(blitting_positions)):
                    if blitting_positions[i][3] == 1:    # button is active
                        X = blitting_positions[i][2][0]
                        Y = blitting_positions[i][2][1]
                        if X+width_image+30 > mouseX > X-30 and Y+width_image+30 > mouseY > Y-30:
                            blitting_positions[i][1] = image
                            # making button inactive
                            blitting_positions[i][3] = 0

                            if image == 'x':
                                image = 'o'
                            elif image == 'o':
                                image = 'x'

                winner = getWinner(blitting_positions)
                if winner != None:
                    winner_found = True


def gameOver(winner):
    """displays the win screen

    Args:
        winner (string): contains 'x' or 'o' or 'draw'
    """

    while True:
        win.fill(BACKGROUND_COLOR)
        display_text("TIC TAC TOE", (winWidth*0.2, winHeight*0.2), 50)
        if winner != 'draw':
            win.blit(IMAGES[winner], (winWidth*0.2, winHeight*0.5-20))
            display_text("WINS", (winWidth*0.45, winHeight*0.5), 50)
        else:
            display_text("DRAW", (winWidth*0.35, winHeight*0.5), 50)

        display_text("Press 'R' to restart",
                     (winWidth*0.65, winHeight*0.92), 20)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_r:  # restart game
                return


if __name__ == "__main__":
    pygame.init()

    win = pygame.display.set_mode((winWidth, winHeight))
    pygame.display.set_caption("Tic Tac Toe")

    image_size = 120

    IMAGES = {
        'board': pygame.image.load(dir+"\\images\\background.png").convert_alpha(),
        'o': pygame.transform.scale(pygame.image.load(dir+"\\images\\o.png").convert_alpha(), (image_size, image_size)),
        'x': pygame.transform.scale(pygame.image.load(dir+"\\images\\x.png").convert_alpha(), (image_size, image_size))
    }

    while True:
        welcomeScreen()
        winner = mainGame()
        gameOver(winner)
