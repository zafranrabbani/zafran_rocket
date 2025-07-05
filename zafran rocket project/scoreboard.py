import pygame
from pygame.sprite import Sprite, Group

class Scoreboard:
    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 36)

        self.prep_images()

    def prep_images(self):
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        rounded = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.ai_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 10

    def prep_high_score(self):
        high = int(round(self.stats.high_score, -1))
        high_str = "{:,}".format(high)
        self.high_image = self.font.render(high_str, True,
                                           self.text_color, self.ai_settings.bg_color)
        self.high_rect = self.high_image.get_rect()
        self.high_rect.centerx = self.screen_rect.centerx
        self.high_rect.top = 10

    def prep_level(self):
        self.level_image = self.font.render(str(self.stats.level), True,
                                            self.text_color, self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 5

    def prep_ships(self):
        self.ships = Group()
        icon_img = pygame.image.load('images/heart.png')
        scale_size = (28, 28)              
        icon_img = pygame.transform.scale(icon_img, scale_size)
        
        for i in range(self.stats.ships_left):
            icon = Sprite()
            icon.image = icon_img
            icon.rect = icon.image.get_rect()
            icon.rect.x = 10 + i * (scale_size[0] + 10)   # 10 px jarak antar‑ikon
            icon.rect.y = 10
            self.ships.add(icon)

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_image, self.high_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
