import pygame as pg
import sys, random, time
from settings import *
from sprites import *



# Liste med klyper
clip_list = []

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
        # Lister
        
        # Lager en plattform for bakken
        self.platform_list = [Platform(0, HEIGHT-START_PLATFORM_HEIGHT, WIDTH, START_PLATFORM_HEIGHT)]

        # Liste med vaskemaskiner
        self.washing_machine_list = []

        # Liste med gjørme
        self.mud_list = []

        # Liste med skyer
        self.cloud_list = []

        # Liste med klessnorer
        self.hanger_list = []
        
        # Poeng
        self.score = 0
        
        # Lager spiller-objekt
        self.player = Player()
        
        # Lager plattformer
        while len(self.platform_list) < 7:
            # Lager ny plattform
            random_x = random.randint(10, WIDTH-110)
            random_y = random.randint(10, HEIGHT-20)
            
            new_platform = Platform(
                random_x,
                random_y,
                PLATFORM_WIDTH,
                PLATFORM_HEIGHT
            )
            
            new_platform_margin = Platform(random_x - PLATFORM_MARGIN, random_y - PLATFORM_MARGIN, PLATFORM_MARGIN_WIDTH, PLATFORM_MARGIN_HEIGHT)
            
            rd = random.randint(1, 8)
            if rd == 1:
                new_platform = Platform(
                    random_x,
                    random_y,
                    PLATFORM_LONG_WIDTH,
                    PLATFORM_HEIGHT
                )
                new_platform_margin = Platform(random_x - PLATFORM_MARGIN, random_y - PLATFORM_MARGIN, PLATFORM_MARGIN_LONG_WIDTH, PLATFORM_MARGIN_HEIGHT)
            
            
            
            
            safe = True
            
            # Sjekker om den nye plattformen kolliderer med noen av de gamle
            for p in self.platform_list:
                if pg.Rect.colliderect(new_platform_margin.rect, p.rect):
                    safe = False
                    break
            
            if safe:
                # Legger i lista
                self.platform_list.append(new_platform)
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
            if len(clip_list) > 0:
                self.motion()
            
        
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
        
        # Die!
        if self.player.pos[1] > HEIGHT:
            self.platform_list = [Platform(0, HEIGHT-START_PLATFORM_HEIGHT, WIDTH, START_PLATFORM_HEIGHT)]
            self.playing = False
            print("du døde")
        
        # Sjekker om vi faller
        if self.player.vel[1] > 0:
            collide = False

            # Sjekker om spilleren kolliderer med en plattform
            for p in self.platform_list:
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
        while len(self.cloud_list) < 9:
            self.cloud_list.append(Cloud(random.randint(-20, WIDTH - 20),
                                    random.randint(-HEIGHT, -80),
                                ))
        # Tegner skyene
        for c in self.cloud_list:
            self.screen.blit(c.image, (c.x, c.y))    
        
        # Tegner plattformene
        for p in self.platform_list:
            self.screen.blit(p.image, (p.rect.x, p.rect.y))
        
        # Tegner vaskemaskinene
        for w in self.washing_machine_list:
            self.screen.blit(w.image, (w.rect.x, w.rect.y))
        
        # Tegner gjørmen
        for m in self.mud_list:
            self.screen.blit(m.image, (m.rect.x, m.rect.y))
            
        # Tegner klessnoren
        for h in self.hanger_list:
            self.screen.blit(h.image, (h.rect.x, h.rect.y))
        
        # Tegner klypen
        for c in clip_list:
            self.screen.blit(c.image, (c.rect.x, c.rect.y))
        
        # Tegner spilleren
        self.screen.blit(self.player.image, self.player.pos)
        
        # Tegner poeng
        self.text(f"{self.score}", 40, 40, BLACK, 30)
        
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
        self.screen.fill(LIGHTBLUE)
        self.text("Happy Jump!", WIDTH //2 , HEIGHT // 4, WHITE, 50)
        self.text("Arrows to move, Space to jump!", WIDTH //2 , HEIGHT // 2, WHITE, 25)
        self.text("Press a key to play", WIDTH //2 , HEIGHT * 3/4, WHITE, 25)
        pg.display.flip()
        self.wait_for_key()
    
    # Metode som viser start-skjerm
    def show_end_screen(self):
        # Tester om spilleren ønsker å forlate vinduet og ikke vil se game over skjermen
        if not self.running:
            return
        self.screen.fill(LIGHTBLUE)
        self.text("GAME OVER!", WIDTH //2 , HEIGHT // 4, WHITE, 50)
        self.text(f"Score: {self.score}", WIDTH //2 , HEIGHT // 2, WHITE, 25)
        self.text("Press a key to play again", WIDTH //2 , HEIGHT * 3/4, WHITE, 25)
        pg.display.flip()
        self.wait_for_key()
    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
                
    
    # Metode for å gi spilleren en egenskap
    def enchantement(self):
        
        # Sjekker kollisjon med vaskemaskin og gir deretter økt fart
        for w in self.washing_machine_list:
                if pg.Rect.colliderect(self.player.rect, w.rect):
                    self.washing_machine_list.remove(w)
                    print("gir en boost")
                    self.player.vel[1] = -40
                    break
        
        # Sjekker kollisjon med gjørme og gir deretter minket fart
        for m in self.mud_list:
                if pg.Rect.colliderect(self.player.rect, m.rect) and self.player.vel[1] >= 0:
                    self.player.dirty = True
                    self.player.start = time.time()
                    print("Mud")
                    #self.player.not_dirty()
        
        # Sjekker kollisjon med klype og spiller dør hvis kollisjon
        for c in clip_list:
                if pg.Rect.colliderect(self.player.rect, c.rect):
                    self.playing = False
                    break
                    
    # Metode slik at klesklypen skal bevege seg
    def motion(self):
        clip = clip_list[0]
        clip.rect.x += clip.speed
        if clip.rect.x <= 0 or clip.rect.x >= WIDTH-CLIP_WIDTH:          
            clip.speed = clip.speed*(-1)
            
    # Metode for å scrolle alle elementene nedover
    def scroll(self):
        # Sjekker om spilleren er på den øverste delen av skjermen
        if self.player.rect.top <= HEIGHT / 4:
            

            # Synker graviditet når skjermen scroller ned
            self.player.scrolling = True
            
            
            # Skyene scroller nedover
            for c in self.cloud_list:
                c.y += CLOUD_SPEED
            for c in self.cloud_list:
                if c.y > HEIGHT:
                    self.cloud_list.remove(c)
            
            
            # Lager sannsynligheten for at en egenskap skal tegnes på skjermen
            r = random.randint(1, 200)
        
        
            # Sjekker om en vaskemaskin skal bli laget
            if r == 1 and self.platform_list[-1].taken == False:
                self.platform_list[-1].taken = True
                new_washing_machine = Washing_machine(
                    self.platform_list[-1].rect.x + (self.platform_list[-1].rect.w/2) - PLATFORM_HEIGHT/2,
                    self.platform_list[-1].rect.y - self.platform_list[-1].rect.h,
                    WASHING_MACHINE_SIDE,
                    WASHING_MACHINE_SIDE)
                self.washing_machine_list.append(new_washing_machine)
                
            # Vaskemaskinene scroller nedover
            for w in self.washing_machine_list:
                w.rect.y += ELEMENT_SPEED
            for w in self.washing_machine_list:
                if w.rect.y > HEIGHT:
                    self.washing_machine_list.remove(w)
            
            # Sjekker om gjørme skal bli laget
            r_mud = random.randint(1, 4)
            if r_mud == 1:
                if self.platform_list[-1].rect.w == PLATFORM_LONG_WIDTH:
                    r_mud = random.randint(1, 2)
                    print(r_mud)
                    if r_mud == 2 and self.platform_list[-1].taken == False:
                        self.platform_list[-1].taken = True
                        new_mud = Mud(
                        random.randint(self.platform_list[-1].rect.x, self.platform_list[-1].rect.x + self.platform_list[-1].rect.w - self.platform_list[-1].rect.w/2),
                        self.platform_list[-1].rect.y,
                        self.platform_list[-1].rect.w/2,
                        MUD_HEIGHT)
                        self.mud_list.append(new_mud)

            # Gjørmen scroller nedover
            for m in self.mud_list:
                m.rect.y += ELEMENT_SPEED
            for m in self.mud_list:
                if m.rect.y > HEIGHT:
                    self.mud_list.remove(m)
            
            # Sjekker om en klessnorer og klyper skal bli laget
            if r == 3 and len(hanger_list) < 1:
                new_hanger = Hanger(
                    0,
                    0,
                    WIDTH,
                    2)
                hanger_list.append(new_hanger)
                
                new_clip = Clip(
                    0,
                    0,
                    CLIP_WIDTH,
                    50)
                clip_list.append(new_clip)
                    
            
            # Klessnoren scroller nedover
            for h in self.hanger_list:
                h.rect.y += ELEMENT_SPEED
            for h in self.hanger_list:
                if h.rect.y > HEIGHT:
                    hanger_list.remove(h)
            
            # Klypene scroller nedover
            for c in clip_list:
                c.rect.y += ELEMENT_SPEED
            for c in clip_list:
                if c.rect.y > HEIGHT:
                    clip_list.remove(c)
              
            # Plattformene scroller nedover        
            for p in self.platform_list:
                p.rect.y += ELEMENT_SPEED
            for p in self.platform_list:
                if p.rect.y > HEIGHT:
                    self.score += 10
                    
                    self.platform_list.remove(p)
                    
                    # Lager ny plattform
                    random_x = random.randint(10, WIDTH-110)
                    
                    new_platform = Platform(
                        random_x,
                        0,
                        PLATFORM_WIDTH,
                        PLATFORM_HEIGHT
                    )
                    
                    new_platform_margin = Platform(random_x - PLATFORM_MARGIN, 0 - PLATFORM_MARGIN, PLATFORM_MARGIN_WIDTH, PLATFORM_MARGIN_HEIGHT)
                    
                    rd = random.randint(1, 8)
                    if rd == 1:
                        new_platform = Platform(
                            random_x,
                            0,
                            PLATFORM_LONG_WIDTH,
                            PLATFORM_HEIGHT
                        )
                        new_platform_margin = Platform(random_x - PLATFORM_MARGIN, 0 - PLATFORM_MARGIN, PLATFORM_MARGIN_LONG_WIDTH, PLATFORM_MARGIN_HEIGHT)
                    
                    
                    
                    safe = True
                    
                    # Sjekker om den nye plattformen kolliderer med noen av de gamle
                    for p in self.platform_list:
                        if pg.Rect.colliderect(new_platform_margin.rect, p.rect):
                            safe = False
                            break
                    
                    if safe:
                        # Legger i lista
                        self.platform_list.append(new_platform)
                    else:
                        print("Plattformen kolliderte, prøver på nytt")       
        else:
            self.player.scrolling = False
            

    
# Lager et spill-objekt
game_object = Game()
game_object.show_start_screen()

# Spill-løkken
while game_object.running:
    # Starter et nytt spill
    game_object.new()
   

# Avslutter pygame
pg.quit()
sys.exit() # Dersom det ikke er tilstrekkelig med pg.quit()


