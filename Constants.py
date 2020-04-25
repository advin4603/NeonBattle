from typing import Tuple, List, Union, Dict
import numpy
from math import floor
from Reader import reader
from random import uniform
from math import pi

settings: Union[Dict[str, bool], Dict[str, None]] = reader('Settings.txt')
FPS: int = 60
RESOLUTION: Tuple[float, float] = 1280., 720.

CRT: bool
if 'CRT EFFECT' in settings and settings['CRT EFFECT'] is not None:
    CRT = settings['CRT EFFECT']
else:
    CRT = False

SCANLINES: bool
if 'SCANLINES' in settings and settings['SCANLINES'] is not None:
    SCANLINES = settings['SCANLINES']
else:
    SCANLINES = CRT

WINDOWED: bool
if 'FULLSCREEN' in settings and settings['FULLSCREEN'] is not None:
    WINDOWED = not settings['FULLSCREEN']
else:
    WINDOWED = False

BLOOM: bool
if 'BLOOM' in settings and settings['FULLSCREEN'] is not None:
    BLOOM = settings['BLOOM']
else:
    BLOOM = False

spacehipUpdateInterval: int = 10  # Time is in number of Frames
spaceshipScaleConst = bulletScaleConst = healthBarScaleConst = RESOLUTION[0] / 3840, RESOLUTION[1] / 2160
bulletUpdateInterval: int = 10  # Time is in number of Frames
DEFAULTMAXHEALTH = 100
DEFAULTDAMAGE: float = 1
DEFAULTDAMAGEDAMP: float = 1.
SPEEDLIMIT: float = 520 / FPS
THRUST: float = -20 / FPS
DAMP: float = -THRUST / 20
ROTATELIM: float = 540 / FPS
ROTATETHRUST: float = 12 / FPS
AngularDAMP: float = 0.08
BULLETSPAWNDIST: float = -150
BULLETSPEEDLIMIT:float = 3 * SPEEDLIMIT
DEFAULTBULLETSPEED: float = -2 * SPEEDLIMIT
GRAVBULLETSPEED:float = -3 * SPEEDLIMIT
PowerUpSpawnInterval: int = FPS * 1
PowerUpDespawnInterval: int = FPS * 20
PowerUpSpawnRange: Tuple[int, int] = 2, 5
HEALTHPOWER = 0.5

if RESOLUTION == (1280., 720.):
    healthBarLeftDistance = 50
    healthBarTopDistance = 50
    FRAME = ([65., 1215.], [160, 558])
    BULLETSPAWNDIST: float = -110
    GameStage = FRAME
elif RESOLUTION == (1920., 1080.):
    healthBarLeftDistance = 200
    healthBarTopDistance = 130
    FRAME = ([240.0, 1680.0], [284.0, 796.0])
    GameStage = FRAME

GRAVITYON: bool
if 'GRAVITY' in settings and settings['GRAVITY'] is not None:
    GRAVITYON = settings['GRAVITY']
else:
    GRAVITYON = False
DEFAULTGRAVITY: numpy.array = numpy.array([0., 12 / FPS])
GRAVSCALAR = numpy.sqrt(DEFAULTGRAVITY.dot(DEFAULTGRAVITY))


if GRAVITYON:
    gravDir = uniform(0, 2 * pi)
    DEFAULTGRAVITY: numpy.array = GRAVSCALAR * numpy.array([numpy.cos(gravDir), numpy.sin(gravDir)])
    SPEEDLIMIT: None = None
else:
    DEFAULTGRAVITY: numpy.array = numpy.array([0., 0.])

# Power Up Probabilities
Health = 10
RandomGravity = 2
