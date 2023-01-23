import random
import time
from os import listdir

import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

from setting import *

pygame.init()

main_surface = pygame.display.set_mode(screen)
background = pygame.transform.scale(pygame.image.load(IMG_BACK), screen)
timer = time.time()
player_ingd = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
ball = player_ingd[0]
bal_rect = ball.get_rect()
ball_speed = 5

pygame.font.init()
font1 = pygame.font.Font(None, 80)
win = font1.render(WIN_TEXT, True, WIN_COLOR)
font2 = pygame.font.Font(None, 36)


def enemy_create():
    enemy = pygame.transform.scale(pygame.image.load(IMG_ENEMY), (90, 40))
    enemy_rect = pygame.Rect(width, random.randint(0, height), *enemy.get_size())
    enemy_speed = random.randint(0, 3)
    return [enemy, enemy_rect, enemy_speed]


def scores():
    score = pygame.transform.scale(pygame.image.load(IMG_SCORE), (30, 30))

    score_rect = pygame.Rect(random.randint(0, width), 0, *score.get_size())
    score_speed = random.randint(0, 4)
    return [score, score_rect, score_speed]


bgx = 0
bgx2 = background.get_width()
background_speed = 3

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_SCORE = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_SCORE, random.randint(1500, 2500))
CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)
is_workking = True

while is_workking:
    FPS.tick(70)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_workking = False
        if event.type == CREATE_ENEMY or event.type == CREATE_SCORE:
            enemes.append(enemy_create())
            scores_list.append(scores())
        if event.type == CHANGE_IMG:
            index_img += 1
            if index_img == len(player_ingd):
                index_img = 0
            ball = player_ingd[index_img]
    pressed_keys = pygame.key.get_pressed()
    bgx -= background_speed
    bgx2 -= background_speed
    if bgx < -background.get_width():
        bgx = background.get_width()
    elif bgx2 < -background.get_width():
        bgx2 = background.get_width()
    main_surface.blit(background, (bgx, 0))
    main_surface.blit(background, (bgx2, 0))
    main_surface.blit(ball, bal_rect)
    pygame.display.update()

    for enemy in enemes:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])
        if enemy[1].left < 0:
            enemes.pop(enemes.index(enemy))
        if bal_rect.colliderect(enemy[1]):
            game_over = font2.render('GAME OVER', 1, (0, 0, 0))
            main_surface.blit(game_over, (height/2, width/2))
            is_workking = False
    for score in scores_list:
        score[1] = score[1].move(0, score[2])
        main_surface.blit(score[0], score[1])
        if score[1].top > height:
            scores_list.pop(scores_list.index(score))
        elif bal_rect.colliderect(score[1]):
            scores_list.pop(scores_list.index(score))
            POINTS += 1
        label_win = font2.render('Total:' + str(POINTS), 1, LABEL_WIN_COLOR)
        main_surface.blit(label_win, (30, 30))
        diff_timer = round(time.time() - timer, 2)
        label_timer = font2.render('Time:' + str(diff_timer), 1, LABEL_TIMER_COLOR)
        main_surface.blit(label_timer, (600, 20))
    if pressed_keys[K_DOWN] and bal_rect.bottom <= height:
        bal_rect = bal_rect.move(0, ball_speed)
    elif pressed_keys[K_UP] and bal_rect.top >= 0:
        bal_rect = bal_rect.move(0, -ball_speed)
    elif pressed_keys[K_RIGHT] and bal_rect.right <= width:
        bal_rect = bal_rect.move(ball_speed, 0)
    elif pressed_keys[K_LEFT] and bal_rect.left >= 0:
        bal_rect = bal_rect.move(-ball_speed, 0)

    pygame.display.flip()
