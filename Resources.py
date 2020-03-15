import pygame
import sys
import math

pygame.init()

screen = pygame.display.set_mode((1280, 720))

rectangle = pygame.image.load("Turtle.png").convert_alpha()

print(type(rectangle))
angle = 0
omega = 0
r = (500, 360)
v = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                omega = 0.6
            if event.key == pygame.K_RIGHT:
                omega = -0.6
            if event.key == pygame.K_UP:
                v = -2
            if event.key == pygame.K_DOWN:
                v = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                omega = 0
            if event.key == pygame.K_RIGHT:
                omega = 0
            if event.key == pygame.K_UP:
                v = 0
            if event.key == pygame.K_DOWN:
                v = 0

    angle += omega
    r = (r[0]+v*math.sin(math.radians(angle)),r[1]+v*math.cos(math.radians(angle)))
    newRectangle = pygame.transform.rotate(pygame.transform.scale(rectangle, (307//3, 1069//3)), angle)
    Dimensions = newRectangle.get_rect()
    pos = (r[0] - Dimensions.width / 2, r[1] - Dimensions.height / 2)
    screen.fill((0, 0, 0))
    screen.blit(newRectangle, pos)
    pygame.display.flip()
