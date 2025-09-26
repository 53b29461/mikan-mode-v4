from collections import deque
from typing import List, Optional, Any

class MikanQueue:
    """指定枚数1セットのカードキューを管理するクラス"""

    def __init__(self, cards: List[Any], set_size: int = 5):
        """
        Args:
            cards: 指定枚数までのカードリスト
            set_size: セットのサイズ（デフォルト5枚）
        """
        self.set_size = set_size
        self.queue = deque(cards[:set_size])  # 指定枚数まで
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
    
    def push_front(self, card: Any):
        """カードをキューの先頭に追加"""
        self.queue.appendleft(card)
        # completedからも除去（戻る操作の場合）
        if card in self.completed:
            self.completed.remove(card)

    def __len__(self) -> int:
        """キュー内のカード数"""
        return len(self.queue)