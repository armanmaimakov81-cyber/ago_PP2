import pygame, math

def draw_shape(surf,color,start,end,mode,width):
    x1,y1=start
    x2,y2=end
    dx,dy=x2-x1,y2-y1

    if mode=='rect':
        pygame.draw.rect(surf,color,(min(x1,x2),min(y1,y2),abs(dx),abs(dy)),width)

    elif mode=='circle':
        r=int(math.hypot(dx,dy))
        pygame.draw.circle(surf,color,(x1,y1),r,width)

    elif mode=='square':
        s=max(abs(dx),abs(dy))
        x=x1 if x2>x1 else x1-s
        y=y1 if y2>y1 else y1-s
        pygame.draw.rect(surf,color,(x,y,s,s),width)

    elif mode=='right_tri':
        pygame.draw.polygon(surf,color,[(x1,y1),(x1,y2),(x2,y2)],width)

    elif mode=='equi_tri':
        h=abs(dx)*math.sqrt(3)/2
        pygame.draw.polygon(surf,color,[(x1,y1),(x2,y1),(x1+dx/2,y1-h)],width)

    elif mode=='rhombus':
        pygame.draw.polygon(surf,color,[
            (x1+dx/2,y1),
            (x2,y1+dy/2),
            (x1+dx/2,y2),
            (x1,y1+dy/2)
        ],width)

    elif mode=='line':
        pygame.draw.line(surf,color,start,end,width)


def brush(canvas,color,last,now,size):
    if last:
        pygame.draw.line(canvas,color,last,now,size)


def eraser(canvas,last,now,size):
    if last:
        pygame.draw.line(canvas,(255,255,255),last,now,size)


def flood_fill(surf,x,y,target,color):
    if target==color:
        return

    w,h=surf.get_size()
    stack=[(x,y)]

    while stack:
        px,py=stack.pop()

        if 0<=px<w and 0<=py<h:
            if surf.get_at((px,py))[:3]==target:
                surf.set_at((px,py),color)
                stack.extend([(px+1,py),(px-1,py),(px,py+1),(px,py-1)])
