import pygame, sys
from bubbles import *
from shooter import *
from extras import Extra
import time
# Screen dimensions
SCREEN_WIDTH = 775
SCREEN_HEIGHT = 575

class Game:
    """Class to manage the entire game"""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Bubble Shooter")
        self.background = pygame.image.load('bubpics/sky.png')
        self.music = Extra(self)
        self.music.play(0)
        self.font = pygame.font.SysFont('Times New Roman', 40)
        self.small_font = pygame.font.SysFont('Times New Roman', 20)
       
        self.clock = pygame.time.Clock()
        self.cloud = (pygame.transform.scale(pygame.image.load
                                              ('bubpics/cloud2.png'),(400,300)))
        self.speed = 0.05
        self.score = 0
        self.level = 1
        self.num_rows = 10
        self.start_rows = -300
        
        self.shooter = Shooter(self)
        self.bullets_on_screen = 0
        self.bullets_allowed = 10
        self.bubble_rows = create_bubble_rows(self.num_rows, self.start_rows,
                                              self.speed)
        self.bullets = pygame.sprite.Group()
        self.bullet_color = Bubble.get_rand_color()
        self.final_score=0
        self.remove_float = remove_isolated_bubbles(self.bubble_rows)
    
    def main(self):
        """Main game loop."""
        game_end = False
        running =True
        while running:
            self.music.play(0)
            self._check_events()
            self.check_collisions()
            self.update()
            
            game = self.check_end()
            if game:
                self.draw_end_screen()
                     
    def _check_events(self):
     """Check for key events."""
     for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.shooter.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.shooter.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self.music.stop()
            self.music.play(1)
            self.fire_bullet() 
            self.remove_float
        elif event.key == pygame.k_p:
            return True
        elif event.key == pygame.K_r:
            self.reset_game()
        elif event.key == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.shooter.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.shooter.moving_left = False
        elif event.key == pygame.K_q:
            sys.exit()
            
    def fire_bullet(self):
        """update bullet and position"""
        if len(self.bullets) < self.bullets_allowed:
                angle = self.shooter.get_point()
                bullet = Bullet(self,angle, self.bullet_color)
                self.bullets.add(bullet)
                new_color = Bubble.get_rand_color()
                self.bullet_color = new_color
                self.shooter.set_next_bullet(new_color)   

    def check_collisions(self):
        """Check for collisions between bullets and bubbles."""
        for bullet in self.bullets.copy():
            collided = pygame.sprite.spritecollide(bullet, self.bubble_rows, dokill=False)

            if collided:
                bullet.stop(bullet.rect.y)
                for bubble in collided:
                    if bubble.color == BLACK_COLOR:
                        self.music.play(3)
                        self.music.play_splash_animation()
                        self.draw_end_screen()
                        break
                    elif bullet.color == bubble.color: 
                        connected_bubbles = bubble.check_neighbors(self.bubble_rows)
                        for connected_bubble in connected_bubbles:
                            connected_bubble.kill()
                            bullet.kill()
                        self.music.play(2)
                        self.score += len(connected_bubbles)
                        break
                    elif bullet.color != bubble.color:
                        self.convert_bullet_to_bubble(bullet)
                        break
    def convert_bullet_to_bubble(self, bullet):
        """Convert a Bullet object into a Bubble object."""
        bubble = Bubble(bullet.rect.x, bullet.rect.y, bullet.color, self.speed)
        matching_neighbors = bubble.check_neighbors(self.bubble_rows)
        for neighbor in matching_neighbors:
            if neighbor.color == bubble.color:
                neighbor.kill()
            self.music.play(2)
            bubble.kill()
        else:
            grid_x, grid_y = self.snap_to_grid(bullet.rect.x, bullet.rect.y)
            bubble.rect.x, bubble.rect.y = grid_x, grid_y 
            bullet.stop(grid_y)
            self.bubble_rows.add(bubble)
        if bullet in self.bullets:
            self.bullets.remove(bullet)
    def snap_to_grid(self, x, y):
        """Snap the position to the closest grid position."""
        grid_size = 19  
        grid_x = round(x / grid_size) * grid_size 
        grid_y = round(y / grid_size) * grid_size
        return grid_x,grid_y 
    def check_end(self):
        """Check if too close to the bottom of the screen.""" 
        threshold_distance = 50 
        for bubble in self.bubble_rows:
            if bubble.rect.bottom >= self.screen.get_height() - threshold_distance:
                return True 
        return False   
       
    def update(self):
        """Update the screen"""
        self.screen.fill((135, 206, 250))
        self.screen.blit(self.background,(0,0)) 
        self.screen.blit(self.cloud,(100,0))
        self.shooter.update()
        self.shooter.blitme()
        if self.score > 30:
            self.next_level() 
        self.bullets.update()      
        for bullet in self.bullets:
            bullet.draw()
        self.score_text = self.font.render(f"Score: {self.score}",True,(255,0,0))
        self.screen.blit(self.score_text,(0,525))
        self.bubble_rows.update()
        self.bubble_rows.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(60)
    def reset_game(self):
        """Reset the game state for a new game.""" 
        self.score = 0 
        self.level =1
        self.final_score= 0
        self.bullets.empty() 
        self.bubble_rows.empty()  
        self.num_rows =10
        self.start_rows = -300
        self.bubble_rows = create_bubble_rows(self.num_rows, self.start_rows, self.speed)
        
    def next_level(self):
        """Handle leveling up."""
        self.level += 1
        self.speed += 0.01
        self.final_score += self.score
        self.score = 0
        self.screen.fill((0, 0, 0))
        message = f"Level {self.level}!"
        text = self.font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(2)  
        self.start_rows -= 100  
        self.num_rows += 3
        self.bubble_rows = create_bubble_rows(self.num_rows, self.start_rows, self.speed)
        self.bullets.empty()  
    def draw_end_screen(self):
        """Draw the end screen with the final score and options."""
        if self.final_score <1:
            self.final_score = self.score
        self.screen.fill((0, 0, 0)) 
        font = pygame.font.SysFont('Times New Roman', 60) 
        small_font = pygame.font.SysFont('Times New Roman', 30)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 100)) 
        self.screen.blit(game_over_text, game_over_rect)
        score_text = small_font.render(f"Final Score: {self.final_score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(score_text, score_rect)
        restart_text = small_font.render("Press R to Restart", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 100))
        self.screen.blit(restart_text, restart_rect) 
        quit_text = small_font.render("Press Q to Quit", True, (255, 255, 255)) 
        quit_rect = quit_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 150))
        self.screen.blit(quit_text, quit_rect) 
        self.music.play(4)
        pygame.display.flip()  
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()  
                        waiting = False
                        self.main()  
                    elif event.key == pygame.K_q:
                        pygame.quit() 
                        sys.exit()
        
    def opening_screen(self):
        """Handles opening message"""
        self.screen.fill((255,77,255))
        self.open_text = self.font.render("Welcome to the Bubble shooter game!"
                                          ,True, (0,0,0))
        self.play_t = self.font.render("Press 'p' to begin!", True, (0,0,0))
        self.screen.blit(self.open_text,(120,200))
        self.screen.blit(self.play_t,(260,250))
        pygame.display.flip()
        waiting = True
        while waiting: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.waiting = False
                        self.main()
                              
if __name__ == "__main__":
    bc = Game()
    bc.opening_screen() 