import re
import toml

import xhs
from loguru import logger
from app.lib import QtCore, QtWidgets
from app.lib.core import NormalNote, LinkedUser, Author
from app.lib.globals import NOTE_TYPES
from app.lib.threads import NetworkPool
from app.ui import import_note_ui


class UploadThread(QtCore.QThread):
    finish = QtCore.Signal(list)
    progress = QtCore.Signal(int)
    error = QtCore.Signal(Exception)

    def __init__(self, filepath=None, parent=None):
        super().__init__(parent=parent)
        self._filepath = filepath
        self._method = 1
        self._hash = set()

    def set_method(self, method: int):
        self._method = method

    def set_filepath(self, filepath):
        self._filepath = filepath

    def run(self):
        try:
            if self._method == 1:
                self.handle_toml()
            else:
                self.handle_text()
        except Exception as e:
            self.error.emit(e)

    def handle_text(self):
        note_data = []
        pattern = r"https://www\.xiaohongshu\.com/explore/(?P<note_id>[0-9a-f]{24})(?:\?xsec_token=(?P<xsec_token>[^&]+))?(?:&xsec_source=(?P<xsec_source>[^&]+))?"
        with open(self._filepath, 'r', encoding='utf-8') as file:
            count = 0
            for line in file:
                if count >= 999:
                    break
                match = re.search(pattern, line)
                if match.group("xsec_token"):
                    data = {"note_id": match.group("note_id")}

                    if match.group("xsec_token"):
                        data["xsec_token"] = match.group("xsec_token").strip().strip('\n')

                    if match.group("xsec_source"):
                        data["xsec_source"] = match.group("xsec_source").strip().strip('\n')

                    if data["note_id"] not in self._hash:
                        count += 1
                        note_data.append(data)
                        self._hash.add(data["note_id"])
                        self.progress.emit(count)

        logger.debug(f'本地导入文件采集笔记ID：{note_data}')
        self.finish.emit(note_data)

    def handle_toml(self):
        notes = []
        raw_authors = toml.load(self._filepath)['core']['authors']
        authors = [Author.from_dict(raw_author) for raw_author in raw_authors]
        count = 0
        for author in authors:
            temp_notes = author.notes.values()
            for note in temp_notes:
                count += 1
                note.set_author(author)
                notes.append(note)
                self.progress.emit(count)
        self.finish.emit(notes)


class ImportNote(QtWidgets.QDialog):
    imported = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ui = import_note_ui.Ui_ImportNote()
        self.ui.setupUi(self)
        self.build_interface()
        self.connect_ui_events()
        self.service_deployment()

    def build_interface(self):
        self.upload_notes = []
        self.success_notes = []
        self.failure_notes = []

        self.button_group = QtWidgets.QButtonGroup(self)
        self.button_group.addButton(self.ui.radioButton1, 1)
        self.button_group.addButton(self.ui.radioButton2, 2)
        self.button_group.button(1).setChecked(True)

    def connect_ui_events(self):
        self.ui.success_count_lcd.display(len(self.success_notes))
        self.ui.failure_count_lcd.display(len(self.failure_notes))
        self.ui.upload_file_btn.clicked.connect(self.handle_upload_file_click)
        self.ui.begin_import_btn.clicked.connect(self.handle_begin_import_click)

    def service_deployment(self):
        self.linked_user = LinkedUser.from_session()
        self.network_pool = NetworkPool(parent=self)
        self.network_pool.set_max_thread(6)
        self.network_pool.allTasksDone.connect(self.on_build_note_all_finish)
        self.success_mutex = QtCore.QMutex()
        self.failure_mutex = QtCore.QMutex()
        self.finished_mutex = QtCore.QMutex()

        self.upload_thread = UploadThread(parent=self)
        self.upload_thread.error.connect(self.on_upload_file_error)
        self.upload_thread.finish.connect(self.on_upload_file_finish)
        self.upload_thread.progress.connect(self.on_upload_count_progress)

    def on_upload_file_error(self, e):
        logger.exception(e)
        QtWidgets.QMessageBox.critical(self, '错误', '解析文件出错，请查看软件日志')

    def on_build_note_all_finish(self):
        self.ui.begin_import_btn.setEnabled(True)
        self.imported.emit(self.success_notes)
        self.close()

    def on_upload_file_finish(self, note_ids: list):
        self.upload_notes = note_ids

    def on_upload_count_progress(self, count: int):
        self.ui.upload_count_lcd.display(count)

    def handle_upload_file_click(self):
        self.ui.upload_file_btn.setEnabled(False)
        route_folder = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.DesktopLocation)
        if self.button_group.checkedId() == 1:
            filepath, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, "导入笔记文本 - toml", route_folder, "烤红薯笔记集 (*.toml)")
        else:
            filepath, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, "导入笔记文本 - txt", route_folder, "其他笔记文本 (*.txt)")

        if filepath:
            self.upload_thread.set_method(self.button_group.checkedId())
            self.upload_thread.set_filepath(filepath)
            self.upload_thread.start()

        self.ui.upload_file_btn.setEnabled(True)

    def handle_begin_import_click(self):
        if not self.upload_notes:
            QtWidgets.QMessageBox.critical(self, '导入错误', '请先上传文件并解析出笔记ID后，再点击导入按钮')
            return None

        self.ui.begin_import_btn.setEnabled(False)
        if self.button_group.checkedId() == 1:
            for note in self.upload_notes:
                if note:
                    self.success_notes.append(note)
                    self.ui.success_count_lcd.display(len(self.success_notes))
                else:
                    self.failure_notes.append(note)
                    self.ui.failure_count_lcd.display(len(self.failure_notes))
            self.on_build_note_all_finish()

        elif self.button_group.checkedId() == 2:
            for note_id in self.upload_notes:
                signals = self.network_pool.start_task(self.build_normal_note, note_id)
                signals.finished.connect(self.on_build_note_finished)

    def build_normal_note(self, note: dict):
        note_id = note.get('note_id')
        xsec_token = note.get('xsec_token')
        xsec_source = note.get('xsec_source')
        data = {'msg': f'笔记{note_id}的导入情况未知', 'note_id': note_id, 'xsec_token': xsec_token,
                'xsec_source': xsec_source}
        try:
            if not (note_id and xsec_token and xsec_source):
                raise ValueError('笔记属性并不齐全，必须具备 id、xsec_token、xsec_source')
            response = (xhs.API()
                        .set_cookies(self.linked_user.string_cookies)
                        .note_feed(note_id, xsec_token, xsec_source))
            items = response['data']['items']
            item = items[0] if items else None
            if item:
                note_id = item['id']
                note_title = item['note_card'].get('title', '无标题')
                note_type = NOTE_TYPES.get(item['note_card']['type'], '未知')
                user_id = item['note_card']['user']['user_id']
                nickname = item['note_card']['user']['nickname']
                author = Author(user_id, nickname)
                new_note = NormalNote(note_id, note_title, note_type, xsec_token, xsec_source)
                author.add_note(new_note)
                new_note.set_author(author)
                self.success_mutex.lock()
                self.success_notes.append(new_note)
                self.success_mutex.unlock()
                data = {
                    'msg': f'导入笔记{note_id}成功',
                    'note_id': note_id
                }
        except (KeyError, TypeError, ValueError, AttributeError):
            self.failure_mutex.lock()
            self.failure_notes.append(note_id)
            self.failure_mutex.unlock()

        return data

    def on_build_note_finished(self):
        self.finished_mutex.lock()
        self.ui.success_count_lcd.display(len(self.success_notes))
        self.ui.failure_count_lcd.display(len(self.failure_notes))
        self.finished_mutex.unlock()
