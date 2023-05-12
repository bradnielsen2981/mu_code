# Write your code here :-)

import random
import math
from pgzhelper import *

WIDTH = 800
HEIGHT = 600

#Create an object of the type Actor and give it the variable name "alien"
alien = Actor('alien')
alien.x = 400
alien.y = 300
alien.hspeed = 0
alien.vspeed = 0

#create boolean variables to swithc our game
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
    if GAME: #if game is true
        alien.x += alien.hspeed
        alien.y += alien.vspeed
        if alien.x >= WIDTH or alien.x <= 0:
            alien.x = alien.x%WIDTH
        if alien.y < 0 or alien.y >= HEIGHT:
            alien.y = alien.y%HEIGHT

        #remove any bullet that is off screen
        for bullet in bulletlist: 
            bullet.move_in_direction(bullet.speed)
            if bullet.x >= WIDTH or bullet.x <= 0:
                bulletlist.remove(bullet)
                del bullet
            elif bullet.y < 0 or bullet.y >= HEIGHT:
                bulletlist.remove(bullet)
                del bullet
            

    elif MENU: #if menu is true
        pass

    return

def on_mouse_down(pos, button):
    if GAME:
        sounds.eep.play()
        bullet = Actor('bullet', alien.pos)
        bullet.scale = 0.5
        bullet.speed = 7
        bullet.direction = bullet.angle_to(pos)
        bullet.angle = bullet.direction + 90
        bulletlist.append(bullet)
    elif MENU:
        if button == 1:
            start_game()
    return

def on_key_down(key):
    print("Key down")
    if key == keys.A:
        if alien.hspeed > -8:
            alien.hspeed -= 1
    elif key == keys.D:
        if alien.hspeed < 8:
            alien.hspeed += 1
    elif key == keys.W:
        if alien.vspeed > -8:
            alien.vspeed -= 1
    elif key == keys.S:
        if alien.vspeed < 8:
            alien.vspeed += 1
    return

