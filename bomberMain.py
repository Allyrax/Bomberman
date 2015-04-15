import pygame
from pygame.locals import *
import socket
import pyganim
import constants

from spritesheet_functions import SpriteSheet
from player import Player
from bomb import *
from level import Level
import time
import errno

def main():
    #networking code

    TCP_IP = '127.0.0.1'
    TCP_PORT = 2003
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.setblocking(0)

    pygame.init()

    size = [constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption('Bomberman')

    sprite_sheet = SpriteSheet("spritesheet.png")

    level = Level(screen)

    player = Player(sprite_sheet, screen)
    player.level = level

    player2 = Player(sprite_sheet, screen)
    player2.level = level
    player2.moveConductor.play()
    player2.move_speed_AI = 0



    #wait for a start message from the server
    dataDecoded = ""
    while not (dataDecoded == "player1" or dataDecoded == "player2"):

        try:
            data = s.recv(BUFFER_SIZE)
        except:
            time.sleep(0.1)
            continue

        dataDecoded = data.decode('utf-8')
        dataDecoded = dataDecoded.split(',')[0]
        print ("received data:", dataDecoded)
        time.sleep(0.1)

    if dataDecoded == "player1":
        player.rect.x = 960
        player.rect.y = 750
        player.move()

    if dataDecoded == "player2":
        player2.rect.x = 960
        player2.rect.y = 750
        player2.move()

    mainClock = pygame.time.Clock()

    active_sprite_list = pygame.sprite.Group()

    active_sprite_list.add(player)
    active_sprite_list.add(player2)

    bomb_list = []
    bombData = BombData(sprite_sheet)
    explosionData = ExplosionData(sprite_sheet)
    bomb_count = 0
    player2.bombs = bomb_list

    done = False

    # This is a font we use to draw text on the screen (size 36)
    font = pygame.font.Font(None, 150)

    bomb_placed = 0
    game_over = False
    data = '0,0,0'.encode('utf-8')

    while not done:

        MESSAGE = str(player.rect.x) + ',' + str(player.rect.y) + ',' + str(bomb_placed) + ','
        bytesMessage = MESSAGE.encode('utf-8')

        try:
            s.send(bytesMessage)

            data = s.recv(BUFFER_SIZE)
            dataOld = data

        except ConnectionAbortedError:
            print("The server has shut down")
            done = True

        except:
            pass
        dataDecoded = data.decode('utf-8')
        print (dataDecoded)
        player2Data = dataDecoded.split(',')

        old_x_pos = player2.rect.x
        old_y_pos = player2.rect.y

        try:
            if dataDecoded[0] == "quit":
                s.close()
                break

            if player2Data[0].startswith('-') and player2Data[0][1:].isdigit() or player2Data[0].isdigit():
                player2.rect.x = int(player2Data[0])
                if int(player2Data[0]) == -201:
                    player2.dead
            else:
                player2Data[0] = 0
            player2.rect.y = int(player2Data[1])

            player2.move()

            if int(player2Data[2]) == 1:
                bomb_list.insert(0, (Bomb(screen, player2.x_pos, player2.y_pos, bombData, explosionData, player2, level)))
                bomb_count += 1
                if bomb_count > 25:
                    bomb_list.pop()
                player.bombs = bomb_list
                player2.bombs = bomb_list

            if player2.rect.x > old_x_pos:
                player2.direction = constants.RIGHT
                player2.moving_right = True

            elif player2.rect.x < old_x_pos:
                player2.direction = constants.LEFT
                player2.moving_left = True

            if player2.rect.y > old_y_pos:
                player2.direction = constants.DOWN
                player2.moving_down = True

            elif player2.rect.y < old_y_pos:
                player2.direction = constants.UP
                player2.moving_up = True

            if player2.rect.x == old_x_pos:
                player2.stop()
                player2.moving_left = False
                player2.moving_right = False

            if player2.rect.y == old_y_pos:
                player2.stop()
                player2.moving_up = False
                player2.moving_down = False

        except:
            done = True
            print ("The server has terminated")

        bomb_placed = 0


        for event in pygame.event.get(): # event handling loop
            # handle ending the program
            if event.type == pygame.QUIT:
                done = True

            elif event.type == KEYDOWN:

                if event.key == K_UP:
                    player.direction = constants.UP
                    player.moving_up = True

                if event.key == K_DOWN:
                    player.direction = constants.DOWN
                    player.moving_down = True

                if event.key == K_LEFT:
                    player.direction = constants.LEFT
                    player.moving_left = True

                if event.key == K_RIGHT:
                    player.direction = constants.RIGHT
                    player.moving_right = True

                if event.key == K_SPACE:
                    bomb_list.insert(0, (Bomb(screen, player.x_pos, player.y_pos, bombData, explosionData, player, level)))
                    bomb_count += 1
                    if bomb_count > 50:
                        bomb_list.pop()
                    player.bombs = bomb_list
                    player2.bombs = bomb_list
                    bomb_placed = 1

            elif event.type == KEYUP:
                if event.key == K_UP:
                    player.stop()
                    player.moving_up = False

                elif event.key == K_DOWN:
                    player.stop()
                    player.moving_down = False

                elif event.key == K_LEFT:
                    player.stop()
                    player.moving_left = False

                elif event.key == K_RIGHT:
                    player.stop()
                    player.moving_right = False

        #drawing
        screen.fill(constants.BLACK)

        if not game_over:
            player.update(level)
            player2.update(level)
            level.update()

        level.draw()

        if player.dead and player2.dead:
            text = font.render("It's a Draw", True, constants.WHITE)
            game_over = True

        elif player.dead:
            text = font.render("Player 2 Wins", True, constants.WHITE)
            game_over = True

        elif player2.dead:
            text = font.render("Player 1 Wins", True, constants.WHITE)
            game_over = True

        if game_over:
            text_rect = text.get_rect()
            text_x = screen.get_width() / 2 - text_rect.width / 2
            text_y = screen.get_height() / 2 - text_rect.height / 2
            screen.blit(text, [text_x, text_y])

        for bomb in range(len(bomb_list)):
            bomb_list[bomb].update(level)
            bomb_list[bomb].draw()
        player.draw()
        player2.draw()

        mainClock.tick(60)

        pygame.display.flip()



    #close socket
    print("Quiting")
    MESSAGE = "quit"
    bytesMessage = MESSAGE.encode('utf-8')

    try:
        s.send(bytesMessage)
    except ConnectionAbortedError:
        pass
    s.close()
    pygame.quit()

if __name__ == "__main__":
    main()

