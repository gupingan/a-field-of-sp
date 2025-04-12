import re
import xhs
from loguru import logger
from app.lib import QtCore, QtWidgets, QtGui
from app.lib.factory import PrivateUserCenter, PrivateUserFactory
from app.lib.threads import NetworkPool
from app.ui import import_user_ui


def get_web_session(cookies):
    match = re.search(r'web_session=([^;]+)', cookies)
    if match:
        return match.group(1)
    return None


class ImportUser(QtWidgets.QDialog):
    logger = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlag(QtCore.Qt.WindowType.WindowCloseButtonHint)
        self.ui = import_user_ui.Ui_ImportUsers()
        self.ui.setupUi(self)
        self.connect_ui_events()
        self.service_deployment()

    def connect_ui_events(self):
        self.logger.connect(self.ui.logger.append)
        self.ui.upload_btn.clicked.connect(self.handle_upload_btn_click)
        self.ui.paste_btn.clicked.connect(self.handle_paste_tbn_click)
        self.ui.verify_btn.clicked.connect(self.handle_verify_btn_click)
        self.ui.confirm_btn.clicked.connect(self.handle_confirm_btn_click)

    def service_deployment(self):
        self.factory = PrivateUserFactory()
        self.success_users = []
        self.failure_users = []
        self.network = NetworkPool(self)
        self.network.set_max_thread(6)
        self.network.allTasksDone.connect(self.on_import_user_all_finished)
        self.success_mutex = QtCore.QMutex()
        self.failure_mutex = QtCore.QMutex()

    def on_import_user_all_finished(self):
        self.ui.verify_btn.setEnabled(True)
        self.ui.confirm_btn.setEnabled(True)
        self.logger.emit(f'所有CK均已验证，成功：{len(self.success_users)} 条，失败：{len(self.failure_users)} 条')

    def handle_upload_btn_click(self):
        """
        处理点击导入笔记的事件
        :return:
        """
        route_folder = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.DesktopLocation)
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "导入CK文本", route_folder, "Cookies File (*.txt)")
        if file_path:
            self.logger.emit(f'正在从本地文件 {file_path} 中导入，请稍后')
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    i = 0
                    for line in file:
                        if not line or 'web_session' not in line:
                            continue
                        self.ui.cookies_te.append(line)
                        i += 1
                self.logger.emit(f'导入 Cookie 完成，共计: {i} 条')
            except Exception as e:
                logger.exception(e)
                self.logger.emit('导入文件失败，具体原因可查看软件日志')

    def handle_paste_tbn_click(self):
        clipboard = QtGui.QClipboard(self)
        raw_text = clipboard.text()
        raw_texts = raw_text.split('\n')
        cookies = [rt for rt in raw_texts if 'web_session' in rt]
        for cookie in cookies:
            self.ui.cookies_te.append(cookie)
        self.logger.emit(f'导入 Cookie 完成，共计: {len(cookies)} 条')

    def handle_verify_btn_click(self):
        raw_text = self.ui.cookies_te.toPlainText().split('\n')
        if not raw_text:
            return None

        self.ui.verify_btn.setEnabled(False)
        self.ui.confirm_btn.setEnabled(False)
        cookies = [rt for rt in raw_text if 'web_session' in rt]
        if not cookies:
            self.ui.verify_btn.setEnabled(True)
            self.ui.confirm_btn.setEnabled(True)
            return None

        for cookie in cookies:
            self.network.start_task(self.append_self_users, cookie)

    def append_self_users(self, cookie: str):
        session = get_web_session(cookie)
        try:
            response = xhs.API().set_cookies(cookie).user_me()
            if response.get('code') == 0 and response.get('data'):
                user_id = response['data']['user_id']
                nickname = response['data']['nickname']
                user = self.factory.make_user(user_id, nickname, session, '')
                self.success_mutex.lock()
                self.success_users.append(user)
                self.logger.emit(f'用户 {nickname} - 验证成功')
                self.success_mutex.unlock()
            else:
                failure_message = response.get('msg', '未知原因')
                self.failure_mutex.lock()
                self.failure_users.append(session)
                self.failure_mutex.unlock()
                self.logger.emit(f'{session} - 验证失败，{failure_message}')
        except Exception as e:
            logger.exception(e)
            self.logger.emit(f'{session} - 验证失败，可查看软件日志')
            self.failure_mutex.lock()
            self.failure_users.append(session)
            self.failure_mutex.unlock()

    def handle_confirm_btn_click(self):
        if not self.success_users:
            QtWidgets.QMessageBox.critical(self, '导入错误', '不存在验证成功的用户，无法导入')
            return None

        for user in self.success_users:
            if user in PrivateUserCenter.data:
                self.logger.emit(f'用户 {user.name} - 已存在，不被添加')
                continue

            PrivateUserCenter.append(user)
            self.logger.emit(f'用户 {user.name} - 添加成功')

        PrivateUserCenter.save()

        self.success_users.clear()
        self.logger.emit('成功验证的用户已经清空')
