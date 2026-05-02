import pygame
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, color, width):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, 520)
        self.width = width
        self.hp = 3

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.move_ip(-7, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < self.width: self.rect.move_ip(7, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.image = pygame.Surface((40, 70))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.width = width
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(40, self.width-40), -100)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > 600: self.spawn()

class Coin(pygame.sprite.Sprite):
    def __init__(self, width):
        super().__init__()
        self.weight = random.randint(1, 5)
        size = 15 + (self.weight * 2)
        self.image = pygame.Surface((size, size))
        self.image.fill((255, 215, 0))
        self.rect = self.image.get_rect()
        self.width = width
        self.spawn()

    def spawn(self):
        self.rect.center = (random.randint(20, self.width-20), -50)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > 600: self.spawn()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, p_type):
        super().__init__()
        self.type = p_type
        self.image = pygame.Surface((25, 25))
        colors = {"Nitro": (0, 255, 0), "Shield": (0, 255, 255), "Repair": (255, 0, 255)}
        self.image.fill(colors[p_type])
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, 370), -50)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > 600: self.kill()