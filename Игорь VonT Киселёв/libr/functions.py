import pygame
from libr.classes import Player, Weapon
import math

def init(caption, geometry):
    pygame.init()
    screen = pygame.display.set_mode(geometry)
    pygame.display.set_caption(caption)
    return screen

def draw(screen, FPS, objects, camera):
    for obj in objects:
        pos = [obj.position[0] - camera.position[0], obj.position[1] - camera.position[1]]
        obj.update()
        draw_obj(screen, obj, pos)
        if type(obj) == Player:
            obj.update_direction(pos)
            
    pygame.display.update()
    pygame.time.Clock().tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
            pygame.quit()

def draw_obj(screen, obj, pos):
    screen.blit(obj.image, pos)

def apply_camera():
    pass

def angle(pos):
    cursor = pygame.mouse.get_pos()
    myradians = math.atan2(cursor[1]-pos[1], pos[0]-cursor[0])
    return math.degrees(myradians)