from tkinter import *
import random
import time

class Game(object):
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Mr. Stick Man Races for the Exit")
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=500, height=500, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 500
        self.canvas_width = 500
        self.bg = PhotoImage(file="background.gif")
        self.bg2 = PhotoImage(file="background2.gif")
        w = self.bg.width()
        h = self.bg.height()
        for x in range(0, 5):
            for y in range(0, 5):
                if x % 2 != y % 2:
                    self.canvas.create_image(x * w, y * h, image=self.bg, anchor='nw')
                else:
                    self.canvas.create_image(x * w, y * h, image=self.bg2, anchor='nw')
        self.sprites = []
        self.running = True
        self.text = self.canvas.create_text(240, 50, text="you win",font=("Helvetica", 20), state="hidden")

    def mainloop(self):
        while 1:
            if self.running:
                for sprite in self.sprites:
                    sprite.move()
            else:
                    self.canvas.itemconfig(self.text, state="normal")
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)


class Coords(object):
    def __init__(self, xl=0, yl=0, xr=0, yr=0):
        self.xl = xl
        self.yl = yl
        self.xr = xr
        self.yr = yr

def within_x(co1, co2):
    if (co2.xl < co1.xl < co2.xr) or (co2.xl < co1.xr < co2.xr ) or (co1.xl < co2.xl < co1.xr ) or (co1.xl < co2.xr < co1.xr):
        return True
    else:
        return False

def within_y(co1, co2):
    if (co2.yl < co1.yl < co2.yr ) or (co2.yl < co1.yr < co2.yr ) or (co1.yl < co2.yl < co1.yr ) or (co1.yl < co2.yr < co1.yr):
        return True
    else:
        return False

def collided_left(co1, co2):
    if within_y(co1, co2):
        if co2.xl <= co1.xl <= co2.xr:
            return True
    return False
def collided_right(co1, co2):
    if within_y(co1, co2):
        if co2.xr <= co1.xr <= co2.xl:
            return True
    return False
def collided_top(co1, co2):
    if within_x(co1, co2):
        if co2.yl <= co1.yl <= co2.yr:
            return True
    return False
def collided_bottom(y, co1, co2):
    if within_x(co1, co2):
        y_calc = co1.yr + y
        if co2.yl <= y_calc <= co2.yr:    #check if stickman WILL collide platform rather than if it collided
            return True
    return False


class Sprite(object):
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None
    def move(self):
        pass
    def coords(self):
        return self.coordinates

class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinates = Coords(x, y, x + width, y + height)

class StickFigureSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [
                PhotoImage(file="stick-L1.gif"),
                PhotoImage(file="stick-L2.gif"),
                PhotoImage(file="stick-L3.gif")
                ]
        self.images_right = [
                PhotoImage(file="stick-R1.gif"),
                PhotoImage(file="stick-R2.gif"),
                PhotoImage(file="stick-R3.gif")
                ]
        self.image = game.canvas.create_image(200, 470, image=self.images_left[0], anchor='nw')
        self.x = -2
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>',self.jump)
        game.canvas.bind_all('<KeyPress-Up>', self.jump)
    def turn_left(self, evt):
        #if self.y == 0:
        self.x = -2
    def turn_right(self, evt):
        #if self.y == 0:
        self.x = 2
    def jump(self, evt):
        if self.y == 0:
            self.y = -4
            self.jump_count = 0
    def animate(self):
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >=2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_left[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_left[self.current_image])
        if self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_right[self.current_image])
    def coords(self):
        xy = self.game.canvas.coords(self.image)
        self.coordinates.xl = xy[0]
        self.coordinates.yl = xy[1]
        self.coordinates.xr = xy[0] + 27
        self.coordinates.yr = xy[1] + 30
        return self.coordinates
    def move(self):
        self.animate()
        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 4
        if self.y > 0:
            self.jump_count -= 1
        co = self.coords()
        left = True
        right = True
        top = True
        bottom =True
        falling = True
        if self.y > 0 and co.yr >= self.game.canvas_height:
            self.y = 0
            bottom = False
        elif self.y < 0 and co.yl <= 0:
            self.y = 0
            top = False
        #elif self.x < 0 and co.xl <= 0:
        if self.x < 0 and co.xl <= 0:
            self.x = 0
            left = False
        elif self.x > 0 and co.xr >= self.game.canvas_width:
            self.x = 0
            right = False

        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coords()
            if top and self.y < 0 and collided_top(co, sprite_co):
                self.y = -self.y
                top = False
            if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):
                self.y = sprite_co.yl - co.yr
                if self.y < 0:
                    self.y = 0
                bottom = False
                top = False
            if bottom and falling and self.y == 0  and co.yr < self.game.canvas_height  and collided_bottom(1, co, sprite_co):
                falling = False

            if left and self.x < 0 and collided_left(co, sprite_co):
                self.x = 0
                left = False
                if sprite.endgame:
                    self.end(sprite)
            if right and self.x > 0 and collided_right(co, sprite_co):
                self.x = 0
                right = False
                if sprite.endgame:
                    self.end(sprite)

        if falling and bottom and self.y == 0 and co.yr < self.game.canvas_height:
            self.y = 4
        self.game.canvas.move(self.image, self.x, self.y)
    def end(self, sprite):
        self.game.running = False
        sprite.opendoor()
        time.sleep(1)
        self.game.canvas.itemconfig(self.image, state='hidden')
        sprite.closedoor()


class DoorSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.closed_door = PhotoImage(file="door1.gif")
        self.open_door = PhotoImage(file="door2.gif")
        self.coordinates = Coords(x, y, x + width/2, y + height)
        self.endgame = True
    def opendoor(self):
        self.game.canvas.itemconfig(self.image, image=self.open_door)
        self.game.tk.update_idletasks()

    def closedoor(self):
        self.game.canvas.itemconfig(self.image, image=self.closed_door)
        self.game.tk.update_idletasks()





class MovingPlatformSprite(PlatformSprite):
    def __init__(self, game, photo_image, x, y, width, height):
        PlatformSprite.__init__(self, game, photo_image, x, y, width, height)
        self.x = 1
        self.counter = 0
        self.last_time = time.time()
        self.width = width
        self.height = height
    
    def coords(self):
        xy = list(self.game.canvas.coords(self.image))
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + self.width
        self.coordinates.y2 = xy[1] + self.height
        return self.coordinates
    
    def move(self):
        if time.time() - self.last_time > 0.1:
            self.last_time = time.time()        
            self.game.canvas.move(self.image, self.x, 0)
            self.counter += 1
            if self.counter > 20:
                self.x *= -1
                self.counter = 0

g = Game()
platform1 = PlatformSprite(g, PhotoImage(file="platform3.gif"), \
        0, 480, 100, 10)
platform2 = MovingPlatformSprite(g, PhotoImage(file="platform3.gif"), \
        150, 440, 100, 10)
platform3 = PlatformSprite(g, PhotoImage(file="platform3.gif"), \
        300, 400, 100, 10)
platform4 = PlatformSprite(g, PhotoImage(file="platform3.gif"), \
        300, 160, 100, 10)
platform5 = PlatformSprite(g, PhotoImage(file="platform2.gif"), \
        175, 350, 66, 10)
platform6 = MovingPlatformSprite(g, PhotoImage(file="platform2.gif"), \
        50, 300, 66, 10)
platform7 = PlatformSprite(g, PhotoImage(file="platform2.gif"), \
        170, 120, 66, 10)
platform8 = PlatformSprite(g, PhotoImage(file="platform2.gif"), \
        45, 60, 66, 10)
platform9 = MovingPlatformSprite(g, PhotoImage(file="platform1.gif"), \
        170, 250, 32, 10)
platform10 = PlatformSprite(g, PhotoImage(file="platform1.gif"), \
        230, 200, 32, 10)

g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)
g.sprites.append(platform9)
g.sprites.append(platform10)

door = DoorSprite(g, PhotoImage(file="door1.gif"), 45, 30, 40, 35)
g.sprites.append(door)

sf = StickFigureSprite(g)
g.sprites.append(sf)
g.mainloop()
