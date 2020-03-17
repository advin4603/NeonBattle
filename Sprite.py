import pygame
import imageGroup
import numpy
from typing import Tuple
from math import floor


class Sprite:
    def __init__(self, spriteArray: imageGroup.ImageGroup, scaleConst: Tuple[float, float], updateInterval: int,
                 initPos: Tuple[float, float] = (0, 0)):
        self.origSpriteArray = spriteArray
        self.origSpriteArrayRect = list(self.origSpriteArray.getRect(initPos))
        self.origSpriteMask = self.origSpriteArray.getTransformed(pygame.mask.from_surface)
        self.spriteArray = spriteArray

        def scaler(inSurface: pygame.Surface) -> pygame.Surface:
            dim = inSurface.get_rect()
            return pygame.transform.smoothscale(inSurface, (floor(dim.w * scaleConst[0]), floor(dim.h * scaleConst[1])))

        self.spriteArray.transformAll(scaler)
        self.spriteArrayRect = list(self.spriteArray.getRect(initPos))
        self.spriteArrayMask = self.spriteArray.getTransformed(pygame.mask.from_surface)
        self.updateInterval = updateInterval
        self.counter = self.updateInterval
        self.currentIndex = 0
        self.currentImage = self.spriteArray.imageByIndex(0)
        self.currentRect = self.spriteArrayRect[0]
        self.currentMask = self.origSpriteMask[0]

    def draw(self, screen: pygame.Surface):
        screen.blit(self.currentImage, self.currentRect)

    def UpdateCurrent(self, angle: float, pos: numpy.array):
        self.currentImage, self.currentRect = self.getImageRect()
        if angle % 360 != 0:
            self.currentImage = pygame.transform.rotate(self.currentImage, angle)
            self.currentRect = self.currentImage.get_rect()
            self.currentMask = pygame.mask.from_surface(self.currentImage)
        else:
            self.currentMask = self.spriteArrayMask[self.currentIndex]
        self.currentRect.centerx = pos[0]
        self.currentRect.centery = pos[1]

    def getImageRect(self) -> Tuple[pygame.Surface, pygame.Rect]:
        self.counter -= 1
        if self.counter == 0:
            self.counter = self.updateInterval
            self.currentIndex += 1
            if self.currentIndex >= self.spriteArray.getLen():
                self.currentIndex = 0
        return self.spriteArray.imageByIndex(self.currentIndex), self.spriteArrayRect[self.currentIndex]
