# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'manual_create_user_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_ManualCreateUser(object):
    def setupUi(self, ManualCreateUser):
        if not ManualCreateUser.objectName():
            ManualCreateUser.setObjectName(u"ManualCreateUser")
        ManualCreateUser.resize(405, 173)
        self.verticalLayout = QVBoxLayout(ManualCreateUser)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setVerticalSpacing(4)
        self.label_5 = QLabel(ManualCreateUser)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setTextFormat(Qt.MarkdownText)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_5)

        self.session_le = QLineEdit(ManualCreateUser)
        self.session_le.setObjectName(u"session_le")
        self.session_le.setMaxLength(1024)
        self.session_le.setEchoMode(QLineEdit.Normal)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.session_le)

        self.label_6 = QLabel(ManualCreateUser)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setTextFormat(Qt.MarkdownText)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_6)

        self.remark_te = QTextEdit(ManualCreateUser)
        self.remark_te.setObjectName(u"remark_te")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.remark_te)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_3)

        self.cancel_btn = QPushButton(ManualCreateUser)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.horizontalLayout_5.addWidget(self.cancel_btn)

        self.create_btn = QPushButton(ManualCreateUser)
        self.create_btn.setObjectName(u"create_btn")

        self.horizontalLayout_5.addWidget(self.create_btn)

        self.create_close_btn = QPushButton(ManualCreateUser)
        self.create_close_btn.setObjectName(u"create_close_btn")

        self.horizontalLayout_5.addWidget(self.create_close_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_5)


        self.retranslateUi(ManualCreateUser)

        QMetaObject.connectSlotsByName(ManualCreateUser)
    # setupUi

    def retranslateUi(self, ManualCreateUser):
        ManualCreateUser.setWindowTitle(QCoreApplication.translate("ManualCreateUser", u"\u624b\u52a8\u6dfb\u52a0\u8d26\u53f7", None))
        self.label_5.setText(QCoreApplication.translate("ManualCreateUser", u"**session**", None))
        self.session_le.setPlaceholderText(QCoreApplication.translate("ManualCreateUser", u"\u5fc5\u586b\uff1acookies \u4e2d\u7684 web session \u503c", None))
        self.label_6.setText(QCoreApplication.translate("ManualCreateUser", u"**\u529f\u80fd\u5907\u6ce8**", None))
        self.cancel_btn.setText(QCoreApplication.translate("ManualCreateUser", u"\u53d6\u6d88", None))
        self.create_btn.setText(QCoreApplication.translate("ManualCreateUser", u"\u6dfb\u52a0", None))
        self.create_close_btn.setText(QCoreApplication.translate("ManualCreateUser", u"\u6dfb\u52a0\u5e76\u5173\u95ed", None))
    # retranslateUi

