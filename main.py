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
            
            stage.handle_event(event)

        pg.display.flip()#画面全体を更新
        clock.tick(60)#1秒間に60回

if __name__ == "__main__":
    main()