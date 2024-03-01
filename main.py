import pygame as pg
import sys, random, time
from settings import *
from sprites import *


# Lager en plattform for bakken
platform_list = [Platform(0, HEIGHT-START_PLATFORM_HEIGHT, WIDTH, START_PLATFORM_HEIGHT)]

# Liste med vaskemaskiner
washing_machine_list = []

# Liste med gjørme
#mud_list = [Mud(platform_list[-1].rect.x,platform_list[-1].rect.y,platform_list[-1].rect.w,5)]
mud_list = []

# Liste med skyer
cloud_list = []

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
            random_x = random.randint(10, WIDTH-110)
            random_y = random.randint(10, HEIGHT-20)
            
            new_platform = Platform(
                random_x,
                random_y,
                PLATFORM_WIDTH,
                PLATFORM_HEIGHT
            )
            
            new_platform_margin = Platform(random_x - 10, random_y - 10, 120, 40)
            
            safe = True
            
            # Sjekker om den nye plattformen kolliderer med noen av de gamle
            for p in platform_list:
                if pg.Rect.colliderect(new_platform_margin.rect, p.rect):
                    safe = False
                    break
            
            if safe:
                # Legger i lista
                platform_list.append(new_platform)
            else:
                print("Plattformen kolliderte, prøver på nytt")
            
        
        mud_list.append(Mud(
                    platform_list[1].rect.x,
                    platform_list[1].rect.y,
                    platform_list[1].rect.w,
                    5)
        )
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
        self.screen.fill(LIGHTBLUE)
        

        # Tegner skyer på skjermen
        while len(cloud_list) < 9:
            cloud_list.append(Cloud(random.randint(-20, WIDTH - 20),
                                    random.randint(-HEIGHT, -80),
                                ))
        # Tegner skyene
        for c in cloud_list:
            self.screen.blit(c.image, (c.x, c.y))    
        
        # Tegner plattformene
        for p in platform_list:
            self.screen.blit(p.image, (p.rect.x, p.rect.y))
        
        # Tegner vaskemaskinene
        for w in washing_machine_list:
            self.screen.blit(w.image, (w.rect.x, w.rect.y))
        
        # Tegner gjørmen
        for m in mud_list:
            self.screen.blit(m.image, (m.rect.x, m.rect.y))
        
        # Tegner spilleren
        self.screen.blit(self.player.image, self.player.pos)
        
        # Tegner poeng
        self.text(f"{self.player.points}", 20, 20, BLACK, 30)
        
        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()
    
    # Funksjon som skriver tekst til vinduet
    def text(self, text, x, y, color, fontSize):
        font = pg.font.SysFont("Arial", fontSize)
        textPicture = font.render(text, True, color)
        textRectangle = textPicture.get_rect()
        
        # Putter i vinduet
        self.screen.blit(textPicture, (x - textRectangle.width//2, y - textRectangle.height//2))
        
    # Metode som viser start-skjerm
    def show_start_screen(self):
        pass
    
    # Metode for å gi spilleren en egenskap
    def enchantement(self):
        
        # Sjekker kollisjon med vaskemaskin og gir deretter økt fart
        for w in washing_machine_list:
                if pg.Rect.colliderect(self.player.rect, w.rect):
                    washing_machine_list.remove(w)
                    print("gir en boost")
                    self.player.vel[1] = -40
                    break
        
        # Sjekker kollisjon med gjørme og gir deretter minket fart
        for m in mud_list:
                if pg.Rect.colliderect(self.player.rect, m.rect) and self.player.vel[1] >= 0:
                    self.player.dirty = True
                    self.player.start = time.time()
                    print("Mud")
                    #self.player.not_dirty()
                    
                    
    
    # Metode for å scrolle alle elementene nedover
    def scroll(self):
        # Sjekker om spilleren er på den øverste delen av skjermen
        if self.player.rect.top <= HEIGHT / 4:
            
            
            # Skyene scroller nedover
            for c in cloud_list:
                c.y += CLOUD_SPEED
            for c in cloud_list:
                if c.y > HEIGHT:
                    cloud_list.remove(c)
            
            
            # Lager sannsynligheten for at en egenskap skal tegnes på skjermen
            r = random.randint(1, 200)
        
        
            # Sjekker om en vaskemaskin skal bli laget
            if r == 1 and platform_list[-1].taken == False:
                platform_list[-1].taken = True
                new_washing_machine = Washing_machine(
                    platform_list[-1].rect.x + (platform_list[-1].rect.w/2) - PLATFORM_HEIGHT/2,
                    platform_list[-1].rect.y - platform_list[-1].rect.h,
                    WASHING_MACHINE_SIDE,
                    WASHING_MACHINE_SIDE)
                washing_machine_list.append(new_washing_machine)
                
            # Vaskemaskinene scroller nedover
            for w in washing_machine_list:
                w.rect.y += ELEMENT_SPEED
            for w in washing_machine_list:
                if w.rect.y > HEIGHT:
                    washing_machine_list.remove(w)
             
             
            # Sjekker om gjørme skal bli laget
            if r == 2 and platform_list[-1].taken == False:
                platform_list[-1].taken = True
                new_mud = Mud(
                    platform_list[-1].rect.x,
                    platform_list[-1].rect.y,
                    platform_list[-1].rect.w,
                    MUD_HEIGHT)
                mud_list.append(new_mud)    


            # Gjørmen scroller nedover
            for m in mud_list:
                m.rect.y += ELEMENT_SPEED
            for m in mud_list:
                if m.rect.y > HEIGHT:
                    mud_list.remove(m)
              
              
            # Plattformene scroller nedover        
            for p in platform_list:
                p.rect.y += ELEMENT_SPEED
            for p in platform_list:
                if p.rect.y > HEIGHT:
                    self.player.points += 1
                    
                    platform_list.remove(p)
                    
                    # Lager ny plattform
                    random_x = random.randint(10, WIDTH-110)
                    
                    new_platform = Platform(
                        random_x,
                        0,
                        PLATFORM_WIDTH,
                        PLATFORM_HEIGHT
                    )
                    
                    new_platform_margin = Platform(random_x - 10, 0 - 10, 120, 40)
                    
                    safe = True
                    
                    # Sjekker om den nye plattformen kolliderer med noen av de gamle
                    for p in platform_list:
                        if pg.Rect.colliderect(new_platform_margin.rect, p.rect):
                            safe = False
                            break
                    
                    if safe:
                        # Legger i lista
                        platform_list.append(new_platform)
                    else:
                        print("Plattformen kolliderte, prøver på nytt")
            

    
# Lager et spill-objekt
game_object = Game()

# Spill-løkken
while game_object.running:
    # Starter et nytt spill
    game_object.new()
    


# Avslutter pygame
pg.quit()
sys.exit() # Dersom det ikke er tilstrekkelig med pg.quit()


