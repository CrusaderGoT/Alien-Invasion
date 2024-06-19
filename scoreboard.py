import pygame.font
from pygame.sprite import Group
from ship import Ship

class ScoreBoard:
    '''a class to report scoring info'''
    def __init__(self, ai_game) -> None:
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.setting = ai_game.setting
        self.stats = ai_game.stats
        self.ai_game = ai_game
        #font settings for scorring information
        self.font = pygame.font.SysFont('Bauhaus 93', 15, italic=True)
        self.text_color = (0, 0, 0)
        # prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()

    def prep_score(self):
        '''turn the score into a rendered image'''
        score = self.stats.score
        f_score = '{:,}'.format(score)
        self_str = f'Score: {str(f_score)}'
        self.score_image = self.font.render(self_str, True,
                           self.text_color)
        #display the score at the top right of the screen
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 10
        self.score_image_rect.top = 8

    def prep_high_score(self):
        '''convert highs score to image'''
        score = self.stats.high_score
        f_score = '{:,}'.format(score)
        self.str = f'High Score: {str(f_score)}'
        self.high_score_img = self.font.render(self.str, True, self.text_color)
        self.high_score_rect = self.high_score_img.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_image_rect.top

    def check_high_score(self):
        '''check to see if there's a new high score and loads current high score'''
        self.load_high_score()
        self.prep_high_score()
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()
            self.save_high_score()

    def save_high_score(self):
        file_name = 'high score.txt'
        with open(file_name, 'w') as f:
            high_score = str(self.stats.high_score)
            f.write(high_score)

    def load_high_score(self):
        file_name = 'high score.txt'
        with open(file_name) as f:
            high_score = f.read()
            self.stats.high_score = int(high_score)

    def prep_level(self):
        '''turn the level into a rendered image'''
        level = self.stats.level
        level_str = f'Level {str(level)}'
        self.level_image = self.font.render(level_str,True,self.text_color)
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.left = self.screen_rect.left + 10
        self.level_image_rect.top = self.score_image_rect.top

    def prep_ship(self):
        '''show how many ships are left'''
        self.ship_life = Group()
        for ship_no in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.left = (self.level_image_rect.right + 10) + ship_no * (ship.rect.width + 8)
            ship.rect.bottom = self.level_image_rect.bottom
            self.ship_life.add(ship)
        

    def show_score(self):
        '''draw score, level, ship lifes, and high score on screen'''
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_img, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.ship_life.draw(self.screen)

    