from PySide6 import QtWidgets
from app.lib.core import TomlBase
from app.ui import train_account_settings_ui


class TrainAccountSettings(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = train_account_settings_ui.Ui_TrainAccountSettings()
        self.ui.setupUi(self)
        self.build_interface()
        self.connect_ui_events()

    def build_interface(self):
        self.setting_uis = {
            'like_note': self.ui.random_like_note_cb,
            'collect_note': self.ui.random_collect_note_cb,
            'share_note': self.ui.random_share_note_cb,
            'like_comment': self.ui.random_like_comment_cb,
            'follow_author': self.ui.random_follow_author_cb,
        }
        for name, cb in self.setting_uis.items():
            cb.setProperty('setting_name', name)

        self.ui.preview_time_sp.setValue(TomlBase.preview_min_time)
        for strategy_name in TomlBase.train_strategy:
            if strategy_name in self.setting_uis:
                self.setting_uis[strategy_name].setChecked(True)

    def connect_ui_events(self):
        self.ui.cancel_btn.clicked.connect(self.close)
        self.ui.save_btn.clicked.connect(self.handle_save_btn_click)

    def handle_save_btn_click(self):
        TomlBase.preview_min_time = self.ui.preview_time_sp.value()
        TomlBase.train_strategy = [cb.property('setting_name') for cb in self.setting_uis.values() if cb.isChecked()]
        TomlBase.save()
        self.close()
