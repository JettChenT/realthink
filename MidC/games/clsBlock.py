import pygame
import random
import pprint

def RT_draw(screen, w,data, clrList, scale):
    for dy in range(len(data)):
        line = data[dy]
        for dx in range(w):
            clr = clrList[line & 1]
            x, y = 0+(w-dx-1)*scale, 0+dy*scale
            if scale > 1:
                pygame.draw.rect(screen, clr, (x, y, scale, scale), 0)
            else:
                screen.set_at((x, y), clr)
            line = line >> 1
    return


def RT_block_read(fn):
    try:
        with open(fn, 'r') as f:
            txtLine = f.readlines()[0]
            dataList = txtLine.split()
            block = [int(dataList[p], 16) for p in range(len(dataList))]
    except:
        return None
    return block


def RT_block_init(fn, cList, dw, scale, tm=False):
    pic = pygame.Surface((dw*scale, dw*scale))
    blockList = RT_block_read(fn)
    if blockList != None:
        RT_draw(pic,dw,blockList,cList,scale)
    if tm == True:
        pic.set_colorkey(cList[0])
    # RT_draw(pic, blockList, cList, 0, 0, dm, scale)
    return pic


class CLS_step(object):
    def __init__(self, dx, dy):
        self.dx, self.dy = dx, dy
        return

def RT_drawpath(scr,clr,maze,x,y):
    x0, y0, d = maze.x0, maze.y0, maze.scale
    pos = maze.data[ y ][ x ]         # 自己所在二维列表中保存了父格子下标
    xFth = x0 + pos[0] * d + d // 2   # 根据父格子下标得到父格子中央的屏幕坐标
    yFth = y0 + pos[1] * d + d // 2
    xScr = x0 + x * d + d // 2        # 根据自己的下标得到自己格子中央的屏幕坐标
    yScr = y0 + y * d + d // 2        # 根据自己的下标得到自己格子中央的屏幕坐标
    pygame.draw.line( scr, clr, ( xFth, yFth ), ( xScr, yScr ), 3 )
class CLS_stack(object):
    def __init__(self):
        self.nList = []
        return

    def PUSH(self, step):
        self.nList.append(step)
        return

    def POP(self):
        if len(self.nList) == 0:
            return None
        step = self.nList[-1]
        self.nList.pop()
        return step


class CLS_grid(object):
    def __init__(self, bPic0, bPic1, x0, y0, n, scale, bw, d):
        self.x0, self.y0 = x0, y0
        self.n, self.scale = n, scale
        self.picList = [bPic0, bPic1]
        self.n, self.bw = n, bw
        self.pic = pygame.Surface.Surface(n*bw+100, n*bw)
        self.data = [[0 for x in range(n)] for y in range(n)]
        self.block = [0]*n
        # self.cList = cList
        self.d = d
        return

    def draw_pic(self, fScore):
        self.pic.fill((0, 0, 0))
        for y in range(self.n):
            self.block[y] = 0
            for x in range(self.n):
                self.pic.blit(self.picList[self.data[y][x]],
                              (x*self.bw, y*self.bw))
                self.block[y] += 2**(self.n-1-x)*self.data[y][x]
            imgScore = fScore.render(hex(self.block[y]), True, (240, 240, 240))
            self.pic.blit(imgScore, (self.n*self.bw+10, y*self.bw+10))

    def draw(self, scr):
        scr.blit(self.pic, (self.x0, self.y0))

    def read(self, fName):
        try:
            txtFile = open(fName, 'r')
        except:
            return
        txt = txtFile.readline()
        txtFile.close()
        blockTxt = txt.split()
        for y in range(self.n):
            self.block[y], bit = int(blockTxt[y], 16), int(blockTxt[y], 16)
            for x in range(self.n):
                self.data[y][self.n-1-x] = bit % 2
                bit = bit//2

    def clear(self):
        self.data = [[0 for x in range(self.n)] for y in range(self.n)]
        return


class CLS_maze(object):
    def __init__(self, fn, pic0, pic1, x0, y0, n, scale):
        self.x0, self.y0 = x0, y0
        self.n, self.scale = n, scale
        self.data = [[0 for x in range(n)] for y in range(n)]
        self.block = [0]*n
        # self.cList = cList
        self.img = pygame.Surface((n*scale, n*scale))
        self.read(fn)
        self.end = (15, 15)
        self.log = [[0 for x in range(n)] for y in range(n)]
        for y in range(n):
            for x in range(n):
                if self.data[y][x] == 0:
                    self.img.blit(pic0, (x*scale, y*scale))
                else:
                    self.img.blit(pic1, (x*scale, y*scale))
        return

    def draw(self, scr):
        scr.blit(self.img, (self.x0, self.y0))

    def read(self, fName):
        try:
            txtFile = open(fName, 'r')
        except:
            return
        txt = txtFile.readline()
        txtFile.close()
        blockTxt = txt.split()
        for y in range(self.n):
            self.block[y], bit = int(blockTxt[y], 16), int(blockTxt[y], 16)
            for x in range(self.n):
                self.data[y][self.n-1-x] = bit % 2
                bit = bit//2

    def clear(self):
        self.data = [[0 for x in range(self.n)] for y in range(self.n)]
        return


# pacman
SPEED_X, SPEED_Y = [1, 0, -1, 0], [0, 1, 0, -1]


class CLS_pacman(object):
    def __init__(self, n, x, y, flag):
        self.x, self.y = x, y
        self.n, self.flag = n, flag
        self.moveList = [(0, 0)]
        self.moveList2 = [(0, 0)]
        self.mem = []
        self.moving = 1
        self.testList = [(self.x,self.y)]
        return

    def test(self, grid, flag):
        """test if each move is available"""
        x = self.x+SPEED_X[flag]
        y = self.y+SPEED_Y[flag]
        return 0 <= x < self.n and 0 <= y < self.n and grid[y][x] == 1

    def move(self, grid):
        self.x += SPEED_X[self.flag]
        self.y += SPEED_Y[self.flag]
        return self.x, self.y

    def check(self, m, scr, maze, dot):
        x = m[0]
        y = m[1]
        if self.x == x and self.y == y:
            self.finish(scr, maze, dot)

    def finish(self, scr, maze, dot):
        cx,cy =  maze.end
        while True:
            scr.blit(dot,maze.x0+cx*maze.scale,maze.y0+cy*maze.scale)
            if maze.log[cx][cy] == (0,0) or maze.log[cx,cy] == 0:
                break
            cx,cy = maze.log[cx][cy]
        self.moving = 0
        return

    def rhmove(self, grid):
        """right handed move"""
        if self.test(grid, (self.flag+1) % 4):
            self.flag = (self.flag+1) % 4
            self.move(grid)
        elif self.test(grid, self.flag):
            self.move(grid)
        elif self.test(grid, (self.flag-1) % 4):
            self.flag = (self.flag-1) % 4
            self.move(grid)
        else:
            self.flag = (self.flag+1) % 4

    def memmove(self, grid):
        """This is the search move, which is much more effectivec than the right handed move."""
        self.moveList.append((self.x, self.y))
        self.moveList2.append((self.x, self.y))
        waysList = []
        for f in range(4):
            if self.test(grid, f):
                if (self.x+SPEED_X[f], self.y+SPEED_Y[f]) not in self.moveList:
                    waysList.append(f)
        if len(waysList) == 1:
            self.flag = waysList[0]
            self.move(grid)
            return
        elif len(waysList) == 4:
            self.flag = 0 
            self.move(grid)
            return
        elif len(waysList) > 1:
            for f in waysList:
                self.mem.append((self.x, self.y, f))
            self.x, self.y, self.flag = self.mem[-1]
        elif len(waysList) == 0:
            self.x, self.y, self.flag = self.mem[-1]
            for i in range(len(self.moveList2)):
                if self.moveList2[i][0] == self.x and self.moveList2[i][1] == self.y:
                    del self.moveList2[i+1:]
                    break
        self.move(grid)
        self.mem.pop()

    def memmove2(self, grid):
        self.moveList.append((self.x, self.y))
        self.moveList2.append((self.x, self.y))
        waysList = []
        for f in range(4):
            if self.test(grid, f):
                if (self.x+SPEED_X[f], self.y+SPEED_Y[f]) not in self.moveList:
                    waysList.append(f)
        if len(waysList) == 1:
            self.flag = waysList[0]
            self.move(grid)
            return
        elif len(waysList) > 1:
            for f in waysList:
                self.mem.append((self.x, self.y, f))
            self.x, self.y, self.flag = self.mem[0]
        elif len(waysList) == 0:
            self.x, self.y, self.flag = self.mem[0]
            for i in range(len(self.moveList2)):
                if self.moveList2[i][0] == self.x and self.moveList2[i][1] == self.y:
                    del self.moveList2[i+1:]
                    break
        self.move(grid)
        self.mem.pop(0)
    
    def ultimateMove(self,grid,log,maze):
        if len(self.testList) == 0:
            return
        self.x,self.y = self.testList[0]
        for f in range(4):
            if self.test(grid,f) and log[self.x+SPEED_X[f]][self.y+SPEED_Y[f]]==0:
                self.testList.append((self.x+SPEED_X[f],self.y+SPEED_Y[f]))
                log[self.x+SPEED_X[f]][self.y+SPEED_Y[f]] = (self.x,self.y)
        self.testList.pop(0)

    def run(self,i):
        self.x,self.y,f = self.moveList2[i]
    
    def guimove(self, grid):
        self.flag = (self.flag+random.randint(1, 3)) % 4
        if self.test(grid, self.flag):
            self.move(grid)

    def draw(self, scr, maze, pacpic):
        x0, y0, d = maze.x0, maze.y0, maze.scale
        scr.blit(pacpic, (x0+self.x*d, y0+self.y*d))
        return
# add the dependencies of box-pushing
class CLS_target(object):
    def __init__(self,pic,x,y):
        self.pic = pic
        self.x,self.y = x,y

    def draw(self,scr,maze):
        x = maze.x0 + self.x*maze.scale
        y = maze.y0 + self.y*maze.scale
        scr.blit(self.pic,(x,y))
        return

class CLS_box(CLS_target):
    def test(self,grid,flag):
        x = self.x+SPEED_X[flag]
        y = self.y+SPEED_Y[flag]
        return grid[y][x] == 1
    def move(self,grid,flag):
        if self.test(grid,flag):
            grid[self.y][self.x] = 1
            self.x,self.y  = self.x+SPEED_X[flag],self.y+SPEED_Y[flag]
            grid[self.y][self.x] = self
        return

class CLS_man(CLS_target):
    def test(self,grid,flag):
        # pprint.pprint(grid)
        x = self.x+SPEED_X[flag]
        y = self.y+SPEED_Y[flag]
        if type(grid[y][x]) == CLS_box:
            if grid[y][x].test(grid,flag):
                return True
            else:
                return False
        else:
            return bool(grid[y][x])
        # print(grid)
        # return True
    def move(self,grid,flag,his):
        if self.test(grid,flag):
            self.x+= SPEED_X[flag]
            self.y+= SPEED_Y[flag]
            if type(grid[self.y][self.x]) == CLS_box:
                grid[self.y][self.x].move(grid,flag)
                his.PUSH((1,flag,(self.x,self.y)))
            else:
                his.PUSH((0,flag,(self.x,self.y)))
            return True
        else:
            return False

class CLS_framework(object):
    def __init__(self,pic0,pic1,tgPic,boxPic,manPic,x0,y0,n,scale):
        self.pic0,self.pic1,self.tgPic,self.boxPic,self.manPic\
            =pic0,pic1,tgPic,boxPic,manPic
        self.x0,self.y0,self.n,self.scale = x0,y0,n,scale
        self.maze = CLS_maze('boxmap1.txt',pic0,pic1,self.x0,self.y0,self.n,self.scale)
        self.currentLevel = 1
        self.tgPosList = []
        self.tgList= []
        self.boxList = []
        self.man = CLS_man(manPic,0,0)
        self.history = CLS_stack()
        return
    
    def read_level(self,fileName):
        try:
            fn = open(fileName)
        except:
            print(fileName,'not found!')
            return
        lines =  fn.readlines()
        fn.close()
        # print(lines[0])
        self.maze = CLS_maze(lines[0].strip('\n'),self.pic0,self.pic1,\
            self.x0,self.y0,self.n,self.scale)
        self.tgPosList = eval(lines[1])
        self.tgList = []
        self.boxPosList = eval(lines[2])
        for pos in self.tgPosList:
            target = CLS_target(self.tgPic,pos[0],pos[1])
            self.tgList.append(target)
        self.boxList = []
        for pos in self.boxPosList:
            box = CLS_box(self.boxPic,pos[0],pos[1])
            self.boxList.append(box)
            self.maze.data[pos[1]][pos[0]] = box
        self.man.x,self.man.y = eval(lines[3])
        return
    
    def draw(self,scr):
        scr.fill((0,0,0))
        self.maze.draw(scr)
        # print(self.boxList)
        for target in self.tgList:
            target.draw(scr,self.maze)
        for box in self.boxList:
            box.draw(scr,self.maze)
        self.man.draw(scr,self.maze)
        return
    def regret(self):
        l = self.history.POP()
        if l == None:
            return
        elif l[0] == 1:
            self.man.x+=SPEED_X[3-l[1]]
            self.man.y+=SPEED_Y[3-l[1]]
        elif l[0] == 0:
            self.man.x+=SPEED_X[3-l[1]]
            self.man.y+=SPEED_Y[3-l[1]]
    def eventkey(self,key):
        flag = -1
        if key == pygame.K_RIGHT:
            flag = 0
        elif key == pygame.K_DOWN:
            flag = 1
        elif key == pygame.K_LEFT:
            flag = 2
        elif key == pygame.K_UP:
            flag = 3
        elif key == pygame.K_z:
            self.regret()
        if flag != -1:
            # self.history.PUSH(self.maze.data)
            self.man.move(self.maze.data,flag,self.history)
            # print('move')
        if self.is_ok() == True:
            print('You Win!!')
            self.currentLevel+=1
            # go to the next level
        # print(self.boxPosList)
        return
    
    def is_ok(self):
        st = 1
        for f in self.tgPosList:
            st = 1-(type(self.maze.data[f[1]][f[0]]) == int)
        return st