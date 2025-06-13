TAM_CELDA = 40
VACIO = 0
PARED = 1
PICO = 2
INICIO_JUGADOR = 3
INICIO_ENEMIGO = 4
PUERTA = 5 

class Mapa:
    def __init__(self):
        self.niveles = self.crear_niveles()

    def matriz_vacia(self, filas, columnas, valor=VACIO):
        matriz = []
        for fila in range(filas):
            nueva_fila = []
            for columna in range(columnas):
                nueva_fila.append(valor)
            matriz.append(nueva_fila)
        return matriz

    def crear_niveles(self):
        niveles = []

        for i in range(15):
            if (i + 1) % 5 == 0:
                nivel = self.crear_nivel_jefe(i)
            else:
                nivel = self.crear_nivel_normal(i)
            niveles.append(nivel)

        return niveles
    
    def crear_nivel_normal(self, i):
        filas = 15
        columnas = 20
        nivel = self.matriz_vacia(filas, columnas)

        # Bordes
        for f in range(filas):
            for c in range(columnas):
                if f == 0 or f == filas - 1 or c == 0 or c == columnas - 1:
                    nivel[f][c] = PARED

        # Inicio del jugador
        nivel[filas - 2][2 + (i % 4)] = INICIO_JUGADOR

        # Puerta en cima derecha
        nivel[0][columnas // 2] = PUERTA

        for e in range(2 + i % 3):
            f = 3 + e
            c = 5 + (i + e) % 10
            if f < filas and c < columnas:
                nivel[f][c] = INICIO_ENEMIGO

        for p in range(3 + i):
            f = (5 + (p * 2)) % (filas - 2)
            c = (p * 3 + i) % (columnas - 2) + 1
            if f < filas and c < columnas:
                if nivel[f][c] == VACIO:
                    nivel[f][c] = PICO

        return nivel

    def crear_nivel_jefe(self, i):
        filas = 20
        columnas = 25
        nivel = self.matriz_vacia(filas, columnas)

        for f in range(filas):
            for c in range(columnas):
                if f == 0 or f == filas - 1 or c == 0 or c == columnas - 1:
                    nivel[f][c] = PARED

        nivel[filas - 2][2] = INICIO_JUGADOR

        nivel[filas // 2][columnas // 2] = INICIO_ENEMIGO

        nivel[0][columnas // 2] = PUERTA

        for p in range(10 + i):
            f = (p * 2 + i) % (filas - 2)
            c = (p * 3 + i) % (columnas - 2)
            if nivel[f][c] == VACIO:
                nivel[f][c] = PICO

        return nivel

    def obtener_celda(self, x, y):
        fila = y // TAM_CELDA
        columna = x // TAM_CELDA
        return fila, columna




