from pygame import *
from math import *
from BulletClass import Bullet

class GameEntity(sprite.Sprite):
    def __init__(self, sprite, bullet_sprite, posX, posY, sizeX, sizeY, vida):
        super().__init__()
        self.sizeX = sizeX
        self.sizeY = sizeY
        self.image = image.load(sprite).convert_alpha()
        self.image = transform.scale(self.image, (self.sizeX, self.sizeY))
        self.rect = self.image.get_rect()
        self.rect.center = (posX, posY)
        self.vida = vida
        self.bullet_sprite = bullet_sprite

class Player(GameEntity):
    def __init__(self, sprite, posX, posY, sizeX, sizeY, vida, bullet_sprite):
        super().__init__(sprite, posX, posY, sizeX, sizeY, vida, bullet_sprite)
        self.velocityX = 0
        self.velocityY = 0
        self.angle = 0
        self.mouse_pos = 0
        self.screen_size = 0

    def update(self, sprite, mouse_pos, screen_rect):
        self.velocityX = 0
        self.velocityY = 0
        self.mouse_pos = mouse_pos
        self.screen_size = screen_rect

        teclas = key.get_pressed()

        #Movimiento con WASD
        if teclas[K_w]:
            self.velocityY = -12.5
        if teclas[K_s]:
            self.velocityY = 12.5
        if teclas[K_a]:
            self.velocityX = -12.5
        if teclas[K_d]:
            self.velocityX = 12.5

        self.rect.x += self.velocityX
        self.rect.y += self.velocityY

        #Rotacion del personaje hacia el mouse
        self.angle = degrees(atan2((self.mouse_pos[1] - self.rect.centery), (self.mouse_pos[0] - self.rect.centerx))) + 90
        self.image = image.load(sprite).convert_alpha()
        self.image = transform.rotate(self.image, - self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

        #Calcular distancia en X entre el player y el mouse
        #mouse_pos[0] - self.rect.centerx 

        #Calcular distancia en Y entre el player y el mouse
        #mouse_pos[1] - self.rect.centery

        #Calcular distancia entre el player y el mouse
        #sqrt(((mouse_pos[0] - self.rect.centerx) ** 2) + ((mouse_pos[1] - self.rect.centery) ** 2))

        #Calcular el ángulo entre el player, y el mouse
        #degrees(atan2((mouse_pos[1] - self.rect.centery), (mouse_pos[0] - self.rect.centerx)))


        #Limitar el movimiento del player en la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_size[0]:
            self.rect.right = self.screen_size[0]
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_size[1]:
            self.rect.bottom = self.screen_size[1]

    #Funcion para disparar la o las balas del player
    #Se ejecuta exclusivamente en el for de los eventos en el loop principal
    def Shoot(self, event, objects):

        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            objects.add(Bullet(self.rect.center, self.angle, self.bullet_sprite))