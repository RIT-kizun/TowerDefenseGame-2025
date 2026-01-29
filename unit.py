import pygame as pg

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
        self.img_blocker = pg.image.load("assets/blocker.png")
        

    def blit():
        pass
    
    def draw(self,screen):
        screen.blit(self.img_blocker,(self.x,self.y))
        

class Shooter(Unit):
    def __init__(self,image_file):
        super().__init__()
        self.hp = 3
        
    def blit(self):
        pass
        
class Set(Unit):
    def __init__(self, r, c):
        super().__init__(r, c)
    def blit():
        pass      

    # def draw(self, screen):
    #     m, s = 20, 80
    #     cx, cy = self.x + s//2, self.y + s//2
    #     # 向きに合わせた三角形の頂点
    #     if self.direction == "RIGHT":
    #         pts = [(self.x+m, self.y+m), (self.x+m, self.y+s-m), (self.x+s-m, cy)]
    #     elif self.direction == "LEFT":
    #         pts = [(self.x+s-m, self.y+m), (self.x+s-m, self.y+s-m), (self.x+m, cy)]
    #     elif self.direction == "UP":
    #         pts = [(self.x+m, self.y+s-m), (self.x+s-m, self.y+s-m), (cx, self.y+m)]
    #     else: # DOWN
    #         pts = [(self.x+m, self.y+m), (self.x+s-m, self.y+m), (cx, self.y+s-m)]
    #     pg.draw.polygon(screen, self.color, pts)