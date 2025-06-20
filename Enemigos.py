import pygame
import random
from bala import Bala
from config import *

class EnemigoBase:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vida = 100
        self.vida_maxima = 100
        self.velocidad = 1.3
        self.daño = 10
        self.sprite = SPRITE_ENEMIGO_BASE
        self.color = ROJO  
        self.cooldown_colision = 60
        self.tiempo_cooldown = 0 
        self.width = 40
        self.height = 40 
        self.rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

    def mover_hacia_jugador(self, jugador_x, jugador_y):
        # Calcular dirección
        dx = jugador_x - self.x
        dy = jugador_y - self.y
        distancia = max(1, (dx**2 + dy**2)**0.5)
        
        self.x += (dx / distancia) * self.velocidad
        self.y += (dy / distancia) * self.velocidad
        self.rect.center = (self.x, self.y)

    def actualizar(self, jugador):
        self.mover_hacia_jugador(jugador.x, jugador.y)
        self.verificar_colision_jugador(jugador)

    def verificar_colision_jugador(self, jugador):
        if self.rect.colliderect(jugador.rect):
            if self.tiempo_cooldown == 0:
                jugador.recibir_daño(self.daño)
                self.tiempo_cooldown = self.cooldown_colision
            return True
        return False

    def recibir_daño(self, cantidad):
        self.vida -= cantidad

    def esta_muerto(self):
        return self.vida <= 0



    def dibujar(self, pantalla):
        if self.sprite:
            sprite_escalado = pygame.transform.scale(self.sprite, (self.radio*2, self.radio*2))
            pantalla.blit(sprite_escalado, (self.x - self.radio, self.y - self.radio))
        else:
            pygame.draw.rect(pantalla,self.color,self.rect)
            pygame.draw.rect(pantalla, ROJO, (self.x - 20, self.y - 30, 40, 5))
            pygame.draw.rect(pantalla, VERDE, (self.x - 20, self.y - 30, 40 * (self.vida/self.vida_maxima), 5))
    
    def dibujar_balas(self, pantalla):
        pass

    def dibujar_minions(self, pantalla):
        pass


class EnemigoDispara(EnemigoBase):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vida = 60
        self.vida_maxima = 60
        self.velocidad = 1.0
        self.sprite = SPRITE_ENEMIGO_DISPARA
        self.color = NARANJA
        self.balas = []
        self.tiempo_entre_disparos = 90  
        self.contador_disparo = 0
        self.cooldown_colision = 60  #1 seg
        self.tiempo_cooldown = 0
        self.width = 30
        self.height = 30
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)

    def actualizar(self, jugador):
        super().actualizar(jugador)  

        if self.tiempo_cooldown > 0:
            self.tiempo_cooldown -= 1

        self.contador_disparo += 1
        if self.contador_disparo >= self.tiempo_entre_disparos:
            self.disparar(jugador.x, jugador.y)
            self.contador_disparo = 0

        for bala in self.balas[:]:
            bala.actualizar()
            if bala.rect.colliderect(jugador.rect):
                jugador.recibir_daño(10)
                self.balas.remove(bala)
                continue

            if bala.fuera_de_pantalla():
                self.balas.remove(bala)

    def disparar(self, objetivo_x, objetivo_y):
        dx = objetivo_x - self.x
        dy = objetivo_y - self.y
        distancia = max(1, (dx**2 + dy**2)**0.5)
        
        self.balas.append(Bala(self.x, self.y, dx/distancia, dy/distancia, enemigo=True))

    def dibujar_balas(self, pantalla):
        for bala in self.balas:
            bala.dibujar(pantalla)



class EnemigoInvocador(EnemigoBase):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vida = 80
        self.vida_maxima = 80
        self.velocidad = 0.8
        self.sprite = SPRITE_ENEMIGO_INVOCADOR
        self.color = MORADO
        self.minions = []
        self.tiempo_entre_invocaciones = 200
        self.contador_invocacion = 0
        self.cooldown_colision = 60
        self.tiempo_cooldown = 0 
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)

    def actualizar(self, jugador):
        self.mover_hacia_jugador(jugador.x, jugador.y)

        if self.tiempo_cooldown > 0:
            self.tiempo_cooldown -= 1

        self.contador_invocacion += 1
        if self.contador_invocacion >= self.tiempo_entre_invocaciones and len(self.minions) < 3:
            self.invocar_minion()
            self.contador_invocacion = 0

        for minion in self.minions[:]:
            minion.actualizar(jugador)
            for bala in jugador.balas[:]:  
                if bala.rect.colliderect(minion.rect):
                    minion.recibir_daño(10)  
                    jugador.balas.remove(bala) 
                    break  

            if minion.esta_muerto():
                self.minions.remove(minion)
        self.verificar_colision_jugador(jugador)


    def invocar_minion(self):
        x = self.x + random.randint(-50, 50)
        y = self.y + random.randint(-50, 50)
        tipo = random.choice(['colision', 'disparo'])
        if tipo == 'colision':
            self.minions.append(MinionColision(x, y))
        else:
            self.minions.append(MinionDispara(x, y))

    def dibujar_minions(self, pantalla):
        for minion in self.minions:
            minion.dibujar(pantalla)
            minion.dibujar_balas(pantalla)


class MinionColision(EnemigoBase):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.vida = 40
        self.vida_maxima = 40
        self.velocidad = 1.8
        self.sprite = SPRITE_MINION
        self.color = AMARILLO
        self.cooldown_colision = 60
        self.tiempo_cooldown = 0 
        self.daño = 10 
        self.width = 24
        self.height = 24
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)

    def actualizar(self, jugador):
        super().actualizar(jugador)
        if self.tiempo_cooldown > 0:
            self.tiempo_cooldown -= 1

    def dibujar_balas(self, pantalla):
        pass


class MinionDispara(MinionColision):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = AZUL
        self.balas = []
        self.tiempo_entre_disparos = 120
        self.contador_disparo = 0
        self.daño = 5 
        self.rect = pygame.Rect(x - self.width//2, y - self.height//2, self.width, self.height)

    def actualizar(self, jugador):
        self.mover_hacia_jugador(jugador.x, jugador.y)

        if self.tiempo_cooldown > 0:
            self.tiempo_cooldown -= 1

        self.contador_disparo += 1
        if self.contador_disparo >= self.tiempo_entre_disparos:
            self.disparar(jugador.x, jugador.y)
            self.contador_disparo = 0

        for bala in self.balas[:]:
            bala.actualizar()
            if bala.rect.colliderect (jugador.rect):
                jugador.recibir_daño(self.daño)
                self.balas.remove(bala)
                continue
            if bala.fuera_de_pantalla():
                self.balas.remove(bala)

        self.verificar_colision_jugador(jugador)

    def disparar(self, objetivo_x, objetivo_y):
        dx = objetivo_x - self.x
        dy = objetivo_y - self.y
        distancia = max(1, (dx**2 + dy**2)**0.5)
        self.balas.append(Bala(self.x, self.y, dx/distancia, dy/distancia, enemigo=True))

    def dibujar_balas(self, pantalla):
        for bala in self.balas:
            bala.dibujar(pantalla)

