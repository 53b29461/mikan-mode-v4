from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip, showInfo
from anki.cards import Card
import time
from .mikan_session import MikanSession
from .mikan_queue import MikanQueue

class MikanDialog(QDialog):
    """Mikan Mode用の独立したダイアログ"""
    
    def __init__(self, session: MikanSession):
        super().__init__(mw)
        self.session = session
        self.current_card = None
        self.is_showing_answer = False
        
        self.setWindowTitle("Mikan Mode")
        self.setModal(True)

        # ウィンドウサイズ設定
        self.resize(800, 600)  # 初期サイズ
        self.setMinimumSize(600, 400)  # 最小サイズ

        # リサイズ可能にする
        self.setSizeGripEnabled(True)
        
        self._setup_ui()
        self._setup_shortcuts()
        self._show_next_card()
        
    def _setup_ui(self):
        """UIをセットアップ"""
        layout = QVBoxLayout()
        
        # 進捗表示
        self.progress_label = QLabel()
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setMinimumHeight(30)
        self.progress_label.setMaximumHeight(40)
        layout.addWidget(self.progress_label)
        
        # カード表示エリア
        self.web_view = mw.web.createWindow(self)
        layout.addWidget(self.web_view, 1)
        
        # ボタンエリア
        button_layout = QHBoxLayout()
        
        # ボタンの高さを設定（リサイズに応じて調整可能）
        button_height = 45
        
        self.show_answer_button = QPushButton("Show Answer (Space)")
        self.show_answer_button.clicked.connect(self._on_show_answer)
        self.show_answer_button.setMinimumHeight(button_height)
        self.show_answer_button.setMaximumHeight(button_height + 10)
        button_layout.addWidget(self.show_answer_button)
        
        self.again_button = QPushButton("Again (1)")
        self.again_button.clicked.connect(lambda: self._on_answer(1))
        self.again_button.setMinimumHeight(button_height)
        self.again_button.setMaximumHeight(button_height + 10)
        self.again_button.setVisible(False)
        button_layout.addWidget(self.again_button)

        self.hard_button = QPushButton("Hard (2)")
        self.hard_button.clicked.connect(lambda: self._on_answer(2))
        self.hard_button.setMinimumHeight(button_height)
        self.hard_button.setMaximumHeight(button_height + 10)
        self.hard_button.setVisible(False)
        button_layout.addWidget(self.hard_button)

        self.good_button = QPushButton("Good (Space/3)")
        self.good_button.clicked.connect(lambda: self._on_answer(3))
        self.good_button.setMinimumHeight(button_height)
        self.good_button.setMaximumHeight(button_height + 10)
        self.good_button.setVisible(False)
        button_layout.addWidget(self.good_button)

        self.easy_button = QPushButton("Easy (4)")
        self.easy_button.clicked.connect(lambda: self._on_answer(4))
        self.easy_button.setMinimumHeight(button_height)
        self.easy_button.setMaximumHeight(button_height + 10)
        self.easy_button.setVisible(False)
        button_layout.addWidget(self.easy_button)

        self.back_button = QPushButton("Back (B)")
        self.back_button.clicked.connect(self._on_back)
        self.back_button.setMinimumHeight(button_height)
        self.back_button.setMaximumHeight(button_height + 10)
        self.back_button.setVisible(False)
        button_layout.addWidget(self.back_button)

        self.exit_button = QPushButton("Exit (Esc)")
        self.exit_button.clicked.connect(self._on_exit)
        self.exit_button.setMinimumHeight(button_height)
        self.exit_button.setMaximumHeight(button_height + 10)
        self.exit_button.setVisible(False)  # 非表示にする
        button_layout.addWidget(self.exit_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def _setup_shortcuts(self):
        """ショートカットキーを設定"""
        # スペースキーまたはEnterで解答を表示/わかった
        space_shortcut = QShortcut(QKeySequence("Space"), self)
        space_shortcut.activated.connect(self._on_space_pressed)
        
        enter_shortcut = QShortcut(QKeySequence("Return"), self)
        enter_shortcut.activated.connect(self._on_space_pressed)
        
        # 1キーでもう一度
        one_shortcut = QShortcut(QKeySequence("1"), self)
        one_shortcut.activated.connect(self._on_one_pressed)
        
        # 2キーで難しい
        two_shortcut = QShortcut(QKeySequence("2"), self)
        two_shortcut.activated.connect(self._on_two_pressed)
        
        # 3キーで普通
        three_shortcut = QShortcut(QKeySequence("3"), self)
        three_shortcut.activated.connect(self._on_three_pressed)
        
        # 4キーで簡単
        four_shortcut = QShortcut(QKeySequence("4"), self)
        four_shortcut.activated.connect(self._on_four_pressed)
        
        # Bキーで戻る
        back_shortcut = QShortcut(QKeySequence("B"), self)
        back_shortcut.activated.connect(self._on_back)

        # Escキーで終了
        esc_shortcut = QShortcut(QKeySequence("Escape"), self)
        esc_shortcut.activated.connect(self._on_exit)
        
    def _update_progress(self):
        """進捗表示を更新"""
        progress = self.session.get_progress()
        text = (f"Set: {progress['current_set']}/{progress['total_sets']} | "
                f"Completed: {progress['completed_cards']}/{progress['total_cards']} cards | "
                f"Current queue: {progress['remaining_in_queue']}/{progress['set_size']} cards")
        self.progress_label.setText(text)

    def _update_button_visibility(self):
        """戻るボタンの表示・非表示を更新"""
        can_go_back = self.session.can_go_back()
        self.back_button.setVisible(can_go_back and not self.is_showing_answer)
        
    def _show_next_card(self):
        """次のカードを表示"""
        if self.session.is_complete():
            self._show_completion_message()
            self.accept()
            return
            
        queue = self.session.get_current_queue()
        if not queue:
            self._show_completion_message()
            self.accept()
            return
            
        card_id = queue.get_current_card()
        if card_id:
            self.current_card = mw.col.get_card(card_id)
            # カードを履歴に追加
            self.session.add_to_history(card_id)

            # 質問を表示
            self.is_showing_answer = False
            self._render_card(show_answer=False)
            
            # ボタンの表示を切り替え
            self.show_answer_button.setVisible(True)
            self.again_button.setVisible(False)
            self.hard_button.setVisible(False)
            self.good_button.setVisible(False)
            self.easy_button.setVisible(False)

            self._update_progress()
            self._update_button_visibility()
            
    def _render_card(self, show_answer=False):
        """カードをレンダリング"""
        if not self.current_card:
            return
            
        # Ankiの標準的なレンダリング方法を使用
        if show_answer:
            html = self.current_card.answer()
        else:
            html = self.current_card.question()
            
        # CSSを取得
        css = self.current_card.css()
        
        # 基本的なHTMLテンプレート
        full_html = f"""
<!doctype html>
<html>
<head>
<style>
{css}
</style>
</head>
<body class="card">
{html}
</body>
</html>
"""
        
        self.web_view.stdHtml(full_html)
        
    def _on_show_answer(self):
        """解答を表示"""
        self.is_showing_answer = True
        self._render_card(show_answer=True)
        
        # ボタンの表示を切り替え
        self.show_answer_button.setVisible(False)
        self.again_button.setVisible(True)
        self.hard_button.setVisible(True)
        self.good_button.setVisible(True)
        self.easy_button.setVisible(True)

        # 戻るボタンの表示を更新
        self._update_button_visibility()
        
    def _on_answer(self, ease):
        """回答ボタンの処理"""
        queue = self.session.get_current_queue()
        if queue:
            card_id = queue.get_current_card()
            if card_id:
                # 初回回答結果を記録
                self.session.record_first_answer(card_id, ease)

                if ease == 1:  # Again（もう一度）
                    queue.mark_as_unknown()
                else:  # Hard/Good/Easy（すべてわかった扱い）
                    queue.mark_as_known()
                    self.session.mark_card_complete(card_id)

        self._show_next_card()

    def _on_back(self):
        """戻るボタンの処理"""
        if self.session.can_go_back():
            # 前のカードに戻る
            previous_card_id = self.session.go_back()
            if previous_card_id:
                # カードを再表示
                self.current_card = mw.col.get_card(previous_card_id)

                # 質問を表示
                self.is_showing_answer = False
                self._render_card(show_answer=False)

                # ボタンの表示を切り替え
                self.show_answer_button.setVisible(True)
                self.again_button.setVisible(False)
                self.hard_button.setVisible(False)
                self.good_button.setVisible(False)
                self.easy_button.setVisible(False)

                # 進捗を更新
                self._update_progress()
                self._update_button_visibility()

    def _on_exit(self):
        """終了ボタンの処理"""
        reply = QMessageBox.question(
            self,
            "Exit Mikan Mode",
            "Exit Mikan Mode?\n(Your learning progress will be saved to Anki)",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # 統計を一括更新
            updated_count = self.session.apply_final_answers()
            if updated_count > 0:
                showInfo(f"Learning results saved to Anki\nUpdated cards: {updated_count}")
            self.reject()
            
    def _show_completion_message(self):
        """完了メッセージを表示"""
        # 統計を一括更新
        updated_count = self.session.apply_final_answers()
        
        progress = self.session.get_progress()
        stats = self.session.get_statistics()
        
        showInfo(f"Mikan Mode Complete!\n\n"
                f"Cards studied: {progress['completed_cards']}\n"
                f"Results saved to Anki: {updated_count}\n\n"
                f"--- Performance ---\n"
                f"New cards: {stats['new_correct']}/{stats['new_total']} ({stats['new_percentage']:.0f}%)\n"
                f"All cards: {stats['all_correct']}/{stats['all_total']} ({stats['all_percentage']:.0f}%)\n\n"
                f"Great work!")
                
    def _on_space_pressed(self):
        """スペースキーが押された時の処理"""
        if not self.is_showing_answer:
            # 解答を表示
            self._on_show_answer()
        else:
            # 普通（Good）
            self._on_answer(3)
            
    def _on_one_pressed(self):
        """1キーが押された時の処理"""
        if self.is_showing_answer:
            self._on_answer(1)  # もう一度
            
    def _on_two_pressed(self):
        """2キーが押された時の処理"""
        if self.is_showing_answer:
            self._on_answer(2)  # 難しい
            
    def _on_three_pressed(self):
        """3キーが押された時の処理"""
        if self.is_showing_answer:
            self._on_answer(3)  # 普通
            
    def _on_four_pressed(self):
        """4キーが押された時の処理"""
        if self.is_showing_answer:
            self._on_answer(4)  # 簡単
            
    def closeEvent(self, event):
        """ダイアログが閉じられる時の処理（途中終了時に結果を送信）"""
        # 統計を一括更新
        if hasattr(self, 'session') and self.session:
            updated_count = self.session.apply_final_answers()
            if updated_count > 0:
                from aqt.utils import showInfo
                showInfo(f"Learning results saved to Anki\nUpdated cards: {updated_count}")
        
        super().closeEvent(event)