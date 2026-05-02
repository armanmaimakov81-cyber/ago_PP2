import pygame
import random

BLOCK_SIZE = 20

class Food:
    def __init__(self, width, height, color, weight, lifetime=None):
        self.width, self.height = width, height
        self.color = color
        self.weight = weight
        self.lifetime = lifetime # в миллисекундах
        self.spawn_time = 0
        self.pos = [0, 0]

    def spawn(self, snake_body, obstacles):
        while True:
            self.pos = [
                random.randrange(0, (self.width // BLOCK_SIZE)) * BLOCK_SIZE,
                random.randrange(0, (self.height // BLOCK_SIZE)) * BLOCK_SIZE
            ]
            if self.pos not in snake_body and self.pos not in obstacles:
                break
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, [self.pos[0], self.pos[1], BLOCK_SIZE, BLOCK_SIZE])

class PowerUp(Food):
    def __init__(self, width, height, p_type):
        colors = {'speed': (0, 0, 255), 'slow': (0, 255, 255), 'shield': (255, 255, 255)}
        super().__init__(width, height, colors[p_type], 0, 8000) # Исчезает через 8 сек
        self.type = p_type

class Snake:
    def __init__(self, color):
        self.body = [[100, 100]]
        self.direction = [BLOCK_SIZE, 0]
        self.color = color
        self.shielded = False

    def move(self):
        new_head = [self.body[-1][0] + self.direction[0], self.body[-1][1] + self.direction[1]]
        self.body.append(new_head)
        return new_head