import pygame as pg
import enemy as e
import unit as u
import config as c
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
        if r < 6:
            if 0 <= c < 9:
                return r, c, self.MAP_DATA[r][c]
        else:        
            if 0 <= c <= 1: 
                return "blocker"
            if  2<= c <= 3: 
                return "shooter"
            if c == 6:
                return -1
        
        return None


class Playing(Stage):
    def __init__(self, screen):
        super().__init__()
        self.img_shooter_cost = pg.image.load("assets/shooter_cost.png")
        self.img_shooter = pg.image.load("assets/shooter.png")
        self.img_shooter = pg.transform.scale(self.img_shooter,(60,60))
        self.img_blocker_cost = pg.image.load("assets/blocker_cost.png")
        self.img_blocker = pg.image.load("assets/blocker.png")
        self.img_blocker = pg.transform.scale(self.img_blocker,(60,60))
        self.img_select = pg.image.load("assets/select.png")
        self.img_cancel = pg.image.load("assets/cancel.png")
        self.font = pg.font.SysFont(None, 27)
        self.selected_unit = None
        self.units = []    # Unitオブジェクトのリスト
        


    def blit(self, screen, clock):
        screen.blit(self.img_shooter_cost, (160, 480))
        screen.blit(self.img_blocker_cost,(0,480))
        screen.blit(self.img_select,(320,480))
        screen.blit(self.img_cancel,(480,480))
        
        if self.selected_unit:
            if self.selected_unit == "blocker":
                screen.blit(self.img_blocker,(410,490))
            if self.selected_unit == "shooter":
                screen.blit(self.img_shooter,(410,490))
        text_img = self.font.render(f"COST: {COST}", True, pg.Color("BLACK"))
        screen.blit(text_img, (int(7.5*80), int(6.3*80)))
        return self
    
    def draw(self, screen):
        super().draw(screen)  # マップの描画
        for unit in self.units:  # 配置したユニットを順番に描画
            unit.draw(screen)
    
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            info = self.get_tile(event.pos)
            print(f"Selected: {info}")#デバッグ用ログ
            
            # ユニット選択（文字列が返ってきた場合）
            if isinstance(info, str):
                self.selected_unit = info
            
            # ユニット配置（座標タプルが返ってきた場合）
            elif isinstance(info, tuple):
                r, c, tile_type = info
                self._try_place_unit(r, c, tile_type)
                
            elif isinstance(info,int):
                self.selected_unit = None


    def _try_place_unit(self, r, c, tile_type):
        if not self.selected_unit:
            return

        # すでに何かが置かれていないかチェック
        if any(u.r == r and u.c == c for u in self.units):
            return
        

        # ユニットごとの配置条件
        if self.selected_unit == "blocker" and tile_type == ROAD:
            self.units.append(u.Blocker(r, c))
            self.selected_unit = None # 配置後に選択解除
            
        elif self.selected_unit == "shooter" and tile_type == HIGH:
            self.units.append(u.Shooter(r, c))
            self.selected_unit = None # 配置後に選択解除
