import pygame
from config import *

class Bala:
    def __init__(self, x, y, dx, dy, enemigo=False):
        self.x = x
        self.y = y
        self.dx = dx * 7 
        self.dy = dy * 7  
        self.enemigo = enemigo  # True si es una bala enemiga
        self.color = ROJO if enemigo else AZUL  # Rojo para enemigos, azul para jugador
        self.width = 10
        self.height = 10
        self.rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)


    def actualizar(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)

    def fuera_de_pantalla(self):
        return (self.x < -self.width or self.x > ANCHO + self.width or
                self.y < -self.height or self.y > ALTO + self.height)

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, self.rect)

    def verificar_colision(self, objeto):
        return self.rect.colliderect(objeto.rect)
