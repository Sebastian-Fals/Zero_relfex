import time as tm
from pygame import *
from math import *
from threading import *
from queue import *
from BulletClass import Bullet
from funciones import tamanoDinamico

class GameEntity(sprite.Sprite):
    def __init__(self, sprite, bullet_sprite, position, size, vida, screen_size):
        super().__init__()
        self.originalSprite = transform.scale(sprite, size)
        self.image = self.originalSprite
        self.image = transform.scale(self.image, size)
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.center = (self.position[0], self.position[1])
        self.vida = vida
        self.bullet_sprite = bullet_sprite
        self.screen_size = screen_size
        
    def take_damage(self, amount):
        self.vida -= amount
    
    def resize(self, sizeX, sizeY):
        self.image = transform.scale(self.image, (sizeX, sizeY))

class Player(GameEntity):
    def __init__(self, sprite, bullet_sprite, position, size, vida, screen_size):
        super().__init__(sprite, bullet_sprite, position, size, vida, screen_size)
        self.velocityX = 0
        self.velocityY = 0
        self.angle = 0
        self.mouse_pos = 0
        self.target = "enemies" #Define a quien va a dañar la bala que se spawnea
        self.vida = vida
        self.isDead = False
        self.shootSound = mixer.Sound("Assets/SFX/laser_beam.mp3")
        self.shootSound.set_volume(0.3)

    def update(self, deltaTime,  mouse_pos, screen_size):
        self.velocityX = 0
        self.velocityY = 0
        self.mouse_pos = mouse_pos
        self.screen_size = screen_size

        teclas = key.get_pressed()

        #Movimiento con WASD
        if teclas[K_w]:
            self.velocityY = -tamanoDinamico(self.screen_size[0], 0.46875)
        if teclas[K_s]:
            self.velocityY = tamanoDinamico(self.screen_size[0], 0.46875)
        if teclas[K_a]:
            self.velocityX = -tamanoDinamico(self.screen_size[0], 0.46875)
        if teclas[K_d]:
            self.velocityX = tamanoDinamico(self.screen_size[0], 0.46875)

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
        
        if self.vida <= 0:
            self.isDead = True
            self.kill()

    #Funcion para disparar la o las balas del player
    #Se ejecuta exclusivamente en el for de los eventos en el loop principal
    def Shoot(self, event, objects):
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and not self.isDead:
            self.shootSound.play()
            objects.add(Bullet(self.rect.center, self.angle, self.bullet_sprite, tamanoDinamico(self.screen_size[0], 1.5625), self.target, (tamanoDinamico(self.screen_size[0], 1.5625), tamanoDinamico(self.screen_size[0], 1.5625))))

#Esta clase es para todos los tipos de enemigos del juego
class Enemies(GameEntity):
    def __init__(self, sprite, bullet_sprite, position, size, vida, screen_size, enemy_id, final_position):
        super().__init__(sprite, bullet_sprite, position, size, vida, screen_size)
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
        #El enemigo ya puede empezar a disparar?
        self.canShoot = 0

        #Sonido cuando muere
        self.dedSound = mixer.Sound("Assets/SFX/enemyDying.wav")
        self.dedSound.set_volume(0.3)

        self.final_position = final_position

        self.loadEnemy()

    def loadEnemy(self):
        if self.enemy_id == "enemigo_patron_circular":
            #Se configuran las opciones iniciales del enemigo
            self.image = image.load("Assets/Images/circular_enemy.png").convert_alpha()
            self.image = transform.scale(self.image, (tamanoDinamico(self.screen_size[0], 3.125), tamanoDinamico(self.screen_size[0], 3.125)))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.bullet_interval = 0.3
            self.bullet_vertices = 10
            self.suma_del_angulo = 360/self.bullet_vertices
            
        if self.enemy_id == "enemigo_patron_circular_alternado":
            #Se configuran las opciones iniciales del enemigo
            self.image = image.load("Assets/Images/circular_enemy.png").convert_alpha()
            self.image = transform.scale(self.image, (tamanoDinamico(self.screen_size[0], 3.125), tamanoDinamico(self.screen_size[0], 3.125)))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.bullet_interval = 0.3
            self.bullet_vertices = 10
            self.suma_del_angulo = 360/self.bullet_vertices

        if self.enemy_id == "enemigo_patron_espiral":
            #Se configuran las opciones iniciales del enemigo
            self.image = image.load("Assets/Images/circular_enemy.png").convert_alpha()
            self.image = transform.scale(self.image, (tamanoDinamico(self.screen_size[0], 3.125), tamanoDinamico(self.screen_size[0], 3.125)))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.bullet_interval = 0.3
            self.bullet_vertices = 3
            self.suma_del_angulo = 360/self.bullet_vertices
        
        if self.enemy_id == "enemigo_patron_espiral_alternado":
            #Se configuran las opciones iniciales del enemigo
            self.image = image.load("Assets/Images/circular_enemy.png").convert_alpha()
            self.image = transform.scale(self.image, (tamanoDinamico(self.screen_size[0], 3.125), tamanoDinamico(self.screen_size[0], 3.125)))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.bullet_interval = 0.3
            self.bullet_vertices = 5
            self.suma_del_angulo = 360/self.bullet_vertices
        
        if self.enemy_id == "enemigo_patron_estrella":
            #Se configuran las opciones iniciales del enemigo
            self.image = image.load("Assets/Images/circular_enemy.png").convert_alpha()
            self.image = transform.scale(self.image, (tamanoDinamico(self.screen_size[0], 3.125), tamanoDinamico(self.screen_size[0], 3.125)))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.bullet_interval = 1
            self.bullet_vertices = 30
            self.suma_del_angulo = 360/self.bullet_vertices
        
        if self.enemy_id == "enemigo_patron_spray":
            #Se configuran las opciones iniciales del enemigo
            self.image = image.load("Assets/Images/circular_enemy.png").convert_alpha()
            self.image = transform.scale(self.image, (tamanoDinamico(self.screen_size[0], 3.125), tamanoDinamico(self.screen_size[0], 3.125)))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.bullet_interval = 1
            self.bullet_vertices = 30
            self.suma_del_angulo = 360/self.bullet_vertices

    def update(self, objects, deltaTime, screen_size):
        self.screen_size = screen_size
        def ease_out(t):
            return 1.0 - (1.0 - t) * (1.0 - t)
        if self.rect.center != self.final_position:
            self.rect.centerx = math.lerp(self.rect.centerx, self.final_position[0],ease_out(0.1 * deltaTime))
            self.rect.centery = math.lerp(self.rect.centery, self.final_position[1], ease_out(0.1 * deltaTime))

        #Esta condicional depende del tipo de enemigos que se genera
        now = tm.time()
        if self.canShoot == True:            
            if now - self.ultimo_disparo > self.bullet_interval:
                # Disparar balas en un hilo separado
                shoot_thread = Thread(target=self.shoot, args=(objects,))
                shoot_thread.daemon = True
                shoot_thread.start()
                self.ultimo_disparo = now

        #Se destruye el enemigo
        if self.vida <= 0:
            self.dedSound.play()
            self.kill()

    #Esta funcion son los tipos de disparo de los enemigos
    def shoot(self, objects):
        if self.enemy_id == "enemigo_patron_circular":
            for _ in range(self.bullet_vertices):
                self.shoot_queue.put(Bullet(self.rect.center, self.angulo_actual, self.bullet_sprite[1], tamanoDinamico(self.screen_size[0], 0.390625), self.target, (tamanoDinamico(self.screen_size[0], 1.5625), tamanoDinamico(self.screen_size[0], 1.5625))))
                self.angulo_actual += self.suma_del_angulo

            # Agregar las balas a la lista principal fuera del hilo
            while not self.shoot_queue.empty():
                objects.add(self.shoot_queue.get())

        if self.enemy_id == "enemigo_patron_circular_alternado":
            for _ in range(self.bullet_vertices):
                self.shoot_queue.put(Bullet(self.rect.center, self.angulo_actual, self.bullet_sprite[3], tamanoDinamico(self.screen_size[0], 0.390625), self.target, (tamanoDinamico(self.screen_size[0], 1.5625), tamanoDinamico(self.screen_size[0], 1.5625))))
                self.angulo_actual += self.suma_del_angulo
            
            self.angulo_actual += self.suma_del_angulo * 1.5

            # Agregar las balas a la lista principal fuera del hilo
            while not self.shoot_queue.empty():
                objects.add(self.shoot_queue.get())

        if self.enemy_id == "enemigo_patron_espiral":
            for _ in range(self.bullet_vertices):
                self.shoot_queue.put(Bullet(self.rect.center, self.angulo_actual, self.bullet_sprite[2], tamanoDinamico(self.screen_size[0], 0.390625), self.target, (tamanoDinamico(self.screen_size[0], 1.5625), tamanoDinamico(self.screen_size[0], 1.5625))))
                self.angulo_actual += self.suma_del_angulo

            self.angulo_actual += tamanoDinamico(self.screen_size[0], 1.5625)

            # Agregar las balas a la lista principal fuera del hilo
            while not self.shoot_queue.empty():
                objects.add(self.shoot_queue.get())
        
        if self.enemy_id == "enemigo_patron_espiral_alternado":
            for _ in range(self.bullet_vertices):
                self.shoot_queue.put(Bullet(self.rect.center, self.angulo_actual, self.bullet_sprite[6], tamanoDinamico(self.screen_size[0], 0.390625), self.target, (tamanoDinamico(self.screen_size[0], 1.5625), tamanoDinamico(self.screen_size[0], 1.5625))))
                self.angulo_actual += self.suma_del_angulo

            self.angulo_actual -= tamanoDinamico(self.screen_size[0], 1.5625)

            # Agregar las balas a la lista principal fuera del hilo
            while not self.shoot_queue.empty():
                objects.add(self.shoot_queue.get())
        
        if self.enemy_id == "enemigo_patron_estrella":
            for _ in range(self.bullet_vertices):
                self.shoot_queue.put(Bullet(self.rect.center, self.angulo_actual, self.bullet_sprite[5], tamanoDinamico(self.screen_size[0], 0.1171875)*sin(50*self.angulo_actual * (pi/360)) + tamanoDinamico(self.screen_size[0], 0.390625), self.target, (tamanoDinamico(self.screen_size[0], 1.5625), tamanoDinamico(self.screen_size[0], 1.5625))))
                self.angulo_actual += self.suma_del_angulo
            self.angulo_actual = 0

            # Agregar las balas a la lista principal fuera del hilo
            while not self.shoot_queue.empty():
                objects.add(self.shoot_queue.get())
        
        if self.enemy_id == "enemigo_patron_spray":
            for _ in range(self.bullet_vertices):
                self.shoot_queue.put(Bullet(self.rect.center, self.angulo_actual, self.bullet_sprite[4], abs(sin(500*self.angulo_actual * (pi/360)) + tamanoDinamico(self.screen_size[0], 0.390625)), self.target, (tamanoDinamico(self.screen_size[0], 1.5625), tamanoDinamico(self.screen_size[0], 1.5625))))
                self.angulo_actual += self.suma_del_angulo
            self.angulo_actual = 0

            # Agregar las balas a la lista principal fuera del hilo
            while not self.shoot_queue.empty():
                objects.add(self.shoot_queue.get())