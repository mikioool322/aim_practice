import pygame

class Target:
    def __init__(self, x, y, radius=50, shrink_speed=0.2):
        self.x = x
        self.y = y
        self.radius = radius
        self.shrink_speed = shrink_speed
        
    def update(self):
        self.radius -= self.shrink_speed
    
    def render(self, screen, color = (200, 0, 0)):
        if self.radius > 0:
            pygame.draw.circle(screen, color, (self.x, self.y), int(self.radius))
    
    def is_clicked(self, mouse_pos):
        distance = ((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2) ** 0.5
        return distance <= self.radius
    
    def should_disappear(self):
        return self.radius <= 0