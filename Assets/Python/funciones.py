import pickle
from pygame import *

#Esta funcion sirve para localizar un sprite en una prite sheet y convertirlo en una imagen
def get_image(sheet: Surface, frame: int, width: int, height: int, colour: tuple[int]) -> Surface:
    img = Surface((width, height)).convert_alpha()
    img.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    img.set_colorkey(colour)
    return img.convert_alpha()

#Esta funcion calcula un numero según el porcentaje de un tamaño que le pasemos
def tamanoDinamico(tamano, porcentaje):
    tamanoDinamico = porcentaje * tamano/100
    return tamanoDinamico

# Funcion para escribir en el archivo
def save(archivo_binario, variables):
    with open(archivo_binario, "wb") as f:
            pickle.dump(variables, f)