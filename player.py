import pygame
import pyganim

import constants

class Player(pygame.sprite.Sprite):

    direction = constants.DOWN

    dead = False

    x_pos = 0
    y_pos = 0
    move_speed = 0
    move_speed_AI = 1
    moving = False

    moving_up = moving_left = moving_right = moving_down = False

    animObjs = {}

    level = None
    bombs = None

    bombNum = 1
    bombSize = 3

    def __init__(self, spritesheet, screen):

        super().__init__()

        # load the "idle" sprites
        self.front_idle = spritesheet.get_image(0, 64, 24, 32)
        self.back_idle = spritesheet.get_image(0, 0, 24, 32)
        self.left_idle = spritesheet.get_image(64, 32, 24, 32)
        self.right_idle = pygame.transform.flip(self.left_idle, True, False)

        self.image = self.front_idle.copy()
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-20, -50)
        self.bombs = []

        self.screen = screen

        # creating the PygAnimation objects for walking/running in all directions
        animTypes = 'back_walk left_walk front_walk'.split()
        row = -1
        for animType in animTypes:
            row += 1
            imagesAndDurations = [(spritesheet.get_image(32*num, 32*row, 24, 32), 0.1) for num in range(6)]
            self.animObjs[animType] = pyganim.PygAnimation(imagesAndDurations)
        self.animObjs['death'] = pyganim.PygAnimation([(spritesheet.get_image(192 + 32*num, 0, 28, 24), 0.3) for num in range(5)])
        self.animObjs['death'].loop = False

        # create the right-facing sprites by copying and flipping the left-facing sprites
        self.animObjs['right_walk'] = self.animObjs['left_walk'].getCopy()
        self.animObjs['right_walk'].flip(True, False)
        self.animObjs['right_walk'].makeTransformsPermanent()

        self.moveConductor = pyganim.PygConductor(self.animObjs)

    def update(self, level):
        if not self.dead:
            if (self.moving_up or self.moving_down or self.moving_left or self.moving_right) == True:
                self.move()

                if self.rect.left < 0:
                    self.rect.left = 0
                elif self.rect.right > constants.SCREEN_WIDTH:
                    self.rect.right = constants.SCREEN_WIDTH

                if self.rect.top < 0:
                    self.rect.top = 0
                elif self.rect.bottom > constants.SCREEN_HEIGHT:
                    self.rect.bottom = constants.SCREEN_HEIGHT

                # See if we hit anything
                block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
                block_hit_list = block_hit_list + pygame.sprite.spritecollide(self, self.level.destruction_list, False)
                for block in block_hit_list:
                    # If we are moving right,
                    # set our right side to the left side of the item we hit
                    if self.moving_right == True and self.rect.right < block.rect.left + 10:
                        self.rect.right = block.rect.left

                    elif self.moving_left == True  and self.rect.left > block.rect.right - 10:
                        self.rect.left = block.rect.right

                    elif self.moving_down == True:
                        self.rect.bottom = block.rect.top

                    elif self.moving_up == True:
                        self.rect.top = block.rect.bottom

            self.bomb_hit_list = pygame.sprite.spritecollide(self, self.bombs, False)
            for bomb in self.bombs:
                self.bomb_hit_list += pygame.sprite.spritecollide(self, bomb.explosionList, False)
            for bomb_hit in self.bomb_hit_list:
                if bomb_hit.existent == True and bomb_hit.anim.currentFrameNum >= 2:
                    self.dead = True
                    self.rect.x = -201


    def stop(self):
        self.move_speed = 0

    def draw(self):
        if self.dead == False:
            if self.moving_up == True:
                self.animObjs['back_walk'].blit(self.screen, (self.x_pos, self.y_pos))

            elif self.moving_down == True:
                self.animObjs['front_walk'].blit(self.screen, (self.x_pos, self.y_pos))

            elif self.moving_left == True:
                self.animObjs['left_walk'].blit(self.screen, (self.x_pos, self.y_pos))

            elif self.moving_right == True:
                self.animObjs['right_walk'].blit(self.screen, (self.x_pos, self.y_pos))

            elif self.direction == constants.UP:
                self.screen.blit(self.back_idle, (self.x_pos, self.y_pos))
            elif self.direction == constants.DOWN:
                self.screen.blit(self.front_idle, (self.x_pos, self.y_pos))
            elif self.direction == constants.LEFT:
                self.screen.blit(self.left_idle, (self.x_pos, self.y_pos))
            elif self.direction == constants.RIGHT:
                self.screen.blit(self.right_idle, (self.x_pos, self.y_pos))

        else:
            self.animObjs['death'].blit(self.screen, (self.x_pos, self.y_pos))

    def move(self):
        self.move_speed = constants.SPEED * self.move_speed_AI

        if self.moving_up == True:
            self.rect.y -= self.move_speed
            self.moveConductor.play()

        if self.moving_down == True:
            self.rect.y += self.move_speed
            self.moveConductor.play()

        if self.moving_left == True:
            self.rect.x -= self.move_speed
            self.moveConductor.play()

        if self.moving_right == True:
            self.rect.x += self.move_speed
            self.moveConductor.play()

        self.x_pos = self.rect.x - 10
        self.y_pos = self.rect.y - 50