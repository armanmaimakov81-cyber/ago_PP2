import pygame, math
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
color, mode, start_pos, drawing = (0, 0, 0), 'brush', None, False
canvas = pygame.Surface((800, 600))
canvas.fill((255, 255, 255))
def draw_shape(surf, color, start, end, mode, width=2):
    x1, y1, x2, y2 = start[0], start[1], end[0], end[1]
    dx, dy = x2 - x1, y2 - y1
    if mode == 'rect': pygame.draw.rect(surf, color, (min(x1, x2), min(y1, y2), abs(dx), abs(dy)), width)
    elif mode == 'circle':
        rad = int(math.hypot(dx, dy))
        pygame.draw.circle(surf, color, (x1, y1), rad, width)
    elif mode == 'square':
        side = max(abs(dx), abs(dy))
        pygame.draw.rect(surf, color, (x1 if x2 > x1 else x1 - side, y1 if y2 > y1 else y1 - side, side, side), width)
    elif mode == 'right_tri': pygame.draw.polygon(surf, color, [(x1, y1), (x1, y2), (x2, y2)], width)
    elif mode == 'equi_tri':
        h = dx * math.sqrt(3) / 2
        pygame.draw.polygon(surf, color, [(x1, y1), (x1 + dx, y1), (x1 + dx/2, y1 - h)], width)
    elif mode == 'rhombus': pygame.draw.polygon(surf, color, [(x1 + dx/2, y1), (x2, y1 + dy/2), (x1 + dx/2, y2), (x1, y1 + dy/2)], width)
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            # Смена инструментов
            if event.key == pygame.K_r: mode = 'rect'
            if event.key == pygame.K_c: mode = 'circle'
            if event.key == pygame.K_b: mode = 'brush'
            if event.key == pygame.K_e: mode = 'eraser'
            if event.key == pygame.K_s: mode = 'square'
            if event.key == pygame.K_t: mode = 'right_tri'
            if event.key == pygame.K_q: mode = 'equi_tri'
            if event.key == pygame.K_h: mode = 'rhombus'
            # Смена ЦВЕТА (добавил сюда)
            if event.key == pygame.K_1: color = (255, 0, 0) # Красный
            if event.key == pygame.K_2: color = (0, 255, 0) # Зеленый
            if event.key == pygame.K_3: color = (0, 0, 255) # Синий
            if event.key == pygame.K_0: color = (0, 0, 0)   # Черный
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing, start_pos = True, mouse_pos
        if event.type == pygame.MOUSEBUTTONUP:
            if mode not in ['brush', 'eraser']: draw_shape(canvas, color, start_pos, mouse_pos, mode)
            drawing = False
    if drawing:
        if mode == 'brush': pygame.draw.circle(canvas, color, mouse_pos, 3)
        elif mode == 'eraser': pygame.draw.circle(canvas, (255, 255, 255), mouse_pos, 15)
    screen.blit(canvas, (0, 0))
    if drawing and mode not in ['brush', 'eraser']: draw_shape(screen, color, start_pos, mouse_pos, mode)
    pygame.display.set_caption(f"Mode: {mode} | Color: {color} | Keys: 1,2,3,0 for Colors")
    pygame.display.flip()
    clock.tick(60)
pygame.quit()