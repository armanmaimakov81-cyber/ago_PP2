import pygame
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball Game")
clock = pygame.time.Clock()

red_ball = Ball(WIDTH // 2, HEIGHT // 2, 25, (255, 0, 0), WIDTH, HEIGHT)

running = True
while running:
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                red_ball.move("UP")
            elif event.key == pygame.K_DOWN:
                red_ball.move("DOWN")
            elif event.key == pygame.K_LEFT:
                red_ball.move("LEFT")
            elif event.key == pygame.K_RIGHT:
                red_ball.move("RIGHT")

    red_ball.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()