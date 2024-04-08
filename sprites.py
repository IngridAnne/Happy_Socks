# Importerer nyttige biblioteker
import pygame as pg
from pygame import mixer
from settings import *
import random
import time


class Player:
    def __init__(self):
        self.points = 0
        
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        
        self.image = pg.image.load('Bilder/sock1.png')
        self.image = pg.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        self.rect = self.image.get_rect()
          
        self.pos = [WIDTH//2, HEIGHT-PLAYER_START_POSITION]
        self.vel = [0, 0]
        self.acc = [0, 0]
        
        self.dirty = False
        self.scrolling = False
        
        # Liste med bilder
        self.images = [
            pg.transform.scale(pg.image.load('Bilder/sock1.png'), (PLAYER_WIDTH, PLAYER_HEIGHT)),
            pg.transform.scale(pg.image.load('Bilder/sock2.png'), (PLAYER_WIDTH, PLAYER_HEIGHT*STRETCH)),
            pg.transform.scale(pg.image.load('Bilder/dirty_sock1.png'), (PLAYER_WIDTH, PLAYER_HEIGHT)),
            pg.transform.scale(pg.image.load('Bilder/dirty_sock2.png'), (PLAYER_WIDTH, PLAYER_HEIGHT*STRETCH))
            ]
        
        self.start = time.time()
        


    # Metode for hopping
    def jump(self):
        self.vel[1] = -20
 
        
        if self.dirty:
            # musikken er hentet fra: https://pixabay.com/sound-effects/search/mud/
            pg.mixer.Channel(0).play(pg.mixer.Sound('Lyd/mud.mp3'), maxtime=600)
        else:
            # musikken er hentet fra: https://pixabay.com/sound-effects/search/game/
            mixer.Channel(0).set_volume(0.2)
            pg.mixer.Channel(0).play(pg.mixer.Sound('Lyd/jump.mp3'))
    
    
    def update(self):
        self.collision_wall()
        dt = time.time() - self.start
        
        if dt > 3:
            self.dirty = False
            
        if self.dirty and self.scrolling:
            self.acc = [0, 1.8]
        elif self.dirty:
            self.acc = [0, 1.5]
        elif self.scrolling:
            self.acc = [0, 1.3]
        elif not self.dirty:
            self.acc = [0, 0.8]
            
            
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
    
    # Sokken endrer utseende ved hopp
    def change_look(self):
        if self.dirty:
            self.image = self.images[3]
        else:
            self.image = self.images[1]
         
class Elements:
    def __init__(self, x, y, w, h, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        

class Platform(Elements):
    def __init__(self, x, y, w, h, img = 'Bilder/platform.png'):
        # Plattformene er screen fra: https://www.google.com/url?sa=i&url=https%3A%2F%2Fsgfincorp.com%2F%3Fa%3Dfree-platform-game-assets-gui-by-bayat-games-kk-wkVZdLF9&psig=AOvVaw0qxGt-1A5LFFYGGTzkSsZL&ust=1711129113138000&source=images&cd=vfe&opi=89978449&ved=0CBQQjhxqFwoTCJCqm-nyhYUDFQAAAAAdAAAAABAR
        #image = pg.Surface((w, h))
        #image.fill(DARKBROWN)
        image = pg.image.load(img)
        image = pg.transform.scale(image, (w, h))
        
        super().__init__(x, y, w, h, image)

        self.taken = False
        
        
class Washing_machine(Elements):
    def __init__(self, x, y):
        w = WASHING_MACHINE_SIDE
        h = WASHING_MACHINE_SIDE*W_RATIO
  
        image = pg.image.load('Bilder/washing_machine.png')
        image = pg.transform.scale(image, (w, h))
        super().__init__(x, y, w, h, image)
 
 
class Mud(Elements):
    def __init__(self, x, y):
        w = MUD_WIDTH
        h = MUD_HEIGHT
        
        image = pg.image.load('Bilder/mud.png')
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
        
        image = pg.image.load('Bilder/clip.png')
        image = pg.transform.scale(image, (CLIP_WIDTH, CLIP_HEIGHT))
        super().__init__(x, y, w, h, image)
          

class Detergent(Elements):
    def __init__(self, x, y):
        w = DETERGENT_WIDTH
        h = DETERGENT_HEIGHT
        self.speed = 0.6
        
        image = pg.image.load('Bilder/detergent.png')
        image = pg.transform.scale(image, (DETERGENT_WIDTH, DETERGENT_HEIGHT))
        super().__init__(x, y, w, h, image)


class Background_element:
    def __init__(self, x, y, ratio):      
        self.rd = random.randint(40, 80)
        self.image = pg.image.load('Bilder/cloud.png')
        # bildet er hentet fra: https://clipart-library.com/free/cloud-clipart-transparent-background.html
        self.image = pg.transform.scale(self.image, (self.rd*ratio, self.rd))
        
        self.x = x
        self.y = y
        self.speed = 2
