import pygame
import sys
from stages import Stage, TILE_SIZE

def main():
    pygame.init()
    # 9列×80px, 6行×80px
    screen = pygame.display.set_mode((720, 480))
    pygame.display.set_caption("Tower Defense Project")
    clock = pygame.time.Clock()
    
    stage = Stage()

    while True:
        screen.fill((0, 0, 0))
        
        # イベント処理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # クリックした場所のタイル情報を取得
                info = stage.get_tile(event.pos)
                if info:
                    r, c, tile_type = info
                    print(f"Clicked: Row {r}, Col {c}, Type {tile_type}")

        # 描画
        stage.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()