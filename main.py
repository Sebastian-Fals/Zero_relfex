import sys
import os

# Add components to path if needed (though local imports should work if package structure is correct)
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.game_manager import GameManager
from src.scenes.main_menu import MainMenuScene

def main():
    # Root path is current dir
    root_path = os.path.dirname(os.path.abspath(__file__))
    
    game = GameManager(root_path)
    
    # Start with Main Menu
    game.set_scene(MainMenuScene)
    
    game.run()

if __name__ == "__main__":
    main()
