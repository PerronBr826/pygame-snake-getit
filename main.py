# Pygame game template

import pygame
import sys
import config # Import the config module
import random
import draw # Import the drawing module

# Highscore (fake)

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
TITLE = "SNAKE IV"

# Frame rate (frames per second)
fps = 60

def init_game():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # Use constants from config

    pygame.display.set_caption(TITLE)
    return screen

def main():
    run_menu()

def run_menu():
    high_score = 10
    current_title_pose = 0
    tick = 0

    clock = pygame.time.Clock() # Initialize the clock here
    running = True
    
    # Menu Button Dimensions
    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 50


    buttons = [{"text" : "Play", "hover" : 0, "color" : (55,255,55), "purpose" : "play"}, 
               {"text" : "Quit", "hover" : 0, "color" : (255,55,55), "purpose" : "close"},
               ]

    screen = init_game()
    scream = pygame.mixer.Sound("Sounds/screammale.ogg")
    scream.set_volume(30)
    
    try:
        pygame.mixer.music.load("game_weak.ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except:
        print("Music did not load. D:")

    while running:
        tick += 1
        fps = 60
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button_i = 0
                for button in buttons:
                    button_x = WINDOW_WIDTH // 2
                    button_y = WINDOW_HEIGHT // 2 + (65 * button_i)
                    faux_buttonx = BUTTON_WIDTH + button["hover"]
                    faux_buttony = BUTTON_HEIGHT + button["hover"] / 2

                    button_box = pygame.Rect(button_x - faux_buttonx / 2, button_y - faux_buttony / 2, faux_buttonx, faux_buttony)

                    if button_box.collidepoint(event.pos):
                        button["hover"] = 0
                        if button["purpose"] == "close":
                            running = False
                        if button["purpose"] == "play":
                            high_score = run_snake_game(high_score)

                    button_i += 1

            
        screen.fill((0,0,0)) # DO NOT Use color from config

        mouse_x, mouse_y = pygame.mouse.get_pos()
        button_i = 0

        #if current_title_dir == 1:
            
        #else:

        draw.draw_text(screen, ((WINDOW_WIDTH // 2 - 85), WINDOW_HEIGHT * 0.4), f"High Score: {high_score}", 20, font_color=WHITE, font_name="LiberationMono-Italic.ttf")

        # Main Text
        draw.draw_text(screen, (15, WINDOW_HEIGHT * 0.15), f"SNAKE IV", 120, font_color=WHITE, bold=True)

        for button in buttons:
            button_x =  WINDOW_WIDTH // 2
            button_y = WINDOW_HEIGHT // 2 + (65 * button_i)

            faux_buttonx = BUTTON_WIDTH + button["hover"]
            faux_buttony = BUTTON_HEIGHT + button["hover"] / 2

            original_color = button["color"]

            button_box = pygame.Rect(button_x - faux_buttonx / 2, button_y - faux_buttony / 2, faux_buttonx, faux_buttony)



            if button_box.collidepoint(mouse_x, mouse_y):
                button_color = draw.darken_color(button["color"], 0.6)
                button["hover"] = pygame.math.clamp((button["hover"] + 1) * 1.2, 0, 30)

            else:
                button_color = original_color
                button["hover"] = pygame.math.clamp((button["hover"] + 1) * 0.9, 0, 30)


            button_font = pygame.font.SysFont("Comic Sans MS", round(pygame.math.clamp((40 + button["hover"] * 0.3), 40, 76)))
            button_font2 = pygame.font.SysFont("Comic Sans MS", round(pygame.math.clamp((40 + button["hover"] * 0.6), 40, 76)))
                
            button_label = button_font.render(button["text"], True, draw.darken_color(button_color, 0.6))
            button_label2 = button_font2.render(button["text"], True, draw.darken_color(original_color, 0.7))

            faux_buttonx = BUTTON_WIDTH + button["hover"]
            faux_buttony = BUTTON_HEIGHT + button["hover"] / 2
            
            button_box.size = [faux_buttonx, faux_buttony]
            button_box.center = [button_x, button_y]

            text_rect = button_label.get_rect()
            text_rect.center = button_box.center

            text_rect2 = button_label2.get_rect()
            text_rect2.center = button_box.center


            

            pygame.draw.rect(screen, button_color, button_box)
            screen.blit(button_label, text_rect)
            screen.blit(button_label2, text_rect2)

            button_i += 1

        pygame.display.flip()
        # Limit the frame rate to the specified frames per second (fps)
        clock.tick(fps) # Use the clock to control the frame rate

    scream.play()
    pygame.time.delay(560)
    pygame.quit()

    sys.exit()
    

def run_snake_game(high_score):
    screen = init_game()
    clock = pygame.time.Clock() # Initialize the clock here
    game_running = True
    playing = True

    # Game Variables
    CELL_SIZE = 30
    direction = "Up"
    score = 0
    particle_speed = 2
    tick = 0
    fps = 60

    # Establish Debris
    debris = []
    
    def move_apple():
        return [random.randint(0, (WINDOW_WIDTH // CELL_SIZE) - 2) * CELL_SIZE, random.randint(0, (WINDOW_WIDTH // CELL_SIZE) - 2) * CELL_SIZE]
    
    def gen_particles(position, count, color):
        for i in range(count):
            print(color)
            particle = [[position[0] + random.randint(0, CELL_SIZE), position[1] + random.randint(0, CELL_SIZE)], [random.randint(round(-particle_speed/2), round(particle_speed/2)), random.randint(particle_speed * 2, particle_speed * 4)], draw.darken_color(color, random.randint(50,100)/100), ]
            debris.append(particle)



    snake_pos = [[int(WINDOW_WIDTH // 2), int(WINDOW_HEIGHT // 2)]]
    for segment in range(2):
        snake_pos.append([int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2) + CELL_SIZE * (segment + 1)])

    # Define Apple Position
    apple_position = move_apple()

    # Load Sounds
    sound1 = pygame.mixer.Sound("Sounds/coins.ogg")
    sound2 = pygame.mixer.Sound("Sounds/windowbreak.ogg")
    gameover = pygame.mixer.Sound("Sounds/gameover.ogg")
    scream = pygame.mixer.Sound("Sounds/screammale.ogg")
    itemcatch = pygame.mixer.Sound("Sounds/itemcatch.mp3")
    gore = pygame.mixer.Sound("Sounds/gore1.ogg")
    consume = pygame.mixer.Sound("Sounds/gore2.ogg")

    # Set Volume for Sounds
    sound1.set_volume(.25)
    sound2.set_volume(.25)
    consume.set_volume(.25)
    gameover.set_volume(.25)
    scream.set_volume(.5)
    gore.set_volume(.25)

    # Try to Load Music
    try:
        pygame.mixer.music.unload()
        pygame.mixer.music.load("game_intense.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except:
        print("Music did not load. D:")

    while game_running:
        tick += 1
        interior_offset = (CELL_SIZE * 0.1)
        screen.fill(BLACK) # Use color from config

        for particle in debris:
            # Move Particle
            particle[0][0] += particle[1][0]
            particle[0][1] -= particle[1][1]
            # Edit Velocity
            particle[1][1] -= particle_speed/5
            
            if particle[0][0] < 0 and particle[1][0] < 0:
                particle[1][0] *= -1
            elif particle[0][0] > WINDOW_WIDTH and particle[1][0] > 0:
                particle[1][0] *= -1


            draw.draw_rect(screen, particle[2], particle[0], CELL_SIZE/6, CELL_SIZE/6)

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
        if score > high_score:
            high_score = score

        # Check Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
                if event.key == pygame.K_w or event.key == pygame.K_UP and direction != "Down":
                    direction = "Up"
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT and direction != "Left":
                    direction = "Right"
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT and direction != "Right":
                    direction = "Left"
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN and direction != "Up":
                    direction = "Down"

        if playing == True:
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

            if tick % 6 == 0:
                snake_pos.insert(0, new_segment)
                print(f"snake_len {len(snake_pos)}, score {score}")
                if len(snake_pos) - 1 < score + 3:
                    print("add")
                else:
                    snake_pos.pop(-1)

        elif playing == False:
            if tick % 35 == 0 and len(snake_pos) > 0:
                lastpos = snake_pos.pop()
                gen_particles(lastpos, random.randint(10,20), GREEN)
                    
                gore.play()
                fps = round(fps * 1.06)
                
            elif tick % 250 == 0 and len(snake_pos) == 0:
                game_running = False
            


        # Apple Collision
        if playing == True and pygame.Rect(snake_pos[0][0], snake_pos[0][1], CELL_SIZE, CELL_SIZE).colliderect(pygame.Rect(apple_position[0], apple_position[1], CELL_SIZE, CELL_SIZE)):
            score += 1
            gen_particles(apple_position, random.randint(10,20), RED)
            apple_position = move_apple()
            consume.play()

        # Snake Collision
        segment_i = 0
        if playing == True:
            for segment in snake_pos:
                    if segment_i > 0:
                        if snake_pos[0][0] == segment[0] and snake_pos[0][1] == segment[1]:
                            playing = False  
                            scream.play() 
                    else:
                        segment_i += 1
                    
        # Wall Collision
        if playing == True:
            if snake_pos[0][0] >= WINDOW_WIDTH or snake_pos[0][0] < 0 or snake_pos[0][1] >= WINDOW_HEIGHT or snake_pos[0][1] < 0:
                playing = False   
                scream.play()               


        pygame.display.flip()
        # Limit the frame rate to the specified frames per second (fps)
        clock.tick(fps) # Use the clock to control the frame rate


    pygame.mixer.music.unload()
    scream.stop()
    pygame.mixer.music.load("game_weak.ogg")
    pygame.mixer.music.play(-1)

    return high_score
    



if __name__ == "__main__":
    main()