# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mobile_create_user_ui.ui'
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
    QTextEdit, QToolButton, QVBoxLayout, QWidget)

class Ui_MobileCreateUser(object):
    def setupUi(self, MobileCreateUser):
        if not MobileCreateUser.objectName():
            MobileCreateUser.setObjectName(u"MobileCreateUser")
        MobileCreateUser.resize(400, 186)
        self.verticalLayout = QVBoxLayout(MobileCreateUser)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(MobileCreateUser)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.zone_code_le = QLineEdit(MobileCreateUser)
        self.zone_code_le.setObjectName(u"zone_code_le")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zone_code_le.sizePolicy().hasHeightForWidth())
        self.zone_code_le.setSizePolicy(sizePolicy)
        self.zone_code_le.setMaximumSize(QSize(35, 16777215))
        self.zone_code_le.setMaxLength(32)

        self.horizontalLayout_2.addWidget(self.zone_code_le)

        self.phone_number_le = QLineEdit(MobileCreateUser)
        self.phone_number_le.setObjectName(u"phone_number_le")
        self.phone_number_le.setMaxLength(32)

        self.horizontalLayout_2.addWidget(self.phone_number_le)


        self.formLayout.setLayout(0, QFormLayout.FieldRole, self.horizontalLayout_2)

        self.label_2 = QLabel(MobileCreateUser)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.sms_code_le = QLineEdit(MobileCreateUser)
        self.sms_code_le.setObjectName(u"sms_code_le")
        self.sms_code_le.setMaxLength(32)

        self.horizontalLayout_3.addWidget(self.sms_code_le)

        self.get_code_btn = QToolButton(MobileCreateUser)
        self.get_code_btn.setObjectName(u"get_code_btn")

        self.horizontalLayout_3.addWidget(self.get_code_btn)


        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.horizontalLayout_3)

        self.label_3 = QLabel(MobileCreateUser)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.remark_te = QTextEdit(MobileCreateUser)
        self.remark_te.setObjectName(u"remark_te")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.remark_te)


        self.verticalLayout.addLayout(self.formLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.cancel_btn = QPushButton(MobileCreateUser)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.horizontalLayout.addWidget(self.cancel_btn)

        self.create_btn = QPushButton(MobileCreateUser)
        self.create_btn.setObjectName(u"create_btn")

        self.horizontalLayout.addWidget(self.create_btn)

        self.create_close_btn = QPushButton(MobileCreateUser)
        self.create_close_btn.setObjectName(u"create_close_btn")

        self.horizontalLayout.addWidget(self.create_close_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(MobileCreateUser)

        QMetaObject.connectSlotsByName(MobileCreateUser)
    # setupUi

    def retranslateUi(self, MobileCreateUser):
        MobileCreateUser.setWindowTitle(QCoreApplication.translate("MobileCreateUser", u"\u624b\u673a\u53f7\u767b\u5f55", None))
        self.label.setText(QCoreApplication.translate("MobileCreateUser", u"\u624b\u673a\u53f7\u7801", None))
        self.zone_code_le.setText(QCoreApplication.translate("MobileCreateUser", u"86", None))
        self.zone_code_le.setPlaceholderText(QCoreApplication.translate("MobileCreateUser", u"\u533a\u57df\u7801", None))
        self.phone_number_le.setPlaceholderText(QCoreApplication.translate("MobileCreateUser", u"\u7535\u8bdd\u53f7\u7801", None))
        self.label_2.setText(QCoreApplication.translate("MobileCreateUser", u"\u9a8c\u8bc1\u7801", None))
        self.sms_code_le.setPlaceholderText(QCoreApplication.translate("MobileCreateUser", u"\u586b\u5199\u77ed\u4fe1\u9a8c\u8bc1\u7801", None))
        self.get_code_btn.setText(QCoreApplication.translate("MobileCreateUser", u"\u53d1\u9001\u9a8c\u8bc1\u7801", None))
        self.label_3.setText(QCoreApplication.translate("MobileCreateUser", u"\u529f\u80fd\u5907\u6ce8", None))
        self.cancel_btn.setText(QCoreApplication.translate("MobileCreateUser", u"\u53d6\u6d88", None))
        self.create_btn.setText(QCoreApplication.translate("MobileCreateUser", u"\u6dfb\u52a0", None))
        self.create_close_btn.setText(QCoreApplication.translate("MobileCreateUser", u"\u6dfb\u52a0\u5e76\u5173\u95ed", None))
    # retranslateUi

