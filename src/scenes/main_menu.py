import pygame
from pygame import mixer
from .base_scene import BaseScene
from components.ui import Estrellas, Boton
from components.utils import tamanoDinamico

class MainMenuScene(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        
        self.anchopantalla, self.altopantalla = self.screen.get_size()
        
        # Initialize Stars
        self.estrellas = Estrellas(self.screen, 500, self.anchopantalla, self.altopantalla)
        
        # Music
        try:
            self.bg_music = mixer.music
            self.bg_music.load(self.settings.get_asset_path("Music/SkyFire_(Title Screen).ogg"))
            self.bg_music.play(-1)
            self.bg_music.set_volume(0.4)
        except Exception as e:
            print(f"Error loading music: {e}")
            
        # Sounds
        self.botonClick = mixer.Sound(self.settings.get_asset_path("SFX/click.mp3"))
        self.botonHover = mixer.Sound(self.settings.get_asset_path("SFX/hoverButton.mp3"))
        self.botonClick.set_volume(0.6)
        self.botonHover.set_volume(0.6)
        
        # Fonts
        self.init_fonts()
        
        # Colors - Neon/Cyber Theme
        self.WHITE = (255, 255, 255, 255)
        self.CYAN = (0, 243, 255)
        self.DARK_BG = (10, 10, 30, 200)
        self.TEXT_HOVER = (0, 0, 0) # Black text on bright button
        
        # Buttons
        self.init_ui()

    def init_fonts(self):
        self.fps_font = pygame.font.Font(self.settings.get_font_path("Minecraft.ttf"), int(tamanoDinamico(self.altopantalla, 2.5)))
        self.mainMenuFont = pygame.font.Font(self.settings.get_font_path("Vermin_Vibes_1989.ttf"), int(tamanoDinamico(self.altopantalla, 15)))
        self.fuente_botones = pygame.font.Font(self.settings.get_font_path("Minecraft.ttf"), int(tamanoDinamico(self.altopantalla, 5)))

    def init_ui(self):
        # Title
        self.mainMenuText = self.mainMenuFont.render("ZERO REFLEX", True, self.WHITE)
        self.mainMenuShadowText = self.mainMenuFont.render("ZERO REFLEX", True, (76, 117, 117))
        
        # Buttons
        self.botonJugar = Boton(
            self.screen, 
            (tamanoDinamico(self.anchopantalla, 12), tamanoDinamico(self.altopantalla, 7)), 
            (tamanoDinamico(self.anchopantalla, 50), tamanoDinamico(self.altopantalla, 50)),
            self.fuente_botones, "PLAY", self.WHITE , self.TEXT_HOVER, 
            self.botonClick, self.botonHover, True, self.DARK_BG, self.CYAN, int(tamanoDinamico(self.anchopantalla, 0.3125))
        )
        self.botonOpciones = Boton(
            self.screen, 
            (tamanoDinamico(self.anchopantalla, 18), tamanoDinamico(self.altopantalla, 7)), 
            (tamanoDinamico(self.anchopantalla, 50), tamanoDinamico(self.altopantalla, 58)),
            self.fuente_botones, "OPTIONS", self.WHITE , self.TEXT_HOVER, 
            self.botonClick, self.botonHover, True, self.DARK_BG, self.CYAN, int(tamanoDinamico(self.anchopantalla, 0.3125))
        )

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if self.botonJugar.hover:
                         # Start Game
                        from .game_scene import GameScene
                        self.botonJugar.onClick(lambda: None, True, self.bg_music, 0.5) 
                        # Note: original code passed 'Game' function, here we switch scene
                        self.switch_to_scene(GameScene, estrellas=self.estrellas)
                        
                    if self.botonOpciones.hover:
                        # Go to Options
                        from .options import OptionsScene
                        self.botonOpciones.onClick(lambda: None, False, self.bg_music, 0)
                        self.switch_to_scene(OptionsScene, estrellas=self.estrellas)

    def update(self, dt):
        self.estrellas.update(dt)
        self.botonJugar.update()
        self.botonOpciones.update()

    def draw(self, surface):
        # surface.fill((0, 0, 0)) # Removed: Cleared in GameManager. logic draws in update.
        
        # FPSDraw Stars - already drawn in update? No, update just updates pos.
        # Original code: estrellas.update(dt) draws directly to screen because it has 'pantalla' ref.
        # Yes, Estrellas.__init__ takes 'superficie' and update calls draw.circle on it.
        # So we don't need to manually draw stars if update does it.
        # Wait, re-reading Estrellas.update:
        # draw.circle(self.superficie, ...)
        # So yes, it draws.
        
        # FPS
        if self.settings.mostrar_fps:
            fps = self.game_manager.clock.get_fps()
            fps_text = self.fps_font.render("FPS: " + str(int(fps//1)), True, self.WHITE)
            surface.blit(fps_text, fps_text.get_rect(center = (tamanoDinamico(self.anchopantalla, 97), tamanoDinamico(self.anchopantalla, 1))))

        # Title
        surface.blit(self.mainMenuShadowText, self.mainMenuShadowText.get_rect(center = (tamanoDinamico(self.anchopantalla, 50.7), tamanoDinamico(self.altopantalla, 30.7))))
        surface.blit(self.mainMenuText, self.mainMenuText.get_rect(center= (tamanoDinamico(self.anchopantalla, 50), tamanoDinamico(self.altopantalla, 30))))
