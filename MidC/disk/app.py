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

# run
pygame.init()
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
    screen.fill((0,0,0))
    for disk in CLS_disk.group:
        disk.run()
        disk.draw(screen)
    gun.draw(screen)
    img = font.render('score:'+str(gun.score)+'     disks:'+str(gun.diskNum),True,(240,0,140))
    screen.blit(img,(0,0))
    pygame.display.update()
    clock.tick(300)