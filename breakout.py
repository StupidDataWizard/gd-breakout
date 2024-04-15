import random
import settings
from paddle import Paddle
from brick import Brick, HardBrick, SpecialBrick
from ball import Ball
from counter import Counter
from settings import *


def initialize():
    # Initialize the PyGame
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    # Screen setup
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption("Breakout")

    # Clock setup
    clock = pygame.time.Clock()
    FPS = 60

    # Fonts
    MESSAGE_FONT = pygame.font.Font("squarefont.ttf", 50)
    INSTRUCTION_FONT = pygame.font.Font("squarefont.ttf", 30)

    # Start message
    start_message = MESSAGE_FONT.render("HIT SPACE TO START THE BALL", True, BLUE)
    control_message = INSTRUCTION_FONT.render("A/D TO MOVE LEFT/RIGHT", True, BLUE)
    music_message = INSTRUCTION_FONT.render("M TO TOGGLE MUSIC", True, BLUE)
    fx_message = INSTRUCTION_FONT.render("N TO TOGGLE SOUND", True, BLUE)

    # Music
    pygame.mixer.music.load("breakout-music.ogg")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)

    return screen, clock, FPS, BLACK, WHITE, RED, ORANGE, GREEN, YELLOW, BLUE, PINK, GREY, MESSAGE_FONT, INSTRUCTION_FONT, start_message, control_message, music_message, fx_message

def generate_level_layout(total_bricks, hard_brick_percentage):
    n_hard_bricks = int(total_bricks * hard_brick_percentage)
    brick_types = ['hard'] * n_hard_bricks
    brick_types.extend(['normal'] * (total_bricks - n_hard_bricks))
    random.shuffle(brick_types)
    brick_types[random.randint(-14, -1)] = "special"
    return brick_types

def build_brick_wall(bricks, brick_types, N_ROWS, N_COLUMNS, BRICK_BORDER, BRICK_WIDTH, BRICK_MARGIN, BRICK_HEIGHT, BRICK_TOP, ROW_COLORS, HARD_BRICK_COLOR, SPECIAL_BRICK_COLOR):
    index = 0
    for row in range(N_ROWS):
        for column in range(N_COLUMNS):
            x = BRICK_BORDER + column * (BRICK_WIDTH + 2 * BRICK_MARGIN) + BRICK_MARGIN
            y = BRICK_TOP + row * (BRICK_HEIGHT + 2 * BRICK_MARGIN) + BRICK_MARGIN
            if brick_types[index] == 'hard':
                brick = SpecialBrick((x, y), (BRICK_WIDTH, BRICK_HEIGHT), HARD_BRICK_COLOR)
            elif brick_types[index] == 'normal':
                brick = Brick((x, y), (BRICK_WIDTH, BRICK_HEIGHT), ROW_COLORS[row])
            elif brick_types[index] == 'special':
                brick = SpecialBrick((x, y), (BRICK_WIDTH, BRICK_HEIGHT), SPECIAL_BRICK_COLOR)
            index += 1
            bricks.add(brick)
    for brick in bricks:
        brick.init_neighbours(bricks)

def update_game(dt, paddles, balls, bricks):
    # Update
    paddles.update(dt)
    balls.update(dt)
    bricks.update(dt)

def draw_game(screen, background, paddles, bricks, balls, score, lives, start_message, control_message, music_message, fx_message):
    # Draw
    screen.blit(background, (0, 0))
    paddles.draw(screen)
    bricks.draw(screen)
    balls.draw(screen)
    score.draw(screen)
    lives.draw(screen)

screen, clock, FPS, BLACK, WHITE, RED, ORANGE, GREEN, YELLOW, BLUE, PINK, GREY, MESSAGE_FONT, INSTRUCTION_FONT, start_message, control_message, music_message, fx_message = initialize()


# Sprites
paddles = pygame.sprite.Group()
balls = pygame.sprite.Group()
bricks = pygame.sprite.Group()

Paddle.PADDLE_HEIGHT = BRICK_HEIGHT
paddle = Paddle((350, 450), 200, 400, BLUE)
paddles.add(paddle)

N_ROWS = 8
N_COLUMNS = 14
TOTAL_BRICKS = N_ROWS * N_COLUMNS
HARD_BRICK_PERCENTAGE = 0.2

brick_types = generate_level_layout(TOTAL_BRICKS, HARD_BRICK_PERCENTAGE)

build_brick_wall(bricks, brick_types, N_ROWS, N_COLUMNS, BRICK_BORDER, BRICK_WIDTH, BRICK_MARGIN, BRICK_HEIGHT, BRICK_TOP, ROW_COLORS, HARD_BRICK_COLOR, SPECIAL_BRICK_COLOR)

# Counters
score = Counter((10, 10), "squarefont.ttf", 80, WHITE)
lives = Counter((360, 10), "squarefont.ttf", 80, WHITE)
lives.set_value(5)

# Background
background = pygame.Surface(screen.get_rect().size)
background.fill(BLACK)

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
            if len(balls) == 0:
                lives.change_value(-1)
                if lives.get_value() == 0:
                    running = False

    update_game(dt, paddles, balls, bricks)
    draw_game(screen, background, paddles, bricks, balls, score, lives, start_message, control_message, music_message,
              fx_message)

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
