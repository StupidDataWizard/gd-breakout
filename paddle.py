import pygame

class Paddle(pygame.sprite.Sprite):
    
    PADDLE_HEIGHT = 5

    def __init__(self, position, size, speed, color, left=pygame.K_a, right=pygame.K_d):
        super().__init__()
        # Set the image and rect for the position
        # No unneccessary book keeping, positon and size are stored in the rect
        self.image = pygame.Surface((size, Paddle.PADDLE_HEIGHT))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, color, self.rect)

        # The position defines the CENTER of the paddle!
        self.rect.center = position

        # Further configuration
        self.speed = speed
        self.color = color

        # Here, A and D are set by default parameters
        self.left = left
        self.right = right

        # The limits for the left and right wall are hard coded,
        # but can of course be changed via these variables 
        self.min_x = 0
        self.max_x = pygame.display.get_surface().get_size()[0]


    def update(self, dt):
        # dt is delta time in seconds
        pressed = pygame.key.get_pressed()
        dx = 0
        if pressed[self.left]:
            dx -= self.speed * dt
        if pressed[self.right]:
            dx += self.speed * dt
        if dx != 0:
            self.rect.centerx += dx
        if self.rect.left < self.min_x:
            self.rect.left = self.min_x
        if self.rect.right > self.max_x:
            self.rect.right = self.max_x
