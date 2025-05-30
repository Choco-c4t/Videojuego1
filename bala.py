from config import *
class Bala:
    def __init__(self, x, y, dx, dy): #posicion y direccion
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.velocidad = 10
        self.radio = 5 #colision
        self.daño = 25

    def actualizar(self):
        self.x += self.dx * self.velocidad
        self.y += self.dy * self.velocidad

    def fuera_de_pantalla(self):
        return not (0 <= self.x <= ANCHO and 0 <= self.y <= ALTO)