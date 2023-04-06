from timeit import default_timer

import pygame
import math
import Colores
import Entorno
import A_estrella

# Dimension del entorno en casillas (cuadrado)
MEDIDA = 50

# Cantidad casillas que conforman la anchura de la ventana
#FILAS = 30
# Cantidad casillas que conforman la longitud de la ventana
#COLUMNAS = 30

def main(Ventana, filas, columnas, anchura, longitud): 
    entorno = Entorno.establecer_entorno(filas, columnas, anchura, longitud)

    inicio = None
    fin = None

    run = True
    started = False
    # Hacemos que la ventana semantenga emergente
    while run:
        Entorno.dibujar(Ventana, entorno, filas, columnas, anchura, longitud)
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  #Cerrar el programa si el usuario lo indica
                run = False
            
            if started:
                continue

            # En caso de presionar el boton izquierdo del mouse (el que se usa para hacer clic)
            if pygame.mouse.get_pressed()[0]:
                posicion = pygame.mouse.get_pos()

                fila, columna = Entorno.get_clicked_pos(posicion, filas, columnas, anchura, longitud)
                espacio = entorno[fila][columna]

                if not inicio and espacio != fin:
                    inicio = espacio
                    inicio.establecer_aspiradora()          # Casilla de inicio
                
                elif not fin and espacio != inicio:
                    fin = espacio
                    fin.establecer_suciedad()               # Casilla de destino
                
                elif espacio != inicio and espacio != fin:
                    espacio.establecer_obstaculo()
            
            # En caso de presionar el boton derecho del mouse
            elif pygame.mouse.get_pressed()[2]:
                posicion = pygame.mouse.get_pos()

                fila, columna = Entorno.get_clicked_pos(posicion, filas, columnas, anchura, longitud)
                espacio = entorno[fila][columna]
                espacio.establecer_libre()

                if espacio == inicio:
                    inicio = None
                
                elif espacio == fin:
                    fin = None
                
                # Si se presiona la tecla de flecha hacia abajo
                if event.type == pygame.KEYDOWN:
                    # Si se preciona la tecla espaciadora
                    if inicio and fin != None:
                        for fila in entorno:
                            for espacio in fila:
                                espacio.actualizar_vecinos(entorno)
                        
                        start = default_timer() #<-------------------------------Borrame

                        # Despues de que todas las casillas obtengan sus vecinos proximos aplicamos 
                        # el algoritmo a*
                        A_estrella.algoritmo(
                            # Pasamos una funcion anonimos en los parametros de otra para que tenga 
                            # un efecto similar a la recursividad al dibujarse las casillas
                            # función que luego se podra emplear como si se tratase del propio
                            # archivo
                            lambda: Entorno.dibujar(Ventana, entorno, filas, columnas, anchura, longitud),
                            entorno,
                            inicio,
                            fin
                        )

                                                
                        end = default_timer()  #<-------------------------------Borrame
                        print("tiempo de ejecucion = ",end - start)  #<------------------Borrame
                    
                    if event.key == pygame.K_c:
                        start = None
                        end = None
                        grid = Entorno.establecer_entorno(filas, columnas, anchura, longitud)
                    
    pygame.quit()

main(Entorno.Ventana, MEDIDA, MEDIDA, Entorno.ANCHO_VENTANA, Entorno.LARGO_VENTANA)