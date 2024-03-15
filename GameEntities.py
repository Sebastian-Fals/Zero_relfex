import time as tm
from pygame import *
from math import *
from threading import *
from queue import *
from BulletClass import Bullet

class GameEntity(sprite.Sprite):
    def __init__(self, sprite, bullet_sprite, position, size, vida):
        super().__init__()
        self.originalSprite = transform.scale(sprite, size)
        self.image = self.originalSprite
        self.image = transform.scale(self.image, size)
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = (self.position[0], self.position[1])
        self.vida = vida
        self.bullet_sprite = bullet_sprite
        self.screen_size = 0

class Player(GameEntity):
    def __init__(self, sprite, bullet_sprite, position, size, vida):
        super().__init__(sprite, bullet_sprite, position, size, vida)
        self.velocityX = 0
        self.velocityY = 0
        self.angle = 0
        self.mouse_pos = 0
        self.target = "enemies" #Define a quien va a dañar la bala que se spawnea

    def update(self, deltaTime,  mouse_pos, screen_size):
        self.velocityX = 0
        self.velocityY = 0
        self.mouse_pos = mouse_pos
        self.screen_size = screen_size

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

        self.rect.x += self.velocityX * deltaTime
        self.rect.y += self.velocityY * deltaTime

        #Rotacion del personaje hacia el mouse
        self.angle = degrees(atan2((self.mouse_pos[1] - self.rect.centery), (self.mouse_pos[0] - self.rect.centerx))) + 90
        self.image = self.originalSprite
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
            objects.add(Bullet(self.rect.center, self.angle, self.bullet_sprite, 20, self.target))

#Esta clase es para todos los tipos de enemigos del juego
class Enemies(GameEntity):
    def __init__(self, sprite, bullet_sprite, position, size, vida, enemy_id):
        super().__init__(sprite, bullet_sprite, position, size, vida)
        self.enemy_id = enemy_id
        #Bullet interval sirve para calcular el intervalo de disparo de las balas
        self.bullet_interval = 0
        #Bullet vertices sirve para calcular la cantidad de lugares por donde salen las balas
        self.bullet_vertices = 0
        self.suma_del_angulo = 0
        self.angulo_actual = 0
        #Estas dos variables son necesarias para generar los intervalos de los disparos del enemigo
        self.ultimo_disparo = tm.time()
        self.shoot_queue = Queue()
        #Define a quien va a dañar la bala que se spawnea
        self.target = "player"
        self.loadEnemy()

    def loadEnemy(self):
        if self.enemy_id == "enemigo_patron_circular":
            #Se configuran las opciones iniciales del enemigo
            self.image = image.load("Assets/circular_enemy.png").convert_alpha()
            self.image = transform.scale(self.image, (40, 40))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.bullet_interval = 0.3
            self.bullet_vertices = 10
            self.suma_del_angulo = 360/self.bullet_vertices
        if self.enemy_id == "enemigo_patron_espiral":
            #Se configuran las opciones iniciales del enemigo
            self.image = image.load("Assets/circular_enemy.png").convert_alpha()
            self.image = transform.scale(self.image, (40, 40))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.bullet_interval = 0.3
            self.bullet_vertices = 3
            self.suma_del_angulo = 360/self.bullet_vertices

    def update(self, objects):
        #Esta condicional depende del tipo de enemigos que se genera
        now = tm.time()
        if now - self.ultimo_disparo > self.bullet_interval:
            # Disparar balas en un hilo separado
            shoot_thread = Thread(target=self.shoot, args=(objects,))
            shoot_thread.start()
            self.ultimo_disparo = now

        #Se destruye el enemigo
        if self.vida == 0:
            self.kill()

    #Esta funcion son los tipos de disparo de los enemigos
    def shoot(self, objects):
        if self.enemy_id == "enemigo_patron_circular":
            for _ in range(self.bullet_vertices):
                self.shoot_queue.put(Bullet(self.rect.center, self.angulo_actual, self.bullet_sprite[1], 5, self.target))
                self.angulo_actual += self.suma_del_angulo

            # Agregar las balas a la lista principal fuera del hilo
            while not self.shoot_queue.empty():
                objects.add(self.shoot_queue.get())
        if self.enemy_id == "enemigo_patron_espiral":
            for _ in range(self.bullet_vertices):
                self.shoot_queue.put(Bullet(self.rect.center, self.angulo_actual, self.bullet_sprite[2], 5, self.target))
                self.angulo_actual += self.suma_del_angulo

            self.angulo_actual += 20

            # Agregar las balas a la lista principal fuera del hilo
            while not self.shoot_queue.empty():
                objects.add(self.shoot_queue.get())

    def take_damage(self, amount):
        self.vida -= amount