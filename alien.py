# Write your code here :-)
#import pgzrun

import random
import math
from pgzhelper import *

WIDTH = 800
HEIGHT = 600

#Create an object of the type Actor and give it the variable name "alien"
alien = Actor('ship')
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
    global alien
    
    music.play('newdawn')
    GAME = True
    MENU = False
    clock.schedule(CreateEnemy, 5.0) #create a timer
    return

#draw function is called 60 frames per second
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

#update function is called 60 frames per second
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
                continue #skip the remained of the for loop - otherwise the bullet will not exist for collision
                
            elif bullet.y < 0 or bullet.y >= HEIGHT:
                bulletlist.remove(bullet)
                continue #skip the remainer of this for loop - otherwise the bullet will not exist for collision

            for enemy in enemylist:
                if enemy.colliderect(bullet):
                    enemylist.remove(enemy)
                    bulletlist.remove(bullet)
            
        for enemy in enemylist:
            enemy.move_towards(alien, 3)
        
        #a better way to get key presses using pygame
        pressed = pygame.key.get_pressed()
        if len(pressed) > 0:
            OnKeyPress(pressed)

        #a better way to get mouse using pygame
        mousepos = pygame.mouse.get_pos()
        alien.angle = alien.angle_to(mousepos) - 90   

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

'''#pygame zero method of handling key presses
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
'''

def OnKeyPress(pressed): #pygame method of handling key presses
    if pressed[pygame.K_a]:
        if alien.hspeed > -5:
            alien.hspeed -= 1
    elif pressed[pygame.K_d]:
        if alien.hspeed < 5:
            alien.hspeed += 1
    elif pressed[pygame.K_w]:
        if alien.vspeed > -5:
            alien.vspeed -= 1
    elif pressed[pygame.K_s]:
        if alien.vspeed < 5:
            alien.vspeed += 1
    return

#Create an enemy and then reset timer
def CreateEnemy():
    if GAME:
        clock.schedule(CreateEnemy, 5.0) #recurring function
        enemy = Actor('spider')
        enemy.x = random.randint(0,1)*WIDTH #0, 800
        enemy.y = random.randint(0,1)*HEIGHT #0, 600
        enemylist.append(enemy)
    return

#pgzrun.go()