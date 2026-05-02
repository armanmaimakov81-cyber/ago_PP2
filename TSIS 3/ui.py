import pygame

# Определяем цвета здесь, чтобы импортировать их в main
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font_big = pygame.font.SysFont("Verdana", 50)
        self.font_med = pygame.font.SysFont("Verdana", 30)
        self.font_small = pygame.font.SysFont("Verdana", 18)

    def draw_text(self, text, pos, size="small", color=BLACK):
        if size == "med": font = self.font_med
        elif size == "big": font = self.font_big
        else: font = self.font_small
        render = font.render(str(text), True, color)
        self.screen.blit(render, pos)

    def draw_menu(self):
        self.screen.fill(WHITE)
        self.draw_text("RACER PRO", (60, 100), "big", BLUE)
        self.draw_text("1. Play", (100, 250), "med")
        self.draw_text("2. Settings", (100, 320), "med")
        self.draw_text("3. Leaderboard", (100, 390), "med")
        self.draw_text("Q. Quit", (100, 460), "med", RED)