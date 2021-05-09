'''
Модуль 4. Урок 1
Проект лабиринт. Окончательная версия
'''
import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (50, 50, 255)
RED = (255, 0, 0)
WIDTH = 800
HEIGHT = 600
FPS = 30


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, img='buffalo.png'):
        super().__init__()

        self.image = pygame.image.load(img).convert_alpha()
        # self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.alive = True

        self.change_x = 0
        self.change_y = 0
        self.walls = None
        self.coins = None
        self.enemies = pygame.sprite.Group()
        self.collected_coins = 0
        self.finish = None
        self.win = False

    def update(self):
        # Движение вправо - влево
        self.rect.x += self.change_x
        # Проверим, что объект не врезается в стену:
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # Если игрок двигался вправо, вернем его правую границу к левой границе препятствия:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Если он двигался влево, делаем все наоборот:
                self.rect.left = block.rect.right

        # Движение вверх - вниз
        self.rect.y += self.change_y
        # Проверим, что объект не врезается в стену:
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # Вернем игрока за границу препятствия, в которое он врезался:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        coins_hit_list = pygame.sprite.spritecollide(self, self.coins, False)
        for coin in coins_hit_list:
            self.collected_coins += 1
            coin.kill()

        if pygame.sprite.spritecollideany(self, self.enemies):
            self.alive = False

        if pygame.sprite.collide_rect(self, self.finish):
            self.win = True


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, img='coin.png'):
        super().__init__()
        # Загружаем изображение в спрайт
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, img='grid3.png'):
        super().__init__()
        # Загружаем изображение в спрайт
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # спрайт противника ходит туда - обратно по горизонтали от точки start до точки stop:
        self.start = x
        self.stop = x + random.randint(180, 240)
        self.direction = 1


class Finish(pygame.sprite.Sprite):
    def __init__(self, x, y, img='finish.png'):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def quit(e):
    if e.type == pygame.QUIT:
        pygame.quit()


def init(caption):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(caption)
    clock = pygame.time.Clock()
    return screen, clock


def on_keydown(key):
    if key == pygame.K_LEFT:
        player.change_x = -3
    if key == pygame.K_RIGHT:
        player.change_x = 3
    if key == pygame.K_UP:
        player.change_y = -3
    if key == pygame.K_DOWN:
        player.change_y = 3


def on_keyup(key):
    if key == pygame.K_LEFT:
        player.change_x = 0
    if key == pygame.K_RIGHT:
        player.change_x = 0
    if key == pygame.K_UP:
        player.change_y = 0
    if key == pygame.K_DOWN:
        player.change_y = 0


def draw_text(screen, text, font_size, background_color, text_color, pos):
    basic_font = pygame.font.SysFont(None, font_size)
    text = basic_font.render(text, True, text_color, background_color)
    screen.blit(text, pos)


coins_list = pygame.sprite.Group()
all_sprite_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()

wall_coords = [
    [0, 0, 10, 600],
    [790, 0, 10, 600],
    [10, 0, 790, 10],
    [0, 200, 100, 10],
    [0, 590, 600, 10],
    [450, 400, 10, 200],
    [550, 450, 250, 10],
    [228, 109, 250, 10]

]

coins_coord = [[190, 240], [100, 140], [236, 50], [400, 234], [100, 50]]
for coord in wall_coords:
    wall = Wall(coord[0], coord[1], coord[2], coord[3])
    wall_list.add(wall)
    all_sprite_list.add(wall)

screen, clock = init('ЛАБИРИНТ')

for coord in coins_coord:
    coin = Coin(coord[0], coord[1])
    coins_list.add(coin)
    all_sprite_list.add(coin)

enemies_list = pygame.sprite.Group()
enemies_coord = [[100, 50], [10, 500], [400, 50]]
for coord in enemies_coord:
    enemy = Enemy(coord[0], coord[1])
    enemies_list.add(enemy)
    all_sprite_list.add(enemy)


# Create the player paddle object
finish = Finish(650, 550)
player = Player(50, 50)
player.finish = finish
player.coins = coins_list
player.walls = wall_list
player.enemies = enemies_list
all_sprite_list.add(player)
all_sprite_list.add(finish)

done = False

while not done:
    for event in pygame.event.get():
        quit(event)
    if event.type == pygame.KEYDOWN:
        on_keydown(event.key)
    if event.type == pygame.KEYUP:
        on_keyup(event.key)
        
    screen.fill((102, 176, 250))

    if player.win:
        draw_text(screen, 'ТЫ ПОБЕДИЛ', 30, BLACK, RED, (100, 100))

    if player.alive:
        all_sprite_list.update()
        all_sprite_list.draw(screen)
    else:
        draw_text(screen, 'ИГРА ОКОНЧЕНА', 30, BLACK, RED, (100, 100))
        
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
