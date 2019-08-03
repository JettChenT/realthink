import pygame,time,sys
SCREEN_WIDTH,SCREEN_HEIGHT=400,300
ETLED_WIDTH, ETLED_HEIGHT = 34,44
DOT_R = 3
STROKE_WIDTH,STROKE_HEIGHT = 16,12
DIGITAL_MASK=[0b00111111,0b00000110,0b01011011,0b01001111,0b01100110,0b01101101,0b01111101,0b00000111,\
    0b00000111,0b01101111,0b01110111,0b01111100,0b00111001,0b01011110,0b01111001,0b01110001]
class CLS_dgtled(object):
    def __init__(self,x,y):
        #init
        self.x,self.y = x,y
        self.w,self.h = ETLED_WIDTH,ETLED_HEIGHT
        self.posList = [(6,2),(21,7),(21,24),(6,36),(2,24),(2,7),(6,19),(29,39)]
    def draw(self,scr,mark):
        #drawing methond
        pygame.draw.rect(scr,(0,0,180),(self.x,self.y,self.w,self.h))
        bit= 1
        for i in range(8):
            c = (0,0,240)
            x0,y0 = self.x+self.posList[i][0],self.y+self.posList[i][1]
            x1, y1 = x0+STROKE_WIDTH,y0+STROKE_HEIGHT
            if mark & bit == bit:
                c = (240,240,240)
            bit *= 2
            if i in (0,3,6):
                pygame.draw.polygon(scr,c,[(x0,y0+2),(x0+2,y0),(x1-2,y0),(x1,y0+2),(x1,y0+3),(x1-2,y0+5),(x0+2,y0+5),(x0,y0+3)])
            elif i==7:
                pygame.draw.circle(scr,c,(x0,y0),DOT_R,0)
            else:
                pygame.draw.polygon(scr,c,
                                    [(x0+3,y0),(x0+5,y0+2),\
                                     (x0+2,y1),(x0,y1-2),\
                                     (x0,y0+2),(x0+2,y0)])
#main
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('DIGITAL LED')
clock = pygame.time.Clock()
dgt0 = CLS_dgtled(100,100)
dgt1 = CLS_dgtled(100+ETLED_WIDTH,100)
dgt2 = CLS_dgtled(100+ETLED_WIDTH*2,100)
pFlag,num,switch = 0,0,0
while True:
    num += 1
    if switch:
        dgt0.draw(screen,DIGITAL_MASK[num//256%16]+pFlag)
        dgt1.draw(screen,DIGITAL_MASK[num//16%16]+pFlag)
        dgt2.draw(screen,DIGITAL_MASK[num%16]+pFlag)
    else:
        dgt0.draw(screen,DIGITAL_MASK[num//100%10]+pFlag)
        dgt1.draw(screen,DIGITAL_MASK[num//10%10]+pFlag)
        dgt2.draw(screen,DIGITAL_MASK[num%16]+pFlag)
    pygame.display.update()
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if pygame.K_0<=event.key<=pygame.K_9:
                num = event.key-pygame.k_0
            elif event.key == pygame.K_PERIOD:
                pFlag = 128-pFlag
            elif event.key == pygame.K_s:
                switch= 1-switch
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.quit()
