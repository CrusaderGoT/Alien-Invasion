class GameStats:
    '''track statistics for alien invasion'''
    def __init__(self, ai_game) -> None:
        '''initialize statistics'''
        self.setting = ai_game.setting
        self.reset_stats()
        self.game_active = False
        #high score should never be reset
        self.high_score = 0
            
        
    def reset_stats(self):
        '''initialize statistics that can change during the game'''
        self.ships_left = self.setting.ship_limit
        self.score = 0
        self.level = 1