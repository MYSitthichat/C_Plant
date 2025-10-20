# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Report.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Report(object):
    def setupUi(self, Report):
        if not Report.objectName():
            Report.setObjectName(u"Report")
        Report.resize(1550, 850)
        Report.setMinimumSize(QSize(1550, 850))
        Report.setMaximumSize(QSize(1550, 850))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        Report.setFont(font)
        Report.setLocale(QLocale(QLocale.Thai, QLocale.Thailand))
        self.centralwidget = QWidget(Report)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(0, 0, 1550, 850))
        self.groupBox.setMinimumSize(QSize(1550, 850))
        self.groupBox.setMaximumSize(QSize(1550, 850))
        self.select_date_label = QLabel(self.groupBox)
        self.select_date_label.setObjectName(u"select_date_label")
        self.select_date_label.setGeometry(QRect(20, 20, 270, 55))
        font1 = QFont()
        font1.setFamilies([u"TH Niramit AS"])
        font1.setPointSize(20)
        font1.setBold(True)
        self.select_date_label.setFont(font1)
        self.start_date_label = QLabel(self.groupBox)
        self.start_date_label.setObjectName(u"start_date_label")
        self.start_date_label.setGeometry(QRect(20, 80, 91, 55))
        self.start_date_label.setFont(font1)
        self.show_value_label = QLabel(self.groupBox)
        self.show_value_label.setObjectName(u"show_value_label")
        self.show_value_label.setGeometry(QRect(20, 160, 151, 61))
        self.show_value_label.setFont(font1)
        self.start_date_comboBox = QComboBox(self.groupBox)
        self.start_date_comboBox.setObjectName(u"start_date_comboBox")
        self.start_date_comboBox.setGeometry(QRect(140, 90, 180, 30))
        self.end_date_label = QLabel(self.groupBox)
        self.end_date_label.setObjectName(u"end_date_label")
        self.end_date_label.setGeometry(QRect(380, 80, 85, 55))
        self.end_date_label.setFont(font1)
        self.show_value_list_label = QLabel(self.groupBox)
        self.show_value_list_label.setObjectName(u"show_value_list_label")
        self.show_value_list_label.setGeometry(QRect(500, 160, 81, 61))
        self.show_value_list_label.setFont(font1)
        self.end_date_comboBox = QComboBox(self.groupBox)
        self.end_date_comboBox.setObjectName(u"end_date_comboBox")
        self.end_date_comboBox.setGeometry(QRect(520, 90, 180, 30))
        self.show_pushButton = QPushButton(self.groupBox)
        self.show_pushButton.setObjectName(u"show_pushButton")
        self.show_pushButton.setGeometry(QRect(930, 140, 151, 61))
        self.show_pushButton.setFont(font1)
        self.export_pushButton = QPushButton(self.groupBox)
        self.export_pushButton.setObjectName(u"export_pushButton")
        self.export_pushButton.setGeometry(QRect(1120, 140, 151, 61))
        self.export_pushButton.setFont(font1)
        self.show_value_lineEdit = QLineEdit(self.groupBox)
        self.show_value_lineEdit.setObjectName(u"show_value_lineEdit")
        self.show_value_lineEdit.setGeometry(QRect(200, 170, 281, 35))
        self.show_value_lineEdit.setFont(font1)
        self.show_value_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.report_treeWidget = QTreeWidget(self.centralwidget)
        QTreeWidgetItem(self.report_treeWidget)
        QTreeWidgetItem(self.report_treeWidget)
        QTreeWidgetItem(self.report_treeWidget)
        self.report_treeWidget.setObjectName(u"report_treeWidget")
        self.report_treeWidget.setGeometry(QRect(10, 240, 1550, 850))
        self.report_treeWidget.setMinimumSize(QSize(1550, 850))
        self.report_treeWidget.setMaximumSize(QSize(1550, 850))
        self.report_treeWidget.setFont(font1)
        self.report_treeWidget.setAutoExpandDelay(3)
        self.report_treeWidget.setSortingEnabled(False)
        self.report_treeWidget.header().setVisible(True)
        self.report_treeWidget.header().setCascadingSectionResizes(False)
        self.report_treeWidget.header().setMinimumSectionSize(50)
        self.report_treeWidget.header().setDefaultSectionSize(160)
        self.report_treeWidget.header().setHighlightSections(False)
        self.report_treeWidget.header().setProperty(u"showSortIndicator", False)
        self.report_treeWidget.header().setStretchLastSection(True)
        Report.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Report)
        self.statusbar.setObjectName(u"statusbar")
        Report.setStatusBar(self.statusbar)

        self.retranslateUi(Report)

        QMetaObject.connectSlotsByName(Report)
    # setupUi

    def retranslateUi(self, Report):
        Report.setWindowTitle(QCoreApplication.translate("Report", u"\u0e04\u0e2d\u0e19\u0e01\u0e23\u0e35\u0e15\u0e1c\u0e2a\u0e21 \u0e2b\u0e49\u0e32\u0e07\u0e2b\u0e38\u0e49\u0e19\u0e2a\u0e48\u0e27\u0e19\u0e08\u0e33\u0e01\u0e31\u0e14 \u0e1b\u0e32\u0e19\u0e02\u0e1b\u0e23\u0e34\u0e0d \u0e04\u0e2d\u0e19\u0e01\u0e23\u0e35\u0e15", None))
        self.groupBox.setTitle("")
        self.select_date_label.setText(QCoreApplication.translate("Report", u"\u0e40\u0e25\u0e37\u0e2d\u0e01\u0e27\u0e31\u0e19\u0e17\u0e35\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e01\u0e32\u0e23\u0e41\u0e2a\u0e14\u0e07\u0e1c\u0e25", None))
        self.start_date_label.setText(QCoreApplication.translate("Report", u"\u0e27\u0e31\u0e19\u0e17\u0e35\u0e48\u0e40\u0e23\u0e34\u0e48\u0e21", None))
        self.show_value_label.setText(QCoreApplication.translate("Report", u"\u0e41\u0e2a\u0e14\u0e07\u0e04\u0e48\u0e32\u0e17\u0e31\u0e49\u0e07\u0e2b\u0e21\u0e14", None))
        self.end_date_label.setText(QCoreApplication.translate("Report", u"\u0e16\u0e36\u0e07\u0e27\u0e31\u0e19\u0e17\u0e35\u0e48", None))
        self.show_value_list_label.setText(QCoreApplication.translate("Report", u"\u0e23\u0e32\u0e22\u0e01\u0e32\u0e23", None))
        self.show_pushButton.setText(QCoreApplication.translate("Report", u"\u0e41\u0e2a\u0e14\u0e07\u0e1c\u0e25", None))
        self.export_pushButton.setText(QCoreApplication.translate("Report", u"\u0e2a\u0e48\u0e07\u0e04\u0e48\u0e32\u0e2d\u0e2d\u0e01", None))
        ___qtreewidgetitem = self.report_treeWidget.headerItem()
        ___qtreewidgetitem.setText(9, QCoreApplication.translate("Report", u"\u0e04\u0e27\u0e32\u0e21\u0e1c\u0e34\u0e14\u0e1e\u0e25\u0e32\u0e14", None));
        ___qtreewidgetitem.setText(8, QCoreApplication.translate("Report", u"\u0e0a\u0e31\u0e48\u0e07\u0e08\u0e23\u0e34\u0e07", None));
        ___qtreewidgetitem.setText(7, QCoreApplication.translate("Report", u"\u0e04\u0e48\u0e32\u0e17\u0e35\u0e48\u0e01\u0e33\u0e2b\u0e19\u0e14", None));
        ___qtreewidgetitem.setText(6, QCoreApplication.translate("Report", u"\u0e2a\u0e48\u0e27\u0e19\u0e1c\u0e2a\u0e21", None));
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("Report", u"\u0e08\u0e33\u0e19\u0e27\u0e19", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("Report", u"\u0e27\u0e31\u0e19\u0e17\u0e35\u0e48 \u0e40\u0e27\u0e25\u0e32", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Report", u"\u0e01\u0e33\u0e25\u0e31\u0e07\u0e2d\u0e31\u0e14", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Report", u"\u0e23\u0e32\u0e22\u0e25\u0e30\u0e40\u0e2d\u0e35\u0e22\u0e14\u0e01\u0e32\u0e23\u0e2a\u0e48\u0e07\u0e2a\u0e34\u0e19\u0e04\u0e49\u0e32", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Report", u"New Column", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Report", u"\u0e25\u0e33\u0e14\u0e31\u0e1a", None));

        __sortingEnabled = self.report_treeWidget.isSortingEnabled()
        self.report_treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.report_treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(9, QCoreApplication.translate("Report", u"0.27", None));
        ___qtreewidgetitem1.setText(8, QCoreApplication.translate("Report", u"752", None));
        ___qtreewidgetitem1.setText(7, QCoreApplication.translate("Report", u"750", None));
        ___qtreewidgetitem1.setText(6, QCoreApplication.translate("Report", u"\u0e17\u0e23\u0e32\u0e221", None));
        ___qtreewidgetitem1.setText(5, QCoreApplication.translate("Report", u"1.0", None));
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("Report", u"2025/10/18 04:45:18", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("Report", u"100ksc", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("Report", u"\u0e43\u0e15\u0e49\u0e15\u0e49\u0e19\u0e14\u0e2d\u0e01\u0e2a\u0e30\u0e40\u0e14\u0e32", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Report", u"\u0e15\u0e32\u0e19\u0e49\u0e2d\u0e22 \u0e1a\u0e38\u0e0d\u0e44\u0e21\u0e48\u0e22\u0e32\u0e27", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Report", u"3", None));
        ___qtreewidgetitem2 = self.report_treeWidget.topLevelItem(1)
        ___qtreewidgetitem2.setText(9, QCoreApplication.translate("Report", u"0.13", None));
        ___qtreewidgetitem2.setText(8, QCoreApplication.translate("Report", u"801", None));
        ___qtreewidgetitem2.setText(7, QCoreApplication.translate("Report", u"800", None));
        ___qtreewidgetitem2.setText(6, QCoreApplication.translate("Report", u"\u0e2b\u0e34\u0e192", None));
        ___qtreewidgetitem2.setText(5, QCoreApplication.translate("Report", u"2.0", None));
        ___qtreewidgetitem2.setText(4, QCoreApplication.translate("Report", u"2025/10/18 04:41:35", None));
        ___qtreewidgetitem2.setText(3, QCoreApplication.translate("Report", u"150ksc", None));
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("Report", u"\u0e1a\u0e49\u0e32\u0e19\u0e23\u0e31\u0e01\u0e22\u0e32\u0e22\u0e21\u0e35", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("Report", u"\u0e22\u0e32\u0e22\u0e21\u0e35 \u0e44\u0e21\u0e48\u0e21\u0e35\u0e2b\u0e21\u0e49\u0e2d", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Report", u"2", None));
        ___qtreewidgetitem3 = self.report_treeWidget.topLevelItem(2)
        ___qtreewidgetitem3.setText(9, QCoreApplication.translate("Report", u"-0.28", None));
        ___qtreewidgetitem3.setText(8, QCoreApplication.translate("Report", u"698", None));
        ___qtreewidgetitem3.setText(7, QCoreApplication.translate("Report", u"700", None));
        ___qtreewidgetitem3.setText(6, QCoreApplication.translate("Report", u"\u0e2b\u0e34\u0e19\u0e45", None));
        ___qtreewidgetitem3.setText(5, QCoreApplication.translate("Report", u"1.0", None));
        ___qtreewidgetitem3.setText(4, QCoreApplication.translate("Report", u"2025/10/18 04:37:12", None));
        ___qtreewidgetitem3.setText(3, QCoreApplication.translate("Report", u"100ksc", None));
        ___qtreewidgetitem3.setText(2, QCoreApplication.translate("Report", u"\u0e17\u0e35\u0e48\u0e40\u0e01\u0e48\u0e32\u0e40\u0e27\u0e25\u0e32\u0e40\u0e14\u0e34\u0e21", None));
        ___qtreewidgetitem3.setText(1, QCoreApplication.translate("Report", u"\u0e1b\u0e25\u0e32\u0e40\u0e01\u0e4b\u0e32 \u0e40\u0e21\u0e32\u0e22\u0e32\u0e14\u0e21", None));
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("Report", u"1", None));
        self.report_treeWidget.setSortingEnabled(__sortingEnabled)

    # retranslateUi

