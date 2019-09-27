import pygame, psutil, platform
from random import randint
# A pygame program that tells the information of a computer
WIDTH,HEIGHT =  700,768
BG_COLOR = (199,237,233)
INF_COLOR = (255,66,93)
TITLE_COLOR = (0,34,40)
LINE_COLOR = (92,167,86)
BLOCK_COLOR = (147,224,255)

def disText(text,scr,x,y,font,color):
    textSurface = font.render(text,False,color)
    screen.blit(textSurface,(x,y))

# Note: the MemBlock is the first block I created, and, as you can see, it's terrible, a bunch of hard-to-understand variables
# For better blocks check out DiskBlock,UsersBlock...
class MemBlock(object):
    def __init__(self,cx,cy,mtx,mty,mAx,may,memtx,memty,membx,memby,bh,by):
        self.cx = cx
        self.cy = cy
        self.mtx = mtx
        self.mty = mty
        self.max = mAx
        self.may = may
        self.membx,self.memby,self.bh,self.by = membx,memby,bh,by
        self.memtx = memtx
        self.memty = memty
        # self.SysName = self.getSysName()
        self.MemAvailable = self.getMemAvailable()
        self.MemTotal =  self.getMemTotal()
        # self.disk = psutil.disk_partitions()
        # self.diskTotal = len(self.disk)
        # self.usbTotal = 0
    def getMemTotal(self):
        mem = psutil.virtual_memory()
        return mem.total
    def getMemAvailable(self):
        mem = psutil.virtual_memory()
        return mem.available
    def refresh(self):
        self.MemAvailable = self.getMemAvailable()
        # disk = self.getDisks()
        # self.disk = disk
        # self.usbtotal = len(self.disk)-self.diskTotal
    def draw(self,scr,fontScore,fontTitle):
        MemTitleSurface = fontTitle.render("Memory:",False,TITLE_COLOR)
        # SysNameSurface = fontTitle.render(str(self.SysName),False,TITLE_COLOR)
        MemAvailableSurface = fontScore.render(str(self.MemAvailable),False,INF_COLOR)
        MemTotalSurface =  fontScore.render(str(self.MemTotal),False,INF_COLOR)
        memBlock = pygame.Rect(self.membx,self.memby,self.bh,self.by)
        # screen.blit(SysNameSurface,(self.cx,self.cy))
        pygame.draw.rect(screen,BLOCK_COLOR,memBlock)
        screen.blit(MemTitleSurface,(self.memtx,self.memty))
        pygame.draw.line(screen,LINE_COLOR,(self.mtx-20,(self.may+self.may)/2-3),(self.mtx+150,(self.may+self.may)/2-3))
        screen.blit(MemAvailableSurface,(self.mtx,self.mty))
        screen.blit(MemTotalSurface,(self.max,self.may))


class DiskBlock(object):
    def __init__(self,blockX,blockY,blockW,blockH,startX,startY,interval):
        self.block = pygame.Rect(blockX,blockY,blockH,blockW)
        self.startX = startX
        self.startY = startY
        self.interval = interval
        self.textMask = "device:{device},fstype:{fstype}"
        self.disk = psutil.disk_partitions()
        self.diskLen = len(self.disk)
    def refresh(self):
        disk = psutil.disk_partitions()
        self.disk = disk
    def draw(self,scr,fontScore,fontTitle):
        pygame.draw.rect(scr,BLOCK_COLOR,self.block)
        curY = self.startY
        disText("Disks:",screen,self.startX,curY,fontTitle,TITLE_COLOR)
        curY+=self.interval*3
        for d in self.disk:
            tempText = self.textMask.format(device=d.device,fstype=d.fstype)
            disText(tempText,screen,self.startX,curY,fontScore,LINE_COLOR)
            curY+=self.interval

class UsersBlock(object):
    def __init__(self,blockX,blockY,blockW,blockH,startX,startY,interval):
        self.block = pygame.Rect(blockX,blockY,blockH,blockW)
        self.startX = startX
        self.startY = startY
        self.interval = interval
        self.textMask = "{name}({pid})"
        self.users = psutil.users()
    def refresh(self):
        self.Users = psutil.users()
    def draw(self,scr,fontScore,fontTitle):
        pygame.draw.rect(scr,BLOCK_COLOR,self.block)
        curY = self.startY
        disText("Users:",screen,self.startX,curY,fontTitle,TITLE_COLOR)
        curY+=self.interval*3
        for u in self.users:
            tempText = self.textMask.format(name=u.name,pid=u.pid)
            disText(tempText,screen,self.startX,curY,fontScore,LINE_COLOR)
            curY+=self.interval

class sysInf(object):
    def __init__(self,blockX,blockY,blockW,blockH,startX,startY,interval):
        self.block = pygame.Rect(blockX,blockY,blockH,blockW)
        self.startX = startX
        self.startY = startY
        self.interval = interval
        self.un = platform.uname()
        self.system = self.un.system
        self.release = self.un.release
        self.machine = self.un.machine
        self.processor = self.un.processor
        self.mask = "{type}:{inf}"
    def refresh(self):
        return
    def draw(self,scr,fontScore,fontTitle):
        pygame.draw.rect(scr,BLOCK_COLOR,self.block)
        curY = self.startY
        disText("OS Information:",screen,self.startX,curY,fontTitle,TITLE_COLOR)
        curY+=self.interval*3
        disText(self.mask.format(type="system",inf = self.system),screen,self.startX,curY,fontScore,LINE_COLOR)
        curY+=self.interval
        disText(self.mask.format(type="release",inf=self.release),screen,self.startX,curY,fontScore,LINE_COLOR)
        curY+=self.interval
        disText(self.mask.format(type="processor",inf=self.processor),screen,self.startX,curY,fontScore,LINE_COLOR)


class framework(object):
    def __init__(self,blockList):
        self.blockList = blockList
        self.SysName = self.getSysName()
    def refresh(self):
        for block in self.blockList:
            block.refresh()
    def getSysName(self):
        return platform.node()
    def draw(self,scr,fontScore,fontTitle):
        SysNameSurface = fontTitle.render(str(self.SysName),False,TITLE_COLOR)
        cx,cy = 50,10
        scr.fill(BG_COLOR)
        scr.blit(SysNameSurface,(cx,cy))
        for block in self.blockList:
            block.draw(scr,fontScore,fontTitle)



# init
pygame.init()
screen = pygame.display.set_mode((HEIGHT,WIDTH))
fontScore =  pygame.font.Font(None,32)
fontTitle = pygame.font.Font(None,72)
# blocks
# System information block
SI = sysInf(30,70,150,669,50,90,20)
# Memory block
MB = MemBlock(50,10,60,320,60,345,40,270,30,250,250,120)
# Disks block
DB = DiskBlock(300,250,400,400,320,270,20)
# Users block
UB = UsersBlock(30,400,250,250,50,420,23)
blockList = [MB,DB,UB,SI]
fmw = framework(blockList)
clock = pygame.time.Clock()
# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    # sysInf.refresh()
    fmw.refresh()
    fmw.draw(screen,fontScore,fontTitle)
    # sysInf.draw(screen,fontScore,fontTitle)
    pygame.display.update()
    clock.tick(60)
