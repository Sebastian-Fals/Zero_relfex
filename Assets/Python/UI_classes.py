from random import *
from pygame import *
import time as tm
from Assets.Python.funciones import tamanoDinamico

class Estrellas():
    def __init__(self, superficie: Surface, cantidad: int, anchoPantalla: int, altoPantalla: int):
        self.cantidad = cantidad # La cantidad de estrellas a generar
        self.superficie = superficie
        self.anchoPantalla = anchoPantalla # El ancho de la pantalla
        self.altoPantalla = altoPantalla # El alto de la pantalla
        self.estrellas = self.generar() # Las estrellas

    def update(self, deltaTime: float):
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
        # Calcula de nuevo el ancho y el alto de la pantalla
        self.anchoPantalla = anchoPantalla
        self.altoPantalla = altoPantalla

        # Elimina cada una de las estrellas creadas
        for estrella in self.estrellas:
            self.estrellas.remove(estrella)

        # Vuelve a hacer nuevas estrellas
        self.estrellas = self.generar()

class Boton():
    def __init__(self, superficie: Surface, tamano: tuple[float], posicion: tuple[int, int], fuente: font.Font, texto: str, colorTexto: tuple[int], colorTextoEncima: tuple[int], sonidoClick: mixer.Sound, sonidoEncima: mixer.Sound, tieneFondo: bool, colorFondo: tuple[int], colorFondoEncima: tuple[int], radio: float):
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

        self.hover = False
        

    def update(self):
        self.boton.fill((0, 0, 0))
        if not self.hover:
            # Dibujar el fondo si tiene fondo
            if self.tieneFondo:
                # Dibuja el fondo en el boton
                draw.rect(self.boton, self.colorFondo, ((0,0), self.boton.get_size()), border_radius=self.radio)
            # Dibuja el texto
            self.boton.blit(self.textoRenderizado, self.textoRenderizado.get_rect(center= (self.boton.get_rect().centerx, self.boton.get_rect().centery + tamanoDinamico(self.boton.get_size()[1], 15))))
            self.yaSono = False
        else:
            # Dibuja el texto
            self.boton.blit(self.textoRenderizadoEncima, self.textoRenderizado.get_rect(center= (self.boton.get_rect().centerx, self.boton.get_rect().centery + tamanoDinamico(self.boton.get_size()[1], 15))))

        self.onHover()
        # Dibuja el boton en la pantalla
        self.superficie.blit(self.boton, (self.rect.x, self.rect.y))

    def refrescar(self, tamano, posicion):
        self.tamano = tamano
        self.posicion = posicion

    def onHover(self):
        mx, my = mouse.get_pos()

        self.hover = False
        if self.rect.collidepoint((mx, my)):
            # Dibujar el fondo si tiene fondo
            if self.tieneFondo:
                # Dibuja el fondo en el boton
                draw.rect(self.boton, self.colorFondoEncima, ((0,0), self.boton.get_size()), border_radius=self.radio)
                # Dibuja el texto
                self.boton.blit(self.textoRenderizadoEncima, self.textoRenderizado.get_rect(center= (self.boton.get_rect().centerx, self.boton.get_rect().centery + tamanoDinamico(self.boton.get_size()[1], 15))))
            else:
                # Dibuja el texto
                self.boton.blit(self.textoRenderizadoEncima, self.textoRenderizado.get_rect(center= (self.boton.get_rect().centerx, self.boton.get_rect().centery + tamanoDinamico(self.boton.get_size()[1], 15))))
            self.hover = True
            if not self.yaSono:
                self.sonidoEncima.play()
                self.yaSono = True
    
    def onClick(self, funcion, pararMusica, musica, tiempoEspera, *args):
        if pararMusica:
            musica.pause()
        self.sonidoClick.play()
        tm.sleep(tiempoEspera)
        funcion(*args)        