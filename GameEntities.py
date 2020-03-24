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


# bulletsPath = Path('Assets') / Path('Images') / Path('Sprites') / Path('Bullet')
# bulletImageFilePaths = bulletsPath.rglob('*[0-9].png')
# bulletCache = {pth: pygame.image.load(str(pth)).convert_alpha() for pth in bulletImageFilePaths}


class Bullet(Entities.Entity):

    def __init__(self, pos: numpy.array, angle: float, model: str, parent: Spaceship, bulletSpeed: float,
                 killOnImpact: bool, bulletCache: Dict[Path, pygame.Surface]):
        self.pos = pos + Cs.BULLETSPAWNDIST * numpy.array([sin(radians(angle)), cos(radians(angle))])
        self.angularDisplacement = angle
        self.parent = parent
        self.spritePath = Path('Assets') / Path('Images') / Path('Sprites') / Path('Bullet') / Path(model) / Path(
            'Solid')
        self.bulletCache = bulletCache

        def imageLoader(inPath: Path):
            image = self.bulletCache[inPath]
            return image

        self.Images = imageGroup.ImageGroup(imageFolderPath=self.spritePath,
                                            imageLoader=imageLoader)
        self.Sprite = Sprite.Sprite(self.Images, Cs.bulletScaleConst, Cs.bulletUpdateInterval, (pos[0], pos[1]))
        self.bulletHalfHeight = self.Sprite.currentRect.h / 2
        self.angularDisplacement = angle

        self.damage = parent.damagePerBullet
        self.offScreen = False
        self.killOnImpact = killOnImpact

        super().__init__(posVector=self.pos,
                         velVector=bulletSpeed * self.headDirectionVector,
                         sprite=self.Sprite, angularDisplacement=angle,
                         angularSpeed=0, angularAcc=0)

    def Update(self, acc: numpy.array = None, angularAcc: float = None):
        if self.offScreen:
            return
        super().Update(acc, angularAcc)
        if not(Cs.GameStage[0][0] < self.pos[0] < Cs.GameStage[0][1] and Cs.GameStage[1][0] < self.pos[1] < Cs.GameStage[1][1]):
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
        self.damageDamp = Cs.DEFAULTDAMAGEDAMP
        self.piercingBullets = False
        super().__init__(sprite=self.Sprite,
                         angularDisplacement=angularDisplacement,
                         angularSpeed=0.,
                         angularAcc=0.,
                         posVector=pos,
                         limPos=numpy.array(Cs.GameStage),
                         limVelScalar=Cs.SPEEDLIMIT,
                         limAngularSpeed=Cs.ROTATELIM)

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

    def shoot(self, manager, bulletCache):
        """

        :type manager: manager.Manager
        :type bulletCache: Dict[Path, pygame.surface]
        """
        newBullet = Bullet(self.pos + self.headDirectionVector * self.spriteGroup.currentRect.h / 2,
                           self.angularDisplacement, self.model, self,
                           self.bulletSpeed, self.piercingBullets, bulletCache)
        manager.addBullet(newBullet)

    def hit(self, bullet: Bullet):
        self.health -= bullet.damage * self.damageDamp


class PinkSpaceship(Spaceship):
    def __init__(self, pos: numpy.array, angle: float, moveSet: Dict[str, int]):
        self.model = 'Pink'
        super(PinkSpaceship, self).__init__(pos, angle, self.model, moveSet)


class BlueSpaceship(Spaceship):
    def __init__(self, pos: numpy.array, angle: float, moveSet: Dict[str, int]):
        self.model = 'Blue'
        super(BlueSpaceship, self).__init__(pos, angle, self.model, moveSet)


if __name__ == '__main__':
    meanBench = []
    pygame.init()
    from time import time

    screen = pygame.display.set_mode((1920, 1080), flags=pygame.FULLSCREEN | pygame.HWACCEL | pygame.HWSURFACE)
    ent = BlueSpaceship(numpy.array([640., 360]), 0,
                        {'THRUST': pygame.K_w, 'LEFT': pygame.K_a, 'RIGHT': pygame.K_d, 'SHOOT': pygame.K_SPACE})
    ent2 = PinkSpaceship(numpy.array([500., 360]), 0,
                         {'THRUST': pygame.K_w, 'LEFT': pygame.K_a, 'RIGHT': pygame.K_d, 'SHOOT': pygame.K_SPACE})

    done = False
    start = time()

    while not done:
        start = time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True
                continue
            if event.type == pygame.KEYDOWN:
                if event.key == ent.shootKey:
                    print('>>###Bang###')
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    done = True
                    continue
        if done:
            break
        keys = pygame.key.get_pressed()
        if keys[ent.leftKey] and not keys[ent.rightKey]:
            ent.rotateLeft()
            ent2.rotateLeft()
        elif keys[ent.rightKey] and not keys[ent.leftKey]:
            ent.rotateRight()
            ent2.rotateRight()
        else:
            ent.noRotate()
            ent2.noRotate()

        if keys[ent.thrustKey]:
            ent.thrust()
            ent2.thrust()
        else:
            ent.decelerate()
            ent2.decelerate()

        ent.Update(acc=ent.acc + numpy.array([0., 0.07]))
        ent2.Update(acc=ent2.acc + numpy.array([0., 0.07]))
        screen.fill((0, 0, 0))
        ent.drawEntity(screen)
        ent2.drawEntity(screen)
        pygame.display.flip()
        benchmark = time() - start
        meanBench.append(benchmark)
        print(ent.angularSpeed)
        if benchmark > 1 / Cs.FPS:
            print('SLOWWWWW')
        while time() - start < 1 / Cs.FPS:
            pass

    print(sum(meanBench) / len(meanBench))
