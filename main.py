from pygame import *
from math import *

#Se importan las clases y demás
from GameEntities import Player

#Se inicia el programa
init()

#Configuración de la pantalla
resolucion = (1920, 1080)
screen = display.set_mode(resolucion, FULLSCREEN)
clock = time.Clock()
screen_size = screen.get_size()
#----------------------------

#Colores
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 0)
DARK_BLUE = (0, 1, 35, 14)
#----------------------------

#Variables
player_sprite = "Assets/tiny_ship14.png"
bullet_sprites = "Assets/laser_beam.png"
#----------------------------

#Objetos
All_sprite_in_game = sprite.Group()
player = Player(player_sprite, bullet_sprites, 500, 500, 40, 40, 10)
#----------------------------

#Logica de los niveles o pantallas
running = True
#----------------------------

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        #Para que funcione el disparo
        player.Shoot(e, All_sprite_in_game)

    screen.fill(DARK_BLUE)

    #Logica principal del juego

    screen_rect = display.get_surface().get_rect()

    #Posicion del mouse
    mouse_pos = mouse.get_pos()

    player.update(player_sprite, mouse_pos, screen_size)
    screen.blit(player.image, player.rect)
    All_sprite_in_game.update(screen_rect)
    #-----------------

    #Configuración de la pantalla (In-Game)
    All_sprite_in_game.draw(screen)
    display.flip()
    #Control de los fps o cuadros por segundo
    clock.tick(60)
    #-----------------

quit()