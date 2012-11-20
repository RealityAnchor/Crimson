### Crimson
### 2012/11/18
### AAR

#Import modules
import pygame, sys, time, random
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
        main.m[main.cur_map].playarea[main.p.x][main.p.y]['collision'] = False
        for i in range(magnitude):
            if direction == 'right' and self.x < 29 and main.m[main.cur_map].playarea[self.x+1][self.y]['collision'] == False:
                self.x += 1
                out_magnitude+=1
            elif direction == 'left' and self.x > 0 and main.m[main.cur_map].playarea[self.x-1][self.y]['collision'] == False:
                self.x -= 1
                out_magnitude+=1
            elif direction == 'down' and self.y < 29 and main.m[main.cur_map].playarea[self.x][self.y+1]['collision'] == False:
                self.y += 1
                out_magnitude+=1
            elif direction == 'up' and self.y > 0 and main.m[main.cur_map].playarea[self.x][self.y-1]['collision'] == False:
                self.y -= 1
                out_magnitude+=1
        if out_magnitude > 0:
            if out_magnitude > 1:
                plural = 's'
            main.infopaste("[{0}] moves [{1}] square{2} {3}.".format(self.name,out_magnitude,plural,direction))
        main.m[main.cur_map].playarea[main.p.x][main.p.y]['collision'] = True



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
    def get_target(self, mag): #mag = magnitude of range
        cur_target = None #current target
        main.r.x, main.r.y = main.p.x, main.p.y #reticule x/y
        mouse = 'up'
        while cur_target == None:
            main.update_screen()
            if mouse == 'up':
                screen.blit(main.r.unclicked,(main.mouse_to_grid(pygame.mouse.get_pos(),-4)))
            elif mouse == 'down':
                screen.blit(main.r.clicked,(main.mouse_to_grid(pygame.mouse.get_pos(),-4)))
            for event in pygame.event.get():
                if pygame.mouse.get_pressed()[0]:
                    mouse = 'down'
                elif not pygame.mouse.get_pressed()[0]:
                    mouse = 'up'
                if event.type == MOUSEBUTTONUP:
                    cur_target = main.loc2(main.mouse_to_grid(pygame.mouse.get_pos(),-4))
                    main.infopaste(str(str(main.m[main.cur_map].playarea[cur_target[0]][cur_target[1]]) + ', ' + str(cur_target[0])+'-'+str(cur_target[1])))
                    
                    
            pygame.display.update()
            
        
            
            
class Reticule(Unit):
    def __init__(self):
        self.unclicked = pygame.image.load("target.png")
        self.clicked = pygame.image.load("target_clicked.png")
        self.x = None
        self.y = None

class Mob(Unit):
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.maxhp = 2
        self.hp = self.maxhp
        self.ac = 0
        self.name = name


class Map():
    def __init__(self,map_in):
        self.playarea = []
        self.mob_dic = {}
        self.mapfile = open(map_in).read().split("\n")

        #Initialize 30x30 play area.
        for i in range(30):
            self.playarea.append([])
            for j in range(30):
                self.playarea[i].append({})
                self.playarea[i][j]['collision'] = True
                self.playarea[i][j]['wall'] = True
                self.playarea[i][j]['door'] = False
                self.playarea[i][j]['mob'] = None

        #Past here is detection/implementation of things in mapfile. To add later: doors, LOS blockers, destructible terrain (better to make mobs?), etc.
        for i in self.mapfile:
            if i.split(', ')[0] == "room":
                for j in range(int(i.split(', ')[1]),int(i.split(', ')[3])+1):
                    for k in range(int(i.split(', ')[2]),int(i.split(', ')[4])+1):
                        self.playarea[j][k]['collision'] = False
                        self.playarea[j][k]['wall'] = False
            if i.split(', ')[0] == "door":
                self.playarea[int(i.split(', ')[1])][int(i.split(', ')[2])]['door'] = True
                self.playarea[int(i.split(', ')[1])][int(i.split(', ')[2])]['door_target'] = [i.split(', ')[3],(int(i.split(', ')[4]),int(i.split(', ')[5]))]
            if i.split(', ')[0] == 'name':
                self.name = i.split(', ')[1]
                


class CrimsonGame():
    def __init__(self):
        #Set initial variables
        self.name = "Your Name Here"  #input eventually.
        self.p = Player(0,0,self.name) #Player
        self.info = []
        self.m = {"The Moor of Coagulation":Map("map.txt"), #All different maps
                  "The Hole of Murk":Map("map2.txt")}
        self.r = Reticule()
        self.cur_map = "The Moor of Coagulation"

        

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
                    for i in range(-1,2):
                        for j in range(-1,2):
                            if main.m[main.cur_map].playarea[main.p.x+i][main.p.y+j]['mob'] != None:
                                self.damage(2,main.m[main.cur_map].playarea[main.p.x+i][main.p.y+j]['mob'])
                if event.key == K_b:
                    main.p.get_target(5)
                if event.key == K_c:
                    main.spawn_mob(10,6,6,23,23)
    
                #Entering doors
                if self.m[self.cur_map].playarea[self.p.x][self.p.y]['door'] == True:
                    if event.key == K_RETURN:
                        from_x, from_y = self.p.x, self.p.y
                        self.infopaste("You enter {0}.".format(self.m[self.cur_map].playarea[self.p.x][self.p.y]['door_target'][0]))
                        self.p.x,self.p.y = self.m[self.cur_map].playarea[self.p.x][self.p.y]['door_target'][1]
                        self.cur_map = self.m[self.cur_map].playarea[from_x][from_y]['door_target'][0]
                        pygame.display.set_caption('{0}'.format(self.m[self.cur_map].name))
                        
    def spawn_mob(self,mob_magnitude,top,left,bot,right):
        free_spaces = main.detect_spaces(top,left,bot,right)
        if mob_magnitude > free_spaces:
            mob_magnitude = free_spaces
        for i in range(mob_magnitude):
            x,y = random.choice(range(top,bot+1)), random.choice(range(left,right+1))
            while self.m[self.cur_map].playarea[x][y]['collision'] == True:
                x,y = random.choice(range(top,bot+1)), random.choice(range(left,right+1))
            self.m[self.cur_map].playarea[x][y]['mob'] = Mob(x,y,'Goblin')
            self.m[self.cur_map].playarea[x][y]['collision'] = True

    def detect_spaces(self,top,left,bot,right):
        counter = 0
        for i in range(left, right+1):
            for j in range(top, bot+1):
                if self.m[self.cur_map].playarea[i][j]['collision'] == False:
                    counter += 1
        return counter

    def loc(self,in_x,in_y,x_nudge=0,y_nudge=0): #converts x,y from grid location to pixel location
        out_x = in_x*21+5+x_nudge
        out_y = in_y*21+1-y_nudge
        return out_x,out_y
    def loc2(self, xy): #converts x,y from pixel to grid
        out_x = int((xy[0]) / 21)
        out_y = int((xy[1]) / 21)
        return out_x,out_y
    def mouse_to_grid(self,xy,x_nudge=0,y_nudge=0): #converts mouse location to grid location
        out_x = int((xy[0]) / 21) * 21 + 5 + x_nudge
        out_y = int((xy[1]) / 21) * 21 + 1 - y_nudge
        return out_x,out_y

    def damage(self,amount,target):
        initHP = target.hp
        if amount > target.ac:
            if target.hp - amount + target.ac > 0:
                target.hp -= amount - target.ac
                self.infopaste("[{0}] is dealt [{1}] damage. Current HP: [{2}/{3}].".format(target.name, amount-target.ac, target.hp, target.maxhp))
            else:
                target.hp = 0
                self.m[self.cur_map].playarea[target.x][target.y]['mob'] = None
                self.m[self.cur_map].playarea[target.x][target.y]['collision'] = False
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
                if self.m[self.cur_map].playarea[i][j]['wall'] == False:
                    pygame.draw.rect(screen, WHITE, Rect((1+i*21,1+j*21),(20,20)))
                elif self.m[self.cur_map].playarea[i][j]['wall'] == True:
                    pygame.draw.rect(screen, BLACK, Rect((1+i*21,1+j*21),(20,20)))
                #doors
                if self.m[self.cur_map].playarea[i][j]['door'] == True:
                    screen.blit(txt.render("[]", False, GREY),(self.loc(i,j,-2,-2)))
                if self.m[self.cur_map].playarea[i][j]['mob'] != None:
                    screen.blit(itxt.render("G", False, RED),(self.loc(i,j)))

        #player
        screen.blit(itxt.render("@", False, BLUE),(self.loc(self.p.x,self.p.y,-2,+2))) #model
        screen.blit(txt.render("{0}".format(self.p.name), False, BLUE, WHITE),(634,1)) #name
        screen.blit(txt.render("Hit Points: [{0}]".format(self.p.hp), False, WHITE),(634,16))
        screen.blit(txt.render("Location: [{0},{1}]".format(self.p.x,self.p.y), False, WHITE),(634,31))
        screen.blit(txt.render("Press [A] to attack targets within 1 unit of your location.".format(self.p.x,self.p.y), False, WHITE),(634,46))
        screen.blit(txt.render("Press [B] and click on a square to get info about it.".format(self.p.x,self.p.y), False, WHITE),(634,61))
        screen.blit(txt.render("Use the arrow keys to move.".format(self.p.x,self.p.y), False, WHITE),(634,76))
        screen.blit(txt.render("Press [Return] to enter doors.".format(self.p.x,self.p.y), False, WHITE),(634,91))   

        #info
        screen.blit(txt.render("Action Log",False,BLACK,WHITE),(634,151))
        for i,j in enumerate(self.info):
            screen.blit(txt.render(j,False,WHITE),(634,(i+1)*15+151))
        screen.blit(txt.render("Information",False,BLACK,WHITE),(634,361))
        if self.m[self.cur_map].playarea[self.p.x][self.p.y]['door'] == True:
            screen.blit(txt.render("Door to: {0}".format(self.m[self.cur_map].playarea[self.p.x][self.p.y]['door_target'][0]),False,WHITE),(634,376))
    



main = CrimsonGame()

#Main loop
if __name__ == '__main__':
    while True:
        time.sleep(0.02)
        main.check_keys()
        main.update_screen()
        pygame.display.update()
