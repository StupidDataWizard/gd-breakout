import pygame
import settings
#Test
class Ball(pygame.sprite.Sprite):

    BALL_SIZE = 7
    BALL_LOST = pygame.event.custom_type()

    def __init__(self, position, color, border: pygame.Rect, bricks: pygame.sprite.Group, paddle):
        super().__init__()

        # Set the image and rect for the position
        # No unneccessary book keeping, positon and size are stored in the rect
        self.image = pygame.Surface((Ball.BALL_SIZE, Ball.BALL_SIZE))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, color, self.rect)

        # The position defines the CENTER of the ball!
        self.rect.center = position

        self.color = color
        self.border = border
        self.bricks = bricks
        self.paddle = paddle

        # we store direction and speed as velocity vector
        # this is more efficient for the calculation of the
        # position changes in each frame
        self.velocity = pygame.Vector2(0,0)

        # Bounce sound
        self.bounce = pygame.mixer.Sound("bounce.wav")
        self.bounce.set_volume(0.5)


    def update(self, dt):
        # Old position to check for any collisions between old and new
        old = pygame.Rect(self.rect)
        # New position
        self.rect.center += self.velocity * dt
        # Bounding box of both position
        collision_area = old.union(self.rect)
        # Get all bricks within the collision area
        colliding_bricks = []
        for brick in self.bricks:
            if collision_area.colliderect(brick.rect):
                colliding_bricks.append(brick)
        # Find closest collision on line
        closest = None
        point = None
        distance = 10000
        origin = pygame.Vector2(old.center)
        for brick in colliding_bricks:
            clipped_line =  brick.rect.clipline(old.center, self.rect.center)
            if clipped_line:
                start, end = clipped_line
                d = origin.distance_squared_to(start)
                if d < distance:
                    closest = brick
                    point = start
                    distance = d
        # If we have a collision (it is possible that there is none)
        if closest:
            # Make point mutable
            point = list(point)
            if point[1] == closest.rect.bottom - 1 and "bottom" not in closest.neighbours:
                reflection = pygame.Vector2(1, -1)
                # Move away from brick 1 pixel
                point[1] += 1
            elif point[1] == closest.rect.top and "top" not in closest.neighbours:
                reflection = pygame.Vector2(1, -1)
                point[1] -= 1
            elif point[0] == closest.rect.left:
                reflection = pygame.Vector2(-1, 1)
                point[0] -= 1
            elif point[0] == closest.rect.right - 1:
                reflection = pygame.Vector2(-1, 1)
                point[0] += 1
            self.velocity = self.velocity.elementwise() * reflection.elementwise()
            self.rect.center = point
            closest.hit()

        # Check paddle collision
        # First check if we are below the paddle surface
        if self.rect.centery > self.paddle.rect.top:
            # if so, check, if we crossed the paddle
            clipped_line =  self.paddle.rect.clipline(old.center, self.rect.center)
            if clipped_line:
                start, end = clipped_line
                # if so, check if we hit it the ball with the paddle top
                if start[1] == self.paddle.rect.top:
                    # if so, we bounce the ball
                    if not settings.sfx_muted:
                        self.bounce.play()
                    self.velocity.y *= -1
                    self.rect.center = start

        # Check that ball is out
        if self.rect.centery >= self.border.bottom:
            self.kill()
            event = pygame.event.Event(Ball.BALL_LOST)
            pygame.event.post(event)

        # Check borders
        elif not self.border.collidepoint(self.rect.center):
            if not settings.sfx_muted:
                self.bounce.play()
            # Determine reflection
            if self.rect.centerx >= self.border.right or self.rect.centerx <= self.border.left:
                self.velocity.x *= -1
            else:
                self.velocity.y *= -1
            # Set ball back to where it left
            clipped_line =  self.border.clipline(origin, self.rect.center)
            if not clipped_line:
                # If the ball starts exactly at the border,
                # there is no clipped line.
                # So we set it back to its origin.
                self.rect.center = origin
            else:
                self.rect.center = clipped_line[1]


    def start(self, speed, direction):
        # A normalized vector in direction 0 (to the right)
        self.velocity = pygame.Vector2(1, 0)
        # Rotate in desired direction in degrees (clockwise)
        self.velocity.rotate_ip(direction)
        # Set the correct speed
        self.velocity *= speed




