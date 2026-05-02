import pygame
import sys
import json
import db
import random
from game import Snake, Food, PowerUp, BLOCK_SIZE

class Game:
    def __init__(self):
        pygame.init()
        # Инициализация микшера звуков
        pygame.mixer.init()
        
        self.W, self.H = 600, 400
        self.dis = pygame.display.set_mode((self.W, self.H))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("bahnschrift", 22)
        
        db.init_db()
        self.load_settings()
        self.load_sounds() # Загрузка аудиофайлов
        self.username = ""
        self.main_menu()

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f: 
                self.settings = json.load(f)
            if "color" not in self.settings:
                self.settings["color"] = [0, 255, 0]
        except: 
            self.settings = {"color": [0, 255, 0], "grid": True, "sound": True}

    def load_sounds(self):
        """Загрузка звуков с защитой от отсутствующих файлов"""
        try:
            self.eat_sound = pygame.mixer.Sound(r"C:\Users\acer\Downloads\munch-sound-effect.mp3")
            self.power_sound = pygame.mixer.Sound(r"C:\Users\acer\Downloads\01-power-up-mario.mp3")
            self.hurt_sound = pygame.mixer.Sound(r"C:\Users\acer\Downloads\uh-steve-minecraft-online-audio-converter.mp3")
        except FileNotFoundError:
            print("Предупреждение: Аудиофайлы не найдены. Звук отключен.")
            self.settings["sound"] = False

    def main_menu(self):
        while True:
            self.dis.fill((0, 0, 0))
            title = self.font.render(f"Enter Name: {self.username}_", True, (255, 255, 255))
            self.dis.blit(title, [self.W/4, self.H/3])
            self.dis.blit(self.font.render("1. Play  2. Leaderboard  3. Settings  Q. Quit", True, (255, 255, 102)), [self.W/8, self.H/2])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 and self.username: self.play()
                    elif event.key == pygame.K_2: self.leaderboard_screen()
                    elif event.key == pygame.K_3: self.settings_screen()
                    elif event.key == pygame.K_q: pygame.quit(); sys.exit()
                    elif event.key == pygame.K_BACKSPACE: self.username = self.username[:-1]
                    else:
                        if len(self.username) < 12 and event.unicode.isalnum():
                            self.username += event.unicode

    def play(self):
        best_score = db.sync_player(self.username)
        snake = Snake(self.settings["color"])
        score = 0
        level = 1
        speed = 10
        obstacles = []
        
        food = Food(self.W, self.H, (255, 0, 0), 1)
        food.spawn(snake.body, obstacles)
        poison = Food(self.W, self.H, (139, 0, 0), 0)
        poison.spawn(snake.body, obstacles)
        
        p_up = None
        speed_mod = 0
        effect_timer = 0

        while True:
            self.dis.fill((0, 0, 0))
            now = pygame.time.get_ticks()

            if self.settings["grid"]:
                for x in range(0, self.W, BLOCK_SIZE): pygame.draw.line(self.dis, (40, 40, 40), (x, 0), (x, self.H))
                for y in range(0, self.H, BLOCK_SIZE): pygame.draw.line(self.dis, (40, 40, 40), (0, y), (self.W, y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and snake.direction[0] == 0: snake.direction = [-BLOCK_SIZE, 0]
                    elif event.key == pygame.K_RIGHT and snake.direction[0] == 0: snake.direction = [BLOCK_SIZE, 0]
                    elif event.key == pygame.K_UP and snake.direction[1] == 0: snake.direction = [0, -BLOCK_SIZE]
                    elif event.key == pygame.K_DOWN and snake.direction[1] == 0: snake.direction = [0, BLOCK_SIZE]

            head = snake.move()

            # Столкновение
            if head[0] < 0 or head[0] >= self.W or head[1] < 0 or head[1] >= self.H or head in obstacles or head in snake.body[:-1]:
                if snake.shielded:
                    if self.settings["sound"]: self.hurt_sound.play()
                    snake.shielded = False
                    snake.body.pop()
                else: 
                    if self.settings["sound"]: self.hurt_sound.play()
                    break

            # Еда
            if head == food.pos:
                if self.settings["sound"]: self.eat_sound.play()
                score += food.weight
                food.spawn(snake.body, obstacles)
                if score % 5 == 0:
                    level += 1
                    speed += 2
                    if level >= 3:
                        new_obs = [random.randrange(0, self.W//20)*20, random.randrange(0, self.H//20)*20]
                        if new_obs not in snake.body: obstacles.append(new_obs)
            else:
                snake.body.pop(0)

            # Яд
            if head == poison.pos:
                if self.settings["sound"]: self.hurt_sound.play()
                for _ in range(2):
                    if len(snake.body) > 1: snake.body.pop(0)
                    else: break
                if len(snake.body) <= 1: break
                poison.spawn(snake.body, obstacles)

            # Бонусы
            if not p_up and random.randint(1, 100) == 1:
                p_up = PowerUp(self.W, self.H, random.choice(['speed', 'slow', 'shield']))
                p_up.spawn(snake.body, obstacles)
            
            if p_up:
                if now - p_up.spawn_time > p_up.lifetime: p_up = None
                elif head == p_up.pos:
                    if self.settings["sound"]: self.power_sound.play()
                    if p_up.type == 'speed': speed_mod = 10; effect_timer = now + 5000
                    elif p_up.type == 'slow': speed_mod = -5; effect_timer = now + 5000
                    elif p_up.type == 'shield': snake.shielded = True
                    p_up = None

            if now > effect_timer: speed_mod = 0

            # Отрисовка
            food.draw(self.dis)
            poison.draw(self.dis)
            if p_up: p_up.draw(self.dis)
            for obs in obstacles: pygame.draw.rect(self.dis, (100, 100, 100), [obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE])
            for block in snake.body:
                color = snake.color if not snake.shielded else (255, 255, 255)
                pygame.draw.rect(self.dis, color, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

            self.dis.blit(self.font.render(f"Score: {score} Lvl: {level} Best: {best_score}", True, (255, 255, 255)), [5, 5])
            pygame.display.update()
            self.clock.tick(speed + speed_mod)

        db.save_result(self.username, score, level)
        self.main_menu()

    def leaderboard_screen(self):
        while True:
            self.dis.fill((0, 0, 0))
            self.dis.blit(self.font.render("TOP 10 SCORES", True, (255, 255, 102)), [self.W/3, 20])
            data = db.get_top_10()
            for i, row in enumerate(data):
                txt = f"{i+1}. {row[0]} - {row[1]} (Lvl {row[2]}) | {row[3]}"
                self.dis.blit(self.font.render(txt, True, (255, 255, 255)), [50, 60 + i*30])
            self.dis.blit(self.font.render("B - Back", True, (255, 0, 0)), [self.W/2 - 30, 360])
            pygame.display.update()
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN and e.key == pygame.K_b: return
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()

    def settings_screen(self):
        while True:
            self.dis.fill((0, 0, 0))
            self.dis.blit(self.font.render("SETTINGS", True, (255, 255, 102)), [self.W/2 - 40, 50])
            self.dis.blit(self.font.render(f"1. Grid: {'ON' if self.settings['grid'] else 'OFF'}", True, (255, 255, 255)), [100, 120])
            self.dis.blit(self.font.render(f"2. Sound: {'ON' if self.settings['sound'] else 'OFF'}", True, (255, 255, 255)), [100, 160])
            self.dis.blit(self.font.render(f"3. Change Color (Random)", True, (255, 255, 255)), [100, 200])
            self.dis.blit(self.font.render("B - Back and Save", True, (0, 255, 0)), [100, 280])
            pygame.display.update()
            for e in pygame.event.get():
                if e.type == pygame.QUIT: pygame.quit(); sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_1: self.settings["grid"] = not self.settings["grid"]
                    elif e.key == pygame.K_2: self.settings["sound"] = not self.settings["sound"]
                    elif e.key == pygame.K_3: self.settings["color"] = [random.randint(50, 255) for _ in range(3)]
                    elif e.key == pygame.K_b:
                        with open('settings.json', 'w') as f: json.dump(self.settings, f)
                        return

if __name__ == "__main__":
    Game()