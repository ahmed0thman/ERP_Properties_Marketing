from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
constraintsUI,_ = loadUiType('./UserControls/UCconstraints/UC_Constraints.ui')

class window_constraints(QFrame, constraintsUI):
    def __init__(self, frame):
        super().__init__()
        self.setupUi(frame)
