# """this is the main program of game:pushBox"""
from clsBlock import *
import pygame
pygame.init()
SCREEN_WIDTH,SCREEN_HEIGHT = 800,660
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
fontScore = pygame.font.Font(None, 28)
pic1 =  RT_block_init('floor01.txt',[[80,80,200],[160,160,160]],16,2)
pic0 = RT_block_init('brick.txt',[[220,220,220],[160,160,160]],8,4)
boxPic = RT_block_init('box01.txt',[[0,80,30],[240,240,0]],16,2)
tgPic = RT_block_init('point.txt',[[160,160,160],[80,80,200]],8,4)
manPic = RT_block_init('pacman.txt',[[0,0,0],[240,220,0]],8,4,True)
fwork = CLS_framework(pic0,pic1,tgPic,boxPic,manPic,20,80,16,32)
fwork.read_level('boxlevel1.txt')
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type  == pygame.KEYDOWN:
            fwork.eventkey(event.key,screen)
    fwork.draw(screen)
    pygame.display.update()