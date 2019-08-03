import pygame,sys
SCREEN_WIDTH,SCREEN_HEIGHT = 1024,768

def RT_draw(screen,data,clrList,x0,y0,w,scale):
    for dy in range(len(data)):
        line = data[dy]
        for dx in range(w):
            clr  = clrList[line&1]
            tx,ty = x0+(w-dx-1)*scale,y0+dy*scale
            if scale > 1:
                pygame.draw.rect(screen,clr,(tx,ty,scale,scale),0)
            else:
                screen.set_at((s,y),clr)
            line = line >>1
    return
# main program
pygame.init()
screen = pygame.display.set_mode((1024,768))
aData = [0x04,0x0a,0x11,0x11,0x1f,0x11,0x11,0x00]
brickData = [0xff,0x04,0x04,0x04,0xff,0x80,0x80,0x80]
brickColor = [[64,64,64],[225,127,80]]
brickScale = 4
treeData =[0x02,0x15,0x07,0x19,0x2e,0x1f,0xfb,0x6e]
treeColor = [[0,50,0],[0,120,0]]
treeScale = 4
while True:
    screen.fill((0,0,225))
    RT_draw(screen,aData,((0,0,0),(240,240,240)),100,200,8,10)
    RT_draw(screen,brickData,brickColor,300,200,7,10)
    RT_draw(screen,treeData,treeColor,500,200,8,10)
    pygame.display.update()
    pygame.event.get()