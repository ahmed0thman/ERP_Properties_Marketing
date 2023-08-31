from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
from UserControls import responsiveWidget2
from UserControls.UCsearch.Window_Search import Window_Search
from UserControls.UCpropretiesNavigation.window_propreties_navigation import window_propreties_navigation
from UserControls.UCclients.Window_Clients import window_clients
from UserControls.UCowners.Window_Owners import window_owners
from UserControls.UCoffers.Window_Offers import window_offers
from UserControls.UCrequests.Window_Requests import window_requests
from UserControls.UCemployees.Window_Employees import window_employees
from UserControls.UCalerts.Window_Alerts import window_alerts
from UserControls.UCgeneralReports.Window_GeneralReports import window_generalreports
from UserControls.UCconstraints.Window_Constraints import window_constraints
from UserControls.UCmanager.Window_Manager import window_manager
from UserControls.UCdashboard.Window_Dashboard import window_dashboard

mainUI,_ = loadUiType('./UserControls/MainWindow/main_window.ui')

class Main_Window(QFrame, mainUI):
    panels = []
    def __init__(self, frame, size, namespace):
        super().__init__()
        self.setupUi(frame)
        self.namespace = namespace
        self.Size = size
        self.parentLayout = QVBoxLayout()
        self.parentLayout.setContentsMargins(0, 0, 0, 0)
        self.panel.setLayout(self.parentLayout)
        self.panels = [
            window_propreties_navigation,
            window_offers,
            Window_Search,
            window_requests,
            window_clients,
            window_owners,
            window_employees,
            window_alerts,
            window_generalreports,
            window_constraints,
            window_manager,
            window_dashboard
        ]
        self.main_list.setCurrentRow(0)
        self.InitUi()


    def InitUi(self):
        self.main_list.setIconSize(QSize(35, 35))
        self.main_list.currentRowChanged.connect(
            lambda: self.Swipe_panels(self.main_list.currentRow())
        )
        self.main_list.currentRowChanged.connect(
            self.panel_2.setFocus
        )

        temp_UC = QFrame(self.panel_2)
        window_propreties_navigation(temp_UC, self.Size, self.namespace)
        #responsiveWidget2.Responsive(temp_UC, self.Size)
        self.parentLayout.addWidget(temp_UC)




    def Swipe_panels(self, window):
            for widget in reversed(range(self.parentLayout.count())):
                self.parentLayout.itemAt(widget).widget().deleteLater()
            parent = self.panels[window]
            self.temp_UC = QFrame(self.panel_2)
            try:
                parent(self.temp_UC, self.namespace)
            except Exception:
                try:
                    parent(self.temp_UC)
                except:
                    parent(self.temp_UC, self.Size, self.namespace)
            responsiveWidget2.Responsive(self.temp_UC, self.Size)

            self.parentLayout.addWidget(self.temp_UC)


# app = QApplication(sys.argv)
# screen = app.primaryScreen()
# size = screen.size()
# if __name__ == '__main__':
#     window = Main_Window(size)
#     window.show()
#     app.exec_()


