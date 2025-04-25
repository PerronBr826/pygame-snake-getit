# External Module used to draw shapes very nicely

import pygame

def draw_circle(screen, shape):
    pygame.draw.circle(screen, shape['color'], shape['position'], shape['radius'])
    
def draw_rect(screen, color, position, width, height):
    pygame.draw.rect(screen, color, (position[0], position[1], width, height))
    
def draw_line(screen, color, start_pos, end_pos, width):
    pygame.draw.line(screen, color, start_pos, end_pos, width)

def draw_square(screen, shape):
    pygame.draw.rect(screen, shape['color'], (shape['position'][0] - shape['radius'], shape['position'][1] - shape['radius'], shape['radius'] * 2, shape['radius'] * 2))

def draw_text(screen, font_pose, text="No text given!", font_size=10, font_name="DejaVuSans.ttf", font_color=(0,0,0), italic=False, bold=False):
    pygame.font.init()
    font = pygame.font.Font(font_name, font_size)

    font.set_italic(italic)
    font.set_bold(bold)

    text = font.render(text, False, font_color)
    screen.blit(text, font_pose)
    
def darken_color(color, darkness):
    return [color[0] * darkness, color[1] * darkness, color[2] * darkness]