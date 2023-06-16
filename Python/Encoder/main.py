import pygame
import time
import math

# Initialize pygame
pygame.init()

# Create the screen, width=800, height=600
screenX = 1400
screenY = 600
screen = pygame.display.set_mode((screenX, screenY))

# Time stuff
prev_time = time.time()
FPS = 60
clock = pygame.time.Clock()

# Title and Icon
pygame.display.set_caption("Encoder visualisation")

# variables
gearSpeed = 0.3
backColour = (100, 100, 100)
gearCenter = [int(screenX/4), int(screenY/2)]
gearRadius = int(screenY / 4)
gearColour = (0, 0, 0)
numTeeth = 16
numPies = numTeeth * 2
angleTeeth = 2 * math.pi / numPies
gearAngle = 0

laserColour1 = (255, 0, 0)
laserColour2 = (0, 255, 0)

graph1 = [0] * screenX
graph2 = [0] * screenX
graphFactor = screenY / 5

direction = "CW"
mousePressed = False


def pie_slice(center, r, angle, angle_width, colour):
    # This function draws a slice of a pie, which will be used to construct the gear
    point2 = [center[0] + r * math.cos(angle), center[1] + r * math.sin(angle)]
    point3 = [center[0] + r * math.cos(angle + angle_width), center[1] + r * math.sin(angle + angle_width)]
    pygame.draw.polygon(screen, colour, (center, point2, point3))


def draw_gear(angle_offset):
    # Using the pie_slice function, this function draws a gear.
    for i in range(numPies):
        if i % 2:
            pie_slice(gearCenter, gearRadius, i * angleTeeth + angle_offset, angleTeeth, gearColour)
        else:
            pie_slice(gearCenter, gearRadius, i * angleTeeth + angle_offset, angleTeeth, backColour)

    pygame.draw.circle(screen, gearColour, gearCenter, gearRadius * (7 / 8))


def move_gear():
    # This function moves the gear to the position of your mouse, when the left mouse button is pressed
    global gearAngle
    if mouseL:
        new_angle = math.atan2(mouseY - gearCenter[1], mouseX - gearCenter[0])
        return new_angle
    return gearAngle


def automate_gear():
    # This gear automatically moves the gear
    # (clockwise or counterclockwise direction can be toggled with right mouse click)
    global mousePressed
    global direction
    global gearAngle
    if mouseR:
        if not mousePressed and direction == "CW":
            mousePressed = True
            direction = "CCW"
        if not mousePressed and direction == "CCW":
            mousePressed = True
            direction = "CW"
    if not mouseR:
        mousePressed = False

    if direction == "CW":
        gearAngle += dt * gearSpeed
    if direction == "CCW":
        gearAngle -= dt * gearSpeed


def draw_laser():
    # This function draws a laser, that can't go through the gear, simulating how the encoder works
    y_2 = gearCenter[1] + math.ceil(math.sin(angleTeeth / 2) * gearRadius)
    start_pos_2 = (gearCenter[0], y_2)

    if screen.get_at((gearCenter[0] + int(gearRadius*(17/18)), gearCenter[1])) == backColour:
        end_pos_1 = [gearCenter[0] + gearRadius * 2, gearCenter[1]]
        s1 = 1
    else:
        end_pos_1 = [gearCenter[0] + int(gearRadius*(17/18)), gearCenter[1]]
        s1 = 0

    if screen.get_at((gearCenter[0] + int(gearRadius*(17/18)), y_2)) == backColour:
        end_pos_2 = (gearCenter[0] + gearRadius * 2, y_2)
        s2 = 1
    else:
        end_pos_2 = (gearCenter[0] + int(gearRadius*(17/18)), y_2)
        s2 = 0

    pygame.draw.line(screen, laserColour1, gearCenter, end_pos_1)
    pygame.draw.line(screen, laserColour2, start_pos_2, end_pos_2)

    return [s1, s2]


def draw_graph(graph, colour):
    # This function draws a moving graph, to show the phase difference between the two signals
    for i in range(len(graph) - 1):
        n = screenX - i - 2
        pygame.draw.line(screen, colour, (i, screenY - graphFactor * graph[n+1]),
                         (i + 1, screenY - graphFactor * graph[n]))


# main loop
running = True
while running:

    # Background
    screen.fill(backColour)

    # Get dt
    now = time.time()
    dt = now - prev_time
    prev_time = now

    # Get mouse inputs
    [mouseX, mouseY] = pygame.mouse.get_pos()
    [mouseL, mouseM, mouseR] = pygame.mouse.get_pressed()

    # Allow gear to move automatically and allow user to move the gear
    automate_gear()
    gearAngle = move_gear()
    draw_gear(gearAngle)

    # Draw the laser and get info on whether the laser passes through the gear
    [signal1, signal2] = draw_laser()

    # calculate signals for graphing
    graph1.append(signal1)
    graph2.append(signal2)
    graph1.pop(0)
    graph2.pop(0)

    # Draw graphs
    draw_graph(graph1, laserColour1)
    draw_graph(graph2, laserColour2)

    # This forloop loops through all the events, like keyboard-presses, clicks, quit-button-press, etc.
    for event in pygame.event.get():

        # quit game if you press x in right top corner
        if event.type == pygame.QUIT:
            running = False

    # Update the display, so we see what's happening
    pygame.display.update()