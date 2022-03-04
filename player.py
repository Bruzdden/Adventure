from re import M
import sys
import pygame
from Hra import *
from menu import *
from camera import *
from os import path
from tilemapa import *
from camera import *
import math
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, Hra, x,y):
        self.groups = Hra.all_sprites
        self.Hra = Hra
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.player_front = self.Hra.player_img #pygame.image.load("player.png")
        self.image = self.player_front
        #self.rect = self.image.get_rect(topleft= pozice)
        self.rect = self.image.get_rect()
        #self.x = x * MAP_SIZE
        #self.y = y * MAP_SIZE
        #self.rect.x = self.x
        #self.rect.y = self.y
        self.rychlost = 200
        self.walkcount = 1
        self.playerx = 0
        self.playery = 0
        self.vel = vec(0, 0)
        self.pos = vec(x,y)
        self.left, self.right, self.play_up, self.play_down = False, False, False, False
        self.zivoty = ZIVOT
    def update(self):
        self.pohyb()
        self.pos += self.vel * self.Hra.dt
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
    def pohyb(self):
        self.vel = vec(0, 0)
        self.key = pygame.key.get_pressed()
        if self.key[pygame.K_LEFT]: # and self.playerx > self.rychlost:
            #for sprite in self.Hra.all_sprites:
                #sprite.rect.x += self.rychlost
            self.vel.x = -self.rychlost
            self.left = True
            self.right = False
            self.play_down = False
            self.play_up = False
        elif self.key[pygame.K_RIGHT]: # and self.playerx < 800 - 50 - self.rychlost:
            #for sprite in self.Hra.all_sprites:
                #sprite.rect.x -= self.rychlost
            self.vel.x = self.rychlost
            self.right = True
            self.left = False
            self.play_down = False
            self.play_up = False
        else:
            self.left = False
            self.right = False
            self.play_down = False
            self.play_up = False
        if self.key[pygame.K_DOWN]: # and self.playery < 600 - 80 - self.rychlost:
            self.vel.y = self.rychlost
            self.play_down = True
            self.play_up = False
            self.left = False
            self.right = False
        if self.key[pygame.K_UP]: # and self.playery > self.rychlost:
            self.vel.y = -self.rychlost
            self.play_up = True
            self.play_down = False
            self.left = False
            self.right = False
        self.player_animation()
        pygame.display.set_caption("Adventure game")

    def player_animation(self):
        #global walkcount
        #if self.walkcount + 1 >= 27:
            #self.walkcount = 0
        if self.left:
            if self.vel.x == 0:
                self.image = self.player_front
            else:
                self.image = self.Hra.player_left[math.floor(self.walkcount)]
                #self.Hra.okno.blit(self.player_left[self.walkcount//3],(self.rect.x,self.rect.y))
                self.walkcount += 1
                if self.walkcount >= 9:
                    self.walkcount = 1
        elif self.right:
            if self.vel.x == 0:
                self.image = self.player_front
            else:
                self.image = self.Hra.player_right[math.floor(self.walkcount)]
                #self.Hra.okno.blit(self.player_right[self.walkcount//3],(self.rect.x,self.rect.y))
                self.walkcount += 1
                if self.walkcount >= 9:
                    self.walkcount = 1
        elif self.play_up:
            if self.vel.y == 0:
                self.image = self.player_front
            else:
                self.image = self.Hra.player_up[math.floor(self.walkcount)]
                #self.Hra.okno.blit(self.player_right[self.walkcount//3],(self.rect.x,self.rect.y))
                self.walkcount += 1
                if self.walkcount >= 9:
                    self.walkcount = 1
        elif self.play_down:
            if self.vel.y == 0:
                self.image = self.player_front
            else:
                self.image = self.Hra.player_down[math.floor(self.walkcount)]
                #self.Hra.okno.blit(self.player_right[self.walkcount//3],(self.rect.x,self.rect.y))
                self.walkcount += 1
                if self.walkcount >= 9:
                    self.walkcount = 1
        else:
            self.image = self.player_front
        pygame.display.update()
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.Hra.walls_sprites, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.Hra.walls_sprites, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
class Enemy(pygame.sprite.Sprite):
    def __init__(self, Hra, x, y):
        self.groups = Hra.all_sprites, Hra.enemy_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.Hra = Hra
        self.image = Hra.mob_img
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * MAP_SIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rot = 0

    def update(self):
        self.rot = (self.Hra.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pygame.transform.rotate(self.Hra.mob_img, self.rot)
        self.acc = vec(ENEMY_RYCHLOST, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.Hra.dt
        self.pos += self.vel * self.Hra.dt + 0.5 * self.acc * self.Hra.dt ** 2
        self.rect.x = self.pos.x
        self.collide_with_walls('x')
        self.rect.y = self.pos.y
        self.collide_with_walls('y')
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pygame.sprite.spritecollide(self, self.Hra.walls_sprites, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right# + self.rect.width / 2
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pygame.sprite.spritecollide(self, self.Hra.walls_sprites, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom# + self.rect.height / 2
                self.vel.y = 0
                self.rect.y = self.pos.y
class Block(pygame.sprite.Sprite):
    def __init__(self, Hra, x, y):
        self.groups = Hra.all_sprites, Hra.walls_sprites
        super().__init__(self.groups)
        self.Hra = Hra
        self.x = x * MAP_SIZE
        self.y = y * MAP_SIZE
        self.image = pygame.Surface([MAP_SIZE, MAP_SIZE])
        self.image.fill(((0,0,255)))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
class Hit_Box(pygame.sprite.Sprite):
    def __init__(self, Hra, x, y, w, h):
        self.groups = Hra.walls_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = Hra
        self.rect = pygame.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y