import pygame,sys
SCREEN_WIDTH,SCREEN_HEIGHT = 1024,768
fname = input('name of the file(default:demo.txt): ')
d =  eval(input('width of the picture(default:32):'))
if fname == '':
    fname = 'demo.txt'
if d == None:
    d = 32
def RT_draw(screen,data,clrList,x0,y0,w,scale):
    for dy in range(len(data)):
        line = data[dy]
        for dx in range(w):
            clr  = clrList[line&1]
            tx,ty = x0+(w-dx-1)*scale,y0+dy*scale
            if scale > 1:
                pygame.draw.rect(screen,clr,(tx,ty,scale,scale),0)
            else:
                screen.set_at((x,y),clr)
            line = line >>1
    return
def RT_read(fn):
    with open (fn,'r') as f:
        txtLine = f.readlines()[0]
        dataList = txtLine.split()
        block = [int(dataList[p],16) for p in range(len(dataList))]
    return block
# main program
pygame.init()
screen = pygame.display.set_mode((1024,768))
block = RT_read(fname)
while True:
    screen.fill((0,0,225))
    # RT_draw(screen,aData,((0,0,0),(240,240,240)),100,200,8,10)
    # RT_draw(screen,brickData,brickColor,300,200,7,10)
    # RT_draw(screen,treeData,treeColor,500,200,8,10)
    RT_draw(screen,block,[(225,225,225),(0,0,0)],0,0,d,10)
    pygame.display.update()
    pygame.event.get()
