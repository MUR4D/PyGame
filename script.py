import pygame
import random
import math
from pygame import mixer

pygame.init()

game_over=False

screen=pygame.display.set_mode((800,600))

score=0
font=pygame.font.Font('freesansbold.ttf',40)

textX=10
textY=30




pygame.display.set_caption("MUR4DGAMES")
icon=pygame.image.load('nature.png')
pygame.display.set_icon(icon)

player_sprite=pygame.image.load('spaceship.png')
background=pygame.image.load('BG.jpg')
bullet=pygame.image.load('bullet.png')


player_X=360
player_Y=534
pl_x_changed=0

enemy_sprite=list()
enemy_X=list()
enemy_Y=list()
en_x_changed=list()
en_y_changed=list()
num_of_enemies=25


for i in range(num_of_enemies):
    enemy_sprite.append(pygame.image.load('spaceinvader.png'))
    enemy_X.append( random.randint(0, 736))
    enemy_Y.append(random.randint(50, 80))
    en_x_changed.append(1.5)
    en_y_changed.append(40)




bullet_X=360
bullet_Y=534
bl_X_changed=0
bl_Y_changed=8
bullet_state='ready'






def show_score(x,y):
    show=font.render("Score: "+ str(score),True,(0,255,0))
    screen.blit(show,(x,y))

def game_over(x,y):
    show=font.render("Game Over",True,(255,0,0))
    screen.blit(show,(x,y))

def player(x,y):
    screen.blit(player_sprite,(x,y))

def enemy(x,y,i):
    screen.blit(enemy_sprite[i],(x,y))

def fire(x,y):
    global bullet_state
    bullet_state='fire'
    screen.blit(bullet,(x,y))

def collision(enemy_X,enemy_Y,bullet_X,bullet_Y):
    distance=math.sqrt((math.pow(enemy_X-bullet_X,2))+(math.pow(enemy_Y-bullet_Y,2)))
    if distance < 27:
        return True
    else:
        return False



run_time=True
while run_time:

    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_time=False

        if event.type==pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                pl_x_changed=-1.5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                pl_x_changed=1.5
            if event.key == pygame.K_SPACE and len(enemy_sprite)>0:
                if bullet_state is 'ready':
                    mixer.Sound('laser.wav').play()
                    bullet_X = player_X
                    fire(bullet_X, bullet_Y)



        else:
            pl_x_changed=0



    player_X+=pl_x_changed
    bullet_Y += 0.5


    if player_X<=0:
        player_X=0
    elif player_X>=736:
        player_X=736

    for i in range(num_of_enemies):
        enemy_X[i]+=en_x_changed[i]
        if enemy_X[i]<=0:
            en_x_changed[i]=1.5
            enemy_Y[i]+=en_y_changed[i]
        elif enemy_X[i]>=736:
            en_x_changed[i]=-1.5
            enemy_Y[i]+=en_y_changed[i]

        col = collision(enemy_X[i], enemy_Y[i], bullet_X, bullet_Y)
        col1=collision(enemy_X[i],enemy_Y[i],player_X,player_Y)

        if col:
            mixer.Sound('explosion.wav').play()
            bullet_Y = 480
            bullet_state = 'ready'
            enemy_X[i] = random.randint(0, 736)
            enemy_Y[i] = random.randint(50, 80)
            score+=1
        if col1:
            enemy_sprite.clear()
            game_over(400,300)

            # run_time=False
        if len(enemy_sprite)>0:
            enemy(enemy_X[i], enemy_Y[i], i)


    if bullet_Y <=0:
        bullet_Y=480
        bullet_state='ready'


    if bullet_state == 'fire':
        fire(bullet_X,bullet_Y)
        bullet_Y-=bl_Y_changed







    player(player_X,player_Y)
    show_score(textX,textY)
    pygame.display.update()
