import time
import serial
import pygame
import math

arduinoData = serial.Serial('com5', 9600)
time.sleep(1)

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
fps = 60

# Create the screen
screenX = 1000
screenY = 700
screen = pygame.display.set_mode((screenX, screenY))

# Title and Icon
pygame.display.set_caption("Conveyor Belt Visualisation")

# Colours
back_colour = (200, 200, 200)
wheel_colour = (50, 50, 50)
con_colour2 = (50, 50, 50)
con_colour3 = (125, 125, 125)
light_colour = back_colour

# Conveyor Belt Settings
con_pos_a = (screenX / 4, screenY*(2/3))
con_length = screenX / 2                            # num of pixels that represents 1m
con_radius = screenY / 10
con_velocity = 0                                    # Speed of the conveyor belt (meters per second)
max_velocity = 1
con_velocity = (con_length*con_velocity)/fps        # Speed of the conveyor belt (pixels per frame)
stripe_width = math.floor(screenX / 40)
stripe_offset = 0                                   # The offset of the first set of striped lines (in pixels)
stripe_offset2 = 0                                  # The offset of the second set of striped lines (in pixels)
brightness = 0
direction = True
laser = True
exposure = 0

# set up the font
font = pygame.font.SysFont("None", 30)


# Functions:
def conveyor(pos_a, length, radius, colour1, colour2, colour3, offset1, offset2):
    pos_b = (pos_a[0] + length, pos_a[1])

    # Draw the first part of the conveyor belt
    pygame.draw.line(screen, colour2, (pos_a[0], pos_a[1] - radius), (pos_b[0], pos_b[1] - radius), 3)
    pygame.draw.line(screen, colour2, (pos_a[0], pos_a[1] + radius - 1), (pos_b[0], pos_b[1] + radius - 1), 3)

    # Draw moving lines to visualise the movement
    for i in range(int(pos_a[0]), int(pos_b[0]), stripe_width * 2):
        pygame.draw.line(screen, colour3, (i + offset1, pos_a[1] - radius),
                         (i + stripe_width + offset1, pos_b[1] - radius), 3)
        pygame.draw.line(screen, colour3, (i + offset2, pos_a[1] + radius-1),
                         (i + stripe_width + offset2, pos_b[1] + radius-1), 3)

    pygame.draw.rect(screen, back_colour, (pos_b[0], pos_b[1]-radius*2, stripe_width, screenY/2))

    pygame.draw.circle(screen, colour2, pos_a, radius, 3)
    pygame.draw.circle(screen, colour2, pos_b, radius, 3)

    # Draw left moving half-circle
    for i in range(90, 270, stripe_width * 2):
        start_angle = math.radians(i - offset1)
        end_angle = math.radians(i + stripe_width - offset1)
        pygame.draw.arc(screen, colour3, [pos_a[0] - radius, pos_a[1] - radius, radius * 2, radius * 2], start_angle,
                        end_angle, 3)

    # Draw right moving half-circle
    for i in range(270, 450, stripe_width * 2):
        start_angle = math.radians(i - offset1)
        end_angle = math.radians(i + stripe_width - offset1)
        pygame.draw.arc(screen, colour3, [pos_b[0] - radius, pos_b[1] - radius, radius * 2, radius * 2], start_angle,
                        end_angle, 3)


def draw_circular_arrow(pos, radius, angle, thickness):
    arrow_head_width = 10

    pygame.draw.arc(screen, (255, 255, 255), pygame.Rect(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2),
                    math.radians(angle), math.radians(angle + 180), thickness)
    arrow_1 = (pos[0] + radius * math.cos(math.radians(angle)) - (arrow_head_width / 2) * math.cos(math.radians(angle)),
               pos[1] - radius * math.sin(math.radians(angle)) + (arrow_head_width / 2) * math.sin(math.radians(angle)))
    arrow_2 = (pos[0] + radius * math.cos(math.radians(angle)) + (arrow_head_width / 2) * math.cos(math.radians(angle)),
               pos[1] - radius * math.sin(math.radians(angle)) - (arrow_head_width / 2) * math.sin(math.radians(angle)))
    arrow_3 = (pos[0] + radius * math.cos(math.radians(angle - 20)), pos[1] - radius * math.sin(math.radians(angle-20)))
    pygame.draw.polygon(screen, (255, 255, 255), [arrow_1, arrow_2, arrow_3])


def draw_line_light(pos, light_size, light_angle, belt_pos, belt_radius, colour_index):
    belt_pos = belt_pos[1] - belt_radius - 2
    beam_thickness1 = 70    # Percentage of with of camera
    beam_thickness2 = 20    # pixels

    # Calculate camera shell positions
    light_box1 = (pos[0] + light_size * math.cos(math.radians(light_angle - 45)),
                  pos[1] - light_size * math.sin(math.radians(light_angle - 45)))
    light_box2 = (pos[0] + light_size * math.cos(math.radians(light_angle - 45 + (1 / 4) * 360)),
                  pos[1] - light_size * math.sin(math.radians(light_angle - 45 + (1 / 4) * 360)))
    light_box3 = (pos[0] + light_size * math.cos(math.radians(light_angle - 45 + (2 / 4) * 360)),
                  pos[1] - light_size * math.sin(math.radians(light_angle - 45 + (2 / 4) * 360)))
    light_box4 = (pos[0] + light_size * math.cos(math.radians(light_angle - 45 + (3 / 4) * 360)),
                  pos[1] - light_size * math.sin(math.radians(light_angle - 45 + (3 / 4) * 360)))

    # Calculate beam colour
    beam_colour = (back_colour[0] + (colour_index / 100) * (255 - back_colour[0]),
                   back_colour[1] + (colour_index / 100) * (255 - back_colour[1]),
                   back_colour[2] + (colour_index / 100) * (0 - back_colour[2]))

    # Calculate light beam positions
    intersect_point = pos[0] + (math.tan(math.radians(light_angle)) * (belt_pos - pos[1]))
    light_pos1 = (light_box4[0] + (light_box1[0] - light_box4[0]) * (1 - (100 - beam_thickness1) / 200),
                  light_box1[1] + (light_box4[1] - light_box1[1]) * (100 - beam_thickness1) / 200)
    light_pos2 = (light_box4[0] + (light_box1[0] - light_box4[0]) * (100 - beam_thickness1) / 200,
                  light_box1[1] + (light_box4[1] - light_box1[1]) * (1 - (100 - beam_thickness1) / 200))
    light_pos3 = (intersect_point - beam_thickness2, belt_pos)
    light_pos4 = (intersect_point + beam_thickness2, belt_pos)

    # Draw light beam
    pygame.draw.polygon(screen, beam_colour, [light_pos1, light_pos2, light_pos3, light_pos4])
    # Draw camera shell
    pygame.draw.polygon(screen, (255, 255, 255), [light_box1, light_box2, light_box3, light_box4], 2)


def draw_lsc(pos, size, belt_pos, belt_radius, laser):

    lsc_box = pygame.Rect(pos[0], pos[1], size, size)
    lens1 = (pos[0] + 0.8 * size, pos[1] + size - 1)
    lens2 = (pos[0] + 0.2 * size, pos[1] + size - 1)
    lens3 = (pos[0], pos[1] + 1.5 * size)
    lens4 = (pos[0] + size, pos[1] + 1.5 * size)
    lsc_beam1 = (pos[0] + size/2, lens4[1] + 2)
    lsc_beam2 = (lsc_beam1[0], belt_pos[1] - belt_radius - 2)

    pygame.draw.rect(screen, (255, 255, 255), lsc_box, 2)
    pygame.draw.polygon(screen, (255, 255, 255), [lens1, lens2, lens3, lens4], 2)

    if laser:
        pygame.draw.line(screen, (255, 0, 0), lsc_beam1, lsc_beam2, 1)


def draw_text(pos, text):
    # create the square
    square_padding = 10
    text_surface = font.render(text, True, (0, 0, 0))
    square_size = (text_surface.get_width() + 2 * square_padding, text_surface.get_height() + 2 * square_padding)
    square_color = (255, 255, 255)
    square_pos = (pos[0] - square_size[0] // 2, pos[1] - square_size[1] // 2)
    square_rect = pygame.Rect(square_pos, square_size)

    # draw the border
    border_width = 2
    pygame.draw.rect(screen, square_color, square_rect, border_width)

    # add the text
    text_rect = text_surface.get_rect(center=square_rect.center)
    screen.blit(text_surface, text_rect)


# main loop
running = True
while running:
    while (arduinoData.inWaiting() == 0):
        # Background
        screen.fill(back_colour)

        # Update stripe offsets based on conveyor velocity
        stripe_offset += con_velocity
        stripe_offset2 -= con_velocity

        # Calculate brightness based on conveyor belt speed
        brightness = con_velocity * (100 / max_velocity)
        if brightness > 100:
            brightness = 100

        # Calculate if lsc should be exposed
        exposure += con_velocity
        if exposure > 2:
            laser = False
        if exposure > 4:
            laser = True
            exposure = 0

        # Draw conveyor belt
        conveyor(con_pos_a, con_length, con_radius, wheel_colour, con_colour2, con_colour3,
                 stripe_offset % (stripe_width * 2), stripe_offset2 % (stripe_width * 2))

        # Draw arrow in left roller
        draw_circular_arrow(con_pos_a, screenY / 15, - stripe_offset, 1)

        # Draw line light
        draw_line_light((screenX * (5 / 9), screenY * (2 / 5)), 30, 40, con_pos_a, con_radius, brightness)

        # Draw LSC
        draw_lsc((screenX * (7 / 11), screenY * (2 / 9)), 30, con_pos_a, con_radius, laser)

        # Calculate trigger frequency
        trig_freq = con_velocity * 1000 / 0.1953

        # Draw text
        draw_text((screenX * (1 / 4), screenY * (1 / 2)), str(con_velocity) + " m/s")
        draw_text((screenX * (1 / 2), screenY * (1 / 3)), str(round(brightness)) + "%")
        draw_text((screenX * (6 / 8), screenY * (1 / 5)),
                  str(round(trig_freq, 2)) + " Hz")

        # This for loop loops through all the events, like keyboard-presses, clicks, quit-button-press, etc.
        for event in pygame.event.get():

            # quit game if you press x in right top corner
            if event.type == pygame.QUIT:
                running = False

        clock.tick(fps)
        # Update the display, so we see what's happening
        pygame.display.update()
    dataPacket = arduinoData.readline()
    dataPacket = str(dataPacket, 'utf-8')
    dataPacket = dataPacket.strip('\r\n')
    con_velocity = float(dataPacket)
