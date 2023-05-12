# Write your code here :-)
#import pgzrun

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

#create boolean variables
MENU = True
GAME = False
currentlevel = 1
bulletlist = [] #global list of bullets
enemylist = [] #create a list of enemies

def start_game():
    global GAME
    global MENU
    music.play('newdawn')
    GAME = True
    MENU = False
    clock.schedule(CreateEnemy, 5.0) #create a timer
    return


def draw():
    screen.clear()
    screen.blit('spacebackground',(0,0))
    if MENU:
        screen.draw.text("Click to continue", midbottom=(400,300), width=360, fontsize=48, color="white" )
    elif GAME:
        alien.draw()
        for bullet in bulletlist:
            bullet.draw()

        for enemy in enemylist:
            enemy.draw()
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
            for enemy in enemylist:
                if enemy.colliderect(bullet):
                    enemylist.remove(enemy)
                    bulletlist.remove(bullet)
                    continue

            bullet.move_in_direction(bullet.speed)
            if bullet.x >= WIDTH or bullet.x <= 0:
                bulletlist.remove(bullet)
                continue
                
            elif bullet.y < 0 or bullet.y >= HEIGHT:
                bulletlist.remove(bullet)
                continue
            
        for enemy in enemylist:
            enemy.move_towards(alien, 3)
        


        #a better way to get key presses
        '''pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            print("PYGAME Key pressed")  '''  
        

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

def CreateEnemy():
    if GAME:
        clock.schedule(CreateEnemy, 5.0) #recurring function
        enemy = Actor('spider')
        enemy.x = random.randint(0,1)*WIDTH #0, 800
        enemy.y = random.randint(0,1)*HEIGHT #0, 600
        enemylist.append(enemy)
    return

#pgzrun.go()