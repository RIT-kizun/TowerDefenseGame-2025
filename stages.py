import pygame as pg
import enemy as e
import unit as u
import config
import time
import sys
import datetime

TILE_SIZE = 80


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
            found_unit = None
            for unit in self.units:
                if unit.r == r and unit.c == c:
                    found_unit = unit
                    break
            
            if found_unit:
                found_unit.rotate()
            else:
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
        self.cost_timer = 0
        self.units = []    # Unitオブジェクトのリスト
        self.enemies = []
        self.spawn_timer = 0
        self.goal_hp = 3
        self.max_enemy = 15
        self.curr_enemy = 0
        self.bullets = []
        
        


    def blit(self, screen, clock):
        self.draw(screen)
        screen.blit(self.img_shooter_cost, (160, 480))
        screen.blit(self.img_blocker_cost,(0,480))
        screen.blit(self.img_select,(320,480))
        screen.blit(self.img_cancel,(480,480))
        
        for unit in self.units[:]:
            if unit.hp <= 0:
                self.units.remove(unit)
        
        
        #セレクト中の処理
        if self.selected_unit:
            if self.selected_unit == "blocker":
                screen.blit(self.img_blocker,(410,490))
            if self.selected_unit == "shooter":
                screen.blit(self.img_shooter,(410,490))

        #コスト増加
        self.cost_timer += clock.get_time()
        if self.cost_timer >= 1000:
            config.COST += 1
            self.cost_timer -= 1000
        text_COST_img = self.font.render(f"COST: {config.COST}", True, pg.Color("BLACK"))
        text_LIFE_img = self.font.render(f"LIFE: {self.goal_hp}", True, pg.Color("BLACK"))
        text_enemy_count_img = self.font.render(f"ENEMY: {self.max_enemy - self.curr_enemy}", True, pg.Color("BLACK"))
        screen.blit(text_COST_img, (int(7.5*80), int(6*80)))
        screen.blit(text_LIFE_img, (int(7.5*80), int(6.2*80)))
        screen.blit(text_enemy_count_img, (int(7.5*80), int(6.4*80)))
        
        #エネミーの出現
        self.spawn_timer += clock.get_time()
        if self.spawn_timer > 3000 and self.curr_enemy < self.max_enemy:
            self.enemies.append(e.Enemy(1, 0)) 
            self.curr_enemy += 1
            self.spawn_timer = 0
            
        for enemy in self.enemies[:]:
            enemy.move(self.MAP_DATA,self.units,clock)
            enemy.draw(screen)
            if enemy.reached_goal:
                if enemy.blocking_unit:
                    enemy.blocking_unit -= 1
                self.enemies.remove(enemy)
                self.goal_hp -= 1
                
                
                
                
        for unit in self.units:
            if isinstance(unit, u.Shooter):
                unit.update(clock, self.bullets)

        # 2. 矢の移動と当たり判定
        for bullet in self.bullets[:]:
            bullet.move()
            bullet.draw(screen)
            
            # 敵との当たり判定
            bullet_rect = pg.Rect(bullet.x, bullet.y, 8, 8)
            for enemy in self.enemies:
                enemy_rect = pg.Rect(enemy.x, enemy.y, 60, 60)
                if bullet_rect.colliderect(enemy_rect):
                    enemy.hp -= 1
                    bullet.is_active = False
                    break
            
            if not bullet.is_active:
                self.bullets.remove(bullet)

        # 3. 敵の死神判定（HPが0以下なら消す）
        for enemy in self.enemies[:]:
            if getattr(enemy, "hp", 1) <= 0:
                if enemy.blocking_unit:
                    enemy.blocking_unit.curr_block -= 1
                self.enemies.remove(enemy)
                
                
                
        #GAMEOVER
        if self.goal_hp == 0:
            return GameOver(screen)

        #GAMECLEAR
        if self.curr_enemy == self.max_enemy and len(self.enemies) == 0:
            return GameClear(screen)

        return self
    
    def draw(self, screen):
        super().draw(screen)
        for unit in self.units:  # 配置したユニットを順番に描画
            unit.draw(screen)
    
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            info = self.get_tile(event.pos)

            
            # 文字列が返ってきた場合
            if isinstance(info, str):
                self.selected_unit = info
            
            # 座標が返ってきた場合
            elif isinstance(info, tuple):
                r, c, tile_type = info
                self._try_place_unit(r, c, tile_type)
            #   
            elif isinstance(info,int):
                self.selected_unit = None


    def _try_place_unit(self, r, c, tile_type):
        if not self.selected_unit:
            return

        if any(u.r == r and u.c == c for u in self.units):
            return
        

        # ユニットごとの配置条件
        if self.selected_unit == "blocker" and tile_type == ROAD and config.COST >= 8:
            self.units.append(u.Blocker(r, c))
            self.selected_unit = None # 配置後に選択解除
            
        elif self.selected_unit == "shooter" and tile_type == HIGH and config.COST >= 10:
            self.units.append(u.Shooter(r, c))
            self.selected_unit = None # 配置後に選択解除
 


class GameOver(Stage):
    def __init__(self, screen):
        self.surf = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
        self.surf.fill(pg.Color("WHITE"))
        font = pg.font.SysFont(None, 100)
        text = font.render("GAME OVER!", True, pg.Color("RED"))
        text_rect = text.get_rect(center=self.surf.get_rect().center)
        self.steps = 0
        self.surf.blit(text, text_rect)
        
    def blit(self, screen, clock):
        self.steps += 1
        keys = pg.key.get_pressed()
        mouses = pg.mouse.get_pressed()
        screen.blit(self.surf, (0, 0))
        # 1秒（60フレーム）待機後に何か入力があればリスタート
        if self.steps > 60 and (any(keys) or any(mouses)):
            print("----To Be Continued---→")
            pg.quit()
            sys.exit()
        return self
    
    def handle_event(self,event):
        pass

class GameClear(Stage):
    def __init__(self, screen):
        self.steps = 0
        self.surf = pg.Surface((screen.get_width(), screen.get_height()), pg.SRCALPHA)
        self.surf.fill(pg.Color("WHITE"))
        font = pg.font.SysFont(None, 100)
        text = font.render("GAME CLEAR!", True, pg.Color("BLUE"))
        text_rect = text.get_rect(center=self.surf.get_rect().center)
        self.surf.blit(text, text_rect)

    def blit(self, screen, clock):
        self.steps += 1
        keys = pg.key.get_pressed()
        mouses = pg.mouse.get_pressed()
        screen.blit(self.surf, (0, 0))
        if self.steps > 60 and (any(keys) or any(mouses)):
            print("CONGTATULATIONS!!")
            pg.quit
            sys.exit()
        return self

    def handle_event(self,event):
        pass
