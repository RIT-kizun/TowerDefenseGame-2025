import pygame as pg
import sys
import stages

def main():
    pg.init()
    # マップ9列*6行,1マス80px + 下部ボタン部分1行
    screen = pg.display.set_mode((720, 560))
    pg.display.set_caption("Tower Defense Game")
    clock = pg.time.Clock()
    stage = stages.Playing(screen)
    
    

    while True:
        screen.fill((255, 255, 255))
        
        stage = stage.blit(screen,clock)
        
        # 閉じるボタンが押されたら終了する。
        for event in pg.event.get():  # イベント一覧を取得して、各イベントを調べる。
            if event.type == pg.QUIT: # もし、閉じるボタンが押されたら。
                pg.quit()             # PyGame を終了する。これだけではウィンドウは閉じない。
                sys.exit()            # ウィンドウを閉じて、プログラムを終了する。
            
            if event.type == pg.MOUSEBUTTONDOWN:
                # クリックした場所のタイル情報を取得
                info = stage.get_tile(event.pos)
                if info:
                    if len(info) == 3:
                        r, c, tile_type = info
                        print(f"Clicked: Row {r}, Col {c}, Type {tile_type}")
                    else:
                        print(f"Clicked: {info}")

        # 描画
        stage.draw(screen)
        
        pg.display.flip()#画面全体を更新
        clock.tick(60)#1秒間に60回

if __name__ == "__main__":
    main()