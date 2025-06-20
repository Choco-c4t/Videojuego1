import pygame
from config import *
from bala import Bala

class Jugador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 5
        self.balas = []
        self.vida = 100
        self.vida_maxima = 100
        self.sprite = SPRITE_JUGADOR
        self.direccion = "derecha"
        self.width = 40 
        self.height = 40
        self.rect = pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)
        self.robo_vida_activo = False
        self.tiempo_robo_vida = 0  # Rango
        self.duracion_robo = 300
        self.radio_robo_vida = 20

    def mover(self, teclas):
        if teclas[pygame.K_w]:
            self.y -= self.velocidad
            self.direccion = "arriba"
        if teclas[pygame.K_s]:
            self.y += self.velocidad
            self.direccion = "abajo"
        if teclas[pygame.K_a]:
            self.x -= self.velocidad
            self.direccion = "izquierda"
        if teclas[pygame.K_d]:
            self.x += self.velocidad
            self.direccion = "derecha"

        self.rect.center = (self.x, self.y)
        
        
        if self.x < self.width // 2:
            self.x = self.width // 2
        if self.x > ANCHO - self.width // 2:
            self.x = ANCHO - self.width // 2
        if self.y < self.height // 2:
            self.y = self.height // 2
        if self.y > ALTO - self.height // 2:
            self.y = ALTO - self.height // 2

    def verificar_colision_enemigo(self, enemigo):
        return self.rect.colliderect(enemigo.rect)

    def disparar(self):
        if len(self.balas) < 3:  # Max 3 balas
            if self.direccion == "arriba":
                self.balas.append(Bala(self.x, self.y, 0, -1))
            elif self.direccion == "abajo":
                self.balas.append(Bala(self.x, self.y, 0, 1))
            elif self.direccion == "izquierda":
                self.balas.append(Bala(self.x, self.y, -1, 0))
            else:  # derecha
                self.balas.append(Bala(self.x, self.y, 1, 0))
        
        if self.robo_vida_activo:
            self.vida = min(self.vida + 5, self.vida_maxima) 

    def actualizar_balas(self, enemigos):
        balas_activas = []
        for bala in self.balas:
            bala.actualizar()
            golpeo = False
            for enemigo in enemigos:
                if bala.rect.colliderect(enemigo.rect):
                    enemigo.recibir_daño(10)
                    golpeo = True
                    break           
            if not bala.fuera_de_pantalla() and not golpeo:
                balas_activas.append(bala)      
        self.balas = balas_activas

    def recibir_daño(self, cantidad):
        self.vida -= cantidad

    def esta_muerto(self):
        return self.vida <= 0

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, AZUL, self.rect)
        pygame.draw.rect(pantalla, ROJO, (self.x - 20, self.y - 30, 40, 5))
        pygame.draw.rect(pantalla, VERDE, (self.x - 20, self.y - 30, 40 * (self.vida / self.vida_maxima), 5))

        if self.robo_vida_activo:
            pygame.draw.circle(pantalla, (255, 0, 255, 50), (int(self.x), int(self.y)), self.radio_robo_vida, 2)
    
    def activar_robo_vida(self):
        if not self.robo_vida_activo:
            self.robo_vida_activo = True
            self.tiempo_robo_vida = self.duracion_robo
            self.color = MORADO
            return True
        return False
    
    def robar_vida(self, enemigos):
        if not self.robo_vida_activo:
            return           
        self.tiempo_robo_vida -= 1
        if self.tiempo_robo_vida <= 0:
            self.robo_vida_activo = False
            self.color = AZUL
            return
        
        for enemigo in enemigos[:]: 
            if enemigo.esta_muerto() and self.rect.colliderect(enemigo.rect):
                self.vida = min(self.vida + 10, self.vida_maxima)
                enemigos.remove(enemigo)
