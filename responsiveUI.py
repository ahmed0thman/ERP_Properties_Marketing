from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Responsive:
    children_widgets = []
    def __init__(self, window, screenSize):
        self.window = window
        self.Get_Children(window.centralWidget())
        self.Init_Resbonsive(screenSize)
    def Get_Children(self, window):
        childs = window.children()
        for child in childs:
            if child.objectName() != '' and 'qt_' not in child.objectName() and 'Layout' not in child.objectName():
                self.children_widgets.append(child)
                if 'tabWidget' not in child.objectName() :
                    self.Get_Children(child)

    def Init_Resbonsive(self, size):
        new_width = size.width() / 1920
        new_height = size.height() / 1080
        self.window.setGeometry(
            (size.width() - (new_width * self.window.width())) / 2,
            (size.height() - (new_height * self.window.height())) / 2.4,
            new_width * self.window.width(),
            new_height * self.window.height()
        )
        for i in self.children_widgets:
            new_widget_width = new_width * i.width()
            new_widget_height = new_height * i.height()
            i.setGeometry(QRect(i.x() * new_width, i.y() * new_height, new_widget_width, new_widget_height))
            old_font = i.font().pointSize()
            f = i.font()
            if 'header' in i.objectName():
                f.setPointSize(int(old_font * new_width * 2))
            else:
                f.setPointSize(int(old_font * new_width * 1.6))
            i.setFont(f)
            try:
                if i.objectName() != 'main_list':
                    old_icon_width = i.iconSize().width()
                    old_icon_height = i.iconSize().height()
                    i.setIconSize(QSize(old_icon_width * new_width, old_icon_height * new_height))
                else:
                    i.setIconSize(QSize(35 * new_width, 35 * new_height))
            except:
                pass


class Maxmize:
    children_widgets = []
    def __init__(self, window, screenSize):
        self.window = window
        self.Get_Children(window.centralWidget())
        self.Init_Resbonsive(screenSize)
    def Get_Children(self, window):
        childs = window.children()
        for child in childs:
            if child.objectName() != '' and 'qt_' not in child.objectName():
                self.children_widgets.append(child)
                if 'tabWidget' not in child.objectName() :
                    self.Get_Children(child)

    def Init_Resbonsive(self, size):
        new_width = self.window.width() / size.width()
        new_height = self.window.height() / size.height()
        self.window.setGeometry(
            0,
            0,
            new_width,
            new_height
        )
        self.window.setFixedWidth(new_width * self.window.width())
        self.window.setFixedHeight(new_height * self.window.height())
        for i in self.children_widgets:
            new_widget_width = new_width * i.width()
            new_widget_height = new_height * i.height()
            i.setGeometry(QRect(i.x() * new_width, i.y() * new_height, new_widget_width, new_widget_height))
            old_font = i.font().pointSize()
            f = i.font()
            if 'header' in i.objectName():
                f.setPointSize(int(old_font * new_width * 2))
            else:
                f.setPointSize(int(old_font * new_width * 1.6))
            i.setFont(f)
            try:
                if i.objectName() != 'main_list':
                    old_icon_width = i.iconSize().width()
                    old_icon_height = i.iconSize().height()
                    i.setIconSize(QSize(old_icon_width * new_width, old_icon_height * new_height))
                else:
                    i.setIconSize(QSize(35 * new_width, 35 * new_height))
            except:
                pass

