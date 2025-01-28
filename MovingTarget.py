import Target
import random

class MovingTarget(Target.Target):
    def __init__(self, x, y, screen_width, screen_height, radius = 50, speed = 8):
        super().__init__(x, y) 
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_speed = 2 * speed
        self.min_radius = radius * 0.75
        self.max_radius = radius * 1.5
        self.speed_x = random.choice([-1,1]) * speed
        self.speed_y = random.choice([-1,1]) * speed
        self.shrink = False
        self.grow = True
        
    def is_hovered(self, mouse_pos):
        distance = ((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2) ** 0.5
        return distance <= self.radius
        
    def update(self):
        self.speed_x += random.uniform(-1, 1)
        self.speed_y += random.uniform(-1, 1)
        
        self.speed_x = max(min(self.speed_x, self.max_speed), -self.max_speed)
        self.speed_y = max(min(self.speed_y, self.max_speed), -self.max_speed)
        
        if self.grow:
            self.radius += random.uniform(0.1, 0.5)
        if self.shrink:
            self.radius -= random.uniform(0.1, 0.5)

        if self.radius > self.max_radius:  # Example max radius
            self.grow = False
            self.shrink = True

        if self.radius < self.min_radius:  # Example min radius
            self.grow = True
            self.shrink = False
        
        if random.random() < 0.0001:
            self.speed_x *= -1
        if random.random() < 0.0001:
            self.speed_y *= -1

        
        self.x += self.speed_x
        self.y += self.speed_y
        
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.speed_x *= -1
        if self.x + self.radius >= self.screen_width:
            self.x = self.screen_width - self.radius
            self.speed_x *= -1
        if self.y - self.radius <= 100:
            self.y = 100 + self.radius
            self.speed_y *= -1
        if self.y + self.radius >= self.screen_height:
            self.y = self.screen_height - self.radius
            self.speed_y *= -1
        
        
        