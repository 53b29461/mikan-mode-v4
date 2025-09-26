import random
from typing import List, Optional, Set
from aqt import mw
from .mikan_queue import MikanQueue

class MikanSession:
    """Mikan Modeのセッション管理クラス"""
    
    def __init__(self, deck_id: int = None, session_size: int = 100):
        """
        Args:
            deck_id: 対象デッキのID（Noneの場合は現在のデッキ）
            session_size: 1セッションのカード数
        """
        self.deck_id = deck_id or mw.col.decks.selected()
        self.session_size = session_size
        self.all_cards: List[int] = []  # カードIDのリスト
        self.completed_cards: Set[int] = set()  # 完了したカードのIDセット
        self.current_set_index = 0  # 現在のセット番号（0-based）
        self.current_queue: Optional[MikanQueue] = None
        self.first_answers: dict[int, int] = {}  # カードID -> 初回回答結果 (1=Again, 2=Hard, 3=Good, 4=Easy)
        self.card_types: dict[int, str] = {}  # カードID -> カードタイプ ("new" or "review")
        
        # セッション用のカードを準備
        self._prepare_cards()
        
    def _prepare_cards(self):
        """Ankiの復習アルゴリズムに基づいてカードを選出しシャッフル"""
        try:
            # デッキ名を取得
            deck_name = mw.col.decks.name(self.deck_id)
            
            # 復習対象のカードを取得
            due_cards = list(mw.col.find_cards(f'deck:"{deck_name}" is:due'))
            
            # 新規カードを取得
            new_cards = list(mw.col.find_cards(f'deck:"{deck_name}" is:new'))
            
            # 学習中のカードも含める
            learning_cards = list(mw.col.find_cards(f'deck:"{deck_name}" is:learn'))
            
            # すべてのカードを結合
            all_card_ids = due_cards + new_cards + learning_cards
            
            # 重複を除去
            all_card_ids = list(set(all_card_ids))
            
            # カードが見つからない場合はすべてのカードから取得
            if not all_card_ids:
                all_card_ids = list(mw.col.find_cards(f'deck:"{deck_name}"'))
            
            # session_sizeまでに制限
            self.all_cards = all_card_ids[:self.session_size]
            
            # カードが1枚もない場合のエラーハンドリング
            if not self.all_cards:
                raise ValueError(f"デッキ '{deck_name}' にカードが見つかりません。")
            
            # カードタイプを記録
            for card_id in self.all_cards:
                card = mw.col.get_card(card_id)
                if card.type == 0:  # 0 = New
                    self.card_types[card_id] = "new"
                else:  # 1 = Learning, 2 = Review, 3 = Relearning
                    self.card_types[card_id] = "review"
            
            # シャッフル
            random.shuffle(self.all_cards)
            
        except Exception as e:
            # エラーが発生した場合は空のリストを設定
            self.all_cards = []
            raise e
        
    def get_current_queue(self) -> Optional[MikanQueue]:
        """現在のキューを取得（なければ次のセットを作成）"""
        if self.current_queue and not self.current_queue.is_complete():
            return self.current_queue
            
        # 新しいセットを作成
        return self.next_set()
        
    def next_set(self) -> Optional[MikanQueue]:
        """次の5枚セットを作成"""
        start_idx = self.current_set_index * 5
        
        # 残りのカードから最大5枚を取得
        remaining_cards = []
        for card_id in self.all_cards[start_idx:start_idx + 5]:
            if card_id not in self.completed_cards:
                remaining_cards.append(card_id)
                
        if not remaining_cards:
            # もうカードがない
            return None
            
        self.current_queue = MikanQueue(remaining_cards)
        self.current_set_index += 1
        return self.current_queue
        
    def mark_card_complete(self, card_id: int):
        """カードを完了済みとしてマーク"""
        self.completed_cards.add(card_id)
        
    def record_first_answer(self, card_id: int, ease: int):
        """初回回答結果を記録"""
        if card_id not in self.first_answers:
            self.first_answers[card_id] = ease
            
    def apply_final_answers(self):
        """セッション終了時に初回回答結果をAnkiに反映"""
        from aqt.utils import showInfo
        updated_count = 0
        
        for card_id, ease in self.first_answers.items():
            try:
                card = mw.col.get_card(card_id)
                # タイマーを開始（統計更新に必要）
                card.start_timer()
                # 適当な時間を設定（実際の学習時間ではないが統計更新のため）
                import time
                card.timer_started = time.time() - 5  # 5秒として設定
                
                mw.col.sched.answerCard(card, ease)
                updated_count += 1
            except Exception as e:
                print(f"カード {card_id} の統計更新に失敗: {e}")
                
        return updated_count
        
    def is_complete(self) -> bool:
        """セッションが完了したかどうか"""
        return len(self.completed_cards) >= len(self.all_cards)
        
    def get_progress(self) -> dict:
        """進捗情報を取得"""
        return {
            'total_cards': len(self.all_cards),
            'completed_cards': len(self.completed_cards),
            'current_set': self.current_set_index,
            'total_sets': (len(self.all_cards) + 4) // 5,  # 切り上げ
            'remaining_in_queue': self.current_queue.remaining_count() if self.current_queue else 0
        }
        
    def get_statistics(self) -> dict:
        """学習統計を取得"""
        new_total = sum(1 for card_id in self.all_cards if self.card_types.get(card_id) == "new")
        new_correct = sum(1 for card_id, answer in self.first_answers.items() 
                         if self.card_types.get(card_id) == "new" and answer != 1)
        
        all_total = len(self.all_cards)
        all_correct = sum(1 for answer in self.first_answers.values() if answer != 1)
        
        return {
            'new_total': new_total,
            'new_correct': new_correct,
            'new_percentage': (new_correct / new_total * 100) if new_total > 0 else 0,
            'all_total': all_total,
            'all_correct': all_correct,
            'all_percentage': (all_correct / all_total * 100) if all_total > 0 else 0
        }