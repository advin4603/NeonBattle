from Entities import Entity
from spaceship import Spaceship
from bullets import Bullet
import pygame
import Constants


class Manager:
    def __init__(self, *args: Spaceship):
        self.spaceships = list(args)
        self.bullets = []

    def addBullet(self, bullet: Bullet):
        self.bullets.append(bullet)

    def InputCheck(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            for ship in self.spaceships:
                if event.type == pygame.KEYDOWN:
                    if event.key == ship.shootKey:
                        ship.shoot(self)

                if keys[ship.thrustKey]:
                    ship.thrust()
                else:
                    ship.decelerate()

                if keys[ship.leftKey] and not keys[ship.rightKey]:
                    ship.rotateLeft()
                elif keys[ship.rightKey] and not keys[ship.leftKey]:
                    ship.rotateRight()
                else:
                    ship.noRotate()
