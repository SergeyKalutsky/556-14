import pygame
from playerClass import *
import main_menu as menu
import NPC as nc

room_list = ['game1.png', 'game2.png']

def init(name):
    pygame.init()
    screen = pygame.display.set_mode((1920, 1000), pygame.FULLSCREEN)
    pygame.display.set_caption(name)
    clock = pygame.time.Clock()
    return screen, clock

def image_change(player, rooms, image):
    room_cur = rooms
    if player.rect.x > 1700:
        rooms += 1
        player.rect.x = 50
        
    elif player.rect.x < 0:
        rooms -= 1
        player.rect.x = 1699
        
    if room_cur != rooms:
        image = pygame.image.load(room_list[rooms]).convert_alpha()
        image = pygame.transform.scale(image, (1920, 1000))

    return rooms, image

def npc_spawn(rooms, screen):
    if rooms == 0:
        npc_list.draw(screen)
        jack.c(jack, player, screen)
        
GREY = (51, 51, 51)
screen, clock = init('НЕ ГОНКИ')
font = pygame.font.Font(None, 50)
player = Player(50, 500, 0, img)
player_list = pygame.sprite.Group()
player_list.add(player)
npc_list = pygame.sprite.Group()

image = pygame.image.load('game1.png').convert_alpha()
image = pygame.transform.scale(image, (1920, 1000))

main_menu1 = menu.Menu(font)
jack = nc.NPC(500, 500, 0, font)
npc_list.add(jack)
rooms = 0
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            main_menu1.active_a()

    mouse_pos = pygame.mouse.get_pos()
    
    if main_menu1.game_on:
        
        rooms, image = image_change(player, rooms, image)
        screen.blit(image, (0, 0))
        player_list.draw(screen)
        player_list.update()
        npc_spawn(rooms, screen)
    else:
        screen.fill(GREY)
        main_menu1.update(screen, 'Start', mouse_pos)

    pygame.display.update()
    clock.tick(60)
