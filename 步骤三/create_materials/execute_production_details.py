import pandas as pd
import warnings
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressDialog, QApplication, QMainWindow

from create_materials.execute_production_dosage import execute_production_dosage
from create_materials import execute_production_data

# from execute_production_dosage import execute_production_dosage
# import execute_production_data

# 忽略所有警告
warnings.filterwarnings("ignore")

def execute_production_details(production_planning_df, 
                               material_analysis_df, 
                               in_transit_material_df, 
                               current_inventory_df, 
                               production_order_df, 
                               purchase_order_df, 
                               outsourcing_order_df, 
                               material_purchase_df,
                               semi_finished_product_df,
                               order_time):

    # 处理生产计划数据和对应的子件数据
    result_df = execute_production_dosage(production_planning_df, material_analysis_df)

    monthly_plan = result_df.iloc[:5,:].reset_index(drop=True)
    material_list = result_df.iloc[6:,:].reset_index(drop=True)

    # 处理用料明细数据
    material_list.columns = result_df.iloc[5,:].values
    # print(111111)

    # 添加生产在途用料
    material_list = execute_production_data.execute_production_transit(material_list, in_transit_material_df)
    # print(222222)

    # 添加库存
    material_list = execute_production_data.execute_production_inventory(material_list, current_inventory_df)
    # print(333333)

    # 添加半成品生产在途
    material_list = execute_production_data.execute_semi_production_transit(material_list, production_order_df)
    # print(444444)

    # 添加采购在途
    material_list = execute_production_data.execute_purchasing_transit(material_list, purchase_order_df, outsourcing_order_df)
    # print(555555)

    # 添加物料结余
    material_list = execute_production_data.execute_production_balance(material_list, production_planning_df)
    # print(666666)

    # 添加下单模式，最小起订量，阶梯价
    material_list = execute_production_data.execute_production_order_mode(material_list, material_purchase_df)
    # print(777777)

    # 添加安全库存
    material_list = execute_production_data.execute_safety_inventory(material_list, production_planning_df)

    # 添加半成品
    material_list = execute_production_data.execute_semi_finished_product_code(material_list, production_planning_df, semi_finished_product_df, current_inventory_df, purchase_order_df, outsourcing_order_df, material_purchase_df, order_time)


    # 确保monthly_plan具有与material_list相同的列数
    if monthly_plan.shape[1] < material_list.shape[1]:
        # 计算需要添加的列数
        additional_columns = material_list.shape[1] - monthly_plan.shape[1]
        # 添加空列
        for i in range(additional_columns):
            monthly_plan[f'空列{i+1}'] = pd.NA

    monthly_plan.loc[5,:] = material_list.columns

    monthly_plan.reset_index(drop=True, inplace=True)
    material_list.reset_index(drop=True, inplace=True)
    monthly_plan.columns = range(monthly_plan.shape[1])
    material_list.columns = range(material_list.shape[1])
    result_df = pd.concat([monthly_plan, material_list], axis=0)

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
