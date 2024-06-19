import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_game) -> None:
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        #load the alien image and set its rect attribute.
        filepath = 'images\\alien.png'
        self.image = pygame.image.load(filepath)
        self.rect = self.image.get_rect()
        #start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = 10
        #store the alien's exact horizontal position
        self.x = float(self.rect.x)
    
    def update(self):
        '''move the alien right or left'''
        self.x += (self.setting.alien_speed *
                    self.setting.fleet_direction)
        self.rect.x = int(self.x)
    
    def check_edges(self):
        '''returm True if alien is at the edge'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= screen_rect.left:
            return True

    