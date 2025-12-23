import os
import pickle
import sys
from pygame import display

class Settings:
    def __init__(self, root_path):
        self.root_path = root_path
        self.assets_path = os.path.join(self.root_path, "Assets/")
        
        # Save file
        self.save_dir = "data"
        self.save_file = os.path.join(self.save_dir, "save.data")
        
        # Defaults
        self.resolucion_index = 3
        self.max_score = 0
        self.pantalla_completa = False
        self.resolucion_elegida = [False, False, False, True, False]
        self.mostrar_fps = False
        self.limite_fps_texto = "60"
        self.limite_fps = 60
        
        # Monitor info
        if not display.get_init():
            display.init()
        self.monitor_size = (display.Info().current_w, display.Info().current_h)
        self.resoluciones = [(426, 240), (640, 360), (854, 480), (1280, 720), self.monitor_size]
        
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "rb") as f:
                    data = pickle.load(f)
                    # Unpack carefully to avoid versioning errors if possible, 
                    # but for now we follow the exact structure
                    (self.resolucion_index, self.max_score, self.pantalla_completa, 
                     self.resolucion_elegida, self.mostrar_fps, self.limite_fps_texto, 
                     self.limite_fps) = data
            except Exception as e:
                print(f"Error loading save: {e}")
                self.save_data() # Reset/Create if error
        else:
            self.save_data()

    def save_data(self):
        data = [
            self.resolucion_index,
            self.max_score,
            self.pantalla_completa,
            self.resolucion_elegida,
            self.mostrar_fps,
            self.limite_fps_texto,
            self.limite_fps
        ]
        with open(self.save_file, "wb") as f:
            pickle.dump(data, f)
            
    @property
    def current_resolution(self):
        return self.resoluciones[self.resolucion_index]
        
    def get_font_path(self, font_name):
        return os.path.join(self.assets_path, "Fonts", font_name)

    def get_asset_path(self, relative_path):
        return os.path.join(self.assets_path, relative_path)
