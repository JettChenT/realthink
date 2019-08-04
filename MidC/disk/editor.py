# the image editor
import pygame,sys
SCREEN_WIDTH,SCREEN_HEIGHT = 1000,700
class CLS_grid(object):
    def __init__(self,x0,y0,n,scale,d,cList=[(0,0,0),(255,255,255)]):
        self.x0,self.y0 = x0,y0
        self.n, self.scale = n,scale
        self.data = [[0 for x in range(n)] for y in range(n)]
        self.block=['0']*n
        self.cList = cList
        self.d = d
        return
    def draw(self,scr):
        lineC=(255,255,255)
        x0,y0,scl = self.x0,self.y0,self.scale
        d=self.n*scl + 1
        pygame.draw.line(scr, lineC, (x0,y0+d), (x0+d,y0+d), 1)
        pygame.draw.line(scr, lineC, (x0+d,y0), (x0+d,y0+d), 1)
        for y in range(self.n):
            n=0
            for x in range(self.n):
                n+=2**(self.n-x-1)*self.data[y][x]
                gx,gy = x*self.scale, y*self.scale
                pygame.draw.line(scr, lineC, (x0+gx,y0+gy),\
                     (x0+gx,y0+gy+scl), 1)
                pygame.draw.line(scr, lineC, (x0+gx, y0+gy),\
                     (x0+gx+scl,y0+gy), 1)
                pygame.draw.rect(scr, self.cList[self.data[y][x]], (x0+gx+1,y0+gy+1,scl-1,scl-1), 0)
                screen.set_at((x+100,y+40),cList[grid.data[y][x]])
            self.block[y]=hex(n)
            img = font.render(self.block[y],True,lineC)
            bx,by = 500,y*self.scale+150
            screen.blit(img,(bx,by))
        return
    def mousedown(self,mx,my):
        x,y = (mx-15)//self.scale,(my-15)//self.scale-self.d
        if 0<=x<self.n and 0<=y<self.n:
            self.data[y][x] = 1-self.data[y][x]
    def save(self,fname):
        # save
        # generate bytestr
        byteStr = ' '.join(self.block)
        with open(fname,'w') as f:
            f.write(byteStr)
        return
    def clear(self):
        self.data = [[0 for x in range(self.n)] for y in range(self.n)]
        return
# init
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
font = pygame.font.Font(None, 32)
cList = [(0,0,0),(0,255,255)]
grid = CLS_grid(20,120,32,15,7,cList)
grid.draw(screen)
# main program
while True:
    screen.fill((0,0,0))
    grid.draw(screen)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mx,my = event.pos[0],event.pos[1]
            grid.mousedown(mx,my)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                print('saved😊😊')
                grid.save('demo.txt')
            elif event.key == pygame.K_c:
                print("cleared")
                grid.clear()
        elif event.type == pygame.QUIT:
            pygame.quit()
