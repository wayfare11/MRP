import pandas as pd
import re
import warnings
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressDialog, QApplication, QMainWindow
# from create_materials.execute_production_dosage import execute_production_dosage
from execute_production_dosage import execute_production_dosage

# 忽略所有警告
warnings.filterwarnings("ignore")

def extract_year_and_month(column_name):
    # 使用正则表达式匹配 "YYYY年MM月" 格式
    match = re.search(r'(\d{4})年(\d{1,2})月', column_name)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        return year, month
    else:
        return None, None

def add_months(year, month, months):
    month += months
    while month > 12:
        year += 1
        month -= 12
    return year, month

def execute_production_details(production_planning_df, 
                               material_analysis_df, 
                               in_transit_material_df, 
                               current_inventory_df, 
                               production_order_df, 
                               purchase_order_df, 
                               outsourcing_order_df, 
                               material_purchase_df,
                               semi_finished_product_df):

    # 处理生产计划数据和对应的子件数据
    result_df = execute_production_dosage(production_planning_df, material_analysis_df)

    # 添加生产在途用料
    result_df.loc[5, len(result_df.columns)] = "生产在途用料"
    in_transit_material_df = in_transit_material_df.groupby('子件编码', as_index=False).sum()

    # 将生产在途用料添加到 result_df
    for i in range(6, len(result_df)):
        if pd.isna(result_df.iloc[i, 0]):
            break
        in_transit_row = in_transit_material_df[
            in_transit_material_df['子件编码'] == result_df.iloc[i, 0]
        ]
        if not in_transit_row.empty:
            result_df.iloc[i, len(result_df.columns)-1] = in_transit_row.iloc[0]['未领数量']
        else:
            result_df.iloc[i, len(result_df.columns)-1] = 0  # 如果为空则设为0

    # 添加车间库存
    result_df.loc[5, len(result_df.columns)] = "车间库存"
    workshop_inventory_df = current_inventory_df[current_inventory_df['仓库名称'].str.contains('车间库')]
    workshop_inventory_df = workshop_inventory_df.groupby('存货编码', as_index=False).sum()

    # 将车间库存添加到 result_df
    for i in range(6, len(result_df)):
        if pd.isna(result_df.iloc[i, 0]):
            break
        workshop_inventory_row = workshop_inventory_df[
            workshop_inventory_df['存货编码'] == result_df.iloc[i, 0]
        ]
        if not workshop_inventory_row.empty:
            result_df.iloc[i, len(result_df.columns)-1] = workshop_inventory_row.iloc[0]['现存数量']
        else:
            result_df.iloc[i, len(result_df.columns)-1] = 0  # 如果为空则设为0

    # 添加原材料库存
    result_df.loc[5, len(result_df.columns)] = "原材库存"

    raw_material_inventory_df = current_inventory_df[current_inventory_df['仓库名称'].str.contains(r'^附件库$|^原材料库$|^半成品库-2')]
    raw_material_inventory_df = raw_material_inventory_df.groupby('存货编码', as_index=False).sum()

    # 将原材料库存添加到 result_df
    for i in range(6, len(result_df)):
        if pd.isna(result_df.iloc[i, 0]):
            break
        raw_material_inventory_row = raw_material_inventory_df[
            raw_material_inventory_df['存货编码'] == result_df.iloc[i, 0]
        ]
        if not raw_material_inventory_row.empty:
            result_df.iloc[i, len(result_df.columns)-1] = raw_material_inventory_row.iloc[0]['现存数量']
        else:
            result_df.iloc[i, len(result_df.columns)-1] = 0  # 如果为空则设为0

    # 添加半成品生产在途
    result_df.loc[5, len(result_df.columns)] = "半成品生产在途"
    half_finished_in_transit_df = production_order_df[['物料编码', '未完成数量']].groupby('物料编码', as_index=False).sum()

    # 将半成品生产在途添加到 result_df
    for i in range(6, len(result_df)):
        if pd.isna(result_df.iloc[i, 0]):
            break
        half_finished_in_transit_row = half_finished_in_transit_df[
            half_finished_in_transit_df['物料编码'] == result_df.iloc[i, 0]
        ]
        if not half_finished_in_transit_row.empty:
            result_df.iloc[i, len(result_df.columns)-1] = half_finished_in_transit_row.iloc[0]['未完成数量']
        else:
            result_df.iloc[i, len(result_df.columns)-1] = 0  # 如果为空则设为0

    # 添加采购在途
    result_df.loc[5, len(result_df.columns)] = "采购在途"
    # 采购订单
    purchase_order_df = purchase_order_df[['存货编码', '订单未入库数量']].groupby('存货编码', as_index=False).sum()
    purchase_order_df.columns = ['存货编码', '未入库数量']
    # 委外采购
    outsourcing_order_df = outsourcing_order_df[['存货编码', '未入库数量']].groupby('存货编码', as_index=False).sum()
    # 合并 采购订单 和 委外采购
    purchase_order_df = pd.concat([purchase_order_df, outsourcing_order_df], ignore_index=True)
    purchase_order_df = purchase_order_df.groupby('存货编码', as_index=False).sum()

    # 将采购在途添加到 result_df
    for i in range(6, len(result_df)):
        if pd.isna(result_df.iloc[i, 0]):
            break
        purchase_order_row = purchase_order_df[
            purchase_order_df['存货编码'] == result_df.iloc[i, 0]
        ]
        if not purchase_order_row.empty:
            result_df.iloc[i, len(result_df.columns)-1] = purchase_order_row.iloc[0]['未入库数量']
        else:
            result_df.iloc[i, len(result_df.columns)-1] = 0  # 如果为空则设为0

    production_columns = production_planning_df.columns
    mps_column = next((col for col in production_columns if 'mps' in col.lower()), None)
    if mps_column:        
        # 提取列名中的年份和月份
        year, month = extract_year_and_month(mps_column)
        if year and month:   
            for i in range(4):        
                future_year, future_month = add_months(year, month, i)
                result_df.loc[5, len(result_df.columns)] = f"{future_month}月结余"

                # 第一个月结余 车间 + 原材 + 半成品 + 采购在途 - 需求 - 生产在途
                if i == 0:
                    result_df.loc[6:, len(result_df.columns)-1] = (result_df.iloc[6:, len(result_df.columns)-5] #车间
                                                                        + result_df.iloc[6:, len(result_df.columns)-4] #原材料
                                                                        + result_df.iloc[6:, len(result_df.columns)-3] #半成品
                                                                        + result_df.iloc[6:, len(result_df.columns)-2] #采购在途
                                                                        - result_df.iloc[6:, len(result_df.columns)-10] #需求
                                                                        - result_df.iloc[6:, len(result_df.columns)-6] ) #生产在途
                # 其余月为上月的结余 - 需求
                else:
                    result_df.loc[6:, len(result_df.columns)-1] = (result_df.iloc[6:, len(result_df.columns)-2] #上月结余
                                                                        - result_df.iloc[6:, len(result_df.columns)-10] ) #需求
    # 添加下单模式
    result_df.loc[5, len(result_df.columns)] = "下单模式"

    ordering_mode_df = material_purchase_df[['存货编码', '自制/采购']]
    # 下单模式载入
    for i in range(6, len(result_df)):
        if pd.isna(result_df.iloc[i, 0]):
            break
        ordering_mode_row = ordering_mode_df[
            ordering_mode_df['存货编码'] == result_df.iloc[i, 0]]
        if not ordering_mode_row.empty:
            result_df.iloc[i, len(result_df.columns)-1] = ordering_mode_row.iloc[0]['自制/采购']
        else:
            result_df.iloc[i, len(result_df.columns)-1] = ''  # 如果为空则设为空字符串

    # 添加安全库存
    result_df.loc[5, len(result_df.columns)] = "安全库存"

    # 安全库存为四个月用料的和
    result_df.loc[6:, len(result_df.columns)-1] = (result_df.iloc[6:, len(result_df.columns)-15]
                                                    + result_df.iloc[6:, len(result_df.columns)-14]
                                                    + result_df.iloc[6:, len(result_df.columns)-13]
                                                    + result_df.iloc[6:, len(result_df.columns)-12])

    # 添加半成品编码
    result_df.loc[5, len(result_df.columns)] = "半成品编码_1"
    count_semi_finished = 1

    len_balance = len(result_df.columns)
    # 半成品编码
    for i in range(6, len(result_df)):
        if pd.isna(result_df.iloc[i, 0]):
            break
        semi_finished_product_row = semi_finished_product_df[
            semi_finished_product_df['物料编码'] == result_df.iloc[i, 0]
        ]
        semi_finished_product_row = semi_finished_product_row.drop_duplicates(subset=['子件物料编码'])
        if not semi_finished_product_row.empty:
            for j in range(len(semi_finished_product_row)):
                if j == 0:
                    result_df.iloc[i, len_balance-1] = semi_finished_product_row.iloc[j]['子件物料编码']
                else:
                    if len(result_df.columns) <= len_balance + j - 1:
                        result_df.loc[5, len(result_df.columns)] = "半成品编码"+f"_{j+1}"
                        count_semi_finished += 1
                    result_df.iloc[i, len_balance - 1 + j] = semi_finished_product_row.iloc[j]['子件物料编码']

    # 半成品车间库存
    result_df.loc[5, len(result_df.columns)] = "半成品车间库存_1"

    len_semi_finished = len(result_df.columns)
    for i in range(6, len(result_df)):
        if pd.isna(result_df.iloc[i, len_balance-1]):
            continue


    return result_df
        
def main():
    # 示例数据
    production_planning_df = pd.DataFrame({
        '存货编码': ['A', 'B', 'C'],
        '规格型号': ['规格A', '规格B', '规格C'],
        '2023年8月MPS': [100, 200, 300],
        '2023年9月MPS': [110, 210, 310],
        '2023年10月MPS': [120, 220, 320],
        '2023年11月MPS': [130, 230, 330]
    })

    material_analysis_df = pd.DataFrame({
        '物料编码': ['A', 'A', 'B', 'B', 'C'],
        '子件物料编码': ['X1', 'X2', 'X1', 'X3', 'X4'],
        '子件物料名称': ['名称1', '名称2', '名称1', '名称3', '名称4'],
        '子件物料规格': ['规格1', '规格2', '规格1', '规格3', '规格4'],
        '标准用量': [10, 20, 30, 40, 50]
    })

    in_transit_material_df = pd.DataFrame({
        '子件编码': ['X1', 'X2', 'X3', 'X1'],
        '未领数量': [100, 200, 300, 200]
    })

    current_inventory_df = pd.DataFrame({
        '存货编码': ['X1', 'X2', 'X3', 'X4', 'X1', 'X2', 'X3', 'X4'],
        '仓库名称': ['车间库A', '车间库B', '车间库A', '车间库B', '附件库', '原材料库', '半成品库-2', '原材料库'],
        '现存数量': [500, 600, 700, 800, 1000, 1100, 1200, 1300]
    })

    production_order_df = pd.DataFrame({
        '物料编码': ['X1', 'X2', 'X3', 'X4'],
        '未完成数量': [50, 60, 70, 80]
    })

    purchase_order_df = pd.DataFrame({
        '存货编码': ['X1', 'X2', 'X3', 'X4'],
        '订单未入库数量': [150, 160, 170, 180]
    })

    outsourcing_order_df = pd.DataFrame({
        '存货编码': ['X1', 'X2', 'X3', 'X4'],
        '未入库数量': [25, 35, 45, 55]
    })

    material_purchase_df = pd.DataFrame({
        '存货编码': ['X1', 'X2', 'X3', 'X4'],
        '自制/采购': ['自制', '采购', '采购', '自制']
    })

    semi_finished_product_df = pd.DataFrame({
        '物料编码': ['X1', 'X2', 'X3', 'X4', 'X1', 'X1', 'X2','X3','X3','X3','X3',],
        '子件物料编码': ['Y1', 'Y1', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7','Y1','Y2','Y3','Y4',]
    })

    app = QApplication([])
    result_df = execute_production_details(production_planning_df, 
                                           material_analysis_df, 
                                           in_transit_material_df, 
                                           current_inventory_df, 
                                           production_order_df, 
                                           purchase_order_df, 
                                           outsourcing_order_df, 
                                           material_purchase_df,
                                           semi_finished_product_df)
    print(result_df)
    app.quit()  # 自动退出应用程序

if __name__ == '__main__':
    main()
