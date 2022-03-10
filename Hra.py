import time

import pygame
import sys
from menu import *
from player import *
from camera import *
from os import path
from tilemapa import *

def draw_player_health(surf, x, y, p):
    if p < 0:
        p = 0
    BAR_DELKA = 100
    BAR_VYSKA = 20
    fill = p * BAR_DELKA
    outline_rect = pygame.Rect(x, y, BAR_DELKA, BAR_VYSKA)
    fill_rect = pygame.Rect(x, y, fill, BAR_VYSKA)
    if p > 0.6:
        col = GREEN
    elif p > 0.3:
        col = YELLOW
    else:
        col = RED
    pygame.draw.rect(surf, col, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)
class Game:
    def __init__(self):
        pygame.init()
        self.run = True
        self.play = 0
        self.clock = pygame.time.Clock()
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        self.okno = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        # self.screen = pygame.Surface(((self.screen_sirka,self.screen_vyska)))
        self.screen = pygame.display.get_surface()
        self.up, self.down, self.enter, self.back, self.escape = False, False, False, False, False
        pygame.display.set_caption("RPG game")
        self.walk_up = pygame.image.load("player_back.png")
        #self.background = pygame.image.load("jo.jfif")
        self.cursory = pygame.image.load("cursory.png")
        #self.start_game = pygame.image.load("start_game.png")
        self.nazevfontu = pygame.font.get_default_font()
        self.main_menu = HlavniMenu(self)
        self.options = OptionsMenu(self)
        self.ingame_menu = ingame_stop_menu(self)
        self.quits = QuitsMenu(self)
        self.resolution = ResolutionMenu(self)
        self.tohle_menu = self.main_menu
        self.ingame_quit = Ingame_QuitsMenu(self)
        self.game_menu1 = Game_menu1(self)
        # self.player_menu = Player_menu(self)
        self.fullscreen = False
        self.BLOCK_LAYER = 1
        self.GRIDWIDTH = WIDTH / MAP_SIZE
        self.GRIDHEIGHT = HEIGHT / MAP_SIZE
        self.lightgrey = (((80, 80, 80)))
        pygame.key.set_repeat(500, 100)
        self.score = 0
        self.zivot = 0
        self.data()

    def data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        map_folder = path.join(game_folder, 'maps')
        self.map = Tilemap(path.join(map_folder, 'map.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.score_img = pygame.image.load(path.join(img_folder, "score.png")).convert_alpha()
        self.player_img = pygame.image.load(path.join(img_folder, "player.png")).convert_alpha()
        self.mob_img = pygame.image.load(path.join(img_folder, "zombie.png")).convert_alpha()
        self.player_left = [pygame.image.load(path.join(img_folder, "player_left1.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_left2.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_left3.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_left4.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_left5.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_left6.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_left7.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_left8.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_left9.png")).convert_alpha()]
        self.player_right = [pygame.image.load(path.join(img_folder, "player_right1.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_right2.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_right3.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_right4.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_right5.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_right6.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_right7.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_right8.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_right9.png")).convert_alpha()]
        self.player_down = [pygame.image.load(path.join(img_folder, "player_down0.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_down1.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_down2.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_down3.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_down4.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_down5.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_down6.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_down7.png")).convert_alpha(),pygame.image.load(path.join(img_folder, "player_down8.png")).convert_alpha()]
        self.player_up = [pygame.image.load(path.join(img_folder, "player_back0.png")).convert_alpha(), pygame.image.load(path.join(img_folder, "player_back1.png")).convert_alpha(), pygame.image.load(path.join(img_folder, "player_back2.png")).convert_alpha(), pygame.image.load(path.join(img_folder, "player_back3.png")).convert_alpha(), pygame.image.load(path.join(img_folder, "player_back4.png")).convert_alpha(), pygame.image.load(path.join(img_folder, "player_back5.png")).convert_alpha(), pygame.image.load(path.join(img_folder, "player_back6.png")).convert_alpha(), pygame.image.load(path.join(img_folder, "player_back7.png")).convert_alpha(), pygame.image.load(path.join(img_folder, "player_back8.png")).convert_alpha()]
    """def draw_grid(self):
        for x in range(0, WIDTH, MAP_SIZE):
            pygame.draw.line(self.okno, self.lightgrey, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, MAP_SIZE):
            pygame.draw.line(self.okno, self.lightgrey, (0, y), (WIDTH, y))"""

    def draw(self):
        #self.draw_grid()
        #self.all_sprites.custom_draw(self.player)
        self.okno.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.okno.blit(sprite.image, self.camera.apply(sprite))
        draw_player_health(self.okno, 10, 10, self.player.zivoty / ZIVOT)
        self.vyber_textu(str(self.zivot), 20, 130, 20)
        self.vyber_textu('Score:' + str(self.score), 20, 50, 100)
        pygame.display.flip()
        

    """def povidani(self):
        #self.vyber_textu(SPRAVA, 20, WIDTH / 2, HEIGHT / 2 + 300)
        for char in SPRAVA:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.1)"""
    def jo(self):
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.score_sprites = pygame.sprite.Group()
        """for row, xx in enumerate(self.map.data):
            for col, yy in enumerate(xx):
                if yy == "P":
                    self.player = Player(self, row,col)
                if yy == "1":
                    Block(self, row,col)
                if yy == "M":
                    Enemy(self, row, col)"""
        for hitbox in self.map.tmxdata.objects:
            if hitbox.name == 'Player':
                self.player = Player(self, hitbox.x, hitbox.y)
            if hitbox.name == 'Enemy':
                Enemy(self, hitbox.x, hitbox.y)
            if hitbox.name == 'Wall':
                Hit_Box(self, hitbox.x, hitbox.y, hitbox.width, hitbox.height)
            if hitbox.name == "Score":
                self.body = Score(self, hitbox.x, hitbox.y)
        self.camera = Camera(self.map.width, self.map.height)
        self.pause = False

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)
    # hlavni loop
    def loop(self):
        while self.play == 1:
            self.events()
            if self.enter:
                self.play == 0
            self.dt = self.clock.tick(FPS) / 1000.0
            self.draw()
            #self.povidani()
            if not self.pause:

                self.update()
            self.klavesy()
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.play = False
                self.run = False
            if event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    self.okno = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.pause = not self.pause
                if event.key == pygame.K_f:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.okno = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                    else:
                        self.okno = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)
    def eventy(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run, self.play = False, False
                self.tohle_menu.runscreen = False
            if event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    self.okno = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.enter = True
                if event.key == pygame.K_BACKSPACE:
                    self.back = True
                if event.key == pygame.K_DOWN:
                    self.down = True
                if event.key == pygame.K_UP:
                    self.up = True
                if event.key == pygame.K_ESCAPE:
                    self.escape = True
                if event.key == pygame.K_f:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.okno = pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                    else:
                        self.okno = pygame.display.set_mode((WIDTH, HEIGHT),pygame.RESIZABLE)

    def klavesy(self):
        self.up, self.down, self.enter, self.back = False, False, False, False

    def vyber_textu(self, text, velikost, x, y):
        font = pygame.font.Font(self.nazevfontu, velikost)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.okno.blit(text_surface, text_rect)
class Mapa(pygame.sprite.Group):
    def __int__(self):
        super().__init__()

    def custom_draw(self, Player):
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()
        self.offset.x = Player.rect.centerx - self.half_width
        self.offset.y = Player.rect.centery - self.half_height

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

