import pygame
from player import MusicPlayer

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Music Player")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

MUSIC_PATH = r"C:\Users\acer\Documents\hefbvi\Practice 9\play\music"
player = MusicPlayer(MUSIC_PATH)

running = True
while running:
    screen.fill((40, 40, 40))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.pause()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.prev()
            elif event.key == pygame.K_q:
                running = False

    track_info = player.get_current_track()
    text_surf = font.render(f"Track: {track_info}", True, (255, 255, 255))
    screen.blit(text_surf, (50, 150))
    
    controls_text = "P: Play | S: Pause | N: Next | B: Back | Q: Quit"
    controls_surf = font.render(controls_text, True, (150, 150, 150))
    screen.blit(controls_surf, (50, 300))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()