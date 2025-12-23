from random import *
from pygame import *
import time as tm
from .utils import tamanoDinamico

class Estrellas():
    """
    A class to represent the stars in the background.

    ...

    Attributes
    ----------
    cantidad : int
        the number of stars
    superficie : pygame.Surface
        the surface to draw the stars on
    anchoPantalla : int
        the width of the screen
    altoPantalla : int
        the height of the screen
    estrellas : list
        a list of stars

    Methods
    -------
    update(deltaTime):
        Updates the stars.
    generar():
        Generates the stars.
    refrescar(anchoPantalla, altoPantalla):
        Refreshes the stars.
    """
    def __init__(self, superficie: Surface, cantidad: int, anchoPantalla: int, altoPantalla: int):
        """
        Constructs all the necessary attributes for the stars object.

        Parameters
        ----------
            superficie : pygame.Surface
                the surface to draw the stars on
            cantidad : int
                the number of stars
            anchoPantalla : int
                the width of the screen
            altoPantalla : int
                the height of the screen
        """
        self.cantidad = cantidad # La cantidad de estrellas a generar
        self.superficie = superficie
        self.anchoPantalla = anchoPantalla # El ancho de la pantalla
        self.altoPantalla = altoPantalla # El alto de la pantalla
        self.estrellas = self.generar() # Las estrellas

    def update(self, deltaTime: float):
        """
        Updates the stars.

        Parameters
        ----------
            deltaTime : float
                the time since the last frame
        """
        for estrella in self.estrellas:
            # Mueve las estrellas a su velocidad constantemente
            estrella[1][1] += estrella[3] * deltaTime
            # Si la estrella cae de la pantalla se devuelve al inicio
            if estrella[1][1] > self.altoPantalla:
                estrella[3] = randint(int(tamanoDinamico(self.anchoPantalla, 0.078125)), int(tamanoDinamico(self.anchoPantalla, 0.78125)))
                estrella[1][1] = -1
            # Dibuja la estrella en la superficie
            draw.circle(self.superficie, estrella[0], estrella[1], estrella[2])

    def generar(self):
        """
        Generates the stars.

        Returns
        -------
            list
                a list of stars
        """
        # Crea una variable interna para guardar cada estrella
        estrellas =[]

        # Crea cada una de las estrellas con valores random
        for _ in range(self.cantidad):
            randomWhite = randint(100, 230)
            randSize = uniform(int(tamanoDinamico(self.anchoPantalla, 0.078125)), int(tamanoDinamico(self.anchoPantalla, 0.390625)))
            randSpeed = uniform(int(tamanoDinamico(self.anchoPantalla, 0.078125)), int(tamanoDinamico(self.anchoPantalla, 0.78125)))
            particleRect = Rect(uniform(0, self.anchoPantalla), uniform(0, self.altoPantalla), randSize, randSize)
            estrellas.append([[randomWhite, randomWhite, randomWhite], [particleRect.x, particleRect.y], randSize, randSpeed])
        return estrellas
    
    def refrescar(self, anchoPantalla: int, altoPantalla: int):
        """
        Refreshes the stars.

        Parameters
        ----------
            anchoPantalla : int
                the width of the screen
            altoPantalla : int
                the height of the screen
        """
        # Calcula de nuevo el ancho y el alto de la pantalla
        self.anchoPantalla = anchoPantalla
        self.altoPantalla = altoPantalla

        # Elimina cada una de las estrellas creadas
        for estrella in self.estrellas:
            self.estrellas.remove(estrella)

        # Vuelve a hacer nuevas estrellas
        self.estrellas = self.generar()

class Boton():
    """
    A class to represent a button.

    ...

    Attributes
    ----------
    superficie : pygame.Surface
        the surface to draw the button on
    tamano : tuple[float]
        the size of the button
    posicion : tuple[int, int]
        the position of the button
    rect : pygame.Rect
        the rect of the button
    fuente : pygame.font.Font
        the font of the text
    texto : str
        the text of the button
    colorTexto : tuple[int]
        the color of the text
    colorTextoEncima : tuple[int]
        the color of the text when the mouse is over it
    textoRenderizado : pygame.Surface
        the rendered text
    textoRenderizadoEncima : pygame.Surface
        the rendered text when the mouse is over it
    boton : pygame.Surface
        the surface of the button
    sonidoClick : pygame.mixer.Sound
        the sound of the click
    sonidoEncima : pygame.mixer.Sound
        the sound when the mouse is over it
    yaSono : bool
        whether the sound has already been played
    tieneFondo : bool
        whether the button has a background
    colorFondo : tuple[int]
        the color of the background
    colorFondoEncima : tuple[int]
        the color of the background when the mouse is over it
    radio : float
        the radius of the corners
    hover : bool
        whether the mouse is over the button

    Methods
    -------
    update():
        Updates the button.
    refrescar(tamano, posicion):
        Refreshes the button.
    onHover():
        Checks if the mouse is over the button.
    onClick(funcion, pararMusica, musica, tiempoEspera, *args):
        Executes the function when the button is clicked.
    """
    def __init__(self, superficie: Surface, tamano: tuple[float], posicion: tuple[int, int], fuente: font.Font, texto: str, colorTexto: tuple[int], colorTextoEncima: tuple[int], sonidoClick: mixer.Sound, sonidoEncima: mixer.Sound, tieneFondo: bool, colorFondo: tuple[int], colorFondoEncima: tuple[int], radio: float):
        """
        Constructs all the necessary attributes for the button object.

        Parameters
        ----------
            superficie : pygame.Surface
                the surface to draw the button on
            tamano : tuple[float]
                the size of the button
            posicion : tuple[int, int]
                the position of the button
            fuente : pygame.font.Font
                the font of the text
            texto : str
                the text of the button
            colorTexto : tuple[int]
                the color of the text
            colorTextoEncima : tuple[int]
                the color of the text when the mouse is over it
            sonidoClick : pygame.mixer.Sound
                the sound of the click
            sonidoEncima : pygame.mixer.Sound
                the sound when the mouse is over it
            tieneFondo : bool
                whether the button has a background
            colorFondo : tuple[int]
                the color of the background
            colorFondoEncima : tuple[int]
                the color of the background when the mouse is over it
            radio : float
                the radius of the corners
        """
        self.superficie = superficie
        self.tamano = tamano
        self.posicion: tuple[int, int] = posicion
        self.rect = Rect((0, 0), self.tamano)
        self.rect.center = self.posicion
        self.fuente = fuente
        self.texto = texto
        self.colorTexto = colorTexto
        self.colorTextoEncima = colorTextoEncima
        self.textoRenderizado = fuente.render(self.texto, True, self.colorTexto)
        self.textoRenderizadoEncima = fuente.render(self.texto, True, self.colorTextoEncima)
        self.boton = Surface(self.tamano, SRCALPHA)
        self.boton.set_colorkey((0, 0 ,0))
        self.sonidoClick = sonidoClick
        if sonidoEncima != None:
            self.sonidoEncima = sonidoEncima
            self.yaSono = False
        self.tieneFondo = tieneFondo
        if tieneFondo:
            self.colorFondo = colorFondo
            self.colorFondoEncima = colorFondoEncima
            self.radio = radio
            
        self.text_offset_y = tamanoDinamico(self.tamano[1], 15)

        self.hover = False
        

    def update(self):
        """
        Updates the button.
        """
        self.boton.fill((0, 0, 0, 0)) # Clean with transparency
        
        border_color = (0, 243, 255) # Neon Cyan default
        
        if not self.hover:
            # Normal State
            if self.tieneFondo:
                # Ghost style: Transparent bg, colored border? Or Solid?
                # User asked for "better". Let's do:
                # Background: self.colorFondo
                # Border: border_color (thin)
                draw.rect(self.boton, self.colorFondo, ((0,0), self.boton.get_size()), border_radius=int(self.radio))
                draw.rect(self.boton, border_color, ((0,0), self.boton.get_size()), 2, border_radius=int(self.radio))
                
            # Text
            self.boton.blit(self.textoRenderizado, self.textoRenderizado.get_rect(center= (self.boton.get_rect().centerx, self.boton.get_rect().centery + self.text_offset_y)))
            self.yaSono = False
        else:
            # Hover State
            if self.tieneFondo:
                # Hover: Fill with border color (glowy) or brighter background?
                # Let's use colorFondoEncima as fill, and make it glow.
                draw.rect(self.boton, self.colorFondoEncima, ((0,0), self.boton.get_size()), border_radius=int(self.radio))
                # Thicker border
                draw.rect(self.boton, (255, 255, 255), ((0,0), self.boton.get_size()), 3, border_radius=int(self.radio))
                
            # Text (Encima)
            self.boton.blit(self.textoRenderizadoEncima, self.textoRenderizado.get_rect(center= (self.boton.get_rect().centerx, self.boton.get_rect().centery + self.text_offset_y)))

        self.onHover()
        self.superficie.blit(self.boton, (self.rect.x, self.rect.y))

    def refrescar(self, tamano, posicion):
        """
        Refreshes the button.

        Parameters
        ----------
            tamano : tuple[float]
                the size of the button
            posicion : tuple[int, int]
                the position of the button
        """
        self.tamano = tamano
        self.posicion = posicion
        self.text_offset_y = tamanoDinamico(self.tamano[1], 15)

    def onHover(self):
        """
        Checks if the mouse is over the button.
        """
        mx, my = mouse.get_pos()

        self.hover = False
        if self.rect.collidepoint((mx, my)):
            # Dibujar el fondo si tiene fondo
            if self.tieneFondo:
                # Dibuja el fondo en el boton
                draw.rect(self.boton, self.colorFondoEncima, ((0,0), self.boton.get_size()), border_radius=self.radio)
                # Dibuja el texto
                self.boton.blit(self.textoRenderizadoEncima, self.textoRenderizado.get_rect(center= (self.boton.get_rect().centerx, self.boton.get_rect().centery + self.text_offset_y)))
            else:
                # Dibuja el texto
                self.boton.blit(self.textoRenderizadoEncima, self.textoRenderizado.get_rect(center= (self.boton.get_rect().centerx, self.boton.get_rect().centery + self.text_offset_y)))
            self.hover = True
            if not self.yaSono:
                self.sonidoEncima.play()
                self.yaSono = True
    
    def onClick(self, funcion, pararMusica, musica, tiempoEspera, *args):
        """
        Executes the function when the button is clicked.

        Parameters
        ----------
            funcion : function
                the function to execute
            pararMusica : bool
                whether to stop the music
            musica : pygame.mixer.Sound
                the music
            tiempoEspera : float
                the time to wait
            *args : tuple
                the arguments of the function
        """
        if pararMusica:
            musica.pause()
        self.sonidoClick.play()
        tm.sleep(tiempoEspera)
        funcion(*args)

class Panel():
    def __init__(self, superficie: Surface, tamano: tuple[float], posicion: tuple[int, int], colorFondo: tuple[int], radio: float, borde_color: tuple[int] = None, borde_ancho: int = 0):
        self.superficie = superficie
        self.tamano = tamano
        self.posicion = posicion
        self.rect = Rect((0, 0), self.tamano)
        self.rect.center = self.posicion
        self.colorFondo = colorFondo
        self.radio = radio
        self.borde_color = borde_color
        self.borde_ancho = borde_ancho
        
        self.surface = Surface(self.tamano, SRCALPHA)
        
    def draw(self):
        self.surface.fill((0,0,0,0))
        # Draw background
        draw.rect(self.surface, self.colorFondo, ((0,0), self.tamano), border_radius=int(self.radio))
        
        # Draw border if exists
        if self.borde_color and self.borde_ancho > 0:
            draw.rect(self.surface, self.borde_color, ((0,0), self.tamano), self.borde_ancho, border_radius=int(self.radio))
            
        self.superficie.blit(self.surface, self.rect)

# Update Boton to support borders/modern style better
# We will inject a 'draw_modern' logic or just update update()
# Current update is specific. Let's make it more flexible.
# For this refactor, I'll stick to the existing class structure 
# but improve the rendering inside 'update'.
        