from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
requestsUI,_ = loadUiType('./UserControls/UCrequests/UC_Requests.ui')

class window_requests(QFrame, requestsUI):
    def __init__(self, frame):
        super().__init__()
        self.setupUi(frame)
