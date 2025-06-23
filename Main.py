import pygame
import random
from config import *
from Jugador import Jugador
from Enemigos import EnemigoBase, EnemigoDispara, EnemigoInvocador
from Jefe import JefeFinal
from Mapa import Mapa, INICIO_JUGADOR, INICIO_ENEMIGO, PICO, PUERTA, TAM_CELDA, ROBO_VIDA

class Game:
    def __init__(self):
        pygame.init()
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Runas del Cubo")
        self.reloj = pygame.time.Clock()
        self.mapa = Mapa()
        self.jugador = None
        self.nivel_actual = 0
        self.enemigos = []
        self.puerta_abierta = False
        self.fuente = pygame.font.Font('assets\sburbits.ttf', 40)
        self.mensaje = ""
        self.mensaje_tiempo = 0
        self.robo_vida_x = None
        self.robo_vida_y = None
        self.estado = "menu"
        self.spike_cooldown = 60  # 1 segundo a 60 FPS
        self.spike_timer = 0
        self.musica_actual = None
        pygame.mixer.music.set_volume(0.3)
        self.cargar_nivel()

    def inicializar_juego(self):
        self.nivel_actual = 0
        self.jugador = None
        self.enemigos = []
        self.puerta_abierta = False
        self.spike_timer = 0
        self.mensaje = ""
        self.mensaje_tiempo = 0
        self.robo_vida_x = None
        self.robo_vida_y = None
        self.cargar_nivel()

    def mostrar_mensaje(self, texto, tiempo_frames=120):
        self.mensaje = texto
        self.mensaje_tiempo = tiempo_frames

    def cargar_nivel(self):
        nivel_data = self.mapa.niveles[self.nivel_actual]
        self.enemigos = []
        self.puerta_abierta = False
        self.robo_vida_x = None
        self.robo_vida_y = None
        
        for f, fila in enumerate(nivel_data):
            for c, celda in enumerate(fila):
                x = c * TAM_CELDA + TAM_CELDA // 2
                y = f * TAM_CELDA + TAM_CELDA // 2
                
                if celda == ROBO_VIDA:
                    self.robo_vida_x = x
                    self.robo_vida_y = y
                    
                if celda == INICIO_JUGADOR:
                    if self.jugador is None:
                        self.jugador = Jugador(x, y)
                    else:
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
        if self.estado == "menu":
            self.reproducir_musica(cancion_menu)       
        elif self.estado == "juego":
            self.reproducir_musica(cancion_nivel)
            teclas = pygame.key.get_pressed()

            
            # Guardar posición previa para colisiones
            x_prev, y_prev = self.jugador.x, self.jugador.y
            
            # Mover jugador
            self.jugador.mover(teclas)
            
            # Verificar colisión con pinchos
            fila, columna = self.mapa.obtener_celda(self.jugador.x, self.jugador.y)
            if 0 <= fila < len(self.mapa.niveles[self.nivel_actual]) and 0 <= columna < len(self.mapa.niveles[self.nivel_actual][0]):
                if self.mapa.niveles[self.nivel_actual][fila][columna] == PICO:
                    # Revertir movimiento y quitar vida
                    self.jugador.x, self.jugador.y = x_prev, y_prev
                    self.jugador.rect.center = (self.jugador.x, self.jugador.y)
                    if self.spike_timer <= 0:
                        self.jugador.recibir_daño(5)
                        self.mostrar_mensaje("¡Pinchos!", 30)
                        self.spike_timer = self.spike_cooldown
                    else:
                        self.spike_timer -= 1
                else:
                    self.spike_timer = 0 

            # Verificar objeto robo vida
            if (self.robo_vida_x is not None and 
                ((self.jugador.x - self.robo_vida_x)**2 + (self.jugador.y - self.robo_vida_y)**2)**0.5 < 30):
                self.jugador.activar_poder()
                self.robo_vida_x = None
                self.robo_vida_y = None
                self.mostrar_mensaje("¡Poder de robo de vida activado!", 60)

            # Actualizar balas y enemigos
            self.jugador.actualizar_balas(self.enemigos)
            self.jugador.actualizar_poder()

            enemigos_activos = []
            for enemigo in self.enemigos:
                enemigo.actualizar(self.jugador)
                if not enemigo.esta_muerto():
                    enemigos_activos.append(enemigo)
            self.enemigos = enemigos_activos

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
                        self.estado = "resultado"
                        if self.estado == "resultado":
                            self.reproducir_musica(cancion_perder)

            if self.jugador.esta_muerto():
                self.estado = "resultado"
                self.reproducir_musica(cancion_perder)

        if self.mensaje_tiempo > 0:
            self.mensaje_tiempo -= 1
        else:
            self.mensaje = ""

    def dibujar_menu(self):
        self.pantalla.fill(NEGRO)
        self.pantalla.blit(imagen_menu, (ANCHO//2 - imagen_menu.get_width()//2, 30))
        instrucciones = self.fuente.render("Presiona ENTER para JUGAR", True, DORADO)
        self.pantalla.blit(instrucciones, (ANCHO//2 - instrucciones.get_width()//2, 500))
        pygame.display.flip()

    def dibujar_resultado(self):
        self.pantalla.fill(NEGRO)
        if self.jugador.esta_muerto():
            self.pantalla.blit(imagen_perder, (ANCHO//2 - imagen_perder.get_width()//2, 30))
            nivel_texto = self.fuente.render(f"Llegaste al nivel {self.nivel_actual + 1}", True, DORADO)
            self.pantalla.blit(nivel_texto, (ANCHO//2 - nivel_texto.get_width()//2, 250))
        else:
            self.pantalla.blit(imagen_ganar, (ANCHO//2 - imagen_ganar.get_width()//2, 30))

        reiniciar_texto = self.fuente.render("Presiona R para reiniciar", True, DORADO)
        self.pantalla.blit(reiniciar_texto, (ANCHO//2 - reiniciar_texto.get_width()//2, 500))
        pygame.display.flip()

    def dibujar(self):
        if self.estado == "menu":
            self.dibujar_menu()
        elif self.estado == "juego":
            self.pantalla.fill(GRIS)
            nivel = self.mapa.niveles[self.nivel_actual]


            for f, fila in enumerate(nivel):
                for c, celda in enumerate(fila):
                    x = c * TAM_CELDA
                    y = f * TAM_CELDA
                    
                    if celda == PICO:
                        pygame.draw.polygon(self.pantalla, ROJO_OSCURO, [(x + TAM_CELDA//2, y),(x, y + TAM_CELDA),(x + TAM_CELDA, y + TAM_CELDA)])
                        pygame.draw.polygon(self.pantalla, NEGRO, [(x + TAM_CELDA//2, y),(x, y + TAM_CELDA),(x + TAM_CELDA, y + TAM_CELDA)], 1)
                        
                    elif celda == PUERTA:
                        color = VERDE if self.puerta_abierta else MARRON
                        pygame.draw.rect(self.pantalla, color, (x + 5, y + 5, TAM_CELDA - 10, TAM_CELDA - 10))

            # Dibujar objeto robo vida
            if self.robo_vida_x is not None and self.robo_vida_y is not None:
                pygame.draw.circle(self.pantalla, ROSADO, (int(self.robo_vida_x), int(self.robo_vida_y)), 15)
                pygame.draw.circle(self.pantalla, BLANCO, (int(self.robo_vida_x), int(self.robo_vida_y)), 10)

            # Dibujar enemigos
            for enemigo in self.enemigos:
                enemigo.dibujar(self.pantalla)
                enemigo.dibujar_balas(self.pantalla)
                enemigo.dibujar_minions(self.pantalla)

            # Dibujar balas del jugador
            for bala in self.jugador.balas:
                bala.dibujar(self.pantalla)

            # Dibujar jugador
            self.jugador.dibujar(self.pantalla)

            # Dibujar mensajes
            if self.mensaje:
                texto = self.fuente.render(self.mensaje, True, BLANCO)
                self.pantalla.blit(texto, (ANCHO//2 - texto.get_width()//2, 550))

            # Dibujar tiempo restante del poder
            if self.jugador.robo_vida_activo:
                segundos = max(0, self.jugador.tiempo_poder // 60)
                texto_poder = self.fuente.render(f"Poder: {segundos}s", True, BLANCO)
                self.pantalla.blit(texto_poder, (10, 10))

            pygame.display.flip()

        elif self.estado == "resultado":
            self.dibujar_resultado()

    def reproducir_musica(self, ruta):
        if self.musica_actual != ruta:
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.play(-1)
            self.musica_actual = ruta

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if self.estado == "menu":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        self.estado = "juego"

            elif self.estado == "resultado":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_r:
                        self.inicializar_juego()
                        self.estado = "juego"

            if self.estado == "juego":
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
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

