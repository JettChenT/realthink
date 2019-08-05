import pygame


def RT_draw(screen, data, clrList, x0, y0, w, scale):
    for dy in range(len(data)):
        line = data[dy]
        for dx in range(w):
            clr = clrList[line & 1]
            x, y = x0+(w-dx-1)*scale, y0+dy*scale
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


def RT_block_init(fn, cList, dm, scale, tm):
    pic = pygame.Surface((dm*scale, dm*scale))
    blockList = RT_block_read(fn)
    if blockList == None:
        return None
    if tm == True:
        pic.set_colorkey(cList[0])
    RT_draw(pic, blockList, cList, 0, 0, dm, scale)
    return pic


class CLS_step(object):
    def __init__(self, dx, dy):
        self.dx, self.dy = dx, dy
        return


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
        self.end = (15, 12)

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
        self.moveList = []
        self.moving = 1
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
        stt = 1
        for i in range(len(self.moveList)):
            if self.moveList[i] == (self.x, self.y):
                del self.moveList[i+1:]
                stt = 0
                break
        if stt == 1:
            self.moveList.append((self.x, self.y))
        if self.x == x and self.y == y:
            self.finish(scr, maze, dot)

    def finish(self, scr, maze, dot):
        for move in self.moveList:
            x0, y0, d = maze.x0, maze.y0, maze.scale
            scr.blit(dot, (x0+move[0]*d, y0+move[1]*d))
        self.moving = 0

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

    def draw(self, scr, maze, pacpic):
        x0, y0, d = maze.x0, maze.y0, maze.scale
        scr.blit(pacpic, (x0+self.x*d, y0+self.y*d))
        return
