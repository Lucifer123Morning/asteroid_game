import pygame
from constants import EXPLOSION_DURATION  # Ensure you define this constant

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.image.load('assets/explosion_1.png').convert_alpha()  # Load explosion image
        self.rect = self.image.get_rect(center=position)
        self.timer = EXPLOSION_DURATION  # Duration for which the explosion lasts

    def update(self, dt):
        self.timer -= dt  # Decrease the timer
        if self.timer <= 0:  # If time is up, remove the explosion
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)  # Draw the explosion at its rect position
