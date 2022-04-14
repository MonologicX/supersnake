import pygame
import sys
import time
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
lightBlue = (69, 210, 253)
purple = (148,0,211)

winWidth, winHeight = 900, 500
WIN = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Snake")

font = pygame.font.SysFont('Sans', 25)

fps = 30

def draw(snakeSize, foodX, foodY, poisonX, poisonY, speedX, speedY, slowX, slowY, snakeList, snakeLength, score, scoreMultiplyer, ssMultiplyer):
    WIN.fill(black)
    for x in snakeList:
        pygame.draw.rect(WIN, white, [x[0], x[1], snakeSize, snakeSize])
    pygame.draw.rect(WIN, green, [foodX, foodY, snakeSize, snakeSize])
    pygame.draw.rect(WIN, purple, [poisonX, poisonY, snakeSize, snakeSize])
    pygame.draw.rect(WIN, lightBlue, [speedX, speedY, snakeSize, snakeSize])
    pygame.draw.rect(WIN, red, [slowX, slowY, snakeSize, snakeSize])

    msg = font.render(str(score * (scoreMultiplyer + ssMultiplyer - 1)), True, white)
    WIN.blit(msg, [10, 10])

    mult = font.render("x" + str(scoreMultiplyer + ssMultiplyer - 1), True, white)
    WIN.blit(mult, [850, 10])
    
    pygame.display.update()
    
def message(msg, color):
    mesg = font.render(msg, True, color)
    WIN.blit(mesg, [winWidth / 2 - 100, winHeight / 2])
    
def main():

    snakeX = 0
    snakeY = 0
    snakeSize = 10
    snakeXChange = 0
    snakeYChange = 0
    snakeSpeed = 10
    snakeList = []
    snakeLength = 1
    score = 0
    scoreMultiplyer = 1
    ssMultiplyer = 1

    foodX = random.randint(0 + snakeSize, winWidth - snakeSize)
    foodY = random.randint(0 + snakeSize, winHeight - snakeSize)

    poisonX = random.randint(0 + snakeSize, winWidth - snakeSize)
    poisonY = random.randint(0 + snakeSize, winHeight - snakeSize)

    speedX = random.randint(0 + snakeSize, winWidth - snakeSize)
    speedY = random.randint(0 + snakeSize, winHeight - snakeSize)

    slowX = random.randint(0 + snakeSize, winWidth - snakeSize)
    slowY = random.randint(0 + snakeSize, winHeight - snakeSize)

    gameClosed = False
    gameOver = False

    clock = pygame.time.Clock()
    
    while gameClosed == False:

        clock.tick(fps)

        while gameOver == True:

            WIN.fill(white)

            msg = font.render("r to Play Again", True, black)
            WIN.blit(msg, [winWidth / 2 - 100, winHeight / 2])

            msg = font.render(str(score * scoreMultiplyer * ssMultiplyer), True, black)
            WIN.blit(msg, [winWidth / 2 - 20, winHeight / 2 + 50])

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
        #Movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameClosed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    snakeYChange = -snakeSpeed
                    snakeXChange = 0
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snakeXChange = -snakeSpeed
                    snakeYChange = 0
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snakeYChange = snakeSpeed
                    snakeXChange = 0
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snakeXChange = snakeSpeed
                    snakeYChange = 0
        
        snakeRect = pygame.Rect(snakeX, snakeY, snakeSize, snakeSize)
        foodRect = pygame.Rect(foodX, foodY, snakeSize, snakeSize)
        poisonRect = pygame.Rect(poisonX, poisonY, snakeSize, snakeSize)
        speedRect = pygame.Rect(speedX, speedY, snakeSize, snakeSize)
        slowRect = pygame.Rect(slowX, slowY, snakeSize, snakeSize)

        snakeX += snakeXChange
        snakeY += snakeYChange

        #Bounds Detection / Death
        if snakeX < 0 or snakeX > (winWidth - snakeSize):
            gameOver = True
        if snakeY < 0 or snakeY > (winHeight - snakeSize):
            gameOver = True
        if score < 0:
            gameOver = True

        #Snake Tail
        snakeHead = []
        snakeHead.append(snakeX)
        snakeHead.append(snakeY)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]
            
        for x in snakeList[:-1]:
            if x == snakeHead:
                score -= 1

        #Collision
        if snakeRect.colliderect(foodRect) == 1:
            foodX = random.randint(0 + snakeSize, winWidth - snakeSize)
            foodY = random.randint(0 + snakeSize, winHeight - snakeSize)
            snakeLength += 3
            score  += 1

            m = (snakeLength / 30) + 1
            if m >= scoreMultiplyer + 1:
                scoreMultiplyer += 1
            
        if snakeRect.colliderect(poisonRect) == 1:
            poisonX = random.randint(0 + snakeSize, winWidth - snakeSize)
            poisonY = random.randint(0 + snakeSize, winHeight - snakeSize)

            if snakeLength > 1:
                snakeLength -= 1
                del snakeList[0]

                m = (snakeLength / 30) + 1
                if m < scoreMultiplyer:
                    scoreMultiplyer -= 1
                    
        if snakeRect.colliderect(speedRect) == 1:
            speedX = random.randint(0 + snakeSize, winWidth - snakeSize)
            speedY = random.randint(0 + snakeSize, winHeight - snakeSize)
            score += 5
            snakeSpeed += 5

            m = (snakeSpeed / 5)
            if m> 1 and m > ssMultiplyer + 1:
                ssMultiplyer += 1

        if snakeRect.colliderect(slowRect) == 1:
            slowX = random.randint(0 + snakeSize, winWidth - snakeSize)
            slowY = random.randint(0 + snakeSize, winHeight - snakeSize)
            
            if snakeSpeed > 3:
                snakeSpeed -= 2
                m = (snakeSpeed / 10)
                if m < ssMultiplyer - 1:
                    ssMultiplyer -= 1

        #Rendering
        draw(snakeSize, foodX, foodY, poisonX, poisonY, speedX, speedY, slowX, slowY, snakeList, snakeLength, score, scoreMultiplyer, ssMultiplyer)

                
    pygame.quit()
    sys.exit()

main()
