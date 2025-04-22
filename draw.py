# External Module used to draw shapes very nicely

import pygame

def draw_circle(screen, shape):
    pygame.draw.circle(screen, shape['color'], shape['position'], shape['radius'])
    
def draw_rect(screen, shape):
    pygame.draw.rect(screen, shape['color'], (shape['position'][0], shape['position'][1], shape['width'], shape['height']))
    
def draw_line(screen, shape):
    pygame.draw.line(screen, shape['color'], shape['start_pos'], shape['end_pos'], shape['width'])

def draw_square(screen, shape):
    pygame.draw.rect(screen, shape['color'], (shape['position'][0] - shape['radius'], shape['position'][1] - shape['radius'], shape['radius'] * 2, shape['radius'] * 2))

def draw_text(screen, font_pose, text="No text given!", font_size=10, font_name="DejaVuSans.ttf", font_color=(0,0,0), italic=False, bold=False):
    pygame.font.init()
    font = pygame.font.Font(font_name, font_size)

    font.set_italic(italic)
    font.set_bold(bold)

    text = font.render(text, False, font_color)
    screen.blit(text, font_pose)
    