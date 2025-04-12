# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_user_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTextBrowser,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_ImportUsers(object):
    def setupUi(self, ImportUsers):
        if not ImportUsers.objectName():
            ImportUsers.setObjectName(u"ImportUsers")
        ImportUsers.resize(638, 435)
        self.verticalLayout = QVBoxLayout(ImportUsers)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(ImportUsers)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.cookies_te = QTextEdit(ImportUsers)
        self.cookies_te.setObjectName(u"cookies_te")

        self.verticalLayout_2.addWidget(self.cookies_te)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.line = QFrame(ImportUsers)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_2.addWidget(self.line)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label = QLabel(ImportUsers)
        self.label.setObjectName(u"label")

        self.verticalLayout_3.addWidget(self.label)

        self.logger = QTextBrowser(ImportUsers)
        self.logger.setObjectName(u"logger")
        self.logger.setFrameShape(QFrame.NoFrame)
        self.logger.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.logger)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.upload_btn = QPushButton(ImportUsers)
        self.upload_btn.setObjectName(u"upload_btn")

        self.horizontalLayout.addWidget(self.upload_btn)

        self.paste_btn = QPushButton(ImportUsers)
        self.paste_btn.setObjectName(u"paste_btn")

        self.horizontalLayout.addWidget(self.paste_btn)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.verify_btn = QPushButton(ImportUsers)
        self.verify_btn.setObjectName(u"verify_btn")

        self.horizontalLayout.addWidget(self.verify_btn)

        self.confirm_btn = QPushButton(ImportUsers)
        self.confirm_btn.setObjectName(u"confirm_btn")

        self.horizontalLayout.addWidget(self.confirm_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(ImportUsers)

        QMetaObject.connectSlotsByName(ImportUsers)
    # setupUi

    def retranslateUi(self, ImportUsers):
        ImportUsers.setWindowTitle(QCoreApplication.translate("ImportUsers", u"\u5bfc\u5165\u7528\u6237", None))
        self.label_2.setText(QCoreApplication.translate("ImportUsers", u"CK\u6587\u672c", None))
        self.label.setText(QCoreApplication.translate("ImportUsers", u"\u65e5\u5fd7\u6846", None))
        self.upload_btn.setText(QCoreApplication.translate("ImportUsers", u"\u5bfc\u5165\u6587\u4ef6", None))
        self.paste_btn.setText(QCoreApplication.translate("ImportUsers", u"\u70b9\u51fb\u7c98\u8d34", None))
        self.verify_btn.setText(QCoreApplication.translate("ImportUsers", u"\u9a8c\u8bc1", None))
        self.confirm_btn.setText(QCoreApplication.translate("ImportUsers", u"\u5bfc\u5165", None))
    # retranslateUi

