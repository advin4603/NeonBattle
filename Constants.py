FPS: int = 60
RESOLUTION: tuple = 1280, 720
WINDOWED: bool = False
spacehipUpdateInterval: int = 10  # Time is in number of Frames
spaceshipScaleConst: int = 1
bulletScaleConst: int = 1
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
GameStage = [[0, RESOLUTION[0]], [0, RESOLUTION[1]]]

