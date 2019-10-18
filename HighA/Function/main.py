import pygame,random,math
# A program that draws a function
# Some basic settings
PRECISION = 0.1
WIDTH,HEIGHT = 1024,768
SCALE = 50
BG_COLOR = (0,0,0)
START_X = 0-WIDTH//SCALE//2
AXIS_COLOR = (225,225,225)
pointColor = (92,167,86)
LINE_COLOR = (random.randint(0,225),random.randint(0,225),random.randint(0,225))
ORIG_POINT = (WIDTH//2,HEIGHT//2)
# FUNCTION: draw a point
def disText(text,scr,x,y,font,color):
	print(text)
	textSurface = font.render(text,False,color)
	screen.blit(textSurface,(x,y))
def draw_point(screen,c,x,y):
	nx = int(ORIG_POINT[0]+x*SCALE)
	ny = int(ORIG_POINT[1]+y*SCALE)
	global lastx,lasty
	# print(nx,ny)
	pygame.draw.line(screen,pointColor,(lastx,lasty),(nx,ny))
	lastx,lasty = nx,ny
	return

def cal(x,fn):
	if fn == 0:
		return 0-x
	elif fn == 1:
		return 0-x*0.5
	elif fn == 2:
		return 0-math.cos(x)
	elif fn == 3:
		return 0-x**2
	else:
		return None

# init
curX = START_X
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
screen.fill(BG_COLOR)
fontScore =  pygame.font.Font(None,10)
fn = 0
lastx,lasty = START_X,cal(curX,fn)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				curX = START_X
				fn = (fn+1)%4
				lastx,lasty = START_X,cal(curX,fn)
				pointColor = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
	# screen.fill(BG_COLOR)
	for n in range(-50,50):
		nx = int(ORIG_POINT[0]+n*SCALE)
		ny = int(ORIG_POINT[1]+n*SCALE)
		disText(str(n),screen,nx,HEIGHT//2,fontScore,(255,255,255))
		disText(str(n),screen,WIDTH//2,ny,fontScore,(255,255,255))
	pygame.draw.line(screen,(255,255,255),(0,HEIGHT//2),(WIDTH,HEIGHT//2))
	pygame.draw.line(screen,(255,255,255),(WIDTH//2,0),(WIDTH//2,HEIGHT))
	pygame.draw.line(screen,(255,255,255),(WIDTH//2-20,30),(WIDTH//2,0))
	pygame.draw.line(screen,(255,255,255),(WIDTH//2+20,30),(WIDTH//2,0))
	pygame.draw.line(screen,(255,255,255),(WIDTH-20,HEIGHT//2+20),(WIDTH,HEIGHT//2))
	pygame.draw.line(screen,(255,255,255),(WIDTH-20,HEIGHT//2-20),(WIDTH,HEIGHT//2))
	curY = cal(curX,fn)
	print(curX,curY)
	draw_point(screen,pointColor,curX,curY)
	curX+=PRECISION
	pygame.display.update()
	# clock.tick(60)
