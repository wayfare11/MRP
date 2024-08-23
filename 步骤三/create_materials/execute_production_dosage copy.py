import re
import pandas as pd
import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressDialog, QApplication, QMainWindow

from create_materials.extraction_month import extract_year_and_month, add_months
# from extraction_month import extract_year_and_month, add_months

def execute_production_dosage(production_planning_df, material_analysis_df, parent=None):
    # 获取 production_planning_df 的列名
    production_columns = production_planning_df.columns

    # 查找 production_planning_df 中第一个包含“mps”的列名
    mps_column = next((col for col in production_columns if 'mps' in col.lower()), None)

    if mps_column:        
        # 提取列名中的年份和月份
        year, month = extract_year_and_month(mps_column)
        if year and month:            
            # 创建一个新的 DataFrame
            new_data = []
            for i in range(4):
                future_year, future_month = add_months(year, month, i)
                new_data.append([None, None, f"{future_month}月计划"])
            
            result_df = pd.DataFrame(new_data)

            # 获取“存货编码”列的数据
            if '存货编码' in production_planning_df.columns and '规格型号' in production_planning_df.columns:
                inventory_codes = production_planning_df['存货编码'].tolist()
                general_specs = production_planning_df['规格型号'].tolist()
                
                # 获取未来四个月的 MPS 数据
                mps_data = {f"{add_months(year, month, i)[1]}月计划": [] for i in range(4)}
                for i in range(4):
                    future_year, future_month = add_months(year, month, i)
                    for col in production_columns:
                        col_year, col_month = extract_year_and_month(col)
                        if col_year == future_year and col_month == future_month and 'mps' in col.lower():
                            mps_data[f"{future_month}月计划"] = production_planning_df[col].tolist()
                            break
                    else:
                        mps_data[f"{future_month}月计划"] = [None] * len(inventory_codes)
                
                # 确保 result_df 有足够的列来容纳存货编码和 MPS 数据
                while len(result_df.columns) < 3 + len(inventory_codes):
                    result_df[len(result_df.columns)] = None
                
                # 将“存货编码”和 MPS 数据添加到 result_df 中
                for idx, code in enumerate(inventory_codes):
                    result_df.loc[4, 3 + idx] = code
                    result_df.loc[5, 3 + idx] = general_specs[idx]  # 添加通用规格
                    for i in range(4):
                        result_df.loc[i, 3 + idx] = mps_data[f"{add_months(year, month, i)[1]}月计划"][idx]

                # 添加一列用于存放每个月的和
                total_column_index = len(result_df.columns)
                for i in range(4):
                    month_plan = f"{add_months(year, month, i)[1]}月计划"
                    result_df.loc[i, total_column_index] = sum(filter(None, mps_data[month_plan]))

            # 在第 5 行的第 0 到第 2 列中填入指定的字符串
            result_df.loc[5, 0] = '子件物料编码'
            result_df.loc[5, 1] = '子件物料名称'
            result_df.loc[5, 2] = '子件物料规格'

            # 获取 material_analysis_df 中 '子件物料编码', '子件物料名称', 和 '子件物料规格' 去重后的值
            if '子件物料编码' in material_analysis_df.columns and '子件物料名称' in material_analysis_df.columns and '子件物料规格' in material_analysis_df.columns:
                unique_materials = material_analysis_df[['子件物料编码', '子件物料名称', '子件物料规格']].drop_duplicates()
                for idx, row in unique_materials.iterrows():
                    result_df.loc[6 + idx, 0] = row['子件物料编码']
                    result_df.loc[6 + idx, 1] = row['子件物料名称']
                    result_df.loc[6 + idx, 2] = row['子件物料规格']
            
            # 初始化进度对话框
            progress_dialog = QProgressDialog("处理子件数据中...", "取消", 0, 100, parent)
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setValue(0)
            progress_dialog.setWindowTitle("进度条")  # 设置窗口标题为“进度条”
            
            # 调整进度对话框的大小
            progress_dialog.resize(400, 100)
            
            progress_dialog.show()

            # # 从第4行的第3列开始 往右读到不是空的值，循环变量j
            # total_columns = len(result_df.columns) - 3  # 总列数减去前三列
            # for j in range(3, len(result_df.columns)):
            #     if pd.isna(result_df.iloc[4, j]):
            #         break
            #     # 更新进度条
            #     progress = int((j - 3) / total_columns * 100)
            #     progress_dialog.setValue(progress)
            #     QApplication.processEvents()  # 处理事件以更新进度条

            #     # 检查是否被取消
            #     if progress_dialog.wasCanceled():
            #         print("操作被取消")
            #         return None

            #     # 从第6行的第1列开始 往下读，循环变量i
            #     for i in range(6, len(result_df)):
            #         if pd.isna(result_df.iloc[i, 0]):
            #             break
            #         material_row = material_analysis_df[
            #             (material_analysis_df['物料编码'] == result_df.iloc[4, j]) &
            #             (material_analysis_df['子件物料编码'] == result_df.iloc[i, 0])
            #         ]
            #         if not material_row.empty:
            #             # 若存在，设 result_df的第（i，j）的值为 material_analysis_df查找到的第一个的[‘用量’]的值
            #             result_df.iloc[i, j] = material_row.iloc[0]['标准用量']

            for i in range(4):
                future_month = add_months(year, month, i)[1]
                if i==0:
                    result_df.loc[5, len(result_df.columns)-1] = f"{future_month}月用料"
                else:
                    result_df.loc[5, len(result_df.columns)] = f"{future_month}月用料"

                for j in range(6, len(result_df)):
                    if pd.isna(result_df.iloc[j, 0]):
                        break

                    row_data = result_df.iloc[j, 3:len(production_planning_df)+3].tolist()
                    # 将 np.nan 转换为字符串 'nan' 便于阅读，并将 numpy 类型转换为 Python 原生类型
                    row_data = [x if pd.notna(x) else 0 for x in row_data]
                    row_data = [x.item() if isinstance(x, (np.integer, np.floating)) else x for x in row_data]

                    row_data = np.array(row_data, dtype=float)
                    mps_data_month_plan = np.array(mps_data[f'{future_month}月计划'], dtype=float)
                    
                    result_df.iloc[j, len(production_planning_df)+3+i] = sum(row_data*mps_data_month_plan)
                    
            progress_dialog.setValue(100)  # 进度完成

            return result_df