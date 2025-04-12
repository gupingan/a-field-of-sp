import sys
from app.lib import QtWidgets, QtCore, QtGui
from app.lib.globals import LOCK_FILE, ICONS_DIR, LOGS_DIR, NODE_DIR, GlobalStyle
from app.lib.nodejs import NodeJS
from app.utils.logger import logger, register_logger
from app.view.main_window import MainWindow

QtCore.QCoreApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling)


class QSingleApplication(QtWidgets.QApplication):
    def __init__(self, *args, **kwargs):
        super(QSingleApplication, self).__init__(*args, **kwargs)
        self.lock_file_path = str(LOCK_FILE)
        logger.debug(f'锁文件位于：{self.lock_file_path}.')
        self.lock_file = QtCore.QLockFile(self.lock_file_path)
        self.server = None

    @property
    def is_running(self):
        return not self.lock_file.tryLock(1)

    def activate_window(self):
        for widget in self.allWidgets():
            if widget.objectName() == 'Main':
                widget.activateWindow()
                break

    def close_lock(self):
        if self.lock_file is not None:
            self.lock_file.unlock()


def load_stylesheet(app, path):
    file = QtCore.QFile(path)
    file.open(QtCore.QFile.OpenModeFlag.ReadOnly | QtCore.QFile.OpenModeFlag.Text)
    stream = QtCore.QTextStream(file)
    stylesheet = stream.readAll()
    app.setStyleSheet(stylesheet)


def create_app():
    app = QSingleApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon(str(ICONS_DIR / 'app-x48.ico')))
    return app


def app_exit(app=None, errors=None, exit_code=0, clear_lock=True):
    """
    退出程序，确保资源得到释放，并提供错误信息。
    :param app: QApp 应用实例
    :param errors: 应用异常终止所接受的异常示例，提供给 logger记录
    :param exit_code: 退出代码，正常情况下为 0
    :param clear_lock: 是否要清除应用单例锁
    :return:
    """
    if errors:
        logger.exception(errors)
    if app:
        app.closeAllWindows()
    if app and clear_lock:
        app.close_lock()
    sys.exit(exit_code)


def show_message_box(title: str, text: str, icon=QtWidgets.QMessageBox.Icon.Warning):
    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(icon)
    msg_box.setWindowTitle(title)
    msg_box.setText(text)
    msg_box.exec()


def run_app():
    try:
        register_logger(LOGS_DIR)
        NodeJS().setup(NODE_DIR)
    except PermissionError:
        show_message_box(
            '权限错误',
            "解决方式任选其一："
            "\n1.请以管理员身份运行程序；"
            "\n2.请将软件安装在有权限的目录。"
        )
        app_exit()
    except OSError:
        show_message_box(
            '不支持该系统',
            "非常抱歉，当前仅对 Windows 64 位系统进行支持\n"
            "您可以安装 VBox、VMware 等一系列虚拟机后再使用。"
        )
        app_exit()
    except Exception as e:
        app_exit(errors=e)

    app = create_app()

    if app.is_running:
        app.activate_window()
        app_exit(app, clear_lock=False)

    try:
        khs_window = MainWindow()
        khs_window.show()
        exit_code = app.exec_()
        app_exit(app, exit_code=exit_code)
    except Exception as e:
        app_exit(app, e)
