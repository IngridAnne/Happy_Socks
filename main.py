import pygame as pg
import sys, random
from settings import *
from sprites import *

# hei på deg

# Lager en plattform for bakken
platform_list = [Platform(0, HEIGHT-40, WIDTH, 40)]

# Liste med vaskemaskiner
washing_machine_list = []


class Game:
    def __init__(self):
        # Initiere pygame
        pg.init()

        # Lager hovedvinduet
        self.screen = pg.display.set_mode(SIZE)

        # Lager en klokke
        self.clock = pg.time.Clock()
        
        # Attributt som styrer om spillet skal kjøres
        self.running = True
        
        
    # Metode for å starte et nytt spill
    def new(self):
        # Lager spiller-objekt
        self.player = Player()
        
        # Lager plattformer
        while len(platform_list) < 7:
            # Lager ny plattform
            new_platform = Platform(
                random.randint(10, WIDTH-110),
                random.randint(50, HEIGHT-210),
                100,
                20
            )
            
            safe = True
            
            # Sjekker om den nye plattformen kolliderer med noen av de gamle
            for p in platform_list:
                if pg.Rect.colliderect(new_platform.rect, p.rect):
                    safe = False
                    break
            
            if safe:
                # Legger i lista
                platform_list.append(new_platform)
            else:
                print("Plattformen kolliderte, prøver på nytt")
            
        
        self.run()


    # Metode som kjører spillet
    def run(self):
        # Game loop
        self.playing = True
        
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()
            self.enchantement()
            self.update()
            self.scroll()
        
    # Metode som håndterer hendelser
    def events(self):
        # Går gjennom hendelser (events)
        for event in pg.event.get():
            # Sjekker om vi ønsker å lukke vinduet
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False # Spillet skal avsluttes
            
            if event.type == pg.KEYDOWN:
                # Spilleren skal hoppe hvis vi trykker på mellomromstasten
                if event.key == pg.K_SPACE:
                    if self.jump:
                        self.player.jump()
            
    
    # Metode som oppdaterer
    def update(self):
        self.player.update()
        
        self.jump = False
        
        # Sjekker om vi faller
        if self.player.vel[1] > 0:
            collide = False
            if self.player.pos[1] > HEIGHT:
                print("Du døde")
                """
                Game over skjerm!!!
                """
            
            # Sjekker om spilleren kolliderer med en plattform
            for p in platform_list:
                if pg.Rect.colliderect(self.player.rect, p.rect):
                    collide = True
                    self.jump = True
                    break
            
            # Spilleren blir stående oppå plattformen når collide er lik true
            if collide:
                self.player.pos[1] = p.rect.y - PLAYER_HEIGHT
                self.player.vel[1] = 0
                
            
    # Metode som tegner ting på skjermen
    def draw(self):
        # Fyller skjermen med en farge
        self.screen.fill(WHITE)
        
        # Tegner plattformene
        for p in platform_list:
            self.screen.blit(p.image, (p.rect.x, p.rect.y))
        
        # Tegner vaskemaskinene
        for w in washing_machine_list:
            self.screen.blit(w.image, (w.rect.x, w.rect.y))
        
        # Tegner spilleren
        self.screen.blit(self.player.image, self.player.pos)
        
        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()
    
    
    # Metode som viser start-skjerm
    def show_start_screen(self):
        pass
    
    # Metode for å gi spilleren en egenskap
    def enchantement(self):
        
        # Sjekkker kollisjon med vaskemaskin og gir deretter økt fart
        for w in washing_machine_list:
                if pg.Rect.colliderect(self.player.rect, w.rect):
                    washing_machine_list.remove(w)
                    print("gir en boost")
                    self.player.vel[1] = -40
                    break
    
    # Metode for å scrolle alle elementene nedover
    def scroll(self):
        # Sjekker om spilleren er på den øverste delen av skjermen
        if self.player.rect.top <= HEIGHT / 4:
            
            # Lager sannsynligheten for at en egenskap skal tegnes på skjermen
            r = random.randint(1, 200)
        
            # Sjekker om et vaskemaskin skal bli laget
            if r == 1:
                new_washing_machine = Washing_machine(
                    platform_list[-1].rect.x + (platform_list[-1].rect.w/2) - 20/2,
                    platform_list[-1].rect.y - platform_list[-1].rect.h,
                    20,
                    20)
                washing_machine_list.append(new_washing_machine)
            # Vaskemaskinene scroller nedover
            for w in washing_machine_list:
                w.rect.y += 6
                if w.rect.y > HEIGHT:
                    washing_machine_list.remove(w)
                    
            # Plattformene scroller nedover        
            for p in platform_list:
                p.rect.y += 6
                if p.rect.y > HEIGHT:
                    platform_list.remove(p)
                    newest_platform = Platform(
                        random.randint(10, WIDTH-110),
                        0,
                        100,
                        20
                        )
                    platform_list.append(newest_platform)
            

    
    
# Lager et spill-objekt
game_object = Game()

# Spill-løkken
while game_object.running:
    # Starter et nytt spill
    game_object.new()
    


# Avslutter pygame
pg.quit()
sys.exit() # Dersom det ikke er tilstrekkelig med pg.quit()


