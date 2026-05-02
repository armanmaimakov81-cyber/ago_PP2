import pygame, sys, time, random
from persistence import load_data, save_data
from ui import UI, RED, WHITE, BLACK, BLUE, GREY
from racer import Player, Enemy, PowerUp, Coin

# --- ИНИЦИАЛИЗАЦИЯ ---
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Pro 2026")
clock = pygame.time.Clock()
ui = UI(screen)

# --- ЗАГРУЗКА ЗВУКОВ ---
try:
    sfx_coin = pygame.mixer.Sound(r"C:\Users\acer\Downloads\super-mario-coin-sound.mp3")
    sfx_hit = pygame.mixer.Sound(r"C:\Users\acer\Downloads\sike-1.mp3")
    sfx_powerup = pygame.mixer.Sound(r"C:\Users\acer\Downloads\01-power-up-mario.mp3")
    pygame.mixer.music.load(r"C:\Users\acer\Downloads\untitled_3.mp3")
except Exception as e:
    print(f"Предупреждение: Звуковые файлы не найдены ({e}). Играем в тишине.")
    sfx_coin = sfx_hit = sfx_powerup = None

# --- ЗАГРУЗКА НАСТРОЕК ---
raw_settings = load_data("settings.json", {})
settings = {
    "difficulty": raw_settings.get("difficulty", "Normal"),
    "car_color": raw_settings.get("car_color", [0, 0, 255]),
    "sound": raw_settings.get("sound", True),
    "username": raw_settings.get("username", "Player")
}

def play_sfx(sound):
    if settings["sound"] and sound:
        sound.play()

def username_entry_screen():
    """Экран ввода имени перед началом игры."""
    user_text = ""
    entering = True
    while entering:
        screen.fill(WHITE)
        ui.draw_text("ENTER YOUR NAME:", (60, 200), "med", BLUE)
        
        # Рисуем рамку для ввода
        pygame.draw.rect(screen, BLACK, (100, 250, 200, 40), 2)
        ui.draw_text(user_text, (110, 255), "med", BLACK)
        ui.draw_text("Press ENTER to Start", (110, 350), "small", GREY)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_text.strip() != "":
                        settings["username"] = user_text
                    entering = False
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    if len(user_text) < 10: # Ограничение длины
                        user_text += event.unicode
        clock.tick(60)

def game_over_screen(current_score):
    while True:
        screen.fill(RED)
        ui.draw_text("GAME OVER", (60, 200), "big", WHITE)
        ui.draw_text(f"Your Score: {current_score}", (100, 300), "med", WHITE)
        ui.draw_text("Press M for Menu", (110, 400), color=WHITE)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m: return
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

def leaderboard_screen():
    data = load_data("leaderboard.json", [])
    while True:
        screen.fill(WHITE)
        ui.draw_text("TOP 10", (130, 50), "big", RED)
        if not data:
            ui.draw_text("No scores yet", (100, 250), "med", GREY)
        else:
            for i, e in enumerate(data[:10]):
                ui.draw_text(f"{i+1}. {e['name']}: {e['score']}", (80, 130 + i*35))
        ui.draw_text("Press B to Back", (110, 530), color=GREY)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b: return
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

def settings_screen():
    while True:
        screen.fill(WHITE)
        ui.draw_text("SETTINGS", (100, 50), "big")
        ui.draw_text(f"1. Difficulty: {settings['difficulty']}", (50, 200), "med")
        ui.draw_text("2. Change Color", (50, 270), "med")
        pygame.draw.rect(screen, settings['car_color'], (300, 275, 40, 20))
        ui.draw_text(f"3. Sound: {'ON' if settings['sound'] else 'OFF'}", (50, 340), "med")
        ui.draw_text("B. Save & Back", (50, 450), color=GREY)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    d = ["Easy", "Normal", "Hard"]
                    settings["difficulty"] = d[(d.index(settings["difficulty"]) + 1) % 3]
                if event.key == pygame.K_2:
                    colors = [[0,0,255], [0,255,0], [255,0,0], [0,0,0]]
                    settings["car_color"] = colors[(colors.index(settings["car_color"]) + 1) % 4]
                if event.key == pygame.K_3: 
                    settings["sound"] = not settings["sound"]
                if event.key == pygame.K_b:
                    save_data("settings.json", settings)
                    return
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

def game_loop():
    # Сначала спрашиваем имя
    username_entry_screen()
    
    if settings["sound"]:
        pygame.mixer.music.play(-1)

    speed = {"Easy": 4, "Normal": 6, "Hard": 9}[settings["difficulty"]]
    score, coins_count, distance = 0, 0, 0
    
    player = Player(settings["car_color"], WIDTH)
    enemies = pygame.sprite.Group(Enemy(WIDTH))
    coins = pygame.sprite.Group(Coin(WIDTH))
    powerups = pygame.sprite.Group()
    
    shield_end, nitro_end = 0, 0
    running = True

    while running:
        screen.fill(WHITE)
        distance += speed * 0.01
        
        ui.draw_text(f"Pilot: {settings['username']}", (10, 60), color=GREY) # Отображение имени
        ui.draw_text(f"Score: {score}  Coins: {coins_count}", (10, 10))
        ui.draw_text(f"HP: {player.hp}  Dist: {int(distance)}m", (10, 35))
        
        if time.time() < shield_end:
            ui.draw_text("SHIELD ACTIVE", (220, 10), color=BLUE)
        if time.time() < nitro_end:
            ui.draw_text("NITRO BOOST", (220, 35), color=(0, 255, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.mixer.music.stop()
                pygame.quit(); sys.exit()
        
        player.move()
        for sprite in enemies: sprite.move(speed)
        for sprite in coins: sprite.move(speed)
        for sprite in powerups: sprite.move(speed)

        if random.randint(1, 150) == 1:
            powerups.add(PowerUp(random.choice(["Nitro", "Shield", "Repair"])))

        for sprite in coins: screen.blit(sprite.image, sprite.rect)
        for sprite in powerups: screen.blit(sprite.image, sprite.rect)
        for sprite in enemies: screen.blit(sprite.image, sprite.rect)
        screen.blit(player.image, player.rect)

        c_hit = pygame.sprite.spritecollideany(player, coins)
        if c_hit:
            play_sfx(sfx_coin)
            coins_count += c_hit.weight
            score += c_hit.weight * 5
            c_hit.spawn()
            if coins_count > 0 and coins_count % 10 == 0:
                speed += 0.5

        p_hit = pygame.sprite.spritecollideany(player, powerups)
        if p_hit:
            play_sfx(sfx_powerup)
            if p_hit.type == "Nitro":
                speed += 5
                nitro_end = time.time() + 3
            elif p_hit.type == "Shield":
                shield_end = time.time() + 6
            elif p_hit.type == "Repair":
                player.hp = min(3, player.hp + 1)
            p_hit.kill()

        if nitro_end != 0 and time.time() > nitro_end:
            speed -= 5
            nitro_end = 0

        if pygame.sprite.spritecollideany(player, enemies):
            if time.time() < shield_end:
                shield_end = 0 
                play_sfx(sfx_hit)
                for e in enemies: e.spawn()
            else:
                play_sfx(sfx_hit)
                player.hp -= 1
                time.sleep(0.3)
                for e in enemies: e.spawn()
                if player.hp <= 0:
                    pygame.mixer.music.stop()
                    running = False

        pygame.display.update()
        clock.tick(60)
    
    leaderboard = load_data("leaderboard.json", [])
    leaderboard.append({"name": settings["username"], "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x['score'], reverse=True)[:10]
    save_data("leaderboard.json", leaderboard)
    
    game_over_screen(score)

def main_menu():
    while True:
        ui.draw_menu()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: game_loop()
                if event.key == pygame.K_2: settings_screen()
                if event.key == pygame.K_3: leaderboard_screen()
                if event.key == pygame.K_q: pygame.quit(); sys.exit()
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()

if __name__ == "__main__":
    main_menu()