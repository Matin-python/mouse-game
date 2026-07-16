import pygame
import random


pygame.init()
pygame.display.set_caption("Make Bigger")


screen_width = 800
screen_hight = 600

screen = pygame.display.set_mode((screen_width,screen_hight))
clock = pygame.time.Clock()

main_rect_size = 30
rand_rect_size = 15

main_x = screen_width/2
main_y = screen_hight/2

rand_x = random.randint(40, screen_width-40)
rand_y = random.randint(40, screen_hight-40)

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

    main_rect_size -= 0.5
    if main_rect_size <= 10:
        main_rect_size = 10
    elif main_rect_size >= 100:
        main_rect_size = 100

    if main_rect.colliderect(rand_rect):
        pygame.draw.rect(screen, (255,20,20), main_rect)
        rand_x = random.randint(40, screen_width-40)
        rand_y = random.randint(40, screen_hight-40)
        main_rect_size += 15

    

    key = pygame.key.get_pressed()
    if key[pygame.K_w] or key[pygame.K_UP]:
        main_y -= 10
    if key[pygame.K_a] or key[pygame.K_LEFT]:
        main_x -= 10
    if key[pygame.K_s] or key[pygame.K_DOWN]:
        main_y += 10
    if key[pygame.K_d] or key[pygame.K_RIGHT]:
        main_x += 10

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
