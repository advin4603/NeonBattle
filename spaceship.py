import numpy
import pygame
import Entities
import Sprite
import imageGroup
import Constants as Cs
from pathlib import Path
from bullets import Bullet
import manager
from typing import Dict


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

    def shoot(self, manager: manager.Manager):
        newBullet = Bullet(self.spriteGroup.currentRect.midtop, self.angularDisplacement, self.model, self,
                           self.bulletSpeed)
        manager.addBullet(newBullet)
