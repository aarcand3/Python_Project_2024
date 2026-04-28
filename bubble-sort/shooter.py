import pygame
from bubbles import *

class Shooter:
    """Calss to manage shooter that takes out bubbles"""
    def __init__(self, game):
        """initialize shooter and location"""
        self.display = game.screen
        self.image = pygame.image.load('bubpics/arrow.png')
        arrow_rect = self.image.get_rect()
        self.rect = arrow_rect
        self.rect.midbottom = game.screen.get_rect().midbottom
        self.moving_right = False
        self.moving_left =False
        self.next_bullet = None
        # Rotation angle (in degrees)
        self.rotation_angle = 90
    def update (self):
        """update the movement of the shooter when aiming"""
        if self.moving_right and self.rotation_angle <180:
            self.rotation_angle -=2
        if self.moving_left and self.rotation_angle<180:
            self.rotation_angle +=2
        self.rotated_image = pygame.transform.rotate(self.image, self.rotation_angle)
    def get_point(self):
        """get the current angle"""
        return self.rotation_angle
    def blitme(self):
        """Draw arrow where wanted"""
        rotated_rect = self.rotated_image.get_rect(center=self.rect.center)
        self.display.blit(self.rotated_image,rotated_rect)
        if self.next_bullet:
            next_bullet_rect = self.next_bullet.get_rect()
            next_bullet_rect.midtop = self.rect.midtop
            self.display.blit(self.next_bullet,next_bullet_rect)
    def set_next_bullet(self, color):
        """Set the next bullet to be displayed on the shooter.""" 
        bullet_radius = 15
        self.next_bullet = pygame.Surface((bullet_radius * 2, bullet_radius * 2)\
            , pygame.SRCALPHA)
        self.rect_next = pygame.draw.circle(self.next_bullet, color,\
            (bullet_radius, bullet_radius),bullet_radius)
    