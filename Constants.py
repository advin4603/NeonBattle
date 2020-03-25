from typing import Tuple, List
import numpy
from math import floor

FPS: int = 60
RESOLUTION: Tuple[float, float] = 1280.,720.
WINDOWED: bool = False
spacehipUpdateInterval: int = 10  # Time is in number of Frames
spaceshipScaleConst = bulletScaleConst = healthBarScaleConst = RESOLUTION[0] / 3840, RESOLUTION[1] / 2160
bulletUpdateInterval: int = 10  # Time is in number of Frames
DEFAULTDAMAGE: float = 0.1
DEFAULTDAMAGEDAMP: float = 0.
SPEEDLIMIT: float = 520 / FPS
THRUST: float = -20 / FPS
DAMP: float = -THRUST / 20
ROTATELIM: float = 540 / FPS
ROTATETHRUST: float = 12 / FPS
AngularDAMP: float = 0.08
BULLETSPAWNDIST: float = -140
DEFAULTBULLETSPEED: float = -1.5 * SPEEDLIMIT
PowerUpSpawnInterval: int = FPS * 60
PowerUpDespawnInterval: int = FPS * 20
PowerUpSpawnRange: Tuple[int, int] = 2, 5

GRAVITYON = False
if GRAVITYON:
    DEFAULTGRAVITY: numpy.array = numpy.array([0., 12 / FPS])
    SPEEDLIMIT: None = None
else:
    DEFAULTGRAVITY: numpy.array = numpy.array([0., 0.])

FRAME = ([432 * spaceshipScaleConst[0], RESOLUTION[0] - 432 * spaceshipScaleConst[0]],
         [432 * spaceshipScaleConst[1] + spaceshipScaleConst[1] * 156,
          RESOLUTION[1] - 432 * spaceshipScaleConst[1] - +spaceshipScaleConst[1] * 156])
# FRAME = ([2*spaceshipScaleConst[0] * 198 * (2 ** 0.5), RESOLUTION[0] - 2*(spaceshipScaleConst[0] * 198 * (2 ** 0.5))],
#          [spaceshipScaleConst[1] * 198 * (2 ** 0.5) + healthBarScaleConst[1] * (156 + 100),
#           RESOLUTION[1] - (spaceshipScaleConst[1] * 198 * (2 ** 0.5) + healthBarScaleConst[1] * (156 + 100))])

GameStage = FRAME
