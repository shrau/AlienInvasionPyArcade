import pygame

class Military:
    def __init__(self,ai_game):
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()

        self.image=pygame.image.load('images\military-truck-islated_1308-126561.bmp')
        self.rect=self.image.get_rect()

        self.rect_midbottom=self.screen_rect.midbottom
    
    def blitme(self):
        self.screen.blit(self.image,self.rect)