from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
generalReportsUI,_ = loadUiType('./UserControls/UCgeneralReports/UC_General_Reports.ui')

class window_generalreports(QFrame, generalReportsUI):
    def __init__(self, frame):
        super().__init__()
        self.setupUi(frame)
