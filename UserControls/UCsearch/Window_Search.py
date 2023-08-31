from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType

searchUI,_ = loadUiType('./UserControls/UCsearch/UC_Search.ui')


class Window_Search(QFrame, searchUI):
    def __init__(self, frame, namespace):
        super().__init__()
        self.setupUi(frame)
        self.namespace = namespace
        self.Init_Childs_Frames()
        self.InitUi()
        self.createLayout_Container()


    def InitUi(self):
        self.serach_cbx_type.currentIndexChanged.connect(
            lambda: self.View_Target_Frame(self.framesSearchList, self.serach_cbx_type.currentIndex())
        )

    def View_Target_Frame(self, parent, child):
        for frame in parent:
            if frame == parent[child]:
                frame.setVisible(True)
            else:
                frame.setVisible(False)

    def Init_Childs_Frames(self):
        self.framesSearchList = [
            self.Frame_Search_Emarah,
            self.Frame_Search_Villa,
            self.Frame_Search_NormalFlat,
            self.Frame_Search_DoublexFlat,
            self.Frame_Search_Factories,
            self.Frame_Search_Lands,
            self.Frame_search_ServicesBuilding,
            self.Frame_Search_ServicesUnit,
            self.Frame_Search_Eductional,
            self.Frame_Search_Hospital,
        ]


    def createLayout_group(self, father):

        layout_groupbox = QVBoxLayout(father)
        sframe = QFrame()
        sframe.setFixedHeight(int(0.15 * self.namespace.Size.height()))
        sframe.setFixedWidth(int(0.217 * self.namespace.Size.width()))
        sframe.setStyleSheet('border: 1px solid #4689e6;')
        layout_groupbox.addWidget(sframe)

        btn_view = QPushButton('عرض', sframe)
        btn_view.setGeometry(int(0.04 * sframe.width()), int(0.7 * sframe.height()),
                             int(0.2 * sframe.width()), int(0.2 * sframe.height()))
        btn_view.setStyleSheet('font-family: simplified arabic; padding-bottom: 5%')
        f = btn_view.font()
        f.setPointSize(int(sframe.width() * 0.03))
        btn_view.setFont(f)
        icon = QPushButton(sframe)
        icon.setStyleSheet('border: 1px solid #000; background-color: #fff;')
        icon.setGeometry(int(0.77 * sframe.width())
                         , int(0.05 * sframe.height()), int(0.2 * sframe.width()), int(0.2 * sframe.width()))
        #icon.setDisabled(True)
        icon.setIcon(QIcon('imgs/building.png'))
        icon.setIconSize(QSize(icon.width(), icon.height()))
        btn_view.clicked.connect(self.namespace.Open_Galary)
        lbl = QLabel('عنوان العقار ومساحته', sframe)
        lbl.setGeometry((QRect(int(0.14 * sframe.width()),
                               int(0.05 * sframe.height()),
                               int(0.6 * sframe.width()),
                               int(0.2 * sframe.height()))))
        lbl.setStyleSheet('font-family: simplified arabic;font-weight: bold; border: none; ')
        f = lbl.font()
        f.setPointSize(int(sframe.width() * 0.04))
        lbl.setFont(f)
        lbl.setLayoutDirection(Qt.RightToLeft)
        lbl_price = QLabel('السعر: 2,000,000 جم', sframe)
        lbl_price.setGeometry((QRect(int(0.14 * sframe.width()),
                                     int(0.34 * sframe.height()),
                                     int(0.6 * sframe.width()),
                                     int(0.15 * sframe.height()))))
        lbl_price.setStyleSheet('font-family: simplified arabic; border: none; ')
        f = lbl_price.font()
        f.setPointSize(int(sframe.width() * 0.027))
        lbl_price.setFont(f)
        lbl_price.setLayoutDirection(Qt.RightToLeft)
        layout_groupbox.addStretch(1)
        return sframe

    def createLayout_Container(self):
        self.scrollarea = QScrollArea(self.Frame_Search_Results)
        self.scrollarea.setFixedWidth(int(0.24 * self.namespace.Size.width()))
        self.scrollarea.setFixedHeight(int(0.66 * self.namespace.Size.height()))
        self.scrollarea.setWidgetResizable(True)
        self.scrollarea.horizontalScrollBar().setVisible(False)

        widget = QWidget()
        self.scrollarea.setWidget(widget)
        self.layout_SArea = QVBoxLayout(widget)

        for i in range(7):
            self.layout_SArea.addWidget(self.createLayout_group(self.scrollarea))
        #self.layout_SArea.addStretch(100)

