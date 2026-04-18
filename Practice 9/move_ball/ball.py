import pygame

class Ball:
    def __init__(self, x, y, radius, color, screen_width, screen_height):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.step = 20

    def move(self, direction):
        if direction == "UP" and self.y - self.step >= self.radius:
            self.y -= self.step
        elif direction == "DOWN" and self.y + self.step <= self.screen_height - self.radius:
            self.y += self.step
        elif direction == "LEFT" and self.x - self.step >= self.radius:
            self.x -= self.step
        elif direction == "RIGHT" and self.x + self.step <= self.screen_width - self.radius:
            self.x += self.step

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)