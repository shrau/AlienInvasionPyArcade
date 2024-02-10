import sys
import pygame
from settings import Setting
from military import Military

class BlueBackground:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((1200,700))
        pygame.display.set_caption("Alien Invasion")
        self.military_jeep=Military(self)
        self.bg_colour=(0,150,255)
        self.clock=pygame.time.Clock()

    def run_game(self):
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    sys.exit()
        
            self.screen.fill(self.bg_colour)
            self.military_jeep.blitme()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ =='__main__':
    ai=BlueBackground()
    ai.run_game()