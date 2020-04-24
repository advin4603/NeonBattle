import Constants as Cs
import Entities
import GameEntities
import numpy
import pygame

from powerUps import *
from random import choices, randint

from typing import Dict, List, Callable
from pathlib import Path
import sys
from math import floor


def healthBar(model: str, health: float, healthBarCache: Dict, bloomHealthBarCache: Dict = None,
              maxHealth=Cs.DEFAULTMAXHEALTH):
    if model == 'Pink':
        imgs = healthBarCache[model].allImages
        bar, outline = imgs
        outDim = outline.get_rect()
        outDim.center = outDim.w / 2 + Cs.healthBarLeftDistance, outDim.h / 2 + Cs.healthBarTopDistance
        barDim = bar.get_rect()
        bar = pygame.transform.smoothscale(bar, (floor((barDim.w * health) / maxHealth), barDim.h))
        barDim.center = outDim.center
        if Cs.BLOOM:
            if bloomHealthBarCache is None:
                raise Exception('Bloom health Bar not rendered')
            _, bloomOutline = bloomHealthBarCache[model].allImages
            bloomOutDim = bloomOutline.get_rect()
            bloomOutDim.center = outDim.center
            return ((outline, outDim), (bloomOutline, bloomOutDim)), (bar, barDim)
        return (outline, outDim), (bar, barDim)
    elif model == 'Blue':
        imgs = healthBarCache[model].allImages
        bar, outline = imgs
        outDim = outline.get_rect()
        outDim.center = Cs.RESOLUTION[0] - (outDim.w / 2 + Cs.healthBarLeftDistance), \
                        Cs.RESOLUTION[1] - (outDim.h / 2 + Cs.healthBarTopDistance)
        barDim = bar.get_rect()
        bar = pygame.transform.smoothscale(bar, (floor(barDim.w * health/maxHealth), barDim.h))
        barDim.center = outDim.center
        if Cs.BLOOM:
            if bloomHealthBarCache is None:
                raise Exception('Bloom health Bar not rendered')
            _, bloomOutline = bloomHealthBarCache[model].allImages
            bloomOutDim = bloomOutline.get_rect()
            bloomOutDim.center = outDim.center
            return ((outline, outDim), (bloomOutline, bloomOutDim)), (bar, barDim)
        return (outline, outDim), (bar, barDim)


class Manager:
    def __init__(self, display: pygame.Surface, bulletCache: Dict[Path, pygame.Surface], healthBarCache,
                 *args: GameEntities.Spaceship,
                 bloomHealthCache=None,
                 beforeInput: List[Callable] = None,
                 beforeUpdate: List[Callable] = None,
                 beforeCollision: List[Callable] = None,
                 beforeDraw: List[Callable] = None,
                 afterDraw: List[Callable] = None
                 ):
        self.spaceships = list(args)
        self.bullets = []
        self.display = display
        self.PowerUpManager = PowerUpManager()
        self.currentGravity = Cs.DEFAULTGRAVITY
        self.bulletCache = bulletCache
        self.beforeInput = beforeInput if beforeInput is not None else []
        self.beforeUpdate = beforeUpdate if beforeUpdate is not None else []
        self.beforeCollision = beforeCollision if beforeCollision is not None else []
        self.beforeDraw = beforeDraw if beforeDraw is not None else []
        self.afterDraw = afterDraw if afterDraw is not None else []
        self.schedule: List[Callable] = self.beforeInput + [self.InputCheck] + self.beforeUpdate + [
            self.updateAll] + self.beforeCollision + [self.doCollision] + self.beforeDraw + [self.draw] + self.afterDraw
        self.healthBarCache = healthBarCache
        self.bloomHealthCache = bloomHealthCache

        self.scanlines = pygame.Surface((int(Cs.RESOLUTION[0]), int(Cs.RESOLUTION[1]))).convert_alpha()
        self.scanlines.fill((0, 0, 0, 0))
        for j in range(0, int(Cs.RESOLUTION[1]), 4):
            self.scanlines.fill((0, 0, 0, 125), (0, j, Cs.RESOLUTION[0], 2))

    def addBullet(self, bul: GameEntities.Bullet):
        self.bullets.append(bul)

    def InputCheck(self):
        keys = pygame.key.get_pressed()
        events = list(pygame.event.get())
        for ship in self.spaceships:

            for event in events:

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == ship.shootKey:
                        ship.shoot(self, self.bulletCache)

            if keys[ship.thrustKey]:
                ship.thrust()

            else:
                ship.decelerate()

            if keys[ship.leftKey] and not keys[ship.rightKey]:
                ship.rotateLeft()
            elif keys[ship.rightKey] and not keys[ship.leftKey]:

                ship.rotateRight()
            else:
                ship.noRotate()

        if not self.spaceships:
            for event in events:

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def updateAll(self):
        popTheseBullets = []
        for index, entity in enumerate(self.spaceships + self.bullets):
            if isinstance(entity, GameEntities.Bullet):
                if entity.offScreen:
                    popTheseBullets.append(index - len(self.spaceships))
                else:
                    entity.Update(acc=entity.acc + self.currentGravity)
            else:
                entity.Update(acc=entity.acc + self.currentGravity)

        popTheseBullets.sort(reverse=True)
        popTheseBullets = list(set(popTheseBullets))
        for bulletInd in popTheseBullets:
            if bulletInd < len(self.bullets):
                del self.bullets[bulletInd]
        popTheseBullets.clear()
        self.PowerUpManager.updatePowerUps()

    def doCollision(self):

        popTheseBullets = []
        popTheseSpaceships = []
        for index, bullet in enumerate(self.bullets):
            for shipIndex, ent in enumerate(self.spaceships + self.PowerUpManager.spawnedPowerUps):

                if bullet in ent:

                    ent.hit(bullet)
                    if isinstance(ent, GameEntities.Spaceship):
                        if ent.health <= 0:
                            popTheseSpaceships.append(shipIndex)

                    if bullet.killOnImpact:
                        popTheseBullets.append(index)

        for ind in sorted(list(set(popTheseBullets)), reverse=True):
            if ind < len(self.bullets):
                del self.bullets[ind]

        for ind in sorted(list(set(popTheseSpaceships)), reverse=True):
            if ind < len(self.spaceships):
                del self.spaceships[ind]

    def draw(self):
        for ent in self.PowerUpManager.spawnedPowerUps + self.spaceships + self.bullets:
            ent.drawEntity(self.display)
            if isinstance(ent, GameEntities.Spaceship):
                if Cs.BLOOM:
                    (outline, bloomOutline), mainBar = healthBar(ent.model, ent.health,
                                                                 self.healthBarCache,
                                                                 self.bloomHealthCache)
                    self.display.blit(*outline)
                    self.display.blit(*bloomOutline)
                    self.display.blit(*mainBar)
                else:
                    outline, mainBar = healthBar(ent.model, ent.health, self.healthBarCache, maxHealth=ent.maxHealth)
                    self.display.blit(*outline)
                    self.display.blit(*mainBar)
        if Cs.SCANLINES:
            self.display.blit(self.scanlines, (0, 0))

    def completeCycle(self):
        for func in self.schedule:
            func()


class PowerUpManager:
    def __init__(self):
        PowerPath = Path('Assets') / Path('Images') / Path('Sprites') / Path('PowerUps')
        PowerImageFilePaths = PowerPath.rglob('*[0-9].png')
        self.PowerCache = {pth: pygame.image.load(str(pth)).convert_alpha() for pth in PowerImageFilePaths}
        self.Powers = list(PowerUp.__subclasses__())

        def ProbGetter(inPower: PowerUp) -> float:
            return inPower.probability

        self.Probabilities = list(map(ProbGetter, self.Powers))
        self.spawnInterval = Cs.PowerUpSpawnInterval
        self.despawnInterval = Cs.PowerUpDespawnInterval
        self.spawnedPowerUps = []

    def caller(self, n):
        return n(self.PowerCache)

    def updatePowerUps(self):
        if self.despawnInterval == 1:
            self.spawnedPowerUps.clear()
            self.despawnInterval = Cs.PowerUpDespawnInterval
        elif self.spawnedPowerUps:
            self.despawnInterval -= 1
        elif not self.spawnedPowerUps:
            self.despawnInterval = Cs.PowerUpDespawnInterval

        if self.spawnInterval == 1:
            self.spawnedPowerUps.clear()
            self.spawnInterval = Cs.PowerUpSpawnInterval
            # newPowers = choices(self.Powers, self.Probabilities, k=randint(*Cs.PowerUpSpawnRange))
            # newPowers = map(self.caller, newPowers)
            # self.spawnedPowerUps.extend(newPowers)
        else:
            self.spawnInterval -= 1


if __name__ == '__main__':
    try:
        pygame.init()
        clock = pygame.time.Clock()

        screen = pygame.display.set_mode((int(Cs.RESOLUTION[0]), int(Cs.RESOLUTION[1])),
                                         flags=pygame.FULLSCREEN | pygame.HWACCEL | pygame.HWSURFACE | pygame.DOUBLEBUF)
        player1 = GameEntities.PinkSpaceship(numpy.array([Cs.RESOLUTION[0] / 2. - 400, Cs.RESOLUTION[1] / 2 - 400]), 0,
                                             {'THRUST': pygame.K_w, 'LEFT': pygame.K_a, 'RIGHT': pygame.K_d,
                                              'SHOOT': pygame.K_SPACE})
        player2 = GameEntities.BlueSpaceship(numpy.array([Cs.RESOLUTION[0] / 2. + 400, Cs.RESOLUTION[1] / 2 + 400]), 0,
                                             {'THRUST': pygame.K_UP, 'LEFT': pygame.K_LEFT, 'RIGHT': pygame.K_RIGHT,
                                              'SHOOT': pygame.K_RCTRL})
        bulletsPath = Path('Assets') / Path('Images') / Path('Sprites') / Path('Bullet')
        bulletImageFilePaths = bulletsPath.rglob('*[0-9].png')
        bulletCache = {pth: pygame.image.load(str(pth)).convert_alpha() for pth in bulletImageFilePaths}
        healthBarCache: Dict[str, imageGroup.ImageGroup] = {
            'Pink': imageGroup.ImageGroup(Path('Assets/Images/Sprites/HealthBar/Pink/Solid'),
                                          lambda n: pygame.image.load(str(n)).convert_alpha()),
            'Blue': imageGroup.ImageGroup(Path('Assets/Images/Sprites/HealthBar/Blue/Solid'),
                                          lambda n: pygame.image.load(str(n)).convert_alpha())}


        def scaler(inSurface: pygame.Surface):
            dim = inSurface.get_rect()
            return pygame.transform.smoothscale(inSurface, (
                floor(dim.w * Cs.healthBarScaleConst[0]), floor(dim.h * Cs.healthBarScaleConst[1])))


        for model in healthBarCache:
            healthBarCache[model].transformAll(scaler)
        if Cs.BLOOM:
            bloomHealthBarCache: Dict[str, imageGroup.ImageGroup] = {
                'Pink': imageGroup.ImageGroup(Path('Assets/Images/Sprites/HealthBar/Pink/Bloom'),
                                              lambda n: pygame.image.load(str(n)).convert_alpha()),
                'Blue': imageGroup.ImageGroup(Path('Assets/Images/Sprites/HealthBar/Blue/Bloom'),
                                              lambda n: pygame.image.load(str(n)).convert_alpha())}
            for model in bloomHealthBarCache:
                bloomHealthBarCache[model].transformAll(scaler)

            man = Manager(screen, bulletCache, healthBarCache, player1, player2, bloomHealthCache=bloomHealthBarCache)
        else:
            man = Manager(screen, bulletCache, healthBarCache, player1, player2)
        done = False
        while not done:
            screen.fill((0, 0, 0))
            man.completeCycle()
            pygame.display.flip()
            clock.tick(Cs.FPS)
    except Exception as exc:
        print(exc)
        pygame.quit()
        input('Press any button to exit...')
