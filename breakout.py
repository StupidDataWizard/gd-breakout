import pygame
import random
import settings
from paddle import Paddle
from brick import Brick, HardBrick, SpecialBrick
from ball import Ball
from counter import Counter


# Initialize the PyGame
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Screen setup
screen = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Breakout")

# Clock setup
clock = pygame.time.Clock()
FPS = 60

# Colors
BLACK = pygame.Color("black")
WHITE = pygame.Color("snow")
RED = pygame.Color("red4")
ORANGE = pygame.Color("coral")
GREEN = pygame.Color("green4")
YELLOW = pygame.Color("yellow")
BLUE = pygame.Color("skyblue1")
PINK = pygame.Color("hotpink4")
GREY = pygame.Color("grey50")

# Fonts
MESSAGE_FONT = pygame.font.Font("squarefont.ttf", 50)
INSTRUCTION_FONT = pygame.font.Font("squarefont.ttf", 30)

# Start message
start_message = MESSAGE_FONT.render("HIT SPACE TO START THE BALL", True, BLUE)
control_message = INSTRUCTION_FONT.render("A/D TO MOVE LEFT/RIGHT", True, BLUE)
music_message = INSTRUCTION_FONT.render("M TO TOGGLE MUSIC", True, BLUE)
fx_message = INSTRUCTION_FONT.render("N TO TOGGLE SOUND", True, BLUE)

BRICK_HEIGHT = 15
BRICK_WIDTH = 50
BRICK_MARGIN = 0
BRICK_BORDER = 0
BRICK_TOP = 100

ROW_COLORS = [RED, RED, ORANGE, ORANGE, GREEN, GREEN, YELLOW, YELLOW]

HARD_BRICK_COLOR = GREY
SPECIAL_BRICK_COLOR = PINK
# HARD_BRICK_PERCENTAGE = 20
# Sprites
paddles = pygame.sprite.Group()
balls = pygame.sprite.Group()
bricks = pygame.sprite.Group()

Paddle.PADDLE_HEIGHT = BRICK_HEIGHT
paddle = Paddle((350, 450), 1000, 400, BLUE)
paddles.add(paddle)
'''
for row in range(8):
    for column in range(14):
        x = BRICK_BORDER + column * (BRICK_WIDTH + 2 * BRICK_MARGIN) + BRICK_MARGIN
        y = BRICK_TOP + row * (BRICK_HEIGHT + 2 * BRICK_MARGIN) + BRICK_MARGIN
        if random.randint(1, 100) <= HARD_BRICK_PERCENTAGE:
            brick = HardBrick((x, y), (BRICK_WIDTH, BRICK_HEIGHT), HARD_BRICK_COLOR)
        else:
            brick = Brick((x, y), (BRICK_WIDTH, BRICK_HEIGHT), ROW_COLORS[row])

        # Add brick to the group
        bricks.add(brick)
'''
N_ROWS = 8
N_COLUMNS = 14
TOTAL_BRICKS = N_ROWS * N_COLUMNS
HARD_BRICK_PERCENTAGE = 0.2

n_hard_bricks = int(TOTAL_BRICKS * HARD_BRICK_PERCENTAGE)
brick_types = []

for i in range(n_hard_bricks):
    brick_types.append('hard')
brick_types.extend(['normal'] * (TOTAL_BRICKS - n_hard_bricks))
random.shuffle(brick_types)
brick_types[random.randint(-14, -1)] = "special"

index = 0
for row in range(N_ROWS):
    for column in range(N_COLUMNS):
        x = BRICK_BORDER + column * (BRICK_WIDTH + 2 * BRICK_MARGIN) + BRICK_MARGIN
        y = BRICK_TOP + row * (BRICK_HEIGHT + 2 * BRICK_MARGIN) + BRICK_MARGIN
        if brick_types[index] == 'hard':
            brick = HardBrick((x, y), (BRICK_WIDTH, BRICK_HEIGHT), HARD_BRICK_COLOR)
        elif brick_types[index] == 'normal':
            brick = Brick((x, y), (BRICK_WIDTH, BRICK_HEIGHT), ROW_COLORS[row])
        elif brick_types[index] == 'special':
            brick = SpecialBrick((x, y), (BRICK_WIDTH, BRICK_HEIGHT), SPECIAL_BRICK_COLOR)
        index += 1
        bricks.add(brick)
for brick in bricks:
    brick.init_neighbours(bricks)

# Counters
score = Counter((10, 10), "squarefont.ttf", 80, WHITE)
lives = Counter((360, 10), "squarefont.ttf", 80, WHITE)
lives.set_value(5)

# Background
background = pygame.Surface(screen.get_rect().size)
background.fill(BLACK)

# Music
pygame.mixer.music.load("breakout-music.ogg")
pygame.mixer.music.play(-1)

pygame.mixer.music.set_volume(0.5)

# Flag for sound effect mute
muted = True

# Game loop
running = True
dt = 0
while running:

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Only start a ball if there is none
                if not len(balls):
                    # We start a new ball at the center of the paddle
                    ball = Ball(paddle.rect.midtop, PINK, pygame.Rect(0, 90, 700, 410), bricks, paddle)
                    balls.add(ball)
                    ball.start(600, random.randint(-135, -45))
            if event.key == pygame.K_m:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play()
            if event.key == pygame.K_n:
                settings.sfx_muted = not settings.sfx_muted
        elif event.type == SpecialBrick.SPAWN_BALL:
            position = event.position
            new_ball = Ball(position, PINK, pygame.Rect(0, 90, 700, 410), bricks, paddle)
            balls.add(new_ball)
            new_ball.start(600, random.randint(-135, -45))
        elif event.type == Brick.BRICK_DESTROYED:
            score.change_value(event.value)
        elif event.type == Ball.BALL_LOST:
            lives.change_value(-1)
            if lives.get_value() == 0:
                running = False

    # Update
    paddles.update(dt)
    balls.update(dt)
    bricks.update(dt)

    # Draw
    screen.blit(background, (0, 0))
    paddles.draw(screen)
    bricks.draw(screen)
    balls.draw(screen)
    score.draw(screen)
    lives.draw(screen)

    # Show start message if there is no ball
    if not len(balls):
        y = screen.get_rect().centery
        for msg in [start_message, control_message, music_message, fx_message]:
            rect = msg.get_rect()
            rect.centerx = screen.get_rect().centerx
            rect.centery = y
            screen.blit(msg, rect)
            y += rect.height * 1.2

    # Display new frame
    pygame.display.flip()

    # Calculate delta time
    dt = clock.tick(FPS) / 1000

# Very simple game over screen...
pygame.mixer.music.stop()
screen.fill(RED)
text = MESSAGE_FONT.render(f"Your Score: {score.get_value()}", True, WHITE)
rect = text.get_rect()
rect.center = screen.get_rect().center
screen.blit(text, rect)
pygame.display.flip()

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(FPS)
