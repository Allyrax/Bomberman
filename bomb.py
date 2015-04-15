import pygame
import pyganim

import constants

class BombData(pygame.sprite.Sprite):
    def __init__(self, spritesheet):
        super().__init__()

        self.idle = spritesheet.get_image(0, 64, 24, 32)

        self.image = self.idle.copy()

        self.imagesAndDurations = [(spritesheet.get_image(32*num, 96, 32, 32), 0.1) for num in range(9)]
        self.imagesAndDurations.insert(0, (spritesheet.get_image(0, 96, 32, 32), 0.5))
        self.imagesAndDurations.insert(1, (spritesheet.get_image(32, 96, 32, 32), 0.5))

class Bomb(pygame.sprite.Sprite):

    existent = True

    explode = False

    explosionList = []

    level = []

    def __init__(self, screen, x, y, bombData, explosionData, player, level):

        self.explosionData = explosionData
        self.player = player

        self.image = bombData.image
        self.rect = bombData.image.get_rect()
        self.rect.x = int(96 * round(float(x)/96)) - 15
        self.rect.y = int(96 * round(float(y + 40)/96)) - 20

        self.screen = screen
        self.level  = level

        self.anim = pyganim.PygAnimation(bombData.imagesAndDurations)
        self.anim.loop = False

        self.anim.play()

    def draw(self):
        self.anim.blit(self.screen, (self.rect.x, self.rect.y))
        if self.anim.isFinished():
            self.existent = False

    def update(self, level):
        if self.anim.currentFrameNum == 2 and not self.explode:
            self.addExplosions(level)


        if self.anim.currentFrameNum >= 2:
            for explosion in self.explosionList:
                explosion.draw()

    def addExplosions(self, level):
        x_index = int(self.rect.x/96 + 1)
        y_index = int(self.rect.y/96 + 1)
        self.explode = True

        #to the left of the bomb
        for x in range(self.player.bombSize):
            new_x_index = x_index - x - 1
            hit = False

            if new_x_index >= 0 and new_x_index <=10 and y_index >= 0 and y_index <=8:
                value = self.level.levelDesign[y_index][new_x_index]
                if value == "D":
                    newExplosion = Explosion(self.explosionData, self, level, self.rect.x - 96 - 96*x, self.rect.y)
                    self.explosionList.append(newExplosion)

                    self.level.levelDesign[y_index][new_x_index] = "S"
                    break
                elif value == "S":
                    newExplosion = Explosion(self.explosionData, self, level, self.rect.x - 96 - 96*x, self.rect.y)
                    self.explosionList.append(newExplosion)
                elif value == "W":
                    break

        #to the right of the bomb
        for x in range(self.player.bombSize):
            new_x_index = x_index + x + 1
            hit = False

            if new_x_index >= 0 and new_x_index <=10 and y_index >= 0 and y_index <=8:
                value = self.level.levelDesign[y_index][new_x_index]

                if value == "D":
                    newExplosion = Explosion(self.explosionData, self, level, self.rect.x + 96 + 96*x, self.rect.y)
                    self.explosionList.append(newExplosion)

                    self.level.levelDesign[y_index][new_x_index] = "S"
                    break
                elif value == "S":
                    newExplosion = Explosion(self.explosionData, self, level, self.rect.x + 96 + 96*x, self.rect.y)
                    self.explosionList.append(newExplosion)
                elif value == "W":
                    break

        #to the top of the bomb
        for y in range(self.player.bombSize):
            new_y_index = y_index - y -1
            hit = False

            if x_index >= 0 and x_index <=10 and new_y_index >= 0 and new_y_index <=8:
                value = self.level.levelDesign[new_y_index][x_index]
                if value == "D":
                    newExplosion = Explosion(self.explosionData, self, level, self.rect.x, self.rect.y - 96 - 96*y)
                    self.explosionList.append(newExplosion)

                    self.level.levelDesign[new_y_index][x_index] = "S"
                    break
                elif value == "S":
                    newExplosion = Explosion(self.explosionData, self, level, self.rect.x, self.rect.y - 96 - 96*y)
                    self.explosionList.append(newExplosion)
                elif value == "W":
                    break

        #to the bottom of the bomb
        for y in range(self.player.bombSize):
            new_y_index = y_index + y + 1
            hit = False

            if x_index >= 0 and x_index <=10 and new_y_index >= 0 and new_y_index <=8:
                value = self.level.levelDesign[new_y_index][x_index]

                if value == "D":
                    newExplosion = Explosion(self.explosionData, self, level, self.rect.x, self.rect.y + 96 + 96*y)
                    self.explosionList.append(newExplosion)
                    self.level.levelDesign[new_y_index][x_index] = "S"
                    break
                elif value == "S":
                    newExplosion = Explosion(self.explosionData, self, level, self.rect.x, self.rect.y + 96 + 96*y)
                    self.explosionList.append(newExplosion)
                elif value == "W":
                    break

import pygame
import pyganim

import constants

class ExplosionData(pygame.sprite.Sprite):
    def __init__(self, spritesheet):
        super().__init__()

        self.idle = spritesheet.get_image(0, 64, 24, 32)

        self.image = self.idle.copy()

        self.imagesAndDurations = [(spritesheet.get_image(64 + 32*num, 96, 32, 32), 0.1) for num in range(7)]

class Explosion(pygame.sprite.Sprite):

    existent = True
    hit = False

    def __init__(self, explosionData, bomb, level, x, y):
        self.level = level

        self.image = explosionData.image
        self.rect = explosionData.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.screen = bomb.screen

        self.anim = pyganim.PygAnimation(explosionData.imagesAndDurations)
        self.anim.loop = False

        self.anim.play()

    def draw(self):
        self.anim.blit(self.screen, (self.rect.x, self.rect.y))
        if self.anim.isFinished():
            self.existent = False