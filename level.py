import random


class Level:
    def __init__(self, level_number, total_bricks, hard_brick_percentage):
        self.level_number = level_number
        self.total_bricks = total_bricks
        self.hard_brick_percentage = hard_brick_percentage

    def generate_level_layout(self):
        n_hard_bricks = int(self.total_bricks * self.hard_brick_percentage)
        brick_types = ['hard'] * n_hard_bricks
        brick_types.extend(['normal'] * (self.total_bricks - n_hard_bricks))
        random.shuffle(brick_types)
        brick_types[random.randint(-14, -1)] = "special"
        return brick_types
