import pygame
import sys
from pygame import mixer
from .settings import Settings

class GameManager:
    def __init__(self, root_path):
        self.settings = Settings(root_path)
        
        # Initialize Pygame
        pygame.init()
        mixer.init()
        pygame.font.init()
        
        # Setup Display
        if self.settings.pantalla_completa:
            self.screen = pygame.display.set_mode(
                self.settings.current_resolution, 
                pygame.FULLSCREEN, 
                32
            )
        else:
            self.screen = pygame.display.set_mode(
                self.settings.current_resolution, 
                pygame.DOUBLEBUF, 
                32
            )
            
        pygame.display.set_caption("Zero Reflex")
        try:
            icon = pygame.image.load(self.settings.get_asset_path("Icon/icon.png"))
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"Warning: Could not load icon: {e}")

        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene = None
        
        # Global state shared across scenes
        self.resoluciones = self.settings.resoluciones  

    def set_scene(self, scene_class, **kwargs):
        self.current_scene = scene_class(self, **kwargs)

    def run(self):
        while self.running:
            dt = 60 / self.settings.limite_fps # Approximate dt scaling or use tick return
            # Better dt calculation
            dt_seconds = self.clock.tick(self.settings.limite_fps) / 1000.0
            dt_scaled = dt_seconds * 60 # Scale to 60 FPS reference as per original logic

            # Clear screen at start of frame
            self.screen.fill((0, 0, 0))

            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit_game()
            
            if self.current_scene:
                # Debug print once
                if not hasattr(self, 'debugged'):
                    print(f"Drawing scene: {type(self.current_scene).__name__}")
                    print(f"Screen size: {self.screen.get_size()}")
                    self.debugged = True
                    
                self.current_scene.handle_events(events)
                self.current_scene.update(dt_scaled)
                self.current_scene.draw(self.screen)
                
                # Check for scene switch
                if self.current_scene.next_scene:
                    new_class, kwargs = self.current_scene.next_scene
                    self.set_scene(new_class, **kwargs)

            pygame.display.flip()

    def change_resolution(self, resolution, fullscreen):
        self.settings.resolucion_index = self.settings.resoluciones.index(resolution) if resolution in self.settings.resoluciones else 0
        self.settings.pantalla_completa = fullscreen
        
        flags = pygame.FULLSCREEN if fullscreen else pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode(resolution, flags, 32)
        
        # We might need to notify the current scene about the resize or just let it handle it via get_size()
        # But if the scene cached size in __init__, it needs a refresh.
        # OptionsScene specifically re-inits UI on resize.
        if self.current_scene:
            # Re-initialize scene to fit new resolution? 
            # Or call a resize method?
            # Easiest is to reload the scene or have a resize callback.
            if hasattr(self.current_scene, 'on_resize'):
                self.current_scene.on_resize(resolution)

    def quit_game(self):
        self.settings.save_data()
        self.running = False
        pygame.quit()
        sys.exit()
