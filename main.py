import pygame, sys, random

class Floor():
    def __init__(self):
        self.floor_surface = pygame.image.load('assets/base.png').convert()
        self.floor_x = 0

    def draw_floor(self):
        screen.blit(self.floor_surface, (self.floor_x, 450))
        screen.blit(self.floor_surface, (self.floor_x+screen_width, 450))
        if self.floor_x <= -screen_width:
            self.floor_x = 0

class Bird():
    def __init__(self):
        self.bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
        self.bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
        self.bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
        self.bird_frames = [self.bird_upflap, self.bird_midflap, self.bird_downflap]
        self.bird_index = 0
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center = (screen_width / 4, screen_height / 2))
        self.bird_speed = 0
        self.gravity = 0.25

    def draw_bird(self):
        screen.blit(self.rotated_bird, self.bird_rect)

    def bird_jump(self):
        self.bird_speed = 0
        self.bird_speed -= 6

    def bird_rotate(self):
        self.rotated_bird = pygame.transform.rotozoom(self.bird_surface, self.bird_speed * -3,1)

    def bird_animation(self):
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center = (screen_width / 4, self.bird_rect.centery))

class Pipe():
    def __init__(self):
        self.pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
        self.pipe_list = []
        self.pipe_height = [200,300,400]

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe_surface.get_rect(topleft = (screen_width, random_pipe_pos))
        top_pipe = self.pipe_surface.get_rect(bottomleft = (screen_width, random_pipe_pos - 150))
        return bottom_pipe,top_pipe

    def move_pipe(self):
        for pp in self.pipe_list:
            pp.centerx -= 2

    def draw_pipe(self):
        for pp in self.pipe_list:
            if pp.bottom >= screen_height:
                screen.blit(self.pipe_surface, pp)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                screen.blit(flip_pipe, pp)

    def remove_pipe(self):
        for i in self.pipe_list:
            if i.centerx < -600:
                self.pipe_list.remove(i)

class Main():
    def __init__(self):
        self.bg_surface = pygame.image.load('assets/background-day.png').convert()
        self.floor = Floor()
        self.bird = Bird()
        self.pipe = Pipe()
        self.game_active = True
        self.score = 0
        f = open('High_score.txt')
        self.high_score = int(f.read())
        f.close()
        self.game_font = pygame.font.Font('04B_19.ttf', 20)
        self.game_state = 'main_game'

    def draw_main_surfaces(self):
        screen.blit(self.bg_surface, (0, 0))
        self.floor.floor_x -= 2
        self.floor.draw_floor()

    def draw_surfaces(self):
        self.bird.bird_speed += self.bird.gravity
        self.bird.bird_rect.centery += self.bird.bird_speed
        self.bird.bird_rotate()
        self.bird.draw_bird()
        self.pipe.move_pipe()
        self.pipe.draw_pipe()

    def check_collision(self):
        for pp in self.pipe.pipe_list:
            if self.bird.bird_rect.colliderect(pp):
                self.game_active = False
                death_sound.play()
        if self.bird.bird_rect.top <= -50:
            self.game_active = False
            death_sound.play()
        if self.bird.bird_rect.bottom >= 450:
            self.game_active = False
            death_sound.play()

    def reset(self):
        self.pipe.pipe_list.clear()
        self.bird.bird_rect.center = (screen_width / 4, screen_height / 2)
        self.bird.bird_speed = -6
        self.score = 0
        self.game_state = 'main_game'

    def score_display(self):
        if self.game_state == 'main_game':
            score_surface = self.game_font.render(f"Score: {int(self.score)}", True, (255,255,255))
            score_rect = score_surface.get_rect(center = (screen_width/2, 50))
            screen.blit(score_surface,score_rect)

        if self.game_state == 'game_over':
            score_surface = self.game_font.render(f"Score: {int(self.score)}", True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(screen_width / 2, 50))
            screen.blit(score_surface, score_rect)

            high_score_surface = self.game_font.render(f"High score: {int(self.high_score)}", True, (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(center=(screen_width / 2, 400))
            screen.blit(high_score_surface, high_score_rect)

    def score_update(self):
        for i in self.pipe.pipe_list:
            if i.centerx == self.bird.bird_rect.centerx:
                self.score += 0.5
                score_sound.play()

        if self.high_score < self.score:
            self.high_score = self.score
            f = open('High_score.txt', 'w')
            f.write(str(int(self.high_score)))
            f.close()

#initializing pygame
#pygame.mixer.pre_init(frequency = 44100, size = 8, channels = 2, buffer = 1024)
pygame.init()
clock = pygame.time.Clock()

#setting up the screen
screen_height = 512
screen_width = 288
screen = pygame.display.set_mode((screen_width,screen_height))

#surfaces and rects
main_game = Main()
BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,2400)
game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (screen_width / 2, screen_height / 2))
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_die.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

while True:
    #handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                main_game.bird.bird_jump()
                flap_sound.play()
            if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and not(main_game.game_active):
                main_game.game_active = True
                main_game.reset()
        if event.type == SPAWNPIPE:
            main_game.pipe.pipe_list.extend(main_game.pipe.create_pipe())
        if event.type == BIRDFLAP:
            if main_game.bird.bird_index < 2:
                main_game.bird.bird_index += 1
            else:
                main_game.bird.bird_index = 0
            main_game.bird.bird_animation()

    #graphics
    main_game.draw_main_surfaces()
    if main_game.game_active:
        main_game.draw_surfaces()
        main_game.score_display()
        main_game.check_collision()
        main_game.score_update()
        main_game.score_display()
        main_game.pipe.remove_pipe()
    else:
        screen.blit(game_over_surface,game_over_rect)
        main_game.game_state = 'game_over'
        main_game.score_update()
        main_game.score_display()

    #updating screen
    pygame.display.update()
    clock.tick(60)