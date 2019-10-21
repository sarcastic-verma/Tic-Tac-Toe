import pygame
from pygame.locals import *
import os
import csv

dir = os.path.dirname(__file__)

pygame.init()

COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = (255,0,0)
FONT = pygame.font.Font(None, 32)

winWidth = 601
winHeight = 601
BACKGROUND_COLOR = (0, 0, 255)
TEXT_COLOR = (255, 255, 0)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class CSV:
    def __init__(self):
        self.filename = dir+'\\database.csv'
        self.fieldnames = ['S No', 'Name', 'Score']
        self.names = []
        self.scores=[]
        self.no_of_lines = 0

        if not os.path.exists(self.filename) or os.path.getsize(self.filename)==0:
            with open(self.filename, 'w',newline='') as csvFile:
                wr = csv.writer(csvFile)
                wr.writerow(self.fieldnames)

    def appendToDatabase(self, row):
        with open(self.filename, 'a',newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)

    def getFieldNames(self):
        return self.fieldnames
    
    def getNames(self):
        self.names=[]
        with open(self.filename, 'r',newline='') as csvFile:
            csv_reader=csv.reader(csvFile)
            next(csvFile)
            for line in csv_reader:
                if not len(line)<3:
                    self.names.append(line[1].upper())
        return self.names

    def getScores(self):
        self.scores=[]
        with open(self.filename, 'r',newline='') as csvFile:
            csv_reader=csv.reader(csvFile)
            next(csvFile)
            for line in csv_reader:
                if not len(line)<3:
                    self.scores.append(line[2])
        return self.scores

    def updateScore(self, name):
        file_data=[]
        with open(self.filename, 'r',newline='') as csvFile:
            csvFile.seek(0,0)
            csv_reader=csv.reader(csvFile)
            file_data=list(csv_reader)
            with open(self.filename, 'w',newline='') as File:
                for x in range(0,len(file_data)):
                    if name.lower()==file_data[x][1].lower():
                        self.appendToDatabase([file_data[x][0],file_data[x][1],str(1+int(file_data[x][2]))])
                    else:
                        self.appendToDatabase(file_data[x])

    def getLines(self):
        self.no_of_lines=0
        with open(self.filename, 'r',newline='') as csvFile:
            next(csvFile)
            for line in csvFile:
                if not len(line.split(",")) < 3:
                    self.no_of_lines += 1
        return self.no_of_lines

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

def openLeaderboard():
    fieldnames=database.getFieldNames()
    names=database.getNames()
    scores=database.getScores()
    fields=''
    Y=0

    win.fill((0,0,255))

    display_text("LEADERBOARDS",(winWidth*0.18,winHeight*0.05),50,color=(255,0,0))

    if len(names)==0:
        display_text("NO DATA",(winWidth*0.4,winHeight*0.4))
    else:
        Y=winHeight*0.2
        # display fieldnames
        for f in fieldnames:
            if f=='Name':
                fields+=f"|    {f}         "
            else:
                fields+=f"|  {f}  "
        fields+="|"

        display_text("-"*43,(winWidth*0.12,Y))

        Y+=winHeight*0.05
        display_text(fields,(winWidth*0.12,Y))

        Y+=winHeight*0.05

        display_text("-"*43,(winWidth*0.12,Y))

        Y+=winHeight*0.05
        
        for x in range(0,len(names)):
            display_text(f"|   {x+1}.",(winWidth*0.12,Y))
            display_text(f" |   {names[x]}",(winWidth*0.3,Y))
            display_text(f" |   {scores[x]}",(winWidth*0.65,Y))
            display_text(f"  |",(winWidth*0.85,Y))
            Y+=50
        Y-=50
        Y+=winHeight*0.05
        display_text("-"*43,(winWidth*0.12,Y))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_l):  # start game
                return
    


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
            elif event.type == KEYDOWN and event.key == K_l:  # start game
                openLeaderboard()
            else:
                win.fill(BACKGROUND_COLOR)
                display_text(
                    "TIC TAC TOE", (winWidth*0.15, winHeight*0.15), 60)
                display_text("'L' FOR LEADERBOARD",
                             (winWidth*0.3, winHeight*0.5))
                display_text("Press 'ENTER' to start",
                             (winWidth*0.05, winHeight*0.8), 50)
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

def getName():
    name1=''
    name2=''

    name1_entered=False
    name2_entered=False


    input_box1 = InputBox(200, 250, 140, 32)
    input_box2 = InputBox(200, 450, 140, 32)
    input_boxes = [input_box1, input_box2]

    pygame.mouse.set_visible(True)
    while True:
        win.fill(BACKGROUND_COLOR)
        display_text("Enter Name X and hit 'ENTER'",(90,150))
        display_text("X : ",(150,250))
        
        display_text("Enter Name O and hit 'ENTER'",(90,350))
        display_text("O : ",(150,450))
        display_text("ENTER NAMES",(winWidth*0.1,winHeight*0.07),70,color=COLOR_ACTIVE)
        for box in input_boxes:
            box.draw(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if not name1_entered:
                name1=input_box1.handle_event(event)
            if name1!=None:
                name1_entered=True
            
            if not name2_entered:
                name2=input_box2.handle_event(event)
            if name2!=None:
                name2_entered=True
    
            if name1!=None and name2!=None:
                return name1,name2
        for box in input_boxes:
            box.update()

        pygame.display.update()
        
def mainGame(database,nameX,nameO):
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

            if winner=='x':
                if nameX.upper() in database.getNames():
                    database.updateScore(nameX)
                else:
                    database.appendToDatabase([database.getLines()+1,nameX,1])
            if winner=='o':
                if nameO.upper() in database.getNames():
                    database.updateScore(nameO)
                else:
                    database.appendToDatabase([database.getLines()+1,nameO,1])


            pygame.time.delay(500)
            if winner=='x':
                return winner,nameX
            if winner=='o':
                return winner,nameO
            

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


def gameOver(winner,name):
    """displays the win screen

    Args:
        winner (string): contains 'x' or 'o' or 'draw'
    """

    while True:
        win.fill(BACKGROUND_COLOR)
        display_text("TIC TAC TOE", (winWidth*0.2, winHeight*0.1), 50)
        if winner != 'draw':
            win.blit(IMAGES[winner], (winWidth*0.2, winHeight*0.4-20))
            display_text("WINS", (winWidth*0.45, winHeight*0.4), 50)
            display_text(f"[{name}]", (winWidth*0.35, winHeight*0.6), 50)
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

    get_name=True

    win = pygame.display.set_mode((winWidth, winHeight))
    pygame.display.set_caption("Tic Tac Toe")

    image_size = 120
    names=[]
    name=''

    IMAGES = {
        'board': pygame.image.load(dir+"\\images\\background.png").convert_alpha(),
        'o': pygame.transform.scale(pygame.image.load(dir+"\\images\\o.png").convert_alpha(), (image_size, image_size)),
        'x': pygame.transform.scale(pygame.image.load(dir+"\\images\\x.png").convert_alpha(), (image_size, image_size))
    }

    database=CSV()

    while True:
        welcomeScreen()
        if get_name: 
            names=getName()
            get_name=False
        winner,name = mainGame(database,names[0],names[1])
        gameOver(winner,name)
