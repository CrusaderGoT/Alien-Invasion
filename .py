import sys
import pygame

class Image:
    def __init__(self, test) -> None:
        self.screen = test.screen
        self.screen_rect = test.screen.get_rect()
        self.image = pygame.image.load('c:/Users/DELL/Documents/Python Files/Alien Invasion/images/marvel.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
    def blitme(self):
        self.screen.blit(self.image, self.rect)

class Try:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((700, 650))
        self.screen.fill(('white'))
        self.image = Image(self)
        
    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()
            self.image.blitme()
        

ai = Try()
ai.run_game()