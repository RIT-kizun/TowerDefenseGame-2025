import pygame as pg

TILE_SIZE = 80
WALL   = 0  # 壁（配置不可）
PATH   = 1  # 道（味方1: Blocker用）
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
                PATH: (100, 100, 100), # 灰色
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
        return None
