# Write your code here :-)
import random
import math
from pgzhelper import *

WIDTH = 800
HEIGHT = 600

alien = Actor('alien')
alien.x = 400
alien.y = 300
alien.hspeed = 0
alien.vspeed = 0

MENU = True
GAME = False

def start_game():
    global GAME
    global MENU
    music.play('newdawn')
    GAME = True
    MENU = False
    return

currentlevel = 1
bulletlist = []

def draw():
    screen.clear()
    screen.blit('spacebackground',(0,0))
    if MENU:
        screen.draw.text("Click to continue", midbottom=(400,300), width=360, fontsize=48, color="white" )
    elif GAME:
        alien.draw()
        for bullet in bulletlist:
            bullet.draw()
    return

def update():
    if GAME:
        alien.x += alien.hspeed
        alien.y += alien.vspeed
        if alien.right >= WIDTH or alien.left <= 0:
            pass
        if alien.top < 0 or alien.bottom >= HEIGHT:
            pass

        for bullet in bulletlist:
            bullet.move_in_direction(2)

    elif MENU:
        pass

    return

def on_mouse_down(pos, button):
    if GAME:
        pass
        bullet = Actor('bullet', alien.pos)
        bullet.direction = bullet.angle_to(pos)
        bullet.angle = bullet.direction + 90
        bulletlist.append(bullet)
    elif MENU:
        if button == 1:
            start_game()
    return

def on_key_down(key):
    if key == keys.SPACE:
        print("Space key pressed...")
    return

def set_alien_normal():
    alien.image = 'alien'
    return

def set_alien_hurt():
    sounds.eep.play()
    return


