import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from UI_files.mainwindow_ui import Ui_MainWindow
from mps.mps_plan_app import MPSPlanApp
from create_materials.create_materials_app import CreateMaterialsApp

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionPre_Scheduling.triggered.connect(self.open_mps_plan_app)
        self.actionCreate_Production_Material_Details.triggered.connect(self.open_create_production_material_details)

    def open_mps_plan_app(self):
        self.logTextEdit.append("点击了预排产计划菜单项，打开排产计划工具窗口")
        self.mps_plan_app = MPSPlanApp(self)
        self.mps_plan_app.show()

    def open_create_production_material_details(self):
        self.logTextEdit.append("点击了创建生产物料明细菜单项，打开创建生产物料明细窗口")
        self.create_production_material_details_window = CreateMaterialsApp(self)
        self.create_production_material_details_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
