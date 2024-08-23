from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QApplication
from PyQt5.QtCore import Qt
from UI_files.creatematerials_ui import Ui_MainWindow as CreateMaterialsUi
from create_materials.data_readers_materials import read_material_analysis, read_production_planning, read_in_transit_materials, read_stock_inquiry, read_production_order_list, read_purchase_order_execution_statistics, read_outsourcing_order_execution_statistics, read_material_purchase_information, read_semi_finished_product_comparison
from create_materials.execute_production_details import execute_production_details

class CreateMaterialsApp(QMainWindow, CreateMaterialsUi):
    def __init__(self, parent=None):
        super(CreateMaterialsApp, self).__init__(parent)
        self.setupUi(self)
        self.uploadProductionScheduleButton.clicked.connect(self.select_production_schedule)
        self.uploadMaterialAnalysisButton.clicked.connect(self.select_material_analysis)
        self.uploadInTransitMaterialButton.clicked.connect(self.select_in_transit_material)
        
        # 连接新的按钮到其处理函数
        self.uploadCurrentInventoryQueryButton.clicked.connect(self.select_current_inventory_query)
        self.uploadProductionOrderListButton.clicked.connect(self.select_production_order_list)
        self.uploadPurchaseOrderExecutionStatisticsButton.clicked.connect(self.select_purchase_order_execution_statistics)
        self.uploadOutsourcingOrderExecutionStatisticsButton.clicked.connect(self.select_outsourcing_order_execution_statistics)
        self.uploadMaterialPurchaseInformationButton.clicked.connect(self.select_material_purchase_information)
        self.uploadSemiFinishedProductComparisonButton.clicked.connect(self.select_semi_finished_product_comparison)
        
        self.runButton.clicked.connect(self.execute_operations)
        self.exportButton.clicked.connect(self.export_results)
        self.productionScheduleStatusLabel.setText("未上传")
        self.materialAnalysisStatusLabel.setText("未上传")
        self.inTransitMaterialStatusLabel.setText("未上传")
        self.currentInventoryQueryStatusLabel.setText("未上传")
        self.productionOrderListStatusLabel.setText("未上传")
        self.purchaseOrderExecutionStatisticsStatusLabel.setText("未上传")
        self.outsourcingOrderExecutionStatisticsStatusLabel.setText("未上传")
        self.materialPurchaseInformationStatusLabel.setText("未上传")
        self.semiFinishedProductComparisonStatusLabel.setText("未上传")
        self.logTextEdit.setReadOnly(True)
        self.logTextEdit.clear()
        
        self.production_schedule_file = None
        self.material_analysis_file = None
        self.in_transit_material_file = None
        self.current_inventory_query_file = None
        self.production_order_list_file = None
        self.purchase_order_execution_statistics_file = None
        self.outsourcing_order_execution_statistics_file = None
        self.material_purchase_information_file = None
        self.semi_finished_product_comparison_file = None
        self.result_details = None

    def select_production_schedule(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "上传排产计划文件", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
        if file_name:
            self.production_schedule_file = file_name
            self.productionScheduleStatusLabel.setText("已选择")
            self.logTextEdit.append(f"排产计划文件已选择: {file_name}")

    def select_material_analysis(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "上传生产用料分析文件", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
        if file_name:
            self.material_analysis_file = file_name
            self.materialAnalysisStatusLabel.setText("已选择")
            self.logTextEdit.append(f"生产用料分析文件已选择: {file_name}")

    def select_in_transit_material(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "上传生产在途用料文件", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
        if file_name:
            self.in_transit_material_file = file_name
            self.inTransitMaterialStatusLabel.setText("已选择")
            self.logTextEdit.append(f"生产在途用料文件已选择: {file_name}")

    def select_current_inventory_query(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "上传现存量查询文件", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
        if file_name:
            self.current_inventory_query_file = file_name
            self.currentInventoryQueryStatusLabel.setText("已选择")
            self.logTextEdit.append(f"现存量查询文件已选择: {file_name}")

    def select_production_order_list(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "上传生产订单列表文件", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
        if file_name:
            self.production_order_list_file = file_name
            self.productionOrderListStatusLabel.setText("已选择")
            self.logTextEdit.append(f"生产订单列表文件已选择: {file_name}")

    def select_purchase_order_execution_statistics(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "上传采购订单执行统计表文件", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
        if file_name:
            self.purchase_order_execution_statistics_file = file_name
            self.purchaseOrderExecutionStatisticsStatusLabel.setText("已选择")
            self.logTextEdit.append(f"采购订单执行统计表文件已选择: {file_name}")

    def select_outsourcing_order_execution_statistics(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "上传委外订单执行统计表文件", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
        if file_name:
            self.outsourcing_order_execution_statistics_file = file_name
            self.outsourcingOrderExecutionStatisticsStatusLabel.setText("已选择")
            self.logTextEdit.append(f"委外订单执行统计表文件已选择: {file_name}")

    def select_material_purchase_information(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "上传物料采购信息文件", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
        if file_name:
            self.material_purchase_information_file = file_name
            self.materialPurchaseInformationStatusLabel.setText("已选择")
            self.logTextEdit.append(f"物料采购信息文件已选择: {file_name}")

    def select_semi_finished_product_comparison(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "上传半成品对照表文件", "", "Excel Files (*.xlsx *.xls);;All Files (*)", options=options)
        if file_name:
            self.semi_finished_product_comparison_file = file_name
            self.semiFinishedProductComparisonStatusLabel.setText("已选择")
            self.logTextEdit.append(f"半成品对照表文件已选择: {file_name}")

    def execute_operations(self):
        if not self.production_schedule_file:
            QMessageBox.warning(self, "警告", "请先上传排产计划文件。")
            self.logTextEdit.append("执行操作失败: 排产计划文件未上传")
            return

        if not self.material_analysis_file:
            QMessageBox.warning(self, "警告", "请先上传生产用料分析文件。")
            self.logTextEdit.append("执行操作失败: 生产用料分析文件未上传")
            return
        
        if not self.in_transit_material_file:
            QMessageBox.warning(self, "警告", "请先上传生产在途用料文件。")
            self.logTextEdit.append("执行操作失败: 生产在途用料文件未上传")
            return
        
        if not self.current_inventory_query_file:
            QMessageBox.warning(self, "警告", "请先上传现存量查询文件。")
            self.logTextEdit.append("执行操作失败: 现存量查询文件未上传")
            return

        if not self.production_order_list_file:
            QMessageBox.warning(self, "警告", "请先上传生产订单列表文件。")
            self.logTextEdit.append("执行操作失败: 生产订单列表文件未上传")
            return

        if not self.purchase_order_execution_statistics_file:
            QMessageBox.warning(self, "警告", "请先上传采购订单执行统计表文件。")
            self.logTextEdit.append("执行操作失败: 采购订单执行统计表文件未上传")
            return

        if not self.outsourcing_order_execution_statistics_file:
            QMessageBox.warning(self, "警告", "请先上传委外订单执行统计表文件。")
            self.logTextEdit.append("执行操作失败: 委外订单执行统计表文件未上传")
            return
        
        if not self.material_purchase_information_file:
            QMessageBox.warning(self, "警告", "请先上传物料采购信息文件。")
            self.logTextEdit.append("执行操作失败: 物料采购信息文件未上传")
            return

        if not self.semi_finished_product_comparison_file:
            QMessageBox.warning(self, "警告", "请先上传半成品对照表文件。")
            self.logTextEdit.append("执行操作失败: 半成品对照表文件未上传")
            return

        try:
            # 获取下单时间
            order_time = self.orderTimeEdit.dateTime().toString("yyyy-MM-dd")

            production_schedule_result = read_production_planning(self.production_schedule_file)
            self.productionScheduleStatusLabel.setText("上传成功")
            self.logTextEdit.append(f"排产计划文件处理成功: {self.production_schedule_file}")

            material_analysis_result = read_material_analysis(self.material_analysis_file)
            self.materialAnalysisStatusLabel.setText("上传成功")
            self.logTextEdit.append(f"生产用料分析文件处理成功: {self.material_analysis_file}")

            in_transit_material_result = read_in_transit_materials(self.in_transit_material_file)
            self.inTransitMaterialStatusLabel.setText("上传成功")
            self.logTextEdit.append(f"生产在途用料文件处理成功: {self.in_transit_material_file}")

            current_inventory_query_result = read_stock_inquiry(self.current_inventory_query_file)
            self.currentInventoryQueryStatusLabel.setText("上传成功")
            self.logTextEdit.append(f"现存量查询文件处理成功: {self.current_inventory_query_file}")

            production_order_list_result = read_production_order_list(self.production_order_list_file)
            self.productionOrderListStatusLabel.setText("上传成功")
            self.logTextEdit.append(f"生产订单列表文件处理成功: {self.production_order_list_file}")

            purchase_order_execution_statistics_result = read_purchase_order_execution_statistics(self.purchase_order_execution_statistics_file)
            self.purchaseOrderExecutionStatisticsStatusLabel.setText("上传成功")
            self.logTextEdit.append(f"采购订单执行统计表文件处理成功: {self.purchase_order_execution_statistics_file}")

            outsourcing_order_execution_statistics_result = read_outsourcing_order_execution_statistics(self.outsourcing_order_execution_statistics_file)
            self.outsourcingOrderExecutionStatisticsStatusLabel.setText("上传成功")
            self.logTextEdit.append(f"委外订单执行统计表文件处理成功: {self.outsourcing_order_execution_statistics_file}")

            material_purchase_information_result = read_material_purchase_information(self.material_purchase_information_file)
            self.materialPurchaseInformationStatusLabel.setText("上传成功")
            self.logTextEdit.append(f"物料采购信息文件处理成功: {self.material_purchase_information_file}")

            semi_finished_product_comparison_result = read_semi_finished_product_comparison(self.semi_finished_product_comparison_file)
            self.semiFinishedProductComparisonStatusLabel.setText("上传成功")
            self.logTextEdit.append(f"半成品对照表文件处理成功: {self.semi_finished_product_comparison_file}")

            self.result_details = execute_production_details(
                production_schedule_result, 
                material_analysis_result, 
                in_transit_material_result, 
                current_inventory_query_result, 
                production_order_list_result,
                purchase_order_execution_statistics_result,
                outsourcing_order_execution_statistics_result,
                material_purchase_information_result,
                semi_finished_product_comparison_result,
                order_time
            )

            # 在这里可以添加进一步的处理逻辑
            self.logTextEdit.append("所有文件处理成功，执行操作完成。")

            # 添加弹窗提示
            QMessageBox.information(self, "完成", "文件处理成功")

        except FileNotFoundError as e:
            QMessageBox.critical(self, "错误", f"文件未找到，请检查文件路径。错误: {str(e)}")
            self.logTextEdit.append(f"文件处理失败: {str(e)}")
            self.productionScheduleStatusLabel.setText("上传失败")
            self.materialAnalysisStatusLabel.setText("上传失败")
            self.inTransitMaterialStatusLabel.setText("上传失败")
            self.currentInventoryQueryStatusLabel.setText("上传失败")
            self.productionOrderListStatusLabel.setText("上传失败")
            self.purchaseOrderExecutionStatisticsStatusLabel.setText("上传失败")
            self.outsourcingOrderExecutionStatisticsStatusLabel.setText("上传失败")
            self.materialPurchaseInformationStatusLabel.setText("上传失败")
            self.semiFinishedProductComparisonStatusLabel.setText("上传失败")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"处理文件时出错: {str(e)}")
            self.logTextEdit.append(f"文件处理失败: {str(e)}")
            self.productionScheduleStatusLabel.setText("上传失败")
            self.materialAnalysisStatusLabel.setText("上传失败")
            self.inTransitMaterialStatusLabel.setText("上传失败")
            self.currentInventoryQueryStatusLabel.setText("上传失败")
            self.productionOrderListStatusLabel.setText("上传失败")
            self.purchaseOrderExecutionStatisticsStatusLabel.setText("上传失败")
            self.outsourcingOrderExecutionStatisticsStatusLabel.setText("上传失败")
            self.materialPurchaseInformationStatusLabel.setText("上传失败")
            self.semiFinishedProductComparisonStatusLabel.setText("上传失败")

    def export_results(self):
        if self.result_details is None or self.result_details.empty:
            QMessageBox.warning(self, "警告", "没有可导出的结果，请先执行操作。")
            self.logTextEdit.append("导出操作失败: 没有可导出的结果")
            return

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "导出结果", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if file_name:
            try:
                # 假设 result_details 是一个 pandas DataFrame
                self.result_details.to_excel(file_name, index=False, header=False)
                self.logTextEdit.append(f"结果成功导出到: {file_name}")
                QMessageBox.information(self, "成功", "结果成功导出")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出结果时出错: {str(e)}")
                self.logTextEdit.append(f"导出操作失败: {str(e)}")

if __name__ == "__main__":
    app = QApplication([])
    window = CreateMaterialsApp()
    window.show()
    app.exec_()
