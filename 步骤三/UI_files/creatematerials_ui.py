from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.fileUploadGroupBox = QtWidgets.QGroupBox(self.splitter)
        self.fileUploadGroupBox.setObjectName("fileUploadGroupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.fileUploadGroupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.uploadProductionScheduleButton = QtWidgets.QPushButton(self.fileUploadGroupBox)
        self.uploadProductionScheduleButton.setObjectName("uploadProductionScheduleButton")
        self.verticalLayout_2.addWidget(self.uploadProductionScheduleButton)
        self.productionScheduleStatusLabel = QtWidgets.QLabel(self.fileUploadGroupBox)
        self.productionScheduleStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.productionScheduleStatusLabel.setObjectName("productionScheduleStatusLabel")
        self.verticalLayout_2.addWidget(self.productionScheduleStatusLabel)
        
        self.uploadMaterialAnalysisButton = QtWidgets.QPushButton(self.fileUploadGroupBox)
        self.uploadMaterialAnalysisButton.setObjectName("uploadMaterialAnalysisButton")
        self.verticalLayout_2.addWidget(self.uploadMaterialAnalysisButton)
        self.materialAnalysisStatusLabel = QtWidgets.QLabel(self.fileUploadGroupBox)
        self.materialAnalysisStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.materialAnalysisStatusLabel.setObjectName("materialAnalysisStatusLabel")
        self.verticalLayout_2.addWidget(self.materialAnalysisStatusLabel)
        
        self.uploadInTransitMaterialButton = QtWidgets.QPushButton(self.fileUploadGroupBox)
        self.uploadInTransitMaterialButton.setObjectName("uploadInTransitMaterialButton")
        self.verticalLayout_2.addWidget(self.uploadInTransitMaterialButton)
        self.inTransitMaterialStatusLabel = QtWidgets.QLabel(self.fileUploadGroupBox)
        self.inTransitMaterialStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.inTransitMaterialStatusLabel.setObjectName("inTransitMaterialStatusLabel")
        self.verticalLayout_2.addWidget(self.inTransitMaterialStatusLabel)
        
        self.uploadCurrentInventoryQueryButton = QtWidgets.QPushButton(self.fileUploadGroupBox)
        self.uploadCurrentInventoryQueryButton.setObjectName("uploadCurrentInventoryQueryButton")
        self.verticalLayout_2.addWidget(self.uploadCurrentInventoryQueryButton)
        self.currentInventoryQueryStatusLabel = QtWidgets.QLabel(self.fileUploadGroupBox)
        self.currentInventoryQueryStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.currentInventoryQueryStatusLabel.setObjectName("currentInventoryQueryStatusLabel")
        self.verticalLayout_2.addWidget(self.currentInventoryQueryStatusLabel)

        self.uploadProductionOrderListButton = QtWidgets.QPushButton(self.fileUploadGroupBox)
        self.uploadProductionOrderListButton.setObjectName("uploadProductionOrderListButton")
        self.verticalLayout_2.addWidget(self.uploadProductionOrderListButton)
        self.productionOrderListStatusLabel = QtWidgets.QLabel(self.fileUploadGroupBox)
        self.productionOrderListStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.productionOrderListStatusLabel.setObjectName("productionOrderListStatusLabel")
        self.verticalLayout_2.addWidget(self.productionOrderListStatusLabel)
        
        self.uploadPurchaseOrderExecutionStatisticsButton = QtWidgets.QPushButton(self.fileUploadGroupBox)
        self.uploadPurchaseOrderExecutionStatisticsButton.setObjectName("uploadPurchaseOrderExecutionStatisticsButton")
        self.verticalLayout_2.addWidget(self.uploadPurchaseOrderExecutionStatisticsButton)
        self.purchaseOrderExecutionStatisticsStatusLabel = QtWidgets.QLabel(self.fileUploadGroupBox)
        self.purchaseOrderExecutionStatisticsStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.purchaseOrderExecutionStatisticsStatusLabel.setObjectName("purchaseOrderExecutionStatisticsStatusLabel")
        self.verticalLayout_2.addWidget(self.purchaseOrderExecutionStatisticsStatusLabel)
        
        self.uploadOutsourcingOrderExecutionStatisticsButton = QtWidgets.QPushButton(self.fileUploadGroupBox)
        self.uploadOutsourcingOrderExecutionStatisticsButton.setObjectName("uploadOutsourcingOrderExecutionStatisticsButton")
        self.verticalLayout_2.addWidget(self.uploadOutsourcingOrderExecutionStatisticsButton)
        self.outsourcingOrderExecutionStatisticsStatusLabel = QtWidgets.QLabel(self.fileUploadGroupBox)
        self.outsourcingOrderExecutionStatisticsStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.outsourcingOrderExecutionStatisticsStatusLabel.setObjectName("outsourcingOrderExecutionStatisticsStatusLabel")
        self.verticalLayout_2.addWidget(self.outsourcingOrderExecutionStatisticsStatusLabel)
        
        self.uploadMaterialPurchaseInformationButton = QtWidgets.QPushButton(self.fileUploadGroupBox)
        self.uploadMaterialPurchaseInformationButton.setObjectName("uploadMaterialPurchaseInformationButton")
        self.verticalLayout_2.addWidget(self.uploadMaterialPurchaseInformationButton)
        self.materialPurchaseInformationStatusLabel = QtWidgets.QLabel(self.fileUploadGroupBox)
        self.materialPurchaseInformationStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.materialPurchaseInformationStatusLabel.setObjectName("materialPurchaseInformationStatusLabel")
        self.verticalLayout_2.addWidget(self.materialPurchaseInformationStatusLabel)
        
        self.uploadSemiFinishedProductComparisonButton = QtWidgets.QPushButton(self.fileUploadGroupBox)
        self.uploadSemiFinishedProductComparisonButton.setObjectName("uploadSemiFinishedProductComparisonButton")
        self.verticalLayout_2.addWidget(self.uploadSemiFinishedProductComparisonButton)
        self.semiFinishedProductComparisonStatusLabel = QtWidgets.QLabel(self.fileUploadGroupBox)
        self.semiFinishedProductComparisonStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.semiFinishedProductComparisonStatusLabel.setObjectName("semiFinishedProductComparisonStatusLabel")
        self.verticalLayout_2.addWidget(self.semiFinishedProductComparisonStatusLabel)

        self.operationGroupBox = QtWidgets.QGroupBox(self.splitter)
        self.operationGroupBox.setObjectName("operationGroupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.operationGroupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        
        # Add a top spacer to push the order time label and edit down
        self.topSpacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(self.topSpacer)
        
        self.orderTimeLabel = QtWidgets.QLabel(self.operationGroupBox)
        self.orderTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.orderTimeLabel.setObjectName("orderTimeLabel")
        self.verticalLayout_3.addWidget(self.orderTimeLabel)
        
        self.orderTimeEdit = QtWidgets.QDateTimeEdit(self.operationGroupBox)
        self.orderTimeEdit.setObjectName("orderTimeEdit")
        self.orderTimeEdit.setDisplayFormat("yyyy-MM-dd")  # Set display format to year-month-day
        self.orderTimeEdit.setCalendarPopup(True)  # Enable calendar popup for easier date selection
        self.orderTimeEdit.setDate(QtCore.QDate.currentDate())  # Set initial date to current date
        self.verticalLayout_3.addWidget(self.orderTimeEdit)
        
        # Add vertical spacers to center the buttons
        self.verticalSpacerTop = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(self.verticalSpacerTop)
        
        self.runButton = QtWidgets.QPushButton(self.operationGroupBox)
        self.runButton.setObjectName("runButton")
        self.verticalLayout_3.addWidget(self.runButton)
        self.exportButton = QtWidgets.QPushButton(self.operationGroupBox)
        self.exportButton.setObjectName("exportButton")
        self.verticalLayout_3.addWidget(self.exportButton)
        
        self.verticalSpacerBottom = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(self.verticalSpacerBottom)
        
        self.logGroupBox = QtWidgets.QGroupBox(self.splitter)
        self.logGroupBox.setObjectName("logGroupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.logGroupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.logTextEdit = QtWidgets.QTextEdit(self.logGroupBox)
        self.logTextEdit.setReadOnly(True)
        self.logTextEdit.setObjectName("logTextEdit")
        self.verticalLayout_4.addWidget(self.logTextEdit)
        
        self.horizontalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "用料明细工具"))
        self.fileUploadGroupBox.setTitle(_translate("MainWindow", "文件上传"))
        self.uploadProductionScheduleButton.setText(_translate("MainWindow", "上传排产计划文件"))
        self.productionScheduleStatusLabel.setText(_translate("MainWindow", "未上传"))
        self.uploadMaterialAnalysisButton.setText(_translate("MainWindow", "上传生产用料分析文件"))
        self.materialAnalysisStatusLabel.setText(_translate("MainWindow", "未上传"))
        self.uploadInTransitMaterialButton.setText(_translate("MainWindow", "上传生产在途用料文件"))
        self.inTransitMaterialStatusLabel.setText(_translate("MainWindow", "未上传"))
        
        self.uploadCurrentInventoryQueryButton.setText(_translate("MainWindow", "上传现存量查询文件"))
        self.currentInventoryQueryStatusLabel.setText(_translate("MainWindow", "未上传"))
        
        self.uploadProductionOrderListButton.setText(_translate("MainWindow", "上传生产订单列表文件"))
        self.productionOrderListStatusLabel.setText(_translate("MainWindow", "未上传"))
        
        self.uploadPurchaseOrderExecutionStatisticsButton.setText(_translate("MainWindow", "上传采购订单执行统计表文件"))
        self.purchaseOrderExecutionStatisticsStatusLabel.setText(_translate("MainWindow", "未上传"))
        
        self.uploadOutsourcingOrderExecutionStatisticsButton.setText(_translate("MainWindow", "上传委外订单执行统计表文件"))
        self.outsourcingOrderExecutionStatisticsStatusLabel.setText(_translate("MainWindow", "未上传"))
        
        self.uploadMaterialPurchaseInformationButton.setText(_translate("MainWindow", "上传物料采购信息文件"))
        self.materialPurchaseInformationStatusLabel.setText(_translate("MainWindow", "未上传"))
        
        self.uploadSemiFinishedProductComparisonButton.setText(_translate("MainWindow", "上传半成品对照表文件"))
        self.semiFinishedProductComparisonStatusLabel.setText(_translate("MainWindow", "未上传"))
        
        self.orderTimeLabel.setText(_translate("MainWindow", "请输入下单时间"))
        
        self.operationGroupBox.setTitle(_translate("MainWindow", "操作"))
        self.runButton.setText(_translate("MainWindow", "执行操作"))
        self.exportButton.setText(_translate("MainWindow", "导出结果"))
        self.logGroupBox.setTitle(_translate("MainWindow", "日志"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
