# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'train_account_settings_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_TrainAccountSettings(object):
    def setupUi(self, TrainAccountSettings):
        if not TrainAccountSettings.objectName():
            TrainAccountSettings.setObjectName(u"TrainAccountSettings")
        TrainAccountSettings.resize(326, 132)
        self.verticalLayout = QVBoxLayout(TrainAccountSettings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(TrainAccountSettings)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.preview_time_sp = QSpinBox(TrainAccountSettings)
        self.preview_time_sp.setObjectName(u"preview_time_sp")
        self.preview_time_sp.setMaximum(9999999)

        self.horizontalLayout.addWidget(self.preview_time_sp)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.random_like_note_cb = QCheckBox(TrainAccountSettings)
        self.random_like_note_cb.setObjectName(u"random_like_note_cb")

        self.horizontalLayout_2.addWidget(self.random_like_note_cb)

        self.random_collect_note_cb = QCheckBox(TrainAccountSettings)
        self.random_collect_note_cb.setObjectName(u"random_collect_note_cb")

        self.horizontalLayout_2.addWidget(self.random_collect_note_cb)

        self.random_share_note_cb = QCheckBox(TrainAccountSettings)
        self.random_share_note_cb.setObjectName(u"random_share_note_cb")

        self.horizontalLayout_2.addWidget(self.random_share_note_cb)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.random_like_comment_cb = QCheckBox(TrainAccountSettings)
        self.random_like_comment_cb.setObjectName(u"random_like_comment_cb")

        self.horizontalLayout_3.addWidget(self.random_like_comment_cb)

        self.random_follow_author_cb = QCheckBox(TrainAccountSettings)
        self.random_follow_author_cb.setObjectName(u"random_follow_author_cb")

        self.horizontalLayout_3.addWidget(self.random_follow_author_cb)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)

        self.cancel_btn = QPushButton(TrainAccountSettings)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.horizontalLayout_4.addWidget(self.cancel_btn)

        self.save_btn = QPushButton(TrainAccountSettings)
        self.save_btn.setObjectName(u"save_btn")

        self.horizontalLayout_4.addWidget(self.save_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_4)


        self.retranslateUi(TrainAccountSettings)

        QMetaObject.connectSlotsByName(TrainAccountSettings)
    # setupUi

    def retranslateUi(self, TrainAccountSettings):
        TrainAccountSettings.setWindowTitle(QCoreApplication.translate("TrainAccountSettings", u"\u517b\u53f7\u53c2\u6570\u8bbe\u7f6e", None))
        self.label.setText(QCoreApplication.translate("TrainAccountSettings", u"\u9884\u89c8\u7b14\u8bb0\u6700\u4f4e\u65f6\u95f4", None))
        self.preview_time_sp.setSuffix(QCoreApplication.translate("TrainAccountSettings", u" \u79d2", None))
        self.random_like_note_cb.setText(QCoreApplication.translate("TrainAccountSettings", u"\u968f\u673a\u70b9\u8d5e\u7b14\u8bb0", None))
        self.random_collect_note_cb.setText(QCoreApplication.translate("TrainAccountSettings", u"\u968f\u673a\u6536\u85cf\u7b14\u8bb0", None))
        self.random_share_note_cb.setText(QCoreApplication.translate("TrainAccountSettings", u"\u968f\u673a\u70b9\u51fb\u8f6c\u53d1", None))
        self.random_like_comment_cb.setText(QCoreApplication.translate("TrainAccountSettings", u"\u968f\u673a\u70b9\u8d5e\u8bc4\u8bba", None))
        self.random_follow_author_cb.setText(QCoreApplication.translate("TrainAccountSettings", u"\u968f\u673a\u5173\u6ce8\u4f5c\u8005", None))
        self.cancel_btn.setText(QCoreApplication.translate("TrainAccountSettings", u"\u53d6\u6d88", None))
        self.save_btn.setText(QCoreApplication.translate("TrainAccountSettings", u"\u4fdd\u5b58", None))
    # retranslateUi

