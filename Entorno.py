import pygame
import Colores

# Logitud vertical en pixeles
ANCHO_VENTANA = 700
# Longitud horizontal en pixeles
LARGO_VENTANA = 700

# Inicializamo todos los requerimientos necesarios para emplear pygames
pygame.init()

# Creamos nuestra ventana
Ventana = pygame.display.set_mode((LARGO_VENTANA,ANCHO_VENTANA))

# Titulo a la ventana
pygame.display.set_caption('Mundo de la aspiadora')

class Casilla:
    def __init__(self, fila, columna, total_filas, total_columnas, ancho, largo):
        self.Fila = fila
        self.Columna = columna
        self.Ancho = ancho
        self.Largo = largo
        self.Total_filas = total_filas
        self.Total_columnas = total_columnas
        self.x = fila*ancho
        self.y = columna*largo
        self.Color = Colores.LIBRE_COLOR
        self.Vecinos = []
    
    def obtener_posicion(self):
        return self.Fila, self.Columna

    def actualizar_vecinos(self, casilla):
        self.Vecinos = []
        
        # Checamos la casilla posterior de la actual
        if self.Columna < self.Total_columnas - 1 and not casilla[self.Fila][self.Columna + 1].es_obstaculo():
            self.Vecinos.append(casilla[self.Fila][self.Columna + 1])
        
        # Checamos la casilla anterior de la actual
        if self.Columna > 0 and not casilla[self.Fila][self.Columna - 1].es_obstaculo():
            self.Vecinos.append(casilla[self.Fila][self.Columna - 1])
        
        # Checamos la casilla debajo de la actual
        if self.Fila < self.Total_filas - 1 and not casilla[self.Fila + 1][self.Columna].es_obstaculo():
            self.Vecinos.append(casilla[self.Fila + 1][self.Columna])
        
        # Checamos la casilla arriba de la actual
        if self.Fila > 0 and not casilla[self.Fila - 1][self.Columna].es_obstaculo():
            self.Vecinos.append(casilla[self.Fila - 1][self.Columna])

    def __lt__(self, otro):
        return False

    def es_inicio(self):
        return self.Color == Colores.ASPIRADORA_COLOR

    def es_suciedad(self):
        return self.Color == Colores.SUCIEDAD_COLOR

    def es_obstaculo(self):
        return self.Color == Colores.OBSTACULO_COLOR
        
    def es_explorado(self):
        return self.Color == Colores.EXPLORADO_COLOR
    
    def es_noexplorado(self):
        return self.Color == Colores.NOEXPLORADO_COLOR
    
    def establecer_aspiradora(self):
        self.Color = []
        return self.Color.extend(Colores.ASPIRADORA_COLOR)

    def establecer_libre(self):
        self.Color = []
        return self.Color.extend(Colores.LIBRE_COLOR)
    
    def establecer_obstaculo(self):
        self.Color = []
        return self.Color.extend(Colores.OBSTACULO_COLOR)
    
    def establecer_suciedad(self):
        self.Color = []
        return self.Color.extend(Colores.SUCIEDAD_COLOR)
    
    def establecer_camino(self):
        self.Color = []
        return self.Color.extend(Colores.CAMINO_COLOR)
    
    def establecer_explorado(self):
        self.Color = []
        return self.Color.extend(Colores.EXPLORADO_COLOR)
    
    def establecer_noexplorado(self):
        self.Color = []
        return self.Color.extend(Colores.NOEXPLORADO_COLOR)
    
    def dibujar(self, Ventana):
        # Dibujamos un rectangulo pequeño (casilla) en las coordenada indicadas
        pygame.draw.rect(Ventana, self.Color, (self.x, self.y, self.Largo, self.Ancho))

def establecer_entorno(filas, columnas, anchura, longitud):
    entorno = []
    anchura_casilla = anchura//filas                    # Division entera
    longitud_casilla = longitud//columnas               # Division entera
    
    # Construimos nuestro entorno
    for i in range(filas):
        entorno.append([])
        for j in range(columnas):
            casilla = Casilla(i, j, filas, columnas, anchura_casilla, longitud_casilla)
            entorno[i].append(casilla)
    
    return entorno

def dibujar_entorno(Ventana, filas, columnas, anchura, longitud):
    anchura_casillas = anchura // filas
    longitud_casillas = longitud // columnas
    
    # Lineas horizontales
    for i in range(filas):
        pygame.draw.line(Ventana, Colores.GRIS, [0, i * anchura_casillas], [longitud, i * anchura_casillas])
        # Lineas verticales
        for j in range(columnas):
            pygame.draw.line(Ventana, Colores.GRIS, [j * longitud_casillas, 0], [j * longitud_casillas, anchura])

def dibujar(Ventana, entorno, filas, columnas, anchura, longitud):
    Ventana.fill(Colores.WHITE)             # Color default de todo el entorno: blanco
    for fila in entorno:
        for casilla in fila:
            casilla.dibujar(Ventana)

    dibujar_entorno(Ventana, filas, columnas, anchura, longitud)
    
    pygame.display.update()
    return 0

# Obtenemos la posicion del mouse al hacer click
def get_clicked_pos(posicion, filas, columnas, anchura, longitud):
    anchura_casillas = anchura // filas
    longitud_casillas = longitud // columnas
    x, y = posicion
    fila = x // anchura_casillas
    columna = y // longitud_casillas
    return fila, columna

def recrear_camino(procedencia, actual, dibujar):
    while actual in procedencia:
        actual = procedencia[actual]
        actual.establecer_camino()
        dibujar
