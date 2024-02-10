import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button

class AlienInvasion:
    """overall class to manage game assets and behaviour."""

    def __init__(self):
        """initialize the game and create game resource."""
        pygame.init()

        self.clock=pygame.time.Clock()
        self.settings=Settings()
        self.screen=pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        #create an instance to store the statistics
        self.stats=GameStats(self)

        #for full screen mode
        #self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        #self.settings.screen_width=self.screen.get_rect().width
        #self.settings.screen_height=self.screen.get_rect().height

        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()

        self._create_fleet()
        #pygame.display.set_caption("Alien Invasion")

        #set the background colour
        self.bg_color=(230,230,230)
    
        #start Alien Invasion in an inactive state.
        self.game_active=False

        #make the Play button
        self.play_button=Button(self,"Play")

    def run_game(self):
        """start the main loop for game"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()

            #print(len(self.bullets))
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """respond to keypress and mouse events."""
        #watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                sys.exit()
            elif event.type==pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type==pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        """start new game when player click Play."""
        button_clicked= self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #reset the game statistics.
            self.stats.reset_stats()
            self.game_active=True

            #get rid of any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            #create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
        
            #Hide the mouse cursor
            pygame.mouse.set_visible(False)
        
    def _check_keydown_events(self,event):
        """respond to keypresses."""
        if event.key==pygame.K_RIGHT:
        #move the ship to right
            self.ship.moving_right=True
        elif event.key==pygame.K_LEFT:
        #move the ship to left
            self.ship.moving_left=True
        #to quit the game
        elif event.key==pygame.K_q:
            sys.exit()
        elif event.key==pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self,event):
        """responses to key releases"""
        if event.key==pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key==pygame.K_LEFT:
            self.ship.moving_left=False

    def _fire_bullet(self):
        """create new bullet and add it to the bullets group."""
        if len(self.bullets)<self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)
    
    def _update_aliens(self):
        """check if the fleet is at edge , then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        #look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        
        #look for aliens hitting the bottom of the screen 
        self._check_alien_bottom()    

    def _ship_hit(self):
        """respond to the ship being hit by an alien"""
        #decrease ships left
        if self.stats.ship_left>0:
        #decrease ships left
            self.stats.ship_left-=1

        #get rid of remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

        #create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()
        
        # create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

        #pause 
            sleep(0.5)
        else:
            self.game_active=False
            pygame.mouse.set_visible(True)

    def _update_bullets(self):
        """update position og bullets and get rid of old bullets."""
        #update bullet positions
        self.bullets.update()

        #get rid of disappered bullets.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom<=0:
                self.bullets.remove(bullet)

        self._check_bullet_collisions()

    def _check_bullet_collisions(self):
        """respond to bullet-alien collisions"""
        #remove any bullets and a.iens that have collided
        collisions=pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,True
        )

        if not self.aliens:
            #destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

    def _create_fleet(self):
        """create the fleet of aliens."""
        #create an alien and keep adding aliens until there's no room left
        #spacing between aliens is one alien width and one alien height
        alien=Alien(self)
        alien_width,alien_height=alien.rect.size

        current_x,current_y=alien_width,alien_height
        while current_y <(self.settings.screen_height-3*alien_height):
            while current_x < (self.settings.screen_width-2*alien_width):
                self._create_alien(current_x,current_y)
                current_x +=2*alien_width
            #finished a row; reset x value and increment y value
            current_x=alien_width
            current_y +=2*alien_height

    def _create_alien(self,x_position,y_position):
            """create an alien and place it in the row"""
            new_alien=Alien(self)
            new_alien.x=x_position
            new_alien.rect.x=x_position
            new_alien.rect.y=y_position
            self.aliens.add(new_alien)

    def _check_alien_bottom(self):
        """check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >=self.settings.screen_height:
                #treat this the same as if the ship got it.
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """respond appropriately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """drop the entire fleet and change the direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """update images on the screen and flip to the new screen."""
        #redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)   

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.aliens.draw(self.screen)

        #Draw the play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        #make the most recently drawn screen visible
        pygame.display.flip()



if __name__=='__main__':
    #make game instance and run the game
    ai=AlienInvasion()
    #Code for running game
    ai.run_game()