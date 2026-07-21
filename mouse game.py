"""
Mouse Game

Author: Mohammad Reza Bakhshandeh
Year: 2026

A mouse-controlled arcade game built with Python and Pygame.
"""

import pygame
import random


pygame.init()

icon = pygame.Surface((32, 32), pygame.SRCALPHA)  # Transparent icon
pygame.display.set_icon(icon)

pygame.display.set_caption("Make Bigger")

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TOP_MARGIN = 60

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
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 200)
YELLOW = (255, 190, 20)
ORANGE = (255, 100, 0)

MENU = "menu"
PLAYING = "playing"
PAUSED = "paused"
WIN = "win"
GAME_OVER = "game_over"


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

        self.state = PLAYING     # state = ["menu", "playing", "paused", "game_over", "win"]

        self.max_size_timer = None
        self.win_delay = 3000   # milliseconds (3 seconds)

        self.screen = screen

        self.clock = pygame.time.Clock()
        self.fps = 30


    def run(self):
        while self.state != MENU:

            self.process_events()

            if self.state == GAME_OVER:
                self.draw_game_over()

            elif self.state == PAUSED:
                self.draw_pause_menu()
            
            elif self.state == WIN:
                self.draw_win_screen()

            elif self.state == PLAYING:
                self.update()
                self.draw()


            pygame.display.flip()
            self.clock.tick(self.fps)


    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == PAUSED:
                        self.state = PLAYING
                    elif self.state == PLAYING:
                        self.state = PAUSED


    def update(self):
        self.player.update()
        self.player.eat(self.food)

        if self.player.size >= 94:
            if self.max_size_timer is None:
                self.max_size_timer = pygame.time.get_ticks()

            elif pygame.time.get_ticks() - self.max_size_timer >= self.win_delay:
                self.state = "win"

        else:
            self.max_size_timer = None

        if self.player.size <= 10:
            self.state = GAME_OVER


    def draw(self):
        self.screen.fill(BLACK)

        self.player.draw(self.screen)
        self.food.draw(self.screen)

        self.draw_ui()


    def draw_ui(self):
        draw_text("Score= " + str(self.player.score), font, WHITE, 70, TOP_MARGIN // 2)

        # draw_text("Difficulty= " + str(difficulty), font, RED, SCREEN_WIDTH-100, 20)
        pygame.draw.line(self.screen, RED, (0, TOP_MARGIN), (SCREEN_WIDTH, TOP_MARGIN), 5)
        pygame.draw.line(self.screen, RED, (0, TOP_MARGIN), (0, SCREEN_HEIGHT), 5)
        pygame.draw.line(self.screen, RED, (SCREEN_WIDTH-2, TOP_MARGIN), (SCREEN_WIDTH-2, SCREEN_HEIGHT), 5)
        pygame.draw.line(self.screen, RED, (0, SCREEN_HEIGHT-2), (SCREEN_WIDTH, SCREEN_HEIGHT-2), 5)
        
        self.draw_win_progress()


    def draw_win_progress(self):
        if self.max_size_timer is None:
            return

        elapsed = pygame.time.get_ticks() - self.max_size_timer
        progress = min(elapsed / self.win_delay, 1)

        remaining = max(0, (self.win_delay - elapsed) / 1000)

        bar_width = 250
        bar_height = 18

        x = SCREEN_WIDTH // 2 - bar_width // 2
        y = 12

        # Countdown text
        draw_text( f"Hold to Win: {remaining:.1f}s", small_font, WHITE, SCREEN_WIDTH // 2, y + 10)

        # Background
        pygame.draw.rect(self.screen, GRAY, (x, y + 20, bar_width , bar_height), border_radius=8)

        # Filled portion
        pygame.draw.rect(self.screen, YELLOW, (x, y + 20, int(bar_width * progress), bar_height), border_radius=8)

        # Border
        pygame.draw.rect(self.screen, WHITE, (x, y + 20, bar_width , bar_height), 2, border_radius=8)


    def draw_pause_menu(self):
        self.screen.fill(BLACK)

        draw_text("PAUSED", title_font, YELLOW, SCREEN_WIDTH//2, 180)

        draw_text("Note: The game starts immediately after you pressed resume.", small_font, RED, SCREEN_WIDTH//2, 250)

        if draw_button("Resume", SCREEN_WIDTH//2-150, 300, 120, 50, GREEN, DARK_GREEN):
            self.state = PLAYING

        if draw_button("Main Menu", SCREEN_WIDTH//2+30, 300, 120, 50, BLUE, DARK_BLUE):
            self.state = MENU

        draw_text("Press ESC to Resume", small_font, GRAY, SCREEN_WIDTH//2, 390)


    def draw_win_screen(self):
        self.screen.fill(BLACK)
        draw_text("You Won!", title_font, RED, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-70)
        draw_text(f"Final Score: {self.player.score}", font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 -30)

        if draw_button("Play Again", SCREEN_WIDTH/2-130, SCREEN_HEIGHT/2, 120, 50, GREEN, DARK_GREEN):
            self.reset()
        if draw_button("Menu", SCREEN_WIDTH/2+10, SCREEN_HEIGHT/2, 120, 50, BLUE, DARK_BLUE):
            self.state = MENU


    def draw_game_over(self):
        self.screen.fill(BLACK)
        draw_text("GAME OVER!", title_font, RED, SCREEN_WIDTH/2, SCREEN_HEIGHT/2-70)
        draw_text(f"Final Score: {self.player.score}", font, WHITE, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 -30)

        if draw_button("Play Again", SCREEN_WIDTH/2-130, SCREEN_HEIGHT/2, 120, 50, GREEN, DARK_GREEN):
            self.reset()
        if draw_button("Menu", SCREEN_WIDTH/2+10, SCREEN_HEIGHT/2, 120, 50, BLUE, DARK_BLUE):
            self.state = MENU


    def reset(self):
        self.player = Player()
        self.food = Food()
        self.state = "playing"


class Player:
    def __init__(self):
        self.size = 30

        self.loc_x = SCREEN_WIDTH // 2
        self.loc_y = SCREEN_HEIGHT // 2

        self.rect = pygame.Rect(self.loc_x, self.loc_y, self.size, self.size)

        self.score = 0


    def update(self):
        half = self.size // 2

        mouse_x, mouse_y = pygame.mouse.get_pos()

        self.loc_x = max(half, min(mouse_x, SCREEN_WIDTH - half))
        self.loc_y = max(TOP_MARGIN + half, min(mouse_y, SCREEN_HEIGHT - half))
        
        #set max and min size for object
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
        self.loc_y = random.randint(TOP_MARGIN + 10, SCREEN_HEIGHT - 40)

        self.rect = pygame.Rect(self.loc_x, self.loc_y, self.size, self.size)


    def update(self):
        self.loc_x = random.randint(40, SCREEN_WIDTH-40)
        self.loc_y = random.randint(TOP_MARGIN + 10, SCREEN_HEIGHT - 40)

        self.rect = pygame.Rect(self.loc_x, self.loc_y, self.size, self.size)   
                                    

    def draw(self, screen):
        pygame.draw.rect(screen, FOOD_COLOR, self.rect)


def menu():
    while True:
        screen.fill(BLACK)
        
        # title
        draw_text(" Mouse Game ", title_font, GREEN, SCREEN_WIDTH/2, 160)
        
        # buttons
        if draw_button("Start", SCREEN_WIDTH/2 -150, SCREEN_HEIGHT/2 -60, 100, 50, GREEN, DARK_GREEN):
            return "start"
        if draw_button("Exit", SCREEN_WIDTH/2 +50, SCREEN_HEIGHT/2 -60, 100, 50, ORANGE, YELLOW):
            return "exit"

        # guide
        draw_text("Move your mouse to control the green square.", small_font, GRAY, SCREEN_WIDTH/2, 350)
        draw_text("Collect blue food to grow larger.", small_font, GRAY, SCREEN_WIDTH/2, 380)
        draw_text("If your size reaches the minimum, you lose.", small_font, GRAY, SCREEN_WIDTH/2, 410)
        draw_text("Reach the maximum size and hold it for 3 seconds to win!", small_font, GRAY, SCREEN_WIDTH/2, 440)
        draw_text("Press ESC to Pause and Resume", small_font, GRAY, SCREEN_WIDTH/2, 470)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game() 


def main():
    while True:
        action = menu()

        if action == "start":
            Game().run()

        elif action == "exit":
            quit_game()

if __name__ == "__main__":
    main()
