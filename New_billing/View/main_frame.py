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
from PySide6.QtWidgets import (QApplication, QHeaderView, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QTreeWidget, QTreeWidgetItem,
    QWidget)

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
        QTreeWidgetItem(self.billing_treeWidget)
        QTreeWidgetItem(self.billing_treeWidget)
        QTreeWidgetItem(self.billing_treeWidget)
        self.billing_treeWidget.setObjectName(u"billing_treeWidget")
        self.billing_treeWidget.setGeometry(QRect(0, 50, 1250, 850))
        self.billing_treeWidget.setMinimumSize(QSize(1250, 850))
        self.billing_treeWidget.setMaximumSize(QSize(1300, 850))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(24)
        self.billing_treeWidget.setFont(font)
        self.billing_treeWidget.header().setDefaultSectionSize(300)
        self.print_pushButton = QPushButton(self.centralwidget)
        self.print_pushButton.setObjectName(u"print_pushButton")
        self.print_pushButton.setGeometry(QRect(1290, 120, 151, 61))
        self.print_pushButton.setFont(font)
        self.reload_pushButton = QPushButton(self.centralwidget)
        self.reload_pushButton.setObjectName(u"reload_pushButton")
        self.reload_pushButton.setGeometry(QRect(1290, 40, 151, 61))
        self.reload_pushButton.setFont(font)
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

        __sortingEnabled = self.billing_treeWidget.isSortingEnabled()
        self.billing_treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.billing_treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("Billing", u"1.0", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("Billing", u"aaaa", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Billing", u"2025/10/18 07:44:15", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Billing", u"1", None));
        ___qtreewidgetitem2 = self.billing_treeWidget.topLevelItem(1)
        ___qtreewidgetitem2.setText(3, QCoreApplication.translate("Billing", u"2.0", None));
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("Billing", u"bbb", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("Billing", u"2025/10/18 07:50:20", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Billing", u"2", None));
        ___qtreewidgetitem3 = self.billing_treeWidget.topLevelItem(2)
        ___qtreewidgetitem3.setText(3, QCoreApplication.translate("Billing", u"1.0", None));
        ___qtreewidgetitem3.setText(2, QCoreApplication.translate("Billing", u"cccc", None));
        ___qtreewidgetitem3.setText(1, QCoreApplication.translate("Billing", u"2025/10/18 07:58:06", None));
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("Billing", u"3", None));
        self.billing_treeWidget.setSortingEnabled(__sortingEnabled)

        self.print_pushButton.setText(QCoreApplication.translate("Billing", u"Print", None))
        self.reload_pushButton.setText(QCoreApplication.translate("Billing", u"Reload", None))
    # retranslateUi

