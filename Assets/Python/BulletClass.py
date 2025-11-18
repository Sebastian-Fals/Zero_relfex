from pygame import *
from math import *

class Bullet(sprite.Sprite):
    """
    A class to represent a bullet.

    ...

    Attributes
    ----------
    image : pygame.Surface
        the bullet's sprite
    angle : float
        the angle of the bullet in radians
    rect : pygame.Rect
        the rectangle of the bullet
    move : list[float, float]
        the position of the bullet
    speed_magnitude : int
        the speed of the bullet
    speed : tuple[float, float]
        the speed of the bullet in x and y
    bullet_target : str
        the target of the bullet

    Methods
    -------
    update(screen_rect, deltaTime):
        Updates the bullet's position.
    remove(screen_rect):
        Removes the bullet if it is off screen.
    """
    def __init__(self, location, angle, sprite, speed, bullet_target, size):
        """
        Constructs all the necessary attributes for the bullet object.

        Parameters
        ----------
            location : tuple[int, int]
                the initial location of the bullet
            angle : float
                the angle of the bullet in degrees
            sprite : pygame.Surface
                the bullet's sprite
            speed : int
                the speed of the bullet
            bullet_target : str
                the target of the bullet
            size : tuple[int, int]
                the size of the bullet
        """
        super().__init__()
        self.image = sprite
        self.image = transform.scale(self.image, size)
        #Rota la bala hacia donde está viendo el player
        self.angle = radians(angle - 90)
        self.image = transform.rotate(self.image, -angle)
        self.rect = self.image.get_rect(center = location)
        self.move = [self.rect.x, self.rect.y]
        #Se calcula la velocidad en X y en Y respectivamente
        self.speed_magnitude = speed
        self.speed = (self.speed_magnitude* cos(self.angle),
                      self.speed_magnitude* sin(self.angle))
        self.bullet_target = bullet_target
        
    def update(self, screen_rect, deltaTime):
        """
        Updates the bullet's position.

        Parameters
        ----------
            screen_rect : pygame.Rect
                the rectangle of the screen
            deltaTime : float
                the time since the last frame
        """
        self.move[0] += self.speed[0] * deltaTime
        self.move[1] += self.speed[1] * deltaTime
        self.rect.topleft = self.move
        self.remove(screen_rect)

    def remove(self, screen_rect):
        """
        Removes the bullet if it is off screen.

        Parameters
        ----------
            screen_rect : pygame.Rect
                the rectangle of the screen
        """
        if not self.rect.colliderect(screen_rect):
            self.kill()