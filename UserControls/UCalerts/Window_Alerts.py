from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
alertsUI,_ = loadUiType('./UserControls/UCalerts/UC_Alerts.ui')

class window_alerts(QFrame, alertsUI):

    def __init__(self, frame):
        super().__init__()
        self.setupUi(frame)
        self.alerts_frames = [
            self.Frame_Alerts_Offers,
            self.Frame_Alerts_Rents,
            self.Frame_Alerts_Requests

        ]
        self.Swipe_Alerts_Frames(self.Frame_Alerts_Offers)
        self.InitUi()


    def Swipe_Alerts_Frames(self, frame):
        for frm in self.alerts_frames:
            if frm == frame:
                frm.setVisible(True)
            else:
                frm.setVisible(False)

    def InitUi(self):
        self.btn_alert_offers_frame.clicked.connect(
            lambda: self.Swipe_Alerts_Frames(self.Frame_Alerts_Offers)
        )
        self.btn_alert_rent_frame.clicked.connect(
            lambda: self.Swipe_Alerts_Frames(self.Frame_Alerts_Rents)
        )
        self.btn_alert_requests_frame.clicked.connect(
            lambda: self.Swipe_Alerts_Frames(self.Frame_Alerts_Requests)
        )
