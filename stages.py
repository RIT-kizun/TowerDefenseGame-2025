import pygame as pg
import enemy as e
import unit as u
import time
import datetime


TILE_SIZE = 80
COST = 0
WALL   = 0  # 壁（配置不可）
ROAD   = 1  # 道（味方1: Blocker用）
HIGH   = 2  # 高台（味方2: Shooter用）
GOAL   = 3  # 味方拠点（青）
START  = 4  # 敵拠点（赤）



class Stage:
    def __init__(self):
        self.MAP_DATA = [
            [0,0,0,0,0,0,0,0,0],
            [4,1,1,2,2,2,2,2,0],
            [0,2,1,2,1,1,1,2,0],
            [0,2,1,1,1,2,1,2,0],
            [0,2,2,2,2,2,1,1,3],
            [0,0,0,0,0,0,0,0,0],
        ]
        
        self.colors = {
                WALL: (0, 0, 0),       # 黒
                ROAD: (100, 100, 100), # 灰色
                HIGH: (255, 255, 255), # 白
                START: (255, 0, 0),    # 赤
                GOAL: (0, 0, 255)      # 青
            }
        
    def draw(self, screen):
        for r, row in enumerate(self.MAP_DATA):#行
            for c, tile in enumerate(row):#列
                color = self.colors.get(tile, (255, 255, 255))
                rect = (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pg.draw.rect(screen, color, rect)# マスの枠線
                pg.draw.rect(screen, (50, 50, 50), rect, 1)

    def get_tile(self, mouse_pos): #マウス座標
        c = mouse_pos[0] // TILE_SIZE
        r = mouse_pos[1] // TILE_SIZE
        if 0 <= r < 6 and 0 <= c < 9:
            return r, c, self.MAP_DATA[r][c]
        if mouse_pos[1] > 480 and 0 <= mouse_pos[0] < 160: 
            ans = "blocker"
            return ans
        if mouse_pos[1] > 480 and 160 <= mouse_pos[0] < 320: 
            ans = "shooter"
            return ans
        return None


class Playing(Stage):
    def __init__(self, screen):
        super().__init__()
        self.img_shooter_cost = pg.image.load("assets/shooter_cost.png")
        self.img_blocker_cost = pg.image.load("assets/blocker_cost.png")
        self.font = pg.font.SysFont(None, 24)
        self.enemies = []  # Enemyオブジェクトのリスト
        self.units = []    # Unitオブジェクトのリスト
        


    def blit(self, screen, clock):
        screen.blit(self.img_shooter_cost, (160, 480))
        screen.blit(self.img_blocker_cost,(0,480))
        text_img = self.font.render(f"COST: {COST}", True, pg.Color("WHITE"))
        screen.blit(text_img, (5*80, 6*80))
        return self
