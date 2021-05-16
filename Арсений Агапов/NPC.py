import pygame
class NPC(pygame.sprite.Sprite):
    img = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png']
    def __init__(self, x, y, speed, font, img=img):
        
        super().__init__()
        self.image = pygame.image.load(img[0]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (300, 250))
        self.rect = self.image.get_rect()
        # Задаем положение спрайта игрока на экране
        self.font = font
        self.rect.x = x
        self.rect.y = y
        texts = ['Hi']
        self.text1 = self.font.render(texts[0], 1, (0, 0, 0))
        self.act = False
        self.text2 = self.font.render(
                'ТЫ пока что ничего не можешь, но можешь пострелять на P', 1, (255, 255, 255))
            
        
    def c(self, name, player, screen):
        if pygame.sprite.collide_rect(name, player):
            text2 = self.font.render('Нажмите Y для диалога', 1, (0, 0, 0))
            self.text1 = self.font.render(
                'Привет. Давай играть? но я ничего не умею', 1, (255, 255, 255))
            screen.blit(self.text1, (500, 900))
            screen.blit(text2, (500, 800))
            
            
    
            
    def di(self, screen):
        if self.act:
            pygame.draw.rect(screen, (0,0,0), (0, 900, 1920, 250))
            screen.blit(self.text2, (200, 900))
        
        
    
        
    
            
            
    
   
    

