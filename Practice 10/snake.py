import pygame
import random
import time
# Инициализация Pygame
pygame.init()
# Настройки цветов
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
# Размеры окна и блока змейки
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20
# Настройка дисплея
dis = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game: Levels & Score')
clock = pygame.time.Clock()
# Шрифты
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
def display_info(score, level):
    """Отображает текущий счет и уровень в углу экрана"""
    value = score_font.render("Score: " + str(score), True, YELLOW)
    lvl_value = score_font.render("Level: " + str(level), True, YELLOW)
    dis.blit(value, [0, 0])
    dis.blit(lvl_value, [WIDTH - 150, 0])
def draw_snake(block_size, snake_list):
    """Рисует змейку на экране"""
    for x in snake_list:
        pygame.draw.rect(dis, GREEN, [x[0], x[1], block_size, block_size])
def generate_food(snake_list):
    """Генерирует еду так, чтобы она не попала на тело змейки"""
    while True:
        food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
        food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE       
        # Проверяем, не находится ли еда внутри змейки
        if [food_x, food_y] not in snake_list:
            return food_x, food_y
def gameLoop():
    game_over = False
    game_close = False
    # Начальные координаты змейки
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1   
    score = 0
    level = 1
    speed = 10 # Начальная скорость
    foodx, foody = generate_food(snake_List)
    while not game_over:
        while game_close == True:
            dis.fill(BLUE)
            message = font_style.render("Game Over! Press C-Play Again or Q-Quit", True, RED)
            dis.blit(message, [WIDTH / 6, HEIGHT / 3])
            display_info(score, level)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0
        # 1. Проверка столкновения со стенами (Border Collision)
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True       
        x1 += x1_change
        y1 += y1_change
        dis.fill(BLACK)       
        # Рисуем еду
        pygame.draw.rect(dis, RED, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])       
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)     
        if len(snake_List) > Length_of_snake:
            del snake_List[0]
        # 2. Проверка столкновения змейки с собой
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True
        draw_snake(BLOCK_SIZE, snake_List)
        display_info(score, level)
        pygame.display.update()
        # 3. Проверка: съела ли змейка еду
        if x1 == foodx and y1 == foody:
            foodx, foody = generate_food(snake_List)
            Length_of_snake += 1
            score += 1 
            # 4. Переход на новый уровень каждые 3 очка
            if score % 3 == 0:
                level += 1
                speed += 1 # 5. Увеличение скорости
        clock.tick(speed)
    pygame.quit()
    quit()
gameLoop()