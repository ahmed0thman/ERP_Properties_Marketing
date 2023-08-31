# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UC_PropretiesNavigator.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_UC_Propreties_Navigation(object):
    def setupUi(self, UC_Propreties_Navigation):
        UC_Propreties_Navigation.setObjectName("UC_Propreties_Navigation")
        UC_Propreties_Navigation.resize(1031, 800)
        UC_Propreties_Navigation.setFrameShape(QtWidgets.QFrame.StyledPanel)
        UC_Propreties_Navigation.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Propreties_Navigator = QtWidgets.QFrame(UC_Propreties_Navigation)
        self.Propreties_Navigator.setGeometry(QtCore.QRect(0, 0, 1031, 800))
        self.Propreties_Navigator.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Propreties_Navigator.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Propreties_Navigator.setObjectName("Propreties_Navigator")
        self.btn_lands = QtWidgets.QPushButton(self.Propreties_Navigator)
        self.btn_lands.setGeometry(QtCore.QRect(100, 440, 350, 200))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.btn_lands.setFont(font)
        self.btn_lands.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_lands.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_lands.setStyleSheet("color: #fff;\n"
"background-color:#e2d82d;\n"
"font-size: 40px;")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../imgs/land-sales.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_lands.setIcon(icon)
        self.btn_lands.setIconSize(QtCore.QSize(150, 150))
        self.btn_lands.setObjectName("btn_lands")
        self.btn_sakani = QtWidgets.QPushButton(self.Propreties_Navigator)
        self.btn_sakani.setGeometry(QtCore.QRect(539, 160, 350, 200))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.btn_sakani.setFont(font)
        self.btn_sakani.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_sakani.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_sakani.setStyleSheet("color: #fff;\n"
"background-color:#d81a1a;\n"
"font-size: 40px;\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../imgs/building.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_sakani.setIcon(icon1)
        self.btn_sakani.setIconSize(QtCore.QSize(150, 150))
        self.btn_sakani.setObjectName("btn_sakani")
        self.btn_5adami = QtWidgets.QPushButton(self.Propreties_Navigator)
        self.btn_5adami.setGeometry(QtCore.QRect(540, 440, 350, 200))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.btn_5adami.setFont(font)
        self.btn_5adami.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_5adami.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_5adami.setStyleSheet("color: #fff;\n"
"background-color:#4689e6;\n"
"font-size: 40px;")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../imgs/museum.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_5adami.setIcon(icon2)
        self.btn_5adami.setIconSize(QtCore.QSize(150, 150))
        self.btn_5adami.setObjectName("btn_5adami")
        self.btn_sena3i = QtWidgets.QPushButton(self.Propreties_Navigator)
        self.btn_sena3i.setGeometry(QtCore.QRect(100, 160, 350, 200))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.btn_sena3i.setFont(font)
        self.btn_sena3i.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_sena3i.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_sena3i.setStyleSheet("color: #fff;\n"
"background-color:#61d309;\n"
"font-size: 40px;")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../../imgs/factory2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_sena3i.setIcon(icon3)
        self.btn_sena3i.setIconSize(QtCore.QSize(150, 150))
        self.btn_sena3i.setObjectName("btn_sena3i")

        self.retranslateUi(UC_Propreties_Navigation)
        QtCore.QMetaObject.connectSlotsByName(UC_Propreties_Navigation)

    def retranslateUi(self, UC_Propreties_Navigation):
        _translate = QtCore.QCoreApplication.translate
        UC_Propreties_Navigation.setWindowTitle(_translate("UC_Propreties_Navigation", "Frame"))
        self.btn_lands.setText(_translate("UC_Propreties_Navigation", "الاراضى"))
        self.btn_sakani.setText(_translate("UC_Propreties_Navigation", "السكنى"))
        self.btn_5adami.setText(_translate("UC_Propreties_Navigation", "الخدمى "))
        self.btn_sena3i.setText(_translate("UC_Propreties_Navigation", "الصناعى "))


