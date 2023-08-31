from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
offersUI,_ = loadUiType('./UserControls/UCoffers/UC_Offers.ui')

class window_offers(QFrame, offersUI):
    def __init__(self, frame):
        super().__init__()
        self.setupUi(frame)
