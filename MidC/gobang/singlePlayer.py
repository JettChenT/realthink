import pygame,sys,time
SCREEN_WIDTH,SCREEN_HEIGHT = 800,680
BOARD_ORDER,BOARD_SIZE = 19,30
BOARD_X0,BOARD_Y0 = 15,15
GRID_NULL,GRID_BLACK,GRID_WHITE = 0,1,2
SPEED_X = [1,0,1,-1]
SPEED_Y = [0,1,1,1]
"""
_      `-._     `-.     `.   \      :      /   .'     .-'     _.-'      _
 `--._     `-._    `-.    `.  `.    :    .'  .'    .-'    _.-'     _.--'
      `--._    `-._   `-.   `.  \   :   /  .'   .-'   _.-'    _.--'
`--.__     `--._   `-._  `-.  `. `. : .' .'  .-'  _.-'   _.--'     __.--'
__    `--.__    `--._  `-._ `-. `. \:/ .' .-' _.-'  _.--'    __.--'    __
  `--..__   `--.__   `--._ `-._`-.`_=_'.-'_.-' _.--'   __.--'   __..--'
--..__   `--..__  `--.__  `--._`-q(-_-)p-'_.--'  __.--'  __..--'   __..--
      ``--..__  `--..__ `--.__ `-'_) (_`-' __.--' __..--'  __..--''
...___        ``--..__ `--..__`--/__/  \--'__..--' __..--''        ___...
      ```---...___    ``--..__`_(<_   _/)_'__..--''    ___...---'''
```-----....._____```---...___(__\_\_|_/__)___...---'''_____.....-----'''
 ___   __  ________   _______   _       _   _______    ___   __   _______
|| \\  ||     ||     ||_____))  \\     //  ||_____||  || \\  ||  ||_____||
||  \\_||  ___||___  ||     \\   \\___//   ||     ||  ||  \\_||  ||     ||
"""
def is_five(grid,x,y,flag):
	# print(grid)
	try:
		for i in range(4):
			# print(i)
			isF = True
			cx,cy = x,y
			# is = True
			sx = SPEED_X[i]
			sy = SPEED_Y[i]
			# print(sx,sy)
			for j in range(5):
				# print(j)
				if j>=1:
					cx+=sx
					cy+=sy
				# print(cy,cx)
				# print(grid[cy][cx])
				# print('-------')
				if grid[cy][cx] != flag:
					isF = False
					break
			if isF == True:
				return True
			isF = True
			cx,cy = x,y
			for j in range(5):
				# print(j)
				if j>=1:
					cx-=sx
					cy-=sy
				# print(cy,cx)
				# print('-----')
				if grid[cy][cx] != flag:
					isF = False
					break
			if isF == True:
				return True
		return False
	except:
		return False

def RT_draw_txt(scr,fnt,cls,txt,x,y):
	pic = fnt.render(txt,True,cls)
	scr.blit(pic,(x,y))
	return

def RT_get_flag_beads(grid,x,y,man,flag):
	beadsNum,powerNum = 1,0
	for i in range(-1,-5,-1):
		tx,ty = x+i*SPEED_X[flag], y+i*SPEED_Y[flag]
		if tx<0 or tx >= BOARD_ORDER or ty < 0 or ty >= BOARD_ORDER:
			break
		if grid[ty][tx] != man:
			powerNum+=(grid[ty][tx] == GRID_NULL)
			break
		beadsNum+=1
	for i in range(1,5,1):
		tx,ty = x+i*SPEED_X[flag], y+i*SPEED_Y[flag]
		if tx<0 or tx >= BOARD_ORDER or ty<0 or ty >= BOARD_ORDER:
			break
		if grid[ty][tx] != man:
			powerNum+=(grid[ty][tx] == GRID_NULL)
			break
		beadsNum = beadsNum+1
	if beadsNum>=5:
		beadsNum = 5
	return [beadsNum,powerNum]

ASSESS_WIN,ASSESS_ANS,ASSESS_COUNT  = 2,1,0
def RT_get_assess_value(countList):
	assess,value = 0,0
	if ([5,2] in countList) or ([5,1] in countList) or ([5,0] in countList):
		assess,value = ASSESS_WIN,200
	elif [4,2] in countList:
		assess,value = ASSESS_ANS,100
	else:
		value += countList.count([4,1])*70
		value += countList.count([3,2])*60
		value += countList.count([3,1])*30
		value += countList.count([2,2])*20
		value += countList.count([2,1])*15
		assess = ASSESS_COUNT
	return assess,value

class CLS_assess(object):
	def __init__(self,x,y):
		self.x,self.y = x,y
		self.bAssess,self.wAssess = 0,0
		self.bValue,self.wValue = 0,0
		self.bCount =  [[0,0],[0,0],[0,0],[0,0]]
		self.wCount = [[0,0],[0,0],[0,0],[0,0]]
		return
	def beads(self,grid):
		for flag in (0,1,2,3):
			self.bCount[flag]=RT_get_flag_beads(grid,self.x,self.y,GRID_BLACK,flag)
			self.wCount[flag]=RT_get_flag_beads(grid,self.x,self.y,GRID_WHITE,flag)
		return
	def assess(self,grid):
		self.beads(grid)
		self.bAssess,self.bValue = RT_get_assess_value(self.bCount)
		self.wAssess,self.wValue = RT_get_assess_value(self.wCount)
		return
class CLS_gobang(object):
	def __init__(self,fPic,bPic,wPic,x0,y0):
		self.facePic,self.bMan,self.wMan = fPic,bPic,wPic
		self.font = pygame.font.Font(None,32)
		self.fontScore = pygame.font.Font(None,16)
		self.fontWin = pygame.font.Font(None,96)
		self.board = pygame.Surface((570,570))
		self.draw_board()
		self.x0,self.y0 = x0,y0
		self.grid_init()
		self.sysStat = 0
		self.assessFlag = True
		self.winner = -1
		return
	def grid_init(self):
		self.grid = []
		for y in range(BOARD_ORDER):
			line = [GRID_NULL]*BOARD_ORDER
			self.grid.append(line)
		self.assessList = []
		for y in range(BOARD_ORDER):
			line = []
			for x in range(BOARD_ORDER):
				score = CLS_assess(x,y)
				line.append(score)
			self.assessList.append(line)
		self.bMaxAssess,self.bMaxValue,self.bpX,self.bpY = 0,0,9,9
		self.wMaxAssess,self.wMaxValue,self.wpX,self.wpY = 0,0,-1,-1
		self.SumValue, self.pX, self.pY = 0,-1,-1
		self.grid[9][9] = GRID_BLACK
		return

	def draw_chess(self,scr):
		# print(self.grid)
		for y in range(BOARD_ORDER):
			for x in range(BOARD_ORDER):
				# print(y,x)
				# print(GRID_BLACK,GRID_WHITE)
				if self.grid[y][x] == GRID_BLACK:
					# print('black')
					scr.blit(self.bMan,\
						(self.x0+x*BOARD_SIZE,self.y0+y*BOARD_SIZE))
				elif self.grid[y][x] == GRID_WHITE:
					# print('white')
					scr.blit(self.wMan,\
						(self.x0+x*BOARD_SIZE,self.y0+y*BOARD_SIZE))
				elif self.assessFlag == True:
					# print('assess')
					pnt = self.assessList[y][x]
					if pnt.bAssess >0 or pnt.bValue >0:
						txt = str(pnt.bAssess)+','+str(pnt.bValue)
						RT_draw_txt(scr,self.fontScore,(0,0,0),txt,\
							self.x0+x*BOARD_SIZE,self.y0+y*BOARD_SIZE+2)
					if pnt.wAssess >0 or pnt.wValue >0:
						txt = str(pnt.wAssess)+','+str(pnt.wValue)
						RT_draw_txt(scr,self.fontScore,(255,255,255),txt,self.x0+x*BOARD_SIZE,self.y0+y*BOARD_SIZE+16)
		return

	def draw_board(self):
		self.board.fill((240,200,0))
		L = BOARD_X0+(BOARD_ORDER-1)*BOARD_SIZE
		for i in range(BOARD_X0,SCREEN_HEIGHT,BOARD_SIZE):
			pygame.draw.line(self.board,(0,0,0),
				(BOARD_X0,i),(L,i),1)
			pygame.draw.line(self.board,(0,0,0),
				(i,BOARD_Y0),(i,L),1)
		pygame.draw.rect(self.board,(0,0,0),(BOARD_X0-1,BOARD_Y0-1,L+3-BOARD_X0,L+3-BOARD_Y0),1 )
		return

	def draw(self,scr):
		scr.fill((180,140,0))
		scr.blit(self.facePic,(0,0))
		scr.blit(self.board,(self.x0,self.y0))
		self.draw_chess(scr)
		if self.sysStat == 1:
			txt,cls = 'YOU WIN!!',(255,0,0)
			if self.winner == GRID_BLACK:
				txt,cls = 'YOU LOSE!!',(0,0,255)
			RT_draw_txt(scr,self.fontWin,cls,txt,200,290)
		return

	def grid_assess(self):
		self.bMaxAssess,self.bMaxValue,self.bpX,self.bpY = 0,0,-1,-1
		self.wMaxAssess,self.wMaxValue,self.wpX,self.wpY = 0,0,-1,-1
		self.SumValue,self.pX,self.pY = 0,-1,-1
		for y in range(BOARD_ORDER):
			for x in range(BOARD_ORDER):
				if self.grid[y][x] != GRID_NULL:
					continue
				self.assessList[y][x].assess(self.grid)
				pnt = self.assessList[y][x]
				if (pnt.bAssess>self.bMaxAssess) or ((pnt.bAssess > self.bMaxAssess) and (pnt.bValue>self.bMaxValue)):
					self.bMaxAssess,self.bMaxValue = pnt.bAssess,pnt.bValue
					self.bpX,self.bpY = x,y
				if (pnt.wAssess>self.wMaxAssess) or ((pnt.wAssess==self.wMaxAssess) and (pnt.wValue>self.wMaxValue)):
					self.wMaxAssess,self.wMaxValue = pnt.wAssess,pnt.wValue
					self.wpX,self.wpY = x,y
				if pnt.wValue + pnt.bValue>self.SumValue:
					self.SumValue = pnt.wValue + pnt.bValue
					self.pX,self.pY = x,y
		return

	def grid_policy(self):
		if self.bMaxAssess == ASSESS_WIN:
			print('ASSESS_WIN:',self.bpX,self.bpY)
			return self.bpX,self.bpY
		elif self.wMaxAssess == ASSESS_WIN:
			print('ASSESS_WIN:',self.wpX,self.wpY)
			return self.wpX,self.wpY
		elif self.bMaxAssess > ASSESS_COUNT:
			print('B ASSESS_COUNT:',self.bpX,self.bpY)
			return self.bpX,self.bpY
		elif self.wMaxAssess>ASSESS_COUNT:
			print('W ASSESS_COUNT:',self.wpX,self.wpY)
			return self.wpX,self.wpY
		else:
			print('SUM ASSESS_COUNT:',self.pX,self.pY)
			return self.pX,self.pY


	def mouse_down(self,mx,my):
		if self.sysStat == 1:
			return
		x = int((mx-self.x0-BOARD_X0)/BOARD_SIZE+0.5)
		y = int((my-self.y0-BOARD_Y0)/BOARD_SIZE+0.5)
		if 0<= x <BOARD_ORDER and 0<=y<BOARD_ORDER:
			if self.grid[y][x] == GRID_NULL:
				self.grid[y][x] = GRID_WHITE
				if is_five(self.grid,x,y,GRID_WHITE):
					self.winner = GRID_WHITE
					self.sysStat = 1
					print('you win!!!')
					return
				self.grid_assess()
				x,y = self.grid_policy()
				self.grid[y][x] = GRID_BLACK
				if is_five(self.grid,x,y,GRID_BLACK):
					self.winner = GRID_BLACK
					self.sysStat = 1
					print('you lose!!!')
					return
				self.grid_assess()
		return

	def event(self,key):
		if key == pygame.K_RETURN and self.sysStat == 1:
			self.grid_init()
			self.sysStat = 0
		if key == pygame.K_s:
			self.assessFlag = not self.assessFlag
		return
# main program
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
fPic = pygame.image.load('face01.bmp')
fPic.set_colorkey((0,0,0))
wPic = pygame.image.load('WCMan.bmp')
wPic.set_colorkey((255,0,0))
bPic = pygame.image.load('BCMan.bmp')
bPic.set_colorkey((255,0,0))
gobang = CLS_gobang(fPic,bPic,wPic,30,80)
while True:
	gobang.draw(screen)
	# screen.blit(gobang.bMan,(50,50))
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button != 1:
				continue
			mx,my = event.pos
			gobang.mouse_down(mx,my)
		if event.type == pygame.KEYDOWN:
			gobang.event(event.key)
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()