from Entities import Entity
from spaceship import Spaceship
from bullets import Bullet
import pygame
import Constants


class Manager:
    def __init__(self, *args: Entity):
        self.spaceships = []
        self.bullets = []
        for entity in args:
            if isinstance(entity, Spaceship):
                self.spaceships.append(entity)
            elif isinstance(entity, Bullet):
                self.bullets.append(entity)

    def addBullet(self, bullet: Bullet):
        self.bullets.append(bullet)

