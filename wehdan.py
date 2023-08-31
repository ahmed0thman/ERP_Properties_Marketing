from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import sys
import mysql.connector
import datetime
from responsiveUI import Responsive
from UserControls import responsiveWidget
from UserControls.MainWindow.main_window import Main_Window

mainUi,_ = loadUiType('wehdan.ui')

class main(QMainWindow,mainUi):

    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.sql = mysql.connector
        self.Handle_DB_Connection()
        self.Init_Ui()
        flags = Qt.WindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(flags)
        self.Init_UC_Objects()
        self.currentEmployee = '2981101600994'
        #-----------------------------------------
        # Responsive(self, size)
        self.show()
        self.oldPos = self.pos()
        self.second_click = QPoint(1000000, 1000000)
        self.Size = size

    def Init_Ui(self):
        self.exit.clicked.connect(self.Exit)
        self.minimize.clicked.connect(self.Minimize)
        self.btn_home.clicked.connect(self.Return_To_Mainwindow)
        self.btn_next_img.clicked.connect(self.Next_Img)
        self.btn_previous_img.clicked.connect(self.Previous_Img)

        #self.Frame_Navigation_Handler()
        #self.Navigators_Signals_Slots()
        #self.createLayout_Container()
        # self.layout_All = QVBoxLayout(self)
        # self.layout_All.addWidget(self.scrollarea)
        self.close_galary.clicked.connect(self.Close_Galary)
        self.show_owner_info.clicked.connect(self.Show_Owner_info)

    def Handle_Status(self, text, type):

        if type == 1:
            self.status.setStyleSheet("#status{padding:0px 10px 0px 10px;height:10px;background:transparent;color:green;font-weight:bold;text-align: justify;}")
        elif type == 2:
            self.status.setStyleSheet("#status{padding:0px 10px 0px 10px;height:10px;background:transparent;color:red;font-weight:bold;text-align: justify;}")
        elif type == 3:
            self.status.setStyleSheet("#status{padding:0px 10px 0px 10px;height:10px;background:transparent;color:orange;font-weight:bold;text-align: justify;}")
        elif type == 4:
            self.status.setStyleSheet("#status{padding:0px 10px 0px 10px;height:10px;background:transparent;color:black;font-weight:bold;text-align: justify;}")
        self.status.setText(text)


    def Handle_DB_Connection(self):

        try:
            self.db = self.sql.connect(user="root", password="", host="localhost", database="properties")
            self.cur = self.db.cursor()
            self.Handle_Status('تم الاتصل بالسيرفر بنجاح', 1)


            return True
        except mysql.connector.errors.InterfaceError:
            self.Handle_Status('فشل الاتصال بالسيرفر', 2)
            self.MainFrame.setEnabled(False)
            return False


    def Init_UC_Objects(self):
        self.parentLayout = QVBoxLayout()
        self.parentLayout.setObjectName('parentLayout')
        self.parentLayout.setContentsMargins(0, 0, 0, 0)
        self.MainFrame.setLayout(self.parentLayout)
        main_window = QFrame(self.hidden_frame)
        Main_Window(main_window, size, self)
        self.parentLayout.addWidget(main_window)

    def Return_To_Mainwindow(self):
        for widget in reversed(range(self.parentLayout.count())):
            self.parentLayout.itemAt(widget).widget().deleteLater()
        main_window = QFrame(self.hidden_frame)
        Main_Window(main_window, size, self)
        responsiveWidget.Responsive(main_window,size)
        self.parentLayout.addWidget(main_window)


    def Open_Galary(self, images = list()):
        self.images = images
        self.animate = QPropertyAnimation(self.galary, b'geometry')
        self.animate.setDuration(200)
        self.animate.setStartValue(QRect(0, 0, self.galary.width(), 0))
        self.animate.setEndValue(QRect(0, 0, self.galary.width(), self.height()))
        self.animate.start()
        if type(images) != bool:
            self.btn_previous_img.setEnabled(True)
            self.btn_next_img.setEnabled(True)
            self.galary_pics.setText('')
            self.currentImg = 0
            self.galary_pics.setIcon(QIcon(images[self.currentImg]))
        else:
            self.btn_previous_img.setEnabled(False)
            self.btn_next_img.setEnabled(False)
            self.galary_pics.setText('لا يوجد صور')

    def Previous_Img(self):
        if self.currentImg != 0:
            self.currentImg -= 1
            self.galary_pics.setIcon(QIcon(self.images[self.currentImg]))

    def Next_Img(self):
        if self.currentImg < len(self.images) - 1:
            self.currentImg += 1
            self.galary_pics.setIcon(QIcon(self.images[self.currentImg]))


    def Close_Galary(self):
        self.animate = QPropertyAnimation(self.galary, b'geometry')
        self.animate.setDuration(200)
        self.animate.setStartValue(QRect(0, 0, self.galary.width(), self.height()))
        self.animate.setEndValue(QRect(0, 0, self.galary.width(), 0))
        self.animate.start()

    def Show_Owner_info(self):
        if self.show_owner_info.text() == '^':
            self.anim = QPropertyAnimation(self.owner_info, b'geometry')
            self.anim.setDuration(100)
            self.anim.setStartValue(QRect(self.owner_info.x(), self.owner_info.y(),self.owner_info.width(), self.owner_info.height()))
            self.anim.setEndValue(QRect(self.owner_info.x(), self.owner_info.y()- (self.height() * 0.1),self.owner_info.width(), self.owner_info.height()))
            self.anim.start()

            self.anim2 = QPropertyAnimation(self.show_owner_info, b'geometry')
            self.anim2.setDuration(100)
            self.anim2.setStartValue(QRect(self.show_owner_info.x(), self.show_owner_info.y(),self.show_owner_info.width(), self.show_owner_info.height()))
            self.anim2.setEndValue(QRect(self.show_owner_info.x(), self.show_owner_info.y()-(self.height() * 0.1),self.show_owner_info.width(), self.show_owner_info.height()))
            self.anim2.start()
            self.show_owner_info.setText('-')
        elif self.show_owner_info.text() == '-':
            self.anim = QPropertyAnimation(self.owner_info, b'geometry')
            self.anim.setDuration(100)
            self.anim.setStartValue(QRect(self.owner_info.x(), self.owner_info.y(),self.owner_info.width(), self.owner_info.height()))
            self.anim.setEndValue(QRect(self.owner_info.x(), self.owner_info.y()+(self.height() * 0.1),self.owner_info.width(), self.owner_info.height()))
            self.anim.start()

            self.anim2 = QPropertyAnimation(self.show_owner_info, b'geometry')
            self.anim2.setDuration(100)
            self.anim2.setStartValue(QRect(self.show_owner_info.x(), self.show_owner_info.y(),self.show_owner_info.width(), self.show_owner_info.height()))
            self.anim2.setEndValue(QRect(self.show_owner_info.x(), self.show_owner_info.y()+(self.height() * 0.1),self.show_owner_info.width(), self.show_owner_info.height()))
            self.anim2.start()
            self.show_owner_info.setText('^')


    def Exit(self):
        self.close()

    def Minimize(self):
        self.setWindowState(Qt.WindowMinimized)


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.second_click = event.pos()

    def mouseMoveEvent(self, event):
        if QPoint(self.second_click).y() < self.frame_header.height():
            delta = QPoint(event.globalPos() - self.oldPos)
            if delta == None:
                pass
            else:
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.second_click = QPoint(1000000, 1000000)

app = QApplication(sys.argv)
screen = app.primaryScreen()
size = screen.size()
if __name__ == '__main__':
    window = main()
    app.exec_()
