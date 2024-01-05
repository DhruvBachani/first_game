import random
import time

import pygame as pg

pg.init()

display_width = 700
display_height = 675
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
lives = 3
points = 0

displayWindow = pg.display.set_mode((display_width, display_height))
pg.display.set_caption('Save the Universe')
shipImg = pg.image.load('ship.png')
laserImg = pg.image.load('lasers.png')
backImg = pg.image.load('background.jpg')
laser_sound = pg.mixer.Sound('Laser-SoundBible.com-602495617.wav')
crash_sound = pg.mixer.Sound('crash.wav')
gameover_sound = pg.mixer.Sound('gameover.wav')
background_sound = pg.mixer.Sound('backmusic.wav')

clock = pg.time.Clock()


def displayMessage(text, color, background,t):
    font = pg.font.Font('freesansbold.ttf', 32)
    textSurf, textRect = text_objects(text, font, color, background)
    textRect.center = ((display_width / 2), (display_height / 2))
    displayWindow.blit(textSurf, textRect)
    pg.display.update()
    time.sleep(t)


def block(blockx, blocky):
    blockImg = pg.image.load('block.jpg')
    displayWindow.blit(blockImg, (blockx, blocky))


def text_objects(text, font, color, background):
    textSurf = font.render(text, True, color, background)
    return textSurf, textSurf.get_rect()


def button(msg, size, x, y, w, h, incolor, accolor, action=None):
    global lives
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pg.draw.rect(displayWindow, accolor, [x, y, w, h])
        fcolor = black
        if click[0] == 1 and action != None:
            if action == 'play':
                displayWindow.fill(white)

                displayMessage('Lives:  ' + str(lives), red, blue,1.5)
                gameloop()

            elif action == 'quit':
                pg.quit()
                quit()
    else:
        pg.draw.rect(displayWindow, incolor, [x, y, w, h])
        fcolor = white

    font = pg.font.Font('freesansbold.ttf', size)
    textSurf, textRect = text_objects(msg, font, fcolor, None)
    textRect.center = (x + w / 2, y + h / 2)
    displayWindow.blit(textSurf, textRect)


def crashscreen():
    pg.mixer.Sound.play(gameover_sound)
    pg.mixer.music.stop()
    displayWindow.fill(white)
    displayMessage("Score is : " + str(int(points)), black, None,3)
    intro()


def pointsystem():
    global points
    points += 0.05
    font = pg.font.Font('freesansbold.ttf', 14)
    textSurf, textRect = text_objects('Points : ' + str(int(points)), font, white, None)
    textRect.center = (display_width / 2, 7)
    displayWindow.blit(textSurf, textRect)


def intro():
    intr = True
    global lives, points
    lives = 3
    points = 0

    while intr:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        displayWindow.blit(backImg, (0, 0))
        font = pg.font.Font('freesansbold.ttf', 50)
        textSurf, textRect = text_objects('Save the Universe..!!!', font, white, None)
        textRect.center = ((display_width / 1.9), (display_height / 4))
        displayWindow.blit(textSurf, textRect)

        button('Yes, I\'m in', 20, 300, 275, 100, 50, red, green, 'play')
        button('Nah, not now!', 15, 300, 375, 100, 50, red, green, 'quit')
        button('Options', 20, 300, 475, 100, 50, red, green)

        pg.display.update()


def gameloop():
    x, y = 306, 505
    x_change = 0
    laserx_change, lasery_change = 0, 0
    crashed = False
    global lives, points

    block_startx = random.randrange(0, display_width)
    block_starty = 0
    block_speed = 4
    laser_startx = 0
    laser_starty = 487



    while not crashed:
        displayWindow.blit(backImg, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                crashed = True
                pg.quit()
                quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    x_change = 10

                elif event.key == pg.K_LEFT:
                    x_change = -10

                elif event.key == pg.K_SPACE:
                    lasery_change = 7
                    pg.mixer.Sound.play(laser_sound)
                    pg.mixer.music.stop()

            if event.type == pg.KEYUP:
                x_change = 0

        x += x_change
        block_speed += 0.001

        block(block_startx, block_starty)

        laser_starty -= lasery_change
        block_starty += block_speed
        displayWindow.blit(shipImg, (x, y))
        pointsystem()

        if x > 613 or x < 0:
            lives -= 1
            pg.mixer.Sound.play(crash_sound)
            pg.mixer.music.stop()
            displayMessage('Crashed..!!   Lives remaining:  ' + str(lives), red, blue,1.5)
            gameloop()
        if laser_starty < -60:
            laser_starty = 487
            lasery_change = 0
        if laser_starty == 487:
            laser_startx = x + 20
        if block_starty > display_height:
            block_starty = -100
            block_startx = random.randrange(0, display_width)
        if laser_starty < block_starty + 87 and laser_starty < 487:
            if (block_startx < laser_startx < block_startx + 87) or (
                    block_startx < laser_startx + 47 < block_startx + 87):
                block_starty = -100
                block_startx = random.randrange(0, display_width)
                laser_starty = 487
                lasery_change = 0
                points += 5

        if y < block_starty + 87:
            if (block_startx < x < block_startx + 87) or (block_startx < x + 87 < block_startx + 87):
                lives -= 1
                pg.mixer.Sound.play(crash_sound)
                pg.mixer.music.stop()
                displayMessage('Crashed..!!   Lives remaining:  ' + str(lives), red, blue,1.5)
                gameloop()
        if lives == 0:
            crashscreen()
        displayWindow.blit(laserImg, (laser_startx, laser_starty))
        pg.display.update()
        clock.tick(90)


intro()
