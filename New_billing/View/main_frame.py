# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'billing.ui'
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

class Ui_Billing(object):
    def setupUi(self, Billing):
        if not Billing.objectName():
            Billing.setObjectName(u"Billing")
        Billing.resize(1450, 800)
        self.centralwidget = QWidget(Billing)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(460, 250, 541, 191))
        font = QFont()
        font.setPointSize(72)
        self.label.setFont(font)
        Billing.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Billing)
        self.statusbar.setObjectName(u"statusbar")
        Billing.setStatusBar(self.statusbar)

        self.retranslateUi(Billing)

        QMetaObject.connectSlotsByName(Billing)
    # setupUi

    def retranslateUi(self, Billing):
        Billing.setWindowTitle(QCoreApplication.translate("Billing", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("Billing", u"HIiiii", None))
    # retranslateUi

