import pygame
from constants import *
from random import choice

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, img='images/character_without_drop.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        # Задаем положение спрайта игрока на экране
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        # Задаем скорость игрока по x и по y
        self.change_x = 0
        self.change_y = 0
        self.platforms = pygame.sprite.Group()
        self.drops = pygame.sprite.Group()
        self.jumps = 0

    
    
    
    def update(self):
        self.rect.x += self.change_x
        # Проверяем столкновение с препятствием
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            # Если персонаж двигался вправо, остановим его слева от препятствия
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Наоборот, если движение было влево остановим его справа от препятствия
                self.rect.left = block.rect.right

        self.rect.y += self.change_y

        # Проверяем столкновение с препятствием
        block_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        for block in block_hit_list:
            # При движении вниз, персонаж упал на препятcтвие - он должен встать на него сверху
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # В прыжке персонаж врезался в препятствия - движение вверх должно прекратиться.
            self.change_y = 0

        # Проверяем столкновение с ящиком
        drop_hit_list = pygame.sprite.spritecollide(self, self.drops, False)
        for drop in drop_hit_list:
            drop.kill()
    
    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            # Моделируем ускорение свободного падения:
            self.change_y += .35

        # Проверка: персонаж на земле или нет
        if self.rect.y >= WIN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = WIN_HEIGHT - self.rect.height

    
    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.y -= 2

        if len(platform_hit_list) > 0 or self.rect.bottom >= WIN_HEIGHT:
            self.change_y = -10

    def go_left(self):
        self.change_x = -5

    def go_right(self):
        self.change_x = 5

    def stop(self):
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
# Препятствия, по которым моежт перемещаться персонаж, но не сквозь них
    images = ['images/ground01.png']
    def __init__(self, x, y, width, height):
        super().__init__()
        # Создаем прямоугольник заданных параметров
        img = choice(self.images)
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        # Помещаем прямоугольник в заданне место на экране
        self.rect.y = y
        self.rect.x = x


class Drop(pygame.sprite.Sprite):
    def __init__(self, x, y, img='images/drop.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        # Задаем положение спрайта игрока на экране
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Enemy(pygame.sprite.Sprite):
   def __init__(self, x, y, img="images/crocodile.png"):
       super().__init__()
       # Загружаем изображение в спрайт
       self.image = pygame.image.load(img).convert_alpha()
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y
       # спрайт противника ходит туда-обратно по горизонтали от точки start до stop:
       self.start = x
       self.stop = x
       # направление перемещения противника “1” - вправо, “-1” - влево
       self.direction = 1
       # скорость перемещения противника
       self.speed = 2

   def shift(self, x):
       self.rect.x += x
       self.start += x
       self.stop += x

   def update(self):
       # спрайт дошел то stop и должен повернуть обратно, налево
       if self.rect.x >= self.stop:
           self.rect.x = self.stop
           self.direction = -1
       # спрайт дошел до start и должен повернуть обратно, направо
       if self.rect.x <= self.start:
           self.rect.x = self.start
           self.direction = 1
       # смещаем спрайт в указанном направлении
       self.rect.x += self.direction * self.speed

   def run(self):
       self.hit_time = 0
       if self.state == "GAME":
           self.time = pygame.time.get_ticks()
           # Проверяем столкновение игрока с противником:
           if pygame.sprite.spritecollideany(self.player, self.enemy_list, False):
               # очки жизней при столкновении буду отниматься не чаще 1 раза в секунду:
               if self.time - self.hit_time > 1000:
                   self.player.lives -= 1
                   # зафиксируем время последнего столкновения
                   self.hit_time = self.time
               # "отбросим" игрока от противника

   def shift_world(self, shift_x):
       self.shift += shift_x
       for enemy in self.enemy_list:
           enemy.shift(shift_x)