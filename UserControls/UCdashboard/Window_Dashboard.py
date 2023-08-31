from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
dashboardUI,_ = loadUiType('./UserControls/UCdashboard/UC_Dashboard.ui')

class window_dashboard(QFrame, dashboardUI):
    def __init__(self, frame):
        super().__init__()
        self.setupUi(frame)
