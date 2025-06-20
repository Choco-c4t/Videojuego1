import pygame
import random
from config import *
from Jugador import Jugador
from Enemigos import EnemigoBase, EnemigoDispara, EnemigoInvocador
from Jefe import JefeFinal
from Mapa import Mapa, INICIO_JUGADOR, INICIO_ENEMIGO, PICO, PUERTA, TAM_CELDA

class Game:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Crypta Eterna")
        self.reloj = pygame.time.Clock()
        self.mapa = Mapa()
        self.jugador = None
        self.nivel_actual = 0
        self.enemigos = []
        self.puerta_abierta = False
        self.spike_damage_cooldown = 30
        self.spike_damage_timer = 0
        self.fuente = pygame.font.SysFont(None, 30)
        self.mensaje = ""
        self.mensaje_tiempo = 0
        self.robo_vida_activo = False
        self.cargar_nivel()

    def mostrar_mensaje(self, texto, tiempo_frames=120):
        self.mensaje = texto
        self.mensaje_tiempo = tiempo_frames

    def cargar_nivel(self):
        nivel_data = self.mapa.niveles[self.nivel_actual]
        self.enemigos = []
        self.puerta_abierta = False
        for f, fila in enumerate(nivel_data):
            for c, celda in enumerate(fila):
                x = c * TAM_CELDA + TAM_CELDA // 2
                y = f * TAM_CELDA + TAM_CELDA // 2  
                if celda == INICIO_JUGADOR:
                    if self.jugador is None: # crear jugador
                        self.jugador = Jugador(x, y)
                    else: #si existe, cambiar pos
                        self.jugador.x = x
                        self.jugador.y = y
                        self.jugador.rect.center = (x, y)
                    
                elif celda == INICIO_ENEMIGO:
                    if (self.nivel_actual + 1) % 5 == 0:
                        self.enemigos.append(JefeFinal(x, y))
                    else:
                        tipo_enemigo = random.choice(['base', 'dispara', 'invocador'])
                        if tipo_enemigo == 'base':
                            self.enemigos.append(EnemigoBase(x, y))
                        elif tipo_enemigo == 'dispara':
                            self.enemigos.append(EnemigoDispara(x, y))
                        else:
                            self.enemigos.append(EnemigoInvocador(x, y))

    def actualizar(self):
        teclas = pygame.key.get_pressed()
        self.jugador.mover(teclas)
        self.jugador.actualizar_balas(self.enemigos)

        enemigos_activos = []
        for enemigo in self.enemigos:
            enemigo.actualizar(self.jugador)
            if not enemigo.esta_muerto():
                enemigos_activos.append(enemigo)
        self.enemigos = enemigos_activos

        self.jugador.robar_vida(self.enemigos)

        if not self.enemigos and not self.puerta_abierta:
            self.puerta_abierta = True
            self.mostrar_mensaje("¡Puerta abierta!")

        fila, columna = self.mapa.obtener_celda(int(self.jugador.x), int(self.jugador.y))
        nivel = self.mapa.niveles[self.nivel_actual]
        
        if 0 <= fila < len(nivel) and 0 <= columna < len(nivel[0]):
            tile = nivel[fila][columna]
            if tile == PUERTA and self.puerta_abierta:
                self.nivel_actual += 1
                if self.nivel_actual < len(self.mapa.niveles):
                    self.cargar_nivel()
                    self.mostrar_mensaje(f"Nivel {self.nivel_actual + 1} cargado")
                else:
                    self.mostrar_mensaje("¡Has ganado el juego!", tiempo_frames=180)
                    pygame.time.delay(3000)
                    pygame.quit()
                    exit()

        self.spike_damage_timer += 1
        if self.spike_damage_timer >= self.spike_damage_cooldown:
            self.spike_damage_timer = 0
            fila, columna = self.mapa.obtener_celda(int(self.jugador.x), int(self.jugador.y))
            if 0 <= fila < len(self.mapa.niveles[self.nivel_actual]) and 0 <= columna < len(self.mapa.niveles[self.nivel_actual][0]):
                tile = self.mapa.niveles[self.nivel_actual][fila][columna]
                if tile == PICO:
                    self.jugador.recibir_daño(5)
                    self.mostrar_mensaje(f"¡Daño por pinchos! Vida: {self.jugador.vida}", tiempo_frames=60)

        # Evitar que el jugador atraviese puerta cerrada
        if 0 <= fila < len(self.mapa.niveles[self.nivel_actual]) and 0 <= columna < len(self.mapa.niveles[self.nivel_actual][0]):
            tile = self.mapa.niveles[self.nivel_actual][fila][columna]
            if tile == PUERTA and not self.puerta_abierta:
                if teclas[pygame.K_w]: self.jugador.y += self.jugador.velocidad
                if teclas[pygame.K_s]: self.jugador.y -= self.jugador.velocidad
                if teclas[pygame.K_a]: self.jugador.x += self.jugador.velocidad
                if teclas[pygame.K_d]: self.jugador.x -= self.jugador.velocidad

        if self.jugador.esta_muerto():
            self.mostrar_mensaje("¡Has perdido!", tiempo_frames=180)
            self.dibujar()
            pygame.time.delay(3000)
            pygame.quit()
            exit()

        if self.mensaje_tiempo > 0:
            self.mensaje_tiempo -= 1
        else:
            self.mensaje = ""

    def dibujar(self):
        self.pantalla.fill(GRIS)
        nivel = self.mapa.niveles[self.nivel_actual]
        
        for f, fila in enumerate(nivel):
            for c, celda in enumerate(fila):
                x = c * TAM_CELDA
                y = f * TAM_CELDA
                
                if celda == PICO:
                    punto1 = (x + TAM_CELDA // 2, y + 5)
                    punto2 = (x + 5, y + TAM_CELDA - 5)
                    punto3 = (x + TAM_CELDA - 5, y + TAM_CELDA - 5)
                    pygame.draw.polygon(self.pantalla, ROJO, [punto1, punto2, punto3])
                elif celda == PUERTA:
                    color = VERDE if self.puerta_abierta else MARRON
                    rect = pygame.Rect(x + 5, y + 5, TAM_CELDA - 10, TAM_CELDA - 10)
                    pygame.draw.rect(self.pantalla, color, rect)
                    if not self.puerta_abierta:
                        pygame.draw.line(self.pantalla, NEGRO, (x + 15, y + 20), (x + 25, y + 20), 3)

        for enemigo in self.enemigos:
            enemigo.dibujar(self.pantalla)
            enemigo.dibujar_balas(self.pantalla)
            enemigo.dibujar_minions(self.pantalla)

        for bala in self.jugador.balas:
            bala.dibujar(self.pantalla)

        self.jugador.dibujar(self.pantalla)

        if self.mensaje:
            texto_superficie = self.fuente.render(self.mensaje, True, (255, 255, 255))
            rect_texto = texto_superficie.get_rect(center=(ANCHO // 2, 30))
            self.pantalla.blit(texto_superficie, rect_texto)

        pygame.display.flip()

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.jugador.disparar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r: 
                    self.jugador.activar_robo_vida()
                elif evento.key == pygame.K_SPACE:
                    self.jugador.disparar() 

    def ejecutar(self):
        while True:
            self.reloj.tick(FPS)
            self.manejar_eventos()
            self.actualizar()
            self.dibujar()

if __name__ == "__main__":
    juego = Game()
    juego.ejecutar()


