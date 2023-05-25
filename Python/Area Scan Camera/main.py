import pygame
import os
import time

# Initialize pygame
pygame.init()

# image:
imgSpeed = 0    # pixels per second
dir = os.getcwd()
img = pygame.image.load(dir + '\images\Tree.png')
imgWidth = img.get_width()
imgHeight = img.get_height()
imgPos = [0, 0]
imgMovingTime = 0

# Create the screen
screenX = imgWidth * 2
screenY = imgHeight * 2
screen = pygame.display.set_mode((screenX, screenY))

# Title and Icon
pygame.display.set_caption("Area Scan Camera")

# background
screen.fill((100, 100, 100))

# Time stuff
prev_time = time.time()
FPS = 60
clock = pygame.time.Clock()
passedTimeMoving = 0

# area scan camera:
cameraSpeed = 50      # rows per second
cameraPos = [0, 0]
cameraWidth = imgWidth
cameraHeight = imgHeight
cameraRect = [cameraPos[0], cameraPos[1], cameraWidth, cameraHeight]
cameraColour = (255, 0, 0)
cameraMovingTime = 0
cameraRow = cameraPos[1]
scanning = True


def move_img():
    global imgMovingTime

    imgMovingTime += dt

    if imgMovingTime >= 1/imgSpeed and imgPos[1] < imgHeight:
        imgMovingTime = 0
        imgPos[1] += 1
    screen.blit(img, imgPos)


def capture_area():
    global cameraMovingTime
    global cameraRow

    cameraMovingTime += dt

    # Draw rectangle to visualize the camera size
    # pygame.draw.rect(screen, cameraColour, cameraRect, 1)

    if cameraMovingTime >= 1/cameraSpeed and cameraRow < imgHeight:
        cameraMovingTime = 0

        # copy row of pixels
        from_area = pygame.Rect(cameraPos[0], cameraRow, cameraWidth, 1)
        # Paste row
        screen.blit(screen, (imgPos[0] + imgWidth, cameraRow), from_area)
        # move the camera row
        cameraRow += 1

    # Draw a line where the camera took the picture
    pygame.draw.line(screen, (0, 200, 0), (cameraPos[0] + 1, cameraRow), (cameraPos[0] + imgWidth - 1, cameraRow), 3)


# For recording purposes:
time.sleep(1)

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
