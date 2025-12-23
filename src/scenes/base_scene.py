from abc import ABC, abstractmethod
import pygame

class BaseScene(ABC):
    def __init__(self, game_manager):
        self.game_manager = game_manager
        self.settings = game_manager.settings
        self.screen = game_manager.screen
        self.next_scene = None

    @abstractmethod
    def handle_events(self, events):
        """Process input events."""
        pass

    @abstractmethod
    def update(self, dt):
        """Update game logic."""
        pass

    @abstractmethod
    def draw(self, surface):
        """Render to the screen."""
        pass

    def switch_to_scene(self, scene_class, **kwargs):
        """Request a scene switch."""
        self.next_scene = (scene_class, kwargs)
