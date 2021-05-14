import pygame as pg
from module.settings import *
import math as m
import files

class Mouse:
    def __init__(self, bad, good, screen, player, chanks):
        self.bad = bad
        self.good = good
        self.screen = screen
        self.player = player
        self.chanks = chanks
    
    def block(self):
        mpos = pg.mouse.get_pos()
        pg.draw.rect(self.screen, self.good, (mpos[0]//BSIZE*BSIZE+self.player.x%BSIZE, mpos[1]//BSIZE*BSIZE+(self.player.y-self.player.change_y)%BSIZE, BSIZE, BSIZE), 4)
    
    def select(self):
        mpos = list(pg.mouse.get_pos())
        chank = abs(55-(((self.player.x-WWIDTH//2)//BSIZE-CSIZE//2)//CSIZE+SPAWNCHANK))
        mpos[0] = (mpos[0]//BSIZE-self.player.x//BSIZE)*BSIZE
        mpos[1] = (mpos[1]//BSIZE-self.player.y//BSIZE)*BSIZE
        return self.chanks[chank].get_group(), mpos

    def set_block(self):
        chank, pos = self.select()
        for obj in chank:
            if obj.x == pos[0] and obj.y == pos[1]:
                return
        block = CobbleStone(pos[0], pos[1], self.player)
        chank.add(block)
    
    def del_block(self):
        chank, pos = self.select()
        for obj in chank:
            if obj.x == pos[0] and obj.y == pos[1]:
                if obj.destructible:
                    chank.remove(obj)
                return

class Image(pg.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
    
    def move_to(self, pos):
        self.rect.x, self.rect.y = pos
    
    def move(self, pos):
        self.rect.x += pos[0]
        self.rect.y += pos[1]
    
    def update(self, pos):
        self.move_to(pos)

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, screen, img=None, size=(1, 2)):
        super().__init__()
        self.images_convert()
        self.resprite(0)
        self.screen = screen
        self.sprites_move_to((WWIDTH//2-self.body.rect.width//2-self.lhand.rect.width,
        WHEIGHT//2-self.body.rect.height//2-self.head.rect.height))
        self.x, self.y = (x, y)
        self.change_y = self.change_x = 0
        self.ox, self.oy = (self.lhand.rect.x, self.head.rect.y)
    
    def rect(self, x, y, color=BLUE):
        pg.draw.rect(self.screen, color, (x, y, 5, 5))
        # pg.display.update()
        # pg.time.delay(1000)
        return x, y
        # self.screen.blit(image, (x, y))
    
    def sprites_move_to(self, pos):
        # self.rect(0, 0, self.head.image)
        # self.rect(50, 0, self.lhand.image)
        # self.rect(100, 0, self.body.image)
        # self.rect(150, 0, self.rhand.image)
        # self.rect(0, 150, self.lleg.image)
        # self.rect(100, 150, self.rleg.image)
        self.head.move_to(self.rect(pos[0] + self.lhand.rect.width, pos[1]))
        self.lhand.move_to(self.rect(pos[0], pos[1] + self.head.rect.height))
        self.body.move_to(self.rect(pos[0] + self.lhand.rect.width, pos[1] + self.head.rect.height))
        self.rhand.move_to(self.rect(pos[0] + self.rhand.rect.width + self.body.rect.width, pos[1] + self.head.rect.height))
        self.lleg.move_to(self.rect(pos[0] + self.lhand.rect.width, pos[1] + self.head.rect.height + self.body.rect.height))
        self.rleg.move_to(self.rect(pos[0] + self.lhand.rect.width + self.lleg.rect.width, pos[1] + self.body.rect.height + self.head.rect.height))
        
    def sprites_move(self, pos):
        # print('move:', pos)
        self.body.move(pos)
        self.head.move(pos)
        self.lleg.move(pos)
        self.rleg.move(pos)
        self.lhand.move(pos)
        self.rhand.move(pos)
    
    def resprite(self, num):
        self.sprites = pg.sprite.Group()
        self.body = self.images['body'][num]
        self.head = self.images['head'][num]
        self.rleg = self.images['leg'][num]
        self.lleg = self.images['leg'][num]
        self.rhand = self.images['hand'][num]
        self.lhand = self.images['hand'][num]
        self.sprites.add(self.head, self.rleg, self.lleg, self.rhand, self.lhand, self.body)
        # self.sprites.add(self.head)
    
    def images_convert(self):
        self.images = files.player
        for i in self.images.values():
            for j in i:
                i[j] = Image(i[j], (0, 0))
    
    def update(self, chank):
        self.move(chank)
        self.collision(chank)
        self.change_x = 0
        self.sprites_move_to((self.ox, self.oy))
    
    def draw(self, screen):
        self.sprites.draw(screen)
    
    def jump(self, chank):
        self.sprites_move((0, 2))
        pd = bool(pg.sprite.groupcollide(self.sprites, chank, False, False))
        self.sprites_move((0, -4))
        if pd:
            pd = not bool(pg.sprite.groupcollide(self.sprites, chank, False, False))
        self.sprites_move((0, 2))
        if pd or self.y <= self.lleg.rect.height:
            self.change_y = 5 * ((self.rect.height) // BSIZE)

    def move(self, chank):
        self.grav(chank)
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.change_x += 8
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.change_x -= 8
        if keys[pg.K_UP] or keys[pg.K_w] or keys[pg.K_SPACE]:
            self.jump(chank)
        if keys[pg.K_DOWN] or keys[pg.K_s]: pass
    
    def collision(self, chank):
        pass
    
    def cmove(self, x, y):
        self.x -= x
        self.y -= y

    def grav(self, chank):
        if self.change_y == 0:
            self.change_y = -1
        else:
            self.change_y -= .25
        self.change_y = max(-BSIZE, self.change_y)
        
        if self.y - self.lleg.rect.height <= 0:
            self.y = self.lleg.rect.height
            self.change_y = 0

class Block(pg.sprite.Sprite):
    def __init__(self, x, y, player, image, destructible=True):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.x, self.y = (x, y)
        self.player = player
        self.destructible = destructible
        self.update()
        #self.rect.x, self.rect.y = self.x

    def update(self):
        self.rect.x = self.player.x + self.x
        self.rect.y = self.player.y + self.y
    
    def copy(self):
        copy = self.__class__(self.x, self.y, self.player)
        return copy
    
    def collision(self):
        pass

class Grass(Block):
    def __init__(self, x, y, player):
        image = files.blocks['Grass']
        super().__init__(x, y, player, image)

class Dirt(Block):
    def __init__(self, x, y, player):
        image = files.blocks['Dirt']
        super().__init__(x, y, player, image)

class Stone(Block):
    def __init__(self, x, y, player):
        image = files.blocks['Stone']
        super().__init__(x, y, player, image)

class Bedrock(Block):
    def __init__(self, x, y, player):
        image = files.blocks['Bedrock']
        super().__init__(x, y, player, image, False)

class CobbleStone(Block):
    def __init__(self, x, y, player):
        image = files.blocks['CobbleStone']
        super().__init__(x, y, player, image)

class Chank:
    def __init__(self, generation):
        self.map = pg.sprite.Group()
        self.map.add(*generation)
    
    def get_group(self):
        return self.map
    
    def change_pos(self, move_x=0, move_y=0):
        for obj in self.map:
            obj.x += move_x * BSIZE * CSIZE
            obj.y += move_y * BSIZE * CSIZE
    
    def copy(self):
        new_map = []
        for original in self.map:
            clone = original.copy()
            new_map.append(clone)
        new_map = pg.sprite.Group(new_map)
        return self.__class__(new_map)

class Item(pg.sprite.Sprite):
    def __init__(self, x, y, player, image, name, take):
        super().__init__()
        self.image = image
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.player = player
        self.name = name
        self.change_y = 0
        self.s = 0
        self.take = take
    
    def update(self):
        self.rect.x = self.player.x + self.x
        self.rect.y = self.player.y + self.y + self.change_y
        self.change_y += m.sin(self.s)
        self.s += 0.05
    
    def collision(self):
        return

class TestItem(Item):
    def __init__(self, x, y, player, name='test item', take=True):
        image = pg.Surface((ISIZE, ISIZE))
        image.fill(YELLOW)
        super().__init__(x, y, player, image, name, take)
    
    def collision(self):
        self.player.change_y = 8

class Mob(pg.sprite.Sprite):
    def __init__(self, x, y, player, size=(2, 1)):
        super().__init__()
        self.image = pg.Surface((size[0]*BSIZE, size[1]*BSIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.change_x = 0
        self.change_y = 0
        self.player = player
    
    def update(self, chank1, chank2, chanks):
        self.rect.x = self.player.x + self.x + self.change_x
        self.rect.y = self.player.y + self.y - abs(self.player.change_y)
        index = abs(55-(((-self.x)//BSIZE-CSIZE//2)//CSIZE+SPAWNCHANK))
        if chanks[index] == chank1 or chanks[index] == chank2: chank = chanks[index].get_group()
        else: return
        self.move(chank)
    
    def move(self, chank):
        self.grav(chank)        
        self.collision(chank)
        self.change_x = 0
    
    def jump(self, chank):
        pd = pg.sprite.spritecollide(self, chank, False)
        if not pd:
            self.rect.y += 2
            pd = bool(pg.sprite.spritecollide(self, chank, False))
            self.rect.y -= 4
            if pd:
                pd = not bool(pg.sprite.spritecollide(self, chank, False))
            self.rect.y += 2
            if pd or self.y <= self.rect.height:
                self.change_y = 10 #min(BSIZE, max(8, 5 * ((self.rect.height) // BSIZE)))
    
    def collision(self, chank):
        x, y = (self.rect.x, self.rect.y)
        self.change_x = -self.change_x
        self.rect.x -= self.change_x + self.player.change_x
        col = pg.sprite.spritecollide(self, chank, False)
        if bool(col):
            self.rect.x = x
            if not bool(pg.sprite.spritecollide(self, chank, False)):
                block = col[0]
                if self.change_x > 0:self.rect.left = block.rect.right
                else: self.rect.right = block.rect.left
                self.jump(chank)
            self.change_x = 0
        self.rect.y -= self.change_y
        col = pg.sprite.spritecollide(self, chank, False)
        if bool(col):
            self.rect.y = y
            if bool(pg.sprite.spritecollide(self, chank, False)):
                block = col[0]
                if self.change_y < 0:
                    self.rect.bottom = block.rect.top
                    self.change_y = 0
                else:
                    self.rect.top = block.rect.bottom
                    self.change_y *= -.25
            else:
                self.change_y = 0
        cx = x - self.rect.x
        cy = self.rect.y - y
        self.cmove(cx, cy)
        self.rect.x = x
        self.rect.y = y
    
    def cmove(self, x, y):
        self.x -= x
        self.y += y

    def grav(self, chank):
        if self.change_y == 0:
            self.change_y = -1
        else:
            self.change_y -= .25
