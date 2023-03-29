#!/usr/bin/python3

# Import the pygame module

import pygame, random, time

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (

    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Initialize pygame
pygame.init()
pygame.mixer.init()

PY_DIR = "/home/josiah/py/"
explode = pygame.mixer.Sound("%sexplosion.ogg" % PY_DIR)

BLACK = (000,000,000)
timer = pygame.time.Clock()
# 0 = homescreen, 1 = gameplay, 2 = end screen.
mode = 0

# adding functions for dealing with high scores
def read_high_score():
    hsf = open(r"%shs.txt" % PY_DIR, "r")
    hs = int(hsf.read())
    hsf.close()
    return hs

def check_and_write_high_score(elapsed, hs):
    if elapsed > hs:
        hsf = open(r"%shs.txt" % PY_DIR, "w")
        hsf.write(str(elapsed))
        hsf.close()
        print("New high score: ", str(elapsed))
    else:
        print("Your score: ", str(elapsed), " High score: ", str(hs))
    time.sleep(3)

# Define a player object by extending pygame.sprite.Sprite
# The surface drawn on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("%sjet.gif" % PY_DIR).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    def boom(self):
        self.surf = pygame.image.load("%spixel_explosion.png" % PY_DIR).convert_alpha()
        pygame.mixer.music.stop()
        explode.play()
            
# Define the enemy object by extending pygame.sprite.Sprite
# The surface you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("%sbullet.png" % PY_DIR).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(15, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

def setup_Gameplay():
    global player, start, hs
    # Load music for gameplay
    pygame.mixer.music.load("%sjetengine-loop.ogg" % PY_DIR)
    pygame.mixer.music.play(-1)
    # Instantiate player
    player = Player()
    all_sprites.add(player)
    # Set timer for ADDENEMY event
    pygame.time.set_timer(ADDENEMY, 550)
    # Set a timer for the game score
    start = time.time()
    # Read high score
    hs = read_high_score()

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Variable to keep the main loop running
running = True

setup_Gameplay()

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, check the score for high score, stop the loop.
            if event.key == K_ESCAPE:
                check_and_write_high_score(elapsed, hs)
                running = False
        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            check_and_write_high_score(elapsed, hs)
            running = False
            
        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create the new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()
    
    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
    
    # Update enemy position
    enemies.update()

    # Fill the screen with the sky
    screen.fill((137, 240, 255))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
        
    # create your score
    elapsed = int(time.time() - start)
    draw_string = "Your Score: " + str(elapsed) + "    VS.   High Score: " + str(hs)
    font = pygame.font.SysFont("score", 24)
    text = font.render(draw_string, True, BLACK)
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text, text_rect)
        
    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        player.boom()
        screen.blit(player.surf, player.rect)
        pygame.display.flip()
        # Check for high score
        check_and_write_high_score(elapsed, hs)
        running = False
        print("you got shot!")
        
    

#   pygame.display.update()
    
    # Update the display
    pygame.display.flip()
    
    # Ensure program maintains a rate of 30 frames per second
    clock.tick(50)
# now you can play the game 
