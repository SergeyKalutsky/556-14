import pygame as pg
from module.settings import *

def init():
    global blocks
    fblocks = open('files/blocks.txt')
    fplayer = open('files/player.txt')
    texture = lambda x: 'files/textures/' + x

    blocks = {}
    lines = fblocks.readlines()
    for i in lines:
        i = i.split(' = ')
        block = texture(i[1]).strip('\n')
        block = pg.transform.scale(pg.image.load(block).convert_alpha(), (BSIZE, BSIZE))
        blocks[i[0]] = block
    
    player = {}
    lines = fplayer.readlines()
    for i in lines:
        i = i.strip('\n')
        if i.endswith(':'):
            i = i.strip(':')
            name = i
            player[name] = {}
        elif '=' in i and i.startswith('    '):
            i = i.strip()
            i = i.split(' = ')
            if i[0] == 'image':
                image = pg.image.load(texture(i[1]))
            else:
                i1 = i[1].strip('(').strip(')')
                i1 = i1.split(', ')
                i1 = tuple(map(lambda i: int(i), i1))
                player[name][i[0]] = image.subsurface(i1)

    print(player)

    fplayer.close()
    fblocks.close()