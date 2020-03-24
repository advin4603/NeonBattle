from typing import Tuple, List
import numpy

FPS: int = 60
RESOLUTION: Tuple[float, float] = 1920., 1080.
WINDOWED: bool = False
spacehipUpdateInterval: int = 10  # Time is in number of Frames
spaceshipScaleConst = bulletScaleConst = RESOLUTION[0] / 3840, RESOLUTION[1] / 2160
bulletUpdateInterval: int = 10  # Time is in number of Frames
DEFAULTDAMAGE: float = 0.1
DEFAULTDAMAGEDAMP:float = 0.
SPEEDLIMIT: float = 500/FPS
THRUST: float = -20/FPS
DAMP: float = -THRUST/20
ROTATELIM: float = 540/FPS
ROTATETHRUST: float = 12/FPS
AngularDAMP: float = 0.08
BULLETSPAWNDIST: float = -200
DEFAULTBULLETSPEED: float = -0.10
GameStage: Tuple[List[float], List[float]] = ([0.+200., RESOLUTION[0]-200.], [0.+200., RESOLUTION[1] - 200.])
PowerUpSpawnInterval: int = FPS * 60
PowerUpDespawnInterval: int = FPS * 20
PowerUpSpawnRange: Tuple[int, int] = 2, 5
DEFAULTGRAVITY: numpy.array = numpy.array([0., 0.])
