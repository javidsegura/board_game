# To do: 
    # - add fields to tweak parameters
    # - add money counter
    # - add multipliers
    # - present data on screen
    # - make it look good
    # - finish game loop -> if you hit a bomb get a message and then prompted to play again
    # - store user data
    # - probably room for more efficient coding

import pygame
import pygame_gui

pygame.init()
pygame.display.set_caption("Mines")

# CONSTANTS
size = (700, 500)
numSquares = 25
squareSize = 100
squareColor = "gold"
borderSize = 2
bombs = [[False for _ in range(5)] for _ in range(5)]
bombs[0][1] = True
freeze = False

passedSquares = [] #where we input the x,y tuple of green squares




# size is temp for now it should become dynamic; idea is that the control bar (left side) is about half the width and height of the main box
# IMPORTANT: width needs to be multiple of squareSize for coords to work

#instead of doing pygame.FULLSCREEN:
    # info = pygame.display.Info()
    # width = info.current_w
    # height = info.current_h 
    # print(f"Width: {width}, Height: {height}")

screen = pygame.display.set_mode(size)
# add pygame.FULLSCREEN ^                                 
background = pygame.Surface(size)
background.fill(pygame.Color('#FFFFFF'))
manager = pygame_gui.UIManager(size) #not sure purpose of manager but this guy uses it for gui


# def initializeBombs():


def drawBoard():
    # pygame.draw.rect(screen, )
    for i in range(numSquares):
        column = i % 5
        row = i // 5

        squareX = column*squareSize
        squareY = row * squareSize

        pygame.draw.rect(screen, "black", [200 +  squareX, squareY, squareSize, squareSize])
        pygame.draw.rect(screen, "gold", [200 + squareX + borderSize, squareY + borderSize, squareSize - 2 * borderSize, squareSize - 2 * borderSize])

def updateSquare(click) -> bool:
    drawBoard()

    squareX = click[0] * squareSize
    squareY = click[1] * squareSize

    if bombs[click[0]] [click[1]]:
        pygame.draw.rect(screen, "red", [200 + squareX + borderSize, squareY + borderSize, squareSize -2 * borderSize, squareSize - 2 * borderSize])
        pygame.display.flip() # color change not working
        freeze = True

        print(" Bomb hit")
    else:
        # pygame.draw.rect(screen, "green", [200 + squareX + borderSize, squareY + borderSize, squareSize -2 * borderSize, squareSize - 2 * borderSize])
        # pygame.display.flip() # color change not working
        freeze = False
        passedSquares.append(click)

        print(passedSquares)

    for safeSquare in passedSquares:
        safeSquareX = safeSquare[0] * squareSize
        safeSquareY = safeSquare[1] * squareSize

        pygame.draw.rect(screen, "green", [200 + safeSquareX + borderSize, safeSquareY + borderSize, squareSize -2 * borderSize, squareSize - 2 * borderSize])
        pygame.display.flip() # color change not working

    
    return freeze



clock = pygame.time.Clock()
run = True

screen.blit(background, (0, 0))
drawBoard()

while run:
    time = clock.tick(60) / 1000 #60 fps and time is the number of milliseconds spent per instance of while loop

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("\nQuitting...")
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.pos[0]//100 > 1 and not freeze:
            print(f"Debug: {event.pos[0]//100}")
            x = (200 + event.pos[0]) // 100 - 4
            y = event.pos[1] // 100
            click = (x, y)
            print(f"X: {click[0]}, Y: {click[1]}")
            if updateSquare(click):
                freeze = True
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                print("Quitting...")
                run = False
        manager.process_events(event)
    manager.update(time)

    if not freeze:
        manager.draw_ui(screen)
        pygame.display.flip()