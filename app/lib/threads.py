import random
import zipfile
import xhs
import time
import typing as t
from pathlib import Path
from requests import Response, exceptions
from loguru import logger
from app.lib import QtCore
from app.lib.globals import threads, XHS_JS_FILE
from app.lib.core import AtUserCenter, PrivateUserCenter, ConfigCenter, BaseCenter, TomlBase, Unit


def stop_threads():
    for thread in threads:
        if thread.isRunning():
            thread.stop()


class PreloadThread(QtCore.QThread):
    sendMessage = QtCore.Signal(str)
    sendProgress = QtCore.Signal(int)
    close = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.running = False
        self.works = {
            BaseCenter.check_valid: (0.1, '校验配置中'),
            TomlBase.load: (0.1, '读取基本配置'),
            AtUserCenter.load: (0.2, '读取艾特用户列表'),
            PrivateUserCenter.load: (0.2, '读取用户列表'),
            ConfigCenter.load: (0.2, '读取配置列表'),
            self.load_js: (0.2, '正在读取加密脚本'),
        }
        self.total_score = 0

    @staticmethod
    def load_js():
        xhs.init_context(path=XHS_JS_FILE)

    def run(self):
        try:
            for callback, info in self.works.items():
                score = info[0]
                msg = info[1]
                if self.total_score >= 100:
                    break
                self.sendMessage.emit(f"{msg}...")
                callback()
                self.total_score += int(100 * score)
                self.sendProgress.emit(self.total_score)
                logger.debug(f'预加载：{msg} (完成{self.total_score}%)')
                self.msleep(random.randint(10, 100))
            self.finished.emit()
        except exceptions.ConnectionError:
            self.close.emit()
        except Exception as e:
            logger.exception(e)
            self.close.emit()

    def stop(self):
        self.running = False
        self.wait()


class UpdateInfoThread(QtCore.QThread):
    send = QtCore.Signal(Unit)

    def __init__(self, unit: Unit = None, parent=None):
        super().__init__(parent=parent)
        self.running = False
        self.unit = unit

    def set_unit(self, unit: t.Optional[Unit]):
        self.unit = unit

    def run(self):
        threads.append(self)
        self.running = True
        while True:
            if self.unit:
                self.send.emit(self.unit)

            if not self.running:
                break

            self.sleep(1)

    def stop(self):
        self.running = False
        self.wait()


class SaveAllLogsThread(QtCore.QThread):
    success = QtCore.Signal()
    finish = QtCore.Signal()
    error = QtCore.Signal(str)

    def __init__(self, tab_browser, parent=None):
        super().__init__(parent)
        self.tab_browser = tab_browser

    def run(self):
        tab_browser = self.tab_browser
        desktop_path = QtCore.QStandardPaths.writableLocation(
            QtCore.QStandardPaths.StandardLocation.DesktopLocation)
        zip_path = Path(desktop_path) / 'all_unit_logs.zip'

        try:
            with zipfile.ZipFile(zip_path, 'w') as zip_file:
                for i in range(tab_browser.count()):
                    widget = tab_browser.widget(i)
                    unit = widget.unit
                    if isinstance(unit, Unit):
                        logs = widget.pain_logs
                        log_file_path = f'{unit.id}.log'
                        zip_file.writestr(log_file_path, '\n'.join(logs))
            self.success.emit()
        except Exception as e:
            self.error.emit(str(e))

        self.finish.emit()

    def stop(self):
        self.quit()
        self.wait()


class BaseThead(QtCore.QThread):
    proxies = {"http": None, "https": None}
    success = QtCore.Signal(Response)
    failure = QtCore.Signal(Exception)

    def stop(self):
        try:
            self.success.disconnect()
        except RuntimeError:
            pass
        try:
            self.failure.disconnect()
        except RuntimeError:
            pass
        try:
            self.finished.disconnect()
        except RuntimeError:
            pass
        self.quit()
        self.wait()


class WorkerSignals(QtCore.QObject):
    success = QtCore.Signal(dict)
    failure = QtCore.Signal(Exception)
    finished = QtCore.Signal()


class Worker(QtCore.QRunnable):
    def __init__(self, function, *args, timeout=10, max_retries=3, retry_interval=1, **kwargs):
        super().__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_interval = retry_interval
        self.retries = 0

    @QtCore.Slot()
    def run(self):
        try:
            while self.retries < self.max_retries:
                try:
                    response = self.function(*self.args, **self.kwargs)
                    logger.debug(f'线程池请求：{self.function.__name__} - {response}')
                    self.signals.success.emit(response)
                    break
                except ConnectionError:
                    self.retries += 1
                    time.sleep(self.retry_interval)
            else:
                raise ConnectionError('Maximum retry attempts reached')
        except Exception as e:
            logger.exception(e)
            self.signals.failure.emit(e)
        finally:
            self.signals.finished.emit()


class NetworkPool(QtCore.QObject):
    """
    小红薯 API 接口的网络线程池

    用例：
        pool = NetworkPool()
        pool.set_max_thread(4)  # 设置最大线程数为4
        # 启动一个任务
        signals = pool.start_task(...)
        signals.success.connect(success_function)
        signals.failure.connect(failure_function)
        # 连接 allTasksDone 信号
        pool.allTasksDone.connect(all_done_function)
    """
    allTasksDone = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.threadPool = QtCore.QThreadPool()
        self.activeTasks = 0
        self.mutex = QtCore.QMutex()

    def set_max_thread(self, count: int = 4):
        self.threadPool.setMaxThreadCount(count)

    def start_task(self, function, *args, **kwargs):
        worker = Worker(function, *args, **kwargs)
        worker.signals.finished.connect(self.on_task_finished)
        self.mutex.lock()
        self.activeTasks += 1
        self.mutex.unlock()
        self.threadPool.start(worker)
        return worker.signals

    def on_task_finished(self):
        self.mutex.lock()
        self.activeTasks -= 1
        if self.activeTasks == 0:
            self.allTasksDone.emit()
        self.mutex.unlock()
