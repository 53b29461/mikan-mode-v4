from aqt import mw
from aqt.qt import QAction, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox, QLabel
from aqt.utils import tooltip, showInfo
from aqt import gui_hooks
from .mikan_session import MikanSession
from .mikan_dialog import MikanDialog

def on_profile_loaded():
    action = QAction("Mikan Mode", mw)
    action.triggered.connect(show_mikan_dialog)
    mw.form.menuTools.addAction(action)

def show_mikan_dialog():
    """Mikan Mode開始ダイアログを表示"""
    dialog = QDialog(mw)
    dialog.setWindowTitle("Mikan Mode Settings")
    dialog.setModal(True)
    
    layout = QVBoxLayout()
    
    # Session size setting
    size_layout = QHBoxLayout()
    size_layout.addWidget(QLabel("Session size:"))
    
    size_spinbox = QSpinBox()
    size_spinbox.setMinimum(5)
    size_spinbox.setMaximum(500)
    size_spinbox.setValue(30)
    size_spinbox.setSuffix(" cards")
    size_layout.addWidget(size_spinbox)
    
    layout.addLayout(size_layout)
    
    # Buttons
    button_layout = QHBoxLayout()
    
    start_button = QPushButton("Start")
    start_button.clicked.connect(lambda: start_mikan_mode(size_spinbox.value(), dialog))
    button_layout.addWidget(start_button)
    
    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(dialog.reject)
    button_layout.addWidget(cancel_button)
    
    layout.addLayout(button_layout)
    
    dialog.setLayout(layout)
    dialog.exec()

def start_mikan_mode(session_size: int, dialog: QDialog):
    """Mikan Modeを開始"""
    dialog.accept()
    
    try:
        # 現在のデッキIDを取得
        deck_id = mw.col.decks.selected()
        
        # セッションを作成
        session = MikanSession(deck_id, session_size)
        
        # Mikan Modeダイアログを表示
        mikan_dialog = MikanDialog(session)
        mikan_dialog.exec()
        
    except Exception as e:
        showInfo(f"An error occurred: {str(e)}")

# Ankiのプロフィールがロードされたときに実行
gui_hooks.profile_did_open.append(on_profile_loaded)

