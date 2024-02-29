import pygame as pg
from settings import *
import random


class Player:
    def __init__(self):
        self.image = pg.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        """
        self.rect.center = (
            WIDTH//2 - PLAYER_WIDTH//2,
            HEIGHT//2 - PLAYER_HEIGHT//2
        )
        
        self.pos = list(self.rect.center)
        """
        self.pos = [WIDTH//2, HEIGHT-START_PLATFORM_HEIGHT]
        self.vel = [0, 0]
        self.acc = [0, 0]
    
        self.dirty = False
    
    # Metode for hopping
    def jump(self):
        self.vel[1] = -20
        
    def is_dirty(self):
        self.dirty = True
        self.image.fill(BROWN)
        
    def is_not_dirty(self):
        self.dirty = False
        self.image.fill(GREEN)
        
    def update(self):
        self.collision_wall()
        
        if not self.dirty:
            self.acc = [0, 0.8]
        else:
            self.acc = [0, 3]
            
        # Henter tastene fra tastaturet
        keys = pg.key.get_pressed()
        
        if keys[pg.K_LEFT]:
            self.acc[0] = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc[0] = PLAYER_ACC
            
        # Friksjon
        self.acc[0] += self.vel[0]*PLAYER_FRICTION
        
        # Bevegelseslikning i x-retning
        self.vel[0] += self.acc[0]
        self.pos[0] += self.vel[0] + 0.5*self.acc[0]
        
        # Bevegelseslikning i y-retning
        self.vel[1] += self.acc[1]
        self.pos[1] += self.vel[1] + 0.5*self.acc[1]
        
        # Oppdaterer rektangelets posisjon
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
    
    def collision_wall(self):
        if self.pos[0] > WIDTH:
            self.pos[0] = 0
        elif self.pos[0] <= 0:
            self.pos[0] = WIDTH
    
    


class Platform:
    def __init__(self, x, y, w, h):
        self.image = pg.Surface((w, h))
        self.image.fill(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.taken = False


class Washing_machine:
    def __init__(self, x, y, w, h):
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    
class Mud:
    def __init__(self, x, y, w, h):
        self.image = pg.Surface((w, h))
        self.image.fill(BROWN)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.rd = random.randint(40, 80)
        self.image = pg.image.load('cloud.png')
        # bildet er hentet fra: https://clipart-library.com/free/cloud-clipart-transparent-background.html
        self.image = pg.transform.scale(self.image, (self.rd*2, self.rd))

    
    
    
    
    
    
    
    
    
    
    