import pygame, sys
from pygame.locals import *
import random, time
pygame.init()
FPS = 60
FramePerSec = pygame.time.Clock()
BLUE, RED, GREEN, BLACK, WHITE, YELLOW = (0, 0, 255), (255, 0, 0), (0, 255, 0), (0, 0, 0), (255, 255, 255), (255, 255, 0)
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
SPEED, SCORE, COINS = 5, 0, 0
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)
DISPLAYSURF = pygame.display.set_mode((400,600))
pygame.display.set_caption("Game")
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
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
        self.spawn_new()
    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600): self.spawn_new()
    def spawn_new(self):
        self.weight = random.randint(1, 5)
        size = 15 + (self.weight * 3)
        self.image = pygame.Surface((size, size))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(20, SCREEN_WIDTH-20), 0)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((40, 70))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]: self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]: self.rect.move_ip(5, 0)
P1, E1, C1 = Player(), Enemy(), Coin()
enemies, coins_group, all_sprites = pygame.sprite.Group(E1), pygame.sprite.Group(C1), pygame.sprite.Group(P1, E1, C1)
while True:
    for event in pygame.event.get():
        if event.type == QUIT: pygame.quit(); sys.exit()
    DISPLAYSURF.fill(WHITE)
    scores = font_small.render("Score: " + str(SCORE), True, BLACK)
    coins_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_text, (SCREEN_WIDTH - 100, 10))
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    collided_coin = pygame.sprite.spritecollideany(P1, coins_group)
    if collided_coin:
        old_coins = COINS
        COINS += collided_coin.weight
        if (COINS // 10) > (old_coins // 10): SPEED += 1
        collided_coin.spawn_new() 
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound(r'C:\Users\acer\Downloads\Fall in love again - Everything is romantic (TikTok Version) [muzce.com].mp3').play()
          time.sleep(0.5); DISPLAYSURF.fill(RED); DISPLAYSURF.blit(game_over, (30,250)); pygame.display.update()
          for entity in all_sprites: entity.kill() 
          time.sleep(2); pygame.quit(); sys.exit()        
    pygame.display.update()
    FramePerSec.tick(FPS)