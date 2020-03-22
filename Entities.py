from __future__ import annotations

import numpy
import pygame
import Sprite
import imageGroup
from math import sin, cos, radians


class Entity:
    def __init__(self, sprite: Sprite.Sprite, angularDisplacement: float, angularSpeed: float, angularAcc: float,
                 posVector: numpy.array = numpy.array([0., 0.]),
                 velVector: numpy.array = numpy.array([0., 0.]),
                 accVector: numpy.array = numpy.array([0., 0.]),
                 limPos: numpy.array = None,
                 limVel: numpy.array = None,
                 limVelScalar: float = None,
                 limAngularSpeed: float = None):
        self.spriteGroup = sprite
        self.pos = posVector
        self.vel = velVector
        self.acc = accVector
        self.angularDisplacement = angularDisplacement
        self.angularSpeed = angularSpeed
        self.angularAcceleration = angularAcc
        self.positionLimit = limPos
        self.velocityLimit = limVel
        self.velLimitScalar = limVelScalar
        self.angularSpeedLim = limAngularSpeed

        if self.velocityLimit is not None and self.velLimitScalar is not None:
            maxVelLim = numpy.array([self.velocityLimit[0][1], self.velocityLimit[1][1]])
            velVecMag = numpy.sqrt(maxVelLim.dot(maxVelLim))
            if velVecMag != self.velLimitScalar:
                raise ValueError('The Scalar velocity limit and the vector velocity limit are not matching.')

    @property
    def UnitVelVector(self) -> numpy.array:
        VelMag = numpy.sqrt(self.vel.dot(self.vel))
        UnitVector = self.vel / VelMag
        return UnitVector

    @property
    def headDirectionVector(self) -> numpy.array:
        return numpy.array([sin(radians(self.angularDisplacement)), cos(radians(self.angularDisplacement))])

    @property
    def rightSideDirectionVector(self) -> numpy.array:
        return numpy.array([cos(radians(self.angularDisplacement)), sin(radians(self.angularDisplacement))])

    def Update(self, acc: numpy.array = None, angularAcc: float = None):
        if acc is not None:
            self.acc = acc

        if angularAcc is not None:
            self.angularAcceleration = angularAcc

        self.vel += self.acc
        if self.velocityLimit is not None:
            if self.vel[0] < self.velocityLimit[0][0]:
                self.vel = numpy.array([self.velocityLimit[0][0], self.vel[1]])
            elif self.vel[0] > self.velocityLimit[0][1]:
                self.vel = numpy.array([self.velocityLimit[0][1], self.vel[1]])

            if self.vel[1] < self.velocityLimit[1][0]:
                self.vel = numpy.array([self.vel[0], self.velocityLimit[1][0]])
            elif self.vel[1] > self.velocityLimit[1][1]:
                self.vel = numpy.array([self.vel[0], self.velocityLimit[1][1]])

        if self.velLimitScalar is not None:
            if numpy.sqrt(self.vel.dot(self.vel)) > self.velLimitScalar:
                self.vel = self.velLimitScalar * self.UnitVelVector

        self.pos += self.vel + (self.acc / 2)
        if self.positionLimit is not None:
            if self.pos[0] < self.positionLimit[0][0]:
                self.pos = numpy.array([self.positionLimit[0][0], self.pos[1]])
                self.vel = numpy.array([0., self.vel[1]])
            elif self.pos[0] > self.positionLimit[0][1]:
                self.pos = numpy.array([self.positionLimit[0][1], self.pos[1]])
                self.vel = numpy.array([0., self.vel[1]])

            if self.pos[1] < self.positionLimit[1][0]:
                self.pos = numpy.array([self.pos[0], self.positionLimit[1][0]])
                self.vel = numpy.array([self.vel[0], 0.])
            elif self.pos[1] > self.positionLimit[1][1]:
                self.pos = numpy.array([self.pos[0], self.positionLimit[1][1]])
                self.vel = numpy.array([self.vel[0], 0.])

        self.angularSpeed += self.angularAcceleration
        if self.angularSpeedLim is not None:
            if abs(self.angularSpeed) > self.angularSpeedLim:
                self.angularSpeed = self.angularSpeedLim
        self.angularDisplacement += self.angularSpeed + (self.angularAcceleration / 2)
        self.spriteGroup.UpdateCurrent(self.angularDisplacement, self.pos)

    def drawEntity(self, screen: pygame.Surface):
        self.spriteGroup.draw(screen)

    def __contains__(self, target: Entity) -> bool:
        x1, y1, x2, y2 = self.spriteGroup.currentRect.topleft + self.spriteGroup.currentRect.bottomright
        t_x1, t_y1, t_x2, t_y2 = target.spriteGroup.currentRect.topleft + target.spriteGroup.currentRect.bottomright
        # First Check for Rectangular Collision.
        if t_x1 > x2:
            return False
        if t_x2 < x1:
            return False
        if t_y1 > y2:
            return False
        if t_y2 < y1:
            return False

        # If all conditions are not satisfied then the rectangles have collided.
        # Start checking for pixel perfect collision

        targetPos_wrt_self = (t_x1 - x1, t_y1 - y1)
        overlap = self.spriteGroup.currentMask.overlap(target.spriteGroup.currentMask, targetPos_wrt_self)
        if overlap:
            return True
        return False


if __name__ == '__main__':
    from pathlib import Path
    from time import time

    pygame.init()
    screen = pygame.display.set_mode((1280, 720))


    def ImageLoader(File: Path):
        image = pygame.image.load(str(File)).convert_alpha()
        return image


    Ship1ImageGroup = imageGroup.ImageGroup(Path('TestSprite2'), ImageLoader)
    Ship1ImageGroup2 = imageGroup.ImageGroup(Path('TestSprite3'), ImageLoader)
    Ship1Sprite = Sprite.Sprite(Ship1ImageGroup, (1.,1.), 9, (0, 0))
    Ship1Sprite2 = Sprite.Sprite(Ship1ImageGroup2, (1.,1), 9, (0, 0))
    Ship1 = Entity(Ship1Sprite, 0, 0, 0, numpy.array([640., 360.]), velVector=numpy.array([0., 3.]),
                   accVector=numpy.array([0., 0.01]),
                   limPos=numpy.array([[0, 1280], [0, 720]]),
                   limVelScalar=10)
    Ship2ImageGroup = imageGroup.ImageGroup(Path('TestSprite2'), ImageLoader)
    Ship2ImageGroup2 = imageGroup.ImageGroup(Path('TestSprite3'), ImageLoader)
    Ship2Sprite = Sprite.Sprite(Ship2ImageGroup, (1.,1.), 9, (0, 0))
    Ship2Sprite2 = Sprite.Sprite(Ship2ImageGroup2, (1.,1.), 9, (0, 0))
    Ship2 = Entity(Ship2Sprite, 0, 0, 0, numpy.array([360., 640.]), velVector=numpy.array([0., 3.]),
                   limPos=numpy.array([[0, 1280], [0, 720]]))
    print(Ship1 is Ship2)
    running = True
    start = time()
    while running:
        start = time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        Ship1.Update()
        Ship2.Update()
        if Ship1.pos[1] == 720:
            Ship1.vel = numpy.array([0., -3.])
            Ship1.acc = numpy.array([0., -0.01])
            Ship1Sprite2.UpdateCurrent(Ship1.angularDisplacement, Ship1.pos)
            Ship1.spriteGroup = Ship1Sprite2
        elif Ship1.pos[1] == 0:
            Ship1.vel = numpy.array([0., +3.])
            Ship1.acc = numpy.array([0., 0.01])
            Ship1Sprite.UpdateCurrent(Ship1.angularDisplacement, Ship1.pos)
            Ship1.spriteGroup = Ship1Sprite
        if Ship2.pos[1] >= 720:
            Ship2.vel = numpy.array([0., -3.])
            Ship2.spriteGroup = Ship2Sprite2
        elif Ship2.pos[1] <= 0:
            Ship2.vel = numpy.array([0., +3.])
            Ship2.spriteGroup = Ship2Sprite

        screen.fill((0, 0, 0))
        Ship1.drawEntity(screen)
        Ship2.drawEntity(screen)
        pygame.display.flip()
        completedIn = time() - start
        if completedIn >= 1 / 30:
            print(time() - start)
        while time() - start < 1 / 120:
            pass
    pygame.quit()
