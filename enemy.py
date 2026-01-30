import pygame as pg

class Enemy:
    def __init__(self, r, c, speed=2):
        self.r, self.c = r, c
        self.x = c * 80 + 10 
        self.y = r * 80 + 10
        self.speed = speed
        self.img = pg.transform.scale(pg.image.load("assets/enemy.png"), (60, 60))
        self.rect = pg.Rect(self.x, self.y, 60, 60)
        self.reached_goal = False

    def move(self, map_data):
        curr_c = int((self.x + 30) // 80)
        curr_r = int((self.y + 30) // 80)

        if map_data[curr_r][curr_c] == 3:
            self.reached_goal = True
            return

        if curr_c + 1 < 9 and map_data[curr_r][curr_c + 1] in [1, 3]:
            self.x += self.speed
        elif curr_r + 1 < 6 and map_data[curr_r + 1][curr_c] in [1, 3]:
            self.y += self.speed
            
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))