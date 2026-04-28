import pygame
import random, math
from collections import deque
# Bubble settings
BUBBLE_RADIUS = 19
SPACING = 0  
BUBBLE_COLORS = [
    (255, 0, 0),   # Red
    (0, 255, 0),   # Green
    (0, 0, 255),   # Blue
    (255, 255, 0)  # Yellow
]
BLACK_COLOR = (0, 0, 0)  # Black bubble


bubble_counter = 0


class Bubble(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed):
        super().__init__()
        self.color = color
        self.image = pygame.Surface((BUBBLE_RADIUS * 2, BUBBLE_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (BUBBLE_RADIUS, BUBBLE_RADIUS), BUBBLE_RADIUS)
        self.rect = self.image.get_rect(center=(x, y))
        self.float_y = float(y)
        self.speed = speed
    def update (self):
        self.float_y += self.speed  
        self.rect.y = int(self.float_y)        
   
        if self.rect.top > 600:
            self.float_y = -2 * BUBBLE_RADIUS 
    def get_rand_color():
        return random.choice(BUBBLE_COLORS)

    def check_neighbors(self, bubble_rows):
        """explore neighbors using floodfill"""
        to_explore = [self] 
        visited = set()  
        matching_bubbles = []  

        while to_explore:
            current_bubble = to_explore.pop()
            if current_bubble not in visited:
                visited.add(current_bubble)
                matching_bubbles.append(current_bubble)

                for other_bubble in bubble_rows:
                    if (
                        other_bubble not in visited 
                        and other_bubble.color == self.color  
                        and self.are_neighbors(other_bubble)  
                    ):
                        to_explore.append(other_bubble)

        return matching_bubbles

    def are_neighbors(self, other_bubble):
        """Check if two bubbles are neighbors based on their distance."""
        distance = math.sqrt(
        (self.rect.centerx - other_bubble.rect.centerx) ** 2 +
        (self.rect.centery - other_bubble.rect.centery) ** 2
        )
        return distance <= 2 * BUBBLE_RADIUS
def create_bubble_row(y_position,speed, bubbles_per_row=20):
    """Create a row of bubbles with one random black bubble per group of 50."""
    global bubble_counter
    bubbles = pygame.sprite.Group()
    start_x = 20

    
    if bubble_counter %50 == 0:  
        black_bubble_index = random.randint(0, 49)
    else:
        black_bubble_index = None

    for i in range(bubbles_per_row):
        x = start_x + i * (2 * BUBBLE_RADIUS + SPACING)

        if bubble_counter % 50 == black_bubble_index:
            color = BLACK_COLOR
        else:
            color = random.choice(BUBBLE_COLORS)

        bubble = Bubble(x, y_position, color, speed)
        bubbles.add(bubble)

        bubble_counter += 1  

    return bubbles
def get_float_neighbors(bubble, bubble_group):
        """Find all valid neighbors of a bubble."""
    # Directions to check for neighbors (8 directions: N, S, E, W, NE, NW, SE, SW)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        neighbors = []
        for dx, dy in directions:
            neighbor_pos = (bubble.rect.x + dx, bubble.rect.y + dy)
           
            for other_bubble in bubble_group:
                if other_bubble.rect.x == neighbor_pos[0] and other_bubble.rect.y == neighbor_pos[1]:
                    neighbors.append(other_bubble)
        return neighbors
def find_connected_clusters(bubble_group):
        """Find connected clusters of bubbles using BFS."""
        visited = set()
        clusters = []
        for bubble in bubble_group:
            if bubble not in visited:
                queue = deque([bubble])
                connected_bubble_set = set()

                while queue:
                    current_bubble = queue.popleft()
                    if current_bubble in visited:
                        continue
                    visited.add(current_bubble)
                    connected_bubble_set.add(current_bubble)
                    neighbors = get_float_neighbors(current_bubble, bubble_group)
                    for neighbor in neighbors:
                        if neighbor not in visited:
                            queue.append(neighbor)
                clusters.append(connected_bubble_set)

        return clusters
def remove_isolated_bubbles(bubble_group):
    """Remove bubbles that aren't part of any connected cluster."""
    bubble_set = set(bubble_group)
    clusters = find_connected_clusters(bubble_set)  
    connected_bubbles = set()
    for cluster in clusters:
        connected_bubbles.update(cluster)

    isolated_bubbles = bubble_set - connected_bubbles
    for bubble in isolated_bubbles:
        bubble.kill() 

def create_bubble_rows(num_rows, start_y, speed, bubbles_per_row = 20):
    """Create multiple rows of bubbles starting at a given Y position."""
    rows = pygame.sprite.Group()
    for row in range(num_rows):
        y_position = start_y + row * (2 * BUBBLE_RADIUS + SPACING)
        bubbles = create_bubble_row(y_position,speed,bubbles_per_row)
        rows.add(bubbles)
    return rows

class Bullet(pygame.sprite.Sprite):
    """Class to manage the bullets"""
    def __init__(self, game,angle,bullet_color):
        super().__init__()
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.radius = BUBBLE_RADIUS 
        self.color = bullet_color
        self.image = pygame.Surface((self.radius*2,self.radius*2), pygame.SRCALPHA)
        self.rect =pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect.midbottom =game.shooter.rect.midtop
        self.angle = math.radians(angle)
        self.bullet_speed = 5
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.dx = math.cos(self.angle) * self.bullet_speed
        self.dy = math.sin(self.angle) * self.bullet_speed
        self.stuck = False
        self.direction_changed = False
        self.bubble_speed = game.speed
    def stop(self, collision):
        """to handle the bullet stopping and adding to the bubble row"""
        self.dx = 0 
        self.stuck = True  
        self.y = collision  
        self.x, self.y = self.rect.x, self.rect.y 
        self.update() 
        
    def update(self):
        """Move the bullet upwards"""
        if not self.stuck:
            self.x += self.dx
            self.y -= self.dy
            if self.rect.left <= 0:
                self.dx = abs(self.dx)  # Ensure moving right
                self.rect.left = 1 
            elif self.rect.right >= self.screen_rect.width:
                self.dx = -abs(self.dx)  # Ensure moving left
                self.rect.right = self.screen_rect.width - 1  
        
            self.x += self.dx  
        else:
            self.y += self.bubble_speed

        self.rect.x = self.x
        self.rect.y = self.y


    def draw(self):
        """Draw the bullet as a circle"""
        self.screen.blit(self.image, self.rect)
    