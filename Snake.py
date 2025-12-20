import pygame
import random
import time
import sys
import os
from pygame.locals import (K_UP,K_DOWN,K_LEFT,K_RIGHT,K_ESCAPE,K_RETURN,KEYDOWN,QUIT)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path,relative_path)

pygame.init()

SCREEN_WIDTH,SCREEN_HEIGHT = 500, 500
wdth,hght,spd,score,fps = 10,10,10,0,15
green, black, red, white = (0, 255, 0) , (0, 0, 0), (255, 0, 0), (255,255,255)
clk = pygame.time.Clock()
mainFont = pygame.font.SysFont("arial", 50)
emoji = pygame.transform.scale(pygame.image.load(resource_path("the.png")),(64,64))
options = ["Easy", "Medium", "Hard", emoji, "Quit"]
selected_index = 0
difficulty = None

background = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
pygame.display.set_caption("SNAAAAAAAAAAAKE")

#----------------------------CLASSES-------------------------
class Snake:
    def __init__(self):
        self.body = [[230, 220],[230, 210],[230, 200],[230, 190]]
        self.direction = self.changeDirection = "down"
        self.color = green
    
    def move(self):
        if self.changeDirection == "up" and self.direction != "down":
            self.direction = "up"
        if self.changeDirection == "down" and self.direction != "up":
            self.direction = "down"
        if self.changeDirection == "left" and self.direction != "right":
            self.direction = "left"
        if self.changeDirection == "right" and self.direction != "left":
            self.direction = "right"

        head = self.body[0][:]

        if self.direction == "up":
            head[1]-=spd
        if self.direction == "down":
            head[1]+=spd
        if self.direction == "left":
            head[0]-=spd
        if self.direction == "right":
            head[0]+=spd

        self.body.insert(0, head)
        return head

    def grow(self,walls):
        global score
        score += 10
        walls.counter += 1

    def trim(self):
        self.body.pop()
    
    def draw(self,background):
        for x in self.body:
            pygame.draw.rect(background, green, pygame.Rect(x[0], x[1], wdth, hght))  

class Fruit:
    def __init__(self):
        self.position = [0,0]
        self.respawn([],[])
    
    def randomPosition(self,snake_body,walls_position):
        while True:
            newLocation = [random.randrange(0,SCREEN_WIDTH, 10),random.randrange(0, SCREEN_HEIGHT, 10)]
            if newLocation not in snake_body and newLocation not in walls_position:
                return newLocation
    
    def respawn(self, snake_body,walls_position):
        self.position = self.randomPosition(snake_body,walls_position)
    
    def draw(self,background):
        pygame.draw.rect(background, red, pygame.Rect(self.position[0], self.position[1], 10, 10))

class Wall:
    def __init__(self):
        self.position = []
        self.counter = 0
    
    def update(self, wallCounter, snake_body, fruit_position):
        while len(self.position) < wallCounter:
            newWall = [random.randrange(0,SCREEN_WIDTH,10),random.randrange(0,SCREEN_HEIGHT,10)]
            if newWall not in snake_body and newWall != fruit_position and newWall not in self.position:
                self.position.append(newWall)
    
    def draw(self,background):
        for x in self.position:
            pygame.draw.rect(background,(128,128,128),pygame.Rect(x[0],x[1],10,10))
    
    def check_collision(self,head):
        return head in self.position

#-----------------------END OF CLASSES------------------------
snake = Snake()
fruit = Fruit()
walls = Wall()

def gameOver():
    gameOverSurface = mainFont.render(("Your score is " + str(score)),True,white)
    gameOverRect = gameOverSurface.get_rect()
    gameOverRect.midtop = (SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
    background.blit(gameOverSurface, gameOverRect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

def showScore():
    scoreSurface = mainFont.render(str(score),True,white)
    scoreRect = scoreSurface.get_rect()
    scoreRect.midtop = (SCREEN_WIDTH//2,10)
    background.blit(scoreSurface,scoreRect)

menu_running = True
while menu_running:
    background.fill(black)
    for i,option in enumerate(options):
        yPos = 60+i*80
        if isinstance(option,str):
            menuSurface = mainFont.render(option, True, white)
            optionWidth, optionHeight = menuSurface.get_size()
        else:
            optionWidth,optionHeight = option.get_size()

        xPos = (SCREEN_WIDTH - optionWidth) // 2

        if i == selected_index:
            highlightRect = pygame.Rect(xPos - 10,yPos - 5,optionWidth+20,optionHeight+10)
            pygame.draw.rect(background,red,highlightRect)

        if isinstance(option,str):
            background.blit(menuSurface,(xPos,yPos))
        else:
            background.blit(option,(xPos,yPos))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_running = False
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                selected_index = (selected_index - 1) % len(options)
            elif event.key == K_DOWN:
                selected_index = (selected_index + 1) % len(options)
            elif event.key == K_RETURN:
                choice = options[selected_index]
                if choice == "Quit":
                    menu_running = False
                    pygame.quit()
                    quit()
                else:
                    difficulty_index = selected_index
                    menu_running = False


running = True
while running:
    clk.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

            elif event.key == K_LEFT:
                snake.changeDirection = "left"

            elif event.key == K_RIGHT:
                snake.changeDirection = "right"
            
            elif event.key == K_UP:
                snake.changeDirection = "up"
            
            elif event.key == K_DOWN:
                snake.changeDirection = "down"

    head = snake.move()
    if head[0] < 0 or head[0] >= SCREEN_WIDTH or head[1] < 0 or head[1] >= SCREEN_HEIGHT:
            gameOver()

    for x in snake.body[1:]:
        if head[0] == x[0] and head[1] == x[1]:
            gameOver()

    if head == fruit.position:
        snake.grow(walls)
        fruit.respawn(snake.body,walls.position)
    else:
        snake.trim()

    if difficulty_index == 0:
        fps = (score // 50) + 15
    elif difficulty_index == 1:
        fps = (score // 25) + 20
    elif difficulty_index == 2:
        fps = (score // 15) + 25
    elif difficulty_index == 3:
        fps = (score // 10) + 30
        walls.update(walls.counter,snake.body,fruit.position)
        if walls.check_collision(head):
            gameOver()


    background.fill(black)
    if difficulty_index == 3:
        walls.draw(background)
    snake.draw(background)
    fruit.draw(background)
    showScore()
    pygame.display.flip()

pygame.quit()
quit()