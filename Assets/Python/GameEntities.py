import time as tm
from threading import Thread
from pygame import *
from math import *
from queue import *
from Assets.Python.BulletClass import Bullet
from Assets.Python.funciones import tamanoDinamico

class GameEntity(sprite.Sprite):
    """
    A class to represent a game entity.

    ...

    Attributes
    ----------
    path : str
        the path to the assets folder
    originalSprite : pygame.Surface
        the original sprite of the entity
    image : pygame.Surface
        the current sprite of the entity
    position : tuple[int, int]
        the position of the entity
    rect : pygame.Rect
        the rect of the entity
    vida : int
        the life of the entity
    bullet_sprite : pygame.Surface
        the sprite of the bullet
    screen_size : tuple[int, int]
        the size of the screen

    Methods
    -------
    take_damage(amount):
        Reduces the life of the entity.
    resize(sizeX, sizeY):
        Resizes the entity.
    """
    def __init__(self, path: str, sprite, bullet_sprite, position, size, vida, screen_size):
        """
        Constructs all the necessary attributes for the game entity object.

        Parameters
        ----------
            path : str
                the path to the assets folder
            sprite : pygame.Surface
                the sprite of the entity
            bullet_sprite : pygame.Surface
                the sprite of the bullet
            position : tuple[int, int]
                the position of the entity
            size : tuple[int, int]
                the size of the entity
            vida : int
                the life of the entity
            screen_size : tuple[int, int]
                the size of the screen
        """
        super().__init__()
        self.path: str = path
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
        """
        Reduces the life of the entity.

        Parameters
        ----------
            amount : int
                the amount of damage
        """
        self.vida -= amount
    
    def resize(self, sizeX, sizeY):
        """
        Resizes the entity.

        Parameters
        ----------
            sizeX : int
                the new width of the entity
            sizeY : int
                the new height of the entity
        """
        self.image = transform.scale(self.image, (sizeX, sizeY))

class Player(GameEntity):
    """
    A class to represent the player.

    ...

    Attributes
    ----------
    velocityX : int
        the velocity of the player in the x axis
    velocityY : int
        the velocity of the player in the y axis
    angle : int
        the angle of the player
    mouse_pos : int
        the position of the mouse
    target : str
        the target of the bullets
    vida : int
        the life of the player
    isDead : bool
        whether the player is dead or not
    shootSound : pygame.mixer.Sound
        the sound of the shoot

    Methods
    -------
    update(deltaTime, mouse_pos, screen_size):
        Updates the player.
    Shoot(event, objects):
        Shoots a bullet.
    """
    def __init__(self, path, sprite, bullet_sprite, position, size, vida, screen_size):
        """
        Constructs all the necessary attributes for the player object.

        Parameters
        ----------
            path : str
                the path to the assets folder
            sprite : pygame.Surface
                the sprite of the player
            bullet_sprite : pygame.Surface
                the sprite of the bullet
            position : tuple[int, int]
                the position of the player
            size : tuple[int, int]
                the size of the player
            vida : int
                the life of the player
            screen_size : tuple[int, int]
                the size of the screen
        """
        super().__init__(path, sprite, bullet_sprite, position, size, vida, screen_size)
        self.velocityX = 0
        self.velocityY = 0
        self.angle = 0
        self.mouse_pos = 0
        self.target = "enemies" #Define a quien va a dañar la bala que se spawnea
        self.vida = vida
        self.isDead = False
        self.shootSound = mixer.Sound(self.path + "SFX/laser_beam.mp3")
        self.shootSound.set_volume(0.3)

    def update(self, deltaTime,  mouse_pos, screen_size):
        """
        Updates the player.

        Parameters
        ----------
            deltaTime : float
                the time since the last frame
            mouse_pos : tuple[int, int]
                the position of the mouse
            screen_size : tuple[int, int]
                the size of the screen
        """
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
        """
        Shoots a bullet.

        Parameters
        ----------
            event : pygame.event.Event
                the event
            objects : pygame.sprite.Group
                the group of objects
        """
        if event.type == MOUSEBUTTONDOWN and event.button == 1 and not self.isDead:
            self.shootSound.play()
            objects.add(Bullet(self.rect.center, self.angle, self.bullet_sprite, tamanoDinamico(self.screen_size[0], 1.5625), self.target, (tamanoDinamico(self.screen_size[0], 1.5625), tamanoDinamico(self.screen_size[0], 1.5625))))

#Esta clase es para todos los tipos de enemigos del juego
class Enemies(GameEntity):
    """
    A class to represent the enemies.

    ...

    Attributes
    ----------
    enemy_id : str
        the id of the enemy
    bullet_interval : int
        the interval of the bullets
    bullet_vertices : int
        the vertices of the bullets
    suma_del_angulo : int
        the sum of the angle
    angulo_actual : int
        the current angle
    ultimo_disparo : float
        the time of the last shot
    shoot_queue : Queue
        the queue of the shoots
    target : str
        the target of the bullets
    canShoot : int
        whether the enemy can shoot or not
    dedSound : pygame.mixer.Sound
        the sound of the death
    final_position : tuple[int, int]
        the final position of the enemy

    Methods
    -------
    loadEnemy():
        Loads the enemy.
    update(objects, deltaTime, screen_size):
        Updates the enemy.
    shoot(objects):
        Shoots a bullet.
    """
    def __init__(self, path, sprite, bullet_sprite, position, size, vida, screen_size, enemy_id, final_position):
        """
        Constructs all the necessary attributes for the enemies object.

        Parameters
        ----------
            path : str
                the path to the assets folder
            sprite : pygame.Surface
                the sprite of the enemy
            bullet_sprite : pygame.Surface
                the sprite of the bullet
            position : tuple[int, int]
                the position of the enemy
            size : tuple[int, int]
                the size of the enemy
            vida : int
                the life of the enemy
            screen_size : tuple[int, int]
                the size of the screen
            enemy_id : str
                the id of the enemy
            final_position : tuple[int, int]
                the final position of the enemy
        """
        super().__init__(path, sprite, bullet_sprite, position, size, vida, screen_size)
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
        self.dedSound = mixer.Sound(self.path + "SFX/enemyDying.wav")
        self.dedSound.set_volume(0.3)

        self.final_position = final_position

        self.loadEnemy()

    def loadEnemy(self):
        """
        Loads the enemy.
        """
        if self.enemy_id == "enemigo_patron_circular":
            #Se configuran las opciones iniciales del enemigo
            self.image = image.load(self.path + "Images/circular_enemy.png").convert_alpha()
            self.image = transform.scale(self.image, (tamanoDinamico(self.screen_size[0], 3.125), tamanoDinamico(self.screen_size[0], 3.125)))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.bullet_interval = 0.3
            self.bullet_vertices = 10
            self.suma_del_angulo = 360/self.bullet_vertices
            
        if self.enemy_id == "enemigo_patron_circular_alternado":
            #Se configuran las opciones iniciales del enemigo
            self.image = image.load(self.path + "Images/circular_enemy.png").convert_alpha()
            self.image = transform.scale(self.image, (tamanoDinamico(self.screen_size[0], 3.125), tamanoDinamico(self.screen_size[0], 3.125)))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.bullet_interval = 0.3
            self.bullet_vertices = 10
            self.suma_del_angulo = 360/self.bullet_vertices

        if self.enemy_id == "enemigo_patron_espiral":
            #Se configuran las opciones iniciales del enemigo
            self.image = image.load(self.path + "Images/circular_enemy.png").convert_alpha()
            self.image = transform.scale(self.image, (tamanoDinamico(self.screen_size[0], 3.125), tamanoDinamico(self.screen_size[0], 3.125)))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.bullet_interval = 0.3
            self.bullet_vertices = 3
            self.suma_del_angulo = 360/self.bullet_vertices
        
        if self.enemy_id == "enemigo_patron_espiral_alternado":
            #Se configuran las opciones iniciales del enemigo
            self.image = image.load(self.path + "Images/circular_enemy.png").convert_alpha()
            self.image = transform.scale(self.image, (tamanoDinamico(self.screen_size[0], 3.125), tamanoDinamico(self.screen_size[0], 3.125)))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.bullet_interval = 0.3
            self.bullet_vertices = 5
            self.suma_del_angulo = 360/self.bullet_vertices
        
        if self.enemy_id == "enemigo_patron_estrella":
            #Se configuran las opciones iniciales del enemigo
            self.image = image.load(self.path + "Images/circular_enemy.png").convert_alpha()
            self.image = transform.scale(self.image, (tamanoDinamico(self.screen_size[0], 3.125), tamanoDinamico(self.screen_size[0], 3.125)))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.bullet_interval = 1
            self.bullet_vertices = 30
            self.suma_del_angulo = 360/self.bullet_vertices
        
        if self.enemy_id == "enemigo_patron_spray":
            #Se configuran las opciones iniciales del enemigo
            self.image = image.load(self.path + "Images/circular_enemy.png").convert_alpha()
            self.image = transform.scale(self.image, (tamanoDinamico(self.screen_size[0], 3.125), tamanoDinamico(self.screen_size[0], 3.125)))
            self.rect = self.image.get_rect()
            self.rect.center = self.position
            self.bullet_interval = 1
            self.bullet_vertices = 30
            self.suma_del_angulo = 360/self.bullet_vertices

    def update(self, objects, deltaTime, screen_size):
        """
        Updates the enemy.

        Parameters
        ----------
            objects : pygame.sprite.Group
                the group of objects
            deltaTime : float
                the time since the last frame
            screen_size : tuple[int, int]
                the size of the screen
        """
        self.screen_size = screen_size
        
        def ease_out(t):
            return 1.0 - (1.0 - t) * (1.0 - t)
        
        if self.rect.center != self.final_position:
            self.rect.centerx = math.lerp(self.rect.centerx, self.final_position[0], ease_out(0.1 * deltaTime))
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
        """
        Shoots a bullet.

        Parameters
        ----------
            objects : pygame.sprite.Group
                the group of objects
        """
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