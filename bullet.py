import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''a class to manage bullets fired from ship'''
    def __init__(self, ai_game) -> None:
        '''create a bullet object at ship's position'''
        super().__init__()
        self.screen = ai_game.screen
        self.setting = ai_game.setting
        self.color = self.setting.bullet_rbg_color
        #creat a bullet rect at (0, 0) and the set correct position
        self.rect = pygame.Rect(0, 0, self.setting.bullet_width,
                    self.setting.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop
        #store the bullet's position as a decimal value
        self.y = float(self.rect.y)
    
    def update(self):
        '''move the bullet up the screen'''
        self.y -= self.setting.bullet_speed
        self.rect.y = int(self.y)
    
    def draw_bullet(self):
        '''draw the bullet to screen'''
        pygame.draw.rect(self.screen, self.color, self.rect)

        

