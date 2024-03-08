from pygame import *
from math import *

class Bullet(sprite.Sprite):
    def __init__(self, location, angle, sprite):
        super().__init__()
        self.image = image.load(sprite).convert_alpha()
        self.image = transform.scale(self.image, (20, 20))
        #Rota la bala hacia donde está viendo el player
        self.angle = radians(angle - 90)
        self.image = transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect(center = location)
        self.move = [self.rect.x, self.rect.y]
        #Se calcula la velocidad en X y en Y respectivamente
        self.speed_magnitude = 20
        self.speed = (self.speed_magnitude* cos(self.angle),
                      self.speed_magnitude* sin(self.angle))
        
    def update(self, screen_rect):
        self.move[0] += self.speed[0]
        self.move[1] += self.speed[1]
        self.rect.topleft = self.move
        self.remove(screen_rect)

    def remove(self, screen_rect):
        if not self.rect.colliderect(screen_rect):
            self.kill()