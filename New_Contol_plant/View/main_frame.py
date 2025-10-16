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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QFrame,
    QGroupBox, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QTextEdit, QTreeWidget, QTreeWidgetItem,
    QWidget)

class Ui_Control_Plant(object):
    def setupUi(self, Control_Plant):
        if not Control_Plant.objectName():
            Control_Plant.setObjectName(u"Control_Plant")
        Control_Plant.resize(1550, 850)
        Control_Plant.setMinimumSize(QSize(1550, 850))
        Control_Plant.setMaximumSize(QSize(1550, 871))
        Control_Plant.setSizeIncrement(QSize(1550, 850))
        Control_Plant.setBaseSize(QSize(1550, 850))
        self.centralwidget = QWidget(Control_Plant)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setMinimumSize(QSize(1550, 850))
        self.centralwidget.setMaximumSize(QSize(1550, 850))
        self.centralwidget.setSizeIncrement(QSize(1550, 850))
        self.centralwidget.setBaseSize(QSize(1550, 850))
        self.centralwidget.setStyleSheet(u"background:rgb(255, 244, 235)")
        self.main_tab = QTabWidget(self.centralwidget)
        self.main_tab.setObjectName(u"main_tab")
        self.main_tab.setGeometry(QRect(-10, 0, 1561, 831))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(24)
        font.setBold(True)
        self.main_tab.setFont(font)
        self.main_tab.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.main_tab.setIconSize(QSize(20, 20))
        self.register_tab = QWidget()
        self.register_tab.setObjectName(u"register_tab")
        self.reg_formula_treeWidget = QTreeWidget(self.register_tab)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setTextAlignment(11, Qt.AlignCenter);
        __qtreewidgetitem.setFont(11, font);
        __qtreewidgetitem.setTextAlignment(10, Qt.AlignCenter);
        __qtreewidgetitem.setFont(10, font);
        __qtreewidgetitem.setTextAlignment(9, Qt.AlignCenter);
        __qtreewidgetitem.setFont(9, font);
        __qtreewidgetitem.setTextAlignment(8, Qt.AlignCenter);
        __qtreewidgetitem.setFont(8, font);
        __qtreewidgetitem.setTextAlignment(7, Qt.AlignCenter);
        __qtreewidgetitem.setFont(7, font);
        __qtreewidgetitem.setTextAlignment(6, Qt.AlignCenter);
        __qtreewidgetitem.setFont(6, font);
        __qtreewidgetitem.setTextAlignment(5, Qt.AlignCenter);
        __qtreewidgetitem.setFont(5, font);
        __qtreewidgetitem.setTextAlignment(4, Qt.AlignCenter);
        __qtreewidgetitem.setFont(4, font);
        __qtreewidgetitem.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem.setFont(3, font);
        __qtreewidgetitem.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem.setFont(2, font);
        __qtreewidgetitem.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem.setFont(1, font);
        __qtreewidgetitem.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem.setFont(0, font);
        self.reg_formula_treeWidget.setHeaderItem(__qtreewidgetitem)
        __qtreewidgetitem1 = QTreeWidgetItem(self.reg_formula_treeWidget)
        __qtreewidgetitem1.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem1.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem1.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem1.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem2 = QTreeWidgetItem(self.reg_formula_treeWidget)
        __qtreewidgetitem2.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem2.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem2.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem2.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem3 = QTreeWidgetItem(self.reg_formula_treeWidget)
        __qtreewidgetitem3.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem3.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem3.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem3.setTextAlignment(0, Qt.AlignCenter);
        self.reg_formula_treeWidget.setObjectName(u"reg_formula_treeWidget")
        self.reg_formula_treeWidget.setGeometry(QRect(10, 430, 1545, 350))
        self.reg_formula_treeWidget.setMinimumSize(QSize(1545, 350))
        self.reg_formula_treeWidget.setMaximumSize(QSize(1545, 350))
        self.reg_formula_treeWidget.setSizeIncrement(QSize(0, 0))
        self.reg_formula_treeWidget.setBaseSize(QSize(0, 0))
        self.reg_formula_treeWidget.setFont(font)
        self.reg_formula_treeWidget.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_formula_treeWidget.setFrameShadow(QFrame.Shadow.Raised)
        self.reg_formula_treeWidget.setLineWidth(1)
        self.reg_formula_treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.reg_formula_treeWidget.setAutoExpandDelay(3)
        self.reg_formula_treeWidget.setItemsExpandable(True)
        self.reg_formula_treeWidget.setSortingEnabled(True)
        self.reg_formula_treeWidget.setAnimated(False)
        self.reg_formula_treeWidget.setAllColumnsShowFocus(False)
        self.reg_formula_treeWidget.setWordWrap(False)
        self.reg_formula_treeWidget.setExpandsOnDoubleClick(False)
        self.reg_formula_treeWidget.setColumnCount(12)
        self.reg_formula_treeWidget.header().setMinimumSectionSize(50)
        self.reg_formula_treeWidget.header().setDefaultSectionSize(123)
        self.reg_name_label = QLabel(self.register_tab)
        self.reg_name_label.setObjectName(u"reg_name_label")
        self.reg_name_label.setGeometry(QRect(20, 10, 41, 41))
        self.reg_name_label.setFont(font)
        self.reg_name_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_name_lineEdit = QLineEdit(self.register_tab)
        self.reg_name_lineEdit.setObjectName(u"reg_name_lineEdit")
        self.reg_name_lineEdit.setGeometry(QRect(70, 5, 181, 41))
        font1 = QFont()
        font1.setFamilies([u"TH Niramit AS"])
        font1.setPointSize(22)
        font1.setBold(True)
        self.reg_name_lineEdit.setFont(font1)
        self.reg_name_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_name_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reg_telephone_label = QLabel(self.register_tab)
        self.reg_telephone_label.setObjectName(u"reg_telephone_label")
        self.reg_telephone_label.setGeometry(QRect(260, 10, 61, 41))
        self.reg_telephone_label.setFont(font)
        self.reg_telephone_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_telephone_lineEdit = QLineEdit(self.register_tab)
        self.reg_telephone_lineEdit.setObjectName(u"reg_telephone_lineEdit")
        self.reg_telephone_lineEdit.setGeometry(QRect(330, 5, 201, 41))
        self.reg_telephone_lineEdit.setFont(font1)
        self.reg_telephone_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_telephone_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reg_address_label = QLabel(self.register_tab)
        self.reg_address_label.setObjectName(u"reg_address_label")
        self.reg_address_label.setGeometry(QRect(20, 60, 51, 41))
        self.reg_address_label.setFont(font)
        self.reg_address_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_address_textEdit = QTextEdit(self.register_tab)
        self.reg_address_textEdit.setObjectName(u"reg_address_textEdit")
        self.reg_address_textEdit.setGeometry(QRect(70, 60, 461, 141))
        self.reg_address_textEdit.setFont(font1)
        self.reg_address_textEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_number_car_lineEdit = QLineEdit(self.register_tab)
        self.reg_number_car_lineEdit.setObjectName(u"reg_number_car_lineEdit")
        self.reg_number_car_lineEdit.setGeometry(QRect(130, 210, 181, 41))
        self.reg_number_car_lineEdit.setFont(font1)
        self.reg_number_car_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_number_car_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reg_number_car_label = QLabel(self.register_tab)
        self.reg_number_car_label.setObjectName(u"reg_number_car_label")
        self.reg_number_car_label.setGeometry(QRect(20, 210, 111, 41))
        self.reg_number_car_label.setFont(font)
        self.reg_number_car_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_comment_label = QLabel(self.register_tab)
        self.reg_comment_label.setObjectName(u"reg_comment_label")
        self.reg_comment_label.setGeometry(QRect(20, 260, 111, 41))
        self.reg_comment_label.setFont(font)
        self.reg_comment_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_comment_textEdit = QTextEdit(self.register_tab)
        self.reg_comment_textEdit.setObjectName(u"reg_comment_textEdit")
        self.reg_comment_textEdit.setGeometry(QRect(130, 270, 401, 131))
        self.reg_comment_textEdit.setFont(font1)
        self.reg_comment_textEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.groupBox = QGroupBox(self.register_tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 0, 811, 421))
        self.reg_formula_comboBox = QComboBox(self.groupBox)
        self.reg_formula_comboBox.addItem("")
        self.reg_formula_comboBox.addItem("")
        self.reg_formula_comboBox.setObjectName(u"reg_formula_comboBox")
        self.reg_formula_comboBox.setGeometry(QRect(620, 5, 171, 41))
        self.reg_formula_comboBox.setFont(font)
        self.reg_formula_comboBox.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_formula_label = QLabel(self.groupBox)
        self.reg_formula_label.setObjectName(u"reg_formula_label")
        self.reg_formula_label.setGeometry(QRect(540, 10, 71, 41))
        self.reg_formula_label.setFont(font)
        self.reg_formula_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_amount_unit_lineEdit = QLineEdit(self.groupBox)
        self.reg_amount_unit_lineEdit.setObjectName(u"reg_amount_unit_lineEdit")
        self.reg_amount_unit_lineEdit.setGeometry(QRect(620, 60, 131, 41))
        self.reg_amount_unit_lineEdit.setFont(font1)
        self.reg_amount_unit_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_amount_unit_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reg_amount_unit_label = QLabel(self.groupBox)
        self.reg_amount_unit_label.setObjectName(u"reg_amount_unit_label")
        self.reg_amount_unit_label.setGeometry(QRect(540, 65, 71, 41))
        self.reg_amount_unit_label.setFont(font)
        self.reg_amount_unit_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_amount_unit_label1 = QLabel(self.groupBox)
        self.reg_amount_unit_label1.setObjectName(u"reg_amount_unit_label1")
        self.reg_amount_unit_label1.setGeometry(QRect(760, 60, 41, 41))
        self.reg_amount_unit_label1.setFont(font)
        self.reg_amount_unit_label1.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_amount_unit_label_2 = QLabel(self.groupBox)
        self.reg_amount_unit_label_2.setObjectName(u"reg_amount_unit_label_2")
        self.reg_amount_unit_label_2.setGeometry(QRect(540, 115, 71, 41))
        self.reg_amount_unit_label_2.setFont(font)
        self.reg_amount_unit_label_2.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_amount_unit_lineEdit_2 = QLineEdit(self.groupBox)
        self.reg_amount_unit_lineEdit_2.setObjectName(u"reg_amount_unit_lineEdit_2")
        self.reg_amount_unit_lineEdit_2.setGeometry(QRect(620, 110, 131, 41))
        self.reg_amount_unit_lineEdit_2.setFont(font1)
        self.reg_amount_unit_lineEdit_2.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_amount_unit_lineEdit_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reg_save_pushButton = QPushButton(self.groupBox)
        self.reg_save_pushButton.setObjectName(u"reg_save_pushButton")
        self.reg_save_pushButton.setGeometry(QRect(530, 180, 271, 61))
        self.reg_save_pushButton.setFont(font)
        self.reg_save_pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color:rgb(156, 255, 181); \n"
"    color: black;\n"
"    border: 2px solid #3498DB; \n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 218, 1); \n"
"    border-color: #5DADE2;  \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 148, 22);\n"
"    border-color: #2874A6;\n"
"}")
        self.reg_clear_pushButton = QPushButton(self.groupBox)
        self.reg_clear_pushButton.setObjectName(u"reg_clear_pushButton")
        self.reg_clear_pushButton.setGeometry(QRect(530, 260, 271, 61))
        self.reg_clear_pushButton.setFont(font)
        self.reg_clear_pushButton.setStyleSheet(u"\n"
"QPushButton {\n"
"   	background:rgb(64, 255, 214);\n"
"    color: black;\n"
"    border: 2px solid #3498DB; \n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 218, 1); \n"
"    border-color: #5DADE2;  \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 148, 22);\n"
"    border-color: #2874A6;\n"
"}")
        self.reg_save_new_custommer_pushButton = QPushButton(self.groupBox)
        self.reg_save_new_custommer_pushButton.setObjectName(u"reg_save_new_custommer_pushButton")
        self.reg_save_new_custommer_pushButton.setGeometry(QRect(530, 340, 271, 61))
        self.reg_save_new_custommer_pushButton.setFont(font)
        self.reg_save_new_custommer_pushButton.setStyleSheet(u"QPushButton {\n"
"   	background:rgb(255, 167, 173);\n"
"    color: black;\n"
"    border: 2px solid #3498DB; \n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 218, 1); \n"
"    border-color: #5DADE2;  \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 148, 22);\n"
"    border-color: #2874A6;\n"
"}")
        self.reg_list_customer_treeWidget = QTreeWidget(self.register_tab)
        __qtreewidgetitem4 = QTreeWidgetItem()
        __qtreewidgetitem4.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem4.setFont(2, font);
        __qtreewidgetitem4.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem4.setFont(1, font);
        __qtreewidgetitem4.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem4.setFont(0, font);
        self.reg_list_customer_treeWidget.setHeaderItem(__qtreewidgetitem4)
        __qtreewidgetitem5 = QTreeWidgetItem(self.reg_list_customer_treeWidget)
        __qtreewidgetitem5.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem5.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem5.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem6 = QTreeWidgetItem(self.reg_list_customer_treeWidget)
        __qtreewidgetitem6.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem6.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem6.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem7 = QTreeWidgetItem(self.reg_list_customer_treeWidget)
        __qtreewidgetitem7.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem7.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem7.setTextAlignment(0, Qt.AlignCenter);
        self.reg_list_customer_treeWidget.setObjectName(u"reg_list_customer_treeWidget")
        self.reg_list_customer_treeWidget.setGeometry(QRect(830, 60, 725, 360))
        self.reg_list_customer_treeWidget.setMinimumSize(QSize(725, 360))
        self.reg_list_customer_treeWidget.setMaximumSize(QSize(725, 360))
        self.reg_list_customer_treeWidget.setSizeIncrement(QSize(0, 0))
        self.reg_list_customer_treeWidget.setBaseSize(QSize(0, 0))
        self.reg_list_customer_treeWidget.setFont(font)
        self.reg_list_customer_treeWidget.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_list_customer_treeWidget.setFrameShadow(QFrame.Shadow.Raised)
        self.reg_list_customer_treeWidget.setLineWidth(1)
        self.reg_list_customer_treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.reg_list_customer_treeWidget.setAutoExpandDelay(3)
        self.reg_list_customer_treeWidget.setItemsExpandable(True)
        self.reg_list_customer_treeWidget.setSortingEnabled(True)
        self.reg_list_customer_treeWidget.setAnimated(False)
        self.reg_list_customer_treeWidget.setAllColumnsShowFocus(False)
        self.reg_list_customer_treeWidget.setWordWrap(False)
        self.reg_list_customer_treeWidget.setExpandsOnDoubleClick(False)
        self.reg_list_customer_treeWidget.setColumnCount(3)
        self.reg_list_customer_treeWidget.header().setMinimumSectionSize(50)
        self.reg_list_customer_treeWidget.header().setDefaultSectionSize(123)
        self.reg_lis_custommer_label = QLabel(self.register_tab)
        self.reg_lis_custommer_label.setObjectName(u"reg_lis_custommer_label")
        self.reg_lis_custommer_label.setGeometry(QRect(1150, 10, 131, 41))
        self.reg_lis_custommer_label.setFont(font)
        self.reg_lis_custommer_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.main_tab.addTab(self.register_tab, "")
        self.groupBox.raise_()
        self.reg_formula_treeWidget.raise_()
        self.reg_name_label.raise_()
        self.reg_name_lineEdit.raise_()
        self.reg_telephone_label.raise_()
        self.reg_telephone_lineEdit.raise_()
        self.reg_address_label.raise_()
        self.reg_address_textEdit.raise_()
        self.reg_number_car_lineEdit.raise_()
        self.reg_number_car_label.raise_()
        self.reg_comment_label.raise_()
        self.reg_comment_textEdit.raise_()
        self.reg_list_customer_treeWidget.raise_()
        self.reg_lis_custommer_label.raise_()
        self.Mix_tab = QWidget()
        self.Mix_tab.setObjectName(u"Mix_tab")
        self.main_tab.addTab(self.Mix_tab, "")
        self.formula_tab = QWidget()
        self.formula_tab.setObjectName(u"formula_tab")
        self.for_formula_treeWidget = QTreeWidget(self.formula_tab)
        __qtreewidgetitem8 = QTreeWidgetItem()
        __qtreewidgetitem8.setTextAlignment(11, Qt.AlignCenter);
        __qtreewidgetitem8.setFont(11, font);
        __qtreewidgetitem8.setTextAlignment(10, Qt.AlignCenter);
        __qtreewidgetitem8.setFont(10, font);
        __qtreewidgetitem8.setTextAlignment(9, Qt.AlignCenter);
        __qtreewidgetitem8.setFont(9, font);
        __qtreewidgetitem8.setTextAlignment(8, Qt.AlignCenter);
        __qtreewidgetitem8.setFont(8, font);
        __qtreewidgetitem8.setTextAlignment(7, Qt.AlignCenter);
        __qtreewidgetitem8.setFont(7, font);
        __qtreewidgetitem8.setTextAlignment(6, Qt.AlignCenter);
        __qtreewidgetitem8.setFont(6, font);
        __qtreewidgetitem8.setTextAlignment(5, Qt.AlignCenter);
        __qtreewidgetitem8.setFont(5, font);
        __qtreewidgetitem8.setTextAlignment(4, Qt.AlignCenter);
        __qtreewidgetitem8.setFont(4, font);
        __qtreewidgetitem8.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem8.setFont(3, font);
        __qtreewidgetitem8.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem8.setFont(2, font);
        __qtreewidgetitem8.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem8.setFont(1, font);
        __qtreewidgetitem8.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem8.setFont(0, font);
        self.for_formula_treeWidget.setHeaderItem(__qtreewidgetitem8)
        __qtreewidgetitem9 = QTreeWidgetItem(self.for_formula_treeWidget)
        __qtreewidgetitem9.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem9.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem9.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem9.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem10 = QTreeWidgetItem(self.for_formula_treeWidget)
        __qtreewidgetitem10.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem10.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem10.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem10.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem11 = QTreeWidgetItem(self.for_formula_treeWidget)
        __qtreewidgetitem11.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem11.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem11.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem11.setTextAlignment(0, Qt.AlignCenter);
        self.for_formula_treeWidget.setObjectName(u"for_formula_treeWidget")
        self.for_formula_treeWidget.setGeometry(QRect(10, 0, 1545, 510))
        self.for_formula_treeWidget.setMinimumSize(QSize(1545, 510))
        self.for_formula_treeWidget.setMaximumSize(QSize(1545, 510))
        self.for_formula_treeWidget.setSizeIncrement(QSize(0, 0))
        self.for_formula_treeWidget.setBaseSize(QSize(0, 0))
        self.for_formula_treeWidget.setFont(font)
        self.for_formula_treeWidget.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.for_formula_treeWidget.setFrameShadow(QFrame.Shadow.Raised)
        self.for_formula_treeWidget.setLineWidth(1)
        self.for_formula_treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.for_formula_treeWidget.setAutoExpandDelay(3)
        self.for_formula_treeWidget.setItemsExpandable(True)
        self.for_formula_treeWidget.setSortingEnabled(True)
        self.for_formula_treeWidget.setAnimated(False)
        self.for_formula_treeWidget.setAllColumnsShowFocus(False)
        self.for_formula_treeWidget.setWordWrap(False)
        self.for_formula_treeWidget.setExpandsOnDoubleClick(False)
        self.for_formula_treeWidget.setColumnCount(12)
        self.for_formula_treeWidget.header().setMinimumSectionSize(50)
        self.for_formula_treeWidget.header().setDefaultSectionSize(123)
        self.for_config_formula_groupBox = QGroupBox(self.formula_tab)
        self.for_config_formula_groupBox.setObjectName(u"for_config_formula_groupBox")
        self.for_config_formula_groupBox.setGeometry(QRect(20, 520, 1531, 151))
        self.for_config_formula_groupBox.setFont(font)
        self.for_config_formula_groupBox.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.for_config_formula_groupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.for_config_formula_groupBox.setFlat(False)
        self.for_config_formula_groupBox.setCheckable(False)
        self.for_id_formula_label = QLabel(self.for_config_formula_groupBox)
        self.for_id_formula_label.setObjectName(u"for_id_formula_label")
        self.for_id_formula_label.setGeometry(QRect(30, 40, 61, 41))
        self.for_id_formula_label.setFont(font)
        self.for_id_formula_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.for_name_formula_label = QLabel(self.for_config_formula_groupBox)
        self.for_name_formula_label.setObjectName(u"for_name_formula_label")
        self.for_name_formula_label.setGeometry(QRect(140, 40, 81, 41))
        self.for_name_formula_label.setFont(font)
        self.for_name_formula_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.for_id_formula_lineEdit = QLineEdit(self.for_config_formula_groupBox)
        self.for_id_formula_lineEdit.setObjectName(u"for_id_formula_lineEdit")
        self.for_id_formula_lineEdit.setGeometry(QRect(10, 90, 91, 41))
        self.for_id_formula_lineEdit.setFont(font1)
        self.for_id_formula_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.for_id_formula_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.for_name_formula_lineEdit = QLineEdit(self.for_config_formula_groupBox)
        self.for_name_formula_lineEdit.setObjectName(u"for_name_formula_lineEdit")
        self.for_name_formula_lineEdit.setGeometry(QRect(110, 90, 131, 41))
        self.for_name_formula_lineEdit.setFont(font1)
        self.for_name_formula_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.for_name_formula_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.for_rock_1_label = QLabel(self.for_config_formula_groupBox)
        self.for_rock_1_label.setObjectName(u"for_rock_1_label")
        self.for_rock_1_label.setGeometry(QRect(280, 40, 51, 41))
        self.for_rock_1_label.setFont(font)
        self.for_rock_1_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.for_sand_label = QLabel(self.for_config_formula_groupBox)
        self.for_sand_label.setObjectName(u"for_sand_label")
        self.for_sand_label.setGeometry(QRect(385, 40, 71, 41))
        self.for_sand_label.setFont(font)
        self.for_sand_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.for_rock_2_label = QLabel(self.for_config_formula_groupBox)
        self.for_rock_2_label.setObjectName(u"for_rock_2_label")
        self.for_rock_2_label.setGeometry(QRect(510, 40, 71, 41))
        self.for_rock_2_label.setFont(font)
        self.for_rock_2_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.for_fyash_label = QLabel(self.for_config_formula_groupBox)
        self.for_fyash_label.setObjectName(u"for_fyash_label")
        self.for_fyash_label.setGeometry(QRect(625, 40, 91, 41))
        self.for_fyash_label.setFont(font)
        self.for_fyash_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.for_cement_label = QLabel(self.for_config_formula_groupBox)
        self.for_cement_label.setObjectName(u"for_cement_label")
        self.for_cement_label.setGeometry(QRect(780, 40, 41, 41))
        self.for_cement_label.setFont(font)
        self.for_cement_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.for_wather_label = QLabel(self.for_config_formula_groupBox)
        self.for_wather_label.setObjectName(u"for_wather_label")
        self.for_wather_label.setGeometry(QRect(895, 40, 41, 41))
        self.for_wather_label.setFont(font)
        self.for_wather_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.for_chem_1_label = QLabel(self.for_config_formula_groupBox)
        self.for_chem_1_label.setObjectName(u"for_chem_1_label")
        self.for_chem_1_label.setGeometry(QRect(990, 40, 121, 41))
        self.for_chem_1_label.setFont(font)
        self.for_chem_1_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.for_chem_2_label = QLabel(self.for_config_formula_groupBox)
        self.for_chem_2_label.setObjectName(u"for_chem_2_label")
        self.for_chem_2_label.setGeometry(QRect(1120, 40, 121, 41))
        self.for_chem_2_label.setFont(font)
        self.for_chem_2_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.for_age_label = QLabel(self.for_config_formula_groupBox)
        self.for_age_label.setObjectName(u"for_age_label")
        self.for_age_label.setGeometry(QRect(1290, 40, 51, 41))
        self.for_age_label.setFont(font)
        self.for_age_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.for_slump_label = QLabel(self.for_config_formula_groupBox)
        self.for_slump_label.setObjectName(u"for_slump_label")
        self.for_slump_label.setGeometry(QRect(1420, 40, 81, 41))
        self.for_slump_label.setFont(font)
        self.for_slump_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.for_rock_1_lineEdit_3 = QLineEdit(self.for_config_formula_groupBox)
        self.for_rock_1_lineEdit_3.setObjectName(u"for_rock_1_lineEdit_3")
        self.for_rock_1_lineEdit_3.setGeometry(QRect(250, 90, 101, 41))
        self.for_rock_1_lineEdit_3.setFont(font1)
        self.for_rock_1_lineEdit_3.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.for_rock_1_lineEdit_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.for_sand_lineEdit = QLineEdit(self.for_config_formula_groupBox)
        self.for_sand_lineEdit.setObjectName(u"for_sand_lineEdit")
        self.for_sand_lineEdit.setGeometry(QRect(360, 90, 111, 41))
        self.for_sand_lineEdit.setFont(font1)
        self.for_sand_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.for_sand_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.for_rock_2_lineEdit = QLineEdit(self.for_config_formula_groupBox)
        self.for_rock_2_lineEdit.setObjectName(u"for_rock_2_lineEdit")
        self.for_rock_2_lineEdit.setGeometry(QRect(480, 90, 111, 41))
        self.for_rock_2_lineEdit.setFont(font1)
        self.for_rock_2_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.for_rock_2_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.for_fyash_lineEdit = QLineEdit(self.for_config_formula_groupBox)
        self.for_fyash_lineEdit.setObjectName(u"for_fyash_lineEdit")
        self.for_fyash_lineEdit.setGeometry(QRect(600, 90, 131, 41))
        self.for_fyash_lineEdit.setFont(font1)
        self.for_fyash_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.for_fyash_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.for_cement_lineEdit = QLineEdit(self.for_config_formula_groupBox)
        self.for_cement_lineEdit.setObjectName(u"for_cement_lineEdit")
        self.for_cement_lineEdit.setGeometry(QRect(740, 90, 111, 41))
        self.for_cement_lineEdit.setFont(font1)
        self.for_cement_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.for_cement_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.for_wather_lineEdit = QLineEdit(self.for_config_formula_groupBox)
        self.for_wather_lineEdit.setObjectName(u"for_wather_lineEdit")
        self.for_wather_lineEdit.setGeometry(QRect(860, 90, 111, 41))
        self.for_wather_lineEdit.setFont(font1)
        self.for_wather_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.for_wather_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.for_chem_1_lineEdit = QLineEdit(self.for_config_formula_groupBox)
        self.for_chem_1_lineEdit.setObjectName(u"for_chem_1_lineEdit")
        self.for_chem_1_lineEdit.setGeometry(QRect(980, 90, 121, 41))
        self.for_chem_1_lineEdit.setFont(font1)
        self.for_chem_1_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.for_chem_1_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.for_chem_2_lineEdit = QLineEdit(self.for_config_formula_groupBox)
        self.for_chem_2_lineEdit.setObjectName(u"for_chem_2_lineEdit")
        self.for_chem_2_lineEdit.setGeometry(QRect(1110, 90, 131, 41))
        self.for_chem_2_lineEdit.setFont(font1)
        self.for_chem_2_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.for_chem_2_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.for_age_lineEdit = QLineEdit(self.for_config_formula_groupBox)
        self.for_age_lineEdit.setObjectName(u"for_age_lineEdit")
        self.for_age_lineEdit.setGeometry(QRect(1250, 90, 131, 41))
        self.for_age_lineEdit.setFont(font1)
        self.for_age_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.for_age_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.for_slump_lineEdit = QLineEdit(self.for_config_formula_groupBox)
        self.for_slump_lineEdit.setObjectName(u"for_slump_lineEdit")
        self.for_slump_lineEdit.setGeometry(QRect(1390, 90, 131, 41))
        self.for_slump_lineEdit.setFont(font1)
        self.for_slump_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.for_slump_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.for_add_formula_pushButton = QPushButton(self.formula_tab)
        self.for_add_formula_pushButton.setObjectName(u"for_add_formula_pushButton")
        self.for_add_formula_pushButton.setGeometry(QRect(20, 680, 241, 81))
        self.for_add_formula_pushButton.setFont(font)
        self.for_add_formula_pushButton.setStyleSheet(u"QPushButton {\n"
"   	background:rgb(148, 212, 255);\n"
"    color: black;\n"
"    border: 2px solid #3498DB; \n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 218, 1); \n"
"    border-color: #5DADE2;  \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 148, 22);\n"
"    border-color: #2874A6;\n"
"}")
        self.for_config_formula_pushButton = QPushButton(self.formula_tab)
        self.for_config_formula_pushButton.setObjectName(u"for_config_formula_pushButton")
        self.for_config_formula_pushButton.setGeometry(QRect(270, 680, 241, 81))
        self.for_config_formula_pushButton.setFont(font)
        self.for_config_formula_pushButton.setStyleSheet(u"\n"
"QPushButton {\n"
"   	background:rgb(255, 211, 107);\n"
"    color: black;\n"
"    border: 2px solid #3498DB; \n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 218, 1); \n"
"    border-color: #5DADE2;  \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 148, 22);\n"
"    border-color: #2874A6;\n"
"}")
        self.for_delete_formula_pushButton = QPushButton(self.formula_tab)
        self.for_delete_formula_pushButton.setObjectName(u"for_delete_formula_pushButton")
        self.for_delete_formula_pushButton.setGeometry(QRect(520, 680, 241, 81))
        self.for_delete_formula_pushButton.setFont(font)
        self.for_delete_formula_pushButton.setStyleSheet(u"\n"
"QPushButton {\n"
"   	background:rgb(255, 102, 105);\n"
"    color: black;\n"
"    border: 2px solid #3498DB; \n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 218, 1); \n"
"    border-color: #5DADE2;  \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 148, 22);\n"
"    border-color: #2874A6;\n"
"}")
        self.for_save_formula_pushButton = QPushButton(self.formula_tab)
        self.for_save_formula_pushButton.setObjectName(u"for_save_formula_pushButton")
        self.for_save_formula_pushButton.setGeometry(QRect(770, 680, 241, 81))
        self.for_save_formula_pushButton.setFont(font)
        self.for_save_formula_pushButton.setStyleSheet(u"\n"
"QPushButton {\n"
"   	background:rgb(121, 218, 94);\n"
"    color: black;\n"
"    border: 2px solid #3498DB; \n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 218, 1); \n"
"    border-color: #5DADE2;  \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 148, 22);\n"
"    border-color: #2874A6;\n"
"}")
        self.for_cancel_pushButton = QPushButton(self.formula_tab)
        self.for_cancel_pushButton.setObjectName(u"for_cancel_pushButton")
        self.for_cancel_pushButton.setGeometry(QRect(1310, 680, 241, 81))
        self.for_cancel_pushButton.setFont(font)
        self.for_cancel_pushButton.setStyleSheet(u"QPushButton {\n"
"   	background:rgb(145, 145, 145);\n"
"    color: black;\n"
"    border: 2px solid #3498DB; \n"
"    border-radius: 5px;\n"
"    padding: 8px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(52, 218, 1); \n"
"    border-color: #5DADE2;  \n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background-color: rgb(0, 148, 22);\n"
"    border-color: #2874A6;\n"
"}")
        self.main_tab.addTab(self.formula_tab, "")
        Control_Plant.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Control_Plant)
        self.statusbar.setObjectName(u"statusbar")
        Control_Plant.setStatusBar(self.statusbar)

        self.retranslateUi(Control_Plant)

        self.main_tab.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(Control_Plant)
    # setupUi

    def retranslateUi(self, Control_Plant):
        Control_Plant.setWindowTitle(QCoreApplication.translate("Control_Plant", u"MainWindow", None))
        ___qtreewidgetitem = self.reg_formula_treeWidget.headerItem()
        ___qtreewidgetitem.setText(11, QCoreApplication.translate("Control_Plant", u"slump", None));
        ___qtreewidgetitem.setText(10, QCoreApplication.translate("Control_Plant", u"age", None));
        ___qtreewidgetitem.setText(9, QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32\u0e40\u0e04\u0e21\u0e35 2", None));
        ___qtreewidgetitem.setText(8, QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32\u0e40\u0e04\u0e21\u0e35 1", None));
        ___qtreewidgetitem.setText(7, QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33", None));
        ___qtreewidgetitem.setText(6, QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e39\u0e19", None));
        ___qtreewidgetitem.setText(5, QCoreApplication.translate("Control_Plant", u"\u0e40\u0e16\u0e49\u0e32\u0e25\u0e2d\u0e22", None));
        ___qtreewidgetitem.setText(4, QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e192", None));
        ___qtreewidgetitem.setText(3, QCoreApplication.translate("Control_Plant", u"\u0e17\u0e23\u0e32\u0e22", None));
        ___qtreewidgetitem.setText(2, QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e191", None));
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Control_Plant", u"\u0e0a\u0e37\u0e48\u0e2d\u0e2a\u0e39\u0e15\u0e23", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Control_Plant", u"\u0e25\u0e33\u0e14\u0e31\u0e1a", None));

        __sortingEnabled = self.reg_formula_treeWidget.isSortingEnabled()
        self.reg_formula_treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.reg_formula_treeWidget.topLevelItem(0)
        ___qtreewidgetitem1.setText(11, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem1.setText(10, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem1.setText(9, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem1.setText(8, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem1.setText(7, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem1.setText(6, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem1.setText(5, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem1.setText(4, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("Control_Plant", u"133", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Control_Plant", u"3", None));
        ___qtreewidgetitem2 = self.reg_formula_treeWidget.topLevelItem(1)
        ___qtreewidgetitem2.setText(11, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem2.setText(10, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem2.setText(9, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem2.setText(8, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem2.setText(7, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem2.setText(6, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem2.setText(5, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem2.setText(4, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem2.setText(3, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("Control_Plant", u"132", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Control_Plant", u"2", None));
        ___qtreewidgetitem3 = self.reg_formula_treeWidget.topLevelItem(2)
        ___qtreewidgetitem3.setText(11, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem3.setText(10, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem3.setText(9, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem3.setText(8, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem3.setText(7, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem3.setText(6, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem3.setText(5, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem3.setText(4, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem3.setText(3, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem3.setText(2, QCoreApplication.translate("Control_Plant", u"123", None));
        ___qtreewidgetitem3.setText(1, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem3.setText(0, QCoreApplication.translate("Control_Plant", u"1", None));
        self.reg_formula_treeWidget.setSortingEnabled(__sortingEnabled)

        self.reg_name_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e0a\u0e37\u0e48\u0e2d", None))
        self.reg_telephone_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1a\u0e2d\u0e23\u0e4c", None))
        self.reg_address_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e17\u0e35\u0e48\u0e2d\u0e22\u0e39\u0e48", None))
        self.reg_number_car_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e17\u0e30\u0e40\u0e1a\u0e35\u0e22\u0e19\u0e23\u0e16", None))
        self.reg_comment_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e2b\u0e15\u0e38", None))
        self.groupBox.setTitle("")
        self.reg_formula_comboBox.setItemText(0, QCoreApplication.translate("Control_Plant", u"\u0e15\u0e49\u0e2d\u0e07\u0e01\u0e32\u0e23\u0e40\u0e01\u0e47\u0e1a", None))
        self.reg_formula_comboBox.setItemText(1, QCoreApplication.translate("Control_Plant", u"\u0e44\u0e21\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e01\u0e32\u0e23\u0e40\u0e01\u0e47\u0e1a", None))

        self.reg_formula_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e25\u0e39\u0e01\u0e1b\u0e39\u0e19", None))
        self.reg_amount_unit_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e08\u0e33\u0e19\u0e27\u0e19", None))
        self.reg_amount_unit_label1.setText(QCoreApplication.translate("Control_Plant", u"\u0e04\u0e34\u0e27", None))
        self.reg_amount_unit_label_2.setText(QCoreApplication.translate("Control_Plant", u"\u0e0a\u0e37\u0e48\u0e2d\u0e2a\u0e39\u0e15\u0e23", None))
        self.reg_save_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1a\u0e31\u0e19\u0e17\u0e36\u0e01", None))
        self.reg_clear_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e04\u0e25\u0e35\u0e22\u0e02\u0e49\u0e2d\u0e21\u0e39\u0e25", None))
        self.reg_save_new_custommer_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1a\u0e31\u0e19\u0e17\u0e36\u0e01\u0e25\u0e39\u0e01\u0e04\u0e49\u0e32\u0e43\u0e2b\u0e21\u0e48", None))
        ___qtreewidgetitem4 = self.reg_list_customer_treeWidget.headerItem()
        ___qtreewidgetitem4.setText(2, QCoreApplication.translate("Control_Plant", u"\u0e17\u0e35\u0e48\u0e2d\u0e22\u0e39\u0e48", None));
        ___qtreewidgetitem4.setText(1, QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1a\u0e2d\u0e23\u0e4c", None));
        ___qtreewidgetitem4.setText(0, QCoreApplication.translate("Control_Plant", u"\u0e0a\u0e37\u0e48\u0e2d", None));

        __sortingEnabled1 = self.reg_list_customer_treeWidget.isSortingEnabled()
        self.reg_list_customer_treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem5 = self.reg_list_customer_treeWidget.topLevelItem(0)
        ___qtreewidgetitem5.setText(2, QCoreApplication.translate("Control_Plant", u"3333333333333333333", None));
        ___qtreewidgetitem5.setText(1, QCoreApplication.translate("Control_Plant", u"333333333", None));
        ___qtreewidgetitem5.setText(0, QCoreApplication.translate("Control_Plant", u"\u0e17\u0e14\u0e2a\u0e2d\u0e1a3", None));
        ___qtreewidgetitem6 = self.reg_list_customer_treeWidget.topLevelItem(1)
        ___qtreewidgetitem6.setText(2, QCoreApplication.translate("Control_Plant", u"2222222222222222222222222", None));
        ___qtreewidgetitem6.setText(1, QCoreApplication.translate("Control_Plant", u"222222222", None));
        ___qtreewidgetitem6.setText(0, QCoreApplication.translate("Control_Plant", u"\u0e17\u0e14\u0e2a\u0e2d\u0e1a2", None));
        ___qtreewidgetitem7 = self.reg_list_customer_treeWidget.topLevelItem(2)
        ___qtreewidgetitem7.setText(2, QCoreApplication.translate("Control_Plant", u"1111111111111111111111", None));
        ___qtreewidgetitem7.setText(1, QCoreApplication.translate("Control_Plant", u"111111111", None));
        ___qtreewidgetitem7.setText(0, QCoreApplication.translate("Control_Plant", u"\u0e17\u0e14\u0e2a\u0e2d\u0e1a1", None));
        self.reg_list_customer_treeWidget.setSortingEnabled(__sortingEnabled1)

        self.reg_lis_custommer_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e23\u0e32\u0e22\u0e0a\u0e37\u0e48\u0e2d\u0e25\u0e39\u0e01\u0e04\u0e49\u0e32", None))
        self.main_tab.setTabText(self.main_tab.indexOf(self.register_tab), QCoreApplication.translate("Control_Plant", u"Register", None))
        self.main_tab.setTabText(self.main_tab.indexOf(self.Mix_tab), QCoreApplication.translate("Control_Plant", u"Mix", None))
        ___qtreewidgetitem8 = self.for_formula_treeWidget.headerItem()
        ___qtreewidgetitem8.setText(11, QCoreApplication.translate("Control_Plant", u"slump", None));
        ___qtreewidgetitem8.setText(10, QCoreApplication.translate("Control_Plant", u"age", None));
        ___qtreewidgetitem8.setText(9, QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32\u0e40\u0e04\u0e21\u0e35 2", None));
        ___qtreewidgetitem8.setText(8, QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32\u0e40\u0e04\u0e21\u0e35 1", None));
        ___qtreewidgetitem8.setText(7, QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33", None));
        ___qtreewidgetitem8.setText(6, QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e39\u0e19", None));
        ___qtreewidgetitem8.setText(5, QCoreApplication.translate("Control_Plant", u"\u0e40\u0e16\u0e49\u0e32\u0e25\u0e2d\u0e22", None));
        ___qtreewidgetitem8.setText(4, QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e192", None));
        ___qtreewidgetitem8.setText(3, QCoreApplication.translate("Control_Plant", u"\u0e17\u0e23\u0e32\u0e22", None));
        ___qtreewidgetitem8.setText(2, QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e191", None));
        ___qtreewidgetitem8.setText(1, QCoreApplication.translate("Control_Plant", u"\u0e0a\u0e37\u0e48\u0e2d\u0e2a\u0e39\u0e15\u0e23", None));
        ___qtreewidgetitem8.setText(0, QCoreApplication.translate("Control_Plant", u"\u0e25\u0e33\u0e14\u0e31\u0e1a", None));

        __sortingEnabled2 = self.for_formula_treeWidget.isSortingEnabled()
        self.for_formula_treeWidget.setSortingEnabled(False)
        ___qtreewidgetitem9 = self.for_formula_treeWidget.topLevelItem(0)
        ___qtreewidgetitem9.setText(11, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem9.setText(10, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem9.setText(9, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem9.setText(8, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem9.setText(7, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem9.setText(6, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem9.setText(5, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem9.setText(4, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem9.setText(3, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem9.setText(2, QCoreApplication.translate("Control_Plant", u"133", None));
        ___qtreewidgetitem9.setText(1, QCoreApplication.translate("Control_Plant", u"333", None));
        ___qtreewidgetitem9.setText(0, QCoreApplication.translate("Control_Plant", u"3", None));
        ___qtreewidgetitem10 = self.for_formula_treeWidget.topLevelItem(1)
        ___qtreewidgetitem10.setText(11, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem10.setText(10, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem10.setText(9, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem10.setText(8, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem10.setText(7, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem10.setText(6, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem10.setText(5, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem10.setText(4, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem10.setText(3, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem10.setText(2, QCoreApplication.translate("Control_Plant", u"132", None));
        ___qtreewidgetitem10.setText(1, QCoreApplication.translate("Control_Plant", u"222", None));
        ___qtreewidgetitem10.setText(0, QCoreApplication.translate("Control_Plant", u"2", None));
        ___qtreewidgetitem11 = self.for_formula_treeWidget.topLevelItem(2)
        ___qtreewidgetitem11.setText(11, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem11.setText(10, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem11.setText(9, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem11.setText(8, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem11.setText(7, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem11.setText(6, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem11.setText(5, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem11.setText(4, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem11.setText(3, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem11.setText(2, QCoreApplication.translate("Control_Plant", u"123", None));
        ___qtreewidgetitem11.setText(1, QCoreApplication.translate("Control_Plant", u"111", None));
        ___qtreewidgetitem11.setText(0, QCoreApplication.translate("Control_Plant", u"1", None));
        self.for_formula_treeWidget.setSortingEnabled(__sortingEnabled2)

        self.for_config_formula_groupBox.setTitle(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e23\u0e31\u0e1a\u0e2a\u0e39\u0e15\u0e23 /  \u0e40\u0e1e\u0e34\u0e48\u0e21\u0e2a\u0e39\u0e15\u0e23", None))
        self.for_id_formula_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e25\u0e33\u0e14\u0e31\u0e1a", None))
        self.for_name_formula_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e0a\u0e37\u0e48\u0e2d\u0e2a\u0e39\u0e15\u0e23", None))
        self.for_rock_1_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e191", None))
        self.for_sand_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e17\u0e23\u0e32\u0e22", None))
        self.for_rock_2_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e192", None))
        self.for_fyash_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e16\u0e49\u0e32\u0e25\u0e2d\u0e22", None))
        self.for_cement_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e39\u0e19", None))
        self.for_wather_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33", None))
        self.for_chem_1_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32\u0e40\u0e04\u0e21\u0e35 1", None))
        self.for_chem_2_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32\u0e40\u0e04\u0e21\u0e35 2", None))
        self.for_age_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2d\u0e32\u0e22\u0e38", None))
        self.for_slump_label.setText(QCoreApplication.translate("Control_Plant", u"slump", None))
        self.for_add_formula_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1e\u0e34\u0e48\u0e21\u0e2a\u0e39\u0e15\u0e23\u0e43\u0e2b\u0e21\u0e48", None))
        self.for_config_formula_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e41\u0e01\u0e49\u0e44\u0e02\u0e2a\u0e39\u0e15\u0e23", None))
        self.for_delete_formula_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e25\u0e1a\u0e2a\u0e39\u0e15\u0e23", None))
        self.for_save_formula_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1a\u0e31\u0e19\u0e17\u0e36\u0e01\u0e2a\u0e39\u0e15\u0e23", None))
        self.for_cancel_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e22\u0e01\u0e40\u0e25\u0e34\u0e01", None))
        self.main_tab.setTabText(self.main_tab.indexOf(self.formula_tab), QCoreApplication.translate("Control_Plant", u"Formula", None))
    # retranslateUi

