import time as tm
from pygame import *
from random import *
from threading import *
from GameEntities import Enemies

class SpawnPoint():
    def __init__(self, position):
        self.position = position
        self.canSpawn = True

    def update(self, group):
        # Por defecto, permitir el spawn si el grupo está vacío
        self.canSpawn = True if not group.sprites() else False

        # Verificar si algún sprite en el grupo ocupa la misma posición
        for enemy in group:
            if enemy.position == self.position:
                self.canSpawn = False
                break  # Si encontramos un sprite en la misma posición, no necesitamos continuar verificando
            else:
                self.canSpawn = True
        

class EnemyGenerator():
    def __init__(self, group,  spawnPoints, enemyCount, enemy_IDs, bulletSprite, difficulty):
        self.spawnPoints = spawnPoints
        self.enemyCount = enemyCount
        self.enemy_IDs = enemy_IDs
        self.bulletSprite = bulletSprite
        self.group = group
        self.difficulty = difficulty
        self.lock = Lock()
        self.has_spawned = False  # Bandera para rastrear si se ha ejecutado el hilo
        self.enemies_generated = 0  # Contador de enemigos generados

    def update(self):
        any_spawn_points_occupied = all(spawn_point.canSpawn for spawn_point in self.spawnPoints)
        if any_spawn_points_occupied:
            self.setDifficulty()
            self.enemies_generated = 0
            # Utilizar threading para generar enemigos sin bloquear el hilo principal
            enemy_thread = Thread(target=self.generateEnemies)
            enemy_thread.start()

    def generateEnemies(self):
        with self.lock:
            while self.enemies_generated < self.enemyCount:
                for position in self.spawnPoints:
                    position.update(self.group)
                # Verifica si todos los spawnPoints están ocupados
                all_spawn_points_occupied = all(not spawn_point.canSpawn for spawn_point in self.spawnPoints)
                if all_spawn_points_occupied:
                    return

                randomPosition = randint(0, (len(self.spawnPoints) - 1))
                randomID = randint(0, (len(self.enemy_IDs) - 1))
                while self.spawnPoints[randomPosition].canSpawn == False:
                    randomPosition = randint(0, (len(self.spawnPoints) - 1))
                if self.spawnPoints[randomPosition].canSpawn == True:
                    self.group.add(Enemies(image.load("Assets/circular_enemy.png").convert_alpha(), self.bulletSprite, self.spawnPoints[randomPosition].position, (40, 40), 10, self.enemy_IDs[randomID]))
                tm.sleep(0.5)
                self.enemies_generated += 1

    def setDifficulty(self):
        if self.difficulty == "easy":
            self.enemyCount = randint(1, 3)
        if self.difficulty == "medium":
            self.enemyCount = randint(2, 5)
        if self.difficulty == "hard":
            self.enemyCount = randint(4, 8)