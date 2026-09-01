# Juego de snake
import pygame, sys, random
# Importando vector2 para poderlo usar
from pygame.math import Vector2

############ DEFINICIONES ##############
pygame.init()

# Asignacion de colores para el juego
Verde = (173, 204, 96)
Verde_oscuro = (43, 51, 24)

# Asignacion del tamaño de la celda
celda_size = 30
# Asignacion de la cantidad de celdas
number_of_celdas = 25

# Creacion de clase para el objeto que sera la comida
class Food:
    # Definicion del metodo del objeto para editar su posicion
    def __init__(self):
        # Vector2 class que ofrece pygame para ubicar la celda con comida, ahora usamos la posicin random que generamos en x y y
        self.position = self.generate_random_pos()   # anterior Vector2(5,6)
        
    def draw(self):
        # el rect es usado para dibujar rectangulos invisibles para posicionamiento de colicion/deteccion y dibujaro bjetos
        # Usamos la posicion de vector2 multiplicado por el size de la celda y luego solo el size y size ya que no tenemos w o h en vector2 (x, y , w, h)
        comida_rect = pygame.Rect(self.position.x * celda_size, self.position.y * celda_size, celda_size, celda_size)
        # Dibujando el rectangulo usando surface, color y rect (donde se vera, que color y que size y posicion tendra)
  #     pygame.draw.rect(pantalla, Verde_oscuro, comida_rect)  anterior metodo que solo dibujaba un rectangulo
        # nuevo metodo que dibujara la imagen de comida que asignamos
        pantalla.blit(comida_surface, comida_rect)
        
    # Dejaremos de hacer que la comida siempre aparezca en la misma posicion para que salga random
    def generate_random_pos(self):
        # toma un numero random en x y en y
        x = random.randint(0, number_of_celdas -1)
        y = random.randint(0, number_of_celdas - 1)
        # hacemos que la posicion tome las coordenadas anteriores
        posicion = Vector2(x, y)
        return posicion
        

# Para crear el canvas/display de 750x750, pasamos de poner el numero fijo a asignar el tamaño dependidendod de el size de las celdas y la cantidad
pantalla = pygame.display.set_mode((celda_size*number_of_celdas,celda_size*number_of_celdas))#750,750 anteriormente

# Titulo de la pantalla o ventana
pygame.display.set_caption("Retro Snake")

# Reloj de objeto
reloj = pygame.time.Clock()

# Asignando la clase Food a la variable comida
comida = Food()
comida_surface = pygame.image.load("Graficos/comida.png")
# como la imgane es usada es de 500x500 toca transformarla a la escala de la celda 30x30
comida_surface = pygame.transform.scale(comida_surface, (celda_size, celda_size))

########################################
############ GAME LOOP #################

# Obtiene los eventos que pasan en pygame como lista
while True:
    for event in pygame.event.get():
        # Quit event o evento de salir para no romper el loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
 # Dibujado
    # Definiendo el color que tendra la pantalla de fondo
    pantalla.fill(Verde)
    # Dibujar todo lo que representa la comida (class Food)
    comida.draw()
    
    
    
    # Toma todo los cambios hechos en los objetos del juego y dibuja la imagen de ellos
    pygame.display.update()
    # Hace que nuestro game loop hace 60 ticks por segundo, necesario para limitar la velocidad
    reloj.tick(60)
    
#######################################