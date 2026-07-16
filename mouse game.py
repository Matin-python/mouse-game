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

title_font = pygame.font.SysFont('arial', 50, bold=True)
font = pygame.font.SysFont('arial', 25)
small_font = pygame.font.SysFont('arial', 18)

# init colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
FOOD_COLOR = (30,90,230)

WHITE = (255, 255, 255)

BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
YELLOW = (255, 190, 20)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)


def quit_game():
    pygame.quit()
    raise SystemExit


def draw_text(text, font_obj, color, x, y):
    screen_text = font_obj.render(text, True, color)
    screen_rect = screen_text.get_rect(center=(x, y))
    screen.blit(screen_text, screen_rect)


def draw_button(text, x, y, w, h, color, hover_color):
    """Draw an interactive button."""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    
    # button text
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=(x + w/2, y + h/2))
    screen.blit(text_surf, text_rect)
    
    return False


class Game:
    def __init__(self):
        self.player = Player()
        self.food = Food()        

        self.running = True
        self.game_over = False
        self.paused = False

        self.screen = screen

        self.clock = pygame.time.Clock()
        self.fps = 30

    def run(self):
        while self.running:
            self.process_events()

            if not self.paused:
                self.update()

            self.draw()

            self.clock.tick(self.fps)


    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused


    def update(self):
        self.player.update()
        self.player.eat(self.food)

    def draw(self):
        self.screen.fill(BLACK)

        self.player.draw(self.screen)
        self.food.draw(self.screen)

        self.draw_ui()

        pygame.display.flip()


    def draw_ui(self):
        draw_text("Score= " + str(self.player.score), font, RED, 70, 20)
        # draw_text("Difficulty= " + str(difficulty), font, RED, SCREEN_WIDTH-100, 20)
        pygame.draw.line(self.screen, RED, (0,40), (SCREEN_WIDTH,40), 5)
        pygame.draw.line(self.screen, RED, (0,40), (0, SCREEN_HEIGHT), 5)
        pygame.draw.line(self.screen, RED, (SCREEN_WIDTH-2,40), (SCREEN_WIDTH-2,SCREEN_HEIGHT), 5)
        pygame.draw.line(self.screen, RED, (0, SCREEN_HEIGHT-2), (SCREEN_WIDTH,SCREEN_HEIGHT-2), 5)

    def reset(self):
        self.player = Player()
        self.food = Food()

        self.game_over = False
        self.paused = False

class Player:
    def __init__(self):
        self.size = 30

        self.loc_x = SCREEN_WIDTH // 2
        self.loc_y = SCREEN_HEIGHT // 2

        self.rect = pygame.Rect(self.loc_x, self.loc_y, self.size, self.size)

        self.score = 0
        
    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.loc_x = mouse_x
        self.loc_y = mouse_y
        
        self.size -= 0.5
        self.size = max(10, min(self.size, 100))

        self.rect = pygame.Rect(self.loc_x, self.loc_y, self.size, self.size)

        self.rect.center = (self.loc_x, self.loc_y)

    def eat(self, food):
        if self.rect.colliderect(food.rect):
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
        pygame.draw.rect(screen, FOOD_COLOR, self.rect)





def menu():
    while True:
        screen.fill(BLACK)
        
        # title
        draw_text(" Mouse Game ", title_font, GREEN, SCREEN_WIDTH/2, 150)
        
        # buttons
        if draw_button("start", SCREEN_WIDTH/2 -150, SCREEN_HEIGHT/2 -70, 100, 50, GREEN, DARK_GREEN):
            return 'game'
        
        draw_text("Select Difficulty", font, GRAY, SCREEN_WIDTH/2, 200)
        
        # guide
        draw_text("move your mause and try to eat food as much as you can.", small_font, GRAY, SCREEN_WIDTH/2, 350)
        draw_text("Press ESC to Return to Menu", small_font, GRAY, SCREEN_WIDTH/2, 380)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game() 


def main():
    while True:
        menu()

        game = Game()
        game.run()


if __name__ == "__main__":
    main()
