# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Report.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QSizePolicy,
    QStatusBar, QWidget)

class Ui_Report(object):
    def setupUi(self, Report):
        if not Report.objectName():
            Report.setObjectName(u"Report")
        Report.resize(1450, 800)
        self.centralwidget = QWidget(Report)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(430, 260, 721, 181))
        font = QFont()
        font.setPointSize(72)
        self.label.setFont(font)
        Report.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Report)
        self.statusbar.setObjectName(u"statusbar")
        Report.setStatusBar(self.statusbar)

        self.retranslateUi(Report)

        QMetaObject.connectSlotsByName(Report)
    # setupUi

    def retranslateUi(self, Report):
        Report.setWindowTitle(QCoreApplication.translate("Report", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("Report", u"Hello Report", None))
    # retranslateUi

