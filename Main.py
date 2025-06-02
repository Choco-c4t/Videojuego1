import pygame
import math
import random
from jugador import Jugador
from enemigos import EnemigoBase, EnemigoDispara, EnemigoInvocador
from mapa import niveles, es_pared, obtener_celda
from config import *

class Game:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Dungeon Game")
        self.reloj = pygame.time.Clock()
        self.fuente = pygame.font.SysFont(None, 24)

        self.nivel_actual = 0
        self.jugador = self.crear_jugador()
        self.enemigos = self.crear_enemigos()
        self.corriendo = True

    def crear_jugador(self):
        for f in range(len(niveles[self.nivel_actual])):
            for c in range(len(niveles[self.nivel_actual][f])):
                if niveles[self.nivel_actual][f][c] == 3:
                    return Jugador(c * 40 + 20, f * 40 + 20)
        return Jugador(100, 100)

    def crear_enemigos(self):
        enemigos = []
        for f in range(len(niveles[self.nivel_actual])):
            for c in range(len(niveles[self.nivel_actual][f])):
                if niveles[self.nivel_actual][f][c] == 4:
                    x = c * 40 + 20
                    y = f * 40 + 20
                    tipo = random.choice(["base", "dispara", "invocador"])
                    if tipo == "base":
                        enemigos.append(EnemigoBase(x, y))
                    elif tipo == "dispara":
                        enemigos.append(EnemigoDispara(x, y))
                    elif tipo == "invocador":
                        enemigos.append(EnemigoInvocador(x, y))
        return enemigos

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.corriendo = False
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                self.jugador.disparar()

    def actualizar(self):
        teclas = pygame.key.get_pressed()
        self.jugador.mover(teclas)
        self.jugador.actualizar_balas(self.enemigos)
        for enemigo in self.enemigos:
            enemigo.actualizar(self.jugador)
        self.enemigos = [e for e in self.enemigos if not e.esta_muerto()]

        fila, col = obtener_celda(self.jugador.x, self.jugador.y)
        if niveles[self.nivel_actual][fila][col] == 2:
            self.jugador.recibir_daño(1)

    def dibujar_mapa(self):
        for f in range(len(niveles[self.nivel_actual])):
            for c in range(len(niveles[self.nivel_actual][f])):
                celda = niveles[self.nivel_actual][f][c]
                x = c * 40
                y = f * 40
                if celda == 1:
                    pygame.draw.rect(self.pantalla, GRIS, (x, y, 40, 40))
                elif celda == 2:
                    pygame.draw.rect(self.pantalla, ROJO, (x+10, y+10, 20, 20))

    def dibujar_barra_vida(self, entidad):
        porcentaje = entidad.vida / entidad.vida_maxima
        largo = 40
        alto = 5
        x = int(entidad.x - largo // 2)
        y = int(entidad.y - entidad.radio - 10)
        pygame.draw.rect(self.pantalla, ROJO, (x, y, largo, alto))
        pygame.draw.rect(self.pantalla, VERDE, (x, y, largo * porcentaje, alto))

    def dibujar(self):
        self.pantalla.fill(NEGRO)
        self.dibujar_mapa()
    

    def run(self):
        while self.corriendo:
            self.reloj.tick(FPS)
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()

            if self.jugador.esta_muerto():
                print("Fin del juego")
                self.corriendo = False

        pygame.quit()

if __name__ == "__main__":
    juego = Game()
    juego.run()

