from clsBlock import *
import pygame,time,random,pprint
pygame.init()
screen = pygame.display.set_mode((1024,768))
clock = pygame.time.Clock()
fontscore = pygame.font.Font(None, 42)
pList = []
picPac = RT_block_init('pacman.txt',[(0,0,0),[200,100,100]],8,4,True)
picPac2 = RT_block_init('pacman2.txt',[(0,0,0),(200,100,100)],8,4,True)
pList.append(picPac)
pList.append(picPac2)
pacman = CLS_pacman(16,0,0,0)
pic0 = RT_block_init('brick.txt',[(100,100,100),(20,20,20)],8,4,False)
pic1 = RT_block_init('tree.txt',[(0,100,0),(90,89,100)],8,4,False)
dot = RT_block_init('dot.txt',[(0,0,0),(225,225,225)],16,2,True)
pacman = CLS_pacman(16,0,0,0)
maze = CLS_maze('maze07.txt',pic0,pic1,20,100,16,32)
t = time.time()
pi = 0
maze.draw(screen)   
while True:
    pacman.check(maze.end,screen,maze,dot)
    pacman.draw(screen,maze,pList[pi])
    screen.blit(pic0,(100,20))
    screen.blit(pic1,(150,20))
    screen.blit(pList[0],(200,20))
    pygame.event.get()
    pygame.display.update()
    pi = (pi+1)%2
    clock.tick(10)
    # pygame.event.get()
    # pprint.pprint(maze.log)
    # maze.draw(screen)
    # pacman.draw(screen,maze,pList[pi])
    # pacman.check(maze.end,screen,maze,dot)
    # pygame.display.update()
    # pygame.event.get()
    # pi = (pi+1)%2
    # clock.tick(1)