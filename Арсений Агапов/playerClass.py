import pygame
#import time


img = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png']

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, speed, img=img):
        super().__init__()
        self.image = pygame.image.load(img[0]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (300, 250))
        # Задаем положение спрайта игрока на экране
        self.rect = self.image.get_rect()
        self.counter = 0
        self.rect.x = x
        self.rect.y = y
        self.move_speed = speed
        self.jumping = False
        self.jump_speed = 0

    def jump(self):
        if self.jumping:
            #self.rect.x += 10
            self.rect.y -= 15

        if not self.jumping and self.rect.y < 500:
            self.rect.y += 15
            #self.rect.x += 10


    def speed(self):
        keys = pygame.key.get_pressed()
        print(keys)
        
    
        if keys[pygame.K_RIGHT]:
            if self.move_speed < 360:
                self.move_speed = self.move_speed + 50
            self.image = pygame.image.load(img[self.counter])
            self.image = pygame.transform.scale(self.image, (300, 250))
            self.counter = (self.counter + 1) % len(img)

        elif keys[pygame.K_LEFT]:
            if self.move_speed > -360:
                self.move_speed = self.move_speed - 50
            self.image = pygame.image.load(img[self.counter])
            self.image = pygame.transform.scale(self.image, (300, 250))
            self.counter = (self.counter + 1) % len(img)
            
        else:
            self.move_speed = 0
           

        if keys[pygame.K_UP] and self.rect.y > 450:
            self.jumping = True
            self.jump_speed = 0.01
            

    def update(self):
        self.speed()
        self.move()
        if self.rect.y < 300:
            self.jumping = False
        self.jump()
        
        # time.sleep(0.001)

    def move(self):
        self.rect.x += self.move_speed * 1/60 + (2*1/3600)/2
