# mapa.py

# Constantes para el tamaño del mapa
TAM_CELDA = 40
FILAS = 15
COLUMNAS = 20

# Códigos para las celdas
VACIO = 0
PARED = 1
PICO = 2
INICIO_JUGADOR = 3
INICIO_ENEMIGO = 4

# Ejemplo de nivel
niveles = [
    [
        [1]*20,  # Fila 0 (pared)
        [1] + [0]*18 + [1],  # Fila 1
        [1] + [0]*18 + [1],  # Fila 2
        [1] + [0, 2] + [0]*15 + [4, 0] + [1],  # Fila 3 con pico y enemigo
        [1] + [0]*18 + [1],
        [1] + [0]*18 + [1],
        [1] + [0]*8 + [2] + [0]*9 + [1],  # Pico en el medio
        [1] + [0]*8 + [3] + [0]*9 + [1],  # Jugador en el centro
        [1] + [0]*18 + [1],
        [1] + [0]*18 + [1],
        [1] + [4] + [0]*16 + [2] + [1],  # Enemigo y pico
        [1] + [0]*18 + [1],
        [1] + [0]*18 + [1],
        [1] + [0]*18 + [1],
        [1]*20  # Fila 14 (pared)
    ],
    # Puedes añadir más niveles aquí...
]

def obtener_celda(x, y):
    """Convierte coordenadas en píxeles a índices de la matriz."""
    fila = y // TAM_CELDA
    columna = x // TAM_CELDA
    return fila, columna

def es_pared(fila, columna, nivel_actual):
    """Devuelve True si la celda es una pared."""
    try:
        return niveles[nivel_actual][fila][columna] == PARED
    except IndexError:
        return True  # Tratar fuera de rango como pared

def obtener_posiciones(codigo, nivel_actual):
   posiciones (x, y) donde se encuentra un código específico en el nivel."""
    posiciones = []
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            if niveles[nivel_actual][fila][columna] == codigo:
                x = columna * TAM_CELDA + TAM_CELDA // 2
                y = fila * TAM_CELDA + TAM_CELDA // 2
                posiciones.append((x, y))
    return posiciones
