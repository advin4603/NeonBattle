import Entities
from GameEntities import Bullet
import Sprite
import imageGroup
from pathlib import Path
import Constants as Cs
import pygame
import numpy
from typing import Tuple, Dict
from random import uniform


# PowerPath = Path('Assets') / Path('Images') / Path('Sprites') / Path('PowerUps')
# PowerImageFilePaths = PowerPath.rglob('*[0-9].png')
# PowerCache = {pth: pygame.image.load(str(pth)).convert_alpha() for pth in PowerImageFilePaths}

class PowerUp(Entities.Entity):
    def __init__(self, pos: numpy.array, model: str, scaleConst: Tuple[float, float], updateInterval: int,
                 probability: float, powerCache: Dict):
        self.model = model
        self.probability = probability
        self.spritePath = Path('Assets') / Path('Images') / Path('Sprites') / Path('PowerUps') / Path(
            self.model) / Path('Solid')
        self.powerCache = powerCache

        def imageLoader(inPath: Path):
            image = self.powerCache[inPath]
            return image

        self.Images = imageGroup.ImageGroup(imageFolderPath=self.spritePath,
                                            imageLoader=imageLoader)
        self.Sprite = Sprite.Sprite(self.Images, scaleConst, updateInterval, (pos[0], pos[1]))
        if Cs.BLOOM:
            self.bloomPath = Path('Assets') / Path('Images') / Path('Sprites') / Path('PowerUps') / Path(
                self.model) / Path('Bloom')
            self.bloomImages = imageGroup.ImageGroup(imageFolderPath=self.bloomPath, imageLoader=imageLoader)
            self.bloomSprite = Sprite.Sprite(self.bloomImages, scaleConst, updateInterval, (pos[0], pos[1]))
        super().__init__(posVector=pos, sprite=self.Sprite, limPos=numpy.array(Cs.GameStage), angularAcc=0,
                         angularSpeed=0, angularDisplacement=0)

    def drawEntity(self, screen: pygame.Surface):
        super().drawEntity(screen)
        if Cs.BLOOM:
            self.bloomSprite.draw(screen)

    def hit(self, bullet: Bullet):
        pass


class Health(PowerUp):
    probability = 10
    def __init__(self, powerCache):
        self.model = 'Health'
        self.spawnRangeX = Cs.GameStage[0]
        self.spawnRangeY = Cs.GameStage[1]
        self.probability = 10
        self.x = uniform(*self.spawnRangeX)
        self.y = uniform(*self.spawnRangeY)
        self.healBy = 0.5
        super().__init__(numpy.array([self.x, self.y]), self.model, Cs.bulletScaleConst, 1, self.probability,
                         powerCache)

    def hit(self, bullet: Bullet):
        bullet.parent.health += (1 - bullet.parent.health) * self.healBy
