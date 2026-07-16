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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FFFFF = (30,90,230)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
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

def quit_game():
    pygame.quit()
    raise SystemExit

class Player():
    def __init__(self):
        self.size = 30

        self.loc_x = SCREEN_WIDTH // 2
        self.loc_y = SCREEN_HEIGHT // 2

        self.rect = pygame.Rect(self.loc_x, self.loc_y, self.size, self.size)

        self.score = 0
        
    def update(self):
        self.size -= 0.5
        self.size = max(10, min(self.size, 100))

        self.rect = pygame.Rect(self.loc_x, self.loc_y, self.size, self.size)

        mouse = pygame.mouse.get_pos()
        self.rect.center = mouse

    def eat(self, food):
        if self.rect.colliderect(food.rect):
            pygame.draw.rect(screen, (255,20,20), self.rect)
            food.update()
            self.size += 15
            self.score += 1

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)


class Food:
    def __init__(self):
        self.size = 15

        self.loc_x = random.randint(40, SCREEN_WIDTH-40)
        self.loc_y = random.randint(50, SCREEN_HEIGHT-40)

        self.rect = pygame.Rect(self.loc_x, self.loc_y, self.size, self.size)

    def update(self):
        self.loc_x = random.randint(40, SCREEN_WIDTH-40)
        self.loc_y = random.randint(50, SCREEN_HEIGHT-40) 

        self.rect = pygame.Rect(self.loc_x, self.loc_y, self.size, self.size)   
                                    
    def draw(self, screen):
        pygame.draw.rect(screen, FFFFF, self.rect)


def draw_ui(player):
    draw_text("Score= " + str(player.score), font, RED, 70, 20)
    # draw_text("Difficulty= " + str(difficulty), font, RED, SCREEN_WIDTH-100, 20)
    pygame.draw.line(screen, RED, (0,40), (SCREEN_WIDTH,40), 5)
    pygame.draw.line(screen, RED, (0,40), (0, SCREEN_HEIGHT), 5)
    pygame.draw.line(screen, RED, (SCREEN_WIDTH-2,40), (SCREEN_WIDTH-2,SCREEN_HEIGHT), 5)
    pygame.draw.line(screen, RED, (0, SCREEN_HEIGHT-2), (SCREEN_WIDTH,SCREEN_HEIGHT-2), 5)


def main():
    player = Player()
    food = Food()

    run = True
    while run:
        screen.fill((0,0,0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        player.update()
        player.eat(food= food)

        player.draw(screen= screen)
        food.draw(screen= screen)
        draw_ui(player= player)

        pygame.display.flip()

        clock.tick(30)


main()
