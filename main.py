# Pygame game template

import pygame
import sys
import config # Import the config module
import random
import draw # Import the drawing module

# Color constants (RGB)
WHITE = (200, 200, 200)
BLACK = (28, 28, 28)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
BLUE = (100, 100, 255)
BODY_INNER = (50, 155, 50)
BODY_OUTER = (0, 105, 0)

# Game window dimensions
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Game window title
TITLE = "Pygame Template"

# Frame rate (frames per second)
FPS = 8

def init_game():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Use constants from config

    pygame.display.set_caption(TITLE)
    return screen


def main():
    screen = init_game()
    clock = pygame.time.Clock() # Initialize the clock here
    running = True

    # Game Variables
    CELL_SIZE = 30
    direction = "Up"
    high_score = 120
    score = 0
    
    def move_apple():
        return [random.randint(0, (WINDOW_WIDTH // CELL_SIZE) - 2) * CELL_SIZE, random.randint(0, (WINDOW_WIDTH // CELL_SIZE) - 2) * CELL_SIZE]


    snake_pos = [[int(WINDOW_WIDTH // 2), int(WINDOW_HEIGHT // 2)]]
    for segment in range(2):
        snake_pos.append([int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2) + CELL_SIZE * (segment + 1)])

    # Establish Debris
    debris = []

    # Define Apple Position
    apple_position = move_apple()

    # Load Sounds
    sound1 = pygame.mixer.Sound("Sounds/coins.ogg")
    sound2 = pygame.mixer.Sound("Sounds/windowbreak.ogg")
    gameover = pygame.mixer.Sound("Sounds/gameover.ogg")
    scream = pygame.mixer.Sound("Sounds/screammale.ogg")

    # Set Volume for Sounds
    sound1.set_volume(1)
    sound2.set_volume(1)
    gameover.set_volume(1)
    scream.set_volume(1)

    # Load Music
    pygame.mixer.music.load("game_weak.ogg")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    while running:
        interior_offset = (CELL_SIZE * 0.1)
        screen.fill(BLACK) # Use color from config

        # Draw Apple
        draw.draw_rect(screen, RED, apple_position, CELL_SIZE, CELL_SIZE)
        draw.draw_rect(screen, draw.darken_color(RED, 0.7), [apple_position[0] + interior_offset, apple_position[1] + interior_offset], CELL_SIZE - interior_offset*2.6, CELL_SIZE - interior_offset*2.6)
        draw.draw_rect(screen, [255,200,200], [apple_position[0] + interior_offset * 1.666, apple_position[1] + interior_offset * 1.666], 5, 5)

        # Draw Snake
        for segment in snake_pos:
            draw.draw_rect(screen, GREEN, segment, CELL_SIZE, CELL_SIZE)
            interior_offset = (CELL_SIZE * 0.1)
            draw.draw_rect(screen, draw.darken_color(GREEN, 0.7), [segment[0] + interior_offset, segment[1] + interior_offset], CELL_SIZE - interior_offset*2, CELL_SIZE - interior_offset*2)
        
        # Draw Score
        draw.draw_text(screen, (50, 50), f"Score: {score}", 20, font_color=WHITE)

        # Check Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_w or event.key == pygame.K_UP and direction != "Down":
                    direction = "Up"
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT and direction != "Left":
                    direction = "Right"
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT and direction != "Right":
                    direction = "Left"
                elif event.key == pygame.K_w or event.key == pygame.K_DOWN and direction != "Up":
                    direction = "Down"

        movement = [0,0]
        new_segment = snake_pos[0].copy()

        if direction == "Up":
            movement[1] = -CELL_SIZE
        if direction == "Down":
            movement[1] = CELL_SIZE
        if direction == "Left":
            movement[0] = -CELL_SIZE
        if direction == "Right":
            movement[0] = CELL_SIZE

        new_segment[0] += movement[0]
        new_segment[1] += movement[1]

        snake_pos.insert(0, new_segment)
        print(f"snake_len {len(snake_pos)}, score {score}")
        if len(snake_pos) - 1 < score + 3:
            print("add")
        else:
            snake_pos.pop(-1)


        # Apple Collision
        if pygame.Rect(snake_pos[0][0], snake_pos[0][1], CELL_SIZE, CELL_SIZE).colliderect(pygame.Rect(apple_position[0], apple_position[1], CELL_SIZE, CELL_SIZE)):
            score += 1
            apple_position = move_apple()
            sound2.play()

        # Snake Collision
        segment_i = 0
        for segment in snake_pos:
                if segment_i > 0:
                    if snake_pos[0][0] == segment[0] and snake_pos[0][1] == segment[1]:
                        running = False
                else:
                    segment_i += 1
                    
        # Wall Collision
        if snake_pos[0][0] >= WINDOW_WIDTH or snake_pos[0][0] < 0 or snake_pos[0][1] >= WINDOW_HEIGHT or snake_pos[0][1] < 0:
            running = False                  


        pygame.display.flip()
        # Limit the frame rate to the specified frames per second (FPS)
        clock.tick(FPS) # Use the clock to control the frame rate

    pygame.quit()

    sys.exit()

if __name__ == "__main__":
    main()