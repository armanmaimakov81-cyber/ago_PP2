import pygame
import random
import time
# Инициализация Pygame
pygame.init()
# Цвета
WHITE, YELLOW, BLACK, RED, GREEN, BLUE = (255, 255, 255), (255, 255, 102), (0, 0, 0), (213, 50, 80), (0, 255, 0), (50, 153, 213)
# Размеры
WIDTH, HEIGHT, BLOCK_SIZE = 600, 400, 20
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game: Food Weights & Timers')
clock = pygame.time.Clock()
# Шрифты
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
def display_score(score):
    value = score_font.render("Score: " + str(score), True, YELLOW)
    dis.blit(value, [0, 0])
def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])
class Food:
    def __init__(self, snake_list):
        self.spawn(snake_list)
    def spawn(self, snake_list):
        # Генерация случайного веса от 1 до 3
        self.weight = random.randint(1, 3)
        # Установка таймера жизни еды (например, 5 секунд)
        self.spawn_time = time.time()
        self.lifetime = 5 
        while True:
            self.x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            self.y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            if [self.x, self.y] not in snake_list: break
    def is_expired(self):
        # Проверка, не вышло ли время жизни еды
        return time.time() - self.spawn_time > self.lifetime
    def draw(self):
        # Цвет еды зависит от веса (чем тяжелее, тем насыщеннее)
        color = (255, 100, 100) if self.weight == 1 else (255, 50, 50) if self.weight == 2 else RED
        pygame.draw.rect(dis, color, [self.x, self.y, BLOCK_SIZE, BLOCK_SIZE])
def gameLoop():
    game_over, game_close = False, False
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0
    snake_List = []
    Length_of_snake = 1
    score = 0
    food = Food(snake_List)
    while not game_over:
        while game_close == True:
            dis.fill(BLUE)
            msg = font_style.render("Game Over! Press C-Play Again or Q-Quit", True, RED)
            dis.blit(msg, [WIDTH / 6, HEIGHT / 3])
            display_score(score)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: game_over, game_close = True, False
                    if event.key == pygame.K_c: gameLoop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0: x1_change, y1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and x1_change == 0: x1_change, y1_change = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and y1_change == 0: y1_change, x1_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_DOWN and y1_change == 0: y1_change, x1_change = BLOCK_SIZE, 0
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0: game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)
        # Проверка таймера еды: если время вышло, спавним новую в другом месте
        if food.is_expired(): food.spawn(snake_List)
        food.draw()
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake: del snake_List[0]
        for x in snake_List[:-1]:
            if x == snake_Head: game_close = True
        draw_snake(snake_List)
        display_score(score)
        pygame.display.update()
        # Проверка поедания еды
        if x1 == food.x and y1 == food.y:
            score += food.weight
            Length_of_snake += food.weight # Змейка растет на величину веса еды
            food.spawn(snake_List)
        clock.tick(15)
    pygame.quit()
    quit()
gameLoop()