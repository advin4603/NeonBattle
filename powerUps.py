import Entities
from GameEntities import Bullet
import Sprite
import imageGroup
from pathlib import Path
import Constants as Cs
import pygame
import numpy
from typing import Tuple


class PowerUp(Entities.Entity):
    def __init__(self, pos: numpy.array, model: str, scaleConst: Tuple[float, float], updateInterval: int,
                 probability: float):
        self.model = model
        self.probability = probability
        self.spritePath = Path('Assets') / Path('Images') / Path('Sprites') / Path('PowerUps') / Path(
            self.model) / Path('solid')

        def imageLoader(inPath: Path):
            image = pygame.image.load(str(inPath)).convert_alpha()
            return image

        self.Images = imageGroup.ImageGroup(imageFolderPath=self.spritePath,
                                            imageLoader=imageLoader)
        self.Sprite = Sprite.Sprite(self.Images, scaleConst, updateInterval, (pos[0], pos[1]))
        super().__init__(posVector=pos, sprite=self.Sprite, limPos=numpy.array(Cs.GameStage), angularAcc=0,
                         angularSpeed=0, angularDisplacement=0)

    def hit(self, bullet: Bullet):
        pass
