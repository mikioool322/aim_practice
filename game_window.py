import pygame
import Target
import random
import time
import MovingTarget
import Timer

class GameWindow:
    def __init__(self, width, height, title, fps):
        self.width = width
        self.height = height
        self.title = title
        self.running = True
        self.fps = fps
        
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont(['Terminal','Arial'], 36)
        pygame.display.set_caption(self.title)
        
        self.bg_color = (0,0,0)
        
        self.targets = []
        self.moving_target = None
        self.total_targets = 0
        self.total_correct_clicks = 0
        self.total_clicks = 0
        self.accuracy = 0.00
        self.target_spawn_time = 0.5
        self.last_target_time = time.time()
        
        self.moving_target = None
        self.moving_target_correct_timer = None
        self.moving_target_total_timer = None
        
        self.mode = 'menu'
        self.last_mode = None
        
        self.correct_timer = Timer.EventTimer()
        self.total_timer = Timer.EventTimer()
    
    def reset(self):
        self.targets = []
        self.moving_target = None
        self.total_targets = 0
        self.total_correct_clicks = 0
        self.total_clicks = 0
        self.accuracy = 0.00
        self.mode = 'menu'
        
        self.moving_target = None
        self.moving_target_correct_timer = None
        self.moving_target_miss_timer = None
        
        self.correct_timer.reset()
        self.total_timer.reset()
        
    def handle_events(self):
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.mode != 'menu' and self.mode != 'escape_menu':
                    self.total_timer.stop()                 
                    self.last_mode = self.mode
                    self.mode = 'escape_menu'
                    print(self.mode)
                elif event.key == pygame.K_ESCAPE and self.mode == 'escape_menu':
                    self.total_timer.start_timer()
                    self.mode = self.last_mode
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.mode == 'game':
                    self.check_target_click(event.pos)
                elif self.mode == 'menu':
                    self.check_menu_click(event.pos)
                elif self.mode == 'escape_menu':
                    self.check_escape_menu_click(event.pos)
                    
    def check_menu_click(self, mouse_pos):
        play_button_rect = pygame.Rect(self.width // 2 - 100, self.height // 2 - 50, 250, 50)
        moving_targets_button_rect = pygame.Rect(self.width // 2 - 100, self.height // 2 + 10, 250, 50)
        
        if play_button_rect.collidepoint(mouse_pos):
            self.mode = 'game'
            self.total_timer.start_timer()
        elif moving_targets_button_rect.collidepoint(mouse_pos):
            self.mode = "moving_target"
            self.total_timer.start_timer()
    
    def check_escape_menu_click(self, mouse_pos):
        resume_button = pygame.Rect(self.width // 2 - 100, self.height // 2 - 50, 250, 50)
        back_to_menu_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 10, 250, 50)
        quit_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 60, 250, 50)
        
        if resume_button.collidepoint(mouse_pos):
            self.mode = self.last_mode
            
        elif back_to_menu_button.collidepoint(mouse_pos):
            self.reset()
            self.mode = 'menu'
            
        elif quit_button.collidepoint(mouse_pos):
            self.running = False
                
    def check_target_click(self, mouse_pos):
        for target in self.targets[:]:
            if target.is_clicked(mouse_pos):
                self.targets.remove(target)
                self.total_correct_clicks += 1
        self.total_clicks += 1
    
    def render_menu(self):
        self.screen.fill(self.bg_color)
        
        play_button_rect = pygame.Rect(self.width // 2 - 100, self.height // 2 - 50, 200, 50)
        pygame.draw.rect(self.screen, (0,200,0), play_button_rect)
        
        moving_targets_button_rect = pygame.Rect(self.width // 2 - 100, self.height // 2 + 10, 200, 50)
        pygame.draw.rect(self.screen, (0, 0, 200), moving_targets_button_rect)
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render("Play", True, (255,255,255))
        text_rect = text_surface.get_rect(center = play_button_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        moving_targets_text_surface = font.render("Moving Target", True, (255, 255, 255))
        moving_targets_text_rect = moving_targets_text_surface.get_rect(center=moving_targets_button_rect.center)
        self.screen.blit(moving_targets_text_surface, moving_targets_text_rect)
        
        pygame.display.flip()
    
    def render_escape_menu(self):
        self.screen.fill(self.bg_color)
        
        resume_button = pygame.Rect(self.width // 2 - 100, self.height // 2 - 50, 250, 50)
        pygame.draw.rect(self.screen, (0,0, 200), resume_button)
        
        back_to_menu_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 10, 250, 50)
        pygame.draw.rect(self.screen, (0,0, 200), back_to_menu_button)
        
        quit_button = pygame.Rect(self.width // 2 - 100, self.height // 2 + 70, 250, 50)
        pygame.draw.rect(self.screen, (0,0, 200), quit_button)
        
        resume_button_surface = self.font.render("Resume", True, (255,255,255))
        resume_button_rect = resume_button_surface.get_rect(center = resume_button.center)
        self.screen.blit(resume_button_surface, resume_button_rect)
        
        back_menu_surface = self.font.render("Back to menu", True, (255,255,255))
        back_menu_rect = back_menu_surface.get_rect(center = back_to_menu_button.center)
        self.screen.blit(back_menu_surface, back_menu_rect)
        
        quit_button_surface = self.font.render("Quit", True, (255,255,255))
        quit_button_rect = quit_button_surface.get_rect(center = quit_button.center)
        self.screen.blit(quit_button_surface, quit_button_rect)
                
        pygame.display.flip()
        
    def render_game(self):
        self.screen.fill(self.bg_color)
        
        total_targets_info = pygame.Rect(self.width // 4 - 25, self.height//90, 50,50)
        pygame.draw.rect(self.screen, (0, 0, 0), total_targets_info)
        
        accuracy_info = pygame.Rect(self.width - (self.width // 4 - 25) , self.height//90, 50,50)
        pygame.draw.rect(self.screen, (0, 0, 0), accuracy_info)
        
        font_targets = pygame.font.Font(None, 36)
        targets_text_surface = font_targets.render("Total targets: "+str(self.total_targets), True, (255,255,255))
        target_text_rect = targets_text_surface.get_rect(center = total_targets_info.center)
        self.screen.blit(targets_text_surface, target_text_rect)
        
        font_accuracy = pygame.font.Font(None, 36)
        font_text_surface = font_accuracy.render("Accuracy: "+str(round(self.accuracy, 1)), True, (255,255,255))
        text_rect = font_text_surface.get_rect(center = accuracy_info.center)
        self.screen.blit(font_text_surface, text_rect)
        
        for target in self.targets:
            target.render(self.screen)
            
        pygame.display.flip()
        
    def render_moving_target(self):
        self.screen.fill(self.bg_color)
        
        timer_info = pygame.Rect(self.width //2, self.height//90, 50, 50)
        pygame.draw.rect(self.screen, (0,0,0), timer_info)
        
        timer_info_surface = self.font.render("Uptime: "+str(round(self.correct_timer.get_active_time()/ self.total_timer.get_active_time()*100, 1))+"%", True, (255,255,255))
        timer_info_rect = timer_info_surface.get_rect(center = timer_info.center)
        self.screen.blit(timer_info_surface, timer_info_rect)
        
        if self.moving_target.is_hovered(pygame.mouse.get_pos()):
            color = (0,200,0)
            self.correct_timer.start_timer()
        else:
            color = (200,0,0)
            self.correct_timer.stop()
            
        self.moving_target.render(self.screen, color)
        
        pygame.display.flip()
        
    def calc_accuracy(self):
        if self.total_clicks > 0:
            self.accuracy = self.total_correct_clicks / self.total_clicks * 100
                
    def update(self):
        if self.mode == 'game':
            for target in self.targets:
                target.update()
                
                if target.should_disappear():
                    self.total_clicks += 1
            
            current_time = time.time()
            
            self.targets = [target for target in self.targets if not target.should_disappear()]
            
            if current_time - self.last_target_time >= self.target_spawn_time or len(self.targets) == 0:
                self.targets.append(Target.Target(random.randint(50, self.width - 50), random.randint(self.height//10 + 50, self.height -50)))
                self.total_targets += 1
                self.last_target_time = current_time
            
            self.calc_accuracy()  
        
        elif self.mode == 'moving_target':
            if self.moving_target == None:
                self.moving_target = MovingTarget.MovingTarget(random.randint(50, self.width - 50), random.randint(self.height//10 + 50, self.height -50), self.width, self.height)
            else:
                self.moving_target.update()
               
    def render(self):
        if self.mode == 'game':
            self.render_game()
        elif self.mode == "moving_target":
            self.render_moving_target()
        elif self.mode == 'menu':
            self.render_menu()
        elif self.mode == 'escape_menu':
            self.render_escape_menu()
        
    
    def run(self):
        while self.running:
            self.clock.tick(self.fps)
            self.handle_events()
            self.update()
            self.render()
            
        pygame.quit()
    
if __name__ == '__main__':
    window = GameWindow(1920, 1080, 'aim practice', 60)
    window.run()
        