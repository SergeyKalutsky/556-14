import pygame
from pygame import *

WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#004400"


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption(" Mario ")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))

    bg.fill(Color(BACKGROUND_COLOR))

    while 1:
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit, "QUIT"
        screen.blit(bg, (0, 0))
        pygame.display.update()


if __name__ == "__main__":
    main()

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#FF6262"

level = [
       "-------------------------",
       "-                       -",
       "-                       -",
       "-                       -",
       "-            --         -",
       "-                       -",
       "--                      -",
       "-                       -",
       "-                   --- -",
       "-                       -",
       "-                       -",
       "-      ---              -",
       "-                       -",
       "-   -----------        -",
       "-                       -",
       "-                -      -",
       "-                   --  -",
       "-                       -",
       "-                       -",
       "-------------------------"]

x = y = 0
for row in level:
    for col in row:
        if col == "-":

            pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
            pf.fill(Color(PLATFORM_COLOR))
            screen.blit(pf, (x, y))

        x += PLATFORM_WIDTH
    y += PLATFORM_HEIGHT
    x = 0

    from pygame import *

    MOVE_SPEED = 7
    WIDTH = 22
    HEIGHT = 32
    COLOR = "#888888"
#Перс
    class Player(sprite.Sprite):
        def __init__(self, x, y):
            sprite.Sprite.__init__(self)
            self.xvel = 0
            self.startX = x
            self.startY = y
            self.image = Surface((WIDTH, HEIGHT))
            self.image.fill(Color(COLOR))
            self.rect = Rect(x, y, WIDTH, HEIGHT)

        def update(self, left, right):
            if left:
                self.xvel = -MOVE_SPEED

            if right:
                self.xvel = MOVE_SPEED

            if not (left or right):
                self.xvel = 0

            self.rect.x += self.xvel

        def draw(self, screen):
            screen.blit(self.image, (self.rect.x, self.rect.y))

            hero = Player(55, 55)
            left = right = False

            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False

                hero.update(left, right)
                hero.draw(screen)

     timer = pygame.time.Clock()
    JUMP_POWER = 10
    GRAVITY = 0.35
self.yvel = 0
 self.onGround = False
if up:
   if self.onGround:
       self.yvel = -JUMP_POWER

       if not self.onGround:
           self.yvel += GRAVITY

       self.onGround = False;
       self.rect.y += self.yvel
       up = false

if e.type == KEYDOWN and e.key == K_UP:
       up = True

if e.type == KEYUP and e.key == K_UP:
      up = False
      hero.update(left, right, up)
      #блоки
      PLATFORM_WIDTH = 32
      PLATFORM_HEIGHT = 32
      PLATFORM_COLOR = "#FF6262"


      class Platform(sprite.Sprite):
          def __init__(self, x, y):
              sprite.Sprite.__init__(self)
              self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
              self.image.fill(Color(PLATFORM_COLOR))
              self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

              entities = pygame.sprite.Group()
              platforms = []
              entities.add(hero)


      if col == "-":
          pf = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
          pf.fill(Color(PLATFORM_COLOR))
          screen.blit(pf, (x, y))

          if col == "-":
              pf = Platform(x, y)
              entities.add(pf)
              platforms.append(pf)
          entities.draw(screen)