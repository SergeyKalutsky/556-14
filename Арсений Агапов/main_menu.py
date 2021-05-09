import pygame


class Menu():
    x = 0
    y = 0
    label = ['Start', 'Setting', 'Exit']
    game_on = False

    def __init__(self, font):
        self.font = font
        self.text1 = self.label[0]
        self.text2 = self.label[1]
        self.text3 = self.label[2]

        self.text1 = self.font.render('Start', 1, (0, 0, 0))
        
        self.text2 = self.font.render('Settings', 1, (0, 0, 0))

        self.text3 = self.font.render('Quit', 1, (0, 0, 0))
        
        self.text4 = self.font.render('Screen', 1, (0, 0, 0))
        
        self.t = self.text1.get_rect()
        self.t1 = self.text2.get_rect()
        self.t2 = self.text3.get_rect()
        self.t3 = self.text3.get_rect()

        self.t.x = 50
        self.t.y = 50
        self.t1.x = 50
        self.t1.y = 150
        self.t2.x = 50
        self.t2.y = 250
        self.t3.x = 50
        self.t3.y = 50
        self.main_menu = True
        self.active_button = False
        self.active_button1 = False
        self.setting_menu = False
        self.setting_button = False
        
    def active_a(self):
        if self.active_button:
            self.game_on = True
        if self.active_button1:
            self.setting_menu = True
            self.main_menu = False
            
        
                
     
        
                
            
    
    def update(self, screen, text, mouse_pos):
        if self.main_menu:
            if self.t.collidepoint(mouse_pos):
                self.text1 = self.font.render(
                    'Start', 1, (4, 234, 34), (255, 255, 255))
                self.active_button = True
            else:
                self.text1 = self.font.render('Start', 1, (0, 0, 0))
                self.active_button = False
            
            if self.t1.collidepoint(mouse_pos):
                self.text2 = self.font.render(
                    'Setting', 1, (4, 234, 34), (255, 255, 255))
                self.active_button1 = True
                
                
            else:
                self.text2 = self.font.render('Setting', 1, (0, 0, 0))
                
                
            if self.t2.collidepoint(mouse_pos):
                self.text3 = self.font.render(
                    'Quit', 1, (4, 234, 34), (255, 255, 255))
                
                
            else:
                self.text3 = self.font.render('Quit', 1, (0, 0, 0))
                

            screen.blit(self.text1, (50, 50))
            screen.blit(self.text2, (50, 150))
            screen.blit(self.text3, (50, 250))
        
        if self.setting_menu:
            screen.fill((51,51,51))
            if self.t3.collidepoint(mouse_pos):
                self.text4 = self.font.render(
                    'Screen', 1, (4, 234, 34), (255, 255, 255))
                
                self.setting_button = True
                
            else:
                self.text4 = self.font.render('Screen', 1, (0, 0, 0))
            
            screen.blit(self.text4, (50, 50))
                
        
