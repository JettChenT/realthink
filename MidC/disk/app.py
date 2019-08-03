import pygame,sys,random
SCREEN_WIDTH,SCREEN_HEIGHT = 1024,768
# The definition of class CLS_disk
class CLS_disk(object):
    group = []
    def __init__(self,rect,color,speedX,speedY):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.speedX,self.speedY,self.accY = speedX,speedY,0.02
        CLS_disk.group.append(self)
    def run(self):
        self.speedY += self.accY
        self.rect.x += self.speedX
        self.rect.y += self.speedY
    def draw(self,scr):
        pygame.draw.ellipse(scr,self.color,self.rect,0)

class CLS_gun(object):
    def __init__(self,x,y,r):
        self.x,self.y,self.r = x,y,r
        self.score = 0
        self.diskNum = 20
        self.bulletNum = 0
        self.fireTime = 0
    def update(self):
        self.fireTime*=(1-(pygame.time.get_ticks() - self.fireTime>100))
    def draw(self,scr):
        self.update()
        s,y,r = self.x,self.y,self.r