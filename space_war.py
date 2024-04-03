import sys
import os
import pickle
from pygame import *
import pygame_gui
from math import *
from random import *
import time as tm

sys.path.append("Assets/Python/")

#Se importan las clases y demás
from GameEntities import Player
from funciones import get_image, responsiveSizeAndPosition
from EnemyGenerator import EnemyGenerator, SpawnPoint

#Se inicia el programa
init()

resolution_index = 3
#Max score
max_score = 0
#Control de las resoluciones
fullscreen = False
selected = [False, False, False, True, False]
#Show FPS?
fps_show = False
selectedOption = "60"
#El limite de fps a los que puede ir el juego
FPS_Limit = 60

#Directorio de los guardados
saveDirectory = "save"

#Se crea la carpeta si no existe
if not os.path.exists(saveDirectory):
    os.makedirs(saveDirectory, mode=0o700)

#Archivo de guardado
binaryArchive = os.path.join(saveDirectory, "save.gayTheOneWhoEdits")


#Se carga el archivo de guardado si existe, si no se crea
if os.path.exists(binaryArchive):
    with open(binaryArchive, "rb") as f:
        resolution_index, max_score, fullscreen = pickle.load(f)
        selected = pickle.load(f)
        fps_show, selectedOption, FPS_Limit = pickle.load(f)
else:
    with open(binaryArchive, "wb") as f:
        pickle.dump((resolution_index, max_score, fullscreen), f)
        pickle.dump(selected, f)
        pickle.dump((fps_show, selectedOption, FPS_Limit), f)

#Configuración de la pantalla
MONITOR_SIZE = [display.Info().current_w, display.Info().current_h]
resolutions = [(426, 240), (640, 360), (854, 480), (1280, 720), MONITOR_SIZE]

screen = display.set_caption("Space war")
if fullscreen:
    screen = display.set_mode(resolutions[resolution_index], FULLSCREEN, 32)
else:
    screen = display.set_mode(resolutions[resolution_index], DOUBLEBUF, 32)
screen_size = screen.get_size()
clock = time.Clock()
#----------------------------

#Colores
WHITE = (255, 255, 255, 255)
BLACK = (0, 0, 0, 0)
DARK_BLUE = (0, 1, 35)
CLAIRE_BLUE = (7, 245, 245)
#----------------------------

#Pantallas
def mainMenu():
    global selected
    click = False
    screen_size = screen.get_size()

    stars = []
    for _ in range(500):
            randomWhite = randint(150, 230)
            randSize = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.390625)))
            randSpeed = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.78125)))
            particleRect = Rect(uniform(0, screen_size[0]), uniform(0, screen_size[1]), randSize, randSize)
            stars.append([[randomWhite, randomWhite, randomWhite], [particleRect.x, particleRect.y], randSize, randSpeed])

    click = False
    bg_music = mixer.music
    bg_music.load("Assets/Music/SkyFire_(Title Screen).ogg")
    bg_music.play(-1)
    bg_music.set_volume(0.4)

    button = mixer.Sound("Assets/SFX/click.mp3")
    button.set_volume(0.3)

    #Fonts
    fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 2.5)))
    buttonPlayFont = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 5)))
    buttonOptionsFont = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 5)))

    last_time = tm.time()#Esta variabe sirve para calcular el deltaTime

    while True:
        dt = 60/FPS_Limit
        #Se dibuja el fondo
        screen.fill(BLACK)
        for particle in stars:
            particle[1][1] += particle[3] * dt
            if particle[1][1] > screen_size[1]:
                particle[3] = randint(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.78125)))
                particle[1][1] = -1
            draw.circle(screen, particle[0], particle[1], particle[2])
        
        #Muestra los fps
        if fps_show:
            fps = clock.get_fps()
            fps_text = fps_font.render("FPS: " + str(int(fps//1)), True, WHITE)
            screen.blit(fps_text, fps_text.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 97), responsiveSizeAndPosition(screen_size, 0, 1))))

        #Mouse position
        mx, my = mouse.get_pos()

        #Title
        mainMenuFont = font.Font("Assets/Fonts/Vermin_Vibes_1989.ttf", int(responsiveSizeAndPosition(screen_size, 1, 15)))
        mainMenuText = mainMenuFont.render("SPACE WAR", True, WHITE)
        mainMenuShadowText = mainMenuFont.render("SPACE WAR", True, (76, 117, 117))
        screen.blit(mainMenuShadowText, mainMenuShadowText.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 50.7), responsiveSizeAndPosition(screen_size, 1, 30.7))))
        screen.blit(mainMenuText, mainMenuText.get_rect(center= (responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 30))))

        #Boton Play
        buttonPlayText = buttonPlayFont.render("PLAY", True, WHITE)
        if buttonPlayText.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 50))).collidepoint((mx, my)):
            buttonPlayText = buttonPlayFont.render("PLAY", True, (154, 237, 237))
            if click:
                bg_music.pause()
                button.play()
                tm.sleep(0.3)
                Game(stars, FPS_Limit)
                bg_music.load("Assets/Music/SkyFire_(Title Screen).ogg")
                bg_music.play(-1)
                bg_music.set_volume(0.2)
                #Remove stars
                for star in stars:
                    stars.remove(star)
                #Create new stars with new size
                for _ in range(500):
                    randomWhite = randint(150, 230)
                    randSize = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.390625)))
                    randSpeed = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.78125)))
                    particleRect = Rect(uniform(0, screen_size[0]), uniform(0, screen_size[1]), randSize, randSize)
                    stars.append([[randomWhite, randomWhite, randomWhite], [particleRect.x, particleRect.y], randSize, randSpeed])

        #Boton Options
        buttonOptionsText = buttonOptionsFont.render("OPTIONS", True, WHITE)
        if buttonOptionsText.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 56))).collidepoint((mx, my)):
            buttonOptionsText = buttonOptionsFont.render("OPTIONS", True, (154, 237, 237))
            if click:
                button.play()
                Options(screen, stars, resolutions)
                #Recalculate the size of the screen
                screen_size = screen.get_size()

                #Resize all the fonts
                fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 2.5)))
                buttonPlayFont = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 5)))
                buttonOptionsFont = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 5)))

                #Remove stars
                for star in stars:
                    stars.remove(star)
                #Create new stars with new size
                for _ in range(500):
                    randomWhite = randint(150, 230)
                    randSize = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.390625)))
                    randSpeed = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.78125)))
                    particleRect = Rect(uniform(0, screen_size[0]), uniform(0, screen_size[1]), randSize, randSize)
                    stars.append([[randomWhite, randomWhite, randomWhite], [particleRect.x, particleRect.y], randSize, randSpeed])


        #Event manager
        click = False
        for e in event.get():
            if e.type == QUIT:
                with open(binaryArchive, "wb") as f:
                    pickle.dump((resolution_index, max_score, fullscreen), f)
                    pickle.dump(selected, f)
                    pickle.dump((fps_show, selectedOption, FPS_Limit), f)

                quit()
                sys.exit()
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    with open(binaryArchive, "wb") as f:
                        pickle.dump((resolution_index, max_score, fullscreen), f)
                        pickle.dump(selected, f)
                        pickle.dump((fps_show, selectedOption, FPS_Limit), f)
                    quit()
                    sys.exit()

        #Pintar el boton play en la pantalla
        screen.blit(buttonPlayText, buttonPlayText.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 50))))

        #Pintar el boton options en la pantalla
        screen.blit(buttonOptionsText, buttonOptionsText.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 56))))

        display.flip()
        clock.tick(FPS_Limit)

def Options(screen, stars, resolutions):
    screen_size = screen.get_size()
    global resolution_index

    #Se inicializa las varibales de manera global para que no haya conflictos y se "guarde" la resolucion
    global fullscreen
    global selected

    manager_ui = pygame_gui.UIManager(resolutions[resolution_index], "themeUI.json")

    #Se inicializa todas las variables necesarias para mostrar los fps
    global fps_show
    global FPS_Limit
    global selectedOption
    fps_limit_options = ["30", "60", "120", "144", "240"]

    
    #Fonts
    fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 2.5)))
    title_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 4.34375)))
    option_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 2.34375)))
    select_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 2)))

    #Fps limit Text
    fps_limit_options_text = select_font.render("FPS Limit: ", True, WHITE)
    fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(fps_limit_options, selectedOption,Rect(responsiveSizeAndPosition(screen_size, 0, 50) + fps_limit_options_text.get_size()[0], responsiveSizeAndPosition(screen_size, 1, 24.5), responsiveSizeAndPosition(screen_size, 0, 5), responsiveSizeAndPosition(screen_size, 0, 2.5)), manager_ui, object_id="#Fps_Limit_Option")

    last_time = tm.time()
    click = False
    running = True
    while running:
        ui_refresh_rate = clock.tick(FPS_Limit)/1000

        #Surface with SourceAlpha
        game_window = Surface(screen_size, SRCALPHA)

        #DeltaTime
        dt = tm.time() - last_time
        dt *= 60
        last_time = tm.time()

        mx, my = mouse.get_pos()

        #Se dibuja el fondo
        screen.fill(BLACK)
        for particle in stars:
            particle[1][1] += particle[3] * dt
            if particle[1][1] > screen_size[1]:
                particle[3] = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.78125)))
                particle[1][1] = 0
            draw.circle(screen, particle[0], particle[1], particle[2])

        #Muestra los fps
        if fps_show:
            fps = clock.get_fps()
            fps_text = fps_font.render("FPS: " + str(int(fps//1)), True, WHITE)
            screen.blit(fps_text, fps_text.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 97), responsiveSizeAndPosition(screen_size, 0, 1))))

        #Panel de fondo
        draw.rect(game_window, (7, 245, 245, 120), (responsiveSizeAndPosition(screen_size, 0, 5), responsiveSizeAndPosition(screen_size, 1, 5), responsiveSizeAndPosition(screen_size, 0, 90), responsiveSizeAndPosition(screen_size, 1, 90)), 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125)))
        #Titulo
        title_text = title_font.render("OPTIONS", True, WHITE)
        game_window.blit(title_text, (responsiveSizeAndPosition(screen_size, 0, 50) - title_text.get_size()[0]/2, responsiveSizeAndPosition(screen_size, 1, 6)))

        #Resoluciones
        resolutions_Text = option_font.render("Resolutions", True, WHITE)
        game_window.blit(resolutions_Text, (responsiveSizeAndPosition(screen_size, 0, 7), responsiveSizeAndPosition(screen_size, 1, 15)))
        #Boton1
        resolution1_text = select_font.render("426 X 240", True, (0, 64, 224))
        panel_rect1 = Rect(responsiveSizeAndPosition(screen_size, 0, 7), responsiveSizeAndPosition(screen_size, 1, 20), responsiveSizeAndPosition(screen_size, 0, 20), responsiveSizeAndPosition(screen_size, 0, 2.5))
        if selected[0]:
                    draw.rect(game_window, DARK_BLUE, panel_rect1, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
                    resolution1_text = select_font.render("426 X 240", True, WHITE)
                    game_window.blit(resolution1_text, resolution1_text.get_rect(center=(panel_rect1.centerx, panel_rect1.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
        else:
            draw.rect(game_window, (180, 245, 245), panel_rect1, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
            game_window.blit(resolution1_text, resolution1_text.get_rect(center=(panel_rect1.centerx, panel_rect1.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
        if panel_rect1.collidepoint(mx, my):
            #Cambia el color con hover
            draw.rect(game_window, (75, 117, 224), panel_rect1, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
            resolution1_text = select_font.render("426 X 240", True, WHITE)
            game_window.blit(resolution1_text, resolution1_text.get_rect(center=(panel_rect1.centerx, panel_rect1.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
            if click:
                resolution_index = 0
                selected = [True, False, False, False, False]
                if fullscreen:
                    screen = display.set_mode(resolutions[resolution_index], FULLSCREEN)
                else:
                    screen = display.set_mode(resolutions[resolution_index], DOUBLEBUF)

                screen_size = screen.get_size()
                
                #Resize all the fonts
                fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 2.5)))
                title_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 4.34375)))
                option_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 2.34375)))
                select_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 2)))
                
                #Resize the manager ui
                manager_ui = pygame_gui.UIManager(resolutions[resolution_index], "themeUI.json")
                fps_limit_options_text = select_font.render("FPS Limit: ", True, WHITE)
                fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(fps_limit_options, selectedOption,Rect(responsiveSizeAndPosition(screen_size, 0, 50) + fps_limit_options_text.get_size()[0], responsiveSizeAndPosition(screen_size, 1, 24.5), responsiveSizeAndPosition(screen_size, 0, 5), responsiveSizeAndPosition(screen_size, 0, 2.5)), manager_ui, object_id="#Fps_Limit_Option")
                
                #Remove stars
                for star in stars:
                    stars.remove(star)
                #Create new stars with new size
                for _ in range(500):
                    randomWhite = randint(150, 230)
                    randSize = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.390625)))
                    randSpeed = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.78125)))
                    particleRect = Rect(uniform(0, screen_size[0]), uniform(0, screen_size[1]), randSize, randSize)
                    stars.append([[randomWhite, randomWhite, randomWhite], [particleRect.x, particleRect.y], randSize, randSpeed])

        #Boton2
        resolution2_text = select_font.render("640 X 360", True, (0, 64, 224))
        panel_rect2 = Rect(responsiveSizeAndPosition(screen_size, 0, 7), responsiveSizeAndPosition(screen_size, 1, 25), responsiveSizeAndPosition(screen_size, 0, 20), responsiveSizeAndPosition(screen_size, 0, 2.5))
        if selected[1]:
                    draw.rect(game_window, DARK_BLUE, panel_rect2, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
                    resolution2_text = select_font.render("640 X 360", True, WHITE)
                    game_window.blit(resolution2_text, resolution2_text.get_rect(center=(panel_rect2.centerx, panel_rect2.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
        else:
            draw.rect(game_window, (180, 245, 245), panel_rect2, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
            game_window.blit(resolution2_text, resolution2_text.get_rect(center=(panel_rect2.centerx, panel_rect2.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
        if panel_rect2.collidepoint(mx, my):
            #Cambia el color con hover
            draw.rect(game_window, (75, 117, 224), panel_rect2, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
            resolution2_text = select_font.render("640 X 360", True, WHITE)
            game_window.blit(resolution2_text, resolution2_text.get_rect(center=(panel_rect2.centerx, panel_rect2.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
            if click:
                resolution_index = 1
                selected = [False, True, False, False, False]
                if fullscreen:
                    screen = display.set_mode(resolutions[resolution_index], FULLSCREEN)
                else:
                    screen = display.set_mode(resolutions[resolution_index], DOUBLEBUF)

                screen_size = screen.get_size()
                
                #Resize all the fonts
                fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 2.5)))
                title_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 4.34375)))
                option_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 2.34375)))
                select_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 2)))
                
                #Resize the manager ui
                manager_ui = pygame_gui.UIManager(resolutions[resolution_index], "themeUI.json")
                fps_limit_options_text = select_font.render("FPS Limit: ", True, WHITE)
                fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(fps_limit_options, selectedOption,Rect(responsiveSizeAndPosition(screen_size, 0, 50) + fps_limit_options_text.get_size()[0], responsiveSizeAndPosition(screen_size, 1, 24.5), responsiveSizeAndPosition(screen_size, 0, 5), responsiveSizeAndPosition(screen_size, 0, 2.5)), manager_ui, object_id="#Fps_Limit_Option")

                #Remove stars
                for star in stars:
                    stars.remove(star)
                #Create new stars with new size
                for _ in range(500):
                    randomWhite = randint(150, 230)
                    randSize = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.390625)))
                    randSpeed = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.78125)))
                    particleRect = Rect(uniform(0, screen_size[0]), uniform(0, screen_size[1]), randSize, randSize)
                    stars.append([[randomWhite, randomWhite, randomWhite], [particleRect.x, particleRect.y], randSize, randSpeed])
        #Boton3
        resolution3_text = select_font.render("854 X 480", True, (0, 64, 224))
        panel_rect3 = Rect(responsiveSizeAndPosition(screen_size, 0, 7), responsiveSizeAndPosition(screen_size, 1, 30), responsiveSizeAndPosition(screen_size, 0, 20), responsiveSizeAndPosition(screen_size, 0, 2.5))
        if selected[2]:
                    draw.rect(game_window, DARK_BLUE, panel_rect3, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
                    resolution3_text = select_font.render("854 X 480", True, WHITE)
                    game_window.blit(resolution3_text, resolution3_text.get_rect(center=(panel_rect3.centerx, panel_rect3.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
        else:
            draw.rect(game_window, (180, 245, 245), panel_rect3, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
            game_window.blit(resolution3_text, resolution3_text.get_rect(center=(panel_rect3.centerx, panel_rect3.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
        if panel_rect3.collidepoint(mx, my):
            #Cambia el color con hover
            draw.rect(game_window, (75, 117, 224), panel_rect3, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
            resolution3_text = select_font.render("854 X 480", True, WHITE)
            game_window.blit(resolution3_text, resolution3_text.get_rect(center=(panel_rect3.centerx, panel_rect3.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
            if click:
                resolution_index = 2
                selected = [False, False, True, False, False]
                if fullscreen:
                    screen = display.set_mode(resolutions[resolution_index], FULLSCREEN)
                else:
                    screen = display.set_mode(resolutions[resolution_index], DOUBLEBUF)

                screen_size = screen.get_size()
                
                #Resize all the fonts
                fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 2.5)))
                title_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 4.34375)))
                option_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 2.34375)))
                select_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 2)))
                
                #Resize the manager ui
                manager_ui = pygame_gui.UIManager(resolutions[resolution_index], "themeUI.json")
                fps_limit_options_text = select_font.render("FPS Limit: ", True, WHITE)
                fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(fps_limit_options, selectedOption,Rect(responsiveSizeAndPosition(screen_size, 0, 50) + fps_limit_options_text.get_size()[0], responsiveSizeAndPosition(screen_size, 1, 24.5), responsiveSizeAndPosition(screen_size, 0, 5), responsiveSizeAndPosition(screen_size, 0, 2.5)), manager_ui, object_id="#Fps_Limit_Option")

                #Remove stars
                for star in stars:
                    stars.remove(star)
                #Create new stars with new size
                for _ in range(500):
                    randomWhite = randint(150, 230)
                    randSize = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.390625)))
                    randSpeed = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.78125)))
                    particleRect = Rect(uniform(0, screen_size[0]), uniform(0, screen_size[1]), randSize, randSize)
                    stars.append([[randomWhite, randomWhite, randomWhite], [particleRect.x, particleRect.y], randSize, randSpeed])
        #Boton4
        resolution4_text = select_font.render("1280 X 720", True, (0, 64, 224))
        panel_rect4 = Rect(responsiveSizeAndPosition(screen_size, 0, 7), responsiveSizeAndPosition(screen_size, 1, 35), responsiveSizeAndPosition(screen_size, 0, 20), responsiveSizeAndPosition(screen_size, 0, 2.5))
        if selected[3]:
                    draw.rect(game_window, DARK_BLUE, panel_rect4, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
                    resolution4_text = select_font.render("1280 X 720", True, WHITE)
                    game_window.blit(resolution4_text, resolution4_text.get_rect(center=(panel_rect4.centerx, panel_rect4.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
        else:
            draw.rect(game_window, (180, 245, 245), panel_rect4, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
            game_window.blit(resolution4_text, resolution4_text.get_rect(center=(panel_rect4.centerx, panel_rect4.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
        if panel_rect4.collidepoint(mx, my):
            #Cambia el color con hover
            draw.rect(game_window, (75, 117, 224), panel_rect4, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
            resolution4_text = select_font.render("1280 X 720", True, WHITE)
            game_window.blit(resolution4_text, resolution4_text.get_rect(center=(panel_rect4.centerx, panel_rect4.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
            if click:
                resolution_index = 3
                selected = [False, False, False, True, False]
                if fullscreen:
                    screen = display.set_mode(resolutions[resolution_index], FULLSCREEN)
                else:
                    screen = display.set_mode(resolutions[resolution_index], DOUBLEBUF)

                screen_size = screen.get_size()
                
                #Resize all the fonts
                fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 2.5)))
                title_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 4.34375)))
                option_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 2.34375)))
                select_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 2)))
                
                #Resize the manager ui
                manager_ui = pygame_gui.UIManager(resolutions[resolution_index], "themeUI.json")
                fps_limit_options_text = select_font.render("FPS Limit: ", True, WHITE)
                fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(fps_limit_options, selectedOption,Rect(responsiveSizeAndPosition(screen_size, 0, 50) + fps_limit_options_text.get_size()[0], responsiveSizeAndPosition(screen_size, 1, 24.5), responsiveSizeAndPosition(screen_size, 0, 5), responsiveSizeAndPosition(screen_size, 0, 2.5)), manager_ui, object_id="#Fps_Limit_Option")

                #Remove stars
                for star in stars:
                    stars.remove(star)
                #Create new stars with new size
                for _ in range(500):
                    randomWhite = randint(150, 230)
                    randSize = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.390625)))
                    randSpeed = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.78125)))
                    particleRect = Rect(uniform(0, screen_size[0]), uniform(0, screen_size[1]), randSize, randSize)
                    stars.append([[randomWhite, randomWhite, randomWhite], [particleRect.x, particleRect.y], randSize, randSpeed])
        #Boton5
        resolution5_text = select_font.render(str(MONITOR_SIZE[0]) + " X " +  str(MONITOR_SIZE[1]), True, (0, 64, 224))
        panel_rect5 = Rect(responsiveSizeAndPosition(screen_size, 0, 7), responsiveSizeAndPosition(screen_size, 1, 40), responsiveSizeAndPosition(screen_size, 0, 20), responsiveSizeAndPosition(screen_size, 0, 2.5))
        if selected[4]:
            draw.rect(game_window, DARK_BLUE, panel_rect5, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
            resolution5_text = select_font.render(str(MONITOR_SIZE[0]) + " X " +  str(MONITOR_SIZE[1]), True, WHITE)
            game_window.blit(resolution5_text, resolution5_text.get_rect(center=(panel_rect5.centerx, panel_rect5.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
        else:
            draw.rect(game_window, (180, 245, 245), panel_rect5, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
            game_window.blit(resolution5_text, resolution5_text.get_rect(center=(panel_rect5.centerx, panel_rect5.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
        if panel_rect5.collidepoint(mx, my):
            #Cambia el color con hover
            draw.rect(game_window, (75, 117, 224), panel_rect5, 0, int(responsiveSizeAndPosition(screen_size, 0, 0.3125 * 8)))
            resolution5_text = select_font.render(str(MONITOR_SIZE[0]) + " X " +  str(MONITOR_SIZE[1]), True, WHITE)
            game_window.blit(resolution5_text, resolution5_text.get_rect(center=(panel_rect5.centerx, panel_rect5.centery + responsiveSizeAndPosition(screen_size, 1, 0.3))))
            if click:
                resolution_index = 4
                selected = [False, False, False, False, True]
                if fullscreen:
                    screen = display.set_mode(resolutions[resolution_index], FULLSCREEN)
                else:
                    screen = display.set_mode(resolutions[resolution_index], DOUBLEBUF)

                screen_size = screen.get_size()
                
                #Resize all the fonts
                fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 2.5)))
                title_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 4.34375)))
                option_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 2.34375)))
                select_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 2)))

                #Resize the manager ui
                manager_ui = pygame_gui.UIManager(resolutions[resolution_index], "themeUI.json")
                fps_limit_options_text = select_font.render("FPS Limit: ", True, WHITE)
                fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(fps_limit_options, selectedOption,Rect(responsiveSizeAndPosition(screen_size, 0, 50) + fps_limit_options_text.get_size()[0], responsiveSizeAndPosition(screen_size, 1, 24.5), responsiveSizeAndPosition(screen_size, 0, 5), responsiveSizeAndPosition(screen_size, 0, 2.5)), manager_ui, object_id="#Fps_Limit_Option")
                
                #Remove stars
                for star in stars:
                    stars.remove(star)
                #Create new stars with new size
                for _ in range(500):
                    randomWhite = randint(150, 230)
                    randSize = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.390625)))
                    randSpeed = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.78125)))
                    particleRect = Rect(uniform(0, screen_size[0]), uniform(0, screen_size[1]), randSize, randSize)
                    stars.append([[randomWhite, randomWhite, randomWhite], [particleRect.x, particleRect.y], randSize, randSpeed])
        #Toogle FullScreen
        resolution6_text = select_font.render("FullScreen", True, WHITE)
        game_window.blit(resolution6_text, resolution6_text.get_rect(center=(panel_rect5.x + resolution6_text.get_size()[0]/2, responsiveSizeAndPosition(screen_size, 1, 50))))
        cube_Rect = Rect(responsiveSizeAndPosition(screen_size, 0, 8) + resolution6_text.get_size()[0], responsiveSizeAndPosition(screen_size, 1, 48), resolution6_text.get_size()[1], resolution6_text.get_size()[1])
        draw.rect(game_window, WHITE, cube_Rect, int(responsiveSizeAndPosition(screen_size, 0, 0.3125)), int(responsiveSizeAndPosition(screen_size, 0, 0.3125)))
        if fullscreen:
                draw.circle(game_window, WHITE, cube_Rect.center, responsiveSizeAndPosition(screen_size, 0, 0.5))
        if cube_Rect.collidepoint(mx, my):
            #Cambia el color con hover
            draw.rect(game_window, (75, 117, 224), cube_Rect, int(responsiveSizeAndPosition(screen_size, 0, 0.3125)), int(responsiveSizeAndPosition(screen_size, 0, 0.3125)))
            if fullscreen:
                draw.circle(game_window, (75, 117, 224), cube_Rect.center, responsiveSizeAndPosition(screen_size, 0, 0.5))
            if click:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = display.set_mode(resolutions[resolution_index], FULLSCREEN)
                else:
                    if selected[0]:
                        resolution_index = 0
                    elif selected[1]:
                        resolution_index = 1
                    elif selected[2]:
                        resolution_index = 2
                    elif selected[3]:
                        resolution_index = 3
                    elif selected[4]:
                        resolution_index = 4
                    screen = display.set_mode(resolutions[resolution_index], DOUBLEBUF)

                screen_size = screen.get_size()

                #Resize all the fonts
                title_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 4.34375)))
                option_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 2.34375)))
                select_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 0, 2)))

                #Resize the manager ui
                manager_ui = pygame_gui.UIManager(resolutions[resolution_index], "themeUI.json")
                fps_limit_options_text = select_font.render("FPS Limit: ", True, WHITE)
                fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(fps_limit_options, selectedOption,Rect(responsiveSizeAndPosition(screen_size, 0, 50) + fps_limit_options_text.get_size()[0], responsiveSizeAndPosition(screen_size, 1, 24.5), responsiveSizeAndPosition(screen_size, 0, 5), responsiveSizeAndPosition(screen_size, 0, 2.5)), manager_ui, object_id="#Fps_Limit_Option")

                #Remove stars
                for star in stars:
                    stars.remove(star)
                #Create new stars with new size
                for _ in range(500):
                    randomWhite = randint(150, 230)
                    randSize = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.390625)))
                    randSpeed = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.78125)))
                    particleRect = Rect(uniform(0, screen_size[0]), uniform(0, screen_size[1]), randSize, randSize)
                    stars.append([[randomWhite, randomWhite, randomWhite], [particleRect.x, particleRect.y], randSize, randSpeed])

        #FPS Control
        fpsControl_Text = option_font.render("FPS Control", True, WHITE)
        game_window.blit(fpsControl_Text, (responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 15)))

        #Toogle Show FPS
        showFPS_text = select_font.render("Show FPS", True, WHITE)
        game_window.blit(showFPS_text, showFPS_text.get_rect(center=(responsiveSizeAndPosition(screen_size, 0, 50) + showFPS_text.get_size()[0]/2, responsiveSizeAndPosition(screen_size, 1, 22))))
        cube_Rect_showFPS = Rect(responsiveSizeAndPosition(screen_size, 0, 51) + showFPS_text.get_size()[0], responsiveSizeAndPosition(screen_size, 1, 20), resolution6_text.get_size()[1], resolution6_text.get_size()[1])
        draw.rect(game_window, WHITE, cube_Rect_showFPS, int(responsiveSizeAndPosition(screen_size, 0, 0.3125)), int(responsiveSizeAndPosition(screen_size, 0, 0.3125)))
        if fps_show:
            draw.circle(game_window, WHITE, cube_Rect_showFPS.center, responsiveSizeAndPosition(screen_size, 0, 0.5))
        if cube_Rect_showFPS.collidepoint(mx, my):
            #Cambia el color con hover
            draw.rect(game_window, (75, 117, 224), cube_Rect_showFPS, int(responsiveSizeAndPosition(screen_size, 0, 0.3125)), int(responsiveSizeAndPosition(screen_size, 0, 0.3125)))
            if fps_show:
                draw.circle(game_window, (75, 117, 224), cube_Rect_showFPS.center, responsiveSizeAndPosition(screen_size, 0, 0.5))
            if click:
                fps_show = not fps_show

        #Draw fps limit on screen
        game_window.blit(fps_limit_options_text, (responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 25.5)))
        

        #event manager
        click = False
        for e in event.get():
            if e.type == QUIT:
                with open(binaryArchive, "wb") as f:
                    pickle.dump((resolution_index, max_score, fullscreen), f)
                    pickle.dump(selected, f)
                    pickle.dump((fps_show, selectedOption, FPS_Limit), f)

                quit()
                sys.exit()

            manager_ui.process_events(e)
            if e.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                selectedOption = e.text
                for option in fps_limit_options:
                    if selectedOption == option:
                        FPS_Limit = int(e.text)

            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    click = True
            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    running = False

        manager_ui.update(ui_refresh_rate)
        manager_ui.draw_ui(game_window)
        screen.blit(game_window, (0,0))
        display.flip()
        clock.tick(FPS_Limit)

        

def Game(stars, fps_limit):
    global selected
    screen_size = screen.get_size()
    game_surface = Surface(screen_size)

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
    global fps_show
    
    #----------------------------
    #Sprite sheets
    playerSheet = image.load("Assets/Images/SpaceShip_sheet.png").convert_alpha()
    bulletsSheet = image.load("Assets/Images/Bullets_sheet.png").convert_alpha()
    #----------------------------

    #Fonts
    fps_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 2.5)))
    coins_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 3)))
    player_lifes_font = font.Font("Assets/Fonts/Minecraft.ttf", int(responsiveSizeAndPosition(screen_size, 1, 4)))

    #Se guardan todas las balas en un array
    bullet_array = [get_image(bulletsSheet, 0, 24, 24, BLACK),
                    get_image(bulletsSheet, 1, 24, 24, BLACK),
                    get_image(bulletsSheet, 2, 24, 24, BLACK),
                    get_image(bulletsSheet, 3, 24, 24, BLACK),
                    get_image(bulletsSheet, 4, 24, 24, BLACK),
                    get_image(bulletsSheet, 5, 24, 24, BLACK),
                    get_image(bulletsSheet, 6, 24, 24, BLACK)]

    #Posibles posiciones de un enemigo
    enemyPos = [SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 25), responsiveSizeAndPosition(screen_size, 1, 10))), 
                SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 75), responsiveSizeAndPosition(screen_size, 1, 10))),
                SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 25), responsiveSizeAndPosition(screen_size, 1, 90))),
                SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 75), responsiveSizeAndPosition(screen_size, 1, 90))),
                SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 20))),
                SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 80))),
                SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 10), responsiveSizeAndPosition(screen_size, 1, 50))),
                SpawnPoint((responsiveSizeAndPosition(screen_size, 0, 90), responsiveSizeAndPosition(screen_size, 1, 50)))]

    enemyID = ["enemigo_patron_circular", 
            "enemigo_patron_espiral",
            "enemigo_patron_espiral_alternado", 
            "enemigo_patron_circular_alternado",
            "enemigo_patron_estrella",
            "enemigo_patron_spray"]

    #Objetos
    player = Player(get_image(playerSheet, 0, 52, 52, BLACK), bullet_array[0], (responsiveSizeAndPosition(screen_size, 0, 50), responsiveSizeAndPosition(screen_size, 1, 90)), (responsiveSizeAndPosition(screen_size, 0, 3), responsiveSizeAndPosition(screen_size, 0, 3)), 3, screen_size)
    player_life_image = transform.scale(image.load("Assets/Images/heart.png"), (responsiveSizeAndPosition(screen_size, 0, 3), responsiveSizeAndPosition(screen_size, 0, 3)))

    playerCollide = Rect(player.rect.x, player.rect.y, responsiveSizeAndPosition(screen_size, 0, 0.5), responsiveSizeAndPosition(screen_size, 0, 0.5))
    playerGroup.add(player)
    enemyGenerator = EnemyGenerator(enemies, enemyPos, 0, enemyID, bullet_array, "easy", screen, screen_size)
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

        screen.blit(game_surface, render_offset)

        #Dibuja el fondo
        game_surface.fill(BLACK)
        for particle in stars:
            particle[1][1] += particle[3] * dt
            if particle[1][1] > screen_size[1]:
                particle[3] = uniform(int(responsiveSizeAndPosition(screen_size, 0, 0.078125)), int(responsiveSizeAndPosition(screen_size, 0, 0.78125)))
                particle[1][1] = 0
            draw.circle(game_surface, particle[0], particle[1], particle[2])


        #Muestra los fps
        if fps_show:
            fps = clock.get_fps()
            fps_text = fps_font.render("FPS: " + str(int(fps//1)), True, WHITE)
            screen.blit(fps_text, fps_text.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 97), responsiveSizeAndPosition(screen_size, 0, 1))))

        #Muestra el puntaje
        coins_text = coins_font.render("Score: " + str(coins), True, WHITE)
        screen.blit(coins_text, (responsiveSizeAndPosition(screen_size, 0 , 2), responsiveSizeAndPosition(screen_size, 1, 2)))

        #Muestra la vida
        player_lifes_text = player_lifes_font.render("X " + str(player.vida -1), True, (255, 105, 84))
        screen.blit(player_life_image, (responsiveSizeAndPosition(screen_size, 0, 2), responsiveSizeAndPosition(screen_size, 1, 6)))
        screen.blit(player_lifes_text, player_lifes_text.get_rect(center = (responsiveSizeAndPosition(screen_size, 0, 2) + (player_life_image.get_size()[0] + 3 + (player_lifes_text.get_size()[0]/2)), responsiveSizeAndPosition(screen_size, 1, 6) + player_life_image.get_size()[1]/2)))

        #Event manager
        for e in event.get():
            if e.type == QUIT:
                with open(binaryArchive, "wb") as f:
                    pickle.dump((resolution_index, max_score, fullscreen), f)
                    pickle.dump(selected, f)
                    pickle.dump((fps_show, selectedOption, FPS_Limit), f)

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
        playerGroup.update(dt, mouse_pos, screen_size)
        for enemy in enemies:
            if enemy.vida == 0:
                coins += 1
        enemies.update(bullets, dt, screen_size)
        enemyGenerator.update(screen_size)
        bullets.update(screen_rect, dt)
        #-----------------

        #Configuración de la pantalla (In-Game)
        playerGroup.draw(game_surface) #Se dibuja el player en pantalla
        bullets.draw(game_surface)
        enemies.draw(game_surface)

        display.flip()

        clock.tick(fps_limit)#Control de los fps o cuadros por segundo
        #-----------------
#----------------------------

mainMenu()

with open(binaryArchive, "wb") as f:
                    pickle.dump((resolution_index, max_score, fullscreen), f)
                    pickle.dump(selected, f)
                    pickle.dump((fps_show, selectedOption, FPS_Limit), f)

quit()
sys.exit()