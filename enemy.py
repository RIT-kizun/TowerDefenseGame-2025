import pygame as pg

class Enemy:
    def __init__(self, r, c):
        self.r, self.c = r, c
        self.x = c * 80 + 10 
        self.y = r * 80 + 10
        self.speed = 2
        self.img = pg.transform.scale(pg.image.load("assets/enemy.png"), (60, 60))
        self.rect = pg.Rect(self.x, self.y, 60, 60)
        self.reached_goal = False
        self.direction = "RIGHT"
        self.last_grid = (r, c)
        self.blocked = False
        self.blocking_unit = None

    def move(self, map_data,units):
        curr_c = int((self.x + 30) // 80)
        curr_r = int((self.y + 30) // 80)
        
        if self.blocking_unit:
            if self.blocking_unit in units:
                return
            else:
                self.blocking_unit = None

        for u in units:
            if u.r == curr_r and u.c == curr_c:
                if u.curr_block < u.max_block:
                    self.blocking_unit = u
                    u.curr_block += 1
                    print(u.curr_block)
                    return

        
        
        #ゴール判定
        if map_data[curr_r][curr_c] == 3:
            self.reached_goal = True
            return

        #移動するマスの判定
        if abs((self.x - 10) % 80) < self.speed and abs((self.y - 10) % 80) < self.speed:
            
            if (curr_r, curr_c) != self.last_grid:
                options = [
                    (0, 1, "RIGHT"),
                    (1, 0, "DOWN"),
                    (-1, 0, "UP"),
                    (0, -1, "LEFT")
                ]

                for dr, dc, d_name in options:
                    next_r, next_c = curr_r + dr, curr_c + dc
                    
                    if 0 <= next_r < 6 and 0 <= next_c < 9:
                        if map_data[next_r][next_c] in [1, 3] and (next_r, next_c) != self.last_grid:
                            self.last_grid = (curr_r, curr_c)
                            self.direction = d_name
                            break
                        
            # 移動処理
        if self.direction == "RIGHT":
            self.x += self.speed
            
        elif self.direction == "DOWN":
            self.y += self.speed
            
        elif self.direction == "UP":
            self.y -= self.speed
            
        elif self.direction == "LEFT":
            self.x -= self.speed

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))