"""
Mouse Game

Author: Mohammad Reza Bakhshandeh
Year: 2026

A mouse-controlled arcade game built with Python and Pygame.
"""

import pygame
import random


pygame.init()
pygame.display.set_caption("Make Bigger")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()

title_font = pygame.font.SysFont('arial', 50, bold=True)
font = pygame.font.SysFont('arial', 25)
small_font = pygame.font.SysFont('arial', 18)

# init colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
YELLOW = (255, 190, 20)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)



def draw_text(text, font_obj, color, x, y):
    screen_text = font_obj.render(text, True, color)
    screen_rect = screen_text.get_rect(center=(x, y))
    screen.blit(screen_text, screen_rect)

def draw(screen, score):
    draw_text("Score= " + str(score), font, RED, 70, 20)
    # draw_text("Difficulty= " + str(difficulty), font, RED, SCREEN_WIDTH-100, 20)
    pygame.draw.line(screen, RED, (0,40), (SCREEN_WIDTH,40), 5)
    pygame.draw.line(screen, RED, (0,40), (0, SCREEN_HEIGHT), 5)
    pygame.draw.line(screen, RED, (SCREEN_WIDTH-2,40), (SCREEN_WIDTH-2,SCREEN_HEIGHT), 5)
    pygame.draw.line(screen, RED, (0, SCREEN_HEIGHT-2), (SCREEN_WIDTH,SCREEN_HEIGHT-2), 5)

def main():
    score = 0

    main_rect_size = 30
    rand_rect_size = 15

    main_x = SCREEN_WIDTH/2
    main_y = SCREEN_HEIGHT/2

    rand_x = random.randint(40, SCREEN_WIDTH-40)
    rand_y = random.randint(40, SCREEN_HEIGHT-40)

    run = True
    while run:
        screen.fill((0,0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        main_rect = pygame.Rect(main_x, main_y, main_rect_size, main_rect_size)
        rand_rect = pygame.Rect(rand_x, rand_y, rand_rect_size, rand_rect_size)

        mouse = pygame.mouse.get_pos()
        main_rect.center = mouse

        pygame.draw.rect(screen, (0,255,0), main_rect)
        pygame.draw.rect(screen, (30,90,230), rand_rect)

        draw(screen, score)

        main_rect_size -= 0.5
        if main_rect_size <= 10:
            main_rect_size = 10
        elif main_rect_size >= 100:
            main_rect_size = 100

        if main_rect.colliderect(rand_rect):
            pygame.draw.rect(screen, (255,20,20), main_rect)
            rand_x = random.randint(40, SCREEN_WIDTH-40)
            rand_y = random.randint(40, SCREEN_HEIGHT-40)
            main_rect_size += 15
            score += 1

        

        pygame.display.flip()

        clock.tick(30)

    pygame.quit()

main()
