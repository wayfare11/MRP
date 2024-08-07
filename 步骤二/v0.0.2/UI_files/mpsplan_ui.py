from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                color: #000000;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }

            QPushButton {
                background-color: #f0f0f0;
                color: #000000;
                border: 1px solid #ccc;
                padding: 10px 20px;
                font-size: 14px;
                margin: 4px 2px;
                border-radius: 8px;
            }

            QPushButton:hover {
                background-color: #e0e0e0;
            }

            QLabel {
                color: #000000;
                font-size: 14px;
                text-align: center;
            }

            QLineEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 4px;
            }

            QProgressBar {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 4px;
                text-align: center;
                color: #000000;
            }

            QProgressBar::chunk {
                background-color: #e0e0e0;
            }

            QTableWidget {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 4px;
            }

            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 4px;
            }
        """)
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
        self.uploadSalesForecastButton = QtWidgets.QPushButton(self.fileUploadGroupBox)
        self.uploadSalesForecastButton.setObjectName("uploadSalesForecastButton")
        self.verticalLayout_2.addWidget(self.uploadSalesForecastButton)
        self.salesForecastStatusLabel = QtWidgets.QLabel(self.fileUploadGroupBox)
        self.salesForecastStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.salesForecastStatusLabel.setObjectName("salesForecastStatusLabel")
        self.verticalLayout_2.addWidget(self.salesForecastStatusLabel)
        self.uploadInventoryButton = QtWidgets.QPushButton(self.fileUploadGroupBox)
        self.uploadInventoryButton.setObjectName("uploadInventoryButton")
        self.verticalLayout_2.addWidget(self.uploadInventoryButton)
        self.inventoryStatusLabel = QtWidgets.QLabel(self.fileUploadGroupBox)
        self.inventoryStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.inventoryStatusLabel.setObjectName("inventoryStatusLabel")
        self.verticalLayout_2.addWidget(self.inventoryStatusLabel)
        self.uploadProductionOrdersButton = QtWidgets.QPushButton(self.fileUploadGroupBox)
        self.uploadProductionOrdersButton.setObjectName("uploadProductionOrdersButton")
        self.verticalLayout_2.addWidget(self.uploadProductionOrdersButton)
        self.productionOrdersStatusLabel = QtWidgets.QLabel(self.fileUploadGroupBox)
        self.productionOrdersStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.productionOrdersStatusLabel.setObjectName("productionOrdersStatusLabel")
        self.verticalLayout_2.addWidget(self.productionOrdersStatusLabel)
        self.uploadSafetyStockButton = QtWidgets.QPushButton(self.fileUploadGroupBox)
        self.uploadSafetyStockButton.setObjectName("uploadSafetyStockButton")
        self.verticalLayout_2.addWidget(self.uploadSafetyStockButton)
        self.safetyStockStatusLabel = QtWidgets.QLabel(self.fileUploadGroupBox)
        self.safetyStockStatusLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.safetyStockStatusLabel.setObjectName("safetyStockStatusLabel")
        self.verticalLayout_2.addWidget(self.safetyStockStatusLabel)
        self.operationGroupBox = QtWidgets.QGroupBox(self.splitter)
        self.operationGroupBox.setObjectName("operationGroupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.operationGroupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # 添加工时输入框
        self.month1HoursLabel = QtWidgets.QLabel(self.operationGroupBox)
        self.month1HoursLabel.setObjectName("month1HoursLabel")
        self.verticalLayout_3.addWidget(self.month1HoursLabel)
        self.month1HoursInput = QtWidgets.QLineEdit(self.operationGroupBox)
        self.month1HoursInput.setObjectName("month1HoursInput")
        self.verticalLayout_3.addWidget(self.month1HoursInput)

        self.month2HoursLabel = QtWidgets.QLabel(self.operationGroupBox)
        self.month2HoursLabel.setObjectName("month2HoursLabel")
        self.verticalLayout_3.addWidget(self.month2HoursLabel)
        self.month2HoursInput = QtWidgets.QLineEdit(self.operationGroupBox)
        self.month2HoursInput.setObjectName("month2HoursInput")
        self.verticalLayout_3.addWidget(self.month2HoursInput)

        self.month3HoursLabel = QtWidgets.QLabel(self.operationGroupBox)
        self.month3HoursLabel.setObjectName("month3HoursLabel")
        self.verticalLayout_3.addWidget(self.month3HoursLabel)
        self.month3HoursInput = QtWidgets.QLineEdit(self.operationGroupBox)
        self.month3HoursInput.setObjectName("month3HoursInput")
        self.verticalLayout_3.addWidget(self.month3HoursInput)

        self.month4HoursLabel = QtWidgets.QLabel(self.operationGroupBox)
        self.month4HoursLabel.setObjectName("month4HoursLabel")
        self.verticalLayout_3.addWidget(self.month4HoursLabel)
        self.month4HoursInput = QtWidgets.QLineEdit(self.operationGroupBox)
        self.month4HoursInput.setObjectName("month4HoursInput")
        self.verticalLayout_3.addWidget(self.month4HoursInput)

        self.runButton = QtWidgets.QPushButton(self.operationGroupBox)
        self.runButton.setObjectName("runButton")
        self.verticalLayout_3.addWidget(self.runButton)
        self.exportButton = QtWidgets.QPushButton(self.operationGroupBox)
        self.exportButton.setObjectName("exportButton")
        self.verticalLayout_3.addWidget(self.exportButton)
        self.logGroupBox = QtWidgets.QGroupBox(self.splitter)
        self.logGroupBox.setObjectName("logGroupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.logGroupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.logTextEdit = QtWidgets.QTextEdit(self.logGroupBox)
        self.logTextEdit.setReadOnly(True)
        self.logTextEdit.setStyleSheet("""
            QTextEdit {
                background-color: #ffffff;
                color: #000000;
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 4px;
            }
        """)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "排产计划工具"))
        self.fileUploadGroupBox.setTitle(_translate("MainWindow", "文件上传"))
        self.uploadSalesForecastButton.setText(_translate("MainWindow", "上传销售预测文件"))
        self.salesForecastStatusLabel.setText(_translate("MainWindow", "未上传"))
        self.uploadInventoryButton.setText(_translate("MainWindow", "上传现存量查询文件"))
        self.inventoryStatusLabel.setText(_translate("MainWindow", "未上传"))
        self.uploadProductionOrdersButton.setText(_translate("MainWindow", "上传生产订单列表文件"))
        self.productionOrdersStatusLabel.setText(_translate("MainWindow", "未上传"))
        self.uploadSafetyStockButton.setText(_translate("MainWindow", "上传安全库存文件"))
        self.safetyStockStatusLabel.setText(_translate("MainWindow", "未上传"))
        self.operationGroupBox.setTitle(_translate("MainWindow", "操作"))
        self.runButton.setText(_translate("MainWindow", "执行操作"))
        self.exportButton.setText(_translate("MainWindow", "导出结果"))
        self.logGroupBox.setTitle(_translate("MainWindow", "日志"))

        # 设置工时输入框的标签
        self.month1HoursLabel.setText(_translate("MainWindow", "第一个月工时:"))
        self.month2HoursLabel.setText(_translate("MainWindow", "第二个月工时:"))
        self.month3HoursLabel.setText(_translate("MainWindow", "第三个月工时:"))
        self.month4HoursLabel.setText(_translate("MainWindow", "第四个月工时:"))
