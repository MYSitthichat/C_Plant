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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QDateTimeEdit,
    QFrame, QGroupBox, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QWidget)

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
        self.tab = QTabWidget(self.centralwidget)
        self.tab.setObjectName(u"tab")
        self.tab.setGeometry(QRect(-10, 0, 1561, 831))
        self.tab.setMinimumSize(QSize(1561, 831))
        self.tab.setMaximumSize(QSize(1561, 831))
        self.tab.setBaseSize(QSize(1561, 831))
        font = QFont()
        font.setFamilies([u"TH Niramit AS"])
        font.setPointSize(24)
        font.setBold(True)
        self.tab.setFont(font)
        self.tab.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.tab.setTabPosition(QTabWidget.TabPosition.North)
        self.tab.setIconSize(QSize(20, 20))
        self.tab.setTabsClosable(False)
        self.tab.setMovable(False)
        self.tab.setTabBarAutoHide(False)
        self.Register_tab = QWidget()
        self.Register_tab.setObjectName(u"Register_tab")
        self.reg_formula_treeWidget = QTreeWidget(self.Register_tab)
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
        self.reg_formula_treeWidget.setSortingEnabled(False)
        self.reg_formula_treeWidget.setAnimated(False)
        self.reg_formula_treeWidget.setAllColumnsShowFocus(False)
        self.reg_formula_treeWidget.setWordWrap(False)
        self.reg_formula_treeWidget.setExpandsOnDoubleClick(False)
        self.reg_formula_treeWidget.setColumnCount(12)
        self.reg_formula_treeWidget.header().setVisible(True)
        self.reg_formula_treeWidget.header().setMinimumSectionSize(50)
        self.reg_formula_treeWidget.header().setDefaultSectionSize(123)
        self.reg_formula_treeWidget.header().setProperty(u"showSortIndicator", False)
        self.reg_formula_treeWidget.header().setStretchLastSection(True)
        self.reg_name_label = QLabel(self.Register_tab)
        self.reg_name_label.setObjectName(u"reg_name_label")
        self.reg_name_label.setGeometry(QRect(20, 10, 41, 41))
        self.reg_name_label.setFont(font)
        self.reg_name_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_name_lineEdit = QLineEdit(self.Register_tab)
        self.reg_name_lineEdit.setObjectName(u"reg_name_lineEdit")
        self.reg_name_lineEdit.setGeometry(QRect(70, 5, 181, 41))
        font1 = QFont()
        font1.setFamilies([u"TH Niramit AS"])
        font1.setPointSize(22)
        font1.setBold(True)
        self.reg_name_lineEdit.setFont(font1)
        self.reg_name_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_name_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reg_telephone_label = QLabel(self.Register_tab)
        self.reg_telephone_label.setObjectName(u"reg_telephone_label")
        self.reg_telephone_label.setGeometry(QRect(260, 10, 61, 41))
        self.reg_telephone_label.setFont(font)
        self.reg_telephone_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_telephone_lineEdit = QLineEdit(self.Register_tab)
        self.reg_telephone_lineEdit.setObjectName(u"reg_telephone_lineEdit")
        self.reg_telephone_lineEdit.setGeometry(QRect(330, 5, 201, 41))
        self.reg_telephone_lineEdit.setFont(font1)
        self.reg_telephone_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_telephone_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reg_address_label = QLabel(self.Register_tab)
        self.reg_address_label.setObjectName(u"reg_address_label")
        self.reg_address_label.setGeometry(QRect(20, 60, 51, 41))
        self.reg_address_label.setFont(font)
        self.reg_address_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_address_textEdit = QTextEdit(self.Register_tab)
        self.reg_address_textEdit.setObjectName(u"reg_address_textEdit")
        self.reg_address_textEdit.setGeometry(QRect(70, 60, 461, 131))
        self.reg_address_textEdit.setFont(font1)
        self.reg_address_textEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_number_car_lineEdit = QLineEdit(self.Register_tab)
        self.reg_number_car_lineEdit.setObjectName(u"reg_number_car_lineEdit")
        self.reg_number_car_lineEdit.setGeometry(QRect(140, 250, 111, 41))
        self.reg_number_car_lineEdit.setFont(font1)
        self.reg_number_car_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_number_car_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.reg_number_car_label = QLabel(self.Register_tab)
        self.reg_number_car_label.setObjectName(u"reg_number_car_label")
        self.reg_number_car_label.setGeometry(QRect(20, 250, 111, 41))
        self.reg_number_car_label.setFont(font)
        self.reg_number_car_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_comment_label = QLabel(self.Register_tab)
        self.reg_comment_label.setObjectName(u"reg_comment_label")
        self.reg_comment_label.setGeometry(QRect(20, 290, 111, 41))
        self.reg_comment_label.setFont(font)
        self.reg_comment_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_comment_textEdit = QTextEdit(self.Register_tab)
        self.reg_comment_textEdit.setObjectName(u"reg_comment_textEdit")
        self.reg_comment_textEdit.setGeometry(QRect(130, 300, 401, 101))
        self.reg_comment_textEdit.setFont(font1)
        self.reg_comment_textEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.groupBox = QGroupBox(self.Register_tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 0, 811, 421))
        self.reg_child_cement_comboBox = QComboBox(self.groupBox)
        self.reg_child_cement_comboBox.addItem("")
        self.reg_child_cement_comboBox.addItem("")
        self.reg_child_cement_comboBox.setObjectName(u"reg_child_cement_comboBox")
        self.reg_child_cement_comboBox.setGeometry(QRect(620, 5, 171, 41))
        self.reg_child_cement_comboBox.setFont(font)
        self.reg_child_cement_comboBox.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_child_cement_label = QLabel(self.groupBox)
        self.reg_child_cement_label.setObjectName(u"reg_child_cement_label")
        self.reg_child_cement_label.setGeometry(QRect(540, 10, 71, 41))
        self.reg_child_cement_label.setFont(font)
        self.reg_child_cement_label.setStyleSheet(u"background:rgb(255, 214, 201)")
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
        self.reg_amount_unit_label_2 = QLabel(self.groupBox)
        self.reg_amount_unit_label_2.setObjectName(u"reg_amount_unit_label_2")
        self.reg_amount_unit_label_2.setGeometry(QRect(760, 60, 41, 41))
        self.reg_amount_unit_label_2.setFont(font)
        self.reg_amount_unit_label_2.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_formula_name_label = QLabel(self.groupBox)
        self.reg_formula_name_label.setObjectName(u"reg_formula_name_label")
        self.reg_formula_name_label.setGeometry(QRect(540, 115, 71, 41))
        self.reg_formula_name_label.setFont(font)
        self.reg_formula_name_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_formula_name_lineEdit = QLineEdit(self.groupBox)
        self.reg_formula_name_lineEdit.setObjectName(u"reg_formula_name_lineEdit")
        self.reg_formula_name_lineEdit.setGeometry(QRect(620, 110, 131, 41))
        self.reg_formula_name_lineEdit.setFont(font1)
        self.reg_formula_name_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_formula_name_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        self.reg_save_new_customer_pushButton = QPushButton(self.groupBox)
        self.reg_save_new_customer_pushButton.setObjectName(u"reg_save_new_customer_pushButton")
        self.reg_save_new_customer_pushButton.setGeometry(QRect(530, 340, 271, 61))
        self.reg_save_new_customer_pushButton.setFont(font)
        self.reg_save_new_customer_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.reg_dateTimeEdit = QDateTimeEdit(self.groupBox)
        self.reg_dateTimeEdit.setObjectName(u"reg_dateTimeEdit")
        self.reg_dateTimeEdit.setGeometry(QRect(90, 200, 241, 41))
        self.reg_dateTimeEdit.setFont(font1)
        self.reg_dateTimeEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.reg_dateTimeEdit.setTime(QTime(0, 0, 0))
        self.reg_dateTimeEdit.setCurrentSection(QDateTimeEdit.Section.AmPmSection)
        self.reg_dateTimeEdit.setCalendarPopup(True)
        self.reg_dateTimeEdit.setCurrentSectionIndex(5)
        self.reg_dateTimeEdit.setTimeSpec(Qt.TimeSpec.LocalTime)
        self.reg_date_time_label = QLabel(self.groupBox)
        self.reg_date_time_label.setObjectName(u"reg_date_time_label")
        self.reg_date_time_label.setGeometry(QRect(10, 200, 81, 41))
        self.reg_date_time_label.setFont(font)
        self.reg_date_time_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_update_time_pushButton = QPushButton(self.groupBox)
        self.reg_update_time_pushButton.setObjectName(u"reg_update_time_pushButton")
        self.reg_update_time_pushButton.setGeometry(QRect(350, 200, 161, 41))
        font2 = QFont()
        font2.setFamilies([u"TH Niramit AS"])
        font2.setPointSize(18)
        font2.setBold(True)
        self.reg_update_time_pushButton.setFont(font2)
        self.reg_update_time_pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color:rgb(117, 202, 255); \n"
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
        self.reg_list_customer_treeWidget = QTreeWidget(self.Register_tab)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem1.setFont(3, font);
        __qtreewidgetitem1.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem1.setFont(2, font);
        __qtreewidgetitem1.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem1.setFont(1, font);
        __qtreewidgetitem1.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem1.setFont(0, font);
        self.reg_list_customer_treeWidget.setHeaderItem(__qtreewidgetitem1)
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
        self.reg_list_customer_treeWidget.setSortingEnabled(False)
        self.reg_list_customer_treeWidget.setAnimated(False)
        self.reg_list_customer_treeWidget.setAllColumnsShowFocus(False)
        self.reg_list_customer_treeWidget.setWordWrap(False)
        self.reg_list_customer_treeWidget.setExpandsOnDoubleClick(False)
        self.reg_list_customer_treeWidget.setColumnCount(4)
        self.reg_list_customer_treeWidget.header().setMinimumSectionSize(50)
        self.reg_list_customer_treeWidget.header().setDefaultSectionSize(123)
        self.reg_lis_custommer_label = QLabel(self.Register_tab)
        self.reg_lis_custommer_label.setObjectName(u"reg_lis_custommer_label")
        self.reg_lis_custommer_label.setGeometry(QRect(1150, 10, 131, 41))
        self.reg_lis_custommer_label.setFont(font)
        self.reg_lis_custommer_label.setStyleSheet(u"background:rgb(255, 214, 201)")
        self.reg_delete_customer_pushButton = QPushButton(self.Register_tab)
        self.reg_delete_customer_pushButton.setObjectName(u"reg_delete_customer_pushButton")
        self.reg_delete_customer_pushButton.setGeometry(QRect(1390, 5, 161, 51))
        self.reg_delete_customer_pushButton.setFont(font2)
        self.reg_delete_customer_pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color:rgb(255, 90, 106); \n"
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
        self.tab.addTab(self.Register_tab, "")
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
        self.reg_delete_customer_pushButton.raise_()
        self.Mix_tab = QWidget()
        self.Mix_tab.setObjectName(u"Mix_tab")
        self.Mix_tab.setMinimumSize(QSize(1555, 773))
        self.Mix_tab.setMaximumSize(QSize(1555, 733))
        self.Mix_tab.setBaseSize(QSize(1555, 773))
        self.mix_detail_customer_groupBox = QGroupBox(self.Mix_tab)
        self.mix_detail_customer_groupBox.setObjectName(u"mix_detail_customer_groupBox")
        self.mix_detail_customer_groupBox.setGeometry(QRect(10, 0, 1545, 81))
        self.mix_detail_customer_groupBox.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_detail_customer_groupBox.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.mix_detail_customer_groupBox.setFlat(False)
        self.mix_detail_customer_groupBox.setCheckable(False)
        self.mix_customer_name_lineEdit = QLineEdit(self.mix_detail_customer_groupBox)
        self.mix_customer_name_lineEdit.setObjectName(u"mix_customer_name_lineEdit")
        self.mix_customer_name_lineEdit.setGeometry(QRect(110, 20, 261, 41))
        self.mix_customer_name_lineEdit.setFont(font1)
        self.mix_customer_name_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_customer_name_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_customer_name_label = QLabel(self.mix_detail_customer_groupBox)
        self.mix_customer_name_label.setObjectName(u"mix_customer_name_label")
        self.mix_customer_name_label.setGeometry(QRect(10, 20, 91, 41))
        self.mix_customer_name_label.setFont(font)
        self.mix_customer_name_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_customer_formula_name_lineEdit = QLineEdit(self.mix_detail_customer_groupBox)
        self.mix_customer_formula_name_lineEdit.setObjectName(u"mix_customer_formula_name_lineEdit")
        self.mix_customer_formula_name_lineEdit.setGeometry(QRect(890, 20, 261, 41))
        self.mix_customer_formula_name_lineEdit.setFont(font1)
        self.mix_customer_formula_name_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_customer_formula_name_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_customer_formula_name_label = QLabel(self.mix_detail_customer_groupBox)
        self.mix_customer_formula_name_label.setObjectName(u"mix_customer_formula_name_label")
        self.mix_customer_formula_name_label.setGeometry(QRect(810, 20, 81, 41))
        self.mix_customer_formula_name_label.setFont(font)
        self.mix_customer_formula_name_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_customer_phone_lineEdit = QLineEdit(self.mix_detail_customer_groupBox)
        self.mix_customer_phone_lineEdit.setObjectName(u"mix_customer_phone_lineEdit")
        self.mix_customer_phone_lineEdit.setGeometry(QRect(510, 20, 261, 41))
        self.mix_customer_phone_lineEdit.setFont(font1)
        self.mix_customer_phone_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_customer_phone_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_customer_phone_label = QLabel(self.mix_detail_customer_groupBox)
        self.mix_customer_phone_label.setObjectName(u"mix_customer_phone_label")
        self.mix_customer_phone_label.setGeometry(QRect(410, 20, 91, 41))
        self.mix_customer_phone_label.setFont(font)
        self.mix_customer_phone_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_number_cube_label = QLabel(self.mix_detail_customer_groupBox)
        self.mix_number_cube_label.setObjectName(u"mix_number_cube_label")
        self.mix_number_cube_label.setGeometry(QRect(1180, 20, 91, 41))
        self.mix_number_cube_label.setFont(font)
        self.mix_number_cube_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_number_cube_lineEdit = QLineEdit(self.mix_detail_customer_groupBox)
        self.mix_number_cube_lineEdit.setObjectName(u"mix_number_cube_lineEdit")
        self.mix_number_cube_lineEdit.setGeometry(QRect(1260, 20, 221, 41))
        self.mix_number_cube_lineEdit.setFont(font1)
        self.mix_number_cube_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_number_cube_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_number_cube_unit_label = QLabel(self.mix_detail_customer_groupBox)
        self.mix_number_cube_unit_label.setObjectName(u"mix_number_cube_unit_label")
        self.mix_number_cube_unit_label.setGeometry(QRect(1490, 20, 41, 41))
        self.mix_number_cube_unit_label.setFont(font)
        self.mix_number_cube_unit_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_main_monitor_groupBox = QGroupBox(self.Mix_tab)
        self.mix_main_monitor_groupBox.setObjectName(u"mix_main_monitor_groupBox")
        self.mix_main_monitor_groupBox.setGeometry(QRect(10, 150, 1161, 461))
        font3 = QFont()
        font3.setFamilies([u"TH Niramit AS"])
        font3.setPointSize(20)
        font3.setBold(True)
        self.mix_main_monitor_groupBox.setFont(font3)
        self.mix_main_monitor_groupBox.setStyleSheet(u"background-color:rgb(206, 242, 255); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.mix_monitor_rock_1_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_rock_1_label.setObjectName(u"mix_monitor_rock_1_label")
        self.mix_monitor_rock_1_label.setGeometry(QRect(30, 160, 120, 91))
        self.mix_monitor_rock_1_label.setFont(font)
        self.mix_monitor_rock_1_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_rock_1_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_rock_1_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_rock_1_label.setLineWidth(2)
        self.mix_monitor_rock_1_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.mix_monitor_sand_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_sand_label.setObjectName(u"mix_monitor_sand_label")
        self.mix_monitor_sand_label.setGeometry(QRect(170, 160, 120, 91))
        self.mix_monitor_sand_label.setFont(font)
        self.mix_monitor_sand_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_sand_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_sand_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_sand_label.setLineWidth(2)
        self.mix_monitor_sand_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.mix_monitor_rock_2_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_rock_2_label.setObjectName(u"mix_monitor_rock_2_label")
        self.mix_monitor_rock_2_label.setGeometry(QRect(310, 160, 120, 91))
        self.mix_monitor_rock_2_label.setFont(font)
        self.mix_monitor_rock_2_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_rock_2_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_rock_2_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_rock_2_label.setLineWidth(2)
        self.mix_monitor_rock_2_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.mix_monitor_fyash_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_fyash_label.setObjectName(u"mix_monitor_fyash_label")
        self.mix_monitor_fyash_label.setGeometry(QRect(590, 30, 120, 91))
        self.mix_monitor_fyash_label.setFont(font)
        self.mix_monitor_fyash_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_fyash_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_fyash_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_fyash_label.setLineWidth(2)
        self.mix_monitor_fyash_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.mix_monitor_cement_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_cement_label.setObjectName(u"mix_monitor_cement_label")
        self.mix_monitor_cement_label.setGeometry(QRect(460, 30, 120, 91))
        self.mix_monitor_cement_label.setFont(font)
        self.mix_monitor_cement_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_cement_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_cement_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_cement_label.setLineWidth(2)
        self.mix_monitor_cement_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.mix_monitor_wather_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_wather_label.setObjectName(u"mix_monitor_wather_label")
        self.mix_monitor_wather_label.setGeometry(QRect(720, 95, 120, 91))
        self.mix_monitor_wather_label.setFont(font)
        self.mix_monitor_wather_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_wather_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_wather_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_wather_label.setLineWidth(2)
        self.mix_monitor_wather_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.mix_monitor_chem_2_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_chem_2_label.setObjectName(u"mix_monitor_chem_2_label")
        self.mix_monitor_chem_2_label.setGeometry(QRect(1010, 155, 120, 91))
        self.mix_monitor_chem_2_label.setFont(font)
        self.mix_monitor_chem_2_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_chem_2_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_chem_2_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_chem_2_label.setLineWidth(2)
        self.mix_monitor_chem_2_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.mix_monitor_chem_1_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_chem_1_label.setObjectName(u"mix_monitor_chem_1_label")
        self.mix_monitor_chem_1_label.setGeometry(QRect(880, 155, 120, 91))
        self.mix_monitor_chem_1_label.setFont(font)
        self.mix_monitor_chem_1_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_chem_1_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_chem_1_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_chem_1_label.setLineWidth(2)
        self.mix_monitor_chem_1_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.mix_monitor_rock_1_lineEdit = QLineEdit(self.mix_main_monitor_groupBox)
        self.mix_monitor_rock_1_lineEdit.setObjectName(u"mix_monitor_rock_1_lineEdit")
        self.mix_monitor_rock_1_lineEdit.setGeometry(QRect(40, 205, 101, 41))
        self.mix_monitor_rock_1_lineEdit.setFont(font1)
        self.mix_monitor_rock_1_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_monitor_rock_1_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_sand_lineEdit = QLineEdit(self.mix_main_monitor_groupBox)
        self.mix_monitor_sand_lineEdit.setObjectName(u"mix_monitor_sand_lineEdit")
        self.mix_monitor_sand_lineEdit.setGeometry(QRect(180, 205, 101, 41))
        self.mix_monitor_sand_lineEdit.setFont(font1)
        self.mix_monitor_sand_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_monitor_sand_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_rock_2_lineEdit = QLineEdit(self.mix_main_monitor_groupBox)
        self.mix_monitor_rock_2_lineEdit.setObjectName(u"mix_monitor_rock_2_lineEdit")
        self.mix_monitor_rock_2_lineEdit.setGeometry(QRect(320, 205, 101, 41))
        self.mix_monitor_rock_2_lineEdit.setFont(font1)
        self.mix_monitor_rock_2_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_monitor_rock_2_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_cement_lineEdit = QLineEdit(self.mix_main_monitor_groupBox)
        self.mix_monitor_cement_lineEdit.setObjectName(u"mix_monitor_cement_lineEdit")
        self.mix_monitor_cement_lineEdit.setGeometry(QRect(470, 75, 101, 41))
        self.mix_monitor_cement_lineEdit.setFont(font1)
        self.mix_monitor_cement_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_monitor_cement_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_fyash_lineEdit = QLineEdit(self.mix_main_monitor_groupBox)
        self.mix_monitor_fyash_lineEdit.setObjectName(u"mix_monitor_fyash_lineEdit")
        self.mix_monitor_fyash_lineEdit.setGeometry(QRect(600, 75, 101, 41))
        self.mix_monitor_fyash_lineEdit.setFont(font1)
        self.mix_monitor_fyash_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_monitor_fyash_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_wather_lineEdit = QLineEdit(self.mix_main_monitor_groupBox)
        self.mix_monitor_wather_lineEdit.setObjectName(u"mix_monitor_wather_lineEdit")
        self.mix_monitor_wather_lineEdit.setGeometry(QRect(730, 140, 101, 41))
        self.mix_monitor_wather_lineEdit.setFont(font1)
        self.mix_monitor_wather_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_monitor_wather_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_chem_1_lineEdit = QLineEdit(self.mix_main_monitor_groupBox)
        self.mix_monitor_chem_1_lineEdit.setObjectName(u"mix_monitor_chem_1_lineEdit")
        self.mix_monitor_chem_1_lineEdit.setGeometry(QRect(890, 200, 101, 41))
        self.mix_monitor_chem_1_lineEdit.setFont(font1)
        self.mix_monitor_chem_1_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_monitor_chem_1_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_chem_2_lineEdit = QLineEdit(self.mix_main_monitor_groupBox)
        self.mix_monitor_chem_2_lineEdit.setObjectName(u"mix_monitor_chem_2_lineEdit")
        self.mix_monitor_chem_2_lineEdit.setGeometry(QRect(1020, 200, 101, 41))
        self.mix_monitor_chem_2_lineEdit.setFont(font1)
        self.mix_monitor_chem_2_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_monitor_chem_2_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_mixer_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_mixer_label.setObjectName(u"mix_monitor_mixer_label")
        self.mix_monitor_mixer_label.setGeometry(QRect(460, 270, 391, 111))
        self.mix_monitor_mixer_label.setFont(font)
        self.mix_monitor_mixer_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_mixer_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_mixer_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_mixer_label.setLineWidth(2)
        self.mix_monitor_mixer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_converyer_rock_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_converyer_rock_label.setObjectName(u"mix_monitor_converyer_rock_label")
        self.mix_monitor_converyer_rock_label.setGeometry(QRect(30, 330, 401, 51))
        self.mix_monitor_converyer_rock_label.setFont(font)
        self.mix_monitor_converyer_rock_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_converyer_rock_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_converyer_rock_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_converyer_rock_label.setLineWidth(2)
        self.mix_monitor_converyer_rock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_vale_fyash_and_cement_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_vale_fyash_and_cement_label.setObjectName(u"mix_monitor_vale_fyash_and_cement_label")
        self.mix_monitor_vale_fyash_and_cement_label.setGeometry(QRect(460, 200, 251, 51))
        self.mix_monitor_vale_fyash_and_cement_label.setFont(font)
        self.mix_monitor_vale_fyash_and_cement_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_vale_fyash_and_cement_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_vale_fyash_and_cement_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_vale_fyash_and_cement_label.setLineWidth(2)
        self.mix_monitor_vale_fyash_and_cement_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_vale_wather_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_vale_wather_label.setObjectName(u"mix_monitor_vale_wather_label")
        self.mix_monitor_vale_wather_label.setGeometry(QRect(720, 200, 121, 51))
        self.mix_monitor_vale_wather_label.setFont(font)
        self.mix_monitor_vale_wather_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_vale_wather_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_vale_wather_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_vale_wather_label.setLineWidth(2)
        self.mix_monitor_vale_wather_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_pump_chem_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_pump_chem_label.setObjectName(u"mix_monitor_pump_chem_label")
        self.mix_monitor_pump_chem_label.setGeometry(QRect(880, 330, 251, 51))
        self.mix_monitor_pump_chem_label.setFont(font)
        self.mix_monitor_pump_chem_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_pump_chem_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_pump_chem_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_pump_chem_label.setLineWidth(2)
        self.mix_monitor_pump_chem_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_main_vale_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_main_vale_label.setObjectName(u"mix_monitor_main_vale_label")
        self.mix_monitor_main_vale_label.setGeometry(QRect(460, 390, 391, 51))
        self.mix_monitor_main_vale_label.setFont(font)
        self.mix_monitor_main_vale_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_main_vale_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_main_vale_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_main_vale_label.setLineWidth(2)
        self.mix_monitor_main_vale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_sum_rock_and_sand_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_sum_rock_and_sand_label.setObjectName(u"mix_monitor_sum_rock_and_sand_label")
        self.mix_monitor_sum_rock_and_sand_label.setGeometry(QRect(100, 270, 251, 51))
        self.mix_monitor_sum_rock_and_sand_label.setFont(font)
        self.mix_monitor_sum_rock_and_sand_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_sum_rock_and_sand_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_sum_rock_and_sand_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_sum_rock_and_sand_label.setLineWidth(2)
        self.mix_monitor_sum_rock_and_sand_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.mix_monitor_sum_rock_and_sand_lineEdit = QLineEdit(self.mix_main_monitor_groupBox)
        self.mix_monitor_sum_rock_and_sand_lineEdit.setObjectName(u"mix_monitor_sum_rock_and_sand_lineEdit")
        self.mix_monitor_sum_rock_and_sand_lineEdit.setGeometry(QRect(230, 275, 111, 41))
        self.mix_monitor_sum_rock_and_sand_lineEdit.setFont(font1)
        self.mix_monitor_sum_rock_and_sand_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_monitor_sum_rock_and_sand_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_sum_chem_lineEdit = QLineEdit(self.mix_main_monitor_groupBox)
        self.mix_monitor_sum_chem_lineEdit.setObjectName(u"mix_monitor_sum_chem_lineEdit")
        self.mix_monitor_sum_chem_lineEdit.setGeometry(QRect(1010, 265, 111, 41))
        self.mix_monitor_sum_chem_lineEdit.setFont(font1)
        self.mix_monitor_sum_chem_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_monitor_sum_chem_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_sum_chem_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_sum_chem_label.setObjectName(u"mix_monitor_sum_chem_label")
        self.mix_monitor_sum_chem_label.setGeometry(QRect(880, 260, 251, 51))
        self.mix_monitor_sum_chem_label.setFont(font)
        self.mix_monitor_sum_chem_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_sum_chem_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_sum_chem_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_sum_chem_label.setLineWidth(2)
        self.mix_monitor_sum_chem_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.mix_monitor_sum_fyash_and_cement_label = QLabel(self.mix_main_monitor_groupBox)
        self.mix_monitor_sum_fyash_and_cement_label.setObjectName(u"mix_monitor_sum_fyash_and_cement_label")
        self.mix_monitor_sum_fyash_and_cement_label.setGeometry(QRect(460, 135, 251, 51))
        self.mix_monitor_sum_fyash_and_cement_label.setFont(font)
        self.mix_monitor_sum_fyash_and_cement_label.setStyleSheet(u"background:rgb(255, 184, 205)")
        self.mix_monitor_sum_fyash_and_cement_label.setFrameShape(QFrame.Shape.Box)
        self.mix_monitor_sum_fyash_and_cement_label.setFrameShadow(QFrame.Shadow.Plain)
        self.mix_monitor_sum_fyash_and_cement_label.setLineWidth(2)
        self.mix_monitor_sum_fyash_and_cement_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.mix_monitor_sum_fyash_and_cement_lineEdit = QLineEdit(self.mix_main_monitor_groupBox)
        self.mix_monitor_sum_fyash_and_cement_lineEdit.setObjectName(u"mix_monitor_sum_fyash_and_cement_lineEdit")
        self.mix_monitor_sum_fyash_and_cement_lineEdit.setGeometry(QRect(590, 140, 111, 41))
        self.mix_monitor_sum_fyash_and_cement_lineEdit.setFont(font1)
        self.mix_monitor_sum_fyash_and_cement_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.mix_monitor_sum_fyash_and_cement_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_monitor_sum_chem_label.raise_()
        self.mix_monitor_rock_1_label.raise_()
        self.mix_monitor_sand_label.raise_()
        self.mix_monitor_rock_2_label.raise_()
        self.mix_monitor_fyash_label.raise_()
        self.mix_monitor_cement_label.raise_()
        self.mix_monitor_wather_label.raise_()
        self.mix_monitor_chem_2_label.raise_()
        self.mix_monitor_chem_1_label.raise_()
        self.mix_monitor_rock_1_lineEdit.raise_()
        self.mix_monitor_sand_lineEdit.raise_()
        self.mix_monitor_rock_2_lineEdit.raise_()
        self.mix_monitor_cement_lineEdit.raise_()
        self.mix_monitor_fyash_lineEdit.raise_()
        self.mix_monitor_wather_lineEdit.raise_()
        self.mix_monitor_chem_1_lineEdit.raise_()
        self.mix_monitor_chem_2_lineEdit.raise_()
        self.mix_monitor_mixer_label.raise_()
        self.mix_monitor_converyer_rock_label.raise_()
        self.mix_monitor_vale_fyash_and_cement_label.raise_()
        self.mix_monitor_vale_wather_label.raise_()
        self.mix_monitor_pump_chem_label.raise_()
        self.mix_monitor_main_vale_label.raise_()
        self.mix_monitor_sum_rock_and_sand_label.raise_()
        self.mix_monitor_sum_rock_and_sand_lineEdit.raise_()
        self.mix_monitor_sum_chem_lineEdit.raise_()
        self.mix_monitor_sum_fyash_and_cement_label.raise_()
        self.mix_monitor_sum_fyash_and_cement_lineEdit.raise_()
        self.mix_monitor_status_groupBox = QGroupBox(self.Mix_tab)
        self.mix_monitor_status_groupBox.setObjectName(u"mix_monitor_status_groupBox")
        self.mix_monitor_status_groupBox.setGeometry(QRect(10, 605, 1161, 165))
        self.mix_monitor_status_groupBox.setFont(font3)
        self.mix_monitor_status_textEdit = QTextEdit(self.mix_monitor_status_groupBox)
        self.mix_monitor_status_textEdit.setObjectName(u"mix_monitor_status_textEdit")
        self.mix_monitor_status_textEdit.setGeometry(QRect(10, 30, 1141, 125))
        self.mix_monitor_status_textEdit.setFont(font3)
        self.mix_monitor_status_textEdit.setStyleSheet(u"background-color:rgb(255, 255, 255); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.mix_wieght_monitor_groupBox = QGroupBox(self.Mix_tab)
        self.mix_wieght_monitor_groupBox.setObjectName(u"mix_wieght_monitor_groupBox")
        self.mix_wieght_monitor_groupBox.setGeometry(QRect(1180, 290, 371, 481))
        self.mix_wieght_monitor_groupBox.setFont(font3)
        self.mix_wieght_monitor_groupBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.mix_wieght_monitor_groupBox.setAutoFillBackground(False)
        self.mix_wieght_monitor_groupBox.setStyleSheet(u"")
        self.mix_wieght_Loaded_label = QLabel(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_label.setObjectName(u"mix_wieght_Loaded_label")
        self.mix_wieght_Loaded_label.setGeometry(QRect(120, 30, 81, 41))
        self.mix_wieght_Loaded_label.setFont(font3)
        self.mix_wieght_target_label = QLabel(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_target_label.setObjectName(u"mix_wieght_target_label")
        self.mix_wieght_target_label.setGeometry(QRect(250, 30, 81, 41))
        self.mix_wieght_target_label.setFont(font3)
        self.mix_wieght_Loaded_rock_1_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_rock_1_lineEdit.setObjectName(u"mix_wieght_Loaded_rock_1_lineEdit")
        self.mix_wieght_Loaded_rock_1_lineEdit.setGeometry(QRect(110, 80, 111, 41))
        self.mix_wieght_Loaded_rock_1_lineEdit.setFont(font3)
        self.mix_wieght_Loaded_rock_1_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_Loaded_rock_1_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_Loaded_rock_1_label = QLabel(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_rock_1_label.setObjectName(u"mix_wieght_Loaded_rock_1_label")
        self.mix_wieght_Loaded_rock_1_label.setGeometry(QRect(20, 80, 81, 41))
        self.mix_wieght_Loaded_rock_1_label.setFont(font3)
        self.mix_wieght_Loaded_sand_label = QLabel(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_sand_label.setObjectName(u"mix_wieght_Loaded_sand_label")
        self.mix_wieght_Loaded_sand_label.setGeometry(QRect(20, 130, 81, 41))
        self.mix_wieght_Loaded_sand_label.setFont(font3)
        self.mix_wieght_Loaded_rock_2_label = QLabel(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_rock_2_label.setObjectName(u"mix_wieght_Loaded_rock_2_label")
        self.mix_wieght_Loaded_rock_2_label.setGeometry(QRect(20, 180, 81, 41))
        self.mix_wieght_Loaded_rock_2_label.setFont(font3)
        self.mix_wieght_Loaded_cement_label = QLabel(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_cement_label.setObjectName(u"mix_wieght_Loaded_cement_label")
        self.mix_wieght_Loaded_cement_label.setGeometry(QRect(20, 230, 81, 41))
        self.mix_wieght_Loaded_cement_label.setFont(font3)
        self.mix_wieght_Loaded_fyash_label = QLabel(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_fyash_label.setObjectName(u"mix_wieght_Loaded_fyash_label")
        self.mix_wieght_Loaded_fyash_label.setGeometry(QRect(20, 280, 81, 41))
        self.mix_wieght_Loaded_fyash_label.setFont(font3)
        self.mix_wieght_Loaded_wather_label = QLabel(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_wather_label.setObjectName(u"mix_wieght_Loaded_wather_label")
        self.mix_wieght_Loaded_wather_label.setGeometry(QRect(20, 330, 81, 41))
        self.mix_wieght_Loaded_wather_label.setFont(font3)
        self.mix_wieght_Loaded_chem_1_label = QLabel(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_chem_1_label.setObjectName(u"mix_wieght_Loaded_chem_1_label")
        self.mix_wieght_Loaded_chem_1_label.setGeometry(QRect(20, 380, 81, 41))
        self.mix_wieght_Loaded_chem_1_label.setFont(font3)
        self.mix_wieght_Loaded_chem_2_label = QLabel(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_chem_2_label.setObjectName(u"mix_wieght_Loaded_chem_2_label")
        self.mix_wieght_Loaded_chem_2_label.setGeometry(QRect(20, 430, 81, 41))
        self.mix_wieght_Loaded_chem_2_label.setFont(font3)
        self.mix_wieght_Loaded_sand_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_sand_lineEdit.setObjectName(u"mix_wieght_Loaded_sand_lineEdit")
        self.mix_wieght_Loaded_sand_lineEdit.setGeometry(QRect(110, 130, 111, 41))
        self.mix_wieght_Loaded_sand_lineEdit.setFont(font3)
        self.mix_wieght_Loaded_sand_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_Loaded_sand_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_Loaded_rock_2_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_rock_2_lineEdit.setObjectName(u"mix_wieght_Loaded_rock_2_lineEdit")
        self.mix_wieght_Loaded_rock_2_lineEdit.setGeometry(QRect(110, 180, 111, 41))
        self.mix_wieght_Loaded_rock_2_lineEdit.setFont(font3)
        self.mix_wieght_Loaded_rock_2_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_Loaded_rock_2_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_Loaded_cement_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_cement_lineEdit.setObjectName(u"mix_wieght_Loaded_cement_lineEdit")
        self.mix_wieght_Loaded_cement_lineEdit.setGeometry(QRect(110, 230, 111, 41))
        self.mix_wieght_Loaded_cement_lineEdit.setFont(font3)
        self.mix_wieght_Loaded_cement_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_Loaded_cement_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_Loaded_fyash_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_fyash_lineEdit.setObjectName(u"mix_wieght_Loaded_fyash_lineEdit")
        self.mix_wieght_Loaded_fyash_lineEdit.setGeometry(QRect(110, 280, 111, 41))
        self.mix_wieght_Loaded_fyash_lineEdit.setFont(font3)
        self.mix_wieght_Loaded_fyash_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_Loaded_fyash_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_Loaded_wather_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_wather_lineEdit.setObjectName(u"mix_wieght_Loaded_wather_lineEdit")
        self.mix_wieght_Loaded_wather_lineEdit.setGeometry(QRect(110, 330, 111, 41))
        self.mix_wieght_Loaded_wather_lineEdit.setFont(font3)
        self.mix_wieght_Loaded_wather_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_Loaded_wather_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_Loaded_chem_1_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_chem_1_lineEdit.setObjectName(u"mix_wieght_Loaded_chem_1_lineEdit")
        self.mix_wieght_Loaded_chem_1_lineEdit.setGeometry(QRect(110, 380, 111, 41))
        self.mix_wieght_Loaded_chem_1_lineEdit.setFont(font3)
        self.mix_wieght_Loaded_chem_1_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_Loaded_chem_1_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_Loaded_chem_2_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_Loaded_chem_2_lineEdit.setObjectName(u"mix_wieght_Loaded_chem_2_lineEdit")
        self.mix_wieght_Loaded_chem_2_lineEdit.setGeometry(QRect(110, 430, 111, 41))
        self.mix_wieght_Loaded_chem_2_lineEdit.setFont(font3)
        self.mix_wieght_Loaded_chem_2_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_Loaded_chem_2_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_target_sand_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_target_sand_lineEdit.setObjectName(u"mix_wieght_target_sand_lineEdit")
        self.mix_wieght_target_sand_lineEdit.setGeometry(QRect(240, 130, 111, 41))
        self.mix_wieght_target_sand_lineEdit.setFont(font3)
        self.mix_wieght_target_sand_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_target_sand_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_target_wather_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_target_wather_lineEdit.setObjectName(u"mix_wieght_target_wather_lineEdit")
        self.mix_wieght_target_wather_lineEdit.setGeometry(QRect(240, 330, 111, 41))
        self.mix_wieght_target_wather_lineEdit.setFont(font3)
        self.mix_wieght_target_wather_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_target_wather_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_target_rock_2_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_target_rock_2_lineEdit.setObjectName(u"mix_wieght_target_rock_2_lineEdit")
        self.mix_wieght_target_rock_2_lineEdit.setGeometry(QRect(240, 180, 111, 41))
        self.mix_wieght_target_rock_2_lineEdit.setFont(font3)
        self.mix_wieght_target_rock_2_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_target_rock_2_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_targrt_rock_1_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_targrt_rock_1_lineEdit.setObjectName(u"mix_wieght_targrt_rock_1_lineEdit")
        self.mix_wieght_targrt_rock_1_lineEdit.setGeometry(QRect(240, 80, 111, 41))
        self.mix_wieght_targrt_rock_1_lineEdit.setFont(font3)
        self.mix_wieght_targrt_rock_1_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_targrt_rock_1_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_target_cement_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_target_cement_lineEdit.setObjectName(u"mix_wieght_target_cement_lineEdit")
        self.mix_wieght_target_cement_lineEdit.setGeometry(QRect(240, 230, 111, 41))
        self.mix_wieght_target_cement_lineEdit.setFont(font3)
        self.mix_wieght_target_cement_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_target_cement_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_target_chem_2_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_target_chem_2_lineEdit.setObjectName(u"mix_wieght_target_chem_2_lineEdit")
        self.mix_wieght_target_chem_2_lineEdit.setGeometry(QRect(240, 430, 111, 41))
        self.mix_wieght_target_chem_2_lineEdit.setFont(font3)
        self.mix_wieght_target_chem_2_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_target_chem_2_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_target_fyash_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_target_fyash_lineEdit.setObjectName(u"mix_wieght_target_fyash_lineEdit")
        self.mix_wieght_target_fyash_lineEdit.setGeometry(QRect(240, 280, 111, 41))
        self.mix_wieght_target_fyash_lineEdit.setFont(font3)
        self.mix_wieght_target_fyash_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_target_fyash_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_wieght_target_chem_1_lineEdit = QLineEdit(self.mix_wieght_monitor_groupBox)
        self.mix_wieght_target_chem_1_lineEdit.setObjectName(u"mix_wieght_target_chem_1_lineEdit")
        self.mix_wieght_target_chem_1_lineEdit.setGeometry(QRect(240, 380, 111, 41))
        self.mix_wieght_target_chem_1_lineEdit.setFont(font3)
        self.mix_wieght_target_chem_1_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_wieght_target_chem_1_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_result_groupBox = QGroupBox(self.Mix_tab)
        self.mix_result_groupBox.setObjectName(u"mix_result_groupBox")
        self.mix_result_groupBox.setGeometry(QRect(1180, 85, 371, 201))
        self.mix_result_groupBox.setFont(font3)
        self.mix_result_groupBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.mix_result_groupBox.setAutoFillBackground(False)
        self.mix_result_groupBox.setStyleSheet(u"")
        self.mix_result_load_lineEdit = QLineEdit(self.mix_result_groupBox)
        self.mix_result_load_lineEdit.setObjectName(u"mix_result_load_lineEdit")
        self.mix_result_load_lineEdit.setGeometry(QRect(180, 40, 101, 41))
        self.mix_result_load_lineEdit.setFont(font3)
        self.mix_result_load_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_result_load_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_result_load_label = QLabel(self.mix_result_groupBox)
        self.mix_result_load_label.setObjectName(u"mix_result_load_label")
        self.mix_result_load_label.setGeometry(QRect(10, 40, 161, 41))
        self.mix_result_load_label.setFont(font3)
        self.mix_result_mix_lineEdit = QLineEdit(self.mix_result_groupBox)
        self.mix_result_mix_lineEdit.setObjectName(u"mix_result_mix_lineEdit")
        self.mix_result_mix_lineEdit.setGeometry(QRect(180, 90, 101, 41))
        self.mix_result_mix_lineEdit.setFont(font3)
        self.mix_result_mix_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_result_mix_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_result_mix_success_lineEdit = QLineEdit(self.mix_result_groupBox)
        self.mix_result_mix_success_lineEdit.setObjectName(u"mix_result_mix_success_lineEdit")
        self.mix_result_mix_success_lineEdit.setGeometry(QRect(180, 140, 101, 41))
        self.mix_result_mix_success_lineEdit.setFont(font3)
        self.mix_result_mix_success_lineEdit.setStyleSheet(u"background:rgb(255, 255, 255)")
        self.mix_result_mix_success_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mix_result_load_unit_label = QLabel(self.mix_result_groupBox)
        self.mix_result_load_unit_label.setObjectName(u"mix_result_load_unit_label")
        self.mix_result_load_unit_label.setGeometry(QRect(300, 40, 61, 41))
        self.mix_result_load_unit_label.setFont(font3)
        self.mix_result_mix_label = QLabel(self.mix_result_groupBox)
        self.mix_result_mix_label.setObjectName(u"mix_result_mix_label")
        self.mix_result_mix_label.setGeometry(QRect(10, 90, 161, 41))
        self.mix_result_mix_label.setFont(font3)
        self.mix_result_mix_success_label = QLabel(self.mix_result_groupBox)
        self.mix_result_mix_success_label.setObjectName(u"mix_result_mix_success_label")
        self.mix_result_mix_success_label.setGeometry(QRect(10, 140, 161, 41))
        self.mix_result_mix_success_label.setFont(font3)
        self.mix_result_mix_unit_label = QLabel(self.mix_result_groupBox)
        self.mix_result_mix_unit_label.setObjectName(u"mix_result_mix_unit_label")
        self.mix_result_mix_unit_label.setGeometry(QRect(300, 90, 61, 41))
        self.mix_result_mix_unit_label.setFont(font3)
        self.mix_result_mix_success_unit_label = QLabel(self.mix_result_groupBox)
        self.mix_result_mix_success_unit_label.setObjectName(u"mix_result_mix_success_unit_label")
        self.mix_result_mix_success_unit_label.setGeometry(QRect(300, 140, 61, 41))
        self.mix_result_mix_success_unit_label.setFont(font3)
        self.mix_cancel_load_pushButton = QPushButton(self.Mix_tab)
        self.mix_cancel_load_pushButton.setObjectName(u"mix_cancel_load_pushButton")
        self.mix_cancel_load_pushButton.setGeometry(QRect(900, 85, 271, 61))
        self.mix_cancel_load_pushButton.setFont(font)
        self.mix_cancel_load_pushButton.setStyleSheet(u"\n"
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
        self.mix_start_load_pushButton = QPushButton(self.Mix_tab)
        self.mix_start_load_pushButton.setObjectName(u"mix_start_load_pushButton")
        self.mix_start_load_pushButton.setGeometry(QRect(620, 85, 271, 61))
        self.mix_start_load_pushButton.setFont(font)
        self.mix_start_load_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.tab.addTab(self.Mix_tab, "")
        self.mix_monitor_status_groupBox.raise_()
        self.mix_detail_customer_groupBox.raise_()
        self.mix_main_monitor_groupBox.raise_()
        self.mix_wieght_monitor_groupBox.raise_()
        self.mix_result_groupBox.raise_()
        self.mix_cancel_load_pushButton.raise_()
        self.mix_start_load_pushButton.raise_()
        self.Formula_tab = QWidget()
        self.Formula_tab.setObjectName(u"Formula_tab")
        self.for_formula_treeWidget = QTreeWidget(self.Formula_tab)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setTextAlignment(11, Qt.AlignCenter);
        __qtreewidgetitem2.setFont(11, font);
        __qtreewidgetitem2.setTextAlignment(10, Qt.AlignCenter);
        __qtreewidgetitem2.setFont(10, font);
        __qtreewidgetitem2.setTextAlignment(9, Qt.AlignCenter);
        __qtreewidgetitem2.setFont(9, font);
        __qtreewidgetitem2.setTextAlignment(8, Qt.AlignCenter);
        __qtreewidgetitem2.setFont(8, font);
        __qtreewidgetitem2.setTextAlignment(7, Qt.AlignCenter);
        __qtreewidgetitem2.setFont(7, font);
        __qtreewidgetitem2.setTextAlignment(6, Qt.AlignCenter);
        __qtreewidgetitem2.setFont(6, font);
        __qtreewidgetitem2.setTextAlignment(5, Qt.AlignCenter);
        __qtreewidgetitem2.setFont(5, font);
        __qtreewidgetitem2.setTextAlignment(4, Qt.AlignCenter);
        __qtreewidgetitem2.setFont(4, font);
        __qtreewidgetitem2.setTextAlignment(3, Qt.AlignCenter);
        __qtreewidgetitem2.setFont(3, font);
        __qtreewidgetitem2.setTextAlignment(2, Qt.AlignCenter);
        __qtreewidgetitem2.setFont(2, font);
        __qtreewidgetitem2.setTextAlignment(1, Qt.AlignCenter);
        __qtreewidgetitem2.setFont(1, font);
        __qtreewidgetitem2.setTextAlignment(0, Qt.AlignCenter);
        __qtreewidgetitem2.setFont(0, font);
        self.for_formula_treeWidget.setHeaderItem(__qtreewidgetitem2)
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
        self.for_formula_treeWidget.setSortingEnabled(False)
        self.for_formula_treeWidget.setAnimated(False)
        self.for_formula_treeWidget.setAllColumnsShowFocus(False)
        self.for_formula_treeWidget.setWordWrap(False)
        self.for_formula_treeWidget.setExpandsOnDoubleClick(False)
        self.for_formula_treeWidget.setColumnCount(12)
        self.for_formula_treeWidget.header().setMinimumSectionSize(50)
        self.for_formula_treeWidget.header().setDefaultSectionSize(123)
        self.for_config_formula_groupBox = QGroupBox(self.Formula_tab)
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
        self.for_add_formula_pushButton = QPushButton(self.Formula_tab)
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
        self.for_config_formula_pushButton = QPushButton(self.Formula_tab)
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
        self.for_delete_formula_pushButton = QPushButton(self.Formula_tab)
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
        self.for_save_formula_pushButton = QPushButton(self.Formula_tab)
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
        self.for_cancel_pushButton = QPushButton(self.Formula_tab)
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
        self.tab.addTab(self.Formula_tab, "")
        self.Debug_tab = QWidget()
        self.Debug_tab.setObjectName(u"Debug_tab")
        self.debug_control_groupBox = QGroupBox(self.Debug_tab)
        self.debug_control_groupBox.setObjectName(u"debug_control_groupBox")
        self.debug_control_groupBox.setGeometry(QRect(10, 0, 1545, 601))
        self.debug_control_groupBox.setFont(font)
        self.debug_open_rock_1_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_rock_1_pushButton.setObjectName(u"debug_open_rock_1_pushButton")
        self.debug_open_rock_1_pushButton.setGeometry(QRect(50, 280, 111, 51))
        self.debug_open_rock_1_pushButton.setFont(font3)
        self.debug_open_rock_1_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_rock_1_label = QLabel(self.debug_control_groupBox)
        self.debug_rock_1_label.setObjectName(u"debug_rock_1_label")
        self.debug_rock_1_label.setGeometry(QRect(40, 240, 131, 161))
        self.debug_rock_1_label.setFont(font3)
        self.debug_rock_1_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_rock_1_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.debug_close_rock_1_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_rock_1_pushButton.setObjectName(u"debug_close_rock_1_pushButton")
        self.debug_close_rock_1_pushButton.setGeometry(QRect(50, 340, 111, 51))
        self.debug_close_rock_1_pushButton.setFont(font3)
        self.debug_close_rock_1_pushButton.setStyleSheet(u"\n"
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
        self.debug_close_sand_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_sand_pushButton.setObjectName(u"debug_close_sand_pushButton")
        self.debug_close_sand_pushButton.setGeometry(QRect(200, 340, 111, 51))
        self.debug_close_sand_pushButton.setFont(font3)
        self.debug_close_sand_pushButton.setStyleSheet(u"\n"
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
        self.debug_open_sand_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_sand_pushButton.setObjectName(u"debug_open_sand_pushButton")
        self.debug_open_sand_pushButton.setGeometry(QRect(200, 280, 111, 51))
        self.debug_open_sand_pushButton.setFont(font3)
        self.debug_open_sand_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_sand_label = QLabel(self.debug_control_groupBox)
        self.debug_sand_label.setObjectName(u"debug_sand_label")
        self.debug_sand_label.setGeometry(QRect(190, 240, 131, 161))
        self.debug_sand_label.setFont(font3)
        self.debug_sand_label.setStyleSheet(u"background-color:rgb(206, 242, 255); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_sand_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.debug_rock_label = QLabel(self.debug_control_groupBox)
        self.debug_rock_label.setObjectName(u"debug_rock_label")
        self.debug_rock_label.setGeometry(QRect(340, 240, 131, 161))
        self.debug_rock_label.setFont(font3)
        self.debug_rock_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_rock_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.debug_close_rock_2_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_rock_2_pushButton.setObjectName(u"debug_close_rock_2_pushButton")
        self.debug_close_rock_2_pushButton.setGeometry(QRect(350, 340, 111, 51))
        self.debug_close_rock_2_pushButton.setFont(font3)
        self.debug_close_rock_2_pushButton.setStyleSheet(u"\n"
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
        self.debug_open_rock_2_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_rock_2_pushButton.setObjectName(u"debug_open_rock_2_pushButton")
        self.debug_open_rock_2_pushButton.setGeometry(QRect(350, 280, 111, 51))
        self.debug_open_rock_2_pushButton.setFont(font3)
        self.debug_open_rock_2_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_converyer_under_label = QLabel(self.debug_control_groupBox)
        self.debug_converyer_under_label.setObjectName(u"debug_converyer_under_label")
        self.debug_converyer_under_label.setGeometry(QRect(40, 410, 431, 71))
        self.debug_converyer_under_label.setFont(font3)
        self.debug_converyer_under_label.setStyleSheet(u"background-color:rgb(209, 195, 170); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_converyer_under_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.debug_open_converyer_under_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_converyer_under_pushButton.setObjectName(u"debug_open_converyer_under_pushButton")
        self.debug_open_converyer_under_pushButton.setGeometry(QRect(190, 420, 121, 51))
        self.debug_open_converyer_under_pushButton.setFont(font3)
        self.debug_open_converyer_under_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_close_converyer_under_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_converyer_under_pushButton.setObjectName(u"debug_close_converyer_under_pushButton")
        self.debug_close_converyer_under_pushButton.setGeometry(QRect(330, 420, 131, 51))
        self.debug_close_converyer_under_pushButton.setFont(font3)
        self.debug_close_converyer_under_pushButton.setStyleSheet(u"\n"
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
        self.debug_converyer_top_label = QLabel(self.debug_control_groupBox)
        self.debug_converyer_top_label.setObjectName(u"debug_converyer_top_label")
        self.debug_converyer_top_label.setGeometry(QRect(40, 490, 431, 71))
        self.debug_converyer_top_label.setFont(font3)
        self.debug_converyer_top_label.setStyleSheet(u"background-color:rgb(255, 221, 135); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_converyer_top_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.debug_close_converyer_top_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_converyer_top_pushButton.setObjectName(u"debug_close_converyer_top_pushButton")
        self.debug_close_converyer_top_pushButton.setGeometry(QRect(330, 500, 131, 51))
        self.debug_close_converyer_top_pushButton.setFont(font3)
        self.debug_close_converyer_top_pushButton.setStyleSheet(u"\n"
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
        self.debug_open_converyer_top_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_converyer_top_pushButton.setObjectName(u"debug_open_converyer_top_pushButton")
        self.debug_open_converyer_top_pushButton.setGeometry(QRect(190, 500, 121, 51))
        self.debug_open_converyer_top_pushButton.setFont(font3)
        self.debug_open_converyer_top_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_cement_label = QLabel(self.debug_control_groupBox)
        self.debug_cement_label.setObjectName(u"debug_cement_label")
        self.debug_cement_label.setGeometry(QRect(560, 50, 251, 101))
        self.debug_cement_label.setFont(font3)
        self.debug_cement_label.setStyleSheet(u"background-color:rgb(180, 194, 255); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_cement_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.debug_close_cement_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_cement_pushButton.setObjectName(u"debug_close_cement_pushButton")
        self.debug_close_cement_pushButton.setGeometry(QRect(690, 90, 111, 51))
        self.debug_close_cement_pushButton.setFont(font3)
        self.debug_close_cement_pushButton.setStyleSheet(u"\n"
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
        self.debug_open_cement_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_cement_pushButton.setObjectName(u"debug_open_cement_pushButton")
        self.debug_open_cement_pushButton.setGeometry(QRect(570, 90, 111, 51))
        self.debug_open_cement_pushButton.setFont(font3)
        self.debug_open_cement_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_close_fyash_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_fyash_pushButton.setObjectName(u"debug_close_fyash_pushButton")
        self.debug_close_fyash_pushButton.setGeometry(QRect(950, 90, 111, 51))
        self.debug_close_fyash_pushButton.setFont(font3)
        self.debug_close_fyash_pushButton.setStyleSheet(u"\n"
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
        self.debug_open_fyash_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_fyash_pushButton.setObjectName(u"debug_open_fyash_pushButton")
        self.debug_open_fyash_pushButton.setGeometry(QRect(830, 90, 111, 51))
        self.debug_open_fyash_pushButton.setFont(font3)
        self.debug_open_fyash_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_fyash_label = QLabel(self.debug_control_groupBox)
        self.debug_fyash_label.setObjectName(u"debug_fyash_label")
        self.debug_fyash_label.setGeometry(QRect(820, 50, 251, 101))
        self.debug_fyash_label.setFont(font3)
        self.debug_fyash_label.setStyleSheet(u"background-color:rgb(255, 248, 143); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_fyash_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.debug_vale_cement_label = QLabel(self.debug_control_groupBox)
        self.debug_vale_cement_label.setObjectName(u"debug_vale_cement_label")
        self.debug_vale_cement_label.setGeometry(QRect(560, 160, 511, 71))
        self.debug_vale_cement_label.setFont(font3)
        self.debug_vale_cement_label.setStyleSheet(u"background-color:rgb(168, 165, 221); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_vale_cement_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.debug_open_vale_cement_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_vale_cement_pushButton.setObjectName(u"debug_open_vale_cement_pushButton")
        self.debug_open_vale_cement_pushButton.setGeometry(QRect(730, 170, 161, 51))
        self.debug_open_vale_cement_pushButton.setFont(font3)
        self.debug_open_vale_cement_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_close_vale_cement_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_vale_cement_pushButton.setObjectName(u"debug_close_vale_cement_pushButton")
        self.debug_close_vale_cement_pushButton.setGeometry(QRect(900, 170, 161, 51))
        self.debug_close_vale_cement_pushButton.setFont(font3)
        self.debug_close_vale_cement_pushButton.setStyleSheet(u"\n"
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
        self.debug_vale_wather_label = QLabel(self.debug_control_groupBox)
        self.debug_vale_wather_label.setObjectName(u"debug_vale_wather_label")
        self.debug_vale_wather_label.setGeometry(QRect(1160, 160, 351, 71))
        self.debug_vale_wather_label.setFont(font3)
        self.debug_vale_wather_label.setStyleSheet(u"background-color:rgb(206, 242, 255); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_vale_wather_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.debug_close_vale_water_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_vale_water_pushButton.setObjectName(u"debug_close_vale_water_pushButton")
        self.debug_close_vale_water_pushButton.setGeometry(QRect(1370, 170, 131, 51))
        self.debug_close_vale_water_pushButton.setFont(font3)
        self.debug_close_vale_water_pushButton.setStyleSheet(u"\n"
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
        self.debug_open_vale_water_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_vale_water_pushButton.setObjectName(u"debug_open_vale_water_pushButton")
        self.debug_open_vale_water_pushButton.setGeometry(QRect(1240, 170, 121, 51))
        self.debug_open_vale_water_pushButton.setFont(font3)
        self.debug_open_vale_water_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_close_mixer_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_mixer_pushButton.setObjectName(u"debug_close_mixer_pushButton")
        self.debug_close_mixer_pushButton.setGeometry(QRect(830, 350, 231, 51))
        self.debug_close_mixer_pushButton.setFont(font3)
        self.debug_close_mixer_pushButton.setStyleSheet(u"\n"
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
        self.debug_open_mixer_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_mixer_pushButton.setObjectName(u"debug_open_mixer_pushButton")
        self.debug_open_mixer_pushButton.setGeometry(QRect(570, 350, 231, 51))
        self.debug_open_mixer_pushButton.setFont(font3)
        self.debug_open_mixer_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_mixer_label = QLabel(self.debug_control_groupBox)
        self.debug_mixer_label.setObjectName(u"debug_mixer_label")
        self.debug_mixer_label.setGeometry(QRect(560, 300, 511, 121))
        self.debug_mixer_label.setFont(font3)
        self.debug_mixer_label.setStyleSheet(u"background-color:rgb(170, 255, 12); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_mixer_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.debug_close_vale_mixer_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_vale_mixer_pushButton.setObjectName(u"debug_close_vale_mixer_pushButton")
        self.debug_close_vale_mixer_pushButton.setGeometry(QRect(820, 500, 141, 51))
        self.debug_close_vale_mixer_pushButton.setFont(font3)
        self.debug_close_vale_mixer_pushButton.setStyleSheet(u"\n"
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
        self.debug_vale_mixer_label = QLabel(self.debug_control_groupBox)
        self.debug_vale_mixer_label.setObjectName(u"debug_vale_mixer_label")
        self.debug_vale_mixer_label.setGeometry(QRect(660, 460, 311, 101))
        self.debug_vale_mixer_label.setFont(font3)
        self.debug_vale_mixer_label.setStyleSheet(u"background-color:rgb(255, 201, 202); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_vale_mixer_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.debug_open_vale_mixer_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_vale_mixer_pushButton.setObjectName(u"debug_open_vale_mixer_pushButton")
        self.debug_open_vale_mixer_pushButton.setGeometry(QRect(670, 500, 141, 51))
        self.debug_open_vale_mixer_pushButton.setFont(font3)
        self.debug_open_vale_mixer_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_close_chem_1_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_chem_1_pushButton.setObjectName(u"debug_close_chem_1_pushButton")
        self.debug_close_chem_1_pushButton.setGeometry(QRect(1200, 400, 111, 51))
        self.debug_close_chem_1_pushButton.setFont(font3)
        self.debug_close_chem_1_pushButton.setStyleSheet(u"\n"
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
        self.debug_chem_1_label = QLabel(self.debug_control_groupBox)
        self.debug_chem_1_label.setObjectName(u"debug_chem_1_label")
        self.debug_chem_1_label.setGeometry(QRect(1190, 300, 131, 161))
        self.debug_chem_1_label.setFont(font3)
        self.debug_chem_1_label.setStyleSheet(u"background-color:rgb(188, 255, 224); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_chem_1_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.debug_open_chem_1_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_chem_1_pushButton.setObjectName(u"debug_open_chem_1_pushButton")
        self.debug_open_chem_1_pushButton.setGeometry(QRect(1200, 340, 111, 51))
        self.debug_open_chem_1_pushButton.setFont(font3)
        self.debug_open_chem_1_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_chem_2_label = QLabel(self.debug_control_groupBox)
        self.debug_chem_2_label.setObjectName(u"debug_chem_2_label")
        self.debug_chem_2_label.setGeometry(QRect(1340, 300, 131, 161))
        self.debug_chem_2_label.setFont(font3)
        self.debug_chem_2_label.setStyleSheet(u"background-color:rgb(156, 255, 159); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_chem_2_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.debug_close_chem_2_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_chem_2_pushButton.setObjectName(u"debug_close_chem_2_pushButton")
        self.debug_close_chem_2_pushButton.setGeometry(QRect(1350, 400, 111, 51))
        self.debug_close_chem_2_pushButton.setFont(font3)
        self.debug_close_chem_2_pushButton.setStyleSheet(u"\n"
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
        self.debug_open_chem_2_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_chem_2_pushButton.setObjectName(u"debug_open_chem_2_pushButton")
        self.debug_open_chem_2_pushButton.setGeometry(QRect(1350, 340, 111, 51))
        self.debug_open_chem_2_pushButton.setFont(font3)
        self.debug_open_chem_2_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_open_vale_chem_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_vale_chem_pushButton.setObjectName(u"debug_open_vale_chem_pushButton")
        self.debug_open_vale_chem_pushButton.setGeometry(QRect(1200, 510, 111, 51))
        self.debug_open_vale_chem_pushButton.setFont(font3)
        self.debug_open_vale_chem_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_vale_chem_label = QLabel(self.debug_control_groupBox)
        self.debug_vale_chem_label.setObjectName(u"debug_vale_chem_label")
        self.debug_vale_chem_label.setGeometry(QRect(1190, 470, 281, 101))
        self.debug_vale_chem_label.setFont(font3)
        self.debug_vale_chem_label.setStyleSheet(u"background-color:rgb(146, 220, 99); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_vale_chem_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.debug_close_vale_chem_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_vale_chem_pushButton.setObjectName(u"debug_close_vale_chem_pushButton")
        self.debug_close_vale_chem_pushButton.setGeometry(QRect(1350, 510, 111, 51))
        self.debug_close_vale_chem_pushButton.setFont(font3)
        self.debug_close_vale_chem_pushButton.setStyleSheet(u"\n"
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
        self.debug_open_water_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_open_water_pushButton.setObjectName(u"debug_open_water_pushButton")
        self.debug_open_water_pushButton.setGeometry(QRect(1220, 90, 111, 51))
        self.debug_open_water_pushButton.setFont(font3)
        self.debug_open_water_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.debug_close_water_pushButton = QPushButton(self.debug_control_groupBox)
        self.debug_close_water_pushButton.setObjectName(u"debug_close_water_pushButton")
        self.debug_close_water_pushButton.setGeometry(QRect(1340, 90, 111, 51))
        self.debug_close_water_pushButton.setFont(font3)
        self.debug_close_water_pushButton.setStyleSheet(u"\n"
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
        self.debug_wather_label = QLabel(self.debug_control_groupBox)
        self.debug_wather_label.setObjectName(u"debug_wather_label")
        self.debug_wather_label.setGeometry(QRect(1210, 50, 251, 101))
        self.debug_wather_label.setFont(font3)
        self.debug_wather_label.setStyleSheet(u"background-color:rgb(206, 242, 255); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_wather_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.debug_plate_1_label = QLabel(self.debug_control_groupBox)
        self.debug_plate_1_label.setObjectName(u"debug_plate_1_label")
        self.debug_plate_1_label.setGeometry(QRect(30, 230, 451, 341))
        self.debug_plate_1_label.setFont(font3)
        self.debug_plate_1_label.setStyleSheet(u"background-color:rgb(0, 0, 0); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_plate_1_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.debug_plate_2_label = QLabel(self.debug_control_groupBox)
        self.debug_plate_2_label.setObjectName(u"debug_plate_2_label")
        self.debug_plate_2_label.setGeometry(QRect(550, 40, 531, 531))
        self.debug_plate_2_label.setFont(font3)
        self.debug_plate_2_label.setStyleSheet(u"background-color:rgb(0, 0, 0); \n"
"color: black;\n"
"border: 2px solid ; \n"
"border-radius: 10px;")
        self.debug_plate_2_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.debug_plate_3_label = QLabel(self.debug_control_groupBox)
        self.debug_plate_3_label.setObjectName(u"debug_plate_3_label")
        self.debug_plate_3_label.setGeometry(QRect(1150, 40, 371, 541))
        self.debug_plate_3_label.setFont(font3)
        self.debug_plate_3_label.setStyleSheet(u"background-color:rgb(0, 0, 0); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.debug_plate_3_label.setAlignment(Qt.AlignmentFlag.AlignHCenter|Qt.AlignmentFlag.AlignTop)
        self.debug_plate_3_label.raise_()
        self.debug_plate_2_label.raise_()
        self.debug_plate_1_label.raise_()
        self.debug_wather_label.raise_()
        self.debug_vale_chem_label.raise_()
        self.debug_chem_1_label.raise_()
        self.debug_vale_mixer_label.raise_()
        self.debug_mixer_label.raise_()
        self.debug_fyash_label.raise_()
        self.debug_sand_label.raise_()
        self.debug_rock_1_label.raise_()
        self.debug_open_rock_1_pushButton.raise_()
        self.debug_close_rock_1_pushButton.raise_()
        self.debug_close_sand_pushButton.raise_()
        self.debug_open_sand_pushButton.raise_()
        self.debug_rock_label.raise_()
        self.debug_close_rock_2_pushButton.raise_()
        self.debug_open_rock_2_pushButton.raise_()
        self.debug_converyer_under_label.raise_()
        self.debug_open_converyer_under_pushButton.raise_()
        self.debug_close_converyer_under_pushButton.raise_()
        self.debug_converyer_top_label.raise_()
        self.debug_close_converyer_top_pushButton.raise_()
        self.debug_open_converyer_top_pushButton.raise_()
        self.debug_cement_label.raise_()
        self.debug_close_cement_pushButton.raise_()
        self.debug_open_cement_pushButton.raise_()
        self.debug_close_fyash_pushButton.raise_()
        self.debug_open_fyash_pushButton.raise_()
        self.debug_vale_cement_label.raise_()
        self.debug_open_vale_cement_pushButton.raise_()
        self.debug_close_vale_cement_pushButton.raise_()
        self.debug_vale_wather_label.raise_()
        self.debug_close_vale_water_pushButton.raise_()
        self.debug_open_vale_water_pushButton.raise_()
        self.debug_close_mixer_pushButton.raise_()
        self.debug_open_mixer_pushButton.raise_()
        self.debug_close_vale_mixer_pushButton.raise_()
        self.debug_open_vale_mixer_pushButton.raise_()
        self.debug_close_chem_1_pushButton.raise_()
        self.debug_open_chem_1_pushButton.raise_()
        self.debug_chem_2_label.raise_()
        self.debug_close_chem_2_pushButton.raise_()
        self.debug_open_chem_2_pushButton.raise_()
        self.debug_open_vale_chem_pushButton.raise_()
        self.debug_close_vale_chem_pushButton.raise_()
        self.debug_open_water_pushButton.raise_()
        self.debug_close_water_pushButton.raise_()
        self.debug_status_groupBox = QGroupBox(self.Debug_tab)
        self.debug_status_groupBox.setObjectName(u"debug_status_groupBox")
        self.debug_status_groupBox.setGeometry(QRect(10, 600, 1545, 171))
        self.debug_status_groupBox.setFont(font)
        self.debug_status_textEdit = QTextEdit(self.debug_status_groupBox)
        self.debug_status_textEdit.setObjectName(u"debug_status_textEdit")
        self.debug_status_textEdit.setGeometry(QRect(10, 40, 1525, 125))
        self.debug_status_textEdit.setFont(font3)
        self.debug_status_textEdit.setStyleSheet(u"background-color:rgb(255, 255, 255); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.tab.addTab(self.Debug_tab, "")
        self.Offset_tab = QWidget()
        self.Offset_tab.setObjectName(u"Offset_tab")
        self.offset_setting_formular_groupBox = QGroupBox(self.Offset_tab)
        self.offset_setting_formular_groupBox.setObjectName(u"offset_setting_formular_groupBox")
        self.offset_setting_formular_groupBox.setGeometry(QRect(20, 0, 1021, 331))
        self.offset_setting_formular_groupBox.setFont(font)
        self.offset_rock_1_label = QLabel(self.offset_setting_formular_groupBox)
        self.offset_rock_1_label.setObjectName(u"offset_rock_1_label")
        self.offset_rock_1_label.setGeometry(QRect(20, 40, 71, 61))
        self.offset_rock_1_label.setFont(font3)
        self.offset_rock_1_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_rock_1_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_rock_1_lineEdit = QLineEdit(self.offset_setting_formular_groupBox)
        self.offset_rock_1_lineEdit.setObjectName(u"offset_rock_1_lineEdit")
        self.offset_rock_1_lineEdit.setGeometry(QRect(100, 40, 91, 61))
        self.offset_rock_1_lineEdit.setFont(font1)
        self.offset_rock_1_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.offset_rock_1_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_sand_1_label = QLabel(self.offset_setting_formular_groupBox)
        self.offset_sand_1_label.setObjectName(u"offset_sand_1_label")
        self.offset_sand_1_label.setGeometry(QRect(380, 40, 71, 61))
        self.offset_sand_1_label.setFont(font3)
        self.offset_sand_1_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_sand_1_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_sand_1_lineEdit = QLineEdit(self.offset_setting_formular_groupBox)
        self.offset_sand_1_lineEdit.setObjectName(u"offset_sand_1_lineEdit")
        self.offset_sand_1_lineEdit.setGeometry(QRect(460, 40, 91, 61))
        self.offset_sand_1_lineEdit.setFont(font1)
        self.offset_sand_1_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.offset_sand_1_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_rock_2_label = QLabel(self.offset_setting_formular_groupBox)
        self.offset_rock_2_label.setObjectName(u"offset_rock_2_label")
        self.offset_rock_2_label.setGeometry(QRect(20, 145, 71, 61))
        self.offset_rock_2_label.setFont(font3)
        self.offset_rock_2_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_rock_2_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_rock_2_lineEdit = QLineEdit(self.offset_setting_formular_groupBox)
        self.offset_rock_2_lineEdit.setObjectName(u"offset_rock_2_lineEdit")
        self.offset_rock_2_lineEdit.setGeometry(QRect(100, 145, 91, 61))
        self.offset_rock_2_lineEdit.setFont(font1)
        self.offset_rock_2_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.offset_rock_2_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_sand_2_label = QLabel(self.offset_setting_formular_groupBox)
        self.offset_sand_2_label.setObjectName(u"offset_sand_2_label")
        self.offset_sand_2_label.setGeometry(QRect(380, 145, 71, 61))
        self.offset_sand_2_label.setFont(font3)
        self.offset_sand_2_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_sand_2_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_sand_2_lineEdit = QLineEdit(self.offset_setting_formular_groupBox)
        self.offset_sand_2_lineEdit.setObjectName(u"offset_sand_2_lineEdit")
        self.offset_sand_2_lineEdit.setGeometry(QRect(460, 145, 91, 61))
        self.offset_sand_2_lineEdit.setFont(font1)
        self.offset_sand_2_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.offset_sand_2_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_cement_label = QLabel(self.offset_setting_formular_groupBox)
        self.offset_cement_label.setObjectName(u"offset_cement_label")
        self.offset_cement_label.setGeometry(QRect(20, 250, 71, 61))
        self.offset_cement_label.setFont(font3)
        self.offset_cement_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_cement_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_fyash_label = QLabel(self.offset_setting_formular_groupBox)
        self.offset_fyash_label.setObjectName(u"offset_fyash_label")
        self.offset_fyash_label.setGeometry(QRect(380, 250, 71, 61))
        self.offset_fyash_label.setFont(font3)
        self.offset_fyash_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_fyash_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_cement_lineEdit = QLineEdit(self.offset_setting_formular_groupBox)
        self.offset_cement_lineEdit.setObjectName(u"offset_cement_lineEdit")
        self.offset_cement_lineEdit.setGeometry(QRect(100, 250, 91, 61))
        self.offset_cement_lineEdit.setFont(font1)
        self.offset_cement_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.offset_cement_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_fyash_lineEdit = QLineEdit(self.offset_setting_formular_groupBox)
        self.offset_fyash_lineEdit.setObjectName(u"offset_fyash_lineEdit")
        self.offset_fyash_lineEdit.setGeometry(QRect(460, 250, 91, 61))
        self.offset_fyash_lineEdit.setFont(font1)
        self.offset_fyash_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.offset_fyash_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_wather_label = QLabel(self.offset_setting_formular_groupBox)
        self.offset_wather_label.setObjectName(u"offset_wather_label")
        self.offset_wather_label.setGeometry(QRect(740, 40, 71, 61))
        self.offset_wather_label.setFont(font3)
        self.offset_wather_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_wather_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_chem_1_label = QLabel(self.offset_setting_formular_groupBox)
        self.offset_chem_1_label.setObjectName(u"offset_chem_1_label")
        self.offset_chem_1_label.setGeometry(QRect(740, 145, 71, 61))
        self.offset_chem_1_label.setFont(font3)
        self.offset_chem_1_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_chem_1_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_wather_lineEdit = QLineEdit(self.offset_setting_formular_groupBox)
        self.offset_wather_lineEdit.setObjectName(u"offset_wather_lineEdit")
        self.offset_wather_lineEdit.setGeometry(QRect(820, 40, 91, 61))
        self.offset_wather_lineEdit.setFont(font1)
        self.offset_wather_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.offset_wather_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_chem_1_lineEdit = QLineEdit(self.offset_setting_formular_groupBox)
        self.offset_chem_1_lineEdit.setObjectName(u"offset_chem_1_lineEdit")
        self.offset_chem_1_lineEdit.setGeometry(QRect(820, 145, 91, 61))
        self.offset_chem_1_lineEdit.setFont(font1)
        self.offset_chem_1_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.offset_chem_1_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_chem_2_lineEdit = QLineEdit(self.offset_setting_formular_groupBox)
        self.offset_chem_2_lineEdit.setObjectName(u"offset_chem_2_lineEdit")
        self.offset_chem_2_lineEdit.setGeometry(QRect(820, 250, 91, 61))
        self.offset_chem_2_lineEdit.setFont(font1)
        self.offset_chem_2_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.offset_chem_2_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_chem_2_label = QLabel(self.offset_setting_formular_groupBox)
        self.offset_chem_2_label.setObjectName(u"offset_chem_2_label")
        self.offset_chem_2_label.setGeometry(QRect(740, 250, 71, 61))
        self.offset_chem_2_label.setFont(font3)
        self.offset_chem_2_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_chem_2_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_unit_time_11 = QLabel(self.offset_setting_formular_groupBox)
        self.offset_unit_time_11.setObjectName(u"offset_unit_time_11")
        self.offset_unit_time_11.setGeometry(QRect(200, 40, 81, 61))
        self.offset_unit_time_11.setFont(font3)
        self.offset_unit_time_11.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_unit_time_11.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_unit_time_12 = QLabel(self.offset_setting_formular_groupBox)
        self.offset_unit_time_12.setObjectName(u"offset_unit_time_12")
        self.offset_unit_time_12.setGeometry(QRect(200, 145, 81, 61))
        self.offset_unit_time_12.setFont(font3)
        self.offset_unit_time_12.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_unit_time_12.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_unit_time_13 = QLabel(self.offset_setting_formular_groupBox)
        self.offset_unit_time_13.setObjectName(u"offset_unit_time_13")
        self.offset_unit_time_13.setGeometry(QRect(200, 250, 81, 61))
        self.offset_unit_time_13.setFont(font3)
        self.offset_unit_time_13.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_unit_time_13.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.line = QFrame(self.offset_setting_formular_groupBox)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(325, 25, 5, 301))
        self.line.setStyleSheet(u"background:rgb(0, 0, 0)")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)
        self.offset_unit_time_8 = QLabel(self.offset_setting_formular_groupBox)
        self.offset_unit_time_8.setObjectName(u"offset_unit_time_8")
        self.offset_unit_time_8.setGeometry(QRect(560, 40, 81, 61))
        self.offset_unit_time_8.setFont(font3)
        self.offset_unit_time_8.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_unit_time_8.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_unit_time_9 = QLabel(self.offset_setting_formular_groupBox)
        self.offset_unit_time_9.setObjectName(u"offset_unit_time_9")
        self.offset_unit_time_9.setGeometry(QRect(560, 145, 81, 61))
        self.offset_unit_time_9.setFont(font3)
        self.offset_unit_time_9.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_unit_time_9.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_unit_time_10 = QLabel(self.offset_setting_formular_groupBox)
        self.offset_unit_time_10.setObjectName(u"offset_unit_time_10")
        self.offset_unit_time_10.setGeometry(QRect(560, 250, 81, 61))
        self.offset_unit_time_10.setFont(font3)
        self.offset_unit_time_10.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_unit_time_10.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.line_2 = QFrame(self.offset_setting_formular_groupBox)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(685, 25, 5, 301))
        self.line_2.setStyleSheet(u"background:rgb(0, 0, 0)")
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.offset_unit_time_5 = QLabel(self.offset_setting_formular_groupBox)
        self.offset_unit_time_5.setObjectName(u"offset_unit_time_5")
        self.offset_unit_time_5.setGeometry(QRect(920, 40, 81, 61))
        self.offset_unit_time_5.setFont(font3)
        self.offset_unit_time_5.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_unit_time_5.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_unit_time_6 = QLabel(self.offset_setting_formular_groupBox)
        self.offset_unit_time_6.setObjectName(u"offset_unit_time_6")
        self.offset_unit_time_6.setGeometry(QRect(920, 145, 81, 61))
        self.offset_unit_time_6.setFont(font3)
        self.offset_unit_time_6.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_unit_time_6.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_unit_time_7 = QLabel(self.offset_setting_formular_groupBox)
        self.offset_unit_time_7.setObjectName(u"offset_unit_time_7")
        self.offset_unit_time_7.setGeometry(QRect(920, 250, 81, 61))
        self.offset_unit_time_7.setFont(font3)
        self.offset_unit_time_7.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_unit_time_7.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_chem_2_label.raise_()
        self.offset_cement_label.raise_()
        self.offset_rock_1_label.raise_()
        self.offset_rock_1_lineEdit.raise_()
        self.offset_sand_1_label.raise_()
        self.offset_sand_1_lineEdit.raise_()
        self.offset_rock_2_label.raise_()
        self.offset_rock_2_lineEdit.raise_()
        self.offset_sand_2_label.raise_()
        self.offset_sand_2_lineEdit.raise_()
        self.offset_fyash_label.raise_()
        self.offset_cement_lineEdit.raise_()
        self.offset_fyash_lineEdit.raise_()
        self.offset_wather_label.raise_()
        self.offset_chem_1_label.raise_()
        self.offset_wather_lineEdit.raise_()
        self.offset_chem_1_lineEdit.raise_()
        self.offset_chem_2_lineEdit.raise_()
        self.offset_unit_time_11.raise_()
        self.offset_unit_time_12.raise_()
        self.offset_unit_time_13.raise_()
        self.line.raise_()
        self.offset_unit_time_8.raise_()
        self.offset_unit_time_9.raise_()
        self.offset_unit_time_10.raise_()
        self.line_2.raise_()
        self.offset_unit_time_5.raise_()
        self.offset_unit_time_6.raise_()
        self.offset_unit_time_7.raise_()
        self.offset_setting_time_groupBox = QGroupBox(self.Offset_tab)
        self.offset_setting_time_groupBox.setObjectName(u"offset_setting_time_groupBox")
        self.offset_setting_time_groupBox.setGeometry(QRect(1050, 0, 501, 331))
        self.offset_setting_time_groupBox.setFont(font)
        self.offset_converyer_silo_time_label = QLabel(self.offset_setting_time_groupBox)
        self.offset_converyer_silo_time_label.setObjectName(u"offset_converyer_silo_time_label")
        self.offset_converyer_silo_time_label.setGeometry(QRect(20, 40, 381, 61))
        self.offset_converyer_silo_time_label.setFont(font3)
        self.offset_converyer_silo_time_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_converyer_silo_time_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_converyer_silo_time_lineEdit = QLineEdit(self.offset_setting_time_groupBox)
        self.offset_converyer_silo_time_lineEdit.setObjectName(u"offset_converyer_silo_time_lineEdit")
        self.offset_converyer_silo_time_lineEdit.setGeometry(QRect(300, 50, 91, 41))
        self.offset_converyer_silo_time_lineEdit.setFont(font1)
        self.offset_converyer_silo_time_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.offset_converyer_silo_time_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_opan_cement_time_label = QLabel(self.offset_setting_time_groupBox)
        self.offset_opan_cement_time_label.setObjectName(u"offset_opan_cement_time_label")
        self.offset_opan_cement_time_label.setGeometry(QRect(20, 110, 381, 61))
        self.offset_opan_cement_time_label.setFont(font3)
        self.offset_opan_cement_time_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_opan_cement_time_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_opan_cement_time_lineEdit = QLineEdit(self.offset_setting_time_groupBox)
        self.offset_opan_cement_time_lineEdit.setObjectName(u"offset_opan_cement_time_lineEdit")
        self.offset_opan_cement_time_lineEdit.setGeometry(QRect(300, 120, 91, 41))
        self.offset_opan_cement_time_lineEdit.setFont(font1)
        self.offset_opan_cement_time_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.offset_opan_cement_time_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_run_mixer_time_lineEdit = QLineEdit(self.offset_setting_time_groupBox)
        self.offset_run_mixer_time_lineEdit.setObjectName(u"offset_run_mixer_time_lineEdit")
        self.offset_run_mixer_time_lineEdit.setGeometry(QRect(300, 190, 91, 41))
        self.offset_run_mixer_time_lineEdit.setFont(font1)
        self.offset_run_mixer_time_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.offset_run_mixer_time_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_run_mixer_time_label = QLabel(self.offset_setting_time_groupBox)
        self.offset_run_mixer_time_label.setObjectName(u"offset_run_mixer_time_label")
        self.offset_run_mixer_time_label.setGeometry(QRect(20, 180, 381, 61))
        self.offset_run_mixer_time_label.setFont(font3)
        self.offset_run_mixer_time_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_run_mixer_time_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_time_next_load_lineEdit = QLineEdit(self.offset_setting_time_groupBox)
        self.offset_time_next_load_lineEdit.setObjectName(u"offset_time_next_load_lineEdit")
        self.offset_time_next_load_lineEdit.setGeometry(QRect(300, 260, 91, 41))
        self.offset_time_next_load_lineEdit.setFont(font1)
        self.offset_time_next_load_lineEdit.setStyleSheet(u"background:rgb(238, 238, 238)")
        self.offset_time_next_load_lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_time_next_load_label = QLabel(self.offset_setting_time_groupBox)
        self.offset_time_next_load_label.setObjectName(u"offset_time_next_load_label")
        self.offset_time_next_load_label.setGeometry(QRect(20, 250, 381, 61))
        self.offset_time_next_load_label.setFont(font3)
        self.offset_time_next_load_label.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_time_next_load_label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_unit_time = QLabel(self.offset_setting_time_groupBox)
        self.offset_unit_time.setObjectName(u"offset_unit_time")
        self.offset_unit_time.setGeometry(QRect(410, 40, 71, 61))
        self.offset_unit_time.setFont(font3)
        self.offset_unit_time.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_unit_time.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_unit_time_2 = QLabel(self.offset_setting_time_groupBox)
        self.offset_unit_time_2.setObjectName(u"offset_unit_time_2")
        self.offset_unit_time_2.setGeometry(QRect(410, 110, 71, 61))
        self.offset_unit_time_2.setFont(font3)
        self.offset_unit_time_2.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_unit_time_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_unit_time_3 = QLabel(self.offset_setting_time_groupBox)
        self.offset_unit_time_3.setObjectName(u"offset_unit_time_3")
        self.offset_unit_time_3.setGeometry(QRect(410, 180, 71, 61))
        self.offset_unit_time_3.setFont(font3)
        self.offset_unit_time_3.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_unit_time_3.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_unit_time_4 = QLabel(self.offset_setting_time_groupBox)
        self.offset_unit_time_4.setObjectName(u"offset_unit_time_4")
        self.offset_unit_time_4.setGeometry(QRect(410, 250, 71, 61))
        self.offset_unit_time_4.setFont(font3)
        self.offset_unit_time_4.setStyleSheet(u"background-color:rgb(216, 255, 180); \n"
"color: black;\n"
"border: 2px solid; \n"
"border-radius: 10px;")
        self.offset_unit_time_4.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.offset_time_next_load_label.raise_()
        self.offset_run_mixer_time_label.raise_()
        self.offset_converyer_silo_time_label.raise_()
        self.offset_converyer_silo_time_lineEdit.raise_()
        self.offset_opan_cement_time_label.raise_()
        self.offset_opan_cement_time_lineEdit.raise_()
        self.offset_run_mixer_time_lineEdit.raise_()
        self.offset_time_next_load_lineEdit.raise_()
        self.offset_unit_time.raise_()
        self.offset_unit_time_2.raise_()
        self.offset_unit_time_3.raise_()
        self.offset_unit_time_4.raise_()
        self.offset_cancel_pushButton = QPushButton(self.Offset_tab)
        self.offset_cancel_pushButton.setObjectName(u"offset_cancel_pushButton")
        self.offset_cancel_pushButton.setGeometry(QRect(1390, 340, 151, 61))
        self.offset_cancel_pushButton.setFont(font3)
        self.offset_cancel_pushButton.setStyleSheet(u"\n"
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
        self.offset_edite_pushButton = QPushButton(self.Offset_tab)
        self.offset_edite_pushButton.setObjectName(u"offset_edite_pushButton")
        self.offset_edite_pushButton.setGeometry(QRect(1220, 340, 151, 61))
        self.offset_edite_pushButton.setFont(font3)
        self.offset_edite_pushButton.setStyleSheet(u"\n"
"QPushButton {\n"
"   	background:rgb(0, 170, 127);\n"
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
        self.offset_save_pushButton = QPushButton(self.Offset_tab)
        self.offset_save_pushButton.setObjectName(u"offset_save_pushButton")
        self.offset_save_pushButton.setGeometry(QRect(1050, 340, 151, 61))
        self.offset_save_pushButton.setFont(font3)
        self.offset_save_pushButton.setStyleSheet(u"QPushButton {\n"
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
        self.tab.addTab(self.Offset_tab, "")
        Control_Plant.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Control_Plant)
        self.statusbar.setObjectName(u"statusbar")
        Control_Plant.setStatusBar(self.statusbar)

        self.retranslateUi(Control_Plant)

        self.tab.setCurrentIndex(0)


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
        self.reg_name_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e0a\u0e37\u0e48\u0e2d", None))
        self.reg_telephone_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1a\u0e2d\u0e23\u0e4c", None))
        self.reg_address_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e17\u0e35\u0e48\u0e2d\u0e22\u0e39\u0e48", None))
        self.reg_number_car_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e17\u0e30\u0e40\u0e1a\u0e35\u0e22\u0e19\u0e23\u0e16", None))
        self.reg_comment_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e21\u0e32\u0e22\u0e40\u0e2b\u0e15\u0e38", None))
        self.groupBox.setTitle("")
        self.reg_child_cement_comboBox.setItemText(0, QCoreApplication.translate("Control_Plant", u"\u0e15\u0e49\u0e2d\u0e07\u0e01\u0e32\u0e23\u0e40\u0e01\u0e47\u0e1a", None))
        self.reg_child_cement_comboBox.setItemText(1, QCoreApplication.translate("Control_Plant", u"\u0e44\u0e21\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e01\u0e32\u0e23\u0e40\u0e01\u0e47\u0e1a", None))

        self.reg_child_cement_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e25\u0e39\u0e01\u0e1b\u0e39\u0e19", None))
        self.reg_amount_unit_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e08\u0e33\u0e19\u0e27\u0e19", None))
        self.reg_amount_unit_label_2.setText(QCoreApplication.translate("Control_Plant", u"\u0e04\u0e34\u0e27", None))
        self.reg_formula_name_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e0a\u0e37\u0e48\u0e2d\u0e2a\u0e39\u0e15\u0e23", None))
        self.reg_save_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1a\u0e31\u0e19\u0e17\u0e36\u0e01", None))
        self.reg_clear_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e04\u0e25\u0e35\u0e22\u0e02\u0e49\u0e2d\u0e21\u0e39\u0e25", None))
        self.reg_save_new_customer_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1a\u0e31\u0e19\u0e17\u0e36\u0e01\u0e25\u0e39\u0e01\u0e04\u0e49\u0e32\u0e43\u0e2b\u0e21\u0e48", None))
        self.reg_dateTimeEdit.setDisplayFormat(QCoreApplication.translate("Control_Plant", u"d/M/yyyy h:mm AP", None))
        self.reg_date_time_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e27\u0e31\u0e19\u0e40\u0e27\u0e25\u0e32", None))
        self.reg_update_time_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e2d\u0e31\u0e1a\u0e40\u0e14\u0e15\u0e40\u0e27\u0e25\u0e32", None))
        ___qtreewidgetitem1 = self.reg_list_customer_treeWidget.headerItem()
        ___qtreewidgetitem1.setText(3, QCoreApplication.translate("Control_Plant", u"\u0e17\u0e35\u0e48\u0e2d\u0e22\u0e39\u0e48", None));
        ___qtreewidgetitem1.setText(2, QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1a\u0e2d\u0e23\u0e4c", None));
        ___qtreewidgetitem1.setText(1, QCoreApplication.translate("Control_Plant", u"\u0e0a\u0e37\u0e48\u0e2d", None));
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("Control_Plant", u"\u0e25\u0e33\u0e14\u0e31\u0e1a", None));
        self.reg_lis_custommer_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e23\u0e32\u0e22\u0e0a\u0e37\u0e48\u0e2d\u0e25\u0e39\u0e01\u0e04\u0e49\u0e32", None))
        self.reg_delete_customer_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e25\u0e1a\u0e25\u0e39\u0e01\u0e04\u0e49\u0e32\u0e17\u0e35\u0e48\u0e40\u0e25\u0e37\u0e2d\u0e01", None))
        self.tab.setTabText(self.tab.indexOf(self.Register_tab), QCoreApplication.translate("Control_Plant", u"Register", None))
        self.mix_detail_customer_groupBox.setTitle("")
        self.mix_customer_name_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e0a\u0e37\u0e48\u0e2d\u0e25\u0e39\u0e01\u0e04\u0e49\u0e32", None))
        self.mix_customer_formula_name_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e0a\u0e37\u0e48\u0e2d\u0e2a\u0e39\u0e15\u0e23", None))
        self.mix_customer_phone_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1a\u0e2d\u0e23\u0e4c\u0e42\u0e17\u0e23", None))
        self.mix_number_cube_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e08\u0e33\u0e19\u0e27\u0e19", None))
        self.mix_number_cube_unit_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e04\u0e34\u0e27", None))
        self.mix_main_monitor_groupBox.setTitle("")
        self.mix_monitor_rock_1_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e19 1", None))
        self.mix_monitor_sand_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e17\u0e23\u0e32\u0e22", None))
        self.mix_monitor_rock_2_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e19 2", None))
        self.mix_monitor_fyash_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e16\u0e49\u0e32\u0e25\u0e2d\u0e22", None))
        self.mix_monitor_cement_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e0b\u0e35\u0e40\u0e21\u0e19\u0e15\u0e4c", None))
        self.mix_monitor_wather_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33", None))
        self.mix_monitor_chem_2_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32 2", None))
        self.mix_monitor_chem_1_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32 1", None))
        self.mix_monitor_mixer_label.setText(QCoreApplication.translate("Control_Plant", u"MIXER \u0e1c\u0e2a\u0e21", None))
        self.mix_monitor_converyer_rock_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2a\u0e32\u0e22\u0e1e\u0e32\u0e19\u0e25\u0e33\u0e40\u0e25\u0e35\u0e22\u0e07", None))
        self.mix_monitor_vale_fyash_and_cement_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e27\u0e32\u0e25\u0e4c\u0e27\u0e1b\u0e39\u0e19/\u0e40\u0e16\u0e49\u0e32\u0e25\u0e2d\u0e22", None))
        self.mix_monitor_vale_wather_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e27\u0e32\u0e25\u0e4c\u0e27\u0e19\u0e49\u0e33", None))
        self.mix_monitor_pump_chem_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e31\u0e49\u0e21\u0e19\u0e49\u0e33\u0e22\u0e32", None))
        self.mix_monitor_main_vale_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e27\u0e32\u0e25\u0e4c\u0e27\u0e1b\u0e25\u0e48\u0e2d\u0e22\u0e1b\u0e39\u0e19", None))
        self.mix_monitor_sum_rock_and_sand_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e23\u0e27\u0e21\u0e17\u0e31\u0e49\u0e07\u0e2b\u0e21\u0e14", None))
        self.mix_monitor_sum_chem_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e23\u0e27\u0e21\u0e17\u0e31\u0e49\u0e07\u0e2b\u0e21\u0e14", None))
        self.mix_monitor_sum_fyash_and_cement_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e23\u0e27\u0e21\u0e17\u0e31\u0e49\u0e07\u0e2b\u0e21\u0e14", None))
        self.mix_monitor_status_groupBox.setTitle(QCoreApplication.translate("Control_Plant", u"\u0e2a\u0e16\u0e32\u0e19\u0e30\u0e01\u0e32\u0e23\u0e17\u0e33\u0e07\u0e32\u0e19", None))
        self.mix_wieght_monitor_groupBox.setTitle(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e2b\u0e19\u0e31\u0e01", None))
        self.mix_wieght_Loaded_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e42\u0e2b\u0e25\u0e14\u0e41\u0e25\u0e49\u0e27", None))
        self.mix_wieght_target_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e49\u0e32\u0e2b\u0e21\u0e32\u0e22", None))
        self.mix_wieght_Loaded_rock_1_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e19 1", None))
        self.mix_wieght_Loaded_sand_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e17\u0e23\u0e32\u0e22", None))
        self.mix_wieght_Loaded_rock_2_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e19 2", None))
        self.mix_wieght_Loaded_cement_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e0b\u0e35\u0e40\u0e21\u0e19\u0e15\u0e4c", None))
        self.mix_wieght_Loaded_fyash_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e16\u0e49\u0e32\u0e25\u0e2d\u0e22", None))
        self.mix_wieght_Loaded_wather_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33", None))
        self.mix_wieght_Loaded_chem_1_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32 1", None))
        self.mix_wieght_Loaded_chem_2_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32 2", None))
        self.mix_result_groupBox.setTitle(QCoreApplication.translate("Control_Plant", u"\u0e2a\u0e23\u0e38\u0e1b\u0e01\u0e32\u0e23\u0e42\u0e2b\u0e25\u0e14", None))
        self.mix_result_load_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e39\u0e19\u0e17\u0e35\u0e48\u0e15\u0e49\u0e2d\u0e07\u0e01\u0e32\u0e23\u0e42\u0e2b\u0e25\u0e14", None))
        self.mix_result_load_unit_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e04\u0e34\u0e27\u0e1a\u0e34\u0e04", None))
        self.mix_result_mix_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e39\u0e19\u0e17\u0e35\u0e48\u0e2d\u0e22\u0e39\u0e48\u0e23\u0e30\u0e2b\u0e27\u0e48\u0e32\u0e07\u0e1c\u0e2a\u0e21", None))
        self.mix_result_mix_success_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e39\u0e19\u0e17\u0e35\u0e48\u0e1c\u0e2a\u0e21\u0e40\u0e2a\u0e23\u0e47\u0e08", None))
        self.mix_result_mix_unit_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e04\u0e34\u0e27\u0e1a\u0e34\u0e04", None))
        self.mix_result_mix_success_unit_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e04\u0e34\u0e27\u0e1a\u0e34\u0e04", None))
        self.mix_cancel_load_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e22\u0e01\u0e40\u0e25\u0e34\u0e01\u0e01\u0e32\u0e23\u0e42\u0e2b\u0e25\u0e14", None))
        self.mix_start_load_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e23\u0e34\u0e48\u0e21\u0e01\u0e32\u0e23\u0e42\u0e2b\u0e25\u0e14", None))
        self.tab.setTabText(self.tab.indexOf(self.Mix_tab), QCoreApplication.translate("Control_Plant", u"Mixer", None))
        ___qtreewidgetitem2 = self.for_formula_treeWidget.headerItem()
        ___qtreewidgetitem2.setText(11, QCoreApplication.translate("Control_Plant", u"slump", None));
        ___qtreewidgetitem2.setText(10, QCoreApplication.translate("Control_Plant", u"age", None));
        ___qtreewidgetitem2.setText(9, QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32\u0e40\u0e04\u0e21\u0e35 2", None));
        ___qtreewidgetitem2.setText(8, QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32\u0e40\u0e04\u0e21\u0e35 1", None));
        ___qtreewidgetitem2.setText(7, QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33", None));
        ___qtreewidgetitem2.setText(6, QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e39\u0e19", None));
        ___qtreewidgetitem2.setText(5, QCoreApplication.translate("Control_Plant", u"\u0e40\u0e16\u0e49\u0e32\u0e25\u0e2d\u0e22", None));
        ___qtreewidgetitem2.setText(4, QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e192", None));
        ___qtreewidgetitem2.setText(3, QCoreApplication.translate("Control_Plant", u"\u0e17\u0e23\u0e32\u0e22", None));
        ___qtreewidgetitem2.setText(2, QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e191", None));
        ___qtreewidgetitem2.setText(1, QCoreApplication.translate("Control_Plant", u"\u0e0a\u0e37\u0e48\u0e2d\u0e2a\u0e39\u0e15\u0e23", None));
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("Control_Plant", u"\u0e25\u0e33\u0e14\u0e31\u0e1a", None));
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
        self.tab.setTabText(self.tab.indexOf(self.Formula_tab), QCoreApplication.translate("Control_Plant", u"Formula", None))
        self.debug_control_groupBox.setTitle(QCoreApplication.translate("Control_Plant", u"\u0e04\u0e27\u0e1a\u0e04\u0e38\u0e21", None))
        self.debug_open_rock_1_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_rock_1_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e19 1", None))
        self.debug_close_rock_1_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_close_sand_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_open_sand_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_sand_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e17\u0e23\u0e32\u0e22", None))
        self.debug_rock_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e19 2", None))
        self.debug_close_rock_2_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_open_rock_2_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_converyer_under_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2a\u0e32\u0e22\u0e1e\u0e32\u0e19\u0e25\u0e48\u0e32\u0e07", None))
        self.debug_open_converyer_under_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_close_converyer_under_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_converyer_top_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2a\u0e32\u0e22\u0e1e\u0e32\u0e19\u0e1a\u0e19", None))
        self.debug_close_converyer_top_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_open_converyer_top_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_cement_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e0b\u0e35\u0e40\u0e21\u0e19\u0e15\u0e4c", None))
        self.debug_close_cement_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_open_cement_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_close_fyash_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_open_fyash_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_fyash_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e16\u0e49\u0e32\u0e25\u0e2d\u0e22", None))
        self.debug_vale_cement_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e27\u0e32\u0e25\u0e4c\u0e27\u0e1b\u0e39\u0e19/\u0e0b\u0e35\u0e40\u0e21\u0e19\u0e15\u0e4c", None))
        self.debug_open_vale_cement_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_close_vale_cement_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_vale_wather_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e27\u0e32\u0e25\u0e4c\u0e27\u0e19\u0e49\u0e33", None))
        self.debug_close_vale_water_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_open_vale_water_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_close_mixer_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_open_mixer_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_mixer_label.setText(QCoreApplication.translate("Control_Plant", u"MIXER", None))
        self.debug_close_vale_mixer_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_vale_mixer_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e27\u0e32\u0e25\u0e4c\u0e25\u0e1b\u0e25\u0e48\u0e2d\u0e22\u0e1b\u0e39\u0e19", None))
        self.debug_open_vale_mixer_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_close_chem_1_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_chem_1_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32\u0e40\u0e04\u0e21\u0e35 1", None))
        self.debug_open_chem_1_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_chem_2_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32\u0e40\u0e04\u0e21\u0e35 2", None))
        self.debug_close_chem_2_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_open_chem_2_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_open_vale_chem_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_vale_chem_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e27\u0e32\u0e25\u0e4c\u0e25\u0e19\u0e49\u0e33\u0e22\u0e32", None))
        self.debug_close_vale_chem_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_open_water_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e1b\u0e34\u0e14", None))
        self.debug_close_water_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1b\u0e34\u0e14", None))
        self.debug_wather_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33", None))
        self.debug_plate_1_label.setText("")
        self.debug_plate_2_label.setText("")
        self.debug_plate_3_label.setText("")
        self.debug_status_groupBox.setTitle(QCoreApplication.translate("Control_Plant", u"\u0e2a\u0e16\u0e32\u0e19\u0e30", None))
        self.tab.setTabText(self.tab.indexOf(self.Debug_tab), QCoreApplication.translate("Control_Plant", u"Debug", None))
        self.offset_setting_formular_groupBox.setTitle(QCoreApplication.translate("Control_Plant", u"Offset Setting \u0e2a\u0e48\u0e27\u0e19\u0e1c\u0e2a\u0e21", None))
        self.offset_rock_1_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e19 1", None))
        self.offset_sand_1_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e17\u0e23\u0e32\u0e22 1", None))
        self.offset_rock_2_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e2b\u0e34\u0e19 2", None))
        self.offset_sand_2_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e17\u0e23\u0e32\u0e22 2", None))
        self.offset_cement_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e0b\u0e35\u0e40\u0e21\u0e19\u0e15\u0e4c", None))
        self.offset_fyash_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e44\u0e1f\u0e41\u0e2d\u0e0a", None))
        self.offset_wather_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33", None))
        self.offset_chem_1_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32 1", None))
        self.offset_chem_2_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e19\u0e49\u0e33\u0e22\u0e32 2", None))
        self.offset_unit_time_11.setText(QCoreApplication.translate("Control_Plant", u"\u0e01\u0e34\u0e42\u0e25\u0e01\u0e23\u0e31\u0e21", None))
        self.offset_unit_time_12.setText(QCoreApplication.translate("Control_Plant", u"\u0e01\u0e34\u0e42\u0e25\u0e01\u0e23\u0e31\u0e21", None))
        self.offset_unit_time_13.setText(QCoreApplication.translate("Control_Plant", u"\u0e01\u0e34\u0e42\u0e25\u0e01\u0e23\u0e31\u0e21", None))
        self.offset_unit_time_8.setText(QCoreApplication.translate("Control_Plant", u"\u0e01\u0e34\u0e42\u0e25\u0e01\u0e23\u0e31\u0e21", None))
        self.offset_unit_time_9.setText(QCoreApplication.translate("Control_Plant", u"\u0e01\u0e34\u0e42\u0e25\u0e01\u0e23\u0e31\u0e21", None))
        self.offset_unit_time_10.setText(QCoreApplication.translate("Control_Plant", u"\u0e01\u0e34\u0e42\u0e25\u0e01\u0e23\u0e31\u0e21", None))
        self.offset_unit_time_5.setText(QCoreApplication.translate("Control_Plant", u"\u0e01\u0e34\u0e42\u0e25\u0e01\u0e23\u0e31\u0e21", None))
        self.offset_unit_time_6.setText(QCoreApplication.translate("Control_Plant", u"\u0e01\u0e34\u0e42\u0e25\u0e01\u0e23\u0e31\u0e21", None))
        self.offset_unit_time_7.setText(QCoreApplication.translate("Control_Plant", u"\u0e01\u0e34\u0e42\u0e25\u0e01\u0e23\u0e31\u0e21", None))
        self.offset_setting_time_groupBox.setTitle(QCoreApplication.translate("Control_Plant", u"Offset Setting \u0e40\u0e27\u0e25\u0e32\u0e43\u0e19\u0e01\u0e32\u0e23\u0e17\u0e33\u0e07\u0e32\u0e19", None))
        self.offset_converyer_silo_time_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e27\u0e25\u0e32\u0e01\u0e48\u0e2d\u0e19\u0e2a\u0e32\u0e22\u0e1e\u0e32\u0e19\u0e14\u0e49\u0e32\u0e19\u0e25\u0e48\u0e32\u0e07\u0e17\u0e33\u0e07\u0e32\u0e19", None))
        self.offset_opan_cement_time_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e27\u0e25\u0e32\u0e01\u0e48\u0e2d\u0e19\u0e1b\u0e25\u0e48\u0e2d\u0e22\u0e1b\u0e39\u0e19\u0e1e\u0e23\u0e49\u0e2d\u0e21\u0e19\u0e49\u0e33", None))
        self.offset_run_mixer_time_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e27\u0e25\u0e32\u0e43\u0e19\u0e01\u0e32\u0e23 run mixer", None))
        self.offset_time_next_load_label.setText(QCoreApplication.translate("Control_Plant", u"\u0e40\u0e27\u0e25\u0e32\u0e01\u0e48\u0e2d\u0e19\u0e17\u0e35\u0e48\u0e08\u0e30\u0e40\u0e23\u0e34\u0e48\u0e21\u0e42\u0e2b\u0e25\u0e14\u0e15\u0e48\u0e2d\u0e44\u0e1b", None))
        self.offset_unit_time.setText(QCoreApplication.translate("Control_Plant", u"\u0e27\u0e34\u0e19\u0e32\u0e17\u0e35", None))
        self.offset_unit_time_2.setText(QCoreApplication.translate("Control_Plant", u"\u0e27\u0e34\u0e19\u0e32\u0e17\u0e35", None))
        self.offset_unit_time_3.setText(QCoreApplication.translate("Control_Plant", u"\u0e27\u0e34\u0e19\u0e32\u0e17\u0e35", None))
        self.offset_unit_time_4.setText(QCoreApplication.translate("Control_Plant", u"\u0e27\u0e34\u0e19\u0e32\u0e17\u0e35", None))
        self.offset_cancel_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e22\u0e01\u0e40\u0e25\u0e34\u0e01", None))
        self.offset_edite_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e41\u0e01\u0e49\u0e44\u0e02", None))
        self.offset_save_pushButton.setText(QCoreApplication.translate("Control_Plant", u"\u0e1a\u0e31\u0e19\u0e17\u0e36\u0e01", None))
        self.tab.setTabText(self.tab.indexOf(self.Offset_tab), QCoreApplication.translate("Control_Plant", u"Offset", None))
    # retranslateUi

