import pygame
import os
import time

# Initialize pygame
pygame.init()

# Title and Icon
pygame.display.set_caption("Line Scan Camera")

# image variables:
imgSpeed = 30           # pixels per second
dir = os.getcwd()
img = pygame.image.load(dir + '\images\Gear.png')
imgWidth = img.get_width()
imgHeight = img.get_height()
imgPos = [0, 0]
imgMovingTime = 0

# Create the screen
screenX = imgWidth * 2
screenY = imgHeight * 2
screen = pygame.display.set_mode((screenX, screenY))

# background
screen.fill((100, 100, 100))

# Time stuff
prev_time = time.time()
FPS = 60
clock = pygame.time.Clock()
passedTimeMoving = 0

# Line scan camera variables:
cameraSpeed = 30                # rows per second
doGuiding = False               # Guiding-test, but didn't use in the end. set to True to see test.
cameraPos = [0, 0]
cameraWidth = imgWidth
cameraHeight = imgHeight
cameraRect = [cameraPos[0], cameraPos[1], cameraWidth, cameraHeight]
cameraColour = (255, 0, 0)
cameraMovingTime = 0
cameraRow = cameraPos[1]
scanning = True

# For recording purposes:
time.sleep(1)


def move_img():
    # This function moves the image from top to bottom and stops moving when the image reached the bottom
    global imgMovingTime

    imgMovingTime += dt

    if imgMovingTime >= 1/imgSpeed and imgPos[1] < imgHeight:
        imgMovingTime = 0
        imgPos[1] += 1
    screen.blit(img, imgPos)


def capture_area():
    # This function captures an image of a line, just like a line scan camera would.
    global cameraMovingTime
    global cameraRow

    cameraMovingTime += dt

    if doGuiding:
        # Bug-fix for guiding lines
        pygame.draw.line(screen, (100, 100, 100), (imgWidth, imgHeight), (imgPos[0] + 2 * imgWidth, cameraRow), 3)

    if cameraMovingTime >= 1/cameraSpeed and cameraRow < imgHeight:
        cameraMovingTime = 0

        # copy row of pixels
        from_area = pygame.Rect(cameraPos[0], imgHeight, cameraWidth, 1)
        # Paste row
        screen.blit(screen, (imgPos[0] + imgWidth, cameraRow), from_area)
        # move the camera row
        cameraRow += 1

    # Draw a line where the camera took the picture
    pygame.draw.line(screen, (0, 200, 0), (cameraPos[0] + 1, imgHeight), (cameraPos[0] + imgWidth - 1, imgHeight), 3)

    if doGuiding:
        # Draw guiding lines to show where line of pixels is going
        pygame.draw.line(screen, (200, 0, 0), (cameraPos[0], imgHeight), (imgPos[0] + imgWidth, cameraRow), 3)
        pygame.draw.line(screen, (200, 0, 0), (imgWidth, imgHeight), (imgPos[0] + 2*imgWidth, cameraRow), 3)


# main loop
running = True
while running:

    # fill what the image left behind
    pygame.draw.rect(screen, (100, 100, 100), (0, 0, imgWidth, imgPos[1]))

    # determine time between frames
    now = time.time()
    dt = now - prev_time
    prev_time = now

    if imgSpeed == 0:
        # Put a static image on screen:
        screen.blit(img, imgPos)
    else:
        # move the image downwards on screen:
        move_img()

    # area scan camera:
    capture_area()

    # This forloop loops through all the events, like keyboard-presses, clicks, quit-button-press, etc.
    for event in pygame.event.get():

        # quit game if you press x in right top corner
        if event.type == pygame.QUIT:
            running = False

    # Update the display, so we see what's happening
    pygame.display.update()
