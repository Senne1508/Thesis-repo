import math

import pygame
import os
import time

# Initialize pygame
pygame.init()

# image:
imgSpeed = 200   # rotational unit per second
rotUnit = 0.5     # degrees
dir = os.getcwd()
img = pygame.image.load(dir + '\images\Rotor_4_blades_small.png')
img_copy = img
imgWidth = img.get_width()
imgHeight = img.get_height()

imgMovingTime = 0
imgAngle = 0

# Title and Icon
pygame.display.set_caption("Line scan camera")

# Time stuff
prev_time = time.time()
FPS = 60
clock = pygame.time.Clock()
passedTimeMoving = 0

# area scan camera:
cameraSpeed = 200      # rows per second
cameraPos = [0, 0]
cameraWidth = int(math.sqrt(imgWidth**2 + imgHeight **2))
cameraHeight = imgHeight*1.1
cameraRect = [cameraPos[0], cameraPos[1], cameraWidth, cameraHeight]
cameraColour = (255, 0, 0)
cameraMovingTime = 0
cameraRow = cameraPos[1]
scanning = True

# Create the screen
screenX = cameraWidth * 2
screenY = imgHeight*1.1
screen = pygame.display.set_mode((screenX, screenY))

imgPos = [screenX / 4, screenY / 2]

# background
screen.fill((100, 100, 100))

#for recording purposes:
time.sleep(1)


def move_img():
    global imgMovingTime
    global imgAngle
    global img
    global img_copy

    imgMovingTime += dt

    if imgMovingTime >= 1/imgSpeed:
        imgMovingTime = 0
        imgAngle += rotUnit
        img_copy = pygame.transform.rotate(img, imgAngle)
    screen.blit(img_copy, (imgPos[0] - int(img_copy.get_width() / 2), imgPos[1] - int(img_copy.get_height() / 2)))


def capture_area():
    global cameraMovingTime
    global cameraRow

    cameraMovingTime += dt

    # Draw rectangle to visualize the camera size
    pygame.draw.rect(screen, cameraColour, cameraRect, 1)

    if cameraMovingTime >= 1/cameraSpeed and cameraRow < cameraHeight:
        cameraMovingTime = 0

        # copy row of pixels
        from_area = pygame.Rect(cameraPos[0], cameraRow, cameraWidth, 1)
        # Paste row
        screen.blit(screen, (cameraWidth, cameraRow), from_area)
        # move the camera row
        cameraRow += 1

    # Draw a line where the camera took the picture
    pygame.draw.line(screen, (0, 200, 0), (cameraPos[0] + 1, cameraRow), (cameraPos[0] + cameraWidth - 1, cameraRow), 3)


# main loop
running = True
while running:

    # fill what the image left behind
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, cameraWidth, cameraHeight))

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
