import pygame
from config import *

class Bala:
    def __init__(self, x, y, dx, dy, enemigo=False):
        self.x = x
        self.y = y
        self.dx = dx * 7 
        self.dy = dy * 7  
        self.radio = 5
        self.enemigo = enemigo  # True si es una bala enemiga
        self.color = ROJO if enemigo else AZUL  # Rojo para enemigos, azul para jugador

    def actualizar(self):
        self.x += self.dx
        self.y += self.dy

    def fuera_de_pantalla(self):
        return (self.x < -self.radio or self.x > ANCHO + self.radio or
                self.y < -self.radio or self.y > ALTO + self.radio)

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.radio)

    def verificar_colision(self, objeto):
        distancia = ((self.x - objeto.x)**2 + (self.y - objeto.y)**2)**0.5
        return distancia < self.radio + objeto.radio