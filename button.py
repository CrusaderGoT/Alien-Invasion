import pygame

class Button:
    def __init__(self, ai_game, msg) -> None:
        '''initialize button attributes'''
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        #set the dimensions and properties of the button
        self.height, self.width = 25, 100
        self.button_color = (196, 196, 196)
        self.text_color = (0, 0, 0)
        self.text_font = pygame.font.SysFont('Agency FB', 18, True, False)
        #build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        #the button msg need to be prepped only once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        '''turn msg into a rendered image and center text on the button'''
        self.msg_image = pygame.font.Font.render(self.text_font, msg, True,
                         self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #draw blank button and the draw messasge
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
