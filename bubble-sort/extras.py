import pygame
from pygame import mixer


class Extra:
    def __init__(self, game):
        """Class to organize music and other cosmetic extras"""
        self.screen = game.screen
        self.background = game.background
        self.splash_images = [
            'splash/Water01.png',
            'splash/Water02.png','splash/Water03.png',
            'splash/Water04.png','splash/Water05.png',
            'splash/Water06.png','splash/Water07.png',
            'splash/Water08.png','splash/Water09.png',
            'splash/Water10.png','splash/Water11.png',
            'splash/Water12.png','splash/Water13.png',
            'splash/Water14.png','splash/Water15.png',
            'splash/Water16.png','splash/Water17.png',
            'splash/Water18.png','splash/Water19.png',
            'splash/Water20.png','splash/Water21.png',
            'splash/Water22.png','splash/Water23.png',
            'splash/Water24.png','splash/Water25.png',
            'splash/Water26.png','splash/Water27.png',
            'splash/Water28.png','splash/Water29.png',
            
        ]
        self.sound_list = [
            'sounds/background.mp3',
            'sounds/shoot.ogg',
            'sounds/popcork.ogg',
            'sounds/splash.mp3',
            'sounds/dead.mp3'
        ]
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.3)
        
        self.animation = [pygame.image.load(path) for path in self.splash_images]
        
    def play(self, sound):
        """To handle playing all sounds"""
        pygame.mixer.music.load(self.sound_list[sound])
        pygame.mixer.get_busy()
        if sound == 0:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)
        else:
            effect = pygame.mixer.Sound(self.sound_list[sound])
            effect.play()
        
    def stop(self):
        """Stop music when needed"""
        mixer.music.stop()
    
    def play_splash_animation(self):
        """Play the splash animation."""
        for splash_surface in self.animation:  
            self.screen.blit(self.background, (0, 0))  
            self.screen.blit(splash_surface, (775 // 2 - 100, 575 // 2 - 100)) 
            pygame.display.flip() 
            pygame.time.delay(50)  
