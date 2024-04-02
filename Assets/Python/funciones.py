from pygame import *

#Esta funcion sirve para localizar un sprite en una prite sheet y convertirlo en una imagen
def get_image(sheet, frame, width, height, colour):
    img = Surface((width, height)).convert_alpha()
    img.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    img.set_colorkey(colour)
    return img.convert_alpha()

#Esta funcion calcula un numero según el porcentaje de un tamaño que le pasemos
def responsiveSizeAndPosition(displaySize, XorY, number):
    pixelSize = number * displaySize[XorY]/100
    return float(pixelSize)