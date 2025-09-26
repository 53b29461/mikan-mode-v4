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

    # Set size setting
    set_size_layout = QHBoxLayout()
    set_size_layout.addWidget(QLabel("Cards per set:"))

    set_size_spinbox = QSpinBox()
    set_size_spinbox.setMinimum(3)
    set_size_spinbox.setMaximum(10)
    set_size_spinbox.setValue(5)
    set_size_spinbox.setSuffix(" cards")
    set_size_layout.addWidget(set_size_spinbox)

    layout.addLayout(set_size_layout)

    # Number of sets setting
    num_sets_layout = QHBoxLayout()
    num_sets_layout.addWidget(QLabel("Number of sets:"))

    num_sets_spinbox = QSpinBox()
    num_sets_spinbox.setMinimum(1)
    num_sets_spinbox.setMaximum(100)
    num_sets_spinbox.setValue(6)
    num_sets_spinbox.setSuffix(" sets")
    num_sets_layout.addWidget(num_sets_spinbox)

    layout.addLayout(num_sets_layout)

    # Total cards display
    total_layout = QHBoxLayout()
    total_label = QLabel("Total cards: 30")
    total_label.setStyleSheet("color: gray; font-style: italic;")
    total_layout.addWidget(total_label)
    layout.addLayout(total_layout)

    # Update total when values change
    def update_total():
        total = set_size_spinbox.value() * num_sets_spinbox.value()
        total_label.setText(f"Total cards: {total}")

    set_size_spinbox.valueChanged.connect(update_total)
    num_sets_spinbox.valueChanged.connect(update_total)

    # Buttons
    button_layout = QHBoxLayout()

    start_button = QPushButton("Start")
    start_button.clicked.connect(lambda: start_mikan_mode(
        set_size_spinbox.value(), num_sets_spinbox.value(), dialog))
    button_layout.addWidget(start_button)

    cancel_button = QPushButton("Cancel")
    cancel_button.clicked.connect(dialog.reject)
    button_layout.addWidget(cancel_button)

    layout.addLayout(button_layout)

    dialog.setLayout(layout)
    dialog.exec()

def start_mikan_mode(set_size: int, num_sets: int, dialog: QDialog):
    """Mikan Modeを開始"""
    dialog.accept()

    try:
        # 現在のデッキIDを取得
        deck_id = mw.col.decks.selected()

        # セッションを作成（総カード数とセットサイズを渡す）
        session_size = set_size * num_sets
        session = MikanSession(deck_id, session_size, set_size)

        # Mikan Modeダイアログを表示
        mikan_dialog = MikanDialog(session)
        mikan_dialog.exec()

    except Exception as e:
        showInfo(f"An error occurred: {str(e)}")

# Ankiのプロフィールがロードされたときに実行
gui_hooks.profile_did_open.append(on_profile_loaded)

