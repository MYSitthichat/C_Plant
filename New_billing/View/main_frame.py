# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'billing.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QTreeWidget, QTreeWidgetItem, QWidget)

class Ui_Billing(object):
    def setupUi(self, Billing):
        if not Billing.objectName():
            Billing.setObjectName(u"Billing")
        Billing.resize(1550, 850)
        Billing.setMinimumSize(QSize(1550, 850))
        Billing.setMaximumSize(QSize(1550, 850))
        self.centralwidget = QWidget(Billing)
        self.centralwidget.setObjectName(u"centralwidget")
        self.billing_treeWidget = QTreeWidget(self.centralwidget)
        self.billing_treeWidget.setObjectName(u"billing_treeWidget")
        self.billing_treeWidget.setGeometry(QRect(20, 160, 1500, 650))
        self.billing_treeWidget.setMinimumSize(QSize(1500, 650))
        self.billing_treeWidget.setMaximumSize(QSize(1500, 650))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(24)
        self.billing_treeWidget.setFont(font)
        self.billing_treeWidget.header().setDefaultSectionSize(300)
        self.print_pushButton = QPushButton(self.centralwidget)
        self.print_pushButton.setObjectName(u"print_pushButton")
        self.print_pushButton.setGeometry(QRect(850, 90, 151, 61))
        self.print_pushButton.setFont(font)
        self.reload_pushButton = QPushButton(self.centralwidget)
        self.reload_pushButton.setObjectName(u"reload_pushButton")
        self.reload_pushButton.setGeometry(QRect(850, 10, 151, 61))
        self.reload_pushButton.setFont(font)
        self.start_date_label = QLabel(self.centralwidget)
        self.start_date_label.setObjectName(u"start_date_label")
        self.start_date_label.setGeometry(QRect(10, 50, 91, 55))
        font1 = QFont()
        font1.setFamilies([u"TH Niramit AS"])
        font1.setPointSize(20)
        font1.setBold(True)
        self.start_date_label.setFont(font1)
        self.end_date_comboBox = QComboBox(self.centralwidget)
        self.end_date_comboBox.setObjectName(u"end_date_comboBox")
        self.end_date_comboBox.setGeometry(QRect(510, 60, 180, 30))
        self.start_date_comboBox = QComboBox(self.centralwidget)
        self.start_date_comboBox.setObjectName(u"start_date_comboBox")
        self.start_date_comboBox.setGeometry(QRect(130, 60, 180, 30))
        self.end_date_label = QLabel(self.centralwidget)
        self.end_date_label.setObjectName(u"end_date_label")
        self.end_date_label.setGeometry(QRect(370, 50, 85, 55))
        self.end_date_label.setFont(font1)
        self.select_date_label = QLabel(self.centralwidget)
        self.select_date_label.setObjectName(u"select_date_label")
        self.select_date_label.setGeometry(QRect(10, -10, 270, 55))
        self.select_date_label.setFont(font1)
        self.show_value_lineEdit = QLineEdit(self.centralwidget)
        self.show_value_lineEdit.setObjectName(u"show_value_lineEdit")
        self.show_value_lineEdit.setGeometry(QRect(190, 110, 281, 35))
        self.show_value_lineEdit.setFont(font1)
        self.show_value_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.show_value_list_label = QLabel(self.centralwidget)
        self.show_value_list_label.setObjectName(u"show_value_list_label")
        self.show_value_list_label.setGeometry(QRect(490, 100, 81, 61))
        self.show_value_list_label.setFont(font1)
        self.show_value_label = QLabel(self.centralwidget)
        self.show_value_label.setObjectName(u"show_value_label")
        self.show_value_label.setGeometry(QRect(10, 100, 151, 61))
        self.show_value_label.setFont(font1)
        Billing.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Billing)
        self.statusbar.setObjectName(u"statusbar")
        Billing.setStatusBar(self.statusbar)

        self.retranslateUi(Billing)

        QMetaObject.connectSlotsByName(Billing)
    # setupUi

    def retranslateUi(self, Billing):
        Billing.setWindowTitle(QCoreApplication.translate("Billing", u"Billing", None))
        ___qtreewidgetitem = self.billing_treeWidget.headerItem()
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Billing", u"order", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Billing", u"customer name", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Billing", u"date-time", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Billing", u"order number", None));
        self.print_pushButton.setText(QCoreApplication.translate("Billing", u"Print", None))
        self.reload_pushButton.setText(QCoreApplication.translate("Billing", u"Reload", None))
        self.start_date_label.setText(QCoreApplication.translate("Billing", u"\u0e27\u0e31\u0e19\u0e17\u0e35\u0e48\u0e40\u0e23\u0e34\u0e48\u0e21", None))
        self.end_date_label.setText(QCoreApplication.translate("Billing", u"\u0e16\u0e36\u0e07\u0e27\u0e31\u0e19\u0e17\u0e35\u0e48", None))
        self.select_date_label.setText(QCoreApplication.translate("Billing", u"\u0e40\u0e25\u0e37\u0e2d\u0e01\u0e27\u0e31\u0e19\u0e17\u0e35\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e01\u0e32\u0e23\u0e41\u0e2a\u0e14\u0e07\u0e1c\u0e25", None))
        self.show_value_list_label.setText(QCoreApplication.translate("Billing", u"\u0e23\u0e32\u0e22\u0e01\u0e32\u0e23", None))
        self.show_value_label.setText(QCoreApplication.translate("Billing", u"\u0e17\u0e31\u0e49\u0e07\u0e2b\u0e21\u0e14", None))
    # retranslateUi

