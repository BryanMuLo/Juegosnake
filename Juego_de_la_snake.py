# Juego de snake
import pygame, sys, random
# Importando vector2 para poderlo usar
from pygame.math import Vector2

############ DEFINICIONES ##############
pygame.init()

# Fondo de titulo y score
title_font = pygame.font.Font(None, 60)
score_font = pygame.font.Font(None, 40)

# Asignacion de colores para el juego
#Verde = (173, 204, 96)
Verde = (118, 216, 174)
Verde_oscuro = (43, 51, 24)

# Asignacion del tamaño de la celda
celda_size = 30
# Asignacion de la cantidad de celdas
number_of_celdas = 25

OFFSET = 75

# Creacion de clase para el objeto que sera la comida
class Food:
    # Definicion del metodo del objeto para editar su posicion
    def __init__(self, snake_body):
        # Vector2 class que ofrece pygame para ubicar la celda con comida, ahora usamos la posicin random que generamos en x y y
        self.position = self.generate_random_pos(snake_body)   # anterior Vector2(5,6)
        
    def draw(self):
        # el rect es usado para dibujar rectangulos invisibles para posicionamiento de colicion/deteccion y dibujaro bjetos
        # Usamos la posicion de vector2 multiplicado por el size de la celda y luego solo el size y size ya que no tenemos w o h en vector2 (x, y , w, h)
        comida_rect = pygame.Rect(OFFSET + self.position.x * celda_size, OFFSET + self.position.y * celda_size, celda_size, celda_size)
        # Dibujando el rectangulo usando surface, color y rect (donde se vera, que color y que size y posicion tendra)
  #     pygame.draw.rect(pantalla, Verde_oscuro, comida_rect)  anterior metodo que solo dibujaba un rectangulo
        # nuevo metodo que dibujara la imagen de comida que asignamos
        pantalla.blit(comida_surface, comida_rect)
        
        # Definimos especificamente para la posicion random de la celula para no copiar y copiar el codigo y solo llamarlo
    def generate_random_cell(self):
        # toma un numero random en x y en y
        x = random.randint(0, number_of_celdas -1)
        y = random.randint(0, number_of_celdas - 1)
        # hacemos que la posicion tome las coordenadas de arriba
        return Vector2(x, y)
        
    # Dejaremos de hacer que la comida siempre aparezca en la misma posicion para que salga random
    def generate_random_pos(self, snake_body):
        # hacemos que la posicion tome las coordenadas que regresa el metodo random cell
        posicion = self.generate_random_cell()
        # Para hacer que si la comida esta en el acuerpo de la serpiente se genere en otro lugar
        while posicion in snake_body:
            # hacemos que la posicion tome las coordenadas de arriba
            posicion = self.generate_random_cell()
        return posicion
    
# Creacion de clase para el objeto que sera la serpiente
class Snake:
    # Coordenadas del cuerpo de la serpiente
    def __init__(self):
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        # Para moverla a la derecha a la serpiente al iniciar el juego
        self.direction = Vector2(1, 0)
        # Definimos por defecto que la serpiente no crece
        self.add_segment = False
    
    # Dibujo del cuerpo de la serpiente
    def draw(self):
        for segmento in self.body:
            segmento_rect = (OFFSET + segmento.x * celda_size, OFFSET + segmento.y * celda_size, celda_size, celda_size)
            # El cero representa si hay hueco, pero con cero lo quitamos y el siete representa cuan redondeada esta la esquina
            pygame.draw.rect(pantalla, Verde_oscuro, segmento_rect, 0, 7)
            
    # Para actualizar la posicion de la serpiente (aqui para moverla siempre se genera una celda mas, pero tambien se borra una, por lo que al hacer que si come no se borre crece uno)
    def update(self):
        # Estamos insertando la nueva parte o cabeza al inicio del cuerpo dependiendo la direccion
        self.body.insert(0, self.body[0] + self.direction)
        # Hacemos un if para cuando la serpiente crezca solo una celda pase a false y ya no crezca hasta comer denuevo
        if self.add_segment == True:
            self.add_segment = False
        # Si es falso no crece
        else:
            # Removemos la ultima parte del cuerpo con cada update para simular que avanza solo cuando no come
            self.body = self.body[:-1]
            
    # Para reiniciar la posicion de la serpiente cuando se pierde
    def reset(self):
        # Coordenadas del cuerpo de la serpiente cuando inicia
        self.body = [Vector2(6,9), Vector2(5,9), Vector2(4,9)]
        # Para moverla a la derecha a la serpiente al iniciar el juego
        self.direction = Vector2(1, 0)

# Creacion de clase para los llamados y asignacion de las otras clases
class Game:
    def __init__(self):
        self.serpiente = Snake()
        self.comida = Food(self.serpiente.body)
        self.estado = "RUNNING"
        self.score = 0
    
    def draw(self):
        self.comida.draw()
        self.serpiente.draw()
        
    def update(self):
        if self.estado == "RUNNING":
            self.serpiente.update()
            self.check_collision_with_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()
        
    def check_collision_with_food(self):
        # Si la serpiente toca la comida segenera una nueva comida en otro lugar
        if self.serpiente.body[0] == self.comida.position:
            self.comida.position = self.comida.generate_random_pos(self.serpiente.body)
            # Hacemos que cada ves que se genera comida tomara como si la serpiente debe crecer
            self.serpiente.add_segment = True
            self.score += 1
            
    def check_collision_with_edges(self):
        # Si la cabeza esta en x en la posicion mayor a la del tablero o menor a 0 que es donde inicia, significa que salio por izquierda o derecha
        if self.serpiente.body[0].x == number_of_celdas or self.serpiente.body[0].x == -1:
            # Pierde
            self.game_over()
        # Si la cabeza esta en y en la posicion mayor a la del tablero o menor a 0 que es donde inicia, signica que salio por arriba o abajo
        if self.serpiente.body[0].y == number_of_celdas or self.serpiente.body[0].y == -1:
            # Pierde
            self.game_over()
            
    def game_over(self):
        # Se reinicia la posicion de la serpiente a la inicial y la comida cambia de lugar
        self.serpiente.reset()
        self.comida.position = self.comida.generate_random_pos(self.serpiente.body)
        # Si el estado esta asi no inicie el juego
        self.estado = "STOPPED"
        self.score = 0
        
    def check_collision_with_tail(self):
        # Se crea una lista con todos los segmentos de la serpiente menos la cabeza, por eso 1 y no 0
        headless_body = self.serpiente.body[1:]
        # Checamos si la cabeza esta en los segmentos guardados, lo que significa colision
        if self.serpiente.body[0] in headless_body:
            self.game_over()

# Para crear el canvas/display de 750x750, pasamos de poner el numero fijo a asignar el tamaño dependidendod de el size de las celdas y la cantidad
pantalla = pygame.display.set_mode((2*OFFSET + celda_size*number_of_celdas,2*OFFSET + celda_size*number_of_celdas))#750,750 anteriormente

# Titulo de la pantalla o ventana
pygame.display.set_caption("Retro Snake")

# Reloj de objeto
reloj = pygame.time.Clock()

# Asignando la clase Food a la variable comida y Snake a serpiente
#comida = Food()  ya no usados, se agregaron a la clase game
#serpiente = Snake()

# Asignando la class Game a juego
juego = Game()

comida_surface = pygame.image.load("Graficos/comida.png")
# como la imgane es usada es de 500x500 toca transformarla a la escala de la celda 30x30
comida_surface = pygame.transform.scale(comida_surface, (celda_size, celda_size))

# Asignando el evento del jugador a una variable, tipo de evento especial para crear evento customs
SERPIENTE_UPDATE = pygame.USEREVENT
# Timer para que el evento de la serpiente pase solo cada 200 milisegundos (trigger o activador y cada cuanto)
pygame.time.set_timer(SERPIENTE_UPDATE, 200)

########################################
############ GAME LOOP #################

# Obtiene los eventos que pasan en pygame como lista
while True:
    for event in pygame.event.get():
        # Hacienco que detecte la activacion del evento
        if event.type == SERPIENTE_UPDATE:
            # Actualizando la posicion de la serpiente en cada llamado de evento
            juego.update()
        # Quit event o evento de salir para no romper el loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Representa el evento de tocar la una tecla para mover la serpiente a esa direccion
        if event.type == pygame.KEYDOWN:
            # Al perder si tocas una tecla inicia denuevo
            if juego.estado == "STOPPED":
                juego.estado = "RUNNING"
            # Representa tocar la flecha hacia arriba solo si no va para abajo
            if event.key == pygame.K_UP and juego.serpiente.direction != Vector2(0, 1):
                juego.serpiente.direction = Vector2(0, -1)
            # Representa tocar la flecha hacia abajo solo si no va para arriba
            if event.key == pygame.K_DOWN and juego.serpiente.direction != Vector2(0, -1):
                juego.serpiente.direction = Vector2(0, 1)
            # Representa tocar la flecha hacia izquierda solo si no va a la izquierda
            if event.key == pygame.K_LEFT and juego.serpiente.direction != Vector2(1, 0):
                juego.serpiente.direction = Vector2(-1, 0)
            # Representa tocar la flecha hacia derecha solo si no va a la izquierda
            if event.key == pygame.K_RIGHT and juego.serpiente.direction != Vector2(-1, 0):
                juego.serpiente.direction = Vector2(1, 0)
    
 # Dibujado
    # Definiendo el color que tendra la pantalla de fondo
    pantalla.fill(Verde)
    
    # Definimos los bordes visuales del juego
    pygame.draw.rect(pantalla, Verde_oscuro, (OFFSET-5, OFFSET-5, celda_size*number_of_celdas + 10, celda_size*number_of_celdas + 10), 5)
    
    # Dibujar todo lo que representa la comida (class Food) y todo lo que repesenta la serpiente (class Snake( ))
    #comida.draw() Se agregaron a la class Game
    #serpiente.draw()
    juego.draw()
    
    # Poniendo el tiulo y el color del mismo y el score
    title_surface = title_font.render("Retro Snake", True, Verde_oscuro)
    score_surface = score_font.render(str(juego.score), True, Verde_oscuro)
    # La ubicacion del titulo y donde
    pantalla.blit(title_surface, (OFFSET-5, 20))
    pantalla.blit(score_surface, (OFFSET-5, OFFSET + celda_size*number_of_celdas + 20))
    
    # Toma todo los cambios hechos en los objetos del juego y dibuja la imagen de ellos
    pygame.display.update()
    # Hace que nuestro game loop hace 60 ticks por segundo, necesario para limitar la velocidad
    reloj.tick(60)
    
#######################################