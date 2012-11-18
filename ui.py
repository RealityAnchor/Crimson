### Crimson
### 2012/11/16
### AAR

#Import modules
import pygame, sys, time
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
pygame.display.set_caption('The Moor of Coagulation')

#Set up text
txt = pygame.font.SysFont('lucidaconsole',14) #for text to right of play area
itxt = pygame.font.SysFont('timesnewroman',16) #for objects in play area




#Classes
class Unit():
    def move(self, magnitude, direction):
        out_magnitude = 0
        plural = ''
        for i in range(magnitude):
            if direction == 'right' and self.x < 29 and main.m[main.current_map].playarea[self.x+1][self.y]['collision'] == False:
                self.x += 1
                out_magnitude+=1
            elif direction == 'left' and self.x > 0 and main.m[main.current_map].playarea[self.x-1][self.y]['collision'] == False:
                self.x -= 1
                out_magnitude+=1
            elif direction == 'down' and self.y < 29 and main.m[main.current_map].playarea[self.x][self.y+1]['collision'] == False:
                self.y += 1
                out_magnitude+=1
            elif direction == 'up' and self.y > 0 and main.m[main.current_map].playarea[self.x][self.y-1]['collision'] == False:
                self.y -= 1
                out_magnitude+=1
        if out_magnitude > 0:
            if out_magnitude > 1:
                plural = 's'
            main.infopaste("[{0}] moves [{1}] square{2} {3}.".format(self.name,out_magnitude,plural,direction))

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

class Mob(Unit):
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.maxhp = 5
        self.hp = 5
        self.ac = 1
        self.name = name


class Map():
    def __init__(self,map_in):
        self.playarea = []
        self.mapfile = open(map_in).read().split("\n")

        #Create a list of range 30 with 30 elements in it.
        for i in range(30):
            self.playarea.append([])
            for j in range(30):
                self.playarea[i].append({})
                self.playarea[i][j]['collision'] = True
                self.playarea[i][j]['door'] = False

        #Past here is detection/implementation of things in mapfile. To add later: doors, LOS blockers, destructible terrain (better to make mobs?), etc.
        for i in self.mapfile:
            if i.split(', ')[0] == "room":
                for j in range(int(i.split(', ')[1]),int(i.split(', ')[3])+1):
                    for k in range(int(i.split(', ')[2]),int(i.split(', ')[4])+1):
                        self.playarea[j][k]['collision'] = False
            if i.split(', ')[0] == "door":
                self.playarea[int(i.split(', ')[1])][int(i.split(', ')[2])]['door'] = True
                self.playarea[int(i.split(', ')[1])][int(i.split(', ')[2])]['door_target'] = [i.split(', ')[3],(int(i.split(', ')[4]),int(i.split(', ')[5]))]
            if i.split(', ')[0] == 'name':
                self.name = i.split(', ')[1]
                


class CrimsonGame():
    def __init__(self):
        #Set initial variables
        self.name = "Your Name Here"  #input eventually. any trivial way to do this in pygame?
        self.info = []
        self.p = Player(0,0,self.name)
        self.a = Mob(4,4,"Monstrous Horse")

        self.m = {"The Moor of Coagulation" :Map("map.txt"),
                  "The Hole of Murk":Map("map2.txt")}

        self.current_map = "The Moor of Coagulation"

        

    #Functions    
    def check_keys(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    self.p.move(3,'up')
                if event.key == K_DOWN:
                    self.p.move(3, 'down')
                if event.key == K_LEFT:
                    self.p.move(3, 'left')
                if event.key == K_RIGHT:
                    self.p.move(3, 'right')
                if event.key == K_a:
                    if self.a.hp > 0:
                        if abs(self.a.x - self.p.x) < 2 and abs(self.a.y - self.p.y) <= 1: #if p and a are within 1 square
                            self.damage(2,self.a)
                #Entering doors
                if self.m[self.current_map].playarea[self.p.x][self.p.y]['door'] == True:
                    if event.key == K_RETURN:
                        from_x, from_y = self.p.x, self.p.y
                        self.infopaste("You enter {0}.".format(self.m[self.current_map].playarea[self.p.x][self.p.y]['door_target'][0]))
                        self.p.x,self.p.y = self.m[self.current_map].playarea[self.p.x][self.p.y]['door_target'][1]
                        self.current_map = self.m[self.current_map].playarea[from_x][from_y]['door_target'][0]
                        pygame.display.set_caption('{0}'.format(self.m[self.current_map].name))
                        
                        

                    
    def loc(self,in_x,in_y,x_nudge=0,y_nudge=0): #converts x,y from grid location to pixel location
        out_x = in_x*21+5+x_nudge
        out_y = in_y*21+1-y_nudge
        return out_x,out_y



    def damage(self,amount,target):
        initHP = target.hp
        if amount > target.ac:
            if target.hp - amount + target.ac > 0:
                target.hp -= amount - target.ac
                self.infopaste("[{0}] is dealt [{1}] damage. Current HP: [{2}/{3}].".format(target.name, amount-target.ac, target.hp, target.maxhp))
            else:
                target.hp = 0
                self.infopaste("[{0}] is dealt [{1}] damage. Current HP: [{2}/{3}]. [{0}] is dead.".format(target.name, initHP, target.hp, target.maxhp))
        else:
            self.infopaste("[{0}] AC is greater than [{1}] damage. [{2}] is dealt no damage. Current HP [{3}/{4}].".format(target.ac, amount, target.name, target.hp, target.maxhp))


    def infopaste(self,text):
        if len(self.info) > 12: #12 is arbitrary
            self.info.pop(0)
        self.info.append(text)

    def update_screen(self):
        #background
        screen.fill(BLACK)
        for i in range(30):
            for j in range(30):
                if self.m[self.current_map].playarea[i][j]['collision'] == False:
                    pygame.draw.rect(screen, WHITE, Rect((1+i*21,1+j*21),(20,20)))
                elif self.m[self.current_map].playarea[i][j]['collision'] == True:
                    pygame.draw.rect(screen, BLACK, Rect((1+i*21,1+j*21),(20,20)))
                #doors
                if self.m[self.current_map].playarea[i][j]['door'] == True:
                    screen.blit(txt.render("[]", False, GREY),(self.loc(i,j,-2,-2)))

                
        #player
        screen.blit(itxt.render("@", False, BLUE),(self.loc(self.p.x,self.p.y,-2,+2))) #model
        screen.blit(txt.render("{0}".format(self.p.name), False, BLUE, WHITE),(634,1)) #name
        screen.blit(txt.render("Hit Points: [{0}]".format(self.p.hp), False, WHITE),(634,16))
        screen.blit(txt.render("Location: [{0},{1}]".format(self.p.x,self.p.y), False, WHITE),(634,31))
        screen.blit(txt.render("Press [A] to attack targets within 1 unit of your location.".format(self.p.x,self.p.y), False, WHITE),(634,46))
        screen.blit(txt.render("Use the arrow keys to move.".format(self.p.x,self.p.y), False, WHITE),(634,61))
        screen.blit(txt.render("Press [Return] to enter doors.".format(self.p.x,self.p.y), False, WHITE),(634,76))        
        

        #enemy
        if self.a.hp > 0:
            screen.blit(itxt.render("H",False,RED),(self.loc(self.a.x,self.a.y))) #model

        #info
        screen.blit(txt.render("What's Happening",False,BLACK,WHITE),(634,151))
        for i,j in enumerate(self.info):
            screen.blit(txt.render(j,False,WHITE),(634,(i+1)*15+151))
        screen.blit(txt.render("Information",False,BLACK,WHITE),(634,361))
        if self.m[self.current_map].playarea[self.p.x][self.p.y]['door'] == True:
            screen.blit(txt.render("Door to: {0}".format(self.m[self.current_map].playarea[self.p.x][self.p.y]['door_target'][0]),False,WHITE),(634,376))
    



main = CrimsonGame()

#Main loop
if __name__ == '__main__':
    while True:
        time.sleep(0.02)
        main.check_keys()
        main.update_screen()
        pygame.display.update()
