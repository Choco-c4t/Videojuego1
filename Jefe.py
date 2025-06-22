import pygame
from Enemigos import EnemigoBase
from config import ROJO, VERDE
from bala import Bala

class JefeFinal(EnemigoBase):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vida = 500
        self.vida_maxima = 500
        self.velocidad = 1.2
        self.daño = 20
        self.disparos_recibidos = 0
        self.vulnerable = False
        self.tiempo_vulnerable = 0
        self.balas = []  
        self.tiempo_entre_disparos = 90 
        self.contador_disparo = 0 
        self.cooldown_colision = 60  #1 seg
        self.tiempo_cooldown = 0 
        self.width = 80
        self.height = 80
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)

    def recibir_daño(self, cantidad):
        if self.vulnerable:
            self.vida -= cantidad
        else:
            self.disparos_recibidos += 1
            if self.disparos_recibidos >= 10:
                self.vulnerable = True
                self.tiempo_vulnerable = 460

    def disparar(self, objetivo_x, objetivo_y):
        dx = objetivo_x - self.x
        dy = objetivo_y - self.y
        distancia = max(1, (dx**2 + dy**2)**0.5)
        self.balas.append(Bala(self.x, self.y, dx / distancia, dy / distancia, enemigo=True))

    def actualizar(self, jugador):
        if self.vulnerable:
            self.tiempo_vulnerable -= 1
            if self.tiempo_vulnerable <= 0:
                self.vulnerable = False
                self.disparos_recibidos = 0
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = max(1, (dx**2 + dy**2) ** 0.5)
        self.x += (dx / distancia) * self.velocidad
        self.y += (dy / distancia) * self.velocidad
        self.rect.center = (self.x, self.y)

        if self.rect.colliderect(jugador.rect):
            if self.tiempo_cooldown <= 0:
                jugador.recibir_daño(self.daño)
                self.tiempo_cooldown = self.cooldown_colision
        if self.tiempo_cooldown > 0:
            self.tiempo_cooldown -= 1

        self.contador_disparo += 1
        if self.contador_disparo >= self.tiempo_entre_disparos:
            self.disparar(jugador.x, jugador.y)
            self.contador_disparo = 0

        for bala in self.balas[:]:
            bala.actualizar()
            if bala.fuera_de_pantalla():
                self.balas.remove(bala)
            elif bala.rect.colliderect(jugador.rect):
                jugador.recibir_daño(10)
                self.balas.remove(bala)

        self.x = max(self.width//2, min(800 - self.width//2, self.x))
        self.y = max(self.height//2, min(600 - self.height//2, self.y))

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, (255, 0, 255), self.rect)
        pygame.draw.rect(pantalla, ROJO, (self.x - 40, self.y - 50, 80, 8))
        pygame.draw.rect(pantalla, VERDE, (self.x - 40, self.y - 50, 80 * (self.vida / self.vida_maxima), 8))
        
        for bala in self.balas:
            bala.dibujar(pantalla)



