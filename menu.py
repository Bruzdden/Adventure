import sys
from camera import *
import pygame

class Menu():
    def __init__(self, Hra):
        self.Hra = Hra
        self.prostredni_sirka, self.prostredni_vyska = WIDTH/2, HEIGHT/2
        self.runscreen = True
        self.cursor_rect = pygame.Rect(0,0,60,20)
        self.offset = -100
    def vyber_cursor(self):
        self.Hra.vyber_textu("*", 40, self.cursor_rect.x, self.cursor_rect.y)
    def pozadi(self):
        self.Hra.okno.blit(self.Hra.okno, (0, 0))
        pygame.display.update()
        self.Hra.klavesy()

class HlavniMenu(Menu):
    def __init__(self, Hra):
        Menu.__init__(self,Hra)
        self.state = "Start"
        self.startx, self.starty  = self.prostredni_sirka, self.prostredni_vyska
        self.optionsx, self.optionsy = self.prostredni_sirka, self.prostredni_vyska +50
        self.quitx, self.quity = self.prostredni_sirka, self.prostredni_vyska +200
        self.cursor_rect.midtop= (self.startx+self.offset, self.starty)
    def ukazat_menu(self):
        self.runscreen=True
        while self.runscreen:
            self.Hra.eventy()
            self.check_input()
            self.Hra.okno.fill((0,0,0))
            self.text()
            self.vyber_cursor()
            self.pozadi()
    def text(self):
        self.Hra.vyber_textu("Main Menu", 70, WIDTH / 2, HEIGHT / 2 - 170)
        self.Hra.vyber_textu("Credits: made by HALO", 15, WIDTH / 2 - 290, HEIGHT / 2 + 270)
        self.Hra.vyber_textu("Start game", 40, self.startx, self.starty)
        self.Hra.vyber_textu("Options", 40, self.optionsx, self.optionsy)
        self.Hra.vyber_textu("Quit", 40, self.quitx, self.quity)
    def pohyb_cursor(self):
        if self.Hra.down:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = "Quit"
            elif self.state == "Quit":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
        elif self.Hra.up:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.quitx + self.offset, self.quity)
                self.state = "Quit"
            elif self.state == "Quit":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start"
    def check_input(self):
        self.pohyb_cursor()
        if self.Hra.enter:
            if self.state == "Start":
                #self.Hra.play = 1
                self.Hra.tohle_menu = self.Hra.game_menu1
            elif self.state == "Options":
                self.Hra.tohle_menu = self.Hra.options
            elif self.state == "Quit":
                self.Hra.tohle_menu = self.Hra.quits
            self.runscreen = False
        if self.Hra.escape:
            self.Hra.tohle_menu = self.Hra.quits
            self.runscreen = False
class OptionsMenu(Menu):
    def __init__(self, Hra):
        Menu.__init__(self,Hra)
        self.state = "Volume"
        self.volumex, self.volumey = self.prostredni_sirka, self.prostredni_vyska + 20
        self.controlsx, self.controlsy = self.prostredni_sirka, self.prostredni_vyska + 40
        self.resolutionx, self.resolutiony = self.prostredni_sirka, self.prostredni_vyska + 60
        self.cursor_rect.midtop = (self.volumex + self.offset, self.volumey)
    def ukazat_menu(self):
        self.runscreen=True
        while self.runscreen:
            self.Hra.eventy()
            self.check_input()
            self.Hra.okno.fill((0, 0, 0))
            self.text()
            self.vyber_cursor()
            self.pozadi()
    def text(self):
        self.Hra.vyber_textu("Options", 20, WIDTH / 2, HEIGHT / 2 - 30)
        self.Hra.vyber_textu("Volume", 20, self.volumex, self.volumey)
        self.Hra.vyber_textu("Controls", 20, self.controlsx, self.controlsy)
        self.Hra.vyber_textu("Resolution", 20, self.resolutionx, self.resolutiony)
    def pohyb_cursor(self):
        if self.Hra.back:
            self.Hra.tohle_menu = self.Hra.main_menu
            self.runscreen = False
        if self.Hra.down:
            if self.state == "Volume":
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                self.state = "Controls"
            elif self.state == "Controls":
                self.cursor_rect.midtop = (self.resolutionx + self.offset, self.resolutiony)
                self.state = "Resolution"
            elif self.state == "Resolution":
                self.cursor_rect.midtop = (self.volumex + self.offset, self.volumey)
                self.state = "Volume"
        elif self.Hra.up:
            if self.state == "Volume":
                self.cursor_rect.midtop = (self.resolutionx + self.offset, self.resolutiony)
                self.state = "Resolution"
            elif self.state == "Resolution":
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
                self.state = "Controls"
            elif self.state == "Controls":
                self.cursor_rect.midtop = (self.volumex + self.offset, self.volumey)
                self.state = "Volume"

    def check_input(self):
        self.pohyb_cursor()
        if self.Hra.enter:
            if self.state == "Volume":
                pass
            elif self.state == "Controls":
                pass
            elif self.state == "Resolution":
                self.Hra.tohle_menu = self.Hra.resolution
            self.runscreen = False
        elif self.Hra.escape:
            pygame.quit()
            sys.exit()

class ResolutionMenu(Menu):
    def __init__(self, Hra):
        Menu.__init__(self, Hra)
        self.state = "1024x768y"
        self.firstbuttonx, self.firstbuttony = self.prostredni_sirka, self.prostredni_vyska + 20
        self.secondbuttonx, self.secondbuttony = self.prostredni_sirka, self.prostredni_vyska + 40
        self.thirdbuttonx, self.thirdbuttony = self.prostredni_sirka, self.prostredni_vyska + 60
        self.cursor_rect.midtop = (self.firstbuttonx + self.offset, self.firstbuttony)
    def ukazat_menu(self):
        self.runscreen = True
        while self.runscreen:
            self.exit()
            self.Hra.eventy()
            self.check_input()
            self.Hra.okno.fill((0, 0, 0))
            self.text()
            self.vyber_cursor()
            self.pozadi()

    def text(self):
        self.Hra.vyber_textu("Resolution", 20, WIDTH / 2, HEIGHT / 2 - 40)
        self.Hra.vyber_textu("1024x768y", 20, self.firstbuttonx, self.firstbuttony)
        self.Hra.vyber_textu("800x600y", 20, self.secondbuttonx, self.secondbuttony)
        self.Hra.vyber_textu("Resolution", 20, self.thirdbuttonx, self.thirdbuttony)

    def pohyb_cursor(self):
        if self.Hra.back:
            self.Hra.tohle_menu = self.Hra.options
            self.runscreen = False
        if self.Hra.down:
            if self.state == "1024x768y":
                self.cursor_rect.midtop = (self.secondbuttonx + self.offset, self.secondbuttony)
                self.state = "800x600y"
            elif self.state == "800x600y":
                self.cursor_rect.midtop = (self.thirdbuttonx + self.offset, self.thirdbuttony)
                self.state = "Resolution"
            elif self.state == "Resolution":
                self.cursor_rect.midtop = (self.firstbuttonx + self.offset, self.firstbuttony)
                self.state = "1024x768y"
        elif self.Hra.up:
            if self.state == "1024x768y":
                self.cursor_rect.midtop = (self.thirdbuttonx + self.offset, self.thirdbuttony)
                self.state = "Resolution"
            elif self.state == "Resolution":
                self.cursor_rect.midtop = (self.secondbuttonx + self.offset, self.secondbuttony)
                self.state = "800x600y"
            elif self.state == "800x600y":
                self.cursor_rect.midtop = (self.firstbuttonx + self.offset, self.firstbuttony)
                self.state = "1024x768y"
    def check_input(self):
        self.pohyb_cursor()
        if self.Hra.enter:
            if self.state == "1024x768y":
                pass
            elif self.state == "800x600y":
                pass
            elif self.state == "Resolution":
                pass
            self.runscreen = False
        elif self.Hra.escape:
            pygame.quit()
            sys.exit()
class QuitsMenu(Menu):
    def __init__(self, Hra):
        Menu.__init__(self,Hra)
        self.state = "YES"
        self.yes_buttonx, self.yes_buttony = self.prostredni_sirka, self.prostredni_vyska + 20
        self.no_buttonx, self.no_buttony = self.prostredni_sirka, self.prostredni_vyska + 200
        self.cursor_rect.midtop = (self.yes_buttonx + self.offset, self.yes_buttony)
    def ukazat_menu(self):
        self.runscreen = True
        while self.runscreen:
            self.Hra.eventy()
            self.check_input()
            self.Hra.okno.fill((0,0,0))
            self.text()
            self.vyber_cursor()
            self.pozadi()
    def text(self):
        self.Hra.vyber_textu("Are u sure, that u want to quit?", 20, WIDTH / 2, HEIGHT / 2 - 40)
        self.Hra.vyber_textu("YES", 80, self.yes_buttonx, self.yes_buttony)
        self.Hra.vyber_textu("NO", 80, self.no_buttonx, self.no_buttony)
    def check_input(self):
        if self.Hra.back:
            self.Hra.tohle_menu = self.Hra.main_menu
            self.runscreen = False
        if self.Hra.up or self.Hra.down:
            if self.state == "YES":
                self.cursor_rect.midtop = (self.no_buttonx + self.offset, self.no_buttony)
                self.state = "NO"
            elif self.state == "NO":
                self.cursor_rect.midtop = (self.yes_buttonx + self.offset, self.yes_buttony)
                self.state = "YES"
        if self.Hra.enter:
            if self.state == "YES":
                pygame.quit()
                sys.exit()
            elif self.state == "NO":
                self.Hra.tohle_menu = self.Hra.main_menu
                self.runscreen = False
        elif self.Hra.escape:
            self.runscreen = False
            pygame.quit()
            sys.exit()

class Game_menu1(Menu):
    def __init__(self, Hra):
        Menu.__init__(self, Hra)
        self.state = "Easy"
        self.Easyx, self.Easyy = self.prostredni_sirka , self.prostredni_vyska + 20
        self.Normalx, self.Normaly = self.prostredni_sirka , self.prostredni_vyska + 70
        self.Hardx, self.Hardy = self.prostredni_sirka, self.prostredni_vyska + 120
        self.cursor_rect.midtop = (self.Easyx + self.offset, self.Easyy)
    def ukazat_menu(self):
        self.runscreen=True
        while self.runscreen:
            self.Hra.eventy()
            self.check_input()
            self.Hra.okno.fill((0,0,0))
            self.text()
            self.vyber_cursor()
            self.pozadi()
    def text(self):
        self.Hra.vyber_textu("Vyber difficulty hry", 70, WIDTH / 2, HEIGHT / 2 - 170)
        self.Hra.vyber_textu("Easy", 40, self.Easyx, self.Easyy)
        self.Hra.vyber_textu(" Normal", 40, self.Normalx, self.Normaly)
        self.Hra.vyber_textu("Hard", 40, self.Hardx, self.Hardy)
    def pohyb_cursor(self):
        if self.Hra.down:
            if self.state == "Easy":
                self.cursor_rect.midtop = (self.Normalx + self.offset, self.Normaly)
                self.state = "Normal"
            elif self.state == "Normal":
                self.cursor_rect.midtop = (self.Hardx + self.offset, self.Hardy)
                self.state = "Hard"
            elif self.state == "Hard":
                self.cursor_rect.midtop = (self.Easyx + self.offset, self.Easyy)
                self.state = "Easy"
        elif self.Hra.up:
            if self.state == "Start":
                self.cursor_rect.midtop = (self.Hardx + self.offset, self.Hardy)
                self.state = "Hard"
            elif self.state == "Hard":
                self.cursor_rect.midtop = (self.Normalx + self.offset, self.Normaly)
                self.state = "Normal"
            elif self.state == "Normal":
                self.cursor_rect.midtop = (self.Easyx + self.offset, self.Easyy)
                self.state = "Easy"
    def check_input(self):
        self.pohyb_cursor()
        if self.Hra.enter:
            if self.state == "Easy":
                self.Hra.play = 1
                self.Hra.zivot += 100
            elif self.state == "Normal":
                pass
            elif self.state == "Hard":
                pass
            self.runscreen = False
        elif self.Hra.escape:
            pygame.quit()
            sys.exit()
        if self.Hra.back:
            self.Hra.tohle_menu = self.Hra.main_menu
            self.runscreen = False

class ingame_stop_menu(Menu):
    def __init__(self, Hra):
        Menu.__init__(self, Hra)
        self.state = "Main menu"
        self.main_menu_buttonx, self.main_menu_buttony = self.prostredni_sirka, self.prostredni_vyska + 20
        self.quit_buttonx, self.quit_buttony = self.prostredni_sirka, self.prostredni_vyska + 200
        self.cursor_rect.midtop = (self.main_menu_buttonx + self.offset, self.main_menu_buttony)
    def ukazat_menu(self):
        self.runscreen=True
        while self.runscreen:
            self.exit()
            self.Hra.eventy()
            self.check_input()
            self.Hra.okno.fill((0,0,0))
            self.Hra.vyber_textu("Pause", 20, WIDTH / 2, HEIGHT / 2 - 40)
            self.Hra.vyber_textu("Main Menu", 40, self.main_menu_buttonx, self.main_menu_buttony)
            self.Hra.vyber_textu("Quit", 40, self.quit_buttonx, self.quit_buttony)
            self.vyber_cursor()
            self.pozadi()

    def check_input(self):
         if self.Hra.back:
            self.Hra.tohle_menu = self.Hra.main_menu
            self.runscreen = False
         elif self.Hra.up or self.Hra.down:
            if self.state == "Main menu":
                self.cursor_rect.midtop = (self.quit_buttonx + self.offset, self.quit_buttony)
                self.state = "Quit"
            elif self.state == "Quit":
                self.cursor_rect.midtop = (self.main_menu_buttonx + self.offset, self.main_menu_buttony)
                self.state = "Main menu"
         elif self.Hra.enter:
            if self.state == "Quit":
                self.Hra.tohle_menu = self.Hra.ingame_quit
                self.runscreen = False
            elif self.state == "Main menu":
                self.Hra.tohle_menu = self.Hra.main_menu
                self.runscreen = False
class Ingame_QuitsMenu(Menu):
    def __init__(self, Hra):
        Menu.__init__(self,Hra)
        self.state = "YES"
        self.yes_buttonx, self.yes_buttony = self.prostredni_sirka, self.prostredni_vyska + 20
        self.no_buttonx, self.no_buttony = self.prostredni_sirka, self.prostredni_vyska + 200
        self.cursor_rect.midtop = (self.yes_buttonx + self.offset, self.yes_buttony)
    def ukazat_menu(self):
        self.runscreen = True
        while self.runscreen:
            self.Hra.eventy()
            self.check_input()
            self.Hra.okno.fill((0,0,0))
            self.Hra.vyber_textu("Are u sure, that u want to quit?", 20, WIDTH / 2, HEIGHT / 2 - 40)
            self.Hra.vyber_textu("YES", 80, self.yes_buttonx, self.yes_buttony)
            self.Hra.vyber_textu("NO", 80, self.no_buttonx, self.no_buttony)
            self.vyber_cursor()
            self.pozadi()
    def check_input(self):
        if self.Hra.back:
            self.Hra.tohle_menu = self.Hra.ingame_menu
            self.runscreen = False
        elif self.Hra.up or self.Hra.down:
            if self.state == "YES":
                self.cursor_rect.midtop = (self.no_buttonx + self.offset, self.no_buttony)
                self.state = "NO"
            elif self.state == "NO":
                self.cursor_rect.midtop = (self.yes_buttonx + self.offset, self.yes_buttony)
                self.state = "YES"
        elif self.Hra.enter:
            if self.state == "YES":
                pygame.quit()
                sys.exit()
            elif self.state == "NO":
                self.Hra.tohle_menu = self.Hra.main_menu
                self.runscreen = False

