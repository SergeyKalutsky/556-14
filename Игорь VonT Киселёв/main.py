import pygame as pg
from libr.classes import *
from libr.functions import *
from libr.settings import settings


objects = []

screen = init(settings['WINDOW_CAPTION'], settings['WINDOW_GEOMETRY'])

player = Player('sprites/player.png', None, 100, 100, 8, [0, 0], size=5)

ground = Ground('sprites/ground.png', [-settings['WINDOW_GEOMETRY'][0], -settings['WINDOW_GEOMETRY'][1]], size=50)

camera = Camera([0, 0])
test = Camera([0,0])

gun = Weapon(player.position, 'sprites/gun01.png', player=player, size=3)






def main():
    objects.append(ground)
    objects.append(player)
    objects.append(gun)
    RUN = True
    while RUN:
        pos = [player.position[0] - camera.position[0], player.position[1] - camera.position[1]]
        camera.follow(player.speed, (player.position[0]-settings['WINDOW_GEOMETRY'][0]/2+player.rect.width/2, player.position[1]-250+player.rect.height/2), player.speed)
        draw(screen, settings['FPS'], objects, camera)
        screen.fill((0, 0, 0))
        player.move()
        gun.hand(player)
        gun.rotate(angle(pos))
        print(angle(pos))
        


main()

