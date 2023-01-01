import pygame
from pygame import mixer
import random
import math
import cmath



# Initialize Pygame
pygame.init()

# Creates the screen for pygame
screen = pygame.display.set_mode((1000, 800))

# Title/Icon
icon = pygame.image.load('Alien.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Ultimate Space Invaders")

#Background Music
pygame.mixer.music.load('background.wav')
mixer.music.play(-1)

# Player, loading image, setting spaceship coordinates, also reshaping the image
playerimage = pygame.image.load('space.png')
playerimage = pygame.transform.scale(playerimage, (80, 80))
playerX = 480
global playerY
playerY = 650
playerX_change = 0
playerY_change = 0

#Enemy1

enemy1image = pygame.image.load('enemy.png')
enemy1image = pygame.transform.scale(enemy1image, (80, 80))

#Puts everything in for loop to make multiple enemies
enemy1image = []
enemy1X = []
enemy1y = []
enemy1X_change = []
enemy1Y_change = []
number_of_enemies = 6


#Make it appear in a random cordinate
for i in range(number_of_enemies):
    enemy1image.append(pygame.image.load('enemy.png'))
    enemy1X.append(random.randint (0,916))
    enemy1y.append(random.randint(40,300))
    enemy1X_change.append(3)
    enemy1Y_change.append(40)





#Bullet for shooting
bulletimg = pygame.image.load('bullet.png')
bulletimg = pygame.transform.scale(bulletimg,(35,35))
bulletx = 0
bullety = 650 #is 650 so it can stay with the spaceship
bulletX_change = 0
bulletY_change = 40
bullet_state = "Ready" #Ready - you can't see the bullet of the screen, Fire - the bullet is moving

Live_value = 5
score_value = 0
font = pygame.font.Font('freesansbold.ttf',40)
over_font = pygame.font.Font('freesansbold.ttf',100)
textX = 10
textY = 10
LiveX = 800
LiveY = 10


def Player(x, y):
    # Draws the spaceship on the screen (image, than x and y coordinates). call in the while run function
    screen.blit(playerimage, (x, y))

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score,(x,y))

def show_lives(x,y):
    Lives = font.render("Lives: "+ str(Live_value), True ,(255,255,255))
    screen.blit(Lives,(x,y))


def enemy1(x,y,i):
    #Draws Enemy1 on screen
    screen.blit(enemy1image[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletimg,(x + 21,y + 10))

#Will get the distance between the bullet and the enemy
def isCollision(enemy1X, enemy1y,bulletx, bullety):
    Distance = math.sqrt(math.pow(enemy1X-bulletx,2) + math.pow(enemy1y-bullety,2))
    if Distance < 27:
        return True
    else:
        return False

#Scorescore_value = 0

def GameoverCollision(enemy1X, enemy1y,playerX,playerY ):
    Distance = math.sqrt(math.pow(enemy1X-playerX,2) + math.pow(enemy1y-playerY,2))
    if Distance < 27:
        return True
    else:
        return False

def game_over_text():
    over_text = over_font.render("GAME OVER",True,(255,255,255))
    screen.blit(over_text,(200,350))




#Game loop: Function for making the pygame screen to run and close when you want to
running = True
while running:
    screen.fill((0,0,0))
    #Background Image (Put it in the while loop)
    background_image = pygame.image.load('SpaceBackground.png')
    screen.blit(background_image,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                playerX_change = -7
            if event.key == pygame.K_d:
                playerX_change = +7
            if event.key == pygame.K_w:
                playerY_change = -7
                print("up Key is pressed")
            if event.key == pygame.K_s:
                playerY_change = +7
                print("down Key is pressed")

            #For shooting the bullet using spacebar
            if event.key == pygame.K_SPACE:
                if bullet_state is "Ready":
                    #When spacebar is hit, will check if a bullet is on the screen and will get the current x and y coordinates of the spaceship
                    bullet_sound = mixer.Sound('Laser.wav')
                    bullet_sound.play()
                    bulletx = playerX
                    bullety = playerY
                    fire_bullet(playerX,playerY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a or event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_DOWN or event.key == pygame.K_s:
                playerX_change = 0
                playerY_change = 0

    Player(playerX, playerY)
    playerX += playerX_change
    playerY += playerY_change

# Adding borders around the game.when the spaceship reach certain cordinates, it will stop
    if playerX <= 0:
        playerX = 0
    elif playerX >= 918:
        playerX = 918
    if playerY <= 0:
        playerY = 0
    elif playerY >= 725:
        playerY = 725


#Enemy1 Movement/boundaries


#Every time the enemy hits the boundary, it moves down
    for i in range(number_of_enemies):
        if Live_value == 0 or enemy1y[i] > 750:
            for j in range(number_of_enemies):
                enemy1y[i] = 2000
            game_over_text()
            break
        #Game Over
        Playercollide = GameoverCollision(enemy1X[i],enemy1y[i],playerX,playerY)
        if Playercollide:
            Damage_sound = mixer.Sound('PlayerDamage.wav')
            mixer.Sound.play(Damage_sound)
            enemy1X[i] = random.randint(0, 916)
            enemy1y[i] = random.randint(0, 150)
            score_value -= 1
            Live_value -= 1
        if score_value < 0:
            score_value = 0
        if Live_value < 0:
            Live_value = 0




        enemy1X[i] += enemy1X_change[i]
        if enemy1X[i] <= 0:
            enemy1X_change[i] = 7
            enemy1y[i] += enemy1Y_change[i]
        elif enemy1X[i] >= 917:
            enemy1X_change[i] = -7
            enemy1y[i] += enemy1Y_change[i]
        enemy1(enemy1X[i], enemy1y[i], i)

    #if enemy1y >= 250:
       # enemy1X_change = -4
        #enemy1y -= enemy1Y_change
        collision = isCollision(enemy1X[i], enemy1y[i], bulletx, bullety)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            mixer.Sound.play(explosion_sound)
            bullety = 650
            bullet_state = "Ready"
            score_value += 1
            enemy1X[i] = random.randint(0, 916)
            enemy1y[i] = random.randint(0, 150)




    #Bullet Movement
    if bullet_state is "Fire":
        fire_bullet(bulletx,bullety)
        bullety -=  bulletY_change
    if bullety <= 0:
        bullety = 650
        bullet_state = "Ready"


    show_lives(LiveX,LiveY)
    show_score(textX,textY)
    pygame.display.update()




































































































































