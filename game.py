import random
from easygui import *
import pygame

health = 5
clock = pygame.time.Clock()
openfile = open("monsters.txt")
monsterList = []
for line in openfile:
    line = line.replace("\n", "")
    line = line.split(",")
    monsterList.append(line)

#---------------------------------------------------------------------------------------------------------------------------------#

def guessing():
    t = 0
    hits = 1
    choices=[str(compGuess), str(random.randint(0, 15)), str(random.randint(0,15)), str(random.randint(0, 15))]
    if int(monsterLevel) > 50:
        guesses = 3
        choices.append(str(random.randint(0,100)))
        choices.append(str(random.randint(0,100)))
    else:
        guesses = 2
    while int(t) < int(guesses):
        msgbox(msg=("You have been encountered by a level " + str(monsterLevel) + " " + str(monsterName) + "!"), title="Danger!")
        if int(monsterLevel) > 50:
            choices[1] = str(random.randint(0,100))
            choices[2] = str(random.randint(0,100))
            random.shuffle(choices)
        if int(monsterLevel) < 50:
            random.shuffle(choices)
        playerGuess = buttonbox("Try to guess the correct number!", choices = choices)
        playerGuess = int(playerGuess)
        if playerGuess == compGuess:
            if hits == 1:
                msgbox(msg=("You killed the monster in " + str(hits) + " hit!"), title="Success!")
            else:
                msgbox(msg=("You killed the monster in " + str(hits) + " hits!"), title="Success!") 
            t = 1
            return True
            break
        elif playerGuess in range(round(int(compGuess)*0.9), round(int(compGuess)*1.1)):
            msgbox("The monster lost 5 health. (CRITICAL HIT!)")
            hits += 1
            t += 1
        elif playerGuess in range(round(int(compGuess)*0.8), round(int(compGuess)*1.2)):
            msgbox("The monster lost 4 health.")
            hits += 1
            t += 1
        elif playerGuess in range(round(int(compGuess)*0.7), round(int(compGuess)*1.3)):
            msgbox("The monster lost 3 health.")
            hits += 1
            t += 1
        elif playerGuess in range(round(int(compGuess)*0.6), round(int(compGuess)*1.4)):
            msgbox("The monster lost 2 health.")
            hits += 1
            t += 1
        elif playerGuess in range(round(int(compGuess)*0.5), round(int(compGuess)*1.5)):
            msgbox("The monster lost 1 health.")
            hits += 1
            t += 1
        elif playerGuess >= (round(int(compGuess)*0)):
            msgbox("You missed.")
            t += 1
        elif int(t) == int(guesses):
            break

#--------------------------------------------------------------------------------------------------#
class Player():
    
    def __init__(self):
        self.rect = pygame.Rect(16, 16, 16, 16)
        
    def move(self, dx, dy):
        
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)
    
    def move_single_axis(self, dx, dy):
        
        #Moving the player
        self.rect.x += dx
        self.rect.y += dy

        #If the player collides with a wall
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: 
                    self.rect.right = wall.rect.left
                if dx < 0: 
                    self.rect.left = wall.rect.right
                if dy > 0: 
                    self.rect.bottom = wall.rect.top
                if dy < 0: 
                    self.rect.top = wall.rect.bottom

#Classes to hold the walls and game-rectangles
class Wall():
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

class GameRects():
    def __init__(self, pos):
        games.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

#--------------------------------------------------------------------------------------------------#

pygame.init()

#Setting up the display...
pygame.display.set_caption("Get to the red square!")
screen = pygame.display.set_mode((320, 240))
walls = []
games = []
player = Player()

#The layout of the level
level = [
"WWWWWWWWWWWWWWWWWWWW",
"W     N            W",
"WWWWWWWWWWWWWWWWWW W",
"W          N       W",
"W WWWWWWWWWWWWWWWWWW",
"W          N       W",
"WWWWWWWWWWWWWWWWWW W",
"W   N    N         W",
"W WWWWWWWWWWWWWWWWWW",
"W         N        W",
"WWWWWWWWWWWWWWWWWW W",
"W        N         W",
"W WWWWWWWWWWWWWWWWWW",
"W          E       W",
"WWWWWWWWWWWWWWWWWWWW",
]

# W = walls, E = exit, N = game
x = y = 0
for row in level:
    for column in row:
        if column == "W":
            Wall((x, y))
        if column == "E":
            end_rect = pygame.Rect(x, y, 16, 16)
        if column == "N":
            GameRects((x, y))
        x += 16
    y += 16
    x = 0

running = True
while running:
    clock.tick(60) 
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            quit()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
            quit()
    
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.move(-2, 0)
    if key[pygame.K_RIGHT]:
        player.move(2, 0)
    if key[pygame.K_UP]:
        player.move(0, -2)
    if key[pygame.K_DOWN]:
        player.move(0, 2)

    # Drawing everything + implementing the game
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    for game in games:
        gamerectangle = pygame.draw.rect(screen, (255, 0, 0), game.rect)
        if player.rect.colliderect(gamerectangle):
            monster = monsterList[random.randint(0, int(len(monsterList))-1)]
            monsterLevel = monster[1]
            monsterName = monster[0]
            compGuess = random.randint(0, 15)
            while True:
                if guessing() == True:
                    msgbox("You won the fight!")
                    games.remove(gamerectangle)
                    break
                elif health == 0:
                    msgbox("You lost the game. Better luck next time!")
                    running = False
                    quit()
                else:
                    health -= 1
                    msgbox(msg=("You lost 1 health. You have " + str(health) + " health remaining."), title="You failed.")
                    games.remove(gamerectangle)
                    break
    if player.rect.colliderect(end_rect):
        msgbox("Congratulations! You won the game!")
        quit()
    pygame.draw.rect(screen, (0, 255, 0), end_rect)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    pygame.display.flip()
