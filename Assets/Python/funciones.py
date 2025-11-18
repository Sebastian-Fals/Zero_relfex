import pickle
from pygame import *

#Esta funcion sirve para localizar un sprite en una prite sheet y convertirlo en una imagen
def get_image(sheet: Surface, frame: int, width: int, height: int, colour: tuple[int]) -> Surface:
    """
    Gets an image from a sprite sheet.

    Parameters
    ----------
        sheet : pygame.Surface
            the sprite sheet
        frame : int
            the frame of the image
        width : int
            the width of the image
        height : int
            the height of the image
        colour : tuple[int]
            the color key of the image

    Returns
    -------
        pygame.Surface
            the image
    """
    img = Surface((width, height)).convert_alpha()
    img.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    img.set_colorkey(colour)
    return img.convert_alpha()

#Esta funcion calcula un numero según el porcentaje de un tamaño que le pasemos
def tamanoDinamico(tamano, porcentaje):
    """
    Calculates a dynamic size.

    Parameters
    ----------
        tamano : int
            the size
        porcentaje : int
            the percentage of the size

    Returns
    -------
        int
            the dynamic size
    """
    tamanoDinamico = porcentaje * tamano/100
    return tamanoDinamico

# Funcion para escribir en el archivo
def save(archivo_binario, variables):
    """
    Saves the variables in a binary file.

    Parameters
    ----------
        archivo_binario : str
            the path of the binary file
        variables : list
            the variables to save
    """
    with open(archivo_binario, "wb") as f:
            pickle.dump(variables, f)