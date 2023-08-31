from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from UserControls import responsiveWidget2
from UserControls.UCfactories.Window_Factories import widnow_factory
from UserControls.UClands.Window_Lands import window_lands
from UserControls.UCsakani.Window_Sakani import window_sakani
from UserControls.UCservices.Window_Services import window_services

propretiesNavigationUI,_ = loadUiType('./UserControls/UCpropretiesNavigation/UC_PropretiesNavigator.ui')

class window_propreties_navigation(QFrame, propretiesNavigationUI):
    def __init__(self, frame, size, namespace):
        super().__init__()
        self.Size = size
        self.namespace = namespace
        self.setupUi(frame)
        self.InitUi()

    def InitUi(self):
        self.btn_sena3i.clicked.connect(lambda: self.Show_Factories_Window())
        self.btn_lands.clicked.connect(lambda: self.Show_Lands_Window())
        self.btn_sakani.clicked.connect(lambda: self.Show_Sakani_Window())
        self.btn_5adami.clicked.connect(lambda: self.Show_5adami_Window())


    def Show_Factories_Window(self):
        for widget in reversed(range(self.namespace.parentLayout.count())):
            self.namespace.parentLayout.itemAt(widget).widget().deleteLater()
        main_window = QFrame(self.namespace.hidden_frame)
        widnow_factory(main_window, self.namespace)
        responsiveWidget2.Responsive(main_window, self.Size)
        self.namespace.parentLayout.addWidget(main_window)

    def Show_Lands_Window(self):
        for widget in reversed(range(self.namespace.parentLayout.count())):
            self.namespace.parentLayout.itemAt(widget).widget().deleteLater()
        main_window = QFrame(self.namespace.hidden_frame)
        window_lands(main_window, self.namespace)
        responsiveWidget2.Responsive(main_window, self.Size)
        self.namespace.parentLayout.addWidget(main_window)

    def Show_Sakani_Window(self):
        for widget in reversed(range(self.namespace.parentLayout.count())):
            self.namespace.parentLayout.itemAt(widget).widget().deleteLater()
        main_window = QFrame(self.namespace.hidden_frame)
        window_sakani(main_window, self.namespace)
        responsiveWidget2.Responsive(main_window, self.Size)
        self.namespace.parentLayout.addWidget(main_window)

    def Show_5adami_Window(self):
        for widget in reversed(range(self.namespace.parentLayout.count())):
            self.namespace.parentLayout.itemAt(widget).widget().deleteLater()
        main_window = QFrame(self.namespace.hidden_frame)
        window_services(main_window, self.namespace)
        responsiveWidget2.Responsive(main_window, self.Size)
        self.namespace.parentLayout.addWidget(main_window)



