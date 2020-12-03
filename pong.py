# This is a program that starts a video game involving
# a ball and two rectangles, which are represented as
# paddles. This game resembles that of Pong.
# Start the game by pressing the spacebar key
# Press "a" to move the left paddle up and "z" to move it down
# Press "k" to move the right paddle up and "m" to move it down
# Press spacebar again to restart the game
# Press "q" to quit the game
# Written by Vico Lee Zheng Yuan
# 30 September 2020

from cs1lib import *
from random import randint

WINDOW_HEIGHT = 400
WINDOW_WIDTH = 400
PADDLE_HEIGHT = 75
PADDLE_WIDTH = 10

# Keys to move the left and right paddle
LEFT_UP = "a"
LEFT_DOWN = "z"
RIGHT_UP = "k"
RIGHT_DOWN = "m"
RIGHT_DOWN = "m"
PADDLE_SPEED = 15

# Paddle image
paddle_img = load_image("./images/paddle.png")

# Top left coordinates of paddle
left_x = 0
left_y = 0

# Top right coordinates of paddle
right_x = WINDOW_WIDTH - PADDLE_WIDTH
right_y = WINDOW_HEIGHT - PADDLE_HEIGHT

# Ball
ball_x = 200
ball_y = 200
ball_speed_x = randint(5, 8)
ball_speed_x_sign = randint(-1, 1)
while ball_speed_x_sign == 0:
    ball_speed_x_sign = randint(-1, 1)  # Make sure that the sign is not zero
ball_speed_x *= ball_speed_x_sign
ball_speed_y = randint(-7, 7)

# Random ball colors which changes at each bounce on the paddle
red_ratio = randint(0, 100) / 100
green_ratio = randint(0, 100) / 100
blue_ratio = randint(0, 100) / 100
BALL_RADIUS = 15

# Score
left_score = 0
right_score = 0

first_bounce = True
pressed_A = False
pressed_Z = False
pressed_K = False
pressed_M = False
start_screen = False  # Set to true to start the game from scratch
started = False
end = False

# press updates the boolean values of the key variables when the key is pressed
def press(key):
    global pressed_A, pressed_K, pressed_M, pressed_Z, start_screen, started, end

    if key == "a":
        pressed_A = True
    if key == "z":
        pressed_Z = True
    if key == "k":
        pressed_K = True
    if key == "m":
        pressed_M = True
    if key == "q":
        start_screen = False
        end = True
    if key == " ":
        start_screen = True
        started = True

# release updates the boolean values of the key variables when the key is released
def release(key):
    global pressed_A, pressed_K, pressed_M, pressed_Z, start_screen, end, started

    if key == "a":
        pressed_A = False
    if key == "z":
        pressed_Z = False
    if key == "k":
        pressed_K = False
    if key == "m":
        pressed_M = False
    if key == "q":
        start_screen = False
        end = False
        started = False
    if key == " ":
        start_screen = False
        started = True

# start_game sets up the paddles and the ball at its starting position
def start_game():
    global started

    started = True
    draw_objects(left_x, left_y, right_x, right_y, ball_x, ball_y)

# left_up shifts the left paddle up when 'a' is pressed
def left_up():
    global left_x, left_y

    if left_y > 0:
        left_y -= PADDLE_SPEED
        draw_objects(left_x, left_y, right_x, right_y, ball_x, ball_y)

# left_down shifts the left paddle down when 'z' is pressed
def left_down():
    global left_x, left_y

    if left_y + PADDLE_HEIGHT < 400:
        left_y += PADDLE_SPEED
        draw_objects(left_x, left_y, right_x, right_y, ball_x, ball_y)

# right_up shifts the right paddle up when 'k' is pressed
def right_up():
    global right_x, right_y

    if right_y > 0:
        right_y -= PADDLE_SPEED
        draw_objects(left_x, left_y, right_x, right_y, ball_x, ball_y)

# right_down shifts the right paddle down when 'm' is pressed
def right_down():
    global right_x, right_y

    if right_y + PADDLE_HEIGHT < 400:
        right_y += PADDLE_SPEED
        draw_objects(left_x, left_y, right_x, right_y, ball_x, ball_y)

"""
move_ball updates the coordinates of the ball, bouncing the ball
when it hits the sides and the paddles and ending the game when
the ball passes the left or right sides.
"""
def move_ball():
    global ball_x, ball_y, ball_speed_x, ball_speed_y, first_bounce

    ball_x += ball_speed_x
    ball_y += ball_speed_y
    draw_objects(left_x, left_y, right_x, right_y, ball_x, ball_y)

    # bounce ball when hits right paddle or ends game if ball passes through
    if ball_x >= right_x - BALL_RADIUS:

        if ball_x - BALL_RADIUS >= WINDOW_WIDTH: # left side of ball crosses right window
            goal("right")

        if ball_y >= right_y and ball_y <= right_y + PADDLE_HEIGHT: # ball hits the right paddle

            if first_bounce:
                ball_speed_y = randint(5, 10)   # start off with a random vertical velocity if its the first bounce
                first_bounce = False

            bounce_ball_x() # Flip the x velocity of the ball
            random_bounce_y() # Add randomness in direction of bounce vertically
            change_ball_color()

            if pressed_K or pressed_M:
                bounce_ball_y() # bounce ball in the vertical direction when paddle is moving.

    # bounce ball when hits left paddle or ends game if ball passes through
    elif ball_x <= left_x + PADDLE_WIDTH + BALL_RADIUS:

        if ball_x + BALL_RADIUS <= 0:
            goal("left")  # right side of ball crosses left window

        if ball_y >= left_y and ball_y <= left_y + PADDLE_HEIGHT:

            if first_bounce:
                ball_speed_y = randint(5, 10) # start off with a random vertical velocity
                first_bounce = False

            bounce_ball_x() # Flip the x velocity of the ball
            random_bounce_y() # Add randomness in direction of bounce vertically
            change_ball_color()

    # bounce ball vertically if hits the top
    elif ball_y - BALL_RADIUS <= 0:
        bounce_ball_y() # Flip the y velocity of the ball
        random_bounce_x() # Add randomness in direction of horizontal bounce

    # bounce ball vertically if hits the bottom
    elif ball_y + BALL_RADIUS >= WINDOW_HEIGHT:
        bounce_ball_y() # Flip the y velocity of the ball
        random_bounce_x() # Add randomness in direction of horizontal bounce

def random_bounce_x():
    global ball_speed_x

    random_speed = randint(5, 10)
    random_sign = randint(-1, 1)
    while random_sign == 0:
        random_sign = randint(-1, 1)
    ball_speed_x = random_speed * random_sign

def random_bounce_y():
    global ball_speed_y

    random_speed = randint(5, 10)
    random_sign = randint(-1, 1)
    while random_sign == 0:
        random_sign = randint(-1, 1)
    ball_speed_y = random_speed * random_sign

def change_ball_color():
    global red_ratio, green_ratio, blue_ratio

    red_ratio = randint(0, 100) / 100
    green_ratio = randint(0, 100) / 100
    blue_ratio = randint(0, 100) / 100

# draw_objects draws the paddles and the ball with their respective coordinates
def draw_objects(left_x, left_y, right_x, right_y, ball_x, ball_y):

    set_clear_color(0, 0, 0) # black background
    clear()
    draw_image(paddle_img, left_x, left_y) # draw left paddle
    draw_image(paddle_img, right_x, right_y) # draw right paddle
    set_stroke_color(1, 1, 0) # draw scoreboard
    set_font_size(30)
    draw_text("{} - {}".format(left_score, right_score), 175, 50)
    set_stroke_color(0, 0, 0)
    set_fill_color(red_ratio, green_ratio, blue_ratio)
    draw_circle(ball_x, ball_y, BALL_RADIUS) # ball

# bounce_ball_x flips the value of ball_speed_x to switch the ball's horizontal direction
def bounce_ball_x():
    global ball_speed_x
    ball_speed_x *= -1

# bounce_ball_x flips the value of ball_speed_y to switch the ball's vertical direction
def bounce_ball_y():
    global ball_speed_y
    ball_speed_y *= -1

# goal is called when the ball passes the left or right side of the window
# param side is the side at which the ball passed through
def goal(side):
    global right_score, left_score

    end_game()
    start_game()

    if side == "left":
        right_score += 1
    elif side == "right":
        left_score += 1

# reset_score resets the score of the game when spacebar is called
def reset_score():
    global right_score, left_score

    right_score = 0
    left_score = 0

# end_game ends the game when the 'q' is pressed or when someone scores a goal
def end_game():
    set_clear_color(0, 0, 0)
    clear()
    reset_game()

# reset_game sets all the variables back to its starting state
def reset_game():
    global left_x, left_y, right_x, right_y, ball_x, ball_y, pressed_A, \
        pressed_Z, pressed_M, pressed_K, start_screen, started, end, ball_speed_x, \
        ball_speed_y, first_bounce

    # Top left coordinates of paddle
    left_x = 0
    left_y = 0

    # Top right coordinates of paddle
    right_x = WINDOW_WIDTH - PADDLE_WIDTH
    right_y = WINDOW_HEIGHT - PADDLE_HEIGHT

    # Ball
    ball_x = 200
    ball_y = 200
    ball_speed_x = randint(5, 8)
    ball_speed_x_sign = randint(-1, 1)
    while ball_speed_x_sign == 0:
        ball_speed_x_sign = randint(-1, 1) # Make sure that the sign is not zero
    ball_speed_x *= ball_speed_x_sign
    ball_speed_y = randint(-7, 7)

    first_bounce = True
    pressed_A = False
    pressed_Z = False
    pressed_K = False
    pressed_M = False
    start_screen = False  # Set to true to start the game from scratch
    started = False
    end = False

def draw():
    if start_screen: # If spacebar pressed, restarts or starts game
        end_game()
        reset_score()
        start_game()
    if started:
        move_ball()
        if end:
            end_game()
        if pressed_A:
            left_up()
        if pressed_Z:
            left_down()
        if pressed_K:
            right_up()
        if pressed_M:
            right_down()

start_graphics(draw, width = WINDOW_WIDTH, height = WINDOW_HEIGHT, key_press = press, key_release = release)
