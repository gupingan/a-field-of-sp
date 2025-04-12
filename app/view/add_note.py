import re
from app.lib import QtCore, QtWidgets
from app.ui import add_note_ui


class AddNote(QtWidgets.QDialog):
    addSignal = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint)
        self.ui = add_note_ui.Ui_AddNote()
        self.ui.setupUi(self)
        self.build_init_datas()
        self.connect_ui_events()

    def build_init_datas(self):
        """
        构建初始的数据 控件参数
        :return:
        """
        self.ui.paste_btn.setFocus()
        self.handle_paste_btn_click()

    def connect_ui_events(self):
        """
        连接各个控件的槽函数与信号
        :return:
        """
        self.ui.confirm_btn.clicked.connect(self.handle_confirm_btn_click)
        self.ui.cancel_btn.clicked.connect(self.reject)
        self.ui.paste_btn.clicked.connect(self.handle_paste_btn_click)

    def handle_confirm_btn_click(self):
        note_id = self.ui.note_id_edit.text().strip()
        if ' ' in note_id:
            QtWidgets.QMessageBox.critical(self, '添加失败', '不允许空格出现，请修改后重试')
        else:
            self.addSignal.emit(note_id)
            self.close()

    def handle_paste_btn_click(self):
        """
        处理`粘贴`按钮的单击事件
        功能：剪贴板获取文本，尝试解析出笔记ID，并将其设置到输入框中
        :return:
        """
        self.ui.note_id_edit.clear()
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard_text = clipboard.text()

        pattern = r"https://www.xiaohongshu.com/explore/([0-9a-f]{24})|([0-9a-f]{24})"
        matches = re.search(pattern, clipboard_text)
        note_id = ""
        if matches:
            if matches.group(1):
                note_id = matches.group(1)
            elif matches.group(2):
                note_id = matches.group(2)
            self.ui.note_id_edit.setText(note_id)
