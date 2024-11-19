import pygame
import random

TILE_SIZE = 50 ##es el tamaño de cada cuadro
WALL_COLOR = (88, 77, 111)

class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = self.generate_maze(rows, cols)
        self.add_extra_paths()  # Agregar caminos adicionales
        self.walls = self.create_walls()

    def generate_maze(self, rows, cols):
        # Crear matriz base con paredes (1 = pared, 0 = camino)
        maze = [[1 for _ in range(cols)] for _ in range(rows)]
        
        # Punto de inicio del laberinto
        start_x, start_y = 1, 1
        self.carve_path(maze, start_x, start_y)
        
        # Definir el punto de salida
        exit_x, exit_y = rows - 2, cols - 2
        maze[exit_x][exit_y] = 0  # Asegurar que haya una salida
        
        return maze

    def carve_path(self, maze, x, y):
        # Lista de direcciones para moverse (arriba, abajo, izquierda, derecha), en pasos de 2 para evitar paredes dobles
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)  # Mezclar direcciones para que el laberinto sea aleatorio cada vez
        
        for dx, dy in directions:
            # Calcular las coordenadas de la celda siguiente
            nx, ny = x + dx, y + dy
            
            # Verificar que la celda siguiente esté dentro de los límites y sea una pared
            if 1 <= nx < self.rows - 1 and 1 <= ny < self.cols - 1 and maze[nx][ny] == 1:
                # Abrir el camino hacia la siguiente celda
                maze[x + dx // 2][y + dy // 2] = 0  # Crear un paso entre celdas
                maze[nx][ny] = 0  # Marcar la celda siguiente como camino
                self.carve_path(maze, nx, ny)  # Llamada recursiva para continuar tallando el laberinto

    def add_extra_paths(self):
        # Agregar caminos adicionales para mayor conectividad
        for row in range(1, self.rows - 1, 2):  # Saltar filas para crear espacios
            for col in range(1, self.cols - 1, 2):  # Saltar columnas
                if random.random() < 0.3:  # Probabilidad de abrir una conexión extra
                    if row + 2 < self.rows - 1:
                        self.grid[row + 1][col] = 0  # Abrir camino vertical
                    if col + 2 < self.cols - 1:
                        self.grid[row][col + 1] = 0  # Abrir camino horizontal

    def create_walls(self):
        walls = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 1:  # 1 representa una pared
                    wall_rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    walls.append(wall_rect)
        return walls

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, WALL_COLOR, wall)