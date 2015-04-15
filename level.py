import pygame
import pyganim

import constants
from spritesheet_functions import SpriteSheet

class Level():

    platform_list = None
    destruction_list = None

    background = None

    def __init__(self, screen):
        self.platform_list = pygame.sprite.Group()
        self.destruction_list = pygame.sprite.Group()

        self.screen = screen

        """ Create level 1. """

        self.background = pygame.image.load("background_01.png").convert()
        self.background.set_colorkey((191, 0, 0))
        self.background = pygame.transform.scale2x(self.background)

        self.blockData = Block()
        self.block = BlockIntrinsic(self.blockData)
        self.destructableData = Destructable()
        self.destructable = DestructableIntrinsic(self.destructableData)

        # Holds the level layout in a list of strings.
        self.levelDesign = [
        list("SSDDDDDDDDD"),
        list("SWDWDWDWDWS"),
        list("DDSDSDDDDDD"),
        list("DWDWDWDWDWS"),
        list("SDDDDDDDSDD"),
        list("DWDWDWSWDWS"),
        list("DSDSSDDSSDD"),
        list("DWDWDWDWDWS"),
        list("SDSDDDDDDSS"),
        ]

        # Parse the level string above. W = wall, S = space, D = destructable
        x = y = 0
        for row in self.levelDesign:
            for col in row:
                if col == "D":
                    destructable = DestructableIntrinsic(self.destructableData)
                    destructable.rect.x = -12 + x*96
                    destructable.rect.y = -20 + y*96
                    self.destruction_list.add(destructable)
                if col == "W":
                    block = BlockIntrinsic(self.blockData)
                    block.rect.x = x*96
                    block.rect.y = y*96
                    self.platform_list.add(block)
                x += 1
            y += 1
            x = 0

    def update(self):
        self.platform_list = pygame.sprite.Group()
        self.destruction_list = pygame.sprite.Group()

        # Parse the level string above. W = wall, S = space, D = destructable
        x = y = 0
        for row in self.levelDesign:
            for col in row:
                if col == "D":
                    destructable = DestructableIntrinsic(self.destructableData)
                    destructable.rect.x = -12 + x*96
                    destructable.rect.y = -20 + y*96
                    self.destruction_list.add(destructable)
                if col == "W":
                    block = BlockIntrinsic(self.blockData)
                    block.rect.x = x*96
                    block.rect.y = y*96
                    self.platform_list.add(block)
                x += 1
            y += 1
            x = 0

        """ Update everything in this level."""
        self.platform_list.update()
        self.destruction_list.update()

    def draw(self):
        """ Draw everything on this level. """

        # Draw the background
        # We don't shift the background as much as the sprites are shifted
        # to give a feeling of depth.
        self.screen.fill(constants.LIGHT_BLUE)
        self.screen.blit(self.background,(0,0))

        # Draw all the sprite lists that we have
        x = y = 0
        for row in self.levelDesign:
            for col in row:
                if col == "D":
                    self.screen.blit(self.destructable.image,(96*x - 12, 96*y - 20))
                if col == "W":
                    self.screen.blit(self.block.image,(96*x,96*y))

                x += 1
            y += 1
            x = 0

    screen = None
    levelDesign = []



class Block(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        sprite_sheet = SpriteSheet("spritesheet.png")
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(4, 132, 24, 24)

class BlockIntrinsic(pygame.sprite.Sprite):

    def __init__(self, block):
        super().__init__()
        self.image = block.image
        self.rect = block.image.get_rect()

class Destructable(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        sprite_sheet = SpriteSheet("spritesheet.png")
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(32, 128, 32, 32)

        self.imagesAndDurations = [(sprite_sheet.get_image(32, 96, 32, 32), 0.1),
                                   (sprite_sheet.get_image(63, 96, 32, 32), 0.5)]

class DestructableIntrinsic(pygame.sprite.Sprite):

    def __init__(self, destructable):
        super().__init__()
        self.image = destructable.image
        self.rect = destructable.image.get_rect()

        self.anim = pyganim.PygAnimation(destructable.imagesAndDurations)
        self.anim.loop = False

        self.anim.pause()