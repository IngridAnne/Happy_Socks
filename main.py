import pygame as pg
import sys, random, time
from settings import *
from sprites import *
import numpy as np
from pygame import mixer
import csv


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
        
        pg.display.set_caption('Happy Sock')
        
         
    # Metode for å starte et nytt spill
    def new(self):
        
        # Spiller bakgrunnsmusikk
        # https://www.educative.io/answers/how-to-play-an-audio-file-in-pygame
        mixer.init()
        mixer.music.load('POPCORN.mp3')
        mixer.music.set_volume(0.2)

        mixer.music.play()
        
        # Lister
        
        # Lager en plattform for bakken
        self.platform_list = [Platform(0, HEIGHT-START_PLATFORM_HEIGHT, WIDTH, START_PLATFORM_HEIGHT)]

        # Liste med vaskemaskiner
        self.washing_machine_list = []

        # Liste med gjørme
        self.mud_list = []

        # Liste med skyer
        self.background_element_list = []

        # Liste med klessnorer
        self.hanger_list = []
        
        # Liste med klyper
        self.clip_list = []
        
        # Liste med vaskemiddel
        self.detergent_list = []
        for i in range(3):
            detergent = Detergent(
                    WIDTH - DETERGENT_SIDE*2,
                    DETERGENT_SIDE*((i*2)+1),
                    DETERGENT_SIDE,
                    DETERGENT_SIDE)
            self.detergent_list.append(detergent)
        print(self.detergent_list)
        
        
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
            self.detergent_movement()
            self.update()
            self.scroll()
            if len(self.clip_list) > 0:
                self.motion()
            self.music()
            self.points()
            
        
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
                # Spilleren skal hoppe hvis vi trykker på piltast opp eller W
                if event.key == pg.K_UP or event.key == pg.K_w:
                    if self.jump:
                        self.player.jump()
                if event.key == pg.K_SPACE:
                    self.detergent_boost()
            
    
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
                #self.player.pos[1] = p.rect.y - PLAYER_HEIGHT
                self.player.pos[1] = p.rect.y - PLAYER_HEIGHT*1.71

                self.player.vel[1] = 0
                
            
    # Metode som tegner ting på skjermen
    def draw(self):
        # Fyller skjermen med en farge og elementer
        if self.score <= 200:
            self.screen.fill(LIGHTBLUE)
            ratio = 2
        elif self.score > 200 and self.score <= 400:
            self.screen.fill(ORANGE)
            ratio = 1.66
            for be in self.background_element_list:
                be.image = pg.transform.scale(pg.image.load('planet.png'), (be.rd*2, be.rd))
                # http://www.clker.com/clipart-6958.html
        else:
            self.screen.fill(PURPLE)
            ratio = 1.69
            for be in self.background_element_list:
                be.image = pg.transform.scale(pg.image.load('ufo.png'), (be.rd*2, be.rd))
                # https://no.pinterest.com/pin/584482857867587248/
                
        # Fyller bakgrunnselementliste med bakgrunnselementer
        while len(self.background_element_list) < 6:
            self.background_element_list.append(Background_element(random.randint(-20, WIDTH - 20),
                                    random.randint(-HEIGHT, -80),
                                    ratio
                                ))
            
        # Tegner bakgrunnselementene
        for be in self.background_element_list:
            self.screen.blit(be.image, (be.x, be.y))
        
        # Tegner vaskemaskinene
        for w in self.washing_machine_list:
            self.screen.blit(w.image, (w.rect.x, w.rect.y))
        
        # Tegner det som skal på skjermen
        draw_list = [self.platform_list, self.mud_list, self.hanger_list, self.clip_list, self.detergent_list]
        for i in range(len(draw_list)):
            for j in draw_list[i]:
                self.screen.blit(j.image, (j.rect.x, j.rect.y))
        
        # Tegner spilleren
        self.screen.blit(self.player.image, (self.player.pos[0], self.player.pos[1]))
        
        # Tegner poeng
        if self.score > 0:
            w = 80
            h = 40
            #pg.draw.rect(self.screen, BLACK,(WIDTH//2 - (w//2), HEIGHT - (h*1.2),w,h))
            self.text(f"{self.score}", WIDTH//2, HEIGHT- (h*0.7), WHITE, 30)
        
        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()
    
    def music(self):
        if self.playing == False:
            mixer.music.stop()
            mixer.music.load('died_song.mp3')

            mixer.music.play()
    
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
        self.text("Happy Sock!", WIDTH //2 , HEIGHT // 4, WHITE, 50)
        self.text("Arrows to move, Enter to boost, Space to jump!", WIDTH //2 , HEIGHT // 2, WHITE, 20)
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
        if (self.score == self.highscore):
            self.text(f"Ny highscore! : {self.highscore}", WIDTH //2 , HEIGHT // 2.5, WHITE, 25)
        else:
            self.text(f"Highscore: {self.highscore}", WIDTH //2 , HEIGHT // 2.5, WHITE, 25)
        self.text(f"Score: {self.score}", WIDTH //2 , HEIGHT // 2, WHITE, 25)
        self.text("Press enter to play again", WIDTH //2 , HEIGHT * 3/4, WHITE, 25)
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
                    if event.key == pg.K_RETURN:
                        waiting = False
                    
    # Metode for å finne poeng til spilleren
    def points(self):
        
        if self.playing == False:
            # Skriver inn poengscoren i en fil
            filename = "score.txt"
            with open(filename, "a") as file:
                file.write(f"{self.score}\n") 
            
            # Henter ut highscoren
            scores_list = np.loadtxt(filename, 'int')
            self.highscore = max(scores_list)
            
    
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
        for c in self.clip_list:
                if pg.Rect.colliderect(self.player.rect, c.rect):
                    self.playing = False
                    break
                
    # Metode for at en får en egenskap ved å ta boost
    def detergent_boost(self):
        if len(self.detergent_list) > 0:
            self.detergent_list.pop()
            self.player.vel[1] = -40
        else:
            pass
        
    # Metode for å gi bevegelse til vaskemiddelet
    def detergent_movement(self):
        for d in range (len(self.detergent_list)):
            det = self.detergent_list[d]
            det.rect.y += det.speed
            if det.rect.y < (det.space/4)+ det.space*(d):
                det.speed *= (-1)
            if det.rect.y > (det.space/2)+ det.space*(d):
                det.speed *= (-1)
        
    
    # Metode slik at klesklypen skal bevege seg
    def motion(self):
        clip = self.clip_list[0]
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
            for be in self.background_element_list:
                be.y += be.speed
            for be in self.background_element_list:
                if be.y > HEIGHT:
                    self.background_element_list.remove(be)
            
            
            # Lager sannsynligheten for at en egenskap skal tegnes på skjermen
            r = random.randint(1, 200)
        
        
            # Sjekker om en vaskemaskin skal bli laget
            if r == 1 and self.platform_list[-1].taken == False:
                self.platform_list[-1].taken = True
                new_washing_machine = Washing_machine(
                    self.platform_list[-1].rect.x + (MUD_WIDTH) - PLATFORM_HEIGHT/2,
                    self.platform_list[-1].rect.y - self.platform_list[-1].rect.h -((WASHING_MACHINE_SIDE*W_RATIO)/2),
                    WASHING_MACHINE_SIDE,
                    WASHING_MACHINE_SIDE)
                self.washing_machine_list.append(new_washing_machine)
                
            
            # Sjekker om gjørme skal bli laget
            r_mud = random.randint(1, 4)
            if r_mud == 1:
                if self.platform_list[-1].rect.w == PLATFORM_LONG_WIDTH:
                    r_mud = random.randint(1, 2)
                    print(r_mud)
                    if r_mud == 2 and self.platform_list[-1].taken == False:
                        self.platform_list[-1].taken = True
                        new_mud = Mud(
                        random.randint(self.platform_list[-1].rect.x, self.platform_list[-1].rect.x + self.platform_list[-1].rect.w - MUD_WIDTH),
                        self.platform_list[-1].rect.y,
                        MUD_WIDTH,
                        MUD_HEIGHT)
                        self.mud_list.append(new_mud)

            
            # Sjekker om en klessnorer og klyper skal bli laget
            if r == 3 and len(self.hanger_list) < 1:
                new_hanger = Hanger(
                    0,
                    0,
                    WIDTH,
                    2)
                self.hanger_list.append(new_hanger)
                
                new_clip = Clip(
                    0,
                    0,
                    CLIP_WIDTH,
                    50)
                self.clip_list.append(new_clip)
            
            # Scroller elementene nedover og fjerner hvis under skjermen
            scroll_list = [self.washing_machine_list, self.mud_list, self.hanger_list, self.clip_list]
            for i in range(len(scroll_list)):
                for j in scroll_list[i]:
                    j.rect.y += ELEMENT_SPEED
                for j in scroll_list[i]:
                    if j.rect.y > HEIGHT:
                        scroll_list[i].remove(j)
            
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
                    
                    # Sjekker om den ny plattform skal være lang
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
    game_object.show_end_screen()
   

# Avslutter pygame
pg.quit()
sys.exit() # Dersom det ikke er tilstrekkelig med pg.quit()


