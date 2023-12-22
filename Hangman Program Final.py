#########################################################
## File Name: Hangman Program Final.py                               ##
## Description: Hangman Project - ICS3U    ##
#########################################################
import pygame
import random
pygame.init()
 
#---------------------------------------#
# initialize global variables/constants #
#---------------------------------------#
BLACK = (0,0, 0)
WHITE = (255,255,255)
RED   = (255,0, 0)
GREEN = (0,255,0)
BLUE  = (0,0,255)
LIGHT_BLUE = (102,255,255)

btn_font = pygame.font.SysFont("arial", 20)
guess_font = pygame.font.SysFont("monospace", 24)
clue_font = pygame.font.SysFont("monospace", 16)

catButtons = [[(56,200,160,80),'NHL Teams'],
              [(271,200,160,80),'Marvel Characters'],
              [(486,200,160,80),'Popular Movies']]
correctSound = pygame.mixer.Sound(r"C:\Users\willh\OneDrive\Desktop\Python Files\Hangman Program\Hangman Program\correct.mp3")
correctSound.set_volume(0.2)
wrongSound = pygame.mixer.Sound(r"C:\Users\willh\OneDrive\Desktop\Python Files\Hangman Program\Hangman Program\incorrect.mp3")
wrongSound.set_volume(0.2)

#---------------------------------------#
# function that returns button data     #
#---------------------------------------#
def createButtons():
    x = 98
    y = 400
    buttons = []
    for btn in range(26):
        buttons.append((x, y))
        x += 42
        if btn == 12:
            x = 98
            y += 42
    return buttons

#---------------------------------------#
# function that draws buttons           #
#---------------------------------------#
def drawButtons(buttons):
    for i,xy in enumerate(buttons):
        #circle(Surface, color, pos, radius, width=0) -> Rect
        if usedLetter[i] == i:
            pygame.draw.circle(win, WHITE, xy, 15, 0)
        else:
            pygame.draw.circle(win, LIGHT_BLUE, xy, 15, 0)
        pygame.draw.circle(win, BLACK, xy, 15, 1)
        ltrToRender = chr(i+65)
        #render(text, antialias, color, background=None) -> Surface
        ltrSurface = btn_font.render(ltrToRender, True, BLACK)
        win.blit(ltrSurface, (xy[0]-ltrSurface.get_width()//2, xy[1]-ltrSurface.get_height()//2))

#---------------------------------------------------#
# function that checks if a button has been pressed #
#---------------------------------------------------#
def clickBtn(mp, buttons):
    for i, xy in enumerate(buttons):
        a = mp[0] - xy[0]
        b = mp[1] - xy[1]
        c = (a**2 + b**2)**.5
        if c <= 15:
            return i
    return -1

#---------------------------------------#
# function that loads images            #
#---------------------------------------#
def loadHangmanImages():
    hmImages = []
    for imgNum in range(7):
        fileName = 'hangman' + str(imgNum) + '.png'
        hmImages.append(pygame.image.load(r"C:\Users\willh\OneDrive\Desktop\Python Files\Hangman Program\Hangman Program" + "\\" + fileName))
    return hmImages

#---------------------------------------#
# function that redraws all objects     #
#---------------------------------------#
def redraw_game_window():
    win.fill(GREEN)
    if windowNum == 1:
        drawCategoryButtons(catButtons)
    else:
        drawButtons(buttons)
        if oldWrongCount == wrongCount and oldWrongCount > 0 and oldWrongCount < 6:
            win.blit(hmHappyImages[wrongCount-1], (275,30))
        else:
            win.blit(hmImages[wrongCount], (275,30))

        drawGuess()
        if wrongCount == 6:
            win.blit(lostSurface, (100,100))
        if guess == puzzle:
            win.blit(wonSurface, (100,100))
    # code to draw things goes here
    pygame.display.update()

#---------------------------------------#
# function that import puzzles          #
#---------------------------------------#
def loadPuzzles():
    puzzles = [[], [], []]
    fi = open(r"C:\Users\willh\OneDrive\Desktop\Python Files\Hangman Program\Hangman Program\Hangman Answers.txt")
    for p in fi:
        nextP = p.strip().split(',')
        pIndex = int(nextP[0])-1
        puzzles[pIndex].append([nextP[1], nextP[2]])
    fi.close()
    return puzzles

#---------------------------------------#
# function that import happy images     #
#---------------------------------------#
def loadHappyHangmanImages():
    hmHappyImages = []
    for imgNum in range(5):
        fileName = 'hangman' + str(imgNum + 1) + '-happy.png'
        hmHappyImages.append(pygame.image.load(r"C:\Users\willh\OneDrive\Desktop\Python Files\Hangman Program\Hangman Program" + "\\" + fileName))
    return hmHappyImages

#---------------------------------------#
# function that chooses puzzle to play  #
#---------------------------------------#
def getRandomPuzzle(cat, puzzles):
    while True:
        rndIndex = random.randrange(0, 6)
        rndPuzzle = puzzles[cat][rndIndex]
        puzzles[cat][rndIndex] = ' '
        return rndPuzzle

#---------------------------------------#
# function that creates starting guess  #
#---------------------------------------#
def initializeGuess(puzzle):
    guess  = ''
    for c in puzzle:
        if c == ' ':
            guess += ' '
        else:
            guess += '_'
    return guess


#---------------------------------------#
# function draws the guess spaces       #
#---------------------------------------#
def spacedOut(guess):
    spacedGuess = ''
    for c in guess:
        spacedGuess += c
        spacedGuess += ' '
    return spacedGuess
    

#---------------------------------------#
# function draws the guess spaces       #
#---------------------------------------#
def drawGuess():
    guessSurface = guess_font.render(spacedOut(guess),True,BLACK)
    x = (win.get_width() - guessSurface.get_width())//2
    win.blit(guessSurface, (x, 270))
    clueSurface = clue_font.render(clue,True,BLACK)
    x = (win.get_width() - clueSurface.get_width())//2
    win.blit(clueSurface, (x,320))

#---------------------------------------#
# function that updates guess           #
#---------------------------------------#
def updateGuess(ltrGuess, guess, puzzle):
    newGuess = ''
    for i,ltr in enumerate(puzzle):
        if ltrGuess == ltr:
            newGuess += ltr
        else:
            newGuess += guess[i]
    return newGuess

#---------------------------------------#
# draws rectangular buttons             #
#---------------------------------------#
def drawCategoryButtons(catButtons):
    for b in catButtons:
        pygame.draw.rect(win,BLUE,b[0],0)
        pygame.draw.rect(win,RED,b[0],3)
        txtSurface = btn_font.render(b[1],True,WHITE)
        x = b[0][0] + (b[0][2] - txtSurface.get_width()) //2
        y = b[0][1] + (b[0][3] - txtSurface.get_height()) // 2
        win.blit(txtSurface,(x,y))

#---------------------------------------------------#
# function that checks if correct button was clicked   #
#---------------------------------------------------#
def catBtnClick(mp,buttons):
    for i,b in enumerate(buttons):
        if pygame.Rect(b[0]).collidepoint(mp):
            return i
    return -1

#---------------------------------------#
# the main program begins here          #
#---------------------------------------#
win = pygame.display.set_mode((700,480))
inPlay = True
buttons = createButtons()
hmImages = loadHangmanImages()
hmHappyImages = loadHappyHangmanImages()
wrongCount = 0
oldWrongCount = 0
windowNum = 1
wonSurface = guess_font.render("YOU WIN!",True,BLACK)
lostSurface = guess_font.render("YOU LOST!",True,BLACK)
roundCount = 1

while inPlay:
    redraw_game_window()                          # window must be constantly redrawn - animation
    if windowNum == 2:
        if wrongCount == 6 or guess == puzzle:
            pygame.time.delay(1000)
            windowNum = 1
    pygame.time.delay(10)                          # pause for 10 miliseconds
    if wrongCount == 6:
        wrongCount = 0
    
    for event in pygame.event.get():               # check for any events
        
        if windowNum == 2:                             # determines which window is being displayed
            guess = updateGuess(ltrGuess, guess, puzzle)      # makes sure that guess carries over
            if event.type == pygame.QUIT:              # if user clicks on the window's 'X' button
                inPlay = False                         # exit from the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    inPlay = False                     # exit from the game
            if event.type == pygame.MOUSEBUTTONDOWN:   # if user clicks anywhere on win
                clickPos = pygame.mouse.get_pos()
                pressedBtn = clickBtn(clickPos, buttons)
                if pressedBtn == -1:                   # checks to see which button has been pressed
                    pass
                else:
                    ltrGuess = chr(pressedBtn + 65)
                    oldWrongCount = wrongCount
                    if ltrGuess in puzzle:
                        correctSound.play()             # plays sound based off of if answer was correct 
                    else:
                        wrongSound.play()               # plays sound based off of if answer was incorrect
                        if wrongCount < 6:              # couunts how many wrong guesses to update the image             
                            wrongCount += 1
                            
                    usedLetter[pressedBtn] = pressedBtn
        else:                                           # opening window is beign displayed
            usedLetter = ['q','q','q','q','q','q','q','q','q','q','q','q','q','q','q','q','q','q','q','q','q','q','q','q','q','q','q'] # will make a list of every letter button that has been pressed
            wrongCount = 0                              # establishes the wrong guesses counter before each game
            oldWrongCount = 0                           # establishes the previous turns wrong counter for each turn to display happy images
            if event.type == pygame.MOUSEBUTTONDOWN:    # checks for event
                clickPos = pygame.mouse.get_pos()
                pressedButton = catBtnClick(clickPos,catButtons)
                if pressedButton > -1:                  # checks if a buttin has been pressed
                    windowNum += 1
                    while True:                         # continues to pick a puzzle until one hasn't been already played
                        if roundCount == 1:
                            puzzles = loadPuzzles()
                            roundCount += 1
                        randomPuz = getRandomPuzzle(pressedButton, puzzles)
                        puzzle = randomPuz[0]
                        if puzzle == ' ':
                            pass
                        else:
                            break
                    clue = randomPuz[1]                 # establishes the clue for the puzzle
                    guess = initializeGuess(puzzle)     # sets all of the letters to blank spaces in the puzzle
                    ltrGuess = ''
            if event.type == pygame.QUIT:              # if user clicks on the window's 'X' button
                inPlay = False                         # exit from the game
            if event.type == pygame.KEYDOWN:           # if user clicks the escape key
                if event.key == pygame.K_ESCAPE:       # exit from the game
                    inPlay = False

#---------------------------------------#                                        
pygame.quit()                           # always quit pygame when done!
