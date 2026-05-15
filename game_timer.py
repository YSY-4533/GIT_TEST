"""
康威生命游戏 - 计时模块
负责时间控制，定时触发游戏更新
"""

import pygame
from life_game import LifeGame


class GameTimer:
    """游戏计时器"""
    
    def __init__(self, game: LifeGame, fps: int = 60):
        """
        初始化计时器
        Args:
            game: 游戏逻辑对象
            fps: 帧率
        """
        self.game = game
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.update_interval = 1000 / fps  # 毫秒
        self.last_update_time = 0
    
    def set_speed(self, speed: int) -> None:
        """设置更新速度（代/秒）"""
        self.game.speed = speed
    
    def update(self, current_time: int) -> bool:
        """
        更新计时器
        Args:
            current_time: 当前时间（毫秒）
        Returns:
            是否需要更新游戏（True表示需要）
        """
        if not self.game.is_running:
            return False
        
        # 根据速度计算更新间隔
        interval = 1000 / self.game.speed
        
        if current_time - self.last_update_time >= interval:
            self.last_update_time = current_time
            self.game.step()
            return True
        
        return False
    
    def tick(self) -> None:
        """每帧调用，控制帧率"""
        self.clock.tick(self.fps)
    
    def get_fps(self) -> float:
        """获取当前FPS"""
        return self.clock.get_fps()
