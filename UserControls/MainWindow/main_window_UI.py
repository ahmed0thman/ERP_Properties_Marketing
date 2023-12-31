# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UC_Frames(object):
    def setupUi(self, UC_Frames):
        UC_Frames.setObjectName("UC_Frames")
        UC_Frames.resize(1260, 800)
        UC_Frames.setFrameShape(QtWidgets.QFrame.StyledPanel)
        UC_Frames.setFrameShadow(QtWidgets.QFrame.Raised)
        self.main_list = QtWidgets.QListWidget(UC_Frames)
        self.main_list.setGeometry(QtCore.QRect(1040, 0, 221, 632))
        font = QtGui.QFont()
        font.setFamily("simplified arabic")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.main_list.setFont(font)
        self.main_list.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.main_list.setStyleSheet("")
        self.main_list.setObjectName("main_list")
        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imgs/building1.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        item.setIcon(icon)
        self.main_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("imgs/offer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon1)
        self.main_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("imgs/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon2)
        self.main_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("imgs/order-history.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon3)
        self.main_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("imgs/man.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon4)
        self.main_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("imgs/owner.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon5)
        self.main_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("imgs/employee.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon6)
        self.main_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("imgs/bell.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon7)
        self.main_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("imgs/report-icon-30.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon8)
        self.main_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("imgs/contracts.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon9)
        self.main_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("imgs/settings.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon10)
        self.main_list.addItem(item)
        item = QtWidgets.QListWidgetItem()
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("imgs/dashboard.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon11)
        self.main_list.addItem(item)
        self.panel = QtWidgets.QFrame(UC_Frames)
        self.panel.setGeometry(QtCore.QRect(5, 0, 1031, 800))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.panel.setFont(font)
        self.panel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.panel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.panel.setObjectName("panel")
        self.main_list_2 = QtWidgets.QListWidget(UC_Frames)
        self.main_list_2.setGeometry(QtCore.QRect(2310, 670, 221, 632))
        font = QtGui.QFont()
        font.setFamily("simplified arabic")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.main_list_2.setFont(font)
        self.main_list_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.main_list_2.setStyleSheet("")
        self.main_list_2.setObjectName("main_list_2")
        item = QtWidgets.QListWidgetItem()
        item.setIcon(icon)
        self.main_list_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setIcon(icon1)
        self.main_list_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setIcon(icon2)
        self.main_list_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setIcon(icon3)
        self.main_list_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setIcon(icon4)
        self.main_list_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setIcon(icon5)
        self.main_list_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setIcon(icon6)
        self.main_list_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setIcon(icon7)
        self.main_list_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setIcon(icon8)
        self.main_list_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setIcon(icon9)
        self.main_list_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setIcon(icon10)
        self.main_list_2.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setIcon(icon11)
        self.main_list_2.addItem(item)
        self.panel_2 = QtWidgets.QFrame(UC_Frames)
        self.panel_2.setGeometry(QtCore.QRect(1275, 670, 1031, 800))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.panel_2.setFont(font)
        self.panel_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.panel_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.panel_2.setObjectName("panel_2")

        self.retranslateUi(UC_Frames)
        QtCore.QMetaObject.connectSlotsByName(UC_Frames)

    def retranslateUi(self, UC_Frames):
        _translate = QtCore.QCoreApplication.translate
        UC_Frames.setWindowTitle(_translate("UC_Frames", "Frame"))
        __sortingEnabled = self.main_list.isSortingEnabled()
        self.main_list.setSortingEnabled(False)
        item = self.main_list.item(0)
        item.setText(_translate("UC_Frames", "   العقارات"))
        item = self.main_list.item(1)
        item.setText(_translate("UC_Frames", "   العروض"))
        item = self.main_list.item(2)
        item.setText(_translate("UC_Frames", "   البحث"))
        item = self.main_list.item(3)
        item.setText(_translate("UC_Frames", "   الطلبات"))
        item = self.main_list.item(4)
        item.setText(_translate("UC_Frames", "   العملاء"))
        item = self.main_list.item(5)
        item.setText(_translate("UC_Frames", "   الملاك"))
        item = self.main_list.item(6)
        item.setText(_translate("UC_Frames", "   الموظفين"))
        item = self.main_list.item(7)
        item.setText(_translate("UC_Frames", "   الإشعارات"))
        item = self.main_list.item(8)
        item.setText(_translate("UC_Frames", "   التقارير العامه"))
        item = self.main_list.item(9)
        item.setText(_translate("UC_Frames", "   العقود"))
        item = self.main_list.item(10)
        item.setText(_translate("UC_Frames", "   الإداره"))
        item = self.main_list.item(11)
        item.setText(_translate("UC_Frames", "   إحصائيات الشركه"))
        self.main_list.setSortingEnabled(__sortingEnabled)
        __sortingEnabled = self.main_list_2.isSortingEnabled()
        self.main_list_2.setSortingEnabled(False)
        item = self.main_list_2.item(0)
        item.setText(_translate("UC_Frames", "   العقارات"))
        item = self.main_list_2.item(1)
        item.setText(_translate("UC_Frames", "   العروض"))
        item = self.main_list_2.item(2)
        item.setText(_translate("UC_Frames", "   البحث"))
        item = self.main_list_2.item(3)
        item.setText(_translate("UC_Frames", "   الطلبات"))
        item = self.main_list_2.item(4)
        item.setText(_translate("UC_Frames", "   العملاء"))
        item = self.main_list_2.item(5)
        item.setText(_translate("UC_Frames", "   الملاك"))
        item = self.main_list_2.item(6)
        item.setText(_translate("UC_Frames", "   الموظفين"))
        item = self.main_list_2.item(7)
        item.setText(_translate("UC_Frames", "   الإشعارات"))
        item = self.main_list_2.item(8)
        item.setText(_translate("UC_Frames", "   التقارير العامه"))
        item = self.main_list_2.item(9)
        item.setText(_translate("UC_Frames", "   العقود"))
        item = self.main_list_2.item(10)
        item.setText(_translate("UC_Frames", "   الإداره"))
        item = self.main_list_2.item(11)
        item.setText(_translate("UC_Frames", "   إحصائيات الشركه"))
        self.main_list_2.setSortingEnabled(__sortingEnabled)


