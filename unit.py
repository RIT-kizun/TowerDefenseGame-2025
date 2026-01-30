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
        self.block = 2
        config.COST -= 8
        self.img_blocker = pg.image.load("assets/blocker.png")
        

    def blit():
        pass
    
    def draw(self,screen):
        screen.blit(self.img_blocker,(self.x,self.y))
        

class Shooter(Unit):
    def __init__(self,r,c):
        super().__init__(r,c)
        self.hp = 3
        self.block = 0
        config.COST -= 10
        self.img_shooter = pg.image.load("assets/shooter.png")
        
    def blit(self):
        pass
    
    def draw(self,screen):
        screen.blit(self.img_shooter,(self.x,self.y))
        

