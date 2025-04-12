import re
import sys
import toml
from loguru import logger
from app.lib import QtWidgets, QtCore, QtGui
from app.lib.core import TomlBase, Unit, UnitState, PrivateUserCenter, ConfigCenter, Config, MigrateConfig, BackupConfig
from app.lib.globals import settings, app_name, threads, IMAGES_DIR, Path
from app.lib.threads import UpdateInfoThread, SaveAllLogsThread, stop_threads
from app.utils.string import validate_note_id, validate_web_session
from app.ui import main_window_ui
from app.view import (
    create_unit, unit_configer, user_manage, config_manage, edit_config, log_view, user_protocol, at_user_manage,
    import_note, stage_manage, note_manage, import_user,
    about_software, set_cookies, preload_view, train_account_settings
)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = main_window_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.preload_service()
        self.build_interface()
        self.connect_ui_events()
        self.service_deployment()

    def preload_service(self):
        preload_view_dialog = preload_view.PreloadView(self)
        preload_view_dialog.close.connect(self.on_preload_service_failure)
        preload_view_dialog.exec()

    def build_interface(self):
        self.setWindowTitle(f'{app_name} - 原作者已授权|禁止二卖')
        self.ui.action_create_unit.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'create_unit.svg')))
        self.ui.action_config_manage.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'config_manage.svg')))
        self.ui.action_create_config.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'create_config.svg')))
        self.ui.action_import_config.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'import_config.svg')))
        self.ui.action_user_manage.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'user_manage.svg')))
        self.ui.action_at_user_manage.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'at_user_manage.svg')))
        self.ui.action_import_user.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'import_user.svg')))
        self.ui.menu_basic_operate.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'basic_operate.svg')))
        self.ui.action_note_manage.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'note_manage.svg')))
        # self.ui.action_show_comments.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'display_comments.svg')))
        self.ui.action_edit_config.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'display_config.svg')))
        self.ui.action_stage_manage.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'stage_manage.svg')))
        self.ui.action_import_note.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'import_note.svg')))
        self.ui.menu_save_log.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'save_log.svg')))
        self.ui.action_terminal.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'stop.svg')))
        self.ui.action_pause.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'pause.svg')))
        self.ui.action_delete.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'delete.svg')))
        self.ui.action_user_protocol.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'user_protocol.svg')))
        self.ui.action_about_software.setIcon(QtGui.QIcon(str(IMAGES_DIR / 'about_software.svg')))

        self.collect_count_label = QtWidgets.QLabel('已采集：0 条')
        self.success_count_label = QtWidgets.QLabel('成功：0 条')
        self.failure_count_label = QtWidgets.QLabel('失败：0 条')
        self.uncomment_count_label = QtWidgets.QLabel('未评论：0 条')
        self.ui.statusbar.setStyleSheet('color: #555555')
        self.collect_count_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.collect_count_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                               QtWidgets.QSizePolicy.Policy.Minimum)
        self.success_count_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.success_count_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                               QtWidgets.QSizePolicy.Policy.Minimum)
        self.failure_count_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.failure_count_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                               QtWidgets.QSizePolicy.Policy.Minimum)
        self.uncomment_count_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.uncomment_count_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum,
                                                 QtWidgets.QSizePolicy.Policy.Minimum)
        self.ui.statusbar.addPermanentWidget(self.collect_count_label)
        self.ui.statusbar.addPermanentWidget(self.uncomment_count_label)
        self.ui.statusbar.addPermanentWidget(self.success_count_label)
        self.ui.statusbar.addPermanentWidget(self.failure_count_label)

        self.ui.action_set_debug.setVisible(True)

        self.reset_unit_button()

        if (not settings.value('gpa-khs-accept-protocol')
                or not settings.value('gpa-khs-accept-name')
                or not settings.value('gpa-khs-accept-date')):
            self.display_user_protocol_dialog(True)

        if not TomlBase.cookies:
            self.display_set_cookies_dialog(True)

        self.ui.action_set_debug.setChecked(bool(settings.value('is-debug')))
        self.ui.action_auto_rename.setChecked(TomlBase.auto_rename)

        menus = [self.ui.menu_M, self.ui.menu_E, self.ui.menu_F, self.ui.menu_S, self.ui.menu_H]
        for menu in menus:
            self.add_short_to_menu(self.ui.menubar, menu)

    def connect_ui_events(self):
        """
        连接 UI 相应的事件
        :return:
        """
        self.ui.tabBrowser.currentChanged.connect(self.handle_tab_browser_toggled)
        self.ui.toggleStateButton.clicked.connect(self.handle_toggle_state_click)
        self.ui.terminalButton.clicked.connect(self.handle_terminal_btn_click)
        self.ui.delete_unit_btn.clicked.connect(self.handle_delete_btn_click)
        self.ui.import_note_btn.clicked.connect(self.handle_import_note_click)
        self.ui.clearLogButton.clicked.connect(self.handle_clear_log_click)
        # menu Manage events
        create_unit_shortcut = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+C'), self)
        create_unit_shortcut.setContext(QtCore.Qt.ShortcutContext.WindowShortcut)
        create_unit_shortcut.activated.connect(self.display_create_unit_dialog)
        self.ui.action_create_unit.triggered.connect(self.display_create_unit_dialog)
        self.ui.action_config_manage.triggered.connect(self.display_config_manage_dialog)
        self.ui.action_create_config.triggered.connect(self.display_create_config_dialog)
        self.ui.action_import_config.triggered.connect(self.handle_import_config_click)
        self.ui.action_user_manage.triggered.connect(self.display_user_manage_dialog)
        self.ui.action_at_user_manage.triggered.connect(self.display_at_users_dialog)
        self.ui.action_import_user.triggered.connect(self.display_import_users_dialog)
        # menu Edit events
        toggle_state_shortcut = QtGui.QShortcut(QtCore.Qt.Key.Key_Space, self)
        toggle_state_shortcut.setContext(QtCore.Qt.ShortcutContext.WindowShortcut)
        toggle_state_shortcut.activated.connect(self.handle_toggle_state_click)
        self.ui.action_pause.triggered.connect(self.handle_toggle_state_click)
        terminal_state_shortcut = QtGui.QShortcut(QtGui.QKeySequence('Ctrl+D'), self)
        terminal_state_shortcut.setContext(QtCore.Qt.ShortcutContext.WindowShortcut)
        terminal_state_shortcut.activated.connect(self.handle_terminal_btn_click)
        self.ui.action_terminal.triggered.connect(self.handle_terminal_btn_click)
        self.ui.action_delete.triggered.connect(self.handle_delete_btn_click)
        self.ui.action_edit_config.triggered.connect(self.handle_edit_config_click)
        self.ui.action_stage_manage.triggered.connect(self.handle_stage_manage_click)
        self.ui.action_note_manage.triggered.connect(self.handle_note_manage_btn_click)
        self.ui.action_import_note.triggered.connect(self.handle_import_note_click)
        # menu File events
        self.ui.action_save_cur.triggered.connect(self.handle_save_cur_unit_log_click)
        self.ui.action_save_all.triggered.connect(self.handle_save_all_unit_log_click)
        self.ui.action_export_user.triggered.connect(self.handle_export_user_click)
        self.ui.action_export_config.triggered.connect(self.handle_export_config_click)
        self.ui.action_export_note.triggered.connect(self.handle_export_note_click)
        self.ui.action_migrate_config.triggered.connect(self.handle_migrate_config_click)
        self.ui.action_backup_config.triggered.connect(self.handle_backup_config_click)
        self.ui.action_resotre_config.triggered.connect(self.handle_restore_config_click)
        # menu Settings events
        self.ui.action_set_browser_path.triggered.connect(self.handle_set_browser_path_click)
        self.ui.action_train_settings.triggered.connect(self.handle_train_settings_click)
        self.ui.action_set_cookies.triggered.connect(lambda: self.display_set_cookies_dialog(False))
        self.ui.action_add_linked_user.triggered.connect(self.handle_add_linked_user_click)
        self.ui.action_set_check_after.triggered.connect(self.handle_set_check_after_click)
        self.ui.action_check_note.triggered.connect(self.handle_target_check_note_click)
        self.ui.action_auto_rename.triggered.connect(self.handle_auto_rename_toggle)
        self.ui.action_config_template.triggered.connect(self.display_edit_template_dialog)
        self.ui.action_set_debug.triggered.connect(self.handle_set_debug_click)
        # menu Help events
        self.ui.action_user_protocol.triggered.connect(lambda: self.display_user_protocol_dialog(False))
        self.ui.action_about_software.triggered.connect(self.handle_about_software_click)

    def service_deployment(self):
        """
        后台服务线程、进程的部署
        :return:
        """
        self.update_info_thread = UpdateInfoThread(parent=self)
        self.update_info_thread.send.connect(self.on_unit_info_send)
        self.update_info_thread.start()

    def reset_unit_button(self):
        self.ui.currentName.setText('--------')
        self.ui.import_note_btn.setVisible(False)
        self.ui.action_import_note.setEnabled(False)
        self.ui.delete_unit_btn.setVisible(False)
        self.ui.toggleStateButton.setVisible(False)
        self.ui.terminalButton.setVisible(False)
        self.ui.action_delete.setEnabled(False)
        self.ui.action_terminal.setEnabled(False)
        self.ui.action_pause.setEnabled(False)
        self.collect_count_label.setText('已采集：0 条')
        self.success_count_label.setText('成功：0 条')
        self.failure_count_label.setText('失败：0 条')
        self.uncomment_count_label.setText('未评论：0 条')

    def add_short_to_menu(self, menubar: QtWidgets.QMenuBar, menu: QtWidgets.QMenu):
        pattern = r"\(([A-Z])\)"
        match = re.search(pattern, menu.title())
        if match:
            key = match.group(1)
            menu_shortcut = QtGui.QShortcut(QtGui.QKeySequence(f'Ctrl+{key}'), self)
            menu_shortcut.setContext(QtCore.Qt.ShortcutContext.WindowShortcut)

            menu_shortcut.activated.connect(lambda: self.show_menu_bar(menubar, menu))

    @staticmethod
    def show_menu_bar(menubar: QtWidgets.QMenuBar, menu: QtWidgets.QMenu):
        # 获取菜单项在菜单栏中的位置
        menu_action = menu.menuAction()
        menu_geometry = menubar.actionGeometry(menu_action)
        menu_global_pos = menubar.mapToGlobal(
            QtCore.QPoint(menu_geometry.x(), menu_geometry.y() + menu_geometry.height()))

        # 让菜单显示在菜单项下方
        menu.exec(menu_global_pos)

    def on_preload_service_failure(self):
        QtWidgets.QMessageBox.critical(
            self,
            '加载错误',
            '预加载失败，原因可能如下：'
            '\n1.服务器已关闭，不可连接'
            '\n2.本地网络错误，连接网络有误'
            '\n2.服务器或者本地配置有误'
        )
        stop_threads()
        sys.exit(0)

    def on_unit_info_send(self, unit: Unit):
        self.ui.action_import_note.setEnabled(unit.is_wait_import)
        self.ui.import_note_btn.setVisible(unit.is_wait_import)
        self.update_unit_button_state(unit.state)
        state_color = UnitState.get_state_color(unit.state)
        state_html = f'<span style="color:{state_color.name()};">[{unit.state.description}]</span>'
        text = f'{unit.id}(阶段{unit.current_stage}：{unit.current_tasker.user.name}){state_html}'
        self.ui.currentName.setText(text)
        self.collect_count_label.setText(f'已采集：{len(unit.notes)} 条')
        self.uncomment_count_label.setText(f'未评论：{len(unit.uncomment_notes)} 条')
        self.success_count_label.setText(f'成功：{len(unit.success_notes)} 条')
        self.failure_count_label.setText(f'失败：{len(unit.failure_notes)} 条')

    def get_current_unit(self):
        current_widget = self.ui.tabBrowser.currentWidget()
        if isinstance(current_widget, log_view.LogView):
            unit = current_widget.unit
            if isinstance(unit, Unit):
                return unit
        return None

    def handle_tab_browser_toggled(self, index):
        current_widget = self.ui.tabBrowser.widget(index)
        if isinstance(current_widget, log_view.LogView):
            unit = current_widget.unit
            if isinstance(unit, Unit):
                self.update_info_thread.set_unit(unit)
                self.update_unit_button_state(unit.state)

    def update_unit_button_state(self, state):
        if state == UnitState.RUNNING:
            self.ui.toggleStateButton.setText('暂停')
            self.ui.action_pause.setText('暂停')
        elif state == UnitState.PAUSED:
            self.ui.toggleStateButton.setText('恢复')
            self.ui.action_pause.setText('恢复')

        self.ui.toggleStateButton.setVisible(state != UnitState.STOP)
        self.ui.terminalButton.setVisible(state != UnitState.STOP)
        self.ui.action_pause.setEnabled(state != UnitState.STOP)
        self.ui.action_terminal.setEnabled(state != UnitState.STOP)
        self.ui.delete_unit_btn.setVisible(state == UnitState.STOP)
        self.ui.action_delete.setEnabled(state == UnitState.STOP)

    def handle_toggle_state_click(self):
        """
        处理 暂停/恢复 按钮的单击事件
        :return:
        """
        unit = self.get_current_unit()
        if unit:
            if unit.state != UnitState.STOP and unit.state != UnitState.READY:
                if unit.state != UnitState.PAUSED:
                    unit.pause()
                elif unit.state != UnitState.RUNNING:
                    unit.resume()
                self.update_unit_button_state(unit.state)

    def handle_terminal_btn_click(self):
        """
        处理终止按钮的点击事件
        功能：负责当前 Unit 实例的状态以及同步界面
        :return:
        """
        unit = self.get_current_unit()
        if unit and unit.state != UnitState.STOP:
            unit.stop()
            self.update_unit_button_state(unit.state)

    def handle_delete_btn_click(self):
        """
        处理删除按钮的点击事件
        功能：负责销毁当前 Unit 实例与界面对象
        :return:
        """
        unit = self.get_current_unit()
        if unit and unit.state == UnitState.STOP:
            index = self.ui.tabBrowser.currentIndex()
            if index != -1:
                self.ui.tabBrowser.removeTab(index)
                threads.remove(unit)
                del unit

                if self.ui.tabBrowser.currentIndex() == -1:
                    self.reset_unit_button()
                    self.update_info_thread.set_unit(None)

    def handle_import_note_click(self):
        if self.ui.tabBrowser.currentIndex() == -1:
            QtWidgets.QMessageBox.critical(self, '操作失败', '当前不存在运行的单元，无法导入')
            return None

        unit = self.get_current_unit()
        if unit:
            if unit.is_wait_import:
                import_note_dialog = import_note.ImportNote(parent=self)
                import_note_dialog.imported.connect(self.on_import_note_imported)
                import_note_dialog.exec()
            else:
                QtWidgets.QMessageBox.critical(self, '操作失败', '当前单元不能中途导入笔记，请等待后续阶段提示再导入')
        else:
            QtWidgets.QMessageBox.critical(self, '操作失败', '当前日志窗口对接的单元不存在，无法导入')

    def on_import_note_imported(self, notes: list):
        unit = self.get_current_unit()
        if unit:
            unit.import_notes.extend(notes)
            unit.resume()

    def handle_clear_log_click(self):
        """
        处理清空日志按钮的单击
        :return:
        """
        current_widget = self.ui.tabBrowser.currentWidget()
        if isinstance(current_widget, log_view.LogView):
            current_widget.clear()

    def display_create_unit_dialog(self):
        create_unit_dialog = create_unit.CreateUnit(parent=self)
        create_unit_dialog.confirm.connect(self.on_create_unit_confirm)
        create_unit_dialog.exec()

    def on_create_unit_confirm(self, config, select_users):
        unit_configer_dialog = unit_configer.UnitConfiger(self, config, select_users)
        unit_configer_dialog.created.connect(self.on_config_unit_created)
        unit_configer_dialog.exec()

    def on_config_unit_created(self, unit: Unit):
        log_view_widget = unit.parent()
        if isinstance(log_view_widget, log_view.LogView):
            unit.insert_tabview(self.ui.tabBrowser)
            threads.append(unit)
            unit.start()

    def display_config_manage_dialog(self):
        config_manage_dialog = config_manage.ConfigManage(parent=self)
        config_manage_dialog.exec()

    def display_create_config_dialog(self):
        edit_config_dialog = edit_config.EditConfig(parent=self)
        edit_config_dialog.exec()

    def handle_import_config_click(self):
        desktop_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.DesktopLocation)
        save_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "导入配置", desktop_path, "配置集 (*.toml)")
        if save_file:
            if not Path(save_file).exists():
                QtWidgets.QMessageBox.critical(self, '错误', '选中的配置文件不存在')
            try:
                import_data = toml.load(save_file)
                import_configs = import_data['core']['configs']
                for config_dict in import_configs:
                    config = Config.from_dict(config_dict)
                    if config in ConfigCenter.data:
                        continue
                    ConfigCenter.data.append(config)
                ConfigCenter.save()
            except Exception as e:
                logger.exception(e)
                QtWidgets.QMessageBox.critical(self, '错误', '配置文件解析出错，请查看软件日志')

    def display_user_manage_dialog(self):
        user_manage_dialog = user_manage.UserManage(parent=self)
        user_manage_dialog.exec()

    def display_at_users_dialog(self):
        at_users_dialog = at_user_manage.AtUserManage(parent=self)
        at_users_dialog.exec()

    def display_import_users_dialog(self):
        import_user_dialog = import_user.ImportUser(parent=self)
        import_user_dialog.exec()

    def handle_edit_config_click(self):
        """
        处理编辑配置按钮的点击事件
        功能：编辑当前单元对应阶段的配置
        :return:
        """
        unit = self.get_current_unit()
        if unit:
            edit_config_dialog = edit_config.EditConfig(self, unit.current_tasker.config, edit_type='copy')
            edit_config_dialog.exec()
        else:
            QtWidgets.QMessageBox.critical(self, '操作失败', '当前不存在运行的单元，无法修改')

    def handle_stage_manage_click(self):
        unit = self.get_current_unit()
        if unit:
            stage_manage_dialog = stage_manage.StageManage(parent=self, unit=unit)
            stage_manage_dialog.exec()
        else:
            QtWidgets.QMessageBox.critical(self, '操作失败', '当前不存在运行的单元，无法获取阶段列表')

    def handle_note_manage_btn_click(self):
        """
        处理点击笔记管理的事件
        :return:
        """
        unit = self.get_current_unit()
        if unit:
            note_manage_dialog = note_manage.NoteManage(parent=self, unit=unit)
            note_manage_dialog.setWindowTitle('笔记列表 - 当前单元')
            note_manage_dialog.exec()
        else:
            QtWidgets.QMessageBox.critical(self, '操作失败', '当前不存在运行的单元，无法获取笔记列表')

    def handle_save_cur_unit_log_click(self):
        current_widget = self.ui.tabBrowser.currentWidget()
        if isinstance(current_widget, log_view.LogView):
            pain_logs = current_widget.pain_logs  # list[str]
            unit = current_widget.unit
            if isinstance(unit, Unit):
                desktop_path = QtCore.QStandardPaths.writableLocation(
                    QtCore.QStandardPaths.StandardLocation.DesktopLocation)
                filepath = Path(desktop_path) / f'{unit.id}.log'
                save_file, _ = QtWidgets.QFileDialog.getSaveFileName(self, "保存日志", str(filepath),
                                                                     "单元日志 (*.log)")

                if save_file:
                    try:
                        with open(save_file, 'w', encoding='utf-8') as f:
                            f.writelines(f'{log}\n' for log in pain_logs)
                        QtWidgets.QMessageBox.information(self, "成功", f"日志保存成功！\n{save_file}")
                    except Exception as e:
                        QtWidgets.QMessageBox.critical(self, "错误", f"保存日志失败：{str(e)}")
                return None

        QtWidgets.QMessageBox.critical(self, '保存失败', '当前不存在运行的单元')

    def handle_save_all_unit_log_click(self):
        if self.ui.tabBrowser.currentIndex() == -1:
            QtWidgets.QMessageBox.critical(self, "错误", "当前没有一个运行的单元！")
            return None

        save_thead = SaveAllLogsThread(self.ui.tabBrowser, parent=self)
        save_thead.success.connect(
            lambda: QtWidgets.QMessageBox.information(self, "成功", "所有单元日志保存成功！")
        )
        save_thead.error.connect(
            lambda e: QtWidgets.QMessageBox.critical(self, "错误", f"保存日志失败：{str(e)}"))
        threads.append(save_thead)
        save_thead.start()

    def handle_export_user_click(self):
        desktop_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.DesktopLocation)
        filepath = Path(desktop_path) / '许曰烤红薯-用户集.toml'
        save_file, _ = QtWidgets.QFileDialog.getSaveFileName(self, "导出用户", str(filepath), "用户集 (*.toml)")
        if save_file:
            data = {'core': {}}
            users = [user_obj.to_dict() for user_obj in PrivateUserCenter.data]
            data['core']['users'] = users
            with open(save_file, 'w', encoding='utf-8') as fw:
                toml.dump(data, fw)

    def handle_export_config_click(self):
        desktop_path = QtCore.QStandardPaths.writableLocation(QtCore.QStandardPaths.StandardLocation.DesktopLocation)
        filepath = Path(desktop_path) / '许曰烤红薯-配置集.toml'
        save_file, _ = QtWidgets.QFileDialog.getSaveFileName(self, "导出配置", str(filepath), "配置集 (*.toml)")
        if save_file:
            data = {'core': {}}
            configs = [config_obj.to_dict() for config_obj in ConfigCenter.data]
            data['core']['configs'] = configs
            with open(save_file, 'w', encoding='utf-8') as fw:
                toml.dump(data, fw)

    def handle_export_note_click(self):
        unit = self.get_current_unit()
        if unit:
            desktop_path = QtCore.QStandardPaths.writableLocation(
                QtCore.QStandardPaths.StandardLocation.DesktopLocation)
            filepath = Path(desktop_path) / '许曰烤红薯-笔记集.toml'
            save_file, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, "导出单元笔记", str(filepath), "笔记集 (*.toml)")
            if save_file:
                data = {'core': {}}
                authors = set([note.author for note in unit.notes])
                authors_dict = [author.to_dict() for author in authors]
                data['core']['authors'] = authors_dict
                with open(save_file, 'w', encoding='utf-8') as fw:
                    toml.dump(data, fw)
        else:
            QtWidgets.QMessageBox.critical(self, '错误', '当前不存在运行的单元，无法导出')

    def handle_migrate_config_click(self):
        migrate_config = MigrateConfig()
        if migrate_config.old_config_exist():
            btn = QtWidgets.QMessageBox.information(
                self, '发现旧配置',
                '当前检测到旧版本的.json配置文件，是否进行迁移到新版本',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
            if btn == QtWidgets.QMessageBox.StandardButton.Yes:
                result = migrate_config.migrate()
                if result:
                    QtWidgets.QMessageBox.information(self, '迁移成功', f'迁移成功\n> {str(migrate_config.new_path)}')
                else:
                    QtWidgets.QMessageBox.critical(self, '迁移失败', f'迁移失败\n{migrate_config.message}')
        else:
            QtWidgets.QMessageBox.critical(self, '未发现旧配置', '尚未检测到旧版本配置文件 ./config.json')

    def handle_backup_config_click(self):
        if BackupConfig.restore_path.exists():
            btn = QtWidgets.QMessageBox.information(
                self, '备份配置',
                '将备份当前配置，后缀名为.backup.toml',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
            if btn == QtWidgets.QMessageBox.StandardButton.Yes:
                result = BackupConfig.backup()
                if result:
                    QtWidgets.QMessageBox.information(self, '备份成功', f'备份成功\n> {str(BackupConfig.backup_path)}')
                else:
                    QtWidgets.QMessageBox.critical(self, '备份失败', '备份失败，可查看具体日志')
        else:
            QtWidgets.QMessageBox.critical(self, '操作失败', f'尚未检测到配置文件\n{str(BackupConfig.restore_path)}')

    def handle_restore_config_click(self):
        if BackupConfig.backup_path.exists():
            btn = QtWidgets.QMessageBox.information(
                self, '恢复配置',
                '将从备份的配置，恢复为当前软件所使用配置，恢复后需要重启方可生效',
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
            if btn == QtWidgets.QMessageBox.StandardButton.Yes:
                result = BackupConfig.restore()
                if result:
                    QtWidgets.QMessageBox.information(self, '恢复成功', '恢复成功，请重启软件加载配置')
                else:
                    QtWidgets.QMessageBox.critical(self, '恢复失败', '恢复失败，可查看具体日志')
        else:
            QtWidgets.QMessageBox.critical(self, '操作失败',
                                           f'尚未检测到已备份的配置文件\n{str(BackupConfig.backup_path)}')

    def handle_set_browser_path_click(self):
        btn = QtWidgets.QMessageBox.information(
            self, '设置浏览器路径',
            '请知悉，仅支持 Chrome 浏览器，导入其他浏览器导致程序异常由自己负责。'
            '点击 Yes 后，将进入 Chrome 程序的目录中，仅选择 `chrome.exe` 即可',
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        if btn == QtWidgets.QMessageBox.StandardButton.Yes:
            default_folder = r'C:\Program Files\Google\Chrome\Application'
            filepath, _ = QtWidgets.QFileDialog.getOpenFileName(
                self, "选择Chrome程序", default_folder, "chrome (*.exe)")
            if filepath:
                TomlBase.browser_path = filepath
                TomlBase.save()

    def handle_train_settings_click(self):
        train_setting_dialog = train_account_settings.TrainAccountSettings(parent=self)
        train_setting_dialog.exec()

    def display_set_cookies_dialog(self, is_load: bool):
        set_cookies_dialog = set_cookies.SetCookies(is_load, parent=self)
        set_cookies_dialog.exit.connect(self.on_base_cookies_invalid)
        set_cookies_dialog.exec()

    @staticmethod
    def on_base_cookies_invalid(is_load: bool):
        if not is_load:
            stop_threads()
        sys.exit(0)

    def handle_add_linked_user_click(self):
        session = TomlBase.linked_user_session
        session, ok = QtWidgets.QInputDialog.getText(
            self, "设置联动账号", "请输入有效的 web_session，用处很大！", text=session)
        session = session.strip()
        if ok and validate_web_session(session):
            TomlBase.linked_user_session = session
            TomlBase.save()

    def handle_set_check_after_click(self):
        current_value = TomlBase.after_check_seconds
        new_value, ok = QtWidgets.QInputDialog.getDouble(
            self, "设置耗时秒数",
            "该设置决定多少秒后去检测评论屏蔽情况（默认 6 秒）",
            value=current_value, minValue=3.0, maxValue=100.0, decimals=1, step=1.0)
        if ok:
            TomlBase.after_check_seconds = new_value
            TomlBase.save()

    def handle_target_check_note_click(self):
        note_id = TomlBase.target_note_id
        note_id, ok = QtWidgets.QInputDialog.getText(
            self, "设置目标检查笔记 ID", "该笔记 ID 用于用户管理中的评论情况检测", text=note_id)
        note_id = note_id.strip()
        if ok and validate_note_id(note_id):
            TomlBase.target_note_id = note_id
            TomlBase.save()

        note_xsec_token = TomlBase.target_note_xsec_token
        note_xsec_token, ok = QtWidgets.QInputDialog.getText(
            self, "设置目标检查笔记 Xsec Token", "该笔记 xsec_token 从 URL 链接中可得到", text=note_xsec_token)
        note_xsec_token = note_xsec_token.strip()
        if ok and note_xsec_token:
            TomlBase.target_note_xsec_token = note_xsec_token
            TomlBase.save()

    @staticmethod
    def handle_auto_rename_toggle(state):
        TomlBase.auto_rename = state
        TomlBase.save()

    def display_edit_template_dialog(self):
        edit_config_dialog = edit_config.EditConfig(self, edit_type='template')
        edit_config_dialog.exec()

    @staticmethod
    def handle_set_debug_click(state):
        settings.setValue('is-debug', int(state))

    def display_user_protocol_dialog(self, is_load):
        user_protocol_dialog = user_protocol.UserProtocol(is_load, parent=self)
        user_protocol_dialog.exit.connect(self.on_protocol_reject)
        user_protocol_dialog.exec()

    @staticmethod
    def on_protocol_reject(is_load: bool):
        if not is_load:
            for thread in threads:
                if thread.isRunning():
                    thread.stop()
        sys.exit(0)

    def handle_about_software_click(self):
        """
        点击关于软件的事件
        :return:
        """
        about_software_dialog = about_software.AboutSoftware(parent=self)
        about_software_dialog.exec()

    def closeEvent(self, event):
        result = QtWidgets.QMessageBox.warning(
            self,
            '退出程序',
            '您确认退出程序吗？',
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel
        )
        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            stop_threads()
            self.close()
        else:
            event.ignore()
