# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStatusBar, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(707, 424)
        self.action_create_unit = QAction(MainWindow)
        self.action_create_unit.setObjectName(u"action_create_unit")
        self.action_user_manage = QAction(MainWindow)
        self.action_user_manage.setObjectName(u"action_user_manage")
        self.action_pause = QAction(MainWindow)
        self.action_pause.setObjectName(u"action_pause")
        self.action_terminal = QAction(MainWindow)
        self.action_terminal.setObjectName(u"action_terminal")
        self.action_delete = QAction(MainWindow)
        self.action_delete.setObjectName(u"action_delete")
        self.action_edit_config = QAction(MainWindow)
        self.action_edit_config.setObjectName(u"action_edit_config")
        self.action_note_manage = QAction(MainWindow)
        self.action_note_manage.setObjectName(u"action_note_manage")
        self.action_save_cur = QAction(MainWindow)
        self.action_save_cur.setObjectName(u"action_save_cur")
        self.action_save_all = QAction(MainWindow)
        self.action_save_all.setObjectName(u"action_save_all")
        self.action_config_template = QAction(MainWindow)
        self.action_config_template.setObjectName(u"action_config_template")
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName(u"action_2")
        self.action_config_manage = QAction(MainWindow)
        self.action_config_manage.setObjectName(u"action_config_manage")
        self.action_create_config = QAction(MainWindow)
        self.action_create_config.setObjectName(u"action_create_config")
        self.action_stage_manage = QAction(MainWindow)
        self.action_stage_manage.setObjectName(u"action_stage_manage")
        self.action_set_debug = QAction(MainWindow)
        self.action_set_debug.setObjectName(u"action_set_debug")
        self.action_set_debug.setCheckable(True)
        self.action_set_debug.setEnabled(True)
        self.action_user_protocol = QAction(MainWindow)
        self.action_user_protocol.setObjectName(u"action_user_protocol")
        self.action_at_user_manage = QAction(MainWindow)
        self.action_at_user_manage.setObjectName(u"action_at_user_manage")
        self.action_import_note = QAction(MainWindow)
        self.action_import_note.setObjectName(u"action_import_note")
        self.action_import_user = QAction(MainWindow)
        self.action_import_user.setObjectName(u"action_import_user")
        self.action_add_linked_user = QAction(MainWindow)
        self.action_add_linked_user.setObjectName(u"action_add_linked_user")
        self.action_check_note = QAction(MainWindow)
        self.action_check_note.setObjectName(u"action_check_note")
        self.action_export_config = QAction(MainWindow)
        self.action_export_config.setObjectName(u"action_export_config")
        self.action_auto_rename = QAction(MainWindow)
        self.action_auto_rename.setObjectName(u"action_auto_rename")
        self.action_auto_rename.setCheckable(True)
        self.action_about_software = QAction(MainWindow)
        self.action_about_software.setObjectName(u"action_about_software")
        self.action_export_user = QAction(MainWindow)
        self.action_export_user.setObjectName(u"action_export_user")
        self.action_set_cookies = QAction(MainWindow)
        self.action_set_cookies.setObjectName(u"action_set_cookies")
        self.action_export_note = QAction(MainWindow)
        self.action_export_note.setObjectName(u"action_export_note")
        self.action_import_config = QAction(MainWindow)
        self.action_import_config.setObjectName(u"action_import_config")
        self.action_migrate_config = QAction(MainWindow)
        self.action_migrate_config.setObjectName(u"action_migrate_config")
        self.action_backup_config = QAction(MainWindow)
        self.action_backup_config.setObjectName(u"action_backup_config")
        self.action_resotre_config = QAction(MainWindow)
        self.action_resotre_config.setObjectName(u"action_resotre_config")
        self.action_set_browser_path = QAction(MainWindow)
        self.action_set_browser_path.setObjectName(u"action_set_browser_path")
        self.action_set_check_after = QAction(MainWindow)
        self.action_set_check_after.setObjectName(u"action_set_check_after")
        self.action_train_settings = QAction(MainWindow)
        self.action_train_settings.setObjectName(u"action_train_settings")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setTextFormat(Qt.MarkdownText)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_3.addWidget(self.label)

        self.currentName = QLabel(self.centralwidget)
        self.currentName.setObjectName(u"currentName")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.currentName.sizePolicy().hasHeightForWidth())
        self.currentName.setSizePolicy(sizePolicy1)
        self.currentName.setStyleSheet(u"")
        self.currentName.setTextFormat(Qt.AutoText)
        self.currentName.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.currentName.setWordWrap(True)

        self.horizontalLayout_3.addWidget(self.currentName)

        self.toggleStateButton = QPushButton(self.centralwidget)
        self.toggleStateButton.setObjectName(u"toggleStateButton")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.toggleStateButton.sizePolicy().hasHeightForWidth())
        self.toggleStateButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.toggleStateButton)

        self.terminalButton = QPushButton(self.centralwidget)
        self.terminalButton.setObjectName(u"terminalButton")
        sizePolicy2.setHeightForWidth(self.terminalButton.sizePolicy().hasHeightForWidth())
        self.terminalButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.terminalButton)

        self.delete_unit_btn = QPushButton(self.centralwidget)
        self.delete_unit_btn.setObjectName(u"delete_unit_btn")
        sizePolicy2.setHeightForWidth(self.delete_unit_btn.sizePolicy().hasHeightForWidth())
        self.delete_unit_btn.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.delete_unit_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.tabBrowser = QTabWidget(self.centralwidget)
        self.tabBrowser.setObjectName(u"tabBrowser")
        self.tabBrowser.setTabShape(QTabWidget.Rounded)
        self.tabBrowser.setDocumentMode(True)

        self.verticalLayout.addWidget(self.tabBrowser)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.import_note_btn = QPushButton(self.centralwidget)
        self.import_note_btn.setObjectName(u"import_note_btn")
        sizePolicy2.setHeightForWidth(self.import_note_btn.sizePolicy().hasHeightForWidth())
        self.import_note_btn.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.import_note_btn)

        self.clearLogButton = QPushButton(self.centralwidget)
        self.clearLogButton.setObjectName(u"clearLogButton")
        sizePolicy2.setHeightForWidth(self.clearLogButton.sizePolicy().hasHeightForWidth())
        self.clearLogButton.setSizePolicy(sizePolicy2)

        self.horizontalLayout_4.addWidget(self.clearLogButton)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 707, 22))
        self.menubar.setDefaultUp(False)
        self.menubar.setNativeMenuBar(True)
        self.menu_S = QMenu(self.menubar)
        self.menu_S.setObjectName(u"menu_S")
        self.menu_save_config = QMenu(self.menu_S)
        self.menu_save_config.setObjectName(u"menu_save_config")
        self.menu_H = QMenu(self.menubar)
        self.menu_H.setObjectName(u"menu_H")
        self.menu_F = QMenu(self.menubar)
        self.menu_F.setObjectName(u"menu_F")
        self.menu_save_log = QMenu(self.menu_F)
        self.menu_save_log.setObjectName(u"menu_save_log")
        self.menu_M = QMenu(self.menubar)
        self.menu_M.setObjectName(u"menu_M")
        self.menu_E = QMenu(self.menubar)
        self.menu_E.setObjectName(u"menu_E")
        self.menu_basic_operate = QMenu(self.menu_E)
        self.menu_basic_operate.setObjectName(u"menu_basic_operate")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_M.menuAction())
        self.menubar.addAction(self.menu_E.menuAction())
        self.menubar.addAction(self.menu_F.menuAction())
        self.menubar.addAction(self.menu_S.menuAction())
        self.menubar.addAction(self.menu_H.menuAction())
        self.menu_S.addAction(self.action_set_browser_path)
        self.menu_S.addAction(self.action_train_settings)
        self.menu_S.addAction(self.action_set_cookies)
        self.menu_S.addAction(self.action_add_linked_user)
        self.menu_S.addAction(self.action_set_check_after)
        self.menu_S.addAction(self.action_check_note)
        self.menu_S.addSeparator()
        self.menu_S.addAction(self.menu_save_config.menuAction())
        self.menu_S.addAction(self.action_config_template)
        self.menu_S.addAction(self.action_set_debug)
        self.menu_save_config.addAction(self.action_auto_rename)
        self.menu_H.addAction(self.action_user_protocol)
        self.menu_H.addAction(self.action_about_software)
        self.menu_F.addAction(self.menu_save_log.menuAction())
        self.menu_F.addSeparator()
        self.menu_F.addAction(self.action_export_config)
        self.menu_F.addAction(self.action_export_user)
        self.menu_F.addAction(self.action_export_note)
        self.menu_F.addSeparator()
        self.menu_F.addAction(self.action_migrate_config)
        self.menu_F.addAction(self.action_backup_config)
        self.menu_F.addAction(self.action_resotre_config)
        self.menu_save_log.addAction(self.action_save_cur)
        self.menu_save_log.addAction(self.action_save_all)
        self.menu_M.addAction(self.action_create_unit)
        self.menu_M.addSeparator()
        self.menu_M.addAction(self.action_config_manage)
        self.menu_M.addAction(self.action_create_config)
        self.menu_M.addAction(self.action_import_config)
        self.menu_M.addSeparator()
        self.menu_M.addAction(self.action_user_manage)
        self.menu_M.addAction(self.action_import_user)
        self.menu_M.addAction(self.action_at_user_manage)
        self.menu_E.addAction(self.menu_basic_operate.menuAction())
        self.menu_E.addSeparator()
        self.menu_E.addAction(self.action_edit_config)
        self.menu_E.addAction(self.action_stage_manage)
        self.menu_E.addSeparator()
        self.menu_E.addAction(self.action_note_manage)
        self.menu_E.addAction(self.action_import_note)
        self.menu_basic_operate.addAction(self.action_pause)
        self.menu_basic_operate.addAction(self.action_terminal)
        self.menu_basic_operate.addAction(self.action_delete)

        self.retranslateUi(MainWindow)

        self.tabBrowser.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u70e4\u7ea2\u85af", None))
        self.action_create_unit.setText(QCoreApplication.translate("MainWindow", u"\u521b\u5efa\u5355\u5143", None))
        self.action_user_manage.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u7ba1\u7406", None))
        self.action_pause.setText(QCoreApplication.translate("MainWindow", u"\u6682\u505c", None))
        self.action_terminal.setText(QCoreApplication.translate("MainWindow", u"\u7ec8\u6b62", None))
        self.action_delete.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664", None))
        self.action_edit_config.setText(QCoreApplication.translate("MainWindow", u"\u4fee\u6539\u914d\u7f6e", None))
        self.action_note_manage.setText(QCoreApplication.translate("MainWindow", u"\u7b14\u8bb0\u5217\u8868", None))
        self.action_save_cur.setText(QCoreApplication.translate("MainWindow", u"\u5f53\u524d\u5355\u5143", None))
        self.action_save_all.setText(QCoreApplication.translate("MainWindow", u"\u6240\u6709\u5355\u5143", None))
        self.action_config_template.setText(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91\u914d\u7f6e\u6a21\u677f", None))
        self.action_2.setText(QCoreApplication.translate("MainWindow", u"------", None))
        self.action_config_manage.setText(QCoreApplication.translate("MainWindow", u"\u914d\u7f6e\u7ba1\u7406", None))
        self.action_create_config.setText(QCoreApplication.translate("MainWindow", u"\u6dfb\u52a0\u914d\u7f6e", None))
        self.action_stage_manage.setText(QCoreApplication.translate("MainWindow", u"\u9636\u6bb5\u7ba1\u7406", None))
        self.action_set_debug.setText(QCoreApplication.translate("MainWindow", u"\u8c03\u8bd5\u6a21\u5f0f", None))
        self.action_user_protocol.setText(QCoreApplication.translate("MainWindow", u"\u7528\u6237\u534f\u8bae", None))
        self.action_at_user_manage.setText(QCoreApplication.translate("MainWindow", u"\u827e\u7279\u7528\u6237", None))
        self.action_import_note.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u7b14\u8bb0", None))
        self.action_import_user.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u7528\u6237", None))
        self.action_add_linked_user.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u8054\u52a8\u8d26\u53f7", None))
        self.action_check_note.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u68c0\u6d4b\u7b14\u8bb0", None))
        self.action_export_config.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u914d\u7f6e", None))
        self.action_auto_rename.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u667a\u80fd\u547d\u540d", None))
        self.action_about_software.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e\u8f6f\u4ef6", None))
        self.action_export_user.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u7528\u6237", None))
        self.action_set_cookies.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e\u73af\u5883CK", None))
        self.action_export_note.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u51fa\u5355\u5143\u7b14\u8bb0", None))
        self.action_import_config.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u914d\u7f6e", None))
        self.action_migrate_config.setText(QCoreApplication.translate("MainWindow", u"\u8f6f\u4ef6\u914d\u7f6e\u8fc1\u79fb", None))
        self.action_backup_config.setText(QCoreApplication.translate("MainWindow", u"\u5907\u4efd\u8f6f\u4ef6\u914d\u7f6e", None))
        self.action_resotre_config.setText(QCoreApplication.translate("MainWindow", u"\u6062\u590d\u8f6f\u4ef6\u914d\u7f6e", None))
        self.action_set_browser_path.setText(QCoreApplication.translate("MainWindow", u"\u6d4f\u89c8\u5668\u8def\u5f84", None))
        self.action_set_check_after.setText(QCoreApplication.translate("MainWindow", u"\u8017\u65f6\u68c0\u67e5\u5c4f\u853d", None))
        self.action_train_settings.setText(QCoreApplication.translate("MainWindow", u"\u517b\u53f7\u53c2\u6570\u8bbe\u7f6e", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"**\u6b63\u5728\u64cd\u4f5c**", None))
        self.currentName.setText(QCoreApplication.translate("MainWindow", u"--------", None))
        self.toggleStateButton.setText(QCoreApplication.translate("MainWindow", u"\u6682\u505c", None))
        self.terminalButton.setText(QCoreApplication.translate("MainWindow", u"\u7ec8\u6b62", None))
        self.delete_unit_btn.setText(QCoreApplication.translate("MainWindow", u"\u5220\u9664", None))
        self.import_note_btn.setText(QCoreApplication.translate("MainWindow", u"\u5bfc\u5165\u7b14\u8bb0", None))
        self.clearLogButton.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7a7a\u65e5\u5fd7", None))
        self.menu_S.setTitle(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e(S)", None))
        self.menu_save_config.setTitle(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u914d\u7f6e", None))
        self.menu_H.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9(H)", None))
        self.menu_F.setTitle(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6(F)", None))
        self.menu_save_log.setTitle(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u65e5\u5fd7", None))
        self.menu_M.setTitle(QCoreApplication.translate("MainWindow", u"\u7ba1\u7406(M)", None))
        self.menu_E.setTitle(QCoreApplication.translate("MainWindow", u"\u7f16\u8f91(E)", None))
        self.menu_basic_operate.setTitle(QCoreApplication.translate("MainWindow", u"\u57fa\u672c\u64cd\u4f5c", None))
    # retranslateUi

