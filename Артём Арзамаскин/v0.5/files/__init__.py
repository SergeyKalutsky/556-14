import pygame as pg
from module.settings import *
import os

def init():
    global blocks
    fblocks = open('files/blocks.txt')
    texture = lambda x: '/'.join(os.getcwd().split('\\')) + '/files/textures/' + x.strip('\n')
    blocks = {}
    lines = fblocks.readlines()
    for i in lines:
        i = i.split('  ')
        block = texture(i[1])
        block = pg.transform.scale(pg.image.load(block).convert_alpha(), (BSIZE, BSIZE))
        blocks[i[0]] = block
        break
    fblocks.close()