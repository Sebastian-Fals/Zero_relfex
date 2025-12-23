import pygame
from pygame import mixer
from random import randint
from .base_scene import BaseScene
from components.entities import Player
from components.enemy_generator import EnemyGenerator, SpawnPoint
from components.ui import Panel
from components.utils import get_image, tamanoDinamico

class GameScene(BaseScene):
    def __init__(self, game_manager, estrellas):
        super().__init__(game_manager)
        self.estrellas = estrellas
        self.anchopantalla, self.altopantalla = self.screen.get_size()
        self.last_dt = 0.016
        
        # Music
        self.bg_game_music = mixer.music
        self.bg_game_music.load(self.settings.get_asset_path("Music/Rain_of_Lasers.ogg"))
        self.bg_game_music.play(-1)
        self.bg_game_music.set_volume(0.2)
        
        # Sounds
        self.punch2 = mixer.Sound(self.settings.get_asset_path("SFX/punch2.wav"))
        self.punch2.set_volume(0.5)
        
        # Groups
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.playerGroup = pygame.sprite.Group()
        
        # Assets
        self.playerSheet = pygame.image.load(self.settings.get_asset_path("Images/SpaceShip_sheet.png")).convert_alpha()
        self.bulletsSheet = pygame.image.load(self.settings.get_asset_path("Images/Bullets_sheet.png")).convert_alpha()
        
        self.load_assets()
        self.setup_game_objects()
        
        self.coins = 0
        self.screen_shake = 0
        self.game_surface = pygame.Surface((self.anchopantalla, self.altopantalla), pygame.SRCALPHA)



    def load_assets(self):
        # Fonts
        self.fps_font = pygame.font.Font(self.settings.get_font_path("Minecraft.ttf"), int(tamanoDinamico(self.altopantalla, 2.5)))
        self.coins_font = pygame.font.Font(self.settings.get_font_path("Minecraft.ttf"), int(tamanoDinamico(self.altopantalla, 3)))
        # Removed text font for lives as we use hearts now
        
        # Colors
        self.CYAN = (0, 243, 255)
        self.DARK_BG = (10, 10, 30, 200)
        self.WHITE = (255, 255, 255)

        # Bullets
        BLACK = (0, 0, 0, 0)
        self.bullet_array = [
            get_image(self.bulletsSheet, 0, 24, 24, BLACK),
            get_image(self.bulletsSheet, 1, 24, 24, BLACK),
            get_image(self.bulletsSheet, 2, 24, 24, BLACK),
            get_image(self.bulletsSheet, 3, 24, 24, BLACK),
            get_image(self.bulletsSheet, 4, 24, 24, BLACK),
            get_image(self.bulletsSheet, 5, 24, 24, BLACK),
            get_image(self.bulletsSheet, 6, 24, 24, BLACK)
        ]
        
    def setup_ui_panels(self):
        # Score Panel (Top Left)
        self.score_panel = Panel(
            self.screen,
            (tamanoDinamico(self.anchopantalla, 20), tamanoDinamico(self.altopantalla, 8)),
            (tamanoDinamico(self.anchopantalla, 12), tamanoDinamico(self.altopantalla, 6)),
            self.DARK_BG, 
            int(tamanoDinamico(self.anchopantalla, 1)),
            self.CYAN, 2
        )
        
        # Lives Panel (Top Right - approximate width for 3 hearts)
        self.lives_panel = Panel(
            self.screen,
            (tamanoDinamico(self.anchopantalla, 20), tamanoDinamico(self.altopantalla, 8)),
            (tamanoDinamico(self.anchopantalla, 88), tamanoDinamico(self.altopantalla, 6)),
            self.DARK_BG, 
            int(tamanoDinamico(self.anchopantalla, 1)),
            self.CYAN, 2
        )

    def setup_game_objects(self):
        self.setup_ui_panels() # Init panels
        BLACK = (0, 0, 0, 0)
        # Enemy Spawn Points
        self.enemyPos = [
            SpawnPoint((tamanoDinamico(self.anchopantalla, 25), tamanoDinamico(self.altopantalla, 10))), 
            SpawnPoint((tamanoDinamico(self.anchopantalla, 75), tamanoDinamico(self.altopantalla, 10))),
            SpawnPoint((tamanoDinamico(self.anchopantalla, 25), tamanoDinamico(self.altopantalla, 90))),
            SpawnPoint((tamanoDinamico(self.anchopantalla, 75), tamanoDinamico(self.altopantalla, 90))),
            SpawnPoint((tamanoDinamico(self.anchopantalla, 50), tamanoDinamico(self.altopantalla, 20))),
            SpawnPoint((tamanoDinamico(self.anchopantalla, 50), tamanoDinamico(self.altopantalla, 80))),
            SpawnPoint((tamanoDinamico(self.anchopantalla, 10), tamanoDinamico(self.altopantalla, 50))),
            SpawnPoint((tamanoDinamico(self.anchopantalla, 90), tamanoDinamico(self.altopantalla, 50)))
        ]
        # ... (rest of setup)
        
        self.enemyID = [
            "enemigo_patron_circular", 
            "enemigo_patron_espiral",
            "enemigo_patron_espiral_alternado", 
            "enemigo_patron_circular_alternado",
            "enemigo_patron_estrella",
            "enemigo_patron_spray"
        ]
        
        # Player
        self.player = Player(
            self.settings.assets_path, 
            get_image(self.playerSheet, 0, 52, 52, BLACK), 
            self.bullet_array[0], 
            (tamanoDinamico(self.anchopantalla, 50), tamanoDinamico(self.altopantalla, 90)), 
            (tamanoDinamico(self.anchopantalla, 3), tamanoDinamico(self.anchopantalla, 3)), 
            3, 
            (self.anchopantalla, self.altopantalla)
        )
        self.player_life_image = pygame.transform.scale(
            pygame.image.load(self.settings.get_asset_path("Images/heart.png")), 
            (tamanoDinamico(self.anchopantalla, 3), tamanoDinamico(self.anchopantalla, 3))
        )

        self.playerCollide = pygame.Rect(self.player.rect.x, self.player.rect.y, tamanoDinamico(self.anchopantalla, 0.5), tamanoDinamico(self.anchopantalla, 0.5))
        self.playerGroup.add(self.player)
        
        self.enemyGenerator = EnemyGenerator(
            self.settings.assets_path, 
            self.enemies, 
            self.enemyPos, 
            0, 
            self.enemyID, 
            self.bullet_array, 
            "easy", 
            self.screen, 
            (self.anchopantalla, self.altopantalla)
        )

    def handle_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_f:
                    self.enemyGenerator.generateEnemy() # Debug spawn?
                if e.key == pygame.K_ESCAPE:
                    # Return to Main Menu
                    from .main_menu import MainMenuScene
                    self.bg_game_music.unload()
                    self.switch_to_scene(MainMenuScene)
            
            # Player shooting
            self.player.Shoot(e, self.bullets)

    def update(self, dt):
        self.last_dt = dt
        self.playerCollide.center = self.player.rect.center

        # Screen Shake Logic
        if self.screen_shake > 0:
            self.screen_shake -= 1 * dt
        if self.screen_shake < 0:
            self.screen_shake = 0

        # Updates
        for position in self.enemyPos:
            position.update(self.enemies)
            
        mouse_pos = pygame.mouse.get_pos()
        self.playerGroup.update(dt, mouse_pos, (self.anchopantalla, self.altopantalla))
        
        # Check coins (dead enemies)
        for enemy in self.enemies:
             if enemy.vida <= 0:
                 self.coins += 1

        self.enemies.update(self.bullets, dt, (self.anchopantalla, self.altopantalla))
        self.enemyGenerator.update((self.anchopantalla, self.altopantalla))
        
        screen_rect = self.screen.get_rect()
        self.bullets.update(screen_rect, dt)

        # Collisions
        bullets_to_enemies = pygame.sprite.groupcollide(self.enemies, self.bullets, False, False)
        for enemy, bullet_list in bullets_to_enemies.items():
            for b in bullet_list:
                if b.bullet_target == "enemies":
                    enemy.take_damage(1)
                    b.kill()

        for bullet in self.bullets:
            if bullet.bullet_target == "player" and self.playerCollide.colliderect(bullet.rect):
                self.screen_shake = 30
                self.punch2.play()
                self.player.take_damage(1)
                bullet.kill()
        
        if self.player.isDead:
            from .main_menu import MainMenuScene
            self.bg_game_music.unload()
            self.switch_to_scene(MainMenuScene)

    def draw(self, surface):
        # 1. Calculate Screen Shake Offset
        render_offset = [0, 0]
        if self.screen_shake > 0:
            render_offset[0] = randint(0, 10) - 4
            render_offset[1] = randint(0, 10) - 4

        # 2. Draw Background (Stars) on Main Screen
        # Clear screen first (optional if stars cover everything, but good practice)
        surface.fill((0, 0, 0))
        self.estrellas.update(self.last_dt) 
        
        # 3. Draw Game World (Entities) on Buffer
        # Clear buffer with transparent pixels
        self.game_surface.fill((0, 0, 0, 0))
        
        self.bullets.draw(self.game_surface)
        self.enemies.draw(self.game_surface)
        self.playerGroup.draw(self.game_surface)
        
        # 4. Blit Buffer to Main Screen (Entities over Stars)
        # Apply screen shake offset here
        surface.blit(self.game_surface, render_offset)
        
        # 5. Draw UI (On top of everything)
        # 5. Draw UI (On top of everything)
        if self.settings.mostrar_fps:
            fps = self.game_manager.clock.get_fps()
            fps_text = self.fps_font.render("FPS: " + str(int(fps//1)), True, self.CYAN)
            surface.blit(fps_text, fps_text.get_rect(center = (tamanoDinamico(self.anchopantalla, 50), tamanoDinamico(self.anchopantalla, 2))))
        
        # Draw Score Panel
        self.score_panel.draw()
        coins_text = self.coins_font.render("SCORE: " + str(self.coins), True, self.CYAN) # Cyan text
        surface.blit(coins_text, coins_text.get_rect(center=self.score_panel.rect.center))

        # Draw Lives Panel
        self.lives_panel.draw()
        # Draw Hearts loop
        # Calculate start pos to center hearts in panel
        heart_w = self.player_life_image.get_width()
        spacing = 5
        total_w = (self.player.vida * heart_w) + ((self.player.vida - 1) * spacing)
        start_x = self.lives_panel.rect.centerx - (total_w / 2)
        y_pos = self.lives_panel.rect.centery - (heart_w / 2)
        
        for i in range(self.player.vida):
             surface.blit(self.player_life_image, (start_x + (i * (heart_w + spacing)), y_pos))
