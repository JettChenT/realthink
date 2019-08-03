import pygame,time,sys,datetime
SCREEN_WIDTH,SCREEN_HEIGHT=136,44
ETLED_WIDTH, ETLED_HEIGHT = 34,44
DOT_R = 3
STROKE_WIDTH,STROKE_HEIGHT = 16,12
DIGITAL_MASK=[0b00111111,0b00000110,0b01011011,0b01001111,0b01100110,0b01101101,0b01111101,0b01111111,\
    0b00000111,0b01101111,0b01110111,0b01111100,0b00111001,0b01011110,0b10111111,0b10000110,\
        0b11011011,0b11001111,0b11100110,0b11101101,0b11111101,0b11111111,0b10000111,0b11101111,0b11110111,0b11111100,\
            0b10111001,0b11011110,0b11111001,0b11110001,0b11011110]
date = str(datetime.date.today()).split('-')
y = int(date[0])
month = int(date[1])
day = int(date[2])
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
                pygame.draw.polygon(scr,c,[(x0,y0+2),(x0+2,y0),(x1-2,y0),(x1,y0+2),\
                    (x1,y0+3),(x1-2,y0+5),(x0+2,y0+5),(x0,y0+3)])
            elif i==7:
                pygame.draw.circle(scr,c,(x0,y0-5),DOT_R,0)
                pygame.draw.circle(scr,c,(x0,y0-30),DOT_R,0)
            else:
                pygame.draw.polygon(scr,c,
                                    [(x0+3,y0),(x0+5,y0+2),\
                                     (x0+2,y1),(x0,y1-10),\
                                     (x0,y0+2),(x0+2,y0)])
# Class clock
class Clock(object):
    def __init__(self,clock,x,y):
        self.clock = clock
        self.dgt0 = CLS_dgtled(x,y)
        self.dgt1 = CLS_dgtled(x+ETLED_WIDTH,y)
        self.dgt2 = CLS_dgtled(x+ETLED_WIDTH*2,y)
        self.dgt3 = CLS_dgtled(x+ETLED_WIDTH*3,y)
        self.clock = clock
        self.startsec = datetime.datetime.now().second
        self.pFlag,self.num,self.switch,self.shine = 0,0,0,1
        self.lastKT=self.startsec
    def draw(self,scr):
        pygame.display.update()
        pFlag = self.pFlag
        time = datetime.datetime.now()
        y = time.year
        m = time.month
        d = time.day
        h = time.hour
        s = time.second
        min = time.minute
        if (s-self.startsec)%2==0:
            self.shine=1
        else:
            self.shine=0
        
        if self.switch == 0:
            self.dgt0.draw(scr,DIGITAL_MASK[m//10%10]+pFlag)
            self.dgt1.draw(scr,DIGITAL_MASK[m%10+self.shine*14]+pFlag)
            self.dgt2.draw(scr,DIGITAL_MASK[d//10%10]+pFlag)
            self.dgt3.draw(scr,DIGITAL_MASK[d%10]+pFlag)
            if (s-self.lastKT)!=0 and (s-self.lastKT)%5==0:
                self.switch=1
        elif self.switch == 1:
            self.dgt0.draw(scr,DIGITAL_MASK[h//10%10]+pFlag)
            self.dgt1.draw(scr,DIGITAL_MASK[h%10+self.shine*14]+pFlag)
            self.dgt2.draw(scr,DIGITAL_MASK[min//10%10]+pFlag)
            self.dgt3.draw(scr,DIGITAL_MASK[min%10]+pFlag)
        elif self.switch == 2:
            self.dgt0.draw(scr,DIGITAL_MASK[y//1000%10]+pFlag)
            self.dgt1.draw(scr,DIGITAL_MASK[y//100%10+self.shine*14]+pFlag)
            self.dgt2.draw(scr,DIGITAL_MASK[y//10%10]+pFlag)
            self.dgt3.draw(scr,DIGITAL_MASK[y%10]+pFlag)
            if (s-self.lastKT)!=0 and (s-self.lastKT)%5==0:
                self.switch=1
        elif self.switch == 3:
            self.dgt0.draw(scr,DIGITAL_MASK[0]+pFlag)
            self.dgt1.draw(scr,DIGITAL_MASK[0+self.shine*14]+pFlag)
            self.dgt2.draw(scr,DIGITAL_MASK[s//10%10]+pFlag)
            self.dgt3.draw(scr,DIGITAL_MASK[s%10]+pFlag)
            if (s-self.lastKT)!=0 and (s-self.lastKT)%5==0:
                self.switch=1
        clock.tick(60)
    def event_key(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PERIOD:
                pFlag = 128-pFlag
            elif event.key == pygame.K_s:
                self.switch= (self.switch+1)%4
                self.lastKT = datetime.datetime.now().second
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.quit()


#main
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('DIGITAL LED')
clock = pygame.time.Clock()
clk = Clock(clock,0,0)
while True:
    clk.draw(screen)
    for event in pygame.event.get():
        clk.event_key(event)