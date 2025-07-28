
import pygame
import random
import os

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# --- Asset paths ---
# Get the absolute path of the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

PLAYER_IMG = os.path.join(script_dir, "player.png")
ENEMY_IMG = os.path.join(script_dir, "sandal.png")
BACKGROUND_IMG = os.path.join(script_dir, "background.png")
MUSIC_FILE = os.path.join(script_dir, "music.mp3")
CRASH_SOUND_FILE = os.path.join(script_dir, "explosion.wav")


# --- Game Classes ---

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load(PLAYER_IMG).convert_alpha()
            self.image = pygame.transform.scale(self.image, (50, 100))
        except pygame.error:
            self.image = pygame.Surface([50, 100])
            self.image.fill(RED)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -8
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 8
        
        self.rect.x += self.speed_x
        
        # Keep player on the screen
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load(ENEMY_IMG).convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 60))
        except pygame.error:
            self.image = pygame.Surface([30, 40])
            self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(4, 8)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(4, 8)

# --- Game Initialization ---
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sandal Racer")
clock = pygame.time.Clock()

# --- Load Assets ---
try:
    background = pygame.image.load(BACKGROUND_IMG).convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    background_rect = background.get_rect()
    crash_sound = pygame.mixer.Sound(CRASH_SOUND_FILE)
    pygame.mixer.music.load(MUSIC_FILE)
    pygame.mixer.music.set_volume(0.4)
    assets_loaded = True
except pygame.error as e:
    print(f"Warning: Could not load one or more assets. Game will run with placeholders. Error: {e}")
    assets_loaded = False


# --- Functions ---
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def show_go_screen():
    screen.fill(BLACK)
    if assets_loaded:
        screen.blit(background, background_rect)
    draw_text(screen, "Sandal Racer!", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    draw_text(screen, "Arrow keys to move, dodge the sandals!", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    draw_text(screen, "Press any key to begin", 18, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYUP:
                waiting = False

# --- Game Loop ---
game_over = True
running = True
if assets_loaded:
    pygame.mixer.music.play(loops=-1)

while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            e = Enemy()
            all_sprites.add(e)
            enemies.add(e)
        score = 0

    # Keep loop running at the right speed
    clock.tick(FPS)
    
    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()
    score += 1 # Score increases with time survived

    # Check for collisions
    hits = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_rect_ratio(0.7))
    if hits:
        if assets_loaded:
            crash_sound.play()
        game_over = True

    # Draw / render
    screen.fill(BLACK)
    if assets_loaded:
        screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 30, SCREEN_WIDTH / 2, 10)
    
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
