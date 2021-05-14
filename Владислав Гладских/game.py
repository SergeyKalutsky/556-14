
import pygame
import game_object
from constants import *
from game_menu import *


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WIN_WIDTH, WIN_HEIGHT])
        pygame.display.set_caption('Test')
        self.background_img = pygame.image.load("images/phon.png").convert()
        self.all_sprite_list = pygame.sprite.Group()
        # Создаем платформы
        self.platform_list = pygame.sprite.Group()
        self.create_walls()
        # Создаем ящики
        self.drop_list = pygame.sprite.Group()
        self.create_drops()
        self.enemy_list = pygame.sprite.Group()
        self.create_enemies()

        # Создаем спрайт игрока
        self.player = game_object.Player(60, 450)
        self.player.platforms = self.platform_list
        self.player.drops = self.drop_list
        self.all_sprite_list.add(self.player)

        # Программируем смещение игрового мира:
        self.shift = 0
        self.player_global_x = self.player.rect.x
        self.game_width = self.background_img.get_rect().width

        # Создаем меню
        self.top_panel = TopPanel(20, 10)
        self.main_menu = MainMenu(300, 200)

        self.clock = pygame.time.Clock()

        # states: 'START', 'GAME', 'PAUSE', 'FINISH', 'GAME_OVER'
        self.state = 'START'

    
    
    
    def create_enemies(self):
        # Создаем противников в игре
        enemies_coords = [

        ]
        for coord in enemies_coords:
            enemy = game_object.Enemy(coord[0], coord[1])
            enemy.stop = coord[2]
            self.enemy_list.add(enemy)
            self.all_sprite_list.add(enemy)

    def shift_world(self, shift_x):
        self.shift += shift_x

        for platform in self.platform_list:
            platform.rect.x += shift_x

        for drop in self.drop_list:
            drop.rect.x += shift_x

    def create_walls(self):
        # Создаем стены и платформы
        platform_coords = [
            [64, 537, 65, 300],
            [0, 537, 65, 300],
            [128, 537, 65, 300],
            [192, 537, 65, 300],
            [256, 537, 65, 300],
            [320, 537, 65, 300],
            [384, 537, 65, 300],
            [448, 537, 65, 300],
            [512, 537, 65, 300],
            [576, 537, 65, 300],
            [640, 537, 65, 300],
            [704, 537, 65, 300],
            [768, 537, 65, 300],

        ]
        for coord in platform_coords:
            platform = game_object.Platform(
                coord[0], coord[1], coord[2], coord[3])
            self.platform_list.add(platform)
            self.all_sprite_list.add(platform)

    def create_drops(self):
        # Создаем ящики
        drop_coords = [
            [410, 500],
        ]
        for coord in drop_coords:
            drop = game_object.Drop(coord[0], coord[1])
            self.drop_list.add(drop)
            self.all_sprite_list.add(drop)

    def handle_scene(self, event):
        if self.state == 'GAME':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                elif event.key == pygame.K_RIGHT:
                    self.player.go_right()
                elif event.key == pygame.K_UP:
                    self.player.jump()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()
                elif event.key == pygame.K_ESCAPE:
                    self.state = 'PAUSE'

        # Если игра не идет, значит на экране главное меню
        # Обрабатываем события главного меню:
        else:
            # Получаем кнопку, на которую нажали в главном меню:
            active_button = self.main_menu.handle_mouse_event(event.type)
            if active_button:
                # После того, как на кнопку нажали, возвращаем ее состояние в "normal":
                active_button.state = 'normal'

                # Нажали на кнопку START, начинаем игру заново:
                if active_button.name == 'START':
                    self.__init__()
                    self.state = 'GAME'

                # На паузе и нажали CONTINUE, переведем игру с состояние GAME:
                elif active_button.name == 'CONTINUE':
                    self.state = 'GAME'

                # Нажали на QUIT - завешим работу приложения:
                elif active_button.name == 'QUIT':
                    pygame.quit()

    def draw_scene(self):
        # Выполняем заливку фона:
        self.screen.fill(BLACK)
        self.screen.blit(self.background_img, [0, 0])
        if self.state == 'START':
            # Рисуем только главное меню:
            self.main_menu.draw(self.screen)

        elif self.state == 'GAME':
            # Рисуем все спрайты в игре:
            self.top_panel.draw(self.screen)
            self.all_sprite_list.draw(self.screen)

        elif self.state == 'PAUSE':
            # Рисуем "обстановку" - платформы и главное меню:
            self.top_panel.draw(self.screen)
            self.platform_list.draw(self.screen)
            self.main_menu.draw(self.screen)

        elif self.state == 'FINISH':
            # Рисуем только главное меню:
            self.main_menu.draw(self.screen)

    def run(self):
        done = False
        while not done:
            if self.player.rect.right >= 600 and abs(self.shift) < self.game_width - WIN_WIDTH:
                diff = self.player.rect.right - 600
                self.player.rect.right = 600
                self.shift_world(-diff)

            if self.player.rect.left <= 120 and abs(self.shift) > 0:
                diff = 120 - self.player.rect.left
                self.player.rect.left = 120
                self.shift_world(diff)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                self.handle_scene(event)

            if self.state == 'GAME':
                self.all_sprite_list.update()

            else:
                self.main_menu.update()

            self.draw_scene()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


game = Game()
game.run()
