import pygame

# Game configuration
FPS = 60
BRICK_HEIGHT = 15
BRICK_WIDTH = 50
BRICK_MARGIN = 0
BRICK_BORDER = 0
BRICK_TOP = 100
N_ROWS = 8
N_COLUMNS = 14
TOTAL_BRICKS = N_ROWS * N_COLUMNS
HARD_BRICK_PERCENTAGE = 0.2
PADDLE_HEIGHT = BRICK_HEIGHT

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
ROW_COLORS = [RED, RED, ORANGE, ORANGE, GREEN, GREEN, YELLOW, YELLOW]
HARD_BRICK_COLOR = GREY
SPECIAL_BRICK_COLOR = PINK

# Sound
sfx_muted = False
