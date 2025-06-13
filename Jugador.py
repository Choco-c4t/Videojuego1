import pygame
from config import *
from bala import Bala

class Jugador:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 5
        self.radio = 20
        self.balas = []
        self.vida = 100
        self.vida_maxima = 100
        self.sprite = SPRITE_JUGADOR
        self.direccion = "derecha"  # Puede ser: "arriba", "abajo", "izquierda", "derecha"
        self.invencible=False

    def ser_invencible(self,miliseg=10000):
        self.invencible=True

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

        if self.x < self.radio:
            self.x = self.radio
        if self.x > ANCHO - self.radio:
            self.x = ANCHO - self.radio
        if self.y < self.radio:
            self.y = self.radio
        if self.y > ALTO - self.radio:
            self.y = ALTO - self.radio

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

    def actualizar_balas(self, enemigos):
        balas_activas = []
        
        for bala in self.balas:
            bala.actualizar()
            
            golpeo = False
            for enemigo in enemigos:
                distancia = ((bala.x - enemigo.x)**2 + (bala.y - enemigo.y)**2)**0.5
                if distancia < enemigo.radio:
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
        if self.sprite:
            sprite_escalado = pygame.transform.scale(self.sprite, (self.radio * 2, self.radio * 2))
        # Rotar segun la direccion
            if self.direccion == "arriba":
                sprite_final = pygame.transform.rotate(sprite_escalado, 90)
            elif self.direccion == "abajo":
                sprite_final = pygame.transform.rotate(sprite_escalado, -90)
            elif self.direccion == "izquierda":
                sprite_final = pygame.transform.flip(sprite_escalado, True, False)
            else:  # derecha
                sprite_final = sprite_escalado

            pantalla.blit(sprite_final, (self.x - self.radio, self.y - self.radio))
        else:
            pygame.draw.circle(pantalla, AZUL, (int(self.x), int(self.y)), self.radio)
        
            pygame.draw.rect(pantalla, ROJO, (self.x - 20, self.y - 30, 40, 5))
            pygame.draw.rect(pantalla, VERDE, (self.x - 20, self.y - 30, 40 * (self.vida/self.vida_maxima), 5))
