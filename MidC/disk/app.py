import pygame
import sys
from random import randint,random
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
# The definition of class CLS_disk
class CLS_disk(object):
    group = []
    def __init__(self, rect, color, speedX, speedY):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.speedX, self.speedY, self.accY = speedX, speedY, 0.02
        CLS_disk.group.append(self)

    def run(self):
        self.speedY += self.accY
        self.rect.x += self.speedX
        self.rect.y += self.speedY

    def draw(self, scr):
        pygame.draw.ellipse(scr, self.color, self.rect, 0)

# the definition of class CLS_gun
class CLS_gun(object):
    def __init__(self, x, y, r):
        self.x, self.y, self.r = x, y, r
        self.score = 0
        self.diskNum = 20
        self.bulletNum = 0
        self.fireTime = 0

    def update(self):
        self.fireTime *= (1-(pygame.time.get_ticks() - self.fireTime > 100))

    def draw(self, scr):
        self.update()
        x, y, r = self.x, self.y, self.r
        pygame.draw.circle(scr, (225, 225, 224), (x, y), r, 1)
        pygame.draw.circle(scr, (225, 225, 225), (x, y), int(r*0.4), 1)
        pygame.draw.line(scr, (225, 225, 225), (x-r, y), (x+r, y), 1)
        pygame.draw.line(scr, (225, 225, 225), (x, y-r), (x, y+1), 1)
        if self.fireTime > 0:
            pygame.draw.polygon(scr, (225, 0, 0), [
                                (x-int(r*0.4), y-4), (x-int(r*0.4), y+4),(x,y)], 0)
            pygame.draw.polygon(scr, (225, 0, 0), [
                                (x+int(r*0.4), y-4), (x-int(r*0.4), y-4),(x,y)], 0)

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

# run
pygame.init()
aData = [0x04,0x0a,0x11,0x11,0x1f,0x11,0x11,0x00]
brickData = [0xff,0x04,0x04,0x04,0xff,0x80,0x80,0x80]
brickColor = [[64,64,64],[225,127,80]]
brickScale = 4
treeData =[0x02,0x15,0x07,0x19,0x2e,0x1f,0xfb,0x6e]
treeColor = [[0,50,0],[0,120,0]]
treeScale = 4
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
pygame.mouse.set_visible(False)
gun = CLS_gun(SCREEN_WIDTH//2,SCREEN_HEIGHT//2,30)
t0 = pygame.time.get_ticks()
t1 = randint(0,3000)+3000
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and gun.bulletNum>0:
            gun.bulletNum-=1
            i=0
            gun.fireTime = pygame.time.get_ticks()
            while i<len(CLS_disk.group):
                d = CLS_disk.group[i]
                if d.rect.collidepoint(gun.x,gun.y):
                    CLS_disk.group.pop(i)
                    gun.score+=1
                    gun.diskNum+=2
                i+=1
        if event.type == pygame.MOUSEMOTION:
            gun.x,gun.y= event.pos
        if event.type == pygame.QUIT:
            pygame.quit()
    if pygame.time.get_ticks()-t0 > t1 and gun.diskNum>0:
        gun.diskNum -= 1
        gun.bulletNum = 2
        w = randint(40,80)
        h = w//2
        disk = CLS_disk((0,SCREEN_HEIGHT,w,h),(0,225,0),random()+1.5,random()-4.5)
        t0 = pygame.time.get_ticks()
        t1 = randint(0,3000)+3000
        if random()<0.3:
            disk = CLS_disk((SCREEN_WIDTH,SCREEN_HEIGHT,w,h),(255,0,0),random()-2.5,random()-4.5)
    screen.fill((0,0,225))
    for x in range(0,SCREEN_WIDTH,32):
        for y in range((SCREEN_HEIGHT//4)*3,SCREEN_HEIGHT,32):
            RT_draw(screen,brickData,brickColor,x,y,8,4)
    for x in range(0,SCREEN_WIDTH,32):
        for y in range(SCREEN_HEIGHT//2,SCREEN_HEIGHT//4*3,32):
            RT_draw(screen,treeData,treeColor,x,y,8,4)
    for disk in CLS_disk.group:
        disk.run()
        disk.draw(screen)
    gun.draw(screen)
    img = font.render('score:'+str(gun.score)+'     disks:'+str(gun.diskNum),True,(240,0,140))
    screen.blit(img,(0,0))
    pygame.display.update()
    clock.tick(300)