# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_note_ui.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLCDNumber,
    QLabel, QPushButton, QRadioButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_ImportNote(object):
    def setupUi(self, ImportNote):
        if not ImportNote.objectName():
            ImportNote.setObjectName(u"ImportNote")
        ImportNote.resize(400, 138)
        self.verticalLayout = QVBoxLayout(ImportNote)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(ImportNote)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label)

        self.upload_count_lcd = QLCDNumber(ImportNote)
        self.upload_count_lcd.setObjectName(u"upload_count_lcd")
        self.upload_count_lcd.setSmallDecimalPoint(False)
        self.upload_count_lcd.setDigitCount(3)
        self.upload_count_lcd.setSegmentStyle(QLCDNumber.Flat)

        self.horizontalLayout_3.addWidget(self.upload_count_lcd)

        self.label_2 = QLabel(ImportNote)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label_2)

        self.success_count_lcd = QLCDNumber(ImportNote)
        self.success_count_lcd.setObjectName(u"success_count_lcd")
        self.success_count_lcd.setSmallDecimalPoint(False)
        self.success_count_lcd.setDigitCount(3)
        self.success_count_lcd.setSegmentStyle(QLCDNumber.Flat)

        self.horizontalLayout_3.addWidget(self.success_count_lcd)

        self.label_3 = QLabel(ImportNote)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.failure_count_lcd = QLCDNumber(ImportNote)
        self.failure_count_lcd.setObjectName(u"failure_count_lcd")
        self.failure_count_lcd.setSmallDecimalPoint(False)
        self.failure_count_lcd.setDigitCount(3)
        self.failure_count_lcd.setSegmentStyle(QLCDNumber.Flat)

        self.horizontalLayout_3.addWidget(self.failure_count_lcd)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.groupBox1 = QGroupBox(ImportNote)
        self.groupBox1.setObjectName(u"groupBox1")
        self.horizontalLayout = QHBoxLayout(self.groupBox1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.radioButton1 = QRadioButton(self.groupBox1)
        self.radioButton1.setObjectName(u"radioButton1")

        self.horizontalLayout.addWidget(self.radioButton1)

        self.radioButton2 = QRadioButton(self.groupBox1)
        self.radioButton2.setObjectName(u"radioButton2")

        self.horizontalLayout.addWidget(self.radioButton2)


        self.verticalLayout.addWidget(self.groupBox1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.upload_file_btn = QPushButton(ImportNote)
        self.upload_file_btn.setObjectName(u"upload_file_btn")

        self.horizontalLayout_2.addWidget(self.upload_file_btn)

        self.begin_import_btn = QPushButton(ImportNote)
        self.begin_import_btn.setObjectName(u"begin_import_btn")

        self.horizontalLayout_2.addWidget(self.begin_import_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(ImportNote)

        QMetaObject.connectSlotsByName(ImportNote)
    # setupUi

    def retranslateUi(self, ImportNote):
        ImportNote.setWindowTitle(QCoreApplication.translate("ImportNote", u"\u5bfc\u5165\u7b14\u8bb0", None))
        self.label.setText(QCoreApplication.translate("ImportNote", u"\u7b14\u8bb0\u603b\u6761\u6570", None))
        self.label_2.setText(QCoreApplication.translate("ImportNote", u"\u5bfc\u5165\u6210\u529f", None))
        self.label_3.setText(QCoreApplication.translate("ImportNote", u"\u5bfc\u5165\u5931\u8d25", None))
        self.groupBox1.setTitle(QCoreApplication.translate("ImportNote", u"\u539f\u6587\u4ef6\u7c7b\u578b", None))
        self.radioButton1.setText(QCoreApplication.translate("ImportNote", u"\u672c\u8f6f\u4ef6\u5bfc\u51fa\u7684 toml \u6587\u4ef6", None))
        self.radioButton2.setText(QCoreApplication.translate("ImportNote", u"\u7b14\u8bb0ID/\u7b14\u8bb0\u94fe\u63a5\u6bcf\u884c\u7684 txt \u6587\u4ef6", None))
        self.upload_file_btn.setText(QCoreApplication.translate("ImportNote", u"1. \u4e0a\u4f20\u6587\u4ef6", None))
        self.begin_import_btn.setText(QCoreApplication.translate("ImportNote", u"2. \u5f00\u59cb\u5bfc\u5165", None))
    # retranslateUi

