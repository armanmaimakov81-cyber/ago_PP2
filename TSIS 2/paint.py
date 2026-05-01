import pygame,datetime
from tools import *

pygame.init()

screen=pygame.display.set_mode((800,600))
clock=pygame.time.Clock()

canvas=pygame.Surface((800,600))
canvas.fill((255,255,255))

temp=pygame.Surface((800,600),pygame.SRCALPHA)

font=pygame.font.SysFont("Arial",20)

color=(0,0,0)
mode='brush'
size=2

start=None
last=None
drawing=False

text_mode=False
text=""
text_pos=None

running=True

while running:

    mouse=pygame.mouse.get_pos()
    temp.fill((0,0,0,0))

    for event in pygame.event.get():

        if event.type==pygame.QUIT:
            running=False

        if event.type==pygame.KEYDOWN:

            # BRUSH SIZE
            if event.key==pygame.K_1: size=2
            if event.key==pygame.K_2: size=5
            if event.key==pygame.K_3: size=10

            # TOOLS
            if not text_mode:
                if event.key==pygame.K_r: mode='rect'
                if event.key==pygame.K_c: mode='circle'
                if event.key==pygame.K_b: mode='brush'
                if event.key==pygame.K_e: mode='eraser'
                if event.key==pygame.K_s: mode='square'
                if event.key==pygame.K_t: mode='right_tri'
                if event.key==pygame.K_q: mode='equi_tri'
                if event.key==pygame.K_h: mode='rhombus'
                if event.key==pygame.K_l: mode='line'
                if event.key==pygame.K_f: mode='fill'

                if event.key==pygame.K_x:
                    text_mode=True
                    text=""
                    text_pos=mouse

            # SAVE (CTRL+S)
            if event.key==pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                import os
                os.makedirs("saves",exist_ok=True)
                name="saves/"+datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+".png"
                pygame.image.save(canvas,name)
                print("saved:",name)

            # TEXT MODE
            if text_mode:
                if event.key==pygame.K_RETURN:
                    img=font.render(text,True,color)
                    canvas.blit(img,text_pos)
                    text_mode=False

                elif event.key==pygame.K_ESCAPE:
                    text_mode=False

                elif event.key==pygame.K_BACKSPACE:
                    text=text[:-1]

                else:
                    if event.unicode.isprintable():
                        text+=event.unicode

        if event.type==pygame.MOUSEBUTTONDOWN:
            start=mouse
            last=mouse
            drawing=True

            if mode=='fill':
                target=canvas.get_at(mouse)[:3]
                flood_fill(canvas,mouse[0],mouse[1],target,color)

        if event.type==pygame.MOUSEBUTTONUP:
            drawing=False

            if mode in ['rect','circle','square','right_tri','equi_tri','rhombus','line']:
                draw_shape(canvas,color,start,mouse,mode,size)

    # PENCIL
    if drawing and mode=='brush':
        brush(canvas,color,last,mouse,size)
        last=mouse

    # ERASER
    if drawing and mode=='eraser':
        eraser(canvas,last,mouse,size)
        last=mouse

    # PREVIEW LINE/SHAPES
    if drawing and mode in ['rect','circle','square','right_tri','equi_tri','rhombus','line']:
        draw_shape(temp,color,start,mouse,mode,size)

    screen.blit(canvas,(0,0))
    screen.blit(temp,(0,0))

    # TEXT PREVIEW
    if text_mode:
        txt=font.render(text,True,color)
        screen.blit(txt,mouse)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
