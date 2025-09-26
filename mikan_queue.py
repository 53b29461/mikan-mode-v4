from collections import deque
from typing import List, Optional, Any

class MikanQueue:
    """5枚1セットのカードキューを管理するクラス"""
    
    def __init__(self, cards: List[Any]):
        """
        Args:
            cards: 最大5枚のカードリスト
        """
        self.queue = deque(cards[:5])  # 最大5枚まで
        self.completed = []  # このセットで完了したカード
        
    def get_current_card(self) -> Optional[Any]:
        """キューの先頭のカードを返す（削除しない）"""
        if self.queue:
            return self.queue[0]
        return None
    
    def mark_as_known(self) -> Optional[Any]:
        """現在のカードを完了としてキューから削除"""
        if self.queue:
            card = self.queue.popleft()
            self.completed.append(card)
            return card
        return None
    
    def mark_as_unknown(self) -> Optional[Any]:
        """現在のカードをキューの最後に移動"""
        if self.queue:
            card = self.queue.popleft()
            self.queue.append(card)
            return card
        return None
    
    def is_complete(self) -> bool:
        """キューが空かどうか"""
        return len(self.queue) == 0
    
    def remaining_count(self) -> int:
        """残りのカード数"""
        return len(self.queue)
    
    def completed_count(self) -> int:
        """完了したカード数"""
        return len(self.completed)
    
    def __len__(self) -> int:
        """キュー内のカード数"""
        return len(self.queue)