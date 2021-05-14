import pygame


class obj(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = list(position)
    def update(self):
        pass

class Ground(obj):
    def __init__(self, image, position, size=1):
        super().__init__(position)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.rect.width*size, self.rect.height*size))
        self.rect = self.image.get_rect()
        

class Player(obj):
    def __init__(self, image, weapon, max_healt_points, max_stamina, max_speed, position, size=1):
        super().__init__(position)
        self.sprite_sheet = SpriteSheet(image, size=size)
        self.image = self.sprite_sheet.get_image(0, 0, 10*size, 10*size)
        self.image_size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.size = size
        

        self.max_healt_points = max_healt_points
        self.max_stamina = max_stamina
        self.max_speed = max_speed

        self.speed = max_speed / 2
        self.vector = Vector2D(0, 0)
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vector.x = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vector.x = 1
        elif not keys[pygame.K_LEFT] and not keys[pygame.K_a]:
            self.vector.x = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vector.y = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vector.y = 1
        elif not keys[pygame.K_UP] and not keys[pygame.K_w]:
            self.vector.y = 0
    def update(self):
        try:
            speed_multiplier = self.speed / abs(self.vector.x)+abs(self.vector.y)
        except:
            speed_multiplier = self.speed

        self.position[0] += self.vector.x * speed_multiplier * 0.71 if self.vector.x != 0 and self.vector.y != 0 else self.vector.x * speed_multiplier
        self.position[1] += self.vector.y * speed_multiplier * 0.71 if self.vector.x != 0 and self.vector.y != 0 else self.vector.y * speed_multiplier
        self.rect.x, self.rect.y = self.position[0], self.position[1]
     

    def update_direction(self, camera_position):
        cursor = pygame.mouse.get_pos()
        if camera_position[0] > cursor[0]:
            if camera_position[1]+self.image.get_height() < cursor[1]:
                self.image = self.sprite_sheet.get_image(70*self.size, 0, 10*self.size, 10*self.size)
            elif camera_position[1] > cursor[1]:
                self.image = self.sprite_sheet.get_image(50*self.size, 0, 10*self.size, 10*self.size)
            else:
                self.image = self.sprite_sheet.get_image(10*self.size, 0, 10*self.size, 10*self.size)

        elif camera_position[0]+self.image.get_width() < cursor[0]:
            if camera_position[1]+self.image.get_height() < cursor[1]:
                self.image = self.sprite_sheet.get_image(80*self.size, 0, 10*self.size, 10*self.size)
            elif camera_position[1] > cursor[1]:
                self.image = self.sprite_sheet.get_image(60*self.size, 0, 10*self.size, 10*self.size)
            else:
                self.image = self.sprite_sheet.get_image(20*self.size, 0, 10*self.size, 10*self.size)

        else:
            if camera_position[1]+self.image.get_height() < cursor[1]:
                self.image = self.sprite_sheet.get_image(40*self.size, 0, 10*self.size, 10*self.size)
            elif camera_position[1] > cursor[1]:
                self.image = self.sprite_sheet.get_image(30*self.size, 0, 10*self.size, 10*self.size)
            else:
                self.image = self.sprite_sheet.get_image(0, 0, 10*self.size, 10*self.size)


    def pick_item():
        pass

    def use_item():
        pass




class Weapon(obj):
    def __init__(self, position, image, size=1, player=None):
        super().__init__(position)
        self.in_hand = True if player else False

        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.rect.width*size, self.rect.height*size))
        self.rect = self.image.get_rect()

    def hand(self, player):
        if self.in_hand:
            self.position = player.position
    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)





class Camera():
    def __init__(self, position):
        self.position = list(position)

    def follow(self, speed, target, inaccuracy):
        if self.position[0] < target[0] and difference(self.position[0], target[0]) > inaccuracy:
            self.position[0] += speed
        if self.position[0] > target[0] and difference(self.position[0], target[0]) > inaccuracy:
            self.position[0] -= speed
        else:
            pass
        if self.position[1] < target[1] and difference(self.position[1], target[1]) > inaccuracy:
            self.position[1] += speed
        if self.position[1] > target[1] and difference(self.position[1], target[1]) > inaccuracy:
            self.position[1] -= speed
        else:
            pass




class Vector2D():
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    def __str__(self):
        return str((self.x, self.y))

    def ZERO():
        return Vector2D(0, 0)




class SpriteSheet(object):
    def __init__(self, file_name, size=1):
        self.sprite_sheet = pygame.image.load(file_name).convert_alpha()
        self.sprite_sheet = pygame.transform.scale(self.sprite_sheet, (self.sprite_sheet.get_width()*size, self.sprite_sheet.get_height()*size))


    def get_image(self, x, y, width, height):

        image = pygame.Surface([width, height], pygame.SRCALPHA).convert_alpha()

        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        return image




def difference(first, second):
    return first - second if first > second else second - first