"""
康威生命游戏 - 逻辑模块
控制完整游戏逻辑，协调地图更新
"""

from game_map import GameMap


class LifeGame:
    """游戏逻辑控制器"""
    
    def __init__(self, width: int, height: int):
        """
        初始化游戏
        Args:
            width: 地图宽度
            height: 地图高度
        """
        self.map = GameMap(width, height)
        self.generation = 0  # 当前代数
        self.is_running = False  # 是否运行中
        self.speed = 10  # 更新速度（代/秒）
    
    def start(self) -> None:
        """开始游戏"""
        self.is_running = True
    
    def stop(self) -> None:
        """暂停游戏"""
        self.is_running = False
    
    def step(self) -> None:
        """手动推进一代"""
        self.map.update()
        self.generation += 1
    
    def reset(self) -> None:
        """重置游戏"""
        self.map.randomize()
        self.generation = 0
    
    def clear(self) -> None:
        """清空地图"""
        self.map.clear()
        self.generation = 0
    
    def toggle_cell(self, x: int, y: int) -> None:
        """切换细胞状态"""
        self.map.toggle_cell(x, y)
    
    def set_cell(self, x: int, y: int, state: int) -> None:
        """设置细胞"""
        self.map.set_cell(x, y, state)
    
    def get_map(self) -> GameMap:
        """获取地图对象"""
        return self.map
    
    def get_generation(self) -> int:
        """获取当前代数"""
        return self.generation
    
    def get_alive_count(self) -> int:
        """获取活细胞数"""
        return self.map.get_alive_count()
