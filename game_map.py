"""
康威生命游戏 - 地图模块
管理地图数据的初始化、获取、更新等
"""

import random
from typing import List, Tuple


class GameMap:
    """游戏地图类"""
    
    def __init__(self, width: int, height: int, initial_state: List[List[int]] = None):
        """
        初始化地图
        Args:
            width: 宽度（列数）
            height: 高度（行数）
            initial_state: 初始状态，可选
        """
        self.width = width
        self.height = height
        
        if initial_state is not None:
            if len(initial_state) != height or len(initial_state[0]) != width:
                raise ValueError(f"尺寸不匹配！期望 {height}x{width}")
            self.grid = [row[:] for row in initial_state]
        else:
            self.grid = self._random_init()
    
    def _random_init(self, alive_prob: float = 0.3) -> List[List[int]]:
        """随机初始化"""
        return [
            [1 if random.random() < alive_prob else 0 
             for _ in range(self.width)]
            for _ in range(self.height)
        ]
    
    def get_cell(self, x: int, y: int) -> int:
        """获取细胞状态（0或1）"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return 0  # 边界外视为死
    
    def set_cell(self, x: int, y: int, state: int) -> None:
        """设置细胞状态"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 1 if state else 0
    
    def toggle_cell(self, x: int, y: int) -> None:
        """翻转细胞状态"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 1 - self.grid[y][x]
    
    def count_neighbors(self, x: int, y: int) -> int:
        """计算周围8个邻居中活细胞的数量"""
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                count += self.get_cell(nx, ny)
        return count
    
    def next_generation(self) -> 'GameMap':
        """计算下一代地图（不修改当前）"""
        new_grid = [[0] * self.width for _ in range(self.height)]
        
        for y in range(self.height):
            for x in range(self.width):
                alive = self.grid[y][x]
                neighbors = self.count_neighbors(x, y)
                
                # 康威规则
                if alive == 1:
                    new_grid[y][x] = 1 if neighbors in [2, 3] else 0
                else:
                    new_grid[y][x] = 1 if neighbors == 3 else 0
        
        return GameMap(self.width, self.height, new_grid)
    
    def update(self) -> None:
        """更新到下一代"""
        self.grid = self.next_generation().grid
    
    def clear(self) -> None:
        """清空地图"""
        self.grid = [[0] * self.width for _ in range(self.height)]
    
    def randomize(self, alive_prob: float = 0.3) -> None:
        """随机重置"""
        self.grid = self._random_init(alive_prob)
    
    def get_alive_count(self) -> int:
        """获取活细胞总数"""
        return sum(sum(row) for row in self.grid)
    
    def get_grid(self) -> List[List[int]]:
        """获取地图深拷贝"""
        return [row[:] for row in self.grid]
    
    def __str__(self) -> str:
        return '\n'.join([''.join(['█' if c else ' ' for c in row]) for row in self.grid])
