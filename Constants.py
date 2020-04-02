from typing import Tuple, List
import numpy
from math import floor

FPS: int = 60
RESOLUTION: Tuple[float, float] = 1280., 720.
WINDOWED: bool = False
BLOOM:bool = True
spacehipUpdateInterval: int = 10  # Time is in number of Frames
spaceshipScaleConst = bulletScaleConst = healthBarScaleConst = RESOLUTION[0] / 3840, RESOLUTION[1] / 2160
bulletUpdateInterval: int = 10  # Time is in number of Frames
DEFAULTDAMAGE: float = 0.1
DEFAULTDAMAGEDAMP: float = 1.
SPEEDLIMIT: float = 520 / FPS
THRUST: float = -20 / FPS
DAMP: float = -THRUST / 20
ROTATELIM: float = 540 / FPS
ROTATETHRUST: float = 12 / FPS
AngularDAMP: float = 0.08
BULLETSPAWNDIST: float = -150
DEFAULTBULLETSPEED: float = -2 * SPEEDLIMIT
PowerUpSpawnInterval: int = FPS * 60
PowerUpDespawnInterval: int = FPS * 20
PowerUpSpawnRange: Tuple[int, int] = 2, 5
if RESOLUTION == (1280., 720.):
    healthBarLeftDistance = 50
    healthBarTopDistance = 50
    FRAME = ([65., 1215.], [160, 558])
    BULLETSPAWNDIST:float = -110
    GameStage = FRAME
elif RESOLUTION == (1920., 1080.):
    healthBarLeftDistance = 200
    healthBarTopDistance = 130
    FRAME = ([240.0, 1680.0], [284.0, 796.0])
    GameStage = FRAME

GRAVITYON = False
if GRAVITYON:
    DEFAULTGRAVITY: numpy.array = numpy.array([0., 12 / FPS])
    SPEEDLIMIT: None = None
else:
    DEFAULTGRAVITY: numpy.array = numpy.array([0., 0.])
