from pathlib import Path
from typing import Callable, Tuple


class ImageGroup:
    def __init__(self, imageFolderPath: Path, imageLoader: Callable):
        print(imageFolderPath)
        self.allImageFilePaths = list(imageFolderPath.glob('*[0-9].png'))
        print(self.allImageFilePaths)
        self.allImages = list(map(imageLoader, self.allImageFilePaths))
        if not self.allImages:
            raise Exception('Image Not Found')

    def transformAll(self, func: Callable):
        self.allImages = list(map(func, self.allImages))

    def getTransformed(self, func: Callable):
        return list(map(func, self.allImages))

    def getRect(self, initPos: Tuple[float, float]):
        def funcRect(inImage):
            currentRect = inImage.get_rect()
            currentRect.center = initPos
            return currentRect

        return map(funcRect, self.allImages)

    def imageByIndex(self, index: int):
        return self.allImages[index]

    def getLen(self) -> int:
        return len(self.allImages)
