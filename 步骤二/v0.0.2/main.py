import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI_files.mainwindow_ui import Ui_MainWindow
from mps.mps_plan_app import MPSPlanApp

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionPre_Scheduling.triggered.connect(self.open_mps_plan_app)

    def open_mps_plan_app(self):
        self.logTextEdit.append("点击了预排产计划菜单项，打开排产计划工具窗口")
        self.mps_plan_app = MPSPlanApp(self)
        self.mps_plan_app.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
