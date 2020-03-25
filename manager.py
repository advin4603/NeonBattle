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


class Manager:
    def __init__(self, display: pygame.Surface, bulletCache: Dict[Path, pygame.Surface], *args: GameEntities.Spaceship,
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

    def updateAll(self):
        popTheseBullets = []
        popTheseSpaceships = []
        for index, entity in enumerate(self.spaceships + self.bullets):
            if isinstance(entity, GameEntities.Bullet):
                if entity.offScreen:
                    popTheseBullets.append(index - len(self.spaceships))
                else:
                    entity.Update(acc=entity.acc + self.currentGravity)
            else:
                if entity.health <= 0:
                    popTheseSpaceships.append(index)
                else:
                    entity.Update(acc=entity.acc + self.currentGravity)

        popTheseBullets.sort(reverse=True)
        for bulletInd in popTheseBullets:
            del self.bullets[bulletInd]
        popTheseBullets.clear()

        popTheseSpaceships.sort(reverse=True)
        for shipInd in popTheseBullets:
            del self.spaceships[shipInd]
        popTheseSpaceships.clear()

        # self.PowerUpManager.updatePowerUps()

    def doCollision(self):
        popThese = []
        for index, bullet in enumerate(self.bullets):
            for ent in self.spaceships + self.PowerUpManager.spawnedPowerUps:
                if bullet in ent:
                    ent.hit(bullet)
                    if bullet.killOnImpact:
                        popThese.append(index)

        for ind in sorted(popThese, reverse=True):
            del self.bullets[ind]

    def draw(self):
        for ent in self.PowerUpManager.spawnedPowerUps + self.spaceships + self.bullets:
            ent.drawEntity(self.display)

    def completeCycle(self):
        for func in self.schedule:
            func()


class PowerUpManager:
    def __init__(self):
        self.Powers = list(PowerUp.__subclasses__())

        def ProbGetter(inPower: PowerUp) -> float:
            return inPower.probability

        self.Probabilities = map(ProbGetter, self.Powers)
        self.spawnInterval = Cs.PowerUpSpawnInterval
        self.despawnInterval = Cs.PowerUpDespawnInterval
        self.spawnedPowerUps = []

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
            # self.spawnedPowerUps.extend(choices(self.Powers, self.Probabilities, k=randint(*Cs.PowerUpSpawnRange)))
        else:
            self.spawnInterval -= 1


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((int(Cs.RESOLUTION[0]), int(Cs.RESOLUTION[1])),
                                     flags=pygame.FULLSCREEN | pygame.HWACCEL | pygame.HWSURFACE | pygame.DOUBLEBUF)
    player1 = GameEntities.PinkSpaceship(numpy.array([1920 / 2. + 400, 1080 / 2 + 400]), 0,
                                         {'THRUST': pygame.K_w, 'LEFT': pygame.K_a, 'RIGHT': pygame.K_d,
                                          'SHOOT': pygame.K_SPACE})
    player2 = GameEntities.BlueSpaceship(numpy.array([1920 / 2. - 400, 1080 / 2 - 400]), 0,
                                         {'THRUST': pygame.K_UP, 'LEFT': pygame.K_LEFT, 'RIGHT': pygame.K_RIGHT,
                                          'SHOOT': pygame.K_RCTRL})
    bulletsPath = Path('Assets') / Path('Images') / Path('Sprites') / Path('Bullet')
    bulletImageFilePaths = bulletsPath.rglob('*[0-9].png')
    bulletCache = {pth: pygame.image.load(str(pth)).convert_alpha() for pth in bulletImageFilePaths}
    man = Manager(screen, bulletCache, player1, player2)
    done = False
    print(player1.spriteGroup.currentRect.h)
    while not done:

        screen.fill((0, 0, 0))
        man.completeCycle()
        print(player1.pos)

        pygame.display.flip()
        clock.tick(Cs.FPS)
