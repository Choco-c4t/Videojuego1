TAM_CELDA = 40
FILAS = 15
COLUMNAS = 20

VACIO = 0
PARED = 1
PICO = 2
INICIO_JUGADOR = 3
INICIO_ENEMIGO = 4

#solo nivel 1
niveles = [
    [ [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
      [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,1],
      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]
]

def obtener_celda(x, y):
    fila = y // TAM_CELDA
    columna = x // TAM_CELDA
    return fila, columna

def es_pared(fila, columna, nivel_actual):
    if 0 <= nivel_actual <len(niveles):
        nivel = niveles[nivel_actual]
        if 0 <= fila < len(nivel) and 0 <= columna < len(nivel[fila]):
            return nivel[fila][columa]== PARED
    return True 

#git cloe
#git add
#git push logearse
