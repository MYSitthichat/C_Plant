# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Control_plant.ui'
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

class Ui_Control_Plant(object):
    def setupUi(self, Control_Plant):
        if not Control_Plant.objectName():
            Control_Plant.setObjectName(u"Control_Plant")
        Control_Plant.resize(1450, 800)
        self.centralwidget = QWidget(Control_Plant)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(450, 270, 751, 141))
        font = QFont()
        font.setPointSize(72)
        self.label.setFont(font)
        Control_Plant.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Control_Plant)
        self.statusbar.setObjectName(u"statusbar")
        Control_Plant.setStatusBar(self.statusbar)

        self.retranslateUi(Control_Plant)

        QMetaObject.connectSlotsByName(Control_Plant)
    # setupUi

    def retranslateUi(self, Control_Plant):
        Control_Plant.setWindowTitle(QCoreApplication.translate("Control_Plant", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("Control_Plant", u"Hello Controll", None))
    # retranslateUi

