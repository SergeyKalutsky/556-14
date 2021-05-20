import random
import pygame
from constants import *


from spritesheet_functions import SpriteSheet
 
class Player(pygame.sprite.Sprite):
  
    def __init__(self, x, y):
        super().__init__()
        # Задаем положение спрайта игрока на экране
        self.score = 0
        self.jumps = 0

        self.change_x = 0
        self.change_y = 0
 
        self.walking_frames_l = []
        self.walking_frames_r = []
 
        self.direction = "R"
    
        sprite_sheet = SpriteSheet("images/p1_walk.png")
        # Загружаем все ориентрованные вправо изображения в список
        image = sprite_sheet.get_image(0, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 0, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 0, 67, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(66, 93, 66, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(132, 93, 72, 90)
        self.walking_frames_r.append(image)
        image = sprite_sheet.get_image(0, 186, 70, 90)
        self.walking_frames_r.append(image)
 
        # Перебираем все ориентированные  вправо изображения
        # затем разворачиваем их влево и добавляем в новый список:
        for img in self.walking_frames_r:
            img = pygame.transform.flip(img, True, False)
            self.walking_frames_l.append(img)
 
        # Устанавливаем изображение, с которого игрок начинает
        self.image = self.walking_frames_r[0]

 
        # Устанавливаем ссылку на изображение прямоугольника
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
 
    def update(self):
    
        # Движение влево-вправо
        self.rect.x += self.change_x
        if self.direction == "R":
            frame = self.rect.x % len(self.walking_frames_r)
            self.image = self.walking_frames_r[frame]
        else:
            frame = self.rect.x % len(self.walking_frames_l)
            self.image = self.walking_frames_l[frame]

     # Расчет гравитации
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

    def draw(self, screen):
        pass

    # Движение, управляемое игроком:
    def go_left(self):
        """ Вызывается, когда пользователь нажимает стрелку влево. """
        self.change_x = -6
        self.direction = "L"
 
    def go_right(self):
        """ Вызывается, когда пользователь нажимает стрелку вправо. """
        self.change_x = 6
        self.direction = "R"
 
    def stop(self):
        """Вызывается, когда пользователь отпускает клавиатуру. """
        self.change_x = 0


class Platform(pygame.sprite.Sprite):
    # Препятствия, по которым моежт перемещаться персонаж, но не сквозь них
    images = ['images/ground00.png', 'images/ground01.png', 'images/ground02.png']

    def __init__(self, x, y):
        super().__init__()
        # Создаем прямоугольник заданных параметров
        img = random.choice(self.images)
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        # Помещаем прямоугольник в заданне место на экране
        self.rect.y = y
        self.rect.x = x


class Artifact(pygame.sprite.Sprite):
    def __init__(self, x, y, img='images/coin.png'):
        super().__init__()
        super().__init__()
        # Задаем размеры прямоугольника
        self.image = pygame.image.load(img).convert_alpha()
        # Задаем положение спрайта игрока на экране
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


# Класс Enemy описывает противника персонажа - по умолчанию это крокодил
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img="images/skeleton.png"):
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
