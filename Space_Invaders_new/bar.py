import sys
import pygame

RED = (255,0,0)
YELLOW = (255,255,0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

class Bar(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        super().__init__()
        self.image = pygame.Surface((40,40))
        self.image.fill((200,30,30))
        self.rect = self.image.get_rect(center = (400,400))
        self.current_health = 200
        self.target_health = 500
        self.max_health = 1000
        self.health_bar_length = 400
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 30
        self.screen = screen
        self.randomize = False
        self.prob = 0
        self.x = x
        self.y = y

    def down(self,amount):
        if self.target_health > 0:
            self.target_health -= amount
        if self.target_health < 0:
            self.target_health = 0

    def up(self,amount):
        if self.target_health < self.max_health:
            self.target_health += amount
        if self.target_health > self.max_health:
            self.target_health = self.max_health

    def update(self):
        self.target_health = max(self.target_health - 0.5, 0)
        uwu = self.advanced_health()

    def advanced_health(self):
        transition_width = 0
        transition_color = RED

        if self.current_health < self.target_health:
            self.current_health += self.health_change_speed
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = RED

        if self.current_health > self.target_health:
            self.current_health -= self.health_change_speed 
            transition_width = int((self.target_health - self.current_health) / self.health_ratio)
            transition_color = RED
        
        health_bar_width = int(self.current_health / self.health_ratio)
        health_bar = pygame.Rect(self.x,self.y,health_bar_width,25)
        transition_bar = pygame.Rect(health_bar.right,self.y,transition_width,25)

        transition_color = GREEN if health_bar.right + transition_width > (self.health_bar_length // 2) + 15 else RED
        
        pygame.draw.rect(self.screen,transition_color,health_bar)
        pygame.draw.rect(self.screen,transition_color,transition_bar)	
        pygame.draw.rect(self.screen,(255,255,255),(self.x,self.y,self.health_bar_length,25),4)
        pygame.draw.rect(self.screen, WHITE, (10 + (self.health_bar_length // 2),self.y,10,25))

        self.randomize = True if transition_color == GREEN else False
        self.prob = transition_width / (self.health_bar_length // 2)



# pygame.init()
# screen = pygame.display.set_mode((800,800))
# clock = pygame.time.Clock()
# bar = pygame.sprite.GroupSingle(Bar())

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#             pygame.quit()
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP:
#                 bar.sprite.up(100)
#             if event.key == pygame.K_DOWN:
#                 bar.sprite.down(5)

#     screen.fill((30,30,30))
#     bar.draw(screen)
#     bar.update()
#     pygame.display.update()
#     clock.tick(60)