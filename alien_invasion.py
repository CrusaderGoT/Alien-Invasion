import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard
from music import Music

class AlienInvasion:
    '''overall class to manage game assets and behaviour'''

    def __init__(self) -> None:
        '''initialize the game, and create game resources'''
        pygame.init()
        self.setting = Settings()
        self.music = Music()
        #set display size/mode
        self.screen = pygame.display.set_mode((self.setting.screen_width, self.setting.screen_height))
        pygame.display.set_caption('Jay vs Ms.Marvels')
        icon = pygame.image.load('images\\marvel.png')
        pygame.display.set_icon(icon)
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullet = pygame.sprite.Group()
        self.alien = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, 'Play')
        self.score = ScoreBoard(self)
    def run_game(self):
        '''start the main loop for the game'''
        while True:
            self._check_events()
            self.score.check_high_score()
            if self.stats.game_active == True:
                self.ship.update()
                self._update_bullet()
                self._check_bullet_alien_collision()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        '''watch for keyboard and mouse events.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_event(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
        
    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #reset the game settings
            self.setting.initialize_dynamic_settings()
            #reset the game statistics
            self.stats.reset_stats()
            self.stats.game_active = True
            self.score.prep_score()
            self.score.prep_high_score()
            self.score.prep_level()
            self.score.check_high_score()
            #empty aliens and bullets
            self.alien.empty()
            self.bullet.empty()
            #create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            #hide mouse cursor during play
            pygame.mouse.set_visible(False)
            #play music
            self.music.play_music()

    def _check_keydown_event(self, event):
        '''respond to key presses'''
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_event(self, event):
        '''respond to key releases'''
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                 self.ship.moving_left = False
                 
    def _update_screen(self):
        '''updates images on the screen, and flip to a new screen.'''
        self.screen.fill(self.setting.rbg_color)
        self.ship.blitme()
        for bullet in self.bullet.sprites():
            bullet.draw_bullet()
        self.alien.draw(self.screen)
        self.score.show_score()
        # draw the play button
        if not self.stats.game_active:
            self.play_button.draw_button()
            #stop music
            self.music.stop_music()
        #make the most recent drawn screen visible.
        pygame.display.flip()
    
    def _fire_bullet(self):
        '''creat a new bullet and add it to the bullet group'''
        if len(self.bullet) < self.setting.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullet.add(new_bullet)
    
    def _update_bullet(self):
        '''updates position of bullets and gets rid of old bullet'''
        self.bullet.update()
        #remove bullets that have dissapeared atop the screen
        for bullet in self.bullet.copy():
            if bullet.rect.bottom <= 0:
                self.bullet.remove(bullet)
        
    def _check_bullet_alien_collision(self):
        '''check for any bullets-alien collision'''
        #remove any bullet that has collided
        collision = pygame.sprite.groupcollide(
                    self.bullet, self.alien, True, True)
        if collision:
            for aliens in collision.values():
                self.stats.score += self.setting.alien_points * len(aliens)
                self.score.prep_score()
                self.score.check_high_score()
        #destroy all bullets and create new fleet
        if not self.alien:
                self.bullet.empty()
                self._create_fleet()
                self.setting.increase_speed()
                #increase level
                self.stats.level += 1
                self.score.prep_level()

    def _create_alien(self, alien_no, row_no):
        '''creates an alien and places it in a row'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        alien.x = alien_width + (2 * alien_width) * alien_no
        alien.rect.x = alien.x
        alien.rect.y = 26 + 2 * alien_height * row_no
        self.alien.add(alien)

    def _create_fleet(self):
        '''creates the fleet of aliens'''
        #spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien_width = alien.rect.width
        aliens_space_x = self.setting.screen_width - (2 * alien_width)
        #find the number of aliens in a row
        no_alien_x = aliens_space_x // (2 * alien_width)
        #determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.setting.screen_height -
                            (3 * alien_height) - ship_height)
        no_rows = available_space_y // (2 * alien_height)
        #create full fleet of aliens
        for row_no in range(no_rows):
            for alien_no in range(no_alien_x):
                self._create_alien(alien_no, row_no)

    def _update_aliens(self):
        '''check if the fleet is at an edge,
        then update the positions of all the aliens in the fleet'''
        self._check_fleet_edges()
        self.alien.update()
        #look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.alien):
            self._ship_hit()
        #look for aliens hitting the bottom of the screen
        self._check_alien_bottom()

    def _check_fleet_edges(self):
        '''respond appropriately if any aliens have reached an edge'''
        for alien in self.alien.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''drop the entire fleet and change fleet's direction'''            
        for alien in self.alien.sprites():
            alien.rect.y += self.setting.fleet_drop_speed
        self.setting.fleet_direction *= -1

    def _ship_hit(self):
        '''respond to a ship being hit by an alien'''
        #drecrement ship left
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.score.prep_ship()
            #get rid of any remaing aliens and bullets
            self.alien.empty()
            self.bullet.empty()
            #create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
            #pause
            sleep(.5)
        else: 
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_alien_bottom(self):
        '''check if any alien has reached the bottom'''
        screen_rect = self.screen.get_rect()
        for alien in self.alien.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat the same as a ship hit
                self._ship_hit()
                break



if __name__ == "__main__":
    # make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()