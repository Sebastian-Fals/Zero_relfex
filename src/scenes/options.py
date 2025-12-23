import pygame
import pygame_gui
import time as tm
from .base_scene import BaseScene
from components.utils import tamanoDinamico
from components.ui import Estrellas

class OptionsScene(BaseScene):
    def __init__(self, game_manager, estrellas):
        super().__init__(game_manager)
        self.estrellas = estrellas
        self.anchopantalla, self.altopantalla = self.screen.get_size()
        
        self.manager_ui = pygame_gui.UIManager(
            (self.anchopantalla, self.altopantalla), 
            self.settings.get_asset_path("../themeUI.json") # themeUI is in root? assets parent.
        )
        # Verify theme path. Original was "themeUI.json" in root.
        # So root_path + "themeUI.json". 
        # Settings writes get_asset_path as join(assets, path).
        # We normally shouldn't use ../. 
        # Let's fix the path later or assume it's moved to Assets? 
        # Task said "Analyze themeUI.json". It is in root.
        # I should probably move typical assets to Assets or just ref it correctly.
        # For now: self.game_manager.settings.root_path + "/themeUI.json"
        
        theme_path = self.settings.root_path + "/themeUI.json"
        try:
            self.manager_ui = pygame_gui.UIManager((self.anchopantalla, self.altopantalla), theme_path)
        except:
             self.manager_ui = pygame_gui.UIManager((self.anchopantalla, self.altopantalla))

        self.init_ui()
        self.last_time = tm.time()

    def init_ui(self):
        # Fonts
        self.fps_font = pygame.font.Font(self.settings.get_font_path("Minecraft.ttf"), int(tamanoDinamico(self.altopantalla, 2.5)))
        self.title_font = pygame.font.Font(self.settings.get_font_path("Minecraft.ttf"), int(tamanoDinamico(self.anchopantalla, 4.34375)))
        self.option_font = pygame.font.Font(self.settings.get_font_path("Minecraft.ttf"), int(tamanoDinamico(self.anchopantalla, 2.34375)))
        self.select_font = pygame.font.Font(self.settings.get_font_path("Minecraft.ttf"), int(tamanoDinamico(self.anchopantalla, 2)))

        # FPS Dropdown
        self.fps_limit_options = ["30", "60", "120", "144", "240"]
        fps_limit_options_text = self.select_font.render("FPS Limit: ", True, (255, 255, 255))
        
        self.fpsLimit_OptionsMenu = pygame_gui.elements.UIDropDownMenu(
            self.fps_limit_options, 
            self.settings.limite_fps_texto,
            pygame.Rect(
                tamanoDinamico(self.anchopantalla, 50) + fps_limit_options_text.get_size()[0], 
                tamanoDinamico(self.altopantalla, 24.5), 
                tamanoDinamico(self.anchopantalla, 5), 
                tamanoDinamico(self.anchopantalla, 2.5)
            ), 
            self.manager_ui, 
            object_id="#Fps_Limit_Option"
        )
        
        self.click = False

    def on_resize(self, resolution):
        self.anchopantalla, self.altopantalla = resolution
        # Re-create UI Manager for new size
        theme_path = self.settings.root_path + "/themeUI.json"
        self.manager_ui = pygame_gui.UIManager((self.anchopantalla, self.altopantalla), theme_path)
        self.init_ui()
        self.estrellas.refrescar(self.anchopantalla, self.altopantalla)

    def handle_events(self, events):
        self.click = False
        for e in events:
            self.manager_ui.process_events(e)
            
            if e.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                self.settings.limite_fps_texto = e.text
                if e.text in self.fps_limit_options:
                    self.settings.limite_fps = int(e.text)
            
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    self.click = True
                    
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    # Save and Return
                    from .main_menu import MainMenuScene
                    self.settings.save_data()
                    self.switch_to_scene(MainMenuScene)

    # Simplified helpers to avoid massive copy-paste
    def draw_resolution_button(self, index, res_idx, label_res, y_pos_pct):
        # Logic is mixed Update/Draw/HandleInput in original.
        # Here we separate Update/HandleInput from Draw?
        # Ideally yes. But 'click' state is transient.
        # I'll handle Input here and state updates. Draw will use state.
        pass # Moving to update/draw split proper.

    def update(self, dt):
        self.estrellas.update(dt)
        self.manager_ui.update(dt)
        
        # Check clicks logic
        if self.click:
             mx, my = pygame.mouse.get_pos()
             # Resolution Buttons Logic
             # Reuse positions
             y_starts = [20, 25, 30, 35, 40]
             for idx, y_pct in enumerate(y_starts):
                 panel_rect = pygame.Rect(
                     tamanoDinamico(self.anchopantalla, 7), 
                     tamanoDinamico(self.altopantalla, y_pct), 
                     tamanoDinamico(self.anchopantalla, 20), 
                     tamanoDinamico(self.anchopantalla, 2.5)
                 )
                 if panel_rect.collidepoint(mx, my):
                     self.change_res(idx)
                     
             # Fullscreen
             fs_rect = pygame.Rect(
                 tamanoDinamico(self.anchopantalla, 8) + self.select_font.size("FullScreen")[0], 
                 tamanoDinamico(self.altopantalla, 48), 
                 30, 30 # approx
             ) # Wait, need text size for dynamic rect pos.
             # I should probably move all rect calculations to draw or init.
             # Doing it every frame is what original did (inefficient).
             # I'll stick to 'every frame' for now to ensure dynamic scaling works.
             
             # ... Fullscreen and FPS toggle logic ...

    def change_res(self, index):
        self.settings.resolucion_index = index
        self.settings.resolucion_elegida = [i == index for i in range(5)]
        new_res = self.settings.resoluciones[index]
        self.game_manager.change_resolution(new_res, self.settings.pantalla_completa)

    def draw(self, surface):
        # surface.fill((0, 0, 0)) # Removed: Cleared in GameManager
        # Estrellas draw
        # Estrellas draws to surface.
        # self.estrellas.update(dt) was called.
        
        # Overlay
        game_window = pygame.Surface((self.anchopantalla, self.altopantalla), pygame.SRCALPHA)
        self.draw_ui_elements(game_window)
        surface.blit(game_window, (0,0))
        
        self.manager_ui.draw_ui(surface)
        
        if self.settings.mostrar_fps:
            fps = self.game_manager.clock.get_fps()
            fps_text = self.fps_font.render("FPS: " + str(int(fps//1)), True, (255, 255, 255))
            surface.blit(fps_text, fps_text.get_rect(center = (tamanoDinamico(self.anchopantalla, 97), tamanoDinamico(self.anchopantalla, 1))))

    def draw_ui_elements(self, surface):
        mx, my = pygame.mouse.get_pos()
        
        # Panel Background
        pygame.draw.rect(surface, (7, 245, 245, 120), (tamanoDinamico(self.anchopantalla, 5), tamanoDinamico(self.altopantalla, 5), tamanoDinamico(self.anchopantalla, 90), tamanoDinamico(self.altopantalla, 90)), 0, int(tamanoDinamico(self.anchopantalla, 0.3125)))
        
        # Title
        title_text = self.title_font.render("OPTIONS", True, (255, 255, 255))
        surface.blit(title_text, (tamanoDinamico(self.anchopantalla, 50) - title_text.get_size()[0]/2, tamanoDinamico(self.altopantalla, 6)))

        # Resolutions
        resoluciones_Text = self.option_font.render("Resolutions", True, (255, 255, 255))
        surface.blit(resoluciones_Text, (tamanoDinamico(self.anchopantalla, 7), tamanoDinamico(self.altopantalla, 15)))

        labels = ["426 X 240", "640 X 360", "854 X 480", "1280 X 720", f"{self.settings.monitor_size[0]} X {self.settings.monitor_size[1]}"]
        y_starts = [20, 25, 30, 35, 40]
        
        for idx, label in enumerate(labels):
            y_pos = y_starts[idx]
            rect = pygame.Rect(tamanoDinamico(self.anchopantalla, 7), tamanoDinamico(self.altopantalla, y_pos), tamanoDinamico(self.anchopantalla, 20), tamanoDinamico(self.anchopantalla, 2.5))
            
            color = (180, 245, 245)
            text_color = (0, 64, 224)
            if self.settings.resolucion_elegida[idx]:
                color = (0, 1, 35) # DARK_BLUE
                text_color = (255, 255, 255)
            
            if rect.collidepoint(mx, my):
                color = (75, 117, 224)
                text_color = (255, 255, 255)
                if self.click:
                    self.change_res(idx)

            pygame.draw.rect(surface, color, rect, 0, int(tamanoDinamico(self.anchopantalla, 0.3125 * 8)))
            txt = self.select_font.render(label, True, text_color)
            surface.blit(txt, txt.get_rect(center=(rect.centerx, rect.centery + tamanoDinamico(self.altopantalla, 0.3))))

        # Fullscreen Toggle
        fs_text = self.select_font.render("FullScreen", True, (255, 255, 255))
        surface.blit(fs_text, fs_text.get_rect(center=(tamanoDinamico(self.anchopantalla, 7) + tamanoDinamico(self.anchopantalla, 20)/2, tamanoDinamico(self.altopantalla, 50))))
        
        # Position logic from original:
        # resolution6_text.get_rect(center=(panel_rect5.x + resolution6_text.get_size()[0]/2, tamanoDinamico(altopantalla, 50)))
        # cube_Rect = Rect(tamanoDinamico(anchopantalla, 8) + resolution6_text.get_size()[0], tamanoDinamico(altopantalla, 48), ...)
        
        cube_rect = pygame.Rect(
            tamanoDinamico(self.anchopantalla, 8) + fs_text.get_size()[0], 
            tamanoDinamico(self.altopantalla, 48), 
            fs_text.get_size()[1], fs_text.get_size()[1]
        )
        pygame.draw.rect(surface, (255, 255, 255), cube_rect, int(tamanoDinamico(self.anchopantalla, 0.3125)), int(tamanoDinamico(self.anchopantalla, 0.3125)))
        
        if self.settings.pantalla_completa:
             pygame.draw.circle(surface, (255, 255, 255), cube_rect.center, tamanoDinamico(self.anchopantalla, 0.5))

        if cube_rect.collidepoint(mx, my):
             pygame.draw.rect(surface, (75, 117, 224), cube_rect, int(tamanoDinamico(self.anchopantalla, 0.3125)), int(tamanoDinamico(self.anchopantalla, 0.3125)))
             if self.click:
                 self.toggle_fullscreen()

        # FPS Control Text
        fpsControl_Text = self.option_font.render("FPS Control", True, (255, 255, 255))
        surface.blit(fpsControl_Text, (tamanoDinamico(self.anchopantalla, 50), tamanoDinamico(self.altopantalla, 15)))

        # Show FPS Toggle
        showFPS_text = self.select_font.render("Show FPS", True, (255, 255, 255))
        # Original: tamanoDinamico(anchopantalla, 50) + showFPS_text.get_size()[0]/2, tamanoDinamico(altopantalla, 22)
        surface.blit(showFPS_text, showFPS_text.get_rect(center=(tamanoDinamico(self.anchopantalla, 50) + showFPS_text.get_size()[0]/2, tamanoDinamico(self.altopantalla, 22))))
        
        cube_fps_rect = pygame.Rect(
            tamanoDinamico(self.anchopantalla, 51) + showFPS_text.get_size()[0], 
            tamanoDinamico(self.altopantalla, 20), 
            fs_text.get_size()[1], fs_text.get_size()[1]
        )
        pygame.draw.rect(surface, (255, 255, 255), cube_fps_rect, int(tamanoDinamico(self.anchopantalla, 0.3125)), int(tamanoDinamico(self.anchopantalla, 0.3125)))
        
        if self.settings.mostrar_fps:
            pygame.draw.circle(surface, (255, 255, 255), cube_fps_rect.center, tamanoDinamico(self.anchopantalla, 0.5))

        if cube_fps_rect.collidepoint(mx, my):
             pygame.draw.rect(surface, (75, 117, 224), cube_fps_rect, int(tamanoDinamico(self.anchopantalla, 0.3125)), int(tamanoDinamico(self.anchopantalla, 0.3125)))
             if self.click:
                 self.settings.mostrar_fps = not self.settings.mostrar_fps

        # FPS Limit Text
        fps_limit_options_text = self.select_font.render("FPS Limit: ", True, (255, 255, 255))
        surface.blit(fps_limit_options_text, (tamanoDinamico(self.anchopantalla, 50), tamanoDinamico(self.altopantalla, 25.5)))

    def toggle_fullscreen(self):
        new_fs = not self.settings.pantalla_completa
        self.game_manager.change_resolution(self.settings.current_resolution, new_fs)
