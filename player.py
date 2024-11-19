import pygame

class Player:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)  # Representación del jugador en forma de rectángulo
        self.speed = speed  # Velocidad de movimiento del jugador
    
    def handle_movement(self, keys, maze):
        # Guardar la posición original para revertir en caso de colisión
        original_x, original_y = self.rect.x, self.rect.y
        
        # Movimiento en cada dirección, basado en las teclas W, A, S, D
        if keys[pygame.K_w]:  # Movimiento hacia arriba
            self.rect.y -= self.speed
            if self.collides_with_walls(maze.walls):
                self.rect.y = original_y  # Revertir si hay colisión

        if keys[pygame.K_s]:  # Movimiento hacia abajo
            self.rect.y += self.speed
            if self.collides_with_walls(maze.walls):
                self.rect.y = original_y  # Revertir si hay colisión

        if keys[pygame.K_a]:  # Movimiento hacia la izquierda
            self.rect.x -= self.speed
            if self.collides_with_walls(maze.walls):
                self.rect.x = original_x  # Revertir si hay colisión

        if keys[pygame.K_d]:  # Movimiento hacia la derecha
            self.rect.x += self.speed
            if self.collides_with_walls(maze.walls):
                self.rect.x = original_x  # Revertir si hay colisión

    def collides_with_walls(self, walls):
        # Recorre todas las paredes y verifica colisiones
        for wall in walls:
            if self.rect.colliderect(wall):
                return True  # Hay colisión con una pared
        return False

    def draw(self, screen):
        # Dibujar al jugador en la pantalla como un cuadrado azul
        pygame.draw.rect(screen, (0, 0, 255), self.rect)
