"""味方ユニットの動きと情報"""
import pygame as pg
import bullet as b
import config

class Unit:
    """味方ユニットの配置場所を決めるためのクラス"""
    def __init__(self, r, c):
        """初期化"""
        image_size = 75
        self.r, self.c = r, c
        offset = (80 - image_size) // 2#余白
        self.x = c * 80 + offset
        self.y = r * 80 + offset

class Blocker(Unit):
    """ブロッカーのクラス"""
    def __init__(self,r,c):
        """初期化"""
        super().__init__(r, c)
        self.hp = 15
        self.max_block = 3
        self.curr_block = 0
        self.is_blocker = True
        config.COST -= 8
        self.img_blocker = pg.image.load("assets/blocker.png")
        self.angle = 0 # 0,90,180,270

    def rotate(self):
        """向きを変える処理"""
        self.angle = (self.angle + 90) % 360
        self.img_blocker = pg.transform.rotate(self.img_blocker,self.angle)

    def draw(self,screen):
        """描画処理"""
        screen.blit(self.img_blocker,(self.x,self.y))


class Shooter(Unit):
    """シューター(READMEではattacker)のクラス"""
    def __init__(self,r,c):
        """初期化"""
        super().__init__(r,c)
        self.hp = 3
        self.block = 0
        config.COST -= 10
        self.img_shooter = pg.image.load("assets/shooter.png")
        self.angle = 90 # 0,90,180,270
        self.shot_timer = 0
        self.shot_interval = 1 * 1000

    def update(self, clock, bullets):
        """弾の発射を管理するための処理"""
        self.shot_timer += clock.get_time()
        if self.shot_timer >= self.shot_interval:
            bullets.append(b.Bullet(self.c * 80, self.r * 80, self.angle))
            self.shot_timer = 0

    def rotate(self):
        """向きを変える処理"""
        self.angle = (self.angle + 90) % 360
        self.img_shooter = pg.transform.rotate(self.img_shooter,90)

    def draw(self,screen):
        """描画処理"""
        screen.blit(self.img_shooter,(self.x,self.y))
