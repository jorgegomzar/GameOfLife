import pygame
import numpy as np
import time
import matplotlib.pyplot as plt

def calculoVecinos(x, y):
    '''
        Devuelve el número de vecinos con vida de una celda (x,y)
    '''
    return  gameState[(x-1) % nxC,(y-1) % nyC] + \
            gameState[x % nxC,(y-1) % nyC] + \
            gameState[(x+1) % nxC,(y-1) % nyC] + \
            gameState[(x-1) % nxC,y % nyC] + \
            gameState[(x+1) % nxC,y % nyC] + \
            gameState[(x-1) % nxC,(y+1) % nyC] + \
            gameState[x % nxC,(y+1) % nyC] + \
            gameState[(x+1) % nxC,(y+1) % nyC]

def calculoVivas():
    '''
        Devuelve el número de celdas vivas
    '''
    vivas = 0
    for y in range(0, nyC):
        for x in range(0, nxC):
            if gameState[x, y] == 1:
                vivas = vivas + 1
    print('################################')
    print('Vivas: ', vivas)
    print('Muertas: ', (nxC * nyC) - vivas)
    return vivas

# MENU
print('{:#<50}'.format(''))
print('# ¡Bienvenido al Juego de la Vida! #'.center(50))
print('{:#<50}'.format(''))
print('CONTROLES'.center(50))
print('# Cualquier tecla: Pausa/Reanuda el juego')
print('# Click izquierdo: Revive una celda')
print('# Click derecho: Mata una celda')
print('# Click rueda del ratón: Finaliza el juego')
print('{:#<50}'.format(''))
print('No se tendrán en cuenta las estadísticas mientras el juego esté pausado')
input('Pulsa cualquier tecla para comenzar...')


# Configuración inicial
pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)

nxC, nyC = 50, 50

dimCW = width / nxC
dimCH = height / nyC


# FLAGS para el control de flujo del juego
gameState = np.zeros((nxC, nyC)) # 1 = vida, 0 = no vida
pauseExect = True   # True = juego pausado, False = juego en ejecución
stop = False    # True = Game Over, False = el juego continua
historialVida = []

# El mojo
while True:

    # Se detiene el juego si el jugador lo desea
    if stop:
        break

    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)

    # Solo se tienen en cuenta las estadísticas cuando el juego no está pausado
    if not pauseExect:
        historialVida.append(calculoVivas())

    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.KEYDOWN:    # Debería coger solo KEYDOWN, pero vale cualquiera (?)
            pauseExect = not pauseExect     # Cada vez que se pulsa una tecla el juego cambia de estado (pause/resume)
        
        mouseClick = pygame.mouse.get_pressed()

        if mouseClick[1] == 1:      # Si se pulsa la rueda del ratón, se para el juego en la siguiente iteración
            stop = True
        elif sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]    # Click izqdo crea vida, Click dcho mata

    for y in range(0, nyC):
        for x in range(0, nxC):
            if not pauseExect:      # Solo se actualiza el juego cuando no está pausado (duh)
                n_neigh = calculoVecinos(x,y)

                # Rule #1 : Una célula muerta con exactamente 3 vecinas vivas, "revive"
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1
                # Rule #2 : Una célula con menos de 2 o más de 3 vecinas vivas, "muere"
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

            # Forma de la celda
            poly = [
                (x * dimCW, y * dimCH),
                ((x+1) * dimCW, y * dimCH),
                ((x+1) * dimCW, (y+1) * dimCH),
                (x * dimCW, (y+1) * dimCH),
            ]

            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Se actualiza la pantalla
    gameState = np.copy(newGameState)
    pygame.display.flip()


# Al finalizar el juego muestra una gráfica con la población por cada iteración
plt.plot(historialVida)
plt.ylabel('Población')
plt.xlabel('Generación')
plt.show()