import pygame as pg
import config

class Unit:
    def __init__(self, r, c):
        image_size = 75
        self.r, self.c = r, c
        self.color = (0, 0, 255) # 青
        offset = (80 - image_size) // 2#余白
        self.x = c * 80 + offset
        self.y = r * 80 + offset

class Blocker(Unit):
    def __init__(self,r,c):
        super().__init__(r, c)
        self.hp = 15
        self.max_block = 3
        self.curr_block = 0
        self.is_blocker = True
        config.COST -= 8
        self.img_blocker = pg.image.load("assets/blocker.png")
        self.angle = 0 # 0,90,180,270
        

    def blit():
        pass
    
    def rotate(self):
        self.angle = (self.angle + 90) % 360
        self.img_blocker = pg.transform.rotate(self.img_blocker,self.angle)
    
    def draw(self,screen):
        screen.blit(self.img_blocker,(self.x,self.y))
        

class Shooter(Unit):
    def __init__(self,r,c):
        super().__init__(r,c)
        self.hp = 3
        self.block = 0
        config.COST -= 10
        self.img_shooter = pg.image.load("assets/shooter.png")
        self.angle = 0 # 0,90,180,270
        
    def blit(self):
        pass

    def rotate(self):
        self.angle = (self.angle + 90) % 360
        self.img_shooter = pg.transform.rotate(self.img_shooter,self.angle)
    
    def draw(self,screen):
        screen.blit(self.img_shooter,(self.x,self.y))
        

