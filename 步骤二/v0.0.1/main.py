import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from mainwindow_ui import Ui_MainWindow
from mpsplan_ui import Ui_MainWindow as MPSPlanUi
from mps.data_readers import read_sales_forecast, read_inventory, read_production_orders
from mps.inventory_extraction import extract_inventory_data, extract_in_transit_quantity
from mps.demand_calculation import calculate_monthly_demand
from mps.mps_calculation import calculate_mps
import pandas as pd

class MPSPlanApp(QMainWindow, MPSPlanUi):
    def __init__(self, main_window):
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window  # 保存对 MainWindow 的引用
        self.sales_forecast_file = None
        self.inventory_file = None
        self.production_orders_file = None

        self.uploadSalesForecastButton.clicked.connect(self.upload_sales_forecast)
        self.uploadInventoryButton.clicked.connect(self.upload_inventory)
        self.uploadProductionOrdersButton.clicked.connect(self.upload_production_orders)
        self.runButton.clicked.connect(self.run_operations)
        self.exportButton.clicked.connect(self.export_results)

    def log_to_main_window(self, message):
        self.main_window.logTextEdit.append(message)

    def upload_sales_forecast(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择销售预测文件", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.sales_forecast_file = file_path
            self.salesForecastStatusLabel.setText("已上传")
            self.logTextEdit.append(f"销售预测文件已上传: {file_path}")
            self.log_to_main_window(f"销售预测文件已上传: {file_path}")

    def upload_inventory(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择现存量查询文件", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.inventory_file = file_path
            self.inventoryStatusLabel.setText("已上传")
            self.logTextEdit.append(f"现存量查询文件已上传: {file_path}")
            self.log_to_main_window(f"现存量查询文件已上传: {file_path}")

    def upload_production_orders(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择生产订单列表文件", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.production_orders_file = file_path
            self.productionOrdersStatusLabel.setText("已上传")
            self.logTextEdit.append(f"生产订单列表文件已上传: {file_path}")
            self.log_to_main_window(f"生产订单列表文件已上传: {file_path}")

    def run_operations(self):
        self.log_to_main_window("点击了运行按钮，开始执行操作")
        if not all([self.sales_forecast_file, self.inventory_file, self.production_orders_file]):
            QMessageBox.warning(self, "警告", "请先上传所有文件")
            self.log_to_main_window("操作失败：未上传所有文件")
            return

        try:
            df_sales_forecast = read_sales_forecast(self.sales_forecast_file)
            df_inventory = read_inventory(self.inventory_file)
            df_production_orders = read_production_orders(self.production_orders_file)

            # 确保存货编码为字符串类型
            df_sales_forecast['存货编码'] = df_sales_forecast['存货编码'].astype(str)
            df_inventory['存货编码'] = df_inventory['存货编码'].astype(str)
            df_production_orders['物料编码'] = df_production_orders['物料编码'].astype(str)

            # 将所有空值替换为0
            df_sales_forecast.fillna(0, inplace=True)
            df_inventory.fillna(0, inplace=True)
            df_production_orders.fillna(0, inplace=True)

            # 初始化新的列
            df_sales_forecast['成品库存(现存量查询)'] = 0
            df_sales_forecast['解析库存(现存量查询)'] = 0
            df_sales_forecast['研发库存(现存量查询)'] = 0
            df_sales_forecast['退货待返工(现存量查询)'] = 0
            df_sales_forecast['在途(生产订单列表)'] = 0
            df_sales_forecast['月底库存'] = 0

            # 根据存货编码匹配并提取库存数据和在途数量
            for index, row in df_sales_forecast.iterrows():
                stock_code = row['存货编码']
                finished_goods_stock, parsing_stock, research_stock, return_stock = extract_inventory_data(df_inventory, stock_code)
                in_transit_quantity = extract_in_transit_quantity(df_production_orders, stock_code)
                
                df_sales_forecast.at[index, '成品库存(现存量查询)'] = finished_goods_stock
                df_sales_forecast.at[index, '解析库存(现存量查询)'] = parsing_stock
                df_sales_forecast.at[index, '研发库存(现存量查询)'] = research_stock
                df_sales_forecast.at[index, '退货待返工(现存量查询)'] = return_stock
                df_sales_forecast.at[index, '在途(生产订单列表)'] = in_transit_quantity

                # 获取未发货订单，如果为空则处理为0
                unshipped_orders = row['未发货订单'] if pd.notna(row['未发货订单']) else 0

                # 计算月底库存
                end_of_month_stock = finished_goods_stock + parsing_stock + in_transit_quantity + return_stock - unshipped_orders
                df_sales_forecast.at[index, '月底库存'] = end_of_month_stock

            
            # 计算每个月的需求
            months = calculate_monthly_demand(df_sales_forecast)
            
            # 计算MPS和结余
            for month in months:
                print(f"Calculating MPS for month: {month}")
                calculate_mps(df_sales_forecast, month)

            self.df_result = df_sales_forecast
            self.logTextEdit.append("操作成功完成")
            self.log_to_main_window("操作成功完成")
            QMessageBox.information(self, "信息", "操作成功完成")
        except Exception as e:
            self.logTextEdit.append(f"操作失败: {str(e)}")
            self.log_to_main_window(f"操作失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"操作失败: {str(e)}")

    def export_results(self):
        self.log_to_main_window("点击了导出按钮，开始导出结果")
        if hasattr(self, 'df_result'):
            file_path, _ = QFileDialog.getSaveFileName(self, "保存结果文件", "", "Excel Files (*.xlsx *.xls)")
            if file_path:
                self.df_result.to_excel(file_path, index=False)
                self.logTextEdit.append(f"结果文件已导出: {file_path}")
                self.log_to_main_window(f"结果文件已导出: {file_path}")
                QMessageBox.information(self, "信息", "结果文件已导出")
        else:
            QMessageBox.warning(self, "警告", "请先运行操作以生成结果")
            self.log_to_main_window("导出失败：请先运行操作以生成结果")

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
