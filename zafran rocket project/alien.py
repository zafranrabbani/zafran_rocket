import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # ✅ Load gambar ALIEN dan SCALE dengan benar
        image_loaded = pygame.image.load('images/alien.bmp')     # ← pastikan file ini ADA
        self.image = pygame.transform.scale(image_loaded, (50, 38))  # ⬅️ (width, height)

        # ✅ Ambil rect dari image
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)
