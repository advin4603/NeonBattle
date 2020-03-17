from typing import Tuple, List
import numpy

FPS: int = 60
RESOLUTION: Tuple[float, float] = 1280., 720.
WINDOWED: bool = False
spacehipUpdateInterval: int = 10  # Time is in number of Frames
spaceshipScaleConst: Tuple[float, float] = 1., 1.
bulletScaleConst: Tuple[float, float] = 1., 1.
bulletUpdateInterval: int = 10  # Time is in number of Frames
DEFAULTDAMAGE: float = 0.1
SPEEDLIMIT: float = RESOLUTION[0] / 32
THRUST: float = 0.1
DAMP: float = 0.1
ROTATELIM: int = 90
ROTATETHRUST: float = 0.1
AngularDAMP: float = 0.2
BULLETSPAWNDIST: float = 5
DEFAULTBULLETSPEED: float = 10.
GameStage: Tuple[List[float], List[float]] = ([0., RESOLUTION[0]], [0., RESOLUTION[1]])
PowerUpSpawnInterval: int = FPS * 60
PowerUpDespawnInterval: int = FPS * 20
PowerUpSpawnRange: Tuple[int, int] = 2, 5
DEFAULTGRAVITY: numpy.array = numpy.array([0., 0.])
