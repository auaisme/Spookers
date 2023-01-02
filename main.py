import pygame
import random
from pygame import mixer #for music shizz

#initializing pygame
pygame.init()

#use the following method to make the game window
screen = pygame.display.set_mode((720, 900))
#<library name>.<what you're fucking with / module>.<command>((width, height))

#Background music
mixer.music.load("background_music.mp3")
mixer.music.play(-1) # the -1 gets it to play on loop else it'll play once and stop

#Title and Icon
#Title/Caption
pygame.display.set_caption("SPOOKERS")
#Icon
#Icons must be png and 32x32
icon = pygame.image.load("alien.png") #loads the image into memory
pygame.display.set_icon(icon) #sets the associated image as the icon

#background
backgroundImg = pygame.image.load("background.jpg")
backgroundY_1 = 0
backgroundY_2 = -900
backgroundY_change = 0.5

def background(x, y):
    screen.blit(backgroundImg, (x, y))

#earth
earthImg = pygame.image.load("earth.png")

#earth_health
earth_health = 3
heartImg = []
earth_healthX = [0, 64, 128]
earth_healthY = [836, 836, 836]
for i in range(0, earth_health):
    heartImg.append(pygame.image.load("heart.png"))

def EarthHealth(x, y, i):
    screen.blit(heartImg[i], (x, y))

#player
playerImg = pygame.image.load("player.png")
playerX = 328 # X coordinate for the playerImg
playerY = 736 # Y coordinate for the playerImg
playerX_change = 0 # will be used to move player along X
playerY_change = 0 # will be used to move player along Y
playerX_change_right = 0
playerX_change_left = 0
playerY_change_up = 0
playerY_change_down = 0

def player(x, y):
    screen.blit(playerImg, (x, y)) # blit is used to draw. screen.blit(what you're drawing, (x, y))


#Enemy
enemyImg = []
enemyY = []
enemyX = []
enemyX_change = []
enemyY_change = []
enemy_state = []
num_of_enemies = 6
old_num_of_enemies = 0

for i in range(0, 100):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(int(random.randint(0, 656)))
    enemyY.append(int(random.randint(0, 150)))
    enemyX_change.append(1)
    enemyY_change.append(20)
    if i < num_of_enemies:
        enemy_state.append("alive")
    else:
        enemy_state.append("dead")

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

#Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = -2
bullet_state = "ready"

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

#Explosion
explosionImg = pygame.image.load("explosion.png")

#Score
score_value = int(0)
font = pygame.font.Font("arcade.ttf", 64) # 1st argument => font type, 2nd argument => size
textX = 16
textY = 5

def show_score(x, y):
    score = font.render("Score     " + str(score_value), True, (255, 0, 0)) # 1st => what's to be shown, 2nd => ?, 3rd => color RGB
    screen.blit(score, (x, y))

#Pause
pauseImg = pygame.image.load("pause.png")
def pause():
    paused = True
    while paused:
        screen.blit(pauseImg, (115, 360))
        pygame.display.update()
        mixer.music.pause()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = False
                    mixer.music.play(-1)
                else:
                    pass

            elif event.type == pygame.QUIT:
                #pygame.QUIT is the event for pressing the cross button
                pygame.quit() # quits pygame
                quit() # quits


#Gameover
gameoverImg = pygame.image.load("gameover.png")

#Restart
restartImg = pygame.image.load("restart.png")

running = True
#creating an infinite loop to maintain the window
while running:

    #Stuff that shouldn't change will be within the while running: loop
    #screen.fill(()) will be used to fill the screen w/ a color
    #screen.fill((red, green, blue, opacity))
    screen.fill((100, 100, 100)) #this won't work alone, display needs to update for it to work.

    #background
    background(0, backgroundY_1)
    background(0, backgroundY_2)
    if backgroundY_1 == 900:
        backgroundY_1 = -900
    backgroundY_1 += backgroundY_change
    if backgroundY_2 == 900:
        backgroundY_2 = -900
    backgroundY_2 += backgroundY_change

    #earth
    screen.blit(earthImg, (-130, 800))

    #score
    show_score(textX, textY)

    #creating a way to check if event exists in the pygame lib and to get the pygame lib events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #pygame.QUIT is the event for pressing the cross button
            running = False
            #this is a way to close the window upon clicking the cross button

        if event.type == pygame.KEYDOWN: #KEYDOWN checks if a key has been pressed
            if event.key == pygame.K_a:
                playerX_change_left = -2

            if event.key == pygame.K_d:
                playerX_change_right = 2

            if event.key == pygame.K_w:
                playerY_change_up = -2

            if event.key == pygame.K_s:
                playerY_change_down = 2

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletX = playerX
                    bulletY = playerY
                    fire_bullet(playerX, bulletY)
                    fire_sound = mixer.Sound("fire.wav")
                    fire_sound.play()

            if event.key == pygame.K_ESCAPE:
                pause()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                playerX_change_left = 0

            if event.key == pygame.K_d:
                playerX_change_right = 0

            if event.key == pygame.K_w:
                playerY_change_up = 0

            if event.key == pygame.K_s:
                playerY_change_down = 0

            #if event.key == pygame.K_SPACE:
                #bulletX = 0

    if bulletY <= 0:
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change

    playerX_change = playerX_change_right + playerX_change_left
    playerX += playerX_change
    if playerX < 0: #this is to confine the player
        playerX = 0
    elif playerX > 656:
        playerX = 656
    playerY_change = playerY_change_up + playerY_change_down
    playerY += playerY_change
    if playerY < 200: #this is to confine the player
        playerY = 200
    elif playerY >= 736:
        playerY = 736
    player(playerX, playerY) #again, we are adding something to the screen so display needs to be updated. also, this is after .fill so that it shows on top of it.

    #enemy movement
    for i in range(0, num_of_enemies):
        if enemy_state[i] is "alive":
            enemyX[i] += enemyX_change[i]
            if enemyX[i] >= 656:
                enemyX[i] = 656
                enemyX_change[i] = -1
            elif enemyX[i] <= 0:
                enemyX[i] = 0
                enemyX_change[i] = 1
            if enemyX[i] == 656 or enemyX[i] == 0:
                enemyY[i] += enemyY_change[i]
            if enemyY[i] >= 900:
                enemyY[i] = 0
                earth_health -= 1
                earth_health_loss = mixer.Sound("scream.wav")
                earth_health_loss.play()
            enemy(enemyX[i], enemyY[i], i) #before update to ensure this actually shows up. this will show an enemy

            if bulletY in range(enemyY[i], enemyY[i]+64) and bulletX in range(enemyX[i], enemyX[i]+64) and enemy_state[i] is "alive" and bullet_state is "fire":
                enemy_state[i] = "dead"
                for n in range(0, 50):
                    screen.blit(explosionImg, (enemyX[i], enemyY[i]))
                    pygame.display.update()
                bullet_state = "ready"
                score_value += 1
                bulletX = playerX
                bulletY = playerY
                explosion_sound = mixer.Sound("explosion_music.wav")
                explosion_sound.play()

            elif enemyY[i] in range(bulletY, bulletY+32) and enemyX[i] in range(bulletX, bulletX+32) and enemy_state[i] is "alive" and bullet_state is "fire":
                enemy_state[i] = "dead"
                for n in range(0, 50):
                    screen.blit(explosionImg, (enemyX[i], enemyY[i]))
                    pygame.display.update()
                bullet_state = "ready"
                score_value += 1
                bulletX = playerX
                bulletY = playerY
                explosion_sound = mixer.Sound("explosion_music.wav")
                explosion_sound.play()

            if enemy_state[i] is "dead":
                enemyX[i] = int(random.randint(0, 656))
                enemyY[i] = int(random.randint(0, 150))
                enemy(enemyX[i], enemyY[i], i)
                enemy_state[i] = "alive"

            if (playerY in range(enemyY[i], enemyY[i]+64) and playerX in range(enemyX[i], enemyX[i]+64) and enemy_state[i] is "alive") or earth_health == 0:
                enemy_state[i] = "alive"
                for n in range(0, 100):
                    screen.blit(explosionImg, (playerX, playerY))
                    pygame.display.update()
                bullet_state = "ready"
                screen.blit(gameoverImg, (100, 100))
                pygame.display.update()
                screen.blit(restartImg ,(104, 600))
                pygame.display.update()
                mixer.music.pause()
                player_death_sound = mixer.Sound("game_over.wav")
                player_death_sound.play()
                inf = True
                while inf == True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            #pygame.QUIT is the event for pressing the cross button
                            running = False
                            inf = False
                            #this is a way to close the window upon clicking the cross button

                        elif event.type == pygame.KEYDOWN: #KEYDOWN checks if a key has been pressed
                            if event.key == pygame.K_r:
                                inf = False
                                for i in range(0, num_of_enemies):
                                    enemyX[i] = int(random.randint(0, 656))
                                    enemyY[i] = int(random.randint(0, 150))
                                    enemy(enemyX[i], enemyY[i], i)
                                    enemy_state[i] = "alive"
                                    playerX = 328
                                    playerY = 800
                                    playerX_change = 0
                                    playerX_change_right = 0
                                    playerX_change_left = 0
                                    playerY_change = 0
                                    playerY_change_up = 0
                                    playerY_change_down = 0
                                    score_value = 0
                                    earth_health = 3
                                    num_of_enemies = 6
                                    mixer.music.rewind()
                                    mixer.music.play(-1)

                            elif event.key == pygame.K_ESCAPE:
                                inf = False
                                running = False

            elif enemyY[i] in range(playerY, playerY+64) and enemyX[i] in range(playerX, playerX+64) and enemy_state[i] is "alive":
                enemy_state[i] = "alive"
                for n in range(0, 100):
                    screen.blit(explosionImg, (playerX, playerY))
                    pygame.display.update()
                bullet_state = "ready"
                screen.blit(gameoverImg, (100, 100))
                pygame.display.update()
                screen.blit(restartImg ,(104, 600))
                pygame.display.update()
                mixer.music.pause()
                player_death_sound = mixer.Sound("game_over.wav")
                player_death_sound.play()
                inf = True
                while inf == True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            #pygame.QUIT is the event for pressing the cross button
                            running = False
                            inf = False
                            #this is a way to close the window upon clicking the cross button

                        elif event.type == pygame.KEYDOWN: #KEYDOWN checks if a key has been pressed
                            if event.key == pygame.K_r:
                                inf = False
                                for i in range(0, num_of_enemies):
                                    enemyX[i] = int(random.randint(0, 656))
                                    enemyY[i] = int(random.randint(0, 150))
                                    enemy(enemyX[i], enemyY[i], i)
                                    enemy_state[i] = "alive"
                                    playerX = 328
                                    playerY = 800
                                    playerX_change = 0
                                    playerY_change = 0
                                    score_value = 0
                                    num_of_enemies = 6
                                    mixer.music.rewind()
                                    mixer.music.play(-1)

                            elif event.key == pygame.K_ESCAPE:
                                inf = False
                                running = False

    for i in range(earth_health):
        EarthHealth(earth_healthX[i], earth_healthY[i], i)

#    if (score_value % 10) == 0 and score_value < 100 and score_value > 0:
#        old_num_of_enemies = num_of_enemies
#        num_of_enemies += 1

    pygame.display.update() #this updates the display
