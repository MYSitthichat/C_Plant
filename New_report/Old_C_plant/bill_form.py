# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'generate_bill.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QMainWindow, QPushButton,
    QRadioButton, QSizePolicy, QStatusBar, QTreeWidget,
    QTreeWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(920, 518)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.treeWidget = QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setGeometry(QRect(0, 60, 761, 431))
        self.printPushButton = QPushButton(self.centralwidget)
        self.printPushButton.setObjectName(u"printPushButton")
        self.printPushButton.setGeometry(QRect(780, 70, 131, 51))
        self.reloadPushButton = QPushButton(self.centralwidget)
        self.reloadPushButton.setObjectName(u"reloadPushButton")
        self.reloadPushButton.setGeometry(QRect(780, 10, 131, 51))
        self.leanRadioButton = QRadioButton(self.centralwidget)
        self.leanRadioButton.setObjectName(u"leanRadioButton")
        self.leanRadioButton.setGeometry(QRect(250, 20, 101, 31))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(16)
        font.setBold(True)
        self.leanRadioButton.setFont(font)
        self.defaultRadioButton = QRadioButton(self.centralwidget)
        self.defaultRadioButton.setObjectName(u"defaultRadioButton")
        self.defaultRadioButton.setGeometry(QRect(10, 20, 191, 31))
        self.defaultRadioButton.setFont(font)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        ___qtreewidgetitem = self.treeWidget.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("MainWindow", u"order", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("MainWindow", u"customer name", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"date-time", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"order number", None));
        self.printPushButton.setText(QCoreApplication.translate("MainWindow", u"Print", None))
        self.reloadPushButton.setText(QCoreApplication.translate("MainWindow", u"Reload", None))
        self.leanRadioButton.setText(QCoreApplication.translate("MainWindow", u"\u0e40\u0e25\u0e37\u0e2d\u0e01 Lean", None))
        self.defaultRadioButton.setText(QCoreApplication.translate("MainWindow", u"\u0e40\u0e25\u0e37\u0e2d\u0e01\u0e1b\u0e23\u0e34\u0e49\u0e19\u0e41\u0e1a\u0e1a\u0e40\u0e1a\u0e37\u0e49\u0e2d\u0e07\u0e15\u0e49\u0e19", None))
    # retranslateUi

