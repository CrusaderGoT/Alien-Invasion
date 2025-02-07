import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    'a class to manage the ship'
    def __init__(self, ai_game) -> None:
        """Initialize the ship and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.setting = ai_game.setting
        #load the ship image and get its rect.
        shooter_file_location = 'images\\shooter.bmp'
        self.image = pygame.image.load(shooter_file_location)
        self.rect = self.image.get_rect()
        #start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        #movement flag
        self.moving_right = False
        self.moving_left = False
        #store a new decimal value for the ship's horizontal position
        self.x = float(self.rect.x)
    def update(self):
        '''updates the ship's position based on the movement flag'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.setting.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.setting.ship_speed
        #update rect object from self.x
        self.rect.x = int(self.x)
    def blitme(self):
        '''draw the shooter/ship at its current location'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''center the ship on the screen'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)