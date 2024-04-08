#Se importan todas las librerias necesarias
import sys
import os
import time as tm
import pickle
import pygame_gui
from pygame import *
from math import *
from random import *

#Se agrega la ruta de los modulos requeridos
sys.path.append("Assets/Python/")

#Se importan los modulos personalizados
from Assets.Python.GameEntities import Player
from Assets.Python.funciones import get_image, tamanoDinamico, save
from Assets.Python.EnemyGenerator import EnemyGenerator, SpawnPoint
from Assets.Python.UI_classes import Estrellas, Boton

#Se inicia el programa
init()

# Se inicializa las variables globales
# La resolucion que esta definida en el juego
resolucion_index: int = 3
# La puntuación máxima
max_score: int = 0
# ¿El juego esta a pantalla completa?
pantalla_completa: bool = False
# Que resolucion está seleccionada
resolucion_elegida: list[bool] = [False, False, False, True, False]
# ¿Mostrar los fps?
mostrar_fps: bool = False
# El limite de fps a los que puede ir el juego
limite_fps_texto: str = "60"
limite_fps: int = 60

# Directorio de los archivos de guardado
carpeta_guardado: str = "data"

# Se crea el directorio si no existe
if not os.path.exists(carpeta_guardado):
    os.makedirs(carpeta_guardado)

# Archivo de guardado
archivo_binario: str = os.path.join(carpeta_guardado, "save.data")


# Se carga el archivo de guardado si existe, si no se crea
if os.path.exists(archivo_binario):
    with open(archivo_binario, "rb") as f:
        resolucion_index, max_score, pantalla_completa, resolucion_elegida, mostrar_fps, limite_fps_texto, limite_fps = pickle.load(f)
else:
    save(archivo_binario, [resolucion_index, max_score, pantalla_completa, resolucion_elegida,
                           mostrar_fps, limite_fps_texto, limite_fps])

# Tamaño del monitor
MONITOR_SIZE: tuple[int, int] = (display.Info().current_w, display.Info().current_h)
# Las resoluciones disponibles
resoluciones: list[tuple[int, int]] = [(426, 240), (640, 360), (854, 480), (1280, 720), MONITOR_SIZE]

# El titulo de la pantalla
display.set_caption("Space war")
# El icono de la pantalla
display.set_icon(image.load("Assets/Icon/icon.png"))

# Pone la pantalla completa si pantalla_completa es true
if pantalla_completa:
    pantalla = display.set_mode(resoluciones[resolucion_index], FULLSCREEN, 32)
# Si no la pone con el tamaño de la resolucion elegida
else:
    pantalla = display.set_mode(resoluciones[resolucion_index], DOUBLEBUF, 32)

# Calcula el tamaño de la pantalla
anchopantalla, altopantalla = pantalla.get_size()

# Se inicializa un reloj
clock = time.Clock()


#Colores
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 0)
DARK_BLUE = (0, 1, 35)
CLAIRE_BLUE = (7, 245, 245)
TEXTO_BOTON_HOVER = (154, 237, 237)
#----------------------------

def mainMenu():
    #Se llama a la variable resolucion_elegida
    global resolucion_elegida
    anchopantalla, altopantalla = pantalla.get_size()

    # La variable que contiene todo lo de la clase estrellas "Ver en Assets/Python/UI_classes.py"
    estrellas = Estrellas(pantalla, 500, anchopantalla, altopantalla)

    bg_music = mixer.music
    bg_music.load("Assets/Music/SkyFire_(Title Screen).ogg")
    bg_music.play(-1)
    bg_music.set_volume(0.4)

    botonClick = mixer.Sound("Assets/SFX/click.mp3")
    botonHover = mixer.Sound("Assets/SFX/hoverButton.mp3")
    botonClick.set_volume(0.6)
    botonHover.set_volume(0.6)

    #Fonts
    fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(altopantalla, 2.5)))
    mainMenuFont = font.Font("Assets/Fonts/Vermin_Vibes_1989.ttf", int(tamanoDinamico(altopantalla, 15)))
    fuente_botones = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(altopantalla, 5)))

    # Titulo
    mainMenuText = mainMenuFont.render("SPACE WAR", True, WHITE)
    mainMenuShadowText = mainMenuFont.render("SPACE WAR", True, (76, 117, 117))

    # Todos los botones del menu
    botonJugar = Boton(pantalla, (tamanoDinamico(anchopantalla, 10), tamanoDinamico(altopantalla, 6)), (tamanoDinamico(anchopantalla, 50), tamanoDinamico(altopantalla, 50)),
                           fuente_botones, "JUGAR", WHITE , TEXTO_BOTON_HOVER, botonClick, botonHover, False, None, None, int(tamanoDinamico(anchopantalla, 0.3125)))
    botonOpciones = Boton(pantalla, (tamanoDinamico(anchopantalla, 16), tamanoDinamico(altopantalla, 6)), (tamanoDinamico(anchopantalla, 50), tamanoDinamico(altopantalla, 56)),
                           fuente_botones, "OPCIONES", WHITE , TEXTO_BOTON_HOVER, botonClick, botonHover, False, None, None, int(tamanoDinamico(anchopantalla, 0.3125)))

    while True:
        dt = 60/limite_fps

        #Se dibuja el fondo
        pantalla.fill(BLACK)
        estrellas.update(dt)
        
        #Muestra los fps
        if mostrar_fps:
            fps = clock.get_fps()
            fps_text = fps_font.render("FPS: " + str(int(fps//1)), True, WHITE)
            pantalla.blit(fps_text, fps_text.get_rect(center = (tamanoDinamico(anchopantalla, 97), tamanoDinamico(anchopantalla, 1))))

        # Dibuja el titulo
        pantalla.blit(mainMenuShadowText, mainMenuShadowText.get_rect(center = (tamanoDinamico(anchopantalla, 50.7), tamanoDinamico(altopantalla, 30.7))))
        pantalla.blit(mainMenuText, mainMenuText.get_rect(center= (tamanoDinamico(anchopantalla, 50), tamanoDinamico(altopantalla, 30))))

        #Event manager
        for e in event.get():
            if e.type == QUIT:
                # Guarda todas las variables necesarias
                save(archivo_binario, [resolucion_index, max_score, pantalla_completa, resolucion_elegida,
                           mostrar_fps, limite_fps_texto, limite_fps])
                # Cierra el programa
                quit()
                sys.exit()
            # Si el mouse hizo click
            if e.type == MOUSEBUTTONDOWN:
                # Si el click es del boton izquierdo
                if e.button == 1:
                    # Si el cick es en el boton asignado
                    if botonJugar.hover:
                        botonJugar.onClick(Game, True, bg_music, 0.5, estrellas)
                        bg_music.load("Assets/Music/SkyFire_(Title Screen).ogg")
                        bg_music.play(-1)
                        bg_music.set_volume(0.2)
                        
                        # Refrasca el tamaño de las estrellas
                        estrellas.refrescar(anchopantalla, altopantalla)

                    if botonOpciones.hover:
                        botonOpciones.onClick(Options, False, bg_music, 0, estrellas, resoluciones)
                        #Recalculate the size of the pantalla
                        anchopantalla, altopantalla = pantalla.get_size()
                
                        #Resize all the fonts
                        fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(altopantalla, 2.5)))
                        fuente_botones = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(altopantalla, 5)))

                        # Refrescar las estrellas
                        estrellas.refrescar(anchopantalla, altopantalla)
                    
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    # Guarda todas las variables necesarias
                    save(archivo_binario, [resolucion_index, max_score, pantalla_completa, resolucion_elegida,
                           mostrar_fps, limite_fps_texto, limite_fps])
                    # Cierra el programa
                    quit()
                    sys.exit()

        # Dibujar los botones en la pantalla
        botonJugar.update()
        botonOpciones.update()

        display.flip()
        clock.tick(limite_fps)

def Options(estrellas, resoluciones):
    global pantalla
    anchopantalla, altopantalla = pantalla.get_size()
    global resolucion_index

    #Se inicializa las varibales de manera global para que no haya conflictos y se "guarde" la resolucion
    global pantalla_completa
    global resolucion_elegida

    manager_ui = pygame_gui.UIManager(resoluciones[resolucion_index], "themeUI.json")

    #Se inicializa todas las variables necesarias para mostrar los fps
    global mostrar_fps
    global limite_fps
    global limite_fps_texto
    fps_limit_options = ["30", "60", "120", "144", "240"]

    
    #Fonts
    fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(altopantalla, 2.5)))
    title_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 4.34375)))
    option_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 2.34375)))
    select_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 2)))

    #Fps limit Text
    fps_limit_options_text = select_font.render("FPS Limit: ", True, WHITE)
    fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(fps_limit_options, limite_fps_texto,Rect(tamanoDinamico(anchopantalla, 50) + fps_limit_options_text.get_size()[0], tamanoDinamico(altopantalla, 24.5), tamanoDinamico(anchopantalla, 5), tamanoDinamico(anchopantalla, 2.5)), manager_ui, object_id="#Fps_Limit_Option")

    last_time = tm.time()
    click = False
    running = True
    while running:
        ui_refresh_rate = clock.tick(limite_fps)/1000

        #Surface with SourceAlpha
        game_window = Surface((anchopantalla, altopantalla), SRCALPHA)

        #DeltaTime
        dt = tm.time() - last_time
        dt *= 60
        last_time = tm.time()

        mx, my = mouse.get_pos()

        #Se dibuja el fondo
        pantalla.fill(BLACK)
        estrellas.update(dt)

        #Muestra los fps
        if mostrar_fps:
            fps = clock.get_fps()
            fps_text = fps_font.render("FPS: " + str(int(fps//1)), True, WHITE)
            pantalla.blit(fps_text, fps_text.get_rect(center = (tamanoDinamico(anchopantalla, 97), tamanoDinamico(anchopantalla, 1))))

        #Panel de fondo
        draw.rect(game_window, (7, 245, 245, 120), (tamanoDinamico(anchopantalla, 5), tamanoDinamico(altopantalla, 5), tamanoDinamico(anchopantalla, 90), tamanoDinamico(altopantalla, 90)), 0, int(tamanoDinamico(anchopantalla, 0.3125)))
        #Titulo
        title_text = title_font.render("OPTIONS", True, WHITE)
        game_window.blit(title_text, (tamanoDinamico(anchopantalla, 50) - title_text.get_size()[0]/2, tamanoDinamico(altopantalla, 6)))

        #Resoluciones
        resoluciones_Text = option_font.render("Resolutions", True, WHITE)
        game_window.blit(resoluciones_Text, (tamanoDinamico(anchopantalla, 7), tamanoDinamico(altopantalla, 15)))
        #Boton1
        resolution1_text = select_font.render("426 X 240", True, (0, 64, 224))
        panel_rect1 = Rect(tamanoDinamico(anchopantalla, 7), tamanoDinamico(altopantalla, 20), tamanoDinamico(anchopantalla, 20), tamanoDinamico(anchopantalla, 2.5))
        if resolucion_elegida[0]:
                    draw.rect(game_window, DARK_BLUE, panel_rect1, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
                    resolution1_text = select_font.render("426 X 240", True, WHITE)
                    game_window.blit(resolution1_text, resolution1_text.get_rect(center=(panel_rect1.centerx, panel_rect1.centery + tamanoDinamico(altopantalla, 0.3))))
        else:
            draw.rect(game_window, (180, 245, 245), panel_rect1, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
            game_window.blit(resolution1_text, resolution1_text.get_rect(center=(panel_rect1.centerx, panel_rect1.centery + tamanoDinamico(altopantalla, 0.3))))
        if panel_rect1.collidepoint(mx, my):
            #Cambia el color con hover
            draw.rect(game_window, (75, 117, 224), panel_rect1, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
            resolution1_text = select_font.render("426 X 240", True, WHITE)
            game_window.blit(resolution1_text, resolution1_text.get_rect(center=(panel_rect1.centerx, panel_rect1.centery + tamanoDinamico(altopantalla, 0.3))))
            if click:
                resolucion_index = 0
                resolucion_elegida = [True, False, False, False, False]
                if pantalla_completa:
                    pantalla = display.set_mode(resoluciones[resolucion_index], FULLSCREEN)
                else:
                    pantalla = display.set_mode(resoluciones[resolucion_index], DOUBLEBUF)

                anchopantalla, altopantalla = pantalla.get_size()
                
                #Resize all the fonts
                fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(altopantalla, 2.5)))
                title_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 4.34375)))
                option_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 2.34375)))
                select_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 2)))
                
                #Resize the manager ui
                manager_ui = pygame_gui.UIManager(resoluciones[resolucion_index], "themeUI.json")
                fps_limit_options_text = select_font.render("FPS Limit: ", True, WHITE)
                fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(fps_limit_options, limite_fps_texto,Rect(tamanoDinamico(anchopantalla, 50) + fps_limit_options_text.get_size()[0], tamanoDinamico(altopantalla, 24.5), tamanoDinamico(anchopantalla, 5), tamanoDinamico(anchopantalla, 2.5)), manager_ui, object_id="#Fps_Limit_Option")
                
                estrellas.refrescar(anchopantalla, altopantalla)

        #Boton2
        resolution2_text = select_font.render("640 X 360", True, (0, 64, 224))
        panel_rect2 = Rect(tamanoDinamico(anchopantalla, 7), tamanoDinamico(altopantalla, 25), tamanoDinamico(anchopantalla, 20), tamanoDinamico(anchopantalla, 2.5))
        if resolucion_elegida[1]:
                    draw.rect(game_window, DARK_BLUE, panel_rect2, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
                    resolution2_text = select_font.render("640 X 360", True, WHITE)
                    game_window.blit(resolution2_text, resolution2_text.get_rect(center=(panel_rect2.centerx, panel_rect2.centery + tamanoDinamico(altopantalla, 0.3))))
        else:
            draw.rect(game_window, (180, 245, 245), panel_rect2, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
            game_window.blit(resolution2_text, resolution2_text.get_rect(center=(panel_rect2.centerx, panel_rect2.centery + tamanoDinamico(altopantalla, 0.3))))
        if panel_rect2.collidepoint(mx, my):
            #Cambia el color con hover
            draw.rect(game_window, (75, 117, 224), panel_rect2, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
            resolution2_text = select_font.render("640 X 360", True, WHITE)
            game_window.blit(resolution2_text, resolution2_text.get_rect(center=(panel_rect2.centerx, panel_rect2.centery + tamanoDinamico(altopantalla, 0.3))))
            if click:
                resolucion_index = 1
                resolucion_elegida = [False, True, False, False, False]
                if pantalla_completa:
                    pantalla = display.set_mode(resoluciones[resolucion_index], FULLSCREEN)
                else:
                    pantalla = display.set_mode(resoluciones[resolucion_index], DOUBLEBUF)

                anchopantalla, altopantalla = pantalla.get_size()
                
                #Resize all the fonts
                fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(altopantalla, 2.5)))
                title_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 4.34375)))
                option_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 2.34375)))
                select_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 2)))
                
                #Resize the manager ui
                manager_ui = pygame_gui.UIManager(resoluciones[resolucion_index], "themeUI.json")
                fps_limit_options_text = select_font.render("FPS Limit: ", True, WHITE)
                fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(fps_limit_options, limite_fps_texto,Rect(tamanoDinamico(anchopantalla, 50) + fps_limit_options_text.get_size()[0], tamanoDinamico(altopantalla, 24.5), tamanoDinamico(anchopantalla, 5), tamanoDinamico(anchopantalla, 2.5)), manager_ui, object_id="#Fps_Limit_Option")

                estrellas.refrescar(anchopantalla, altopantalla)
        #Boton3
        resolution3_text = select_font.render("854 X 480", True, (0, 64, 224))
        panel_rect3 = Rect(tamanoDinamico(anchopantalla, 7), tamanoDinamico(altopantalla, 30), tamanoDinamico(anchopantalla, 20), tamanoDinamico(anchopantalla, 2.5))
        if resolucion_elegida[2]:
                    draw.rect(game_window, DARK_BLUE, panel_rect3, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
                    resolution3_text = select_font.render("854 X 480", True, WHITE)
                    game_window.blit(resolution3_text, resolution3_text.get_rect(center=(panel_rect3.centerx, panel_rect3.centery + tamanoDinamico(altopantalla, 0.3))))
        else:
            draw.rect(game_window, (180, 245, 245), panel_rect3, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
            game_window.blit(resolution3_text, resolution3_text.get_rect(center=(panel_rect3.centerx, panel_rect3.centery + tamanoDinamico(altopantalla, 0.3))))
        if panel_rect3.collidepoint(mx, my):
            #Cambia el color con hover
            draw.rect(game_window, (75, 117, 224), panel_rect3, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
            resolution3_text = select_font.render("854 X 480", True, WHITE)
            game_window.blit(resolution3_text, resolution3_text.get_rect(center=(panel_rect3.centerx, panel_rect3.centery + tamanoDinamico(altopantalla, 0.3))))
            if click:
                resolucion_index = 2
                resolucion_elegida = [False, False, True, False, False]
                if pantalla_completa:
                    pantalla = display.set_mode(resoluciones[resolucion_index], FULLSCREEN)
                else:
                    pantalla = display.set_mode(resoluciones[resolucion_index], DOUBLEBUF)

                anchopantalla, altopantalla = pantalla.get_size()
                
                #Resize all the fonts
                fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(altopantalla, 2.5)))
                title_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 4.34375)))
                option_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 2.34375)))
                select_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 2)))
                
                #Resize the manager ui
                manager_ui = pygame_gui.UIManager(resoluciones[resolucion_index], "themeUI.json")
                fps_limit_options_text = select_font.render("FPS Limit: ", True, WHITE)
                fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(fps_limit_options, limite_fps_texto,Rect(tamanoDinamico(anchopantalla, 50) + fps_limit_options_text.get_size()[0], tamanoDinamico(altopantalla, 24.5), tamanoDinamico(anchopantalla, 5), tamanoDinamico(anchopantalla, 2.5)), manager_ui, object_id="#Fps_Limit_Option")

                estrellas.refrescar(anchopantalla, altopantalla)
        #Boton4
        resolution4_text = select_font.render("1280 X 720", True, (0, 64, 224))
        panel_rect4 = Rect(tamanoDinamico(anchopantalla, 7), tamanoDinamico(altopantalla, 35), tamanoDinamico(anchopantalla, 20), tamanoDinamico(anchopantalla, 2.5))
        if resolucion_elegida[3]:
                    draw.rect(game_window, DARK_BLUE, panel_rect4, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
                    resolution4_text = select_font.render("1280 X 720", True, WHITE)
                    game_window.blit(resolution4_text, resolution4_text.get_rect(center=(panel_rect4.centerx, panel_rect4.centery + tamanoDinamico(altopantalla, 0.3))))
        else:
            draw.rect(game_window, (180, 245, 245), panel_rect4, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
            game_window.blit(resolution4_text, resolution4_text.get_rect(center=(panel_rect4.centerx, panel_rect4.centery + tamanoDinamico(altopantalla, 0.3))))
        if panel_rect4.collidepoint(mx, my):
            #Cambia el color con hover
            draw.rect(game_window, (75, 117, 224), panel_rect4, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
            resolution4_text = select_font.render("1280 X 720", True, WHITE)
            game_window.blit(resolution4_text, resolution4_text.get_rect(center=(panel_rect4.centerx, panel_rect4.centery + tamanoDinamico(altopantalla, 0.3))))
            if click:
                resolucion_index = 3
                resolucion_elegida = [False, False, False, True, False]
                if pantalla_completa:
                    pantalla = display.set_mode(resoluciones[resolucion_index], FULLSCREEN)
                else:
                    pantalla = display.set_mode(resoluciones[resolucion_index], DOUBLEBUF)

                anchopantalla, altopantalla = pantalla.get_size()
                
                #Resize all the fonts
                fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(altopantalla, 2.5)))
                title_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 4.34375)))
                option_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 2.34375)))
                select_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 2)))
                
                #Resize the manager ui
                manager_ui = pygame_gui.UIManager(resoluciones[resolucion_index], "themeUI.json")
                fps_limit_options_text = select_font.render("FPS Limit: ", True, WHITE)
                fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(fps_limit_options, limite_fps_texto,Rect(tamanoDinamico(anchopantalla, 50) + fps_limit_options_text.get_size()[0], tamanoDinamico(altopantalla, 24.5), tamanoDinamico(anchopantalla, 5), tamanoDinamico(anchopantalla, 2.5)), manager_ui, object_id="#Fps_Limit_Option")

                estrellas.refrescar(anchopantalla, altopantalla)
        #Boton5
        resolution5_text = select_font.render(str(MONITOR_SIZE[0]) + " X " +  str(MONITOR_SIZE[1]), True, (0, 64, 224))
        panel_rect5 = Rect(tamanoDinamico(anchopantalla, 7), tamanoDinamico(altopantalla, 40), tamanoDinamico(anchopantalla, 20), tamanoDinamico(anchopantalla, 2.5))
        if resolucion_elegida[4]:
            draw.rect(game_window, DARK_BLUE, panel_rect5, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
            resolution5_text = select_font.render(str(MONITOR_SIZE[0]) + " X " +  str(MONITOR_SIZE[1]), True, WHITE)
            game_window.blit(resolution5_text, resolution5_text.get_rect(center=(panel_rect5.centerx, panel_rect5.centery + tamanoDinamico(altopantalla, 0.3))))
        else:
            draw.rect(game_window, (180, 245, 245), panel_rect5, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
            game_window.blit(resolution5_text, resolution5_text.get_rect(center=(panel_rect5.centerx, panel_rect5.centery + tamanoDinamico(altopantalla, 0.3))))
        if panel_rect5.collidepoint(mx, my):
            #Cambia el color con hover
            draw.rect(game_window, (75, 117, 224), panel_rect5, 0, int(tamanoDinamico(anchopantalla, 0.3125 * 8)))
            resolution5_text = select_font.render(str(MONITOR_SIZE[0]) + " X " +  str(MONITOR_SIZE[1]), True, WHITE)
            game_window.blit(resolution5_text, resolution5_text.get_rect(center=(panel_rect5.centerx, panel_rect5.centery + tamanoDinamico(altopantalla, 0.3))))
            if click:
                resolucion_index = 4
                resolucion_elegida = [False, False, False, False, True]
                if pantalla_completa:
                    pantalla = display.set_mode(resoluciones[resolucion_index], FULLSCREEN)
                else:
                    pantalla = display.set_mode(resoluciones[resolucion_index], DOUBLEBUF)

                anchopantalla, altopantalla = pantalla.get_size()
                
                #Resize all the fonts
                fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(altopantalla, 2.5)))
                title_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 4.34375)))
                option_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 2.34375)))
                select_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 2)))

                #Resize the manager ui
                manager_ui = pygame_gui.UIManager(resoluciones[resolucion_index], "themeUI.json")
                fps_limit_options_text = select_font.render("FPS Limit: ", True, WHITE)
                fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(fps_limit_options, limite_fps_texto,Rect(tamanoDinamico(anchopantalla, 50) + fps_limit_options_text.get_size()[0], tamanoDinamico(altopantalla, 24.5), tamanoDinamico(anchopantalla, 5), tamanoDinamico(anchopantalla, 2.5)), manager_ui, object_id="#Fps_Limit_Option")
                
                estrellas.refrescar(anchopantalla, altopantalla)
        #Toogle FullScreen
        resolution6_text = select_font.render("FullScreen", True, WHITE)
        game_window.blit(resolution6_text, resolution6_text.get_rect(center=(panel_rect5.x + resolution6_text.get_size()[0]/2, tamanoDinamico(altopantalla, 50))))
        cube_Rect = Rect(tamanoDinamico(anchopantalla, 8) + resolution6_text.get_size()[0], tamanoDinamico(altopantalla, 48), resolution6_text.get_size()[1], resolution6_text.get_size()[1])
        draw.rect(game_window, WHITE, cube_Rect, int(tamanoDinamico(anchopantalla, 0.3125)), int(tamanoDinamico(anchopantalla, 0.3125)))
        if pantalla_completa:
                draw.circle(game_window, WHITE, cube_Rect.center, tamanoDinamico(anchopantalla, 0.5))
        if cube_Rect.collidepoint(mx, my):
            #Cambia el color con hover
            draw.rect(game_window, (75, 117, 224), cube_Rect, int(tamanoDinamico(anchopantalla, 0.3125)), int(tamanoDinamico(anchopantalla, 0.3125)))
            if pantalla_completa:
                draw.circle(game_window, (75, 117, 224), cube_Rect.center, tamanoDinamico(anchopantalla, 0.5))
            if click:
                pantalla_completa = not pantalla_completa
                if pantalla_completa:
                    pantalla = display.set_mode(resoluciones[resolucion_index], FULLSCREEN)
                else:
                    if resolucion_elegida[0]:
                        resolucion_index = 0
                    elif resolucion_elegida[1]:
                        resolucion_index = 1
                    elif resolucion_elegida[2]:
                        resolucion_index = 2
                    elif resolucion_elegida[3]:
                        resolucion_index = 3
                    elif resolucion_elegida[4]:
                        resolucion_index = 4
                    pantalla = display.set_mode(resoluciones[resolucion_index], DOUBLEBUF)

                anchopantalla, altopantalla = pantalla.get_size()

                #Resize all the fonts
                title_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 4.34375)))
                option_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 2.34375)))
                select_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(anchopantalla, 2)))

                #Resize the manager ui
                manager_ui = pygame_gui.UIManager(resoluciones[resolucion_index], "themeUI.json")
                fps_limit_options_text = select_font.render("FPS Limit: ", True, WHITE)
                fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(fps_limit_options, limite_fps_texto,Rect(tamanoDinamico(anchopantalla, 50) + fps_limit_options_text.get_size()[0], tamanoDinamico(altopantalla, 24.5), tamanoDinamico(anchopantalla, 5), tamanoDinamico(anchopantalla, 2.5)), manager_ui, object_id="#Fps_Limit_Option")

                estrellas.refrescar(anchopantalla, altopantalla)

        #FPS Control
        fpsControl_Text = option_font.render("FPS Control", True, WHITE)
        game_window.blit(fpsControl_Text, (tamanoDinamico(anchopantalla, 50), tamanoDinamico(altopantalla, 15)))

        #Toogle Show FPS
        showFPS_text = select_font.render("Show FPS", True, WHITE)
        game_window.blit(showFPS_text, showFPS_text.get_rect(center=(tamanoDinamico(anchopantalla, 50) + showFPS_text.get_size()[0]/2, tamanoDinamico(altopantalla, 22))))
        cube_Rect_showFPS = Rect(tamanoDinamico(anchopantalla, 51) + showFPS_text.get_size()[0], tamanoDinamico(altopantalla, 20), resolution6_text.get_size()[1], resolution6_text.get_size()[1])
        draw.rect(game_window, WHITE, cube_Rect_showFPS, int(tamanoDinamico(anchopantalla, 0.3125)), int(tamanoDinamico(anchopantalla, 0.3125)))
        if mostrar_fps:
            draw.circle(game_window, WHITE, cube_Rect_showFPS.center, tamanoDinamico(anchopantalla, 0.5))
        if cube_Rect_showFPS.collidepoint(mx, my):
            #Cambia el color con hover
            draw.rect(game_window, (75, 117, 224), cube_Rect_showFPS, int(tamanoDinamico(anchopantalla, 0.3125)), int(tamanoDinamico(anchopantalla, 0.3125)))
            if mostrar_fps:
                draw.circle(game_window, (75, 117, 224), cube_Rect_showFPS.center, tamanoDinamico(anchopantalla, 0.5))
            if click:
                mostrar_fps = not mostrar_fps

        #Draw fps limit on pantalla
        game_window.blit(fps_limit_options_text, (tamanoDinamico(anchopantalla, 50), tamanoDinamico(altopantalla, 25.5)))
        

        #event manager
        click = False
        for e in event.get():
            if e.type == QUIT:
                save(archivo_binario, [resolucion_index, max_score, pantalla_completa, resolucion_elegida,
                           mostrar_fps, limite_fps_texto, limite_fps])

                quit()
                sys.exit()

            manager_ui.process_events(e)
            if e.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                limite_fps_texto = e.text
                for option in fps_limit_options:
                    if limite_fps_texto == option:
                        limite_fps = int(e.text)

            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    running = False

        manager_ui.update(ui_refresh_rate)
        manager_ui.draw_ui(game_window)
        pantalla.blit(game_window, (0,0))
        display.flip()
        clock.tick(limite_fps)

def Game(estrellas):
    global resolucion_elegida
    global limite_fps
    anchopantalla, altopantalla = pantalla.get_size()
    game_surface = Surface((anchopantalla, altopantalla))

    #Musica de fondo
    bg_game_music  = mixer.music
    bg_game_music.load("Assets/Music/Rain_of_Lasers.ogg")
    bg_game_music.play(-1)
    bg_game_music.set_volume(0.2)

    #Sonidos
    punch2 = mixer.Sound("Assets/SFX/punch2.wav")
    punch2.set_volume(0.5)
    #Grupos
    bullets = sprite.Group()
    enemies = sprite.Group()
    playerGroup = sprite.Group()

    #Se inicializa todas las variables necesarias para mostrar los fps
    global fps_font
    global mostrar_fps
    
    #----------------------------
    #Sprite sheets
    playerSheet = image.load("Assets/Images/SpaceShip_sheet.png").convert_alpha()
    bulletsSheet = image.load("Assets/Images/Bullets_sheet.png").convert_alpha()
    #----------------------------

    #Fonts
    fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(altopantalla, 2.5)))
    coins_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(altopantalla, 3)))
    player_lifes_font = font.Font("Assets/Fonts/Minecraft.ttf", int(tamanoDinamico(altopantalla, 4)))

    #Se guardan todas las balas en un array
    bullet_array = [get_image(bulletsSheet, 0, 24, 24, BLACK),
                    get_image(bulletsSheet, 1, 24, 24, BLACK),
                    get_image(bulletsSheet, 2, 24, 24, BLACK),
                    get_image(bulletsSheet, 3, 24, 24, BLACK),
                    get_image(bulletsSheet, 4, 24, 24, BLACK),
                    get_image(bulletsSheet, 5, 24, 24, BLACK),
                    get_image(bulletsSheet, 6, 24, 24, BLACK)]

    #Posibles posiciones de un enemigo
    enemyPos = [SpawnPoint((tamanoDinamico(anchopantalla, 25), tamanoDinamico(altopantalla, 10))), 
                SpawnPoint((tamanoDinamico(anchopantalla, 75), tamanoDinamico(altopantalla, 10))),
                SpawnPoint((tamanoDinamico(anchopantalla, 25), tamanoDinamico(altopantalla, 90))),
                SpawnPoint((tamanoDinamico(anchopantalla, 75), tamanoDinamico(altopantalla, 90))),
                SpawnPoint((tamanoDinamico(anchopantalla, 50), tamanoDinamico(altopantalla, 20))),
                SpawnPoint((tamanoDinamico(anchopantalla, 50), tamanoDinamico(altopantalla, 80))),
                SpawnPoint((tamanoDinamico(anchopantalla, 10), tamanoDinamico(altopantalla, 50))),
                SpawnPoint((tamanoDinamico(anchopantalla, 90), tamanoDinamico(altopantalla, 50)))]

    enemyID = ["enemigo_patron_circular", 
            "enemigo_patron_espiral",
            "enemigo_patron_espiral_alternado", 
            "enemigo_patron_circular_alternado",
            "enemigo_patron_estrella",
            "enemigo_patron_spray"]

    #Objetos
    player = Player(get_image(playerSheet, 0, 52, 52, BLACK), bullet_array[0], (tamanoDinamico(anchopantalla, 50), tamanoDinamico(altopantalla, 90)), (tamanoDinamico(anchopantalla, 3), tamanoDinamico(anchopantalla, 3)), 3, (anchopantalla, altopantalla))
    player_life_image = transform.scale(image.load("Assets/Images/heart.png"), (tamanoDinamico(anchopantalla, 3), tamanoDinamico(anchopantalla, 3)))

    playerCollide = Rect(player.rect.x, player.rect.y, tamanoDinamico(anchopantalla, 0.5), tamanoDinamico(anchopantalla, 0.5))
    playerGroup.add(player)
    enemyGenerator = EnemyGenerator(enemies, enemyPos, 0, enemyID, bullet_array, "easy", pantalla, (anchopantalla, altopantalla))
    coins = 0
    screen_shake = 0
    #----------------------------
    last_time = tm.time()#Esta variabe sirve para calcular el deltaTime
    running = True
    while running:

        #DeltaTime
        dt = tm.time() - last_time
        dt *= 60
        last_time = tm.time()

        playerCollide.center = player.rect.center

        #Screen shake logic
        if screen_shake > 0:
            screen_shake -= 1 * dt
        if screen_shake < 0:
            screen_shake = 0

        render_offset = [0, 0]
        if screen_shake:
            render_offset[0] = randint(0, 10) - 4
            render_offset[1] = randint(0, 10) - 4

        pantalla.blit(game_surface, render_offset)

        #Dibuja el fondo
        game_surface.fill(BLACK)
        estrellas.update(dt)


        #Muestra los fps
        if mostrar_fps:
            fps = clock.get_fps()
            fps_text = fps_font.render("FPS: " + str(int(fps//1)), True, WHITE)
            pantalla.blit(fps_text, fps_text.get_rect(center = (tamanoDinamico(anchopantalla, 97), tamanoDinamico(anchopantalla, 1))))

        #Muestra el puntaje
        coins_text = coins_font.render("Score: " + str(coins), True, WHITE)
        pantalla.blit(coins_text, (tamanoDinamico(anchopantalla , 2), tamanoDinamico(altopantalla, 2)))

        #Muestra la vida
        player_lifes_text = player_lifes_font.render("X " + str(player.vida -1), True, (255, 105, 84))
        pantalla.blit(player_life_image, (tamanoDinamico(anchopantalla, 2), tamanoDinamico(altopantalla, 6)))
        pantalla.blit(player_lifes_text, player_lifes_text.get_rect(center = (tamanoDinamico(anchopantalla, 2) + (player_life_image.get_size()[0] + 3 + (player_lifes_text.get_size()[0]/2)), tamanoDinamico(altopantalla, 6) + player_life_image.get_size()[1]/2)))

        #Event manager
        for e in event.get():
            if e.type == QUIT:
                save(archivo_binario, [resolucion_index, max_score, pantalla_completa, resolucion_elegida,
                           mostrar_fps, limite_fps_texto, limite_fps])

                quit()
                sys.exit()
            if e.type == KEYDOWN:
                if e.key == K_f:
                    enemyGenerator.generateEnemy()
                if e.key == K_ESCAPE:
                    running = False
            #Para que funcione el disparo
            player.Shoot(e, bullets)

        #Logica principal del juego

        screen_rect = display.get_surface().get_rect()

        #Posicion del mouse
        mouse_pos = mouse.get_pos()

        #Logica de las colisiones
        bullets_to_enemies = sprite.groupcollide(enemies, bullets, False, False)

        for enemy, bullet in bullets_to_enemies.items():
            for b in bullet:
                if b.bullet_target == "enemies":
                    enemy.take_damage(1)
                    b.kill()

        for bullet in bullets:
            if bullet.bullet_target == "player" and playerCollide.colliderect(bullet.rect):
                screen_shake = 30
                punch2.play()
                player.take_damage(1)
                bullet.kill()
        #Si mueres te devuelve al menu principal
        if player.isDead:
            bg_game_music.unload()
            running = False

            #Update de los objetos de la escena
        for position in enemyPos:
            position.update(enemies)           
        playerGroup.update(dt, mouse_pos, (anchopantalla, altopantalla))
        for enemy in enemies:
            if enemy.vida == 0:
                coins += 1
        enemies.update(bullets, dt, (anchopantalla, altopantalla))
        enemyGenerator.update((anchopantalla, altopantalla))
        bullets.update(screen_rect, dt)
        #-----------------

        #Configuración de la pantalla (In-Game)
        playerGroup.draw(game_surface) #Se dibuja el player en pantalla
        bullets.draw(game_surface)
        enemies.draw(game_surface)

        display.flip()

        clock.tick(limite_fps)#Control de los fps o cuadros por segundo
        #-----------------


mainMenu()

save(archivo_binario, [resolucion_index, max_score, pantalla_completa, resolucion_elegida,
                           mostrar_fps, limite_fps_texto, limite_fps])

quit()
sys.exit()