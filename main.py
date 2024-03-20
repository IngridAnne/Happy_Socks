# Importerer nyttige biblioteker
import pygame as pg
import sys, random, time
from settings import *
from sprites import *
import numpy as np
from pygame import mixer
import csv


# Lager gameklassen
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
        
        # Begynner å spille bakgrunnsmusikken
        self.play_background_music()
        
        
        
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
        
        # Liste med vaskemiddeler
        self.detergent_list = []
        for i in range(3):
            detergent = Detergent(
                    WIDTH - DETERGENT_WIDTH*2,
                    DETERGENT_WIDTH*((i*2)+1))
            self.detergent_list.append(detergent)
        #print(self.detergent_list)
        
        
        
        # Poeng
        self.score = 0
        
        # Poeng som avgjør om en får ekstra boost
        self.score_boost = 0
        
        # Høyeste tall i random
        self.highest_random = 200
        
        # Lager spiller-objekt
        self.player = Player()
        
        # Lager plattformer
        while len(self.platform_list) < 10:
            random_y = random.randint(10, HEIGHT-20)
            self.new_platform_method(random_y)
            
        
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
                        # Sokken endrer utseende ved hopp
                        if self.player.dirty:
                            self.player.image = pg.transform.scale(pg.image.load('Bilder/dirty_sock2.png'), (PLAYER_WIDTH, PLAYER_HEIGHT*STRETCH))
                        else:
                            self.player.image = pg.transform.scale(pg.image.load('Bilder/sock2.png'), (PLAYER_WIDTH, PLAYER_HEIGHT*STRETCH))
                # Sokken får boost ved space tastetrykk
                if event.key == pg.K_SPACE:
                    self.detergent_boost()
            
    
    # Metode som oppdaterer
    def update(self):
        self.player.update()
        
        self.jump = False
        
        # Sjekker om en faller nedenfor skjermen og dør
        if self.player.pos[1] > HEIGHT:
            self.platform_list = [Platform(0, HEIGHT-START_PLATFORM_HEIGHT, WIDTH, START_PLATFORM_HEIGHT)]
            self.playing = False
        
        # Sjekker om vi faller
        if self.player.vel[1] > 0:
            collide = False

            # Sjekker om spilleren kolliderer med en plattform
            for p in self.platform_list:
                if pg.Rect.colliderect(self.player.rect, p.rect) and (self.player.rect.y+(self.player.h/1.5) < p.rect.y):

                    if self.player.dirty:
                        self.player.image = pg.transform.scale(pg.image.load('Bilder/dirty_sock1.png'), (PLAYER_WIDTH, PLAYER_HEIGHT))
                    else:       
                        self.player.image = pg.transform.scale(pg.image.load('Bilder/sock1.png'), (PLAYER_WIDTH, PLAYER_HEIGHT))

                    collide = True
                    self.jump = True
                    break
            
            # Spilleren blir stående oppå plattformen når collide er lik true
            if collide:
                self.player.pos[1] = p.rect.y - PLAYER_HEIGHT
                self.player.vel[1] = 0
        
        # Hvis musikken er ferdig begynner den på nytt
        if not pg.mixer.music.get_busy():
                self.play_background_music()
                
                
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
                be.image = pg.transform.scale(pg.image.load('Bilder/planet.png'), (be.rd*2, be.rd))
                # Bildet er hentet fra http://www.clker.com/clipart-6958.html
        else:
            self.screen.fill(PURPLE)
            ratio = 1.69
            for be in self.background_element_list:
                be.image = pg.transform.scale(pg.image.load('Bilder/ufo.png'), (be.rd*2, be.rd))
                # Bildet er hentet fra https://no.pinterest.com/pin/584482857867587248/
         
         
        # Fyller bakgrunnselementliste med bakgrunnselementer
        while len(self.background_element_list) < 6:
            self.background_element_list.append(Background_element(random.randint(-20, WIDTH - 20),
                                    random.randint(-HEIGHT, -80),
                                    ratio
                                ))
            
            
        # Tegner bakgrunnselementene
        for be in self.background_element_list:
            self.screen.blit(be.image, (be.x, be.y))
        
        
        # Tegner det som skal på skjermen
        draw_list = [self.platform_list, self.mud_list, self.hanger_list, self.clip_list, self.detergent_list, self.washing_machine_list]
        for i in range(len(draw_list)):
            for j in draw_list[i]:
                self.screen.blit(j.image, (j.rect.x, j.rect.y))
        
        
        # Tegner spilleren
        self.screen.blit(self.player.image, (self.player.pos[0], self.player.pos[1]))
        
        
        # Tegner poeng
        if self.score > 0:
            h = 30
            self.text(f"{self.score}", WIDTH//2, HEIGHT- (h), WHITE, 30)
        
        
        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()
    
    
    def music(self):
        if self.playing == False:
            mixer.music.stop()
            mixer.music.load('Lyd/game_over.mp3')

            mixer.music.play()
    
    
    # Metode for å spille bakgrunnsmusikk
    def play_background_music(self):
        # https://www.educative.io/answers/how-to-play-an-audio-file-in-pygame
        # https://archive.org/details/popcorn_202209
        mixer.init()
        mixer.music.load('Lyd/POPCORN.mp3')
        mixer.music.set_volume(0.2)

        mixer.music.play()
        
     
    # Funksjon som skriver tekst
    def text(self, text, x, y, color, fontSize):
        font = pg.font.SysFont("Arial", fontSize)
        textPicture = font.render(text, True, color)
        textRectangle = textPicture.get_rect()
        
        # Skriver i vinduet
        self.screen.blit(textPicture, (x - textRectangle.width//2, y - textRectangle.height//2))
        
        
    # Metode som viser startskjerm
    def show_start_screen(self):
        self.screen.fill(LIGHTBLUE)
        self.text("Happy Sock!", WIDTH //2 , HEIGHT // 6, WHITE, 50)
        
        self.image = pg.image.load('Bilder/sock1.png')
        self.image = pg.transform.scale(self.image, (SOCK_WIDTH, SOCK_HEIGHT))
        self.rect = self.image.get_rect()
        self.screen.blit(self.image, (WIDTH//2 - SOCK_WIDTH//2, HEIGHT//2 - SOCK_HEIGHT//2))
        
        self.text("Arrows to move and Space to boost!", WIDTH //2 , HEIGHT * 5/6, WHITE, 20)
        self.text("Press Enter to play", WIDTH //2 , HEIGHT * 11/12, WHITE, 25)
        pg.display.flip()
        self.wait_for_key()
    
    
    # Metode som viser sluttskjerm
    def show_end_screen(self):
        if self.playing == False:
            mixer.music.stop()
            mixer.music.load('Lyd/game_over.mp3')

            mixer.music.play()
        
        # Tester om spilleren ønsker å forlate vinduet og ikke vil se game over skjermen
        if not self.running:
            return
        self.screen.fill(LIGHTBLUE)
        self.text("GAME OVER!", WIDTH //2 , HEIGHT // 6, WHITE, 50)
        
        self.image = pg.image.load('Bilder/dirty_sock1.png')
        self.image = pg.transform.scale(self.image, (SOCK_WIDTH, SOCK_HEIGHT))
        self.rect = self.image.get_rect()
        self.screen.blit(self.image, (WIDTH//2 - SOCK_WIDTH//2, HEIGHT//2 - SOCK_HEIGHT//2))
        
        if (self.score == self.highscore):
            self.text(f"Ny highscore! : {self.highscore}", WIDTH //2 , HEIGHT * 25/30, WHITE, 25)
        else:
            self.text(f"Highscore: {self.highscore}", WIDTH //2 , HEIGHT * 24/30, WHITE, 25)
            
        self.text(f"Score: {self.score}", WIDTH //2 , HEIGHT * 26/30, WHITE, 25)
        self.text("Press enter to play again", WIDTH //2 , HEIGHT * 28/30, WHITE, 25)
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
                    #print("gir en boost")
                    self.player.vel[1] = -40
                    break
        
        # Sjekker kollisjon med gjørme og gir deretter minket fart
        for m in self.mud_list:
                if pg.Rect.colliderect(self.player.rect, m.rect) and self.player.vel[1] >= 0:
                    self.player.dirty = True
                    self.player.start = time.time()
                    #print("Mud")
        
        # Sjekker kollisjon med klype og spiller dør hvis kollisjon
        for c in self.clip_list:
                if pg.Rect.colliderect(self.player.rect, c.rect):
                    self.playing = False
                    break
    
    # Metode som lager plattformer og margin
    def new_platform_method(self, y):
        while len(self.platform_list) < 10:
            # Tar inn et y kordinat (enten random for startskjerm eller null for scrollende skjerm)
            # Setter en random x-verdi
            random_x = random.randint(10, WIDTH-110)
            
            # Lager en ny plattform
            self.new_platform = Platform(
                random_x,
                y,
                PLATFORM_WIDTH,
                PLATFORM_HEIGHT
            )
            
            # Lager en margin til plattformen
            self.new_platform_margin = Platform(
                random_x - PLATFORM_MARGIN,
                y - PLATFORM_MARGIN,
                PLATFORM_MARGIN_WIDTH,
                PLATFORM_MARGIN_HEIGHT
            )
            
            # Lager en random verdi mellom fra og med 1 til og med 8
            rd = random.randint(1, 8)
            
            # Hvis den randome verdien er lik 1 skal plattformen byttes ut med en lang plattform
            if rd == 1:
                self.new_platform = Platform(
                    random_x,
                    y,
                    PLATFORM_LONG_WIDTH,
                    PLATFORM_HEIGHT
                )
                self.new_platform_margin = Platform(
                    random_x - PLATFORM_MARGIN,
                    y - PLATFORM_MARGIN,
                    PLATFORM_MARGIN_LONG_WIDTH,
                    PLATFORM_MARGIN_HEIGHT
                )
            
            safe = True
                
            # Sjekker om den nye plattformen kolliderer med noen av de gamle
            for p in self.platform_list:
                if pg.Rect.colliderect(self.new_platform_margin.rect, p.rect):
                    safe = False
                    break
            
            if safe:
                # Legger i lista
                self.platform_list.append(self.new_platform)
            else:
                print("Plattformen kolliderte, prøver på nytt")
        

                
    # Metode for at spilleren får en egenskap ved å ta boost
    def detergent_boost(self):
        if len(self.detergent_list) > 0:
            self.detergent_list.pop()
            self.player.vel[1] = -40

        
    # Metode for å gi bevegelse til vaskemiddelet
    def detergent_movement(self):
        for d in range (len(self.detergent_list)):
            det = self.detergent_list[d]
            det.rect.y += det.speed
            if det.rect.y <= DETERGENT_WIDTH * (d * 2 + 1):
                det.speed *= (-1)
            elif det.rect.y >= DETERGENT_WIDTH * (d * 2 + 3) - DETERGENT_HEIGHT:
                det.speed *= (-1)  
        
    
    # Metode for at klesklypen skal bevege seg
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
                        
            # Lager sannsynligheten for at en vaskemaskin skal tegnes på skjermen
            r_wm = random.randint(1, 200)
        
            # Sjekker om en vaskemaskin skal bli laget
            if r_wm == 1 and self.platform_list[-1].taken == False:
                self.platform_list[-1].taken = True
                new_washing_machine = Washing_machine(
                    self.platform_list[-1].rect.x + (PLATFORM_WIDTH)/2 - WASHING_MACHINE_SIDE/2,
                    self.platform_list[-1].rect.y - self.platform_list[-1].rect.h -((WASHING_MACHINE_SIDE*W_RATIO)/2)-5)
                self.washing_machine_list.append(new_washing_machine)
                
            
            # Lager sannsynligheten for at en gjørme skal tegnes på skjermen
            r_mud = random.randint(1, 4)
            
            # Sjekker om en gjørme skal bli laget
            if r_mud == 1:
                if self.platform_list[-1].rect.w == PLATFORM_LONG_WIDTH:
                    r_mud = random.randint(1, 2)
                    #print(r_mud)
                    if r_mud == 2 and self.platform_list[-1].taken == False:
                        self.platform_list[-1].taken = True
                        
                        x = int(self.platform_list[-1].rect.x)
                        y = int(self.platform_list[-1].rect.x + self.platform_list[-1].rect.w - MUD_WIDTH)
                        ran = random.randint(x, y)
                        new_mud = Mud(
                            ran,
                            self.platform_list[-1].rect.y - 1)
                        self.mud_list.append(new_mud)

            # Lager sannsynligheten for at kleshenger og klype skal tegnes på skjermen
            r_clip = random.randint(1, self.highest_random)
            
            # Sjekker om kleshenger og klype skal bli laget
            if r_clip == 1 and len(self.hanger_list) < 1:
                new_hanger = Hanger(
                    0,
                    0)
                self.hanger_list.append(new_hanger)
                
                new_clip = Clip(
                    0,
                    -CLIP_HEIGHT//2)
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
                    # Øker poengscoren
                    self.score += 10
                    
                    # Øker farten til klypene
                    for i in range(len(self.clip_list)):
                        self.clip_list[i].increase_speed_clip()
                    
                    # Sikrer at lagingen av et tilfeldig tall ikke blir ugyldig
                    if self.highest_random > 1:
                        self.highest_random -= 1
                    
                    # Fjerner plattform som har gått under skjermen
                    self.platform_list.remove(p)
                    
                    # Legger til nytt vaskemiddel hvert 300 poeng, hvis resterende vaskemidler er under 3
                    self.score_boost += 10
                    if self.score_boost == 300:
                        self.score_boost = 0
                        length = len(self.detergent_list)

                        if length < 3:
                            for i in range(length):
                                self.detergent_list.pop()

                            for i in range(length+1):
                                detergent = Detergent(
                                    WIDTH - DETERGENT_WIDTH*2,
                                    DETERGENT_WIDTH*((i*2)+1))
                                self.detergent_list.append(detergent)

                    
                    y = 0
                    self.new_platform_method(y)
                        
                        
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


