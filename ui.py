### Crimson
### 010/11/2012
### AAR

#Import modules
import pygame, sys, random
from pygame.locals import *

#Colours
WHITE = (255, 255, 255)
GREY = (128,128,128)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

#Autobots initialize
pygame.init()
screen = pygame.display.set_mode((1500,631), 0, 32)
pygame.display.set_caption('How Long Have You Been Beating That Horse?')

#Set up text
txt = pygame.font.SysFont('lucidaconsole',14) #for text to right of play area
itxt = pygame.font.SysFont('timesnewroman',16) #for objects in play area




#Classes
class Unit():
    def move(self, magnitude, direction):
        out_magnitude = 0
        plural = ''
        for i in range(magnitude):
            if direction == 'right' and self.x < 29 and m[current_map].playarea[self.x+1][self.y][0] == True:
                self.x += 1
                out_magnitude+=1
            elif direction == 'left' and self.x > 0 and m[current_map].playarea[self.x-1][self.y][0] == True:
                self.x -= 1
                out_magnitude+=1
            elif direction == 'down' and self.y < 29 and m[current_map].playarea[self.x][self.y+1][0] == True:
                self.y += 1
                out_magnitude+=1
            elif direction == 'up' and self.y > 0 and m[current_map].playarea[self.x][self.y-1][0] == True:
                self.y -= 1
                out_magnitude+=1
        if out_magnitude > 0:
            if out_magnitude > 1:
                plural = 's'
            infopaste("[{0}] moves [{1}] square{2} {3}.".format(self.name,out_magnitude,plural,direction))


class Map_Grid():
    def __init__(self,map_in):
        self.playarea = []
        self.mapfile = open(map_in).read().split("\n")
        self.name = map_in[0:map_in.find('.')]

        #Create a list of range 30 with 30 elements in it.
        for i in range(30):
            self.playarea.append([])
            for j in range(30):
                self.playarea[i].append([''])

        #Past here is detection/implementation of things in mapfile. To add later: doors, LOS blockers, destructible terrain (better to make mobs?), etc.
        for i in self.mapfile:
            if i.split()[0] == "room":
                for j in range(int(i.split()[1]),int(i.split()[3])+1):
                    for k in range(int(i.split()[2]),int(i.split()[4])+1):
                        self.playarea[j][k][0] = True
            if i.split()[0] == "door":
                self.playarea[int(i.split()[1])][int(i.split()[2])].append('door')
        for i,j in enumerate(self.playarea):
            for k,l in enumerate(self.playarea[i]):
                if l == '':
                    self.playarea[i][k][0] = False



class Player(Unit):
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name
        self.hp = 20
        self.ac = 2
        self.actions = 3
    def attack(self,amount,target):
        pass

class Enemy(Unit):
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.maxhp = 5
        self.hp = 5
        self.ac = 1
        self.name = name



#Functions
        
def check_keys():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                p.move(3,'up')
            if event.key == K_DOWN:
                p.move(3, 'down')
            if event.key == K_LEFT:
                p.move(3, 'left')
            if event.key == K_RIGHT:
                p.move(3, 'right')
            if event.key == K_a:
                if abs(a.x - p.x) < 2 and abs(a.y - p.y) <= 1: #if p and a are within 1 square
                    damage(2,a)

            if p.x == 3 and p.y == 3:
                if event.key == K_RETURN:
                    infopaste("Enter door.")
                    current_map = "map2"
                    infopaste(str(m[current_map].name))

                
def loc(in_x,in_y): #converts x,y from grid location to pixel location
    out_x = in_x*21 + 5
    out_y = in_y*21 + 1
    return out_x,out_y



def damage(amount,target):
    global info
    initHP = target.hp
    if amount > target.ac:
        if target.hp - amount + target.ac > 0:
            target.hp -= amount - target.ac
            infopaste("[{0}] is dealt [{1}] damage. Current HP: [{2}/{3}].".format(target.name, amount-target.ac, target.hp, target.maxhp))
        else:
            target.hp = 0
            infopaste("[{0}] is dealt [{1}] damage. Current HP: [{2}/{3}]. [{0}] is dead.".format(target.name, initHP, target.hp, target.maxhp))
    else:
        infopaste("[{0}] AC is greater than [{1}] damage. [{2}] is dealt no damage. Current HP [{3}/{4}].".format(target.ac, amount, target.name, target.hp, target.maxhp))


def infopaste(text):
    global info
    if len(info) > 12: #12 is arbitrary
        info.pop(0)
    info.append(text)

def update_screen():
    #background
    screen.fill(BLACK)
    for i in range(30):
        for j in range(30):
            if m[current_map].playarea[i][j][0] == True:
                pygame.draw.rect(screen, WHITE, Rect((1+i*21,1+j*21),(20,20)))
            elif m[current_map].playarea[i][j][0] == False:
                pygame.draw.rect(screen, BLACK, Rect((1+i*21,1+j*21),(20,20)))

            
    #player
    screen.blit(itxt.render("P", False, BLUE),(loc(p.x,p.y))) #model
    screen.blit(txt.render("{0}".format(p.name), False, BLUE, WHITE),(634,1)) #name
    screen.blit(txt.render("Hit Points: [{0}]".format(p.hp), False, WHITE),(634,16))
    screen.blit(txt.render("Location: [{0},{1}]".format(p.x,p.y), False, WHITE),(634,31))
    screen.blit(txt.render("Press [A] to attack targets within 1 unit of your location.".format(p.x,p.y), False, WHITE),(634,46))
    screen.blit(txt.render("Use the arrow keys to move.".format(p.x,p.y), False, WHITE),(634,61))
    

    #enemy
    screen.blit(itxt.render("H",False,RED),(loc(a.x,a.y))) #model
    screen.blit(txt.render("{0}".format(a.name), False, RED, WHITE),(634,91))
    screen.blit(txt.render("Hit Points: [{0}]".format(a.hp), False, WHITE),(634,106))
    screen.blit(txt.render("Location: [{0},{1}]".format(a.x,a.y), False, WHITE),(634,121))

    #info
    screen.blit(txt.render("What's Happening",False,BLACK,WHITE),(634,151))
    for i,j in enumerate(info):
        screen.blit(txt.render(j,False,WHITE),(634,(i+1)*15+151))
    screen.blit(txt.render("Information",False,BLACK,WHITE),(634,361))
    if p.x == 3 and p.y == 3:
        screen.blit(txt.render("Door",False,WHITE),(634,376))
    



#Set initial variables
name = "Your Name Here"  #input eventually. any trivial way to do this in pygame?
info = []
p = Player(0,0,name)
a = Enemy(4,4,"Monstrous Horse")

m = {"map" :Map_Grid("map.txt"),
     "map2":Map_Grid("map2.txt")}
current_map = "map"

#Main loop
if __name__ == '__main__':
    while True:
        check_keys()
        update_screen()
        pygame.display.update()


        
