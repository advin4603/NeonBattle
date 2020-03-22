import Constants as Cs
import Entities
import GameEntities
import numpy
import pygame

from powerUps import *
from random import choices, randint

from typing import Dict
from pathlib import Path


class Manager:
    def __init__(self, display: pygame.Surface, bulletCache: Dict[Path, pygame.Surface], *args: GameEntities.Spaceship):
        self.spaceships = list(args)
        self.bullets = []
        self.display = display
        self.PowerUpManager = PowerUpManager()
        self.currentGravity = Cs.DEFAULTGRAVITY
        self.bulletCache = bulletCache

    def addBullet(self, *args: GameEntities.Bullet):
        self.bullets.extend(args)

    def InputCheck(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            for ship in self.spaceships:

                if event.type == pygame.KEYDOWN:
                    if event.key == ship.shootKey:
                        ship.shoot(self, self.bulletCache)

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

    def updateAll(self):
        for index, entity in enumerate(self.spaceships + self.bullets):
            if isinstance(entity, GameEntities.Bullet):
                if entity.offScreen:
                    self.bullets.pop(index)
            entity.Update(acc=entity.acc + self.currentGravity)
        self.PowerUpManager.updatePowerUps()

    def doCollision(self):
        for index, bullet in enumerate(self.bullets):
            for ent in self.spaceships + self.PowerUpManager.spawnedPowerUps:
                if bullet in ent:
                    ent.hit(bullet)
                    if bullet.killOnImpact:
                        self.bullets.pop(index)


class PowerUpManager:
    def __init__(self):
        self.Powers = list(PowerUp.__subclasses__())

        def ProbGetter(inPower: PowerUp) -> float:
            return inPower.probability

        self.Probabilities = map(ProbGetter, self.Powers)
        self.spawnInterval = Cs.PowerUpSpawnInterval
        self.despawnInterval = Cs.PowerUpDespawnInterval
        self.spawnedPowerUps = []

    def updatePowerUps(self):
        if self.despawnInterval == 1:
            self.spawnedPowerUps.clear()
            self.despawnInterval = Cs.PowerUpDespawnInterval
        elif self.spawnedPowerUps:
            self.despawnInterval -= 1
        elif not self.spawnedPowerUps:
            self.despawnInterval = Cs.PowerUpDespawnInterval

        if self.spawnInterval == 1:
            self.spawnedPowerUps.clear()
            self.spawnInterval = Cs.PowerUpSpawnInterval
            self.spawnedPowerUps.extend(choices(self.Powers, self.Probabilities, k=randint(*Cs.PowerUpSpawnRange)))
        else:
            self.spawnInterval -= 1
