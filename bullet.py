import pygame as pg

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x + 36
        self.y = y + 36
        self.angle = angle
        self.speed = 10
        self.distance = 0
        self.max_distance = 160 # 2マス分
        self.is_active = True

        self.img = pg.image.load("assets/arrow.png")
        self.img = pg.transform.rotate(self.img, angle)

    def move(self):
        # 向きに合わせて移動
        if self.angle == 0:    self.x += self.speed   # 右
        elif self.angle == 90: self.y -= self.speed   # 上
        elif self.angle == 180: self.x -= self.speed  # 左
        elif self.angle == 270: self.y += self.speed  # 下
        
        self.distance += self.speed
        if self.distance >= self.max_distance:
            self.is_active = False

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))