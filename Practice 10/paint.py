import pygame
import math
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
# Состояние редактора
color = (0, 0, 0)
mode = 'brush' # 'brush', 'rect', 'circle', 'eraser'
start_pos = None
drawing = False
# Поверхность для рисования (чтобы фигуры не исчезали)
canvas = pygame.Surface((800, 600))
canvas.fill((255, 255, 255))
def get_rect(p1, p2):
    return pygame.Rect(min(p1[0], p2[0]), min(p1[1], p2[1]), abs(p1[0]-p2[0]), abs(p1[1]-p2[1]))
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: mode = 'rect'
            if event.key == pygame.K_c: mode = 'circle'
            if event.key == pygame.K_b: mode = 'brush'
            if event.key == pygame.K_e: mode = 'eraser'
            if event.key == pygame.K_1: color = (255, 0, 0)
            if event.key == pygame.K_2: color = (0, 255, 0)
            if event.key == pygame.K_3: color = (0, 0, 255)
            if event.key == pygame.K_0: color = (0, 0, 0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = mouse_pos
        if event.type == pygame.MOUSEBUTTONUP:
            if mode == 'rect':
                pygame.draw.rect(canvas, color, get_rect(start_pos, mouse_pos), 2)
            elif mode == 'circle':
                rad = int(math.hypot(mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
                pygame.draw.circle(canvas, color, start_pos, rad, 2)
            drawing = False
    if drawing:
        if mode == 'brush':
            pygame.draw.circle(canvas, color, mouse_pos, 3)
        elif mode == 'eraser':
            pygame.draw.circle(canvas, (255, 255, 255), mouse_pos, 15)
    screen.blit(canvas, (0, 0))
    # Предпросмотр фигуры во время рисования
    if drawing and mode in ['rect', 'circle']:
        if mode == 'rect':
            pygame.draw.rect(screen, color, get_rect(start_pos, mouse_pos), 2)
        elif mode == 'circle':
            rad = int(math.hypot(mouse_pos[0]-start_pos[0], mouse_pos[1]-start_pos[1]))
            pygame.draw.circle(screen, color, start_pos, rad, 2)
    # UI подсказка
    pygame.display.set_caption(f"Mode: {mode} | Color: {color} | R-Rect, C-Circle, B-Brush, E-Eraser, 1-2-3-Colors")
    pygame.display.flip()
    clock.tick(120)
pygame.quit()