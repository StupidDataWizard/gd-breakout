import pygame
import settings


class Brick(pygame.sprite.Sprite):
    LINE_COLOR = pygame.Color(0, 0, 0)
    BRICK_DESTROYED = pygame.event.custom_type()

    def __init__(self, position, size, color):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, color, self.rect)
        pygame.draw.rect(self.image, Brick.LINE_COLOR, self.rect, 1)
        # The position defines the TOP LEFT of the brick!
        self.rect.topleft = position
        self.color = color
        # The score value of this brick when destroyed
        self.value = 1
        # Dictionary contains neighbour bricks
        # Keys: top, bottom, left, right
        self.neighbours = {}
        # Bounce sound
        self.hit_sound = pygame.mixer.Sound("explosion.wav")
        self.hit_sound.set_volume(0.5)
    # JN: Collision Handling

    def init_neighbours(self, bricks):
        collidepoints = {
            "top": (self.rect.centerx, self.rect.top - 2),
            "bottom": (self.rect.centerx, self.rect.bottom + 2),
            "left": (self.rect.left - 2, self.rect.centery),
            "right": (self.rect.right + 2, self.rect.centery)
        }

        for brick in bricks:
            for side in collidepoints:
                point = collidepoints[side]
                if brick.rect.collidepoint(point):
                    # brick is a neighbour at side
                    self.neighbours[side] = brick
                    # No need to check this side again
                    del collidepoints[side]
                    if not collidepoints:
                        # All neighbours found, we are done
                        return
                    # There are sides left, but this brick is done
                    break

    def clear_neighbours(self):
        if "top" in self.neighbours:
            del self.neighbours["top"].neighbours["bottom"]
        if "bottom" in self.neighbours:
            del self.neighbours["bottom"].neighbours["top"]
        if "left" in self.neighbours:
            del self.neighbours["left"].neighbours["right"]
        if "right" in self.neighbours:
            del self.neighbours["right"].neighbours["left"]

    def hit(self):
        if not settings.sfx_muted:
            self.hit_sound.play()
        self.clear_neighbours()
        self.kill()
        event = pygame.event.Event(Brick.BRICK_DESTROYED, value=self.value)
        pygame.event.post(event)

    def update(self, dt):
        pass


class HardBrick(Brick):
    def __init__(self, position, size, color):
        super().__init__(position, size, color)
        self.value = 1
        self.hit_count = 2
        #PINK = pygame.Color("hotpink4")
        #self.color = PINK

    def hit(self):
        if not settings.sfx_muted:
            self.hit_sound.play()
        self.hit_count -= 1  # Decrement the hit counter
        if self.hit_count <= 0:  # Check if hit counter reaches zero
            self.clear_neighbours()
            self.kill()
            event = pygame.event.Event(Brick.BRICK_DESTROYED, value=self.value)
            pygame.event.post(event)
