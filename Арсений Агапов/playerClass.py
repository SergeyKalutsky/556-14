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
        self.vector = 0
    def jump(self):
        if self.jumping:
            #self.rect.x += 10
            self.rect.y -= 15

        if not self.jumping and self.rect.y < 500:
            self.rect.y += 15
            #self.rect.x += 10
        

        
    def speed(self):
        keys = pygame.key.get_pressed()
        
        
    
        if keys[pygame.K_RIGHT]:
            if self.move_speed < 360:
                self.move_speed = self.move_speed + 50
            self.image = pygame.image.load(img[self.counter])
            self.image = pygame.transform.scale(self.image, (300, 250))
            self.counter = (self.counter + 1) % len(img)
            self.vector = 'Right'

        elif keys[pygame.K_LEFT]:
            if self.move_speed > -360:
                self.move_speed = self.move_speed - 50
            self.image = pygame.image.load(img[self.counter])
            self.image = pygame.transform.scale(self.image, (300, 250))
            self.counter = (self.counter + 1) % len(img)
            self.vector = 'Left'
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
        
class Gun():
        
    def __init__(self, damage, x, y):
        self.damage = damage
        self.shoot = False
        self.x = x
        self.y = y
        self.rad = 10
        self.bul = 0
        self.bullet_x = 0
        
    def bullet_pos(self, bullet_p, vector):
        if vector == 'Right':
            
            bullet_p += 10
        elif vector == 'Left':
            bullet_p -= 10
        return bullet_p
    
    
        
            
    def update(self, engine, screen, player, bullet_x):
        
        
        
        if self.shoot:
            self.bullet_x = self.bullet_pos(self.bullet_x, player.vector)
            engine.draw.circle(screen, (51,51,51), (bullet_x + 100, self.y + 100), self.rad)
            
        
        if self.bullet_x >= 1700 or self.bullet_x < 0:
            self.shoot = False
            
                
