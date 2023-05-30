# Write your code here :-)
import pgzrun #Uncomment to use with VSCODE and see last line of code to also uncomment
import pygame
import random
import math
from pgzhelper import *
import bigboss

WIDTH = 800
HEIGHT = 600

#Create an object of the type Actor and give it the variable name "alien"
alien = Actor('ship')
alien.x = 400
alien.y = 300
alien.hspeed = 0
alien.vspeed = 0
alien.sound = pygame.mixer.Sound("sounds/laser.mp3")


bigboss = bigboss.BigBoss('splat')
bigboss.pos = (400,300)

#create boolean variables
MENU = True
GAME = False
GAMEOVER = False
currentlevel = 1
bulletlist = [] #global list of bullets
enemylist = [] #create a list of enemies


def start_game():
    global GAME
    global MENU
    global currentlevel
    global bulletlist
    global enemylist
    MENU = False
    GAME = True
    currentlevel = 1
    bulletlist = [] #global list of bullets
    enemylist = [] #create a list of enemies
    clock.schedule(CreateEnemy, 3.0) #create a timer
    music.play('newdawn')
    return

def end_game():
    global GAME
    global MENU
    global GAMEOVER
    GAME = False
    MENU = True
    GAMEOVER = False
    return

def game_over():
    global GAME
    global MENU
    global GAMEOVER
    GAME = False
    MENU = False
    GAMEOVER = True
    music.stop()
    clock.schedule(end_game, 3.0)
    return

#draw function is called 60 frames per second
def draw():
    screen.clear()
    screen.blit('spacebackground',(0,0))
    if MENU:
        screen.draw.text("Click to continue", midbottom=(400,300), width=360, fontsize=48, color="white" )
    elif GAME:
        alien.draw()
        bigboss.draw()
        for bullet in bulletlist:
            bullet.draw()
        for enemy in enemylist:
            enemy.draw()
    elif GAMEOVER:
        screen.draw.text("Game Over", midbottom=(400,300), width=360, fontsize=48, color="black" )
    return

#update function is called 60 frames per second
def update():
    if GAME: #if game is true
        bigboss.update(alien.pos)
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

            removebullet = False
            for enemy in enemylist:
                if enemy.collide_pixel(bullet) and enemy.explode < 0: #only if enemy is not exploding
                    enemy.explode = 0 #start enermy explosion
                    removebullet = True
            if removebullet:
                bulletlist.remove(bullet) #need to remove the bullet AFTER all the enemies have been deleted.
                        
        for enemy in enemylist:
            if enemy.collide_pixel(alien) and enemy.explode < 0: #only detect collision if enemy is not exploding
                enemylist.remove(enemy)
                game_over()
            else:
                enemy.move_towards(alien, 3 + currentlevel/10)

            if enemy.explode >= 0 and enemy.explode < 19: #if enemy is exploding
                enemy.explode += 1
                enemy.next_image()
            elif enemy.explode == 19:
                enemylist.remove(enemy)


        #THIS CODE ALLOWS INPUTS TO BE DETECTED BETTER
        #------------------------------------------------
        #a better way to get key presses using pygame
        pressed = pygame.key.get_pressed()
        if len(pressed) > 0:
            OnKeyPress(pressed)

        #a better way to get mouse using pygame
        mousepos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed() == (1, 0, 0):
            onMouseLeftDown(mousepos)
        #-----------------------------------------

        alien.angle = alien.angle_to(mousepos) - 90  
         

    elif MENU: #if menu is true
        pass

    elif GAMEOVER:
        pass

    return

def on_mouse_up(pos, button):
    if GAME:
        alien.sound.play()
        bullet = Actor('bullet', alien.pos)
        bullet.scale = 0.3
        bullet.speed = 7
        bullet.direction = bullet.angle_to(pos)
        bullet.angle = bullet.direction + 90
        bulletlist.append(bullet)
    elif MENU:
        if button == 1:
            start_game()
    return

#pygame method mouse presses
def onMouseLeftDown(pos):
    print(pos)
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
        if alien.hspeed > -4:
            alien.hspeed -= 0.5
    elif pressed[pygame.K_d]:
        if alien.hspeed < 4:
            alien.hspeed += 0.5
    elif pressed[pygame.K_w]:
        if alien.vspeed > -4:
            alien.vspeed -= 0.5
    elif pressed[pygame.K_s]:
        if alien.vspeed < 4:
            alien.vspeed += 0.5
    return

#Create an enemy and then reset timer
def CreateEnemy():
    global currentlevel
    if currentlevel < 40:
        currentlevel += 1  #decrease time of enemy spawn and increase speed of enemy
    if GAME:
        clock.schedule(CreateEnemy, 5.0 - (currentlevel/10)) #recurring function speed up over time

        for i in range(int(currentlevel/2)):
            enemy = Actor('spider') #create new enemy
            enemy.scale = 0.6

            #position of enemy
            cornerx = random.randint(0,1)*WIDTH #0, 800
            cornery = random.randint(0,1)*HEIGHT #0, 600
            enemy.x = cornerx
            if enemy.x == 0:
                enemy.x -= i*100
            else: 
                enemy.x += i*100
            enemy.y = cornery
            if enemy.y == 0:
                enemy.y -= i*100
            else: 
                enemy.y += i*100

            enemy.images = ['spider'] #create animation slides
            for i in range(0,19):
                enemy.images.append('explosion/tile'+str(i))
            enemy.explode = -1 #set enemy to be unexploded
            
            enemylist.append(enemy)
    return


pgzrun.go() #Uncomment to use with VSCODE