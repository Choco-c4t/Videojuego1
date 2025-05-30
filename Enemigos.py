import math, random
from bala import Bala
from config import *

class EnemigoBase:
    def __init__(self, x, y, vida=100,velocidad =1.5, radio = 20):
        self.x = x
        self.y = y
        self.vida = vida
        self.radio = radio
        self.velocidad = velocidad
        self.daño = 10
        self.enfriamiento_golpe = 0

    def actualizar(self, jugador):
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = (dx ** 2 + dy ** 2)**0.5 #dist total entre el jugador 
        if distancia != 0:
            dx /= distancia
            dy /= distancia
            self.x += dx * self.velocidad
            self.y += dy * self.velocidad

        # Colision con el jugador
        if distancia < self.radio + jugador.radio:
            if self.enfriamiento_golpe == 0:
                jugador.recibir_daño(self.daño)
                self.enfriamiento_golpe = 60 #1 seg
        if self.enfriamiento_golpe > 0:
            self.enfriamiento_golpe -= 1

        # No salga de los bordes
        self.x = max(self.radio, min(ANCHO - self.radio, self.x))
        self.y = max(self.radio, min(ALTO - self.radio, self.y))

    def esta_muerto(self):
        return self.vida <= 0

    def recibir_daño(self, cantidad):
        self.vida -= cantidad

class EnemigoDispara(EnemigoBase):
    def __init__(self, x, y):
        super().__init__(x, y,vida=60,velocidad= 2, radio = 15)
        self.enfriamiento_disparo = 0
        self.balas = []
    
    def actualizar(self, jugador):
        super().actualizar(jugador)
        if self.enfriamiento_disparo <= 0:
            self.disparar(jugador)
            self.enfriamiento_disparo = 90
        else:
            self.enfriamiento_disparo -= 1

        # actualizar  balas
        nuevas_balas = []
        for bala in self.balas:
            bala.actualizar()
            if not bala.fuera_de_pantalla():
                nuevas_balas.append(bala)
        self.balas = nuevas_balas

    def disparar(self,jugador):
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = (dx ** 2 + dy ** 2)**0.5
        if distancia != 0:
            dx /= distancia
            dy /= distancia
        self.balas.append(Bala(self.x, self.y, dx, dy, enemigo=True))

class Minion(EnemigoBase):
    def __init__(self, x, y, usa_balas=False):
        super().__init__(x, y, vida=30, velocidad=1.5,radio=12)
        self.usa_balas = usa_balas
        self.balas = []
        self.tiempo_disparo = 0

    def actualizar(self, jugador):
        super().actualizar(jugador)
        if self.usa_balas:
            self.tiempo_disparo += 1
            if self.tiempo_disparo > 90:
                self.disparar(jugador)
                self.tiempo_disparo = 0
            #actualizar balas
            nuevas = []
            for bala in self.balas:
                bala.actualizar()
                if not bala.fuera_de_pantalla():
                    nuevas.append(bala)
            self.balas = nuevas

    def disparar(self, jugador):
        dx = jugador.x - self.x
        dy = jugador.y - self.y
        distancia = (dx ** 2 + dy ** 2)**0.5
        if distancia != 0:
            dx /= distancia
            dy /= distancia
        self.balas.append(Bala(self.x, self.y, dx * 5, dy * 5, enemigo=True))


class EnemigoInvocador(EnemigoBase):
    def __init__(self, x, y):
        super().__init__(x, y, vida=80, velocidad=1,radio=20)
        self.minions = []
        self.enfriamiento_invocacion = 0

    def actualizar(self, jugador):
        super().actualizar(jugador)
        if self.enfriamiento_invocacion<= 0 and len(self.minions)<3:
            usa_balas = random.choice([True, False])
            nuevo = Minion(self.x + random.randint(-40, 40), self.y + random.randint(-40, 40), usa_balas)
            self.minions.append(nuevo)
            self.enfriamiento_invocacion = 200
        else:
            self.enfriamiento_invocacion -= 1
        #actualizar minions
        vivos = []
        for minion in self.minions:
            minion.actualizar(jugador)
            if not minion.esta_muerto():
                vivos.append(minion)
        self.minions = vivos
