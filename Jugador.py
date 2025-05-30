import pygame
from config import *
from bala import Bala

class Jugador:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.velocidad = 5
        self.radio = 20
        self.balas = []
        self.vida = 100
        self.vida_max = 100

    def mover(self, teclas):
        if teclas[pygame.K_w]: 
            self.y -= self.velocidad
        if teclas[pygame.K_s]: 
            self.y += self.velocidad
        if teclas[pygame.K_a]: 
            self.x -= self.velocidad
        if teclas[pygame.K_d]: 
            self.x += self.velocidad

        # No salga de los bordes
        self.x = max(self.radio, min(ANCHO - self.radio, self.x))
        self.y = max(self.radio, min(ALTO - self.radio, self.y))

    #con barra espaciadora
    def disparar(self): #coord del mouse
        mx,my = pygame.mouse.get_pos()
        dx = mx -self.x
        dy = my-self.y
        distancia = (dx ** 2 + dy ** 2)**0.5 #long entre el jugador
        if distancia == 0:
            return 
        dx = dx / distancia #misma velocidad
        dy = dy / distancia
        self.balas.append(Bala(self.x, self.y, dx, dy))
    
    
    def actualizar_balas(self):
        nuevas_balas = []
        for bala in self.balas:
             bala.actualizar()
             if not bala.fuera_de_pantalla():
                  nuevas_balas.append(bala)
        self.balas = nuevas_balas


    def recibir_daño(self, cantidad):
        self.vida -= cantidad

    def esta_muerto(self):
        return self.vida <= 0

