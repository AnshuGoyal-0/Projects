import pygame
import sys
import random
import requests
from io import BytesIO

# Initialize Pygame
pygame.init()
pygame.font.init()

# Set up display
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("AI Flappy Bird - Anshu Goel Edition")

# Function to load image from URL
def load_image_from_url(url):
    response = requests.get(url)
    img = pygame.image.load(BytesIO(response.content)).convert_alpha()
    return img

# Load Images from the Web
BG_IMG = load_image_from_url("https://i.imgur.com/Qr44vG2.png")  # background
BASE_IMG = load_image_from_url("https://i.imgur.com/QsBwsjH.png")  # base
BIRD_IMG = load_image_from_url("https://i.imgur.com/lkJr1ac.png")  # bird
PIPE_IMG = load_image_from_url("https://i.imgur.com/wRHMZ3A.png")  # pipe

# Game Variables
GRAVITY = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
font = pygame.font.SysFont("Arial", 32)

# Rects
bird_rect = BIRD_IMG.get_rect(center=(50, SCREEN_HEIGHT//2))
base_x = 0

# Pipe generation
def create_pipe():
    height = random.randint(150, 350)
    bottom_pipe = PIPE_IMG.get_rect(midtop=(SCREEN_WIDTH + 100, height))
    top_pipe = PIPE_IMG.get_rect(midbottom=(SCREEN_WIDTH + 100, height - 150))
    return bottom_pipe, top_pipe

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

# Rotate bird
def rotate_bird(bird):
    return pygame.transform.rotozoom(bird, -bird_movement * 3, 1)

# Collision detection
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -50 or bird_rect.bottom >= SCREEN_HEIGHT - 100:
        return False
    return True

# Score display
def display_score(game_state):
    if game_state == 'main_game':
        score_surface = font.render(f'Score: {int(score)}', True, (255, 255, 255))
        SCREEN.blit(score_surface, (10, 10))
    if game_state == 'game_over':
        score_surface = font.render(f'Score: {int(score)}', True, (255, 255, 255))
        high_score_surface = font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        SCREEN.blit(score_surface, (10, 10))
        SCREEN.blit(high_score_surface, (10, 50))

# Base scrolling
def draw_base():
    SCREEN.blit(BASE_IMG, (base_x, SCREEN_HEIGHT - 100))
    SCREEN.blit(BASE_IMG, (base_x + SCREEN_WIDTH, SCREEN_HEIGHT - 100))

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    SCREEN.blit(BG_IMG, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (50, SCREEN_HEIGHT//2)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    if game_active:
        # Bird
        bird_movement += GRAVITY
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(BIRD_IMG)
        SCREEN.blit(rotated_bird, bird_rect)

        # Pipes
        pipe_list = [(p.move(-4, 0)) for p in pipe_list]
        for pipe in pipe_list:
            if pipe.bottom >= SCREEN_HEIGHT:
                SCREEN.blit(PIPE_IMG, pipe)
            else:
                flipped_pipe = pygame.transform.flip(PIPE_IMG, False, True)
                SCREEN.blit(flipped_pipe, pipe)

        # Collision
        game_active = check_collision(pipe_list)

        # Score
        for pipe in pipe_list:
            if pipe.centerx == bird_rect.centerx:
                score += 0.5
        display_score('main_game')
    else:
        if score > high_score:
            high_score = score
        display_score('game_over')

    # Base Scroll
    base_x -= 1
    if base_x <= -SCREEN_WIDTH:
        base_x = 0
    draw_base()

    pygame.display.update()
    clock.tick(120)
