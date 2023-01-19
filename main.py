import pygame
import random
from pygame.constants import QUIT

pygame.init()

screen = width, height = 800, 600
main_surface = pygame.display.set_mode(screen)
ball = pygame.Surface((20, 20))
ball.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
bal_rect = ball.get_rect()
ball_speed = [1, 1]
is_workking = True

while is_workking:
    for event in pygame.event.get():
        if event.type == QUIT:
            is_workking = False
    bal_rect = bal_rect.move(ball_speed)

    if bal_rect.bottom >= height or bal_rect.top <= 0:
        ball_speed[1] = -ball_speed[1]
        ball.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    elif bal_rect.right >= width or bal_rect.left <= 0:
        ball_speed[0] = -ball_speed[0]
        ball.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    main_surface.fill((0, 191, 255))
    main_surface.blit(ball, bal_rect)

    pygame.display.flip()
