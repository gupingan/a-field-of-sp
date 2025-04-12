# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_note_ui.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_AddNote(object):
    def setupUi(self, AddNote):
        if not AddNote.objectName():
            AddNote.setObjectName(u"AddNote")
        AddNote.resize(345, 94)
        self.verticalLayout = QVBoxLayout(AddNote)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(AddNote)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.note_id_edit = QLineEdit(AddNote)
        self.note_id_edit.setObjectName(u"note_id_edit")

        self.verticalLayout_2.addWidget(self.note_id_edit)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.paste_btn = QPushButton(AddNote)
        self.paste_btn.setObjectName(u"paste_btn")

        self.horizontalLayout.addWidget(self.paste_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.cancel_btn = QPushButton(AddNote)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.horizontalLayout.addWidget(self.cancel_btn)

        self.confirm_btn = QPushButton(AddNote)
        self.confirm_btn.setObjectName(u"confirm_btn")

        self.horizontalLayout.addWidget(self.confirm_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(AddNote)

        QMetaObject.connectSlotsByName(AddNote)
    # setupUi

    def retranslateUi(self, AddNote):
        AddNote.setWindowTitle(QCoreApplication.translate("AddNote", u"\u6dfb\u52a0\u7b14\u8bb0", None))
        self.label.setText(QCoreApplication.translate("AddNote", u"\u8bf7\u7c98\u8d34\u7b14\u8bb0\u94fe\u63a5\u6216\u7b14\u8bb0\u7f16\u53f7", None))
        self.paste_btn.setText(QCoreApplication.translate("AddNote", u"\u7c98\u8d34", None))
        self.cancel_btn.setText(QCoreApplication.translate("AddNote", u"\u53d6\u6d88", None))
        self.confirm_btn.setText(QCoreApplication.translate("AddNote", u"\u786e\u8ba4", None))
    # retranslateUi

