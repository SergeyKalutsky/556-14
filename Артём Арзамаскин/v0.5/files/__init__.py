import pygame as pg
from module.settings import *

def pull_out(message):
    message = message.strip('(').strip(')')
    message = message.split(', ')
    message = tuple(map(lambda i: int(i)-1, message))
    return message

def init():
    global blocks, player
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
        elif '=' in i:
            original = i
            i = i.strip()
            i = i.split('=')
            i[0], i[1] = (i[0].strip(), i[1].strip())
            if i[0] == 'image':
                image = pg.image.load(texture(i[1])).convert_alpha()
            elif original.startswith('    '):
                del original
                i[0] = int(i[0])
                img = pull_out(i[1])
                img = image.subsurface(img)
                size = img.get_rect()
                size = (size.width, size.height)
                img = pg.transform.scale(img, (size[0]*4, size[1]*4))
                player[name][i[0]] = img

    fplayer.close()
    fblocks.close()