"""
康威生命游戏 - 主程序
使用Pygame实现图形界面
"""

import pygame
import sys
from game_map import GameMap
from life_game import LifeGame
from game_timer import GameTimer

# 配色方案
COLOR_BG = (20, 20, 30)          # 背景色
COLOR_GRID = (40, 40, 50)        # 网格线
COLOR_ALIVE = (0, 255, 150)      # 活细胞
COLOR_DEAD = (30, 30, 40)        # 死细胞
COLOR_UI_BG = (50, 50, 70)       # UI背景
COLOR_TEXT = (200, 200, 220)     # 文字颜色
COLOR_HIGHLIGHT = (100, 200, 255) # 高亮色

# 游戏参数
CELL_SIZE = 10
GRID_WIDTH = 80
GRID_HEIGHT = 60
WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE + 300  # 右侧留UI空间
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE + 50


class GameUI:
    """游戏UI界面"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("康威生命游戏 - Conway's Game of Life")
        
        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        
        # 初始化游戏
        self.game = LifeGame(GRID_WIDTH, GRID_HEIGHT)
        self.timer = GameTimer(self.game, fps=60)
        
        self.paused = False
        self.drawing = False
        self.draw_state = 1  # 1=画活细胞，0=画死细胞
    
    def draw_grid(self) -> None:
        """绘制网格和细胞"""
        grid = self.game.get_map().get_grid()
        
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                if grid[y][x] == 1:
                    pygame.draw.rect(self.screen, COLOR_ALIVE, rect)
                else:
                    pygame.draw.rect(self.screen, COLOR_DEAD, rect)
                
                # 网格线
                pygame.draw.rect(self.screen, COLOR_GRID, rect, 1)
    
    def draw_ui(self) -> None:
        """绘制右侧UI面板"""
        ui_x = GRID_WIDTH * CELL_SIZE + 10
        
        # 面板背景
        pygame.draw.rect(self.screen, COLOR_UI_BG, 
                        (ui_x, 0, 290, WINDOW_HEIGHT))
        
        y_offset = 20
        
        # 标题
        title = self.font.render("康威生命游戏", True, COLOR_HIGHLIGHT)
        self.screen.blit(title, (ui_x + 20, y_offset))
        y_offset += 50
        
        # 统计信息
        gen = self.game.get_generation()
        alive = self.game.get_alive_count()
        
        stats = [
            f"代数: {gen}",
            f"活细胞: {alive}",
            f"速度: {self.game.speed} 代/秒",
            f"{'运行中' if self.game.is_running else '已暂停'}"
        ]
        
        for stat in stats:
            text = self.small_font.render(stat, True, COLOR_TEXT)
            self.screen.blit(text, (ui_x + 20, y_offset))
            y_offset += 35
        
        y_offset += 20
        pygame.draw.line(self.screen, COLOR_GRID, 
                        (ui_x + 20, y_offset), (ui_x + 270, y_offset), 2)
        y_offset += 20
        
        # 操作说明
        instructions = [
            "操作说明:",
            "",
            "空格 - 暂停/继续",
            "R - 随机重置",
            "C - 清空地图",
            "N - 手动下一代",
            "鼠标左键 - 绘制",
            "鼠标右键 - 擦除",
            "+/- - 调整速度",
        ]
        
        for inst in instructions:
            text = self.small_font.render(inst, True, COLOR_TEXT)
            self.screen.blit(text, (ui_x + 20, y_offset))
            y_offset += 30
    
    def handle_events(self) -> bool:
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 空格：暂停/继续
                    if self.game.is_running:
                        self.game.stop()
                        self.paused = True
                    else:
                        self.game.start()
                        self.paused = False
                
                elif event.key == pygame.K_r:
                    # R：随机重置
                    self.game.reset()
                
                elif event.key == pygame.K_c:
                    # C：清空
                    self.game.clear()
                
                elif event.key == pygame.K_n:
                    # N：手动下一代
                    self.game.step()
                
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    # +：加速
                    self.game.speed = min(60, self.game.speed + 1)
                    self.timer.set_speed(self.game.speed)
                
                elif event.key == pygame.K_MINUS:
                    # -：减速
                    self.game.speed = max(1, self.game.speed - 1)
                    self.timer.set_speed(self.game.speed)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                
                # 只在网格区域响应鼠标
                if mx < GRID_WIDTH * CELL_SIZE and my < GRID_HEIGHT * CELL_SIZE:
                    gx = mx // CELL_SIZE
                    gy = my // CELL_SIZE
                    
                    if event.button == 1:  # 左键：画活细胞
                        self.game.set_cell(gx, gy, 1)
                        self.drawing = True
                    elif event.button == 3:  # 右键：画死细胞
                        self.game.set_cell(gx, gy, 0)
                        self.drawing = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.drawing = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.drawing:
                    mx, my = pygame.mouse.get_pos()
                    if mx < GRID_WIDTH * CELL_SIZE and my < GRID_HEIGHT * CELL_SIZE:
                        gx = mx // CELL_SIZE
                        gy = my // CELL_SIZE
                        state = 1 if pygame.mouse.get_pressed()[0] else 0
                        self.game.set_cell(gx, gy, state)
        
        return True
    
    def run(self) -> None:
        """主循环"""
        running = True
        
        while running:
            current_time = pygame.time.get_ticks()
            
            # 处理事件
            running = self.handle_events()
            
            # 更新游戏逻辑
            if self.timer.update(current_time):
                pass  # 游戏已在timer.update中更新
            
            # 绘制
            self.screen.fill(COLOR_BG)
            self.draw_grid()
            self.draw_ui()
            
            pygame.display.flip()
            self.timer.tick()
        
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    ui = GameUI()
    ui.run()
