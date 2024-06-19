class Settings:
    '''a class to store all settings for Alien Invasion'''
    def __init__(self) -> None:
        self.rbg_color = (212, 175, 55)
        self.screen_width = 1000
        self.screen_height = 655
        self.screen_size = (self.screen_width, self.screen_height)
        # ship settings
        self.ship_limit = 3
        #bullet setting
        self.bullet_width = 3
        self.bullet_height = 6
        self.bullet_rbg_color = ('red')
        self.bullet_allowed = 25
        #alien setting
        self.fleet_drop_speed = 20
        #speed the game increase by
        self.speedup_scale = 1.5
        self.alien_level_up = 5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''initialize setting that change as the game progress'''
        self.ship_speed = .5
        self.bullet_speed = 1.0
        self.alien_speed = .1
        #fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        self.alien_points = 5
        
    def increase_speed(self):
        '''increase speed settings and alien point value'''
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points += self.alien_level_up