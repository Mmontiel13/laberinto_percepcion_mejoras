import pygame
import random
import math
import time

class NPC:
    def __init__(self, x, y, size, maze, speed=20, view_distance=120, move_delay=0.05):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = (255, 165, 0)  # Color original naranja
        self.detected_color = (255, 0, 0)  # Color rojo para cuando detecte al jugador
        self.size = size
        self.maze = maze
        self.directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        self.speed = speed
        self.move_counter = 0
        self.view_distance = view_distance
        self.player_detected = False
        self.move_delay = move_delay  # Retardo de movimiento en segundos
        self.last_move_time = time.time()  # Tiempo de la última vez que se movió

    def is_within_vision_range(self, player_position):
        dx = abs(self.rect.centerx - player_position[0])
        dy = abs(self.rect.centery - player_position[1])
        return ((dx <= self.view_distance and dy <= self.rect.height // 2) or 
                (dy <= self.view_distance and dx <= self.rect.width // 2))

    def get_valid_adjacent_position(self, target_position, step=100):
        min_distance = float('inf')
        best_position = None

        for dx, dy in self.directions:
            adj_x = self.rect.x + dx * step
            adj_y = self.rect.y + dy * step
            maze_x, maze_y = adj_x // self.size, adj_y // self.size
            if (0 <= maze_y < len(self.maze.grid) and 
                0 <= maze_x < len(self.maze.grid[0]) and 
                self.maze.grid[maze_y][maze_x] == 0):
                distance = math.sqrt((adj_x - target_position[0]) ** 2 + (adj_y - target_position[1]) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    best_position = (adj_x, adj_y)

        return best_position

    def move(self, player_position):
        current_time = time.time()
        
        self.player_detected = self.is_within_vision_range(player_position)

        if self.player_detected:
            if current_time - self.last_move_time >= self.move_delay:
                best_position = self.get_valid_adjacent_position(player_position, step=10)
                if best_position:
                    self.rect.x, self.rect.y = best_position
                self.last_move_time = current_time
        else:
            if self.move_counter >= self.speed:
                dx, dy = random.choice(self.directions)
                new_x = self.rect.x + dx * self.size
                new_y = self.rect.y + dy * self.size
                maze_x, maze_y = new_x // self.size, new_y // self.size
                if (0 <= maze_y < len(self.maze.grid) and 
                    0 <= maze_x < len(self.maze.grid[0]) and 
                    self.maze.grid[maze_y][maze_x] == 0):
                    self.rect.x = new_x
                    self.rect.y = new_y
                self.move_counter = 0
            self.move_counter += 1

    def draw(self, screen):
        # Dibujar los rectángulos de perspectiva como contornos
        vertical_rect = pygame.Rect(
            self.rect.centerx - self.rect.width // 2,
            self.rect.centery - self.view_distance,
            self.rect.width,
            self.view_distance * 2
        )
        horizontal_rect = pygame.Rect(
            self.rect.centerx - self.view_distance,
            self.rect.centery - self.rect.height // 2,
            self.view_distance * 2,
            self.rect.height
        )
        
        pygame.draw.rect(screen, (255, 255, 255), vertical_rect, 1)  # Contorno vertical
        pygame.draw.rect(screen, (255, 255, 255), horizontal_rect, 1)  # Contorno horizontal
        
        # Cambiar el color si detecta al jugador
        color = self.detected_color if self.player_detected else self.color
        pygame.draw.rect(screen, color, self.rect)
