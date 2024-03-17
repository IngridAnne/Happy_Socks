import pygame as pg
from settings import *
import random
import time


class Player:
    def __init__(self):
        self.points = 0
        
        self.image = pg.image.load('sock1.png')
        self.image = pg.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
          
        self.pos = [WIDTH//2, HEIGHT-START_PLATFORM_HEIGHT]
        self.vel = [0, 0]
        self.acc = [0, 0]
        
        self.dirty = False
        self.scrolling = False
        
        self.start = time.time()

    # Metode for hopping
    def jump(self):
        self.vel[1] = -20
    
    
        
    def update(self):
        self.collision_wall()
        dt = time.time() - self.start
        
        if dt > 3:
            self.dirty = False
            #self.start = time.time()
            
        if self.dirty and self.scrolling:
            self.acc = [0, 1.8]
            #self.color = BROWN
        elif self.dirty:
            self.acc = [0, 1.5]
            #self.color = BROWN
        elif self.scrolling:
            self.acc = [0, 1.3]
        elif not self.dirty:
            self.acc = [0, 0.8]
            #self.color = GREEN 
            
            
        # Henter tastene fra tastaturet
        keys = pg.key.get_pressed()
        
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc[0] = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc[0] = PLAYER_ACC
            
        # Friksjon
        self.acc[0] += self.vel[0]*PLAYER_FRICTION
        
        # Bevegelseslikning i x-retning
        self.vel[0] += self.acc[0]
        self.pos[0] += self.vel[0] + 0.5*self.acc[0]
        
        # Bevegelseslikning i y-retning
        self.vel[1] += self.acc[1]
        self.pos[1] += self.vel[1] + 0.5*self.acc[1]
        
        # Oppdaterer spillerens posisjon
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
    
    def collision_wall(self):
        if self.pos[0] > WIDTH:
            self.pos[0] = 0
        elif self.pos[0] <= 0:
            self.pos[0] = WIDTH
    

class Elements:
    def __init__(self, x, y, w, h, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        


class Platform(Elements):
    def __init__(self, x, y, w, h):
        image = pg.Surface((w, h))
        image.fill(BLACK)
        super().__init__(x, y, w, h, image)

        self.taken = False
        
class Washing_machine(Elements):
    def __init__(self, x, y):
        w = WASHING_MACHINE_SIDE
        h = WASHING_MACHINE_SIDE*W_RATIO # hvorfor w_ratio?
  
        image = pg.image.load('washing_machine.png')
        image = pg.transform.scale(image, (w, h))
        super().__init__(x, y, w, h, image)
 
class Mud(Elements):
    def __init__(self, x, y):
        w = MUD_WIDTH
        h = MUD_HEIGHT
        
        image = pg.image.load('mud.png')
        image = pg.transform.scale(image, (w, h))
        super().__init__(x, y, w, h, image)
        

class Hanger(Elements):
    def __init__(self, x, y):
        w = HANGER_WIDTH
        h = HANGER_HEIGHT
        
        image = pg.Surface((w, h))
        image.fill(BLACK)
        super().__init__(x, y, w, h, image)
        

class Clip(Elements):
    def __init__(self, x, y):
        w = CLIP_WIDTH
        h = CLIP_HEIGHT
        
        image = pg.image.load('clip.png')
        image = pg.transform.scale(image, (CLIP_WIDTH, CLIP_HEIGHT))
        super().__init__(x, y, w, h, image)
        
        self.speed = 5
        

class Detergent(Elements):
    def __init__(self, x, y):
        w = DETERGENT_WIDTH
        h = DETERGENT_HEIGHT
        self.speed = 0
        self.space = 40
        
        image = pg.image.load('detergent.png')
        image = pg.transform.scale(image, (DETERGENT_WIDTH, DETERGENT_HEIGHT))
        super().__init__(x, y, w, h, image)



class Background_element:
    def __init__(self, x, y, ratio):      
        self.rd = random.randint(40, 80)
        self.image = pg.image.load('cloud.png')
        # bildet er hentet fra: https://clipart-library.com/free/cloud-clipart-transparent-background.html
        self.image = pg.transform.scale(self.image, (self.rd*ratio, self.rd))
        
        self.x = x
        self.y = y
        self.speed = 2

"""
class Platform:
    def __init__(self, x, y, w, h):
        self.w = w
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.taken = False
        

class Washing_machine:
    def __init__(self, x, y):
  
        self.image = pg.image.load('washing_machine.png')
        self.image = pg.transform.scale(self.image, (WASHING_MACHINE_SIDE, WASHING_MACHINE_SIDE*W_RATIO))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        
        
class Mud:
    def __init__(self, x, y, w, h):
        #self.image = pg.Surface((w, h))
        #self.image.fill(BROWN)
        self.image = pg.image.load('mud.png')
        self.image = pg.transform.scale(self.image, (MUD_SIDE*M_RATIO, MUD_SIDE))
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
        
class Background_element:
    def __init__(self, x, y, ratio):      
        self.rd = random.randint(40, 80)
        self.image = pg.image.load('cloud.png')
        # bildet er hentet fra: https://clipart-library.com/free/cloud-clipart-transparent-background.html
        self.image = pg.transform.scale(self.image, (self.rd*ratio, self.rd))
        
        self.x = x
        self.y = y
        self.speed = 2
        
        
class Hanger:
    def __init__(self, x, y, w, h):
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Clip:
    def __init__(self, x, y, w, h):
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        self.speed = 5
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y  
"""


         




        




  
    

