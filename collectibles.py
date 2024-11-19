import pygame
import random

class Coin:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x + size // 4, y + size // 4, size // 2, size // 2)

    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 223, 0), self.rect)
