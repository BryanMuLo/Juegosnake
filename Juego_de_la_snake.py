# Juego de snake

import pygame, sys

############ DEFINICIONES ##############
pygame.init()

# Asignacion de colores para el juego
Verde = (173, 204, 96)
Verde_oscuro = (43, 51, 24)

# Para crear el canvas/display de 750x750
pantalla = pygame.display.set_mode((750,750))

# Titulo de la pantalla o ventana
pygame.display.set_caption("Retro Snake")

# Reloj de objeto
reloj = pygame.time.Clock()

########################################
############ GAME LOOP #################

# Obtiene los eventos que pasan en pygame como lista
while True:
    for event in pygame.event.get():
        # Quit event o evento de salir para no romper el loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    # Definiendo el color que tendra la pantalla de fondo
    pantalla.fill(Verde)
    # Toma todo los cambios hechos en los objetos del juego y dibuja la imagen de ellos
    pygame.display.update()
    # Hace que nuestro game loop hace 60 ticks por segundo, necesario para limitar la velocidad
    reloj.tick(60)
    
#######################################