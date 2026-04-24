import pygame, sys
from pygame.locals import *
import random, time
# Инициализация Pygame
pygame.init()
# Настройки экрана и FPS
FPS = 60
FramePerSec = pygame.time.Clock()
# Цвета
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
# Параметры окна
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0  # Переменная для хранения собранных монет
# Настройка шрифтов для текста
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
# Создание окна
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        # Если у тебя нет картинки, можно заменить на Surface
        self.image = pygame.Surface((40, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Создаем монетку в виде желтого квадрата (или круга)
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        # Появляется в случайном месте дороги
        self.rect.center = (random.randint(20, SCREEN_WIDTH-20), 0)
    def move(self):
        self.rect.move_ip(0, SPEED)
        # Если монетка улетела за экран, она пересоздается сверху
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)
    def spawn_new(self):
        """Метод для перемещения монетки после того, как ее подобрали"""
        self.rect.top = 0
        self.rect.center = (random.randint(20, SCREEN_WIDTH - 20), 0)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((40, 70))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
# Создание объектов
P1 = Player()
E1 = Enemy()
C1 = Coin()
# Создание групп спрайтов для удобного управления
enemies = pygame.sprite.Group()
enemies.add(E1)
coins_group = pygame.sprite.Group()
coins_group.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    DISPLAYSURF.fill(WHITE)
    # Отображение счета и количества монет
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    coins_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 100, 10)) # Монетки в правом верхнем углу
    # Движение всех объектов
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    # Проверка столкновения с монеткой
    if pygame.sprite.spritecollideany(P1, coins_group):
        COINS += 1
        C1.spawn_new() # Перемещаем монетку обратно наверх
    # Проверка столкновения с врагом (Game Over)
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound(r'C:\Users\acer\Downloads\Fall in love again - Everything is romantic (TikTok Version) [muzce.com].mp3').play() # Можно добавить звук
          time.sleep(0.5)                   
          DISPLAYSURF.fill(RED)
          DISPLAYSURF.blit(game_over, (30,250))
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()        
    pygame.display.update()
    FramePerSec.tick(FPS)