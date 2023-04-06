from queue import PriorityQueue
import pygame
import Entorno

COSTE_MOVIMIENTO = 1

def heuristica(punto_inicial, punto_final):
    x1,y1 = punto_inicial

    x2,y2 = punto_final
    return abs(x2-x1)+abs(y2-y1)                        # Distancia en forma de L

def algoritmo(dibujar, entorno, inicio, fin):
    cont = 0
    lista_abierta = PriorityQueue()
    lista_abierta.put((0, cont, inicio))
    procedencia = {}

    # Tabla (columna-fila-lista-diccionario) de valores f, g y h para cada nodo (casilla)
    # sin obstaculos
    #|   Nodo   |   f   |   g   |   h   |
    #|----------|-------|-------|-------|
    #|  [0,1]   |   0   |   0   |   0   |
    #|  [0,2]   |  inf  |  inf  |  inf  |
    #|  [0,3]   |  inf  |  inf  |  inf  |
    #|  .....   |  ...  |  ...  |  ...  |

    # g
    # Originalmente, se intuye que todas las casillas son inalcanzable, 
    # por ello se procede a almacenar en el diccionario cada una de las casillas con su respectivo
    # peso inicial de un numero muy grande, de tal forma que realmente es todas las casillas
    # se guardan (sirviendo como llave) aqui
    coste_acumulado = {
        casilla: float("inf") for fila in entorno for casilla in fila
    }
    # Coste acumulado inicial correspondiente a la casilla donde está la aspiradora
    coste_acumulado[inicio] = 0
    
    # f
    coste_f = {
        casilla: float("inf") for fila in entorno for casilla in fila
    }
    # Coste inicial de la casilla donde se encuentra la aspiradora
    coste_f[inicio] = heuristica(inicio.obtener_posicion(), fin.obtener_posicion())

    # Debemos de crear un hash para cada una de las casillas y así poder diferenciar los diferentes 
    # nodos entre si, pues muchos tendran la misma priorida, además de no poder saber que nodos 
    # estan en la lista abierta y cuales si, por ello debemos de darle seguimiento
    lista_abierta_hash = {inicio}

    # Salida de bucle en caso de que no se pueda alcanzar una meta
    while not lista_abierta.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:       #Cerrar el programa si el usuario lo indica
                pygame.quit()

        actual = lista_abierta.get()[2]
        lista_abierta_hash.remove(actual)

        if actual == fin:
            Entorno.recrear_camino(procedencia, fin, dibujar)
            fin.establecer_explorado()
            return True
        
        for vecino in actual.Vecinos:
            aux_g = coste_acumulado[actual] + COSTE_MOVIMIENTO

            if aux_g < coste_acumulado[vecino]:
                procedencia[vecino] = actual
                coste_acumulado[vecino] = aux_g
                coste_f[vecino] = aux_g + heuristica(vecino.obtener_posicion(), fin.obtener_posicion())

                if vecino not in lista_abierta_hash:
                    cont += 1
                    lista_abierta.put((coste_f[vecino], cont, vecino))
                    lista_abierta_hash.add(vecino)
                    vecino.establecer_noexplorado()

        dibujar()

        if actual != inicio:
            actual.establecer_explorado()
            
    return False