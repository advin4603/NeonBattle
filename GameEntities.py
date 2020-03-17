from __future__ import annotations
import pygame
import numpy
import Entities
import imageGroup
import Sprite
import Constants as Cs
from math import sin, cos, radians
from pathlib import Path

from typing import Dict




class Bullet(Entities.Entity):

    def __init__(self, pos: numpy.array, angle: float, model: str, parent: Spaceship, bulletSpeed: float):
        self.parent = parent
        self.spritePath = Path('Assets') / Path('Images') / Path('Sprites') / Path('Bullet') / Path(model) / Path(
            'Solid')

        def imageLoader(inPath: Path):
            image = pygame.image.load(str(inPath)).convert_alpha()
            return image

        self.Images = imageGroup.ImageGroup(imageFolderPath=self.spritePath,
                                            imageLoader=imageLoader)
        self.Sprite = Sprite.Sprite(self.Images, Cs.bulletScaleConst, Cs.bulletUpdateInterval, (pos[0], pos[1]))
        self.bulletHalfHeight = self.Sprite.currentRect.H / 2
        self.direction = numpy.array([sin(radians(angle)), cos(radians(angle))])
        self.Pos = pos + (Cs.BULLETSPAWNDIST + self.bulletHalfHeight) * self.direction

        self.damage = parent.damagePerBullet
        self.offScreen = False

        super().__init__(posVector=self.Pos,
                         velVector=bulletSpeed * self.direction,
                         sprite=self.Sprite, angularDisplacement=angle,
                         angularSpeed=0, angularAcc=0)

    def Update(self, acc: numpy.array = None, angularAcc: float = None):
        if self.offScreen:
            return
        super().Update(acc, angularAcc)
        if (not (Cs.GameStage[0][0] <= self.pos[0] <= Cs.GameStage[0][1])) or (not (
                Cs.GameStage[1][0] <= self.pos[0] <= Cs.GameStage[1][1])):
            self.offScreen = True


class Spaceship(Entities.Entity):
    def __init__(self, pos: numpy.array, angularDisplacement: float, model: str, moveset: Dict[str, int]):
        self.model = model
        self.spritePath = Path('Assets') / Path('Images') / Path('Sprites') / Path('Spaceship') / Path(model) / Path(
            'Solid')

        def imageLoader(inPath: Path):
            image = pygame.image.load(str(inPath)).convert_alpha()
            return image

        self.Images = imageGroup.ImageGroup(imageFolderPath=self.spritePath,
                                            imageLoader=imageLoader)

        self.Sprite = Sprite.Sprite(self.Images, Cs.spaceshipScaleConst, Cs.spacehipUpdateInterval, (pos[0], pos[1]))
        self.thrustOn = False
        self.health = 1
        self.damagePerBullet = Cs.DEFAULTDAMAGE
        self.bulletSpeed = Cs.DEFAULTBULLETSPEED
        self.thrustKey = moveset['THRUST']
        self.leftKey = moveset['LEFT']
        self.rightKey = moveset['RIGHT']
        self.shootKey = moveset['SHOOT']
        super().__init__(sprite=self.Sprite,
                         angularDisplacement=angularDisplacement,
                         angularSpeed=0.,
                         angularAcc=0.,
                         posVector=pos,
                         limPos=numpy.array(Cs.GameStage),
                         limVelScalar=Cs.SPEEDLIMIT)

    def thrust(self):
        self.thrustOn = True
        self.acc = self.headDirectionVector * Cs.THRUST

    def decelerate(self):
        self.thrustOn = False
        self.acc = -Cs.DAMP * self.vel

    def rotateRight(self):
        self.angularAcceleration = - Cs.ROTATETHRUST

    def rotateLeft(self):
        self.angularAcceleration = Cs.ROTATETHRUST

    def noRotate(self):
        self.angularAcceleration = -Cs.AngularDAMP * self.angularSpeed

    def shoot(self, manager: 'Manager'):
        newBullet = Bullet(self.spriteGroup.currentRect.midtop, self.angularDisplacement, self.model, self,
                           self.bulletSpeed)
        manager.addBullet(newBullet)
