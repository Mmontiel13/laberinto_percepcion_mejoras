import pygame
from maze import Maze
from player import Player
from npc import NPC
import random

pygame.init()

# Configuración de pantalla y juego
WIDTH, HEIGHT = 700, 750
TILE_SIZE = 50  # tamaño de cada cuadro
ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE  # cantidad de filas y columnas
screen = pygame.display.set_mode((WIDTH, HEIGHT))
timer = pygame.time.Clock()
fps = 60

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
WALL_COLOR = (88, 77, 111)
HELP_COLOR = (0, 255, 0)  # Verde para las ayudas de pausar NPCs
SPEED_COLOR = (128, 0, 128)  # Morado para las ayudas de velocidad
COIN_COLOR = (255, 223, 0)  # Amarillo para las monedas

# Crear instancia de laberinto
maze = Maze(ROWS, COLS)

# Configuraciones iniciales del jugador
player = Player(x=50, y=50, width=20, height=20, speed=5)

# Generar NPCs en celdas aleatorias del laberinto
npc_list = []
npc_count = 5  # cantidad de NPCs a crear
for _ in range(npc_count):
    while True:
        row = random.randint(1, maze.rows - 2)
        col = random.randint(1, maze.cols - 2)
        if maze.grid[row][col] == 0:  # asegurarse que la posición sea un camino
            npc_x, npc_y = col * TILE_SIZE, row * TILE_SIZE
            npc = NPC(npc_x, npc_y, TILE_SIZE, maze)  # pasar el laberinto a los NPCs
            npc_list.append(npc)
            break

# Generar monedas en celdas aleatorias del laberinto
coins = []
coin_count = 10  # Número de monedas a generar
for _ in range(coin_count):
    while True:
        row = random.randint(1, maze.rows - 2)
        col = random.randint(1, maze.cols - 2)
        if maze.grid[row][col] == 0:  # asegurarse que la posición sea un camino
            coins.append(pygame.Rect(col * TILE_SIZE + 15, row * TILE_SIZE + 15, 20, 20))  # Ajuste de tamaño
            break

# Generar rectángulos de ayuda de pausa de NPCs (verdes)
help_rects = []
help_count = 5  # Número de rectángulos de ayuda
for _ in range(help_count):
    while True:
        row = random.randint(1, maze.rows - 2)
        col = random.randint(1, maze.cols - 2)
        if maze.grid[row][col] == 0:  # asegurarse que la posición sea un camino
            help_rects.append(pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            break

# Generar rectángulos de ayuda de velocidad (morados)
speed_rects = []
speed_count = 3  # Número de rectángulos de velocidad
for _ in range(speed_count):
    while True:
        row = random.randint(1, maze.rows - 2)
        col = random.randint(1, maze.cols - 2)
        if maze.grid[row][col] == 0:  # asegurarse que la posición sea un camino
            speed_rects.append(pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            break

# Configuración inicial del contador de monedas
coins_collected = 0
font = pygame.font.Font(None, 36)  # Fuente para mostrar el contador
font_color = (255, 255, 255)

# Mostrar el contador de monedas en pantalla
def draw_coin_counter(screen, coins_collected, coin_count):
    coin_text = f"Monedas: {coins_collected}/{coin_count}"
    text_surface = font.render(coin_text, True, font_color)
    screen.blit(text_surface, (10, 10))

# Función para restablecer el juego
def reset_game():
    # Restablecer la posición del jugador a su posición inicial
    player.rect.x = 50
    player.rect.y = 50

    # Restablecer las posiciones de los NPCs a sus posiciones iniciales
    for npc in npc_list:
        row = random.randint(1, maze.rows - 2)
        col = random.randint(1, maze.cols - 2)
        if maze.grid[row][col] == 0:  # asegurarse que la posición sea un camino
            npc.rect.x, npc.rect.y = col * TILE_SIZE, row * TILE_SIZE

    # Otras variables que necesiten ser reiniciadas (si es necesario)
    global game_over, coins_collected
    coins_collected = 0
    game_over = False

# Definir los estados de las ayudas
help_active = False  # Estado de si la ayuda de pausar NPCs está activa o no
speed_active = False  # Estado de si la ayuda de velocidad está activa o no
pause_time = 0  # Temporizador para pausar NPCs
speed_time = 0  # Temporizador para la velocidad
exit_x, exit_y = maze.rows - 2, maze.cols - 2  # Coordenadas de la salida

# Bucle principal del juego
run = True
while run:
    timer.tick(fps)
    screen.fill(BLACK)

    # Mostrar el contador de monedas en pantalla
    draw_coin_counter(screen, coins_collected, coin_count)

    # Obtener el estado de las teclas
    keys = pygame.key.get_pressed()

    # Actualizar el movimiento del jugador
    player.handle_movement(keys, maze)

    # Obtener la posición actual del jugador para pasarla a los NPCs
    player_position = (player.rect.x, player.rect.y)

    # Detectar colisión entre el jugador y las monedas
    for coin in coins[:]:
        if player.rect.colliderect(coin):
            coins_collected += 1
            coins.remove(coin)

    # Detectar colisión entre el jugador y los rectángulos de ayuda (verde - pausa NPCs)
    for help_rect in help_rects:
        if player.rect.colliderect(help_rect) and not help_active:
            help_active = True
            pause_time = pygame.time.get_ticks()  # Capturamos el tiempo actual
            break  # Salir del bucle una vez que se activa la ayuda de pausar NPCs

    # Detectar colisión entre el jugador y los rectángulos de velocidad (morado)
    for speed_rect in speed_rects:
        if player.rect.colliderect(speed_rect) and not speed_active:
            player.speed = 10  # Aumentar la velocidad del jugador
            speed_active = True
            speed_time = pygame.time.get_ticks()  # Capturamos el tiempo actual
            break  # Salir del bucle una vez que se activa la ayuda de velocidad

    # Pausar NPCs si la ayuda de pausa está activa
    if help_active:
        # Si han pasado más de 5 segundos (5000 milisegundos), los NPCs pueden reanudar el movimiento
        if pygame.time.get_ticks() - pause_time > 5000:
            help_active = False  # Desactivar la ayuda de pausar NPCs

    # Desactivar la velocidad aumentada después de 5 segundos
    if speed_active:
        if pygame.time.get_ticks() - speed_time > 5000:
            player.speed = 5  # Restablecer la velocidad
            speed_active = False  # Desactivar la ayuda de velocidad

    # Mover el jugador y NPCs (si la ayuda no está activa)
    if not help_active:
        player.handle_movement(keys, maze)
        for npc in npc_list:
            npc.move(player.rect.center)

    # Detectar colisión entre el jugador y los NPCs
    for npc in npc_list:
        if player.rect.colliderect(npc.rect):
            reset_game()  # Reiniciar el juego si el jugador choca con un NPC
            break

    # Detectar si el jugador ha tocado la salida (esquina inferior derecha)
    if player.rect.colliderect(pygame.Rect(exit_y * TILE_SIZE, exit_x * TILE_SIZE, TILE_SIZE, TILE_SIZE)):
        print("¡Has ganado! El jugador llegó a la salida.")
        run = False

    # Dibujar las monedas
    for coin in coins:
        pygame.draw.ellipse(screen, COIN_COLOR, coin)

    # Dibujar los rectángulos de ayuda
    for help_rect in help_rects:
        pygame.draw.rect(screen, HELP_COLOR, help_rect)

    # Dibujar los rectángulos de velocidad
    for speed_rect in speed_rects:
        pygame.draw.rect(screen, SPEED_COLOR, speed_rect)

    # Dibujar el laberinto y el jugador
    maze.draw(screen)
    for npc in npc_list:
        npc.draw(screen)
    player.draw(screen)

    # Mostrar el contador de monedas en pantalla
    draw_coin_counter(screen, coins_collected, coin_count)

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()  # Actualizar pantalla

pygame.quit()
