import pygame
import random
from quicksort import quick_oneNR
SCREEN_WIDTH,SCREEN_HEIGHT = 800,680
BG_COLOR = (199,237,233)
BAR_COLOR_PRIMARY = (255,66,93)
BAR_COLOR_SECONDARY = (147,224,255)
class DataBoard(object):
	def __init__(self,lis):
		self.lis = lis
	def update_lis(self,nLis):
		self.lis = nLis
	def draw(self,scr,pMin,pMax):
		scr.fill(BG_COLOR)
		perWidth = SCREEN_WIDTH//len(self.lis)
		curL = 0
		mx = max(self.lis)
		for i in range(len(self.lis)):
			n = self.lis[i]
			curBlock = pygame.Rect(curL,SCREEN_HEIGHT-int((SCREEN_HEIGHT/mx)*n),perWidth,int((SCREEN_HEIGHT/mx)*n))
			if i>=pMin and i<=pMax:
				pygame.draw.rect(scr,BAR_COLOR_PRIMARY,curBlock)
			else:
				pygame.draw.rect(scr,BAR_COLOR_SECONDARY,curBlock)
			curL+=perWidth

# pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
lis = [random.randint(1,100) for i in range(200)]
db = DataBoard(lis)
clock = pygame.time.Clock()
mem = [(0,0,len(lis)-1)]
c = 1
while len(mem)!=0:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
	# the sorting part
	p=0
	c+=1
	lis,keyI = quick_oneNR(lis,mem[p][0],mem[p][0],mem[p][2])
	db.draw(screen,mem[p][0],mem[p][2])
	if len(lis) == 0:
			# print("break")
			break
	else:
		if (keyI-1)-mem[p][0]>0:
			mem.append((mem[p][0],mem[p][0],keyI-1))
		if (mem[p][-1])-(keyI+1)>0:
			mem.append((keyI+1,keyI+1,mem[p][-1]))
	mem.pop(p)
	# lis = sorted(lis)
	db.update_lis(lis)
	pygame.display.update()
	clock.tick(5)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
	# the sorting part
	db.draw(screen,-1,-1)
	pygame.display.update()
	clock.tick(5)