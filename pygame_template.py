from cmath import inf
import pygame
import random
from core.app_assets import AppAssets
from core.app_colors import AppColors
from core.app_config import AppConfig
from core.app_values_validator import validate_values

# Initialize basic pygame stuff
pygame.font.init()
WIN = pygame.display.set_mode((AppConfig.SCREEN_WIDTH, AppConfig.SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()


class Platform:
    def __init__(self, index):
        self.index = index
        
        # Scale platform assets to values provided by an AppConfig file
        self.image_left = pygame.transform.scale(AppAssets.left_platform_edge, (AppConfig.PLATFORM_PART_WIDTH, AppConfig.PLATFORM_HEIGHT))
        self.image_middle = pygame.transform.scale(AppAssets.middle_platform_part, (AppConfig.PLATFORM_PART_WIDTH, AppConfig.PLATFORM_HEIGHT))
        self.image_right = pygame.transform.scale(AppAssets.right_platform_edge, (AppConfig.PLATFORM_PART_WIDTH, AppConfig.PLATFORM_HEIGHT))
        
        self.length = random.randrange(AppConfig.MIN_PLATFORM_WIDTH, AppConfig.MAX_PLATFORM_WIDTH, AppConfig.PLATFORM_PART_WIDTH)
        self.middle_part_quantity = (self.length - 2 * AppConfig.PLATFORM_PART_WIDTH) // AppConfig.PLATFORM_PART_WIDTH
        self.pos = self.get_initial_pos()

        self.platform_rect = pygame.Rect(self.pos[0],self.pos[1], self.length,AppConfig.PLATFORM_HEIGHT)


    def get_initial_pos(self):
        _pos_y = (AppConfig.SCREEN_HEIGHT - AppConfig.PLATFORM_HEIGHT) - self.index * AppConfig.DISTANCE_BETWEEN_PLATFORMS
        return [random.randint(0, AppConfig.SCREEN_WIDTH - self.length), _pos_y]
    
    def draw_platform(self):
        WIN.blit(self.image_left, (self.pos[0], self.pos[1]))
        # Counts the position where the next middle part should be placed

        for index in range(1, self.middle_part_quantity + 1):
            WIN.blit(self.image_middle, (self.pos[0] + index * AppConfig.PLATFORM_PART_WIDTH, self.pos[1]))

        WIN.blit(self.image_right, (self.pos[0] + self.length - AppConfig.PLATFORM_PART_WIDTH, self.pos[1]))
        return pygame.Rect(self.pos[0],self.pos[1],self.length, AppConfig.PLATFORM_HEIGHT)
            

class Player:
    def __init__(self, starting_x, starting_y):
        self.start_pos = [starting_x, starting_y]
        self.width = AppConfig.PLAYER_WIDTH
        self.height = AppConfig.PLAYER_HEIGHT
        self.rect = pygame.Rect(starting_x, starting_y, self.width, self.height)
        self.image = AppAssets.player
        self.gravity = AppConfig.GRAVITY
        self.run_speed = 1
        self.jump_speed = 30
        self.run_acceleration = 0

        # Right :1 / Left :-1
        self.moving_direction = 0


    def get_pygame_rect(self):
        return pygame.rect(self.pos[0], self.pos[1], self.width, self.height)


class GameView:
    def __init__(self):
        self.is_running = True
        self.platforms = self.create_platforms(AppConfig.PLATFORM_PLATFORMS_TO_GENERATE)
        self.player = Player(starting_x=400, starting_y=800)
        self.background = pygame.transform.scale(AppAssets.background, (800,800))
        self.frame = pygame.transform.scale(AppAssets.frame, (40,800))
        self.background_speeed = 0
        self.height = -800
        self.game_loop()
        

    def game_loop(self):
        while self.is_running:
            CLOCK.tick(AppConfig.FPS)
            self.gravity()
            self.handle_events()
            self.handle_pressed_keys()
            self.redraw_window()
            self.Camera_movement()  
              
    def redraw_window(self):
        self.collision_detection(self.player.rect,self.platforms_rects)
        self.platforms_rects=[]
        WIN.fill(AppColors.WHITE)
        WIN.blit(self.background, (40,self.background_speeed))
        WIN.blit(self.frame, (0,self.background_speeed))
        WIN.blit(self.frame, (840,self.background_speeed))
        WIN.blit(self.background, (40,self.height + self.background_speeed))
        WIN.blit(self.frame, (0,self.height + self.background_speeed))
        WIN.blit(self.frame, (840,self.height + self.background_speeed))
        
        
        if self.background_speeed >= -self.height:
            self.background_speeed = 0
        
        for platform in self.platforms:
            platform.draw_platform()
            self.platforms_rects.append(platform.draw_platform())

        WIN.blit(self.player.image, (self.player.rect.x, self.player.rect.y))
        pygame.display.update()


    def collision_detection(self,player_rect, platforms_rects ):
        for i in range(len(platforms_rects)):
            if player_rect.colliderect(platforms_rects[i]):
                if abs(platforms_rects[i].top - player_rect.bottom) < self.player.gravity:
                    self.player.gravity = 0
                    player_rect.y = platforms_rects[i].y - self.player.height


    # Gravity
    def gravity(self):
        previous_y = self.player.rect.y
        if self.player.rect.y < AppConfig.SCREEN_HEIGHT - AppConfig.PLAYER_HEIGHT:
            self.player.rect.y += self.player.gravity

        else:
            self.player.rect.y = AppConfig.SCREEN_HEIGHT - AppConfig.PLAYER_HEIGHT

        if previous_y != self.player.rect.y:
            self.player.gravity += 1

        else:
            self.player.gravity = AppConfig.GRAVITY


    def handle_events(self):
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                self.is_running = False
                
                
    def create_platforms(self, number_of_latforms):
        _platforms = []
        for platform_index in range(number_of_latforms):
            _platforms.append(Platform(platform_index))
        return _platforms
      

    def handle_pressed_keys(self):
        pressed_keys = pygame.key.get_pressed()
        
        # R/L moves + acceleration
        if pressed_keys[pygame.K_RIGHT]:

            if self.player.rect.x + self.player.run_speed + self.player.run_acceleration > AppConfig.SCREEN_WIDTH - AppConfig.PLAYER_WIDTH:
                self.player.rect.x = AppConfig.SCREEN_WIDTH - AppConfig.PLAYER_WIDTH
                self.player.run_acceleration = 0
            else:
                self.player.rect.x += self.player.run_speed + self.player.run_acceleration

            if self.player.moving_direction == 1:
                self.player.run_acceleration += 0.2
            else:
                self.player.run_acceleration = 0
            self.player.moving_direction = 1

        elif pressed_keys[pygame.K_LEFT]:

            if self.player.rect.x - (self.player.run_speed + self.player.run_acceleration) < 0:
                self.player.rect.x = 0
                self.player.run_acceleration = 0
            else:
                self.player.rect.x -= self.player.run_speed + self.player.run_acceleration
            if self.player.moving_direction == -1:
                self.player.run_acceleration += 0.2
            else:
                self.player.run_acceleration = 0

            self.player.moving_direction = -1

        # Jumping
        if pressed_keys[pygame.K_SPACE]:
            self.player.rect.y += -self.player.jump_speed

        # Acceleretion = 0 when player stoped
        if (pressed_keys[pygame.K_RIGHT] == False and self.player.moving_direction == 1) or (
                pressed_keys[pygame.K_LEFT] == False and self.player.moving_direction == -1):
            self.player.run_acceleration = 0
            #self.platforms.pos = 0 #stop platformy i h
    
    def Camera_movement(self):
        actual_height = self.player.rect.y
        
        if actual_height <  AppConfig.CAMERA_START_GAME:
            for x in range(15):                                             
                self.platforms[x].pos[1] += AppConfig.CAMERA_SPEED
            AppConfig.CAMERA_START_GAME = inf
            #self.player.rect.y += AppConfig.CAMERA_SPEED
            self.background_speeed += AppConfig.CAMERA_SPEED

        if actual_height < AppConfig.CAMERA_NEXT_HEIGHT:                
            self.player.jump_speed = 0
            #self.platforms.append(Platform(AppConfig.PLATFORM_NUMBER+1))   <----- tyu wlozyc generacje platform(ta zakomentowana nie dzialac!)
            #AppConfig.PLATFORM_NUMBER += 1
            self.background_speeed += 40
            for x in range(15):
                self.platforms[x].pos[1] += 40   

        else:   
            self.player.jump_speed = 40    
   
        
def main():
    validate_values()
    GameView()


if __name__ == "__main__":
    main()
