import pandas as pd
import numpy as np 
from datetime import datetime, timedelta
# from extraction_month import extract_year_and_month, add_months
from create_materials.extraction_month import extract_year_and_month,add_months
 
def execute_production_transit(material_list, in_transit_material_df):

    in_transit_material_df = in_transit_material_df.groupby('子件编码', as_index=False).sum()

    merged_df = pd.merge(material_list, in_transit_material_df, 
                         left_on='子件物料编码', right_on='子件编码', 
                         how='left')

    material_list['生产在途用料'] = merged_df['未领数量'].fillna(0)

    return material_list

def execute_production_inventory(material_list, current_inventory_df):

    # 添加车间库存
    workshop_inventory_df = current_inventory_df[current_inventory_df['仓库名称'].str.contains('车间库')]
    workshop_inventory_df = workshop_inventory_df.groupby('存货编码', as_index=False).sum()

    merged_df = pd.merge(material_list, workshop_inventory_df,
                         left_on='子件物料编码', right_on='存货编码',
                         how='left')
    
    material_list['车间库存'] = merged_df['现存数量'].fillna(0)

    # 添加原材库存
    raw_material_inventory_df = current_inventory_df[current_inventory_df['仓库名称'].str.contains(r'^附件库$|^原材料库$|^半成品库-2')]
    raw_material_inventory_df = raw_material_inventory_df.groupby('存货编码', as_index=False).sum()

    merged_df = pd.merge(material_list, raw_material_inventory_df,
                         left_on='子件物料编码', right_on='存货编码',
                         how='left')
    
    material_list['原材料库存'] = merged_df['现存数量'].fillna(0)

    return material_list

def execute_semi_production_transit(material_list, production_order_df):

    half_finished_in_transit_df = production_order_df[['物料编码', '未完成数量']].groupby('物料编码', as_index=False).sum()

    merged_df = pd.merge(material_list, half_finished_in_transit_df, 
                         left_on='子件物料编码', right_on='物料编码', 
                         how='left')

    material_list['半成品生产在途'] = merged_df['未完成数量'].fillna(0)

    return material_list

def execute_purchasing_transit(material_list, purchase_order_df, outsourcing_order_df):

    # 采购订单
    # 筛选备注列中开头是 '生产-' 的行
    purchase_order_df['备注'] = purchase_order_df['备注'].fillna('')
    purchase_order_df = purchase_order_df[purchase_order_df['备注'].str.startswith('生产-')]
    purchase_order_df = purchase_order_df[['存货编码', '订单未入库数量']].groupby('存货编码', as_index=False).sum()
    purchase_order_df.columns = ['存货编码', '未入库数量']
    # 委外采购
    outsourcing_order_df = outsourcing_order_df[['存货编码', '未入库数量']].groupby('存货编码', as_index=False).sum()
    # 合并 采购订单 和 委外采购
    purchase_order_df = pd.concat([purchase_order_df, outsourcing_order_df], ignore_index=True)
    purchase_order_df = purchase_order_df.groupby('存货编码', as_index=False).sum()

    merged_df = pd.merge(material_list, purchase_order_df, 
                         left_on='子件物料编码', right_on='存货编码', 
                         how='left')
    
    material_list['采购在途'] = merged_df['未入库数量'].fillna(0)

    return material_list

def execute_production_balance(material_list, production_planning_df):
    production_columns = production_planning_df.columns
    mps_column = next((col for col in production_columns if 'mps' in col.lower()), None)
    if mps_column:        
        # 提取列名中的年份和月份
        year, month = extract_year_and_month(mps_column)
        if year and month:   
            for i in range(4):        
                future_year, future_month = add_months(year, month, i)
                new_column_name = f"{future_month}月结余"
                if i == 0:
                    material_list[new_column_name] = material_list['车间库存'] + material_list['原材料库存'] + material_list['半成品生产在途'] + material_list['采购在途'] - material_list['生产在途用料'] - material_list[f'{future_month}月用料']
                else:
                    material_list[new_column_name] = material_list[f"{future_month-1}月结余"] - material_list[f"{future_month}月用料"]

    return material_list

def execute_production_order_mode(material_list, material_purchase_df):

    # 采购方式
    ordering_mode_df = material_purchase_df[['存货编码', '自制/采购']]

    merged_df = pd.merge(material_list, ordering_mode_df, 
                        left_on='子件物料编码', right_on='存货编码', 
                        how='left')

    material_list['采购方式'] = merged_df['自制/采购'].fillna('')

    # 最小起订量
    min_order_quantity_df = material_purchase_df[['存货编码', '最小起订量']]

    merged_df = pd.merge(material_list, min_order_quantity_df, 
                        left_on='子件物料编码', right_on='存货编码', 
                        how='left')
    
    material_list['最小起订量'] = merged_df['最小起订量'].fillna(np.nan)

    # 下单量
    material_list_col = [str(col) for col in material_list.columns]
    month_balance_columns = [col for col in material_list_col if '月结余' in col]

    demand_column  = month_balance_columns[-1]
    min_order_column = '最小起订量'
    order_column = '建议下单量'

    material_list[min_order_column].fillna(0, inplace=True)

    # 将 min_order_column 中的零值替换为一个非常小的数值
    material_list[min_order_column] = material_list[min_order_column].replace(0, 1e-10)

    # 计算下单量
    material_list[order_column] = np.where(
        material_list[demand_column] >= 0, 
        0, 
        np.where(
            material_list[min_order_column] == 1e-10, 
            -material_list[demand_column], 
            np.ceil(-material_list[demand_column] / material_list[min_order_column]) * material_list[min_order_column]
        )
    )
    material_list[min_order_column] = material_list[min_order_column].replace(1e-10, np.nan)

    # 采购周期
    purchase_cycle_df = material_purchase_df[['存货编码', '采购周期（天）']]

    merged_df = pd.merge(material_list, purchase_cycle_df, 
                        left_on='子件物料编码', right_on='存货编码', 
                        how='left')
    
    material_list['采购周期'] = merged_df['采购周期（天）'].fillna('')

    # 计算建议到货时间 
    material_list['建议到货时间'] = ''

    # print(month_balance_columns)
    
    # 初始化一个新的列来记录前一个月是否已经有负值
    material_list['前月负值'] = False

    last_days = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }

    for i, item_month in enumerate(month_balance_columns):
        negative_indices = material_list[material_list[item_month] < 0].index
        
        if i == 0:
            material_list.loc[negative_indices, '建议到货时间'] = ''
            material_list.loc[negative_indices, '前月负值'] = True
        else:
            previous_month = month_balance_columns[i-1][:-3]
            # 只更新那些前月没有负值的行
            for index in negative_indices:
                if not material_list.loc[index, '前月负值'] and material_list.loc[index, '建议到货时间'] == '':
                    last_day = last_days[int(previous_month)]
                    material_list.loc[index, '建议到货时间'] = f"{previous_month}月{last_day}日"
                    material_list.loc[index, '前月负值'] = True  # 标记当前月有负值
                    
    # 删除辅助列
    material_list.drop(columns=['前月负值'], inplace=True)

    # 阶梯价
    step_price_df = material_purchase_df[['存货编码', '阶梯价']]

    merged_df = pd.merge(material_list, step_price_df, 
                        left_on='子件物料编码', right_on='存货编码', 
                        how='left')
    
    material_list['阶梯价'] = merged_df['阶梯价'].fillna('')

    return material_list

def execute_safety_inventory(material_list, production_planning_df):
    material_list['安全库存'] = 0
    production_columns = production_planning_df.columns
    mps_column = next((col for col in production_columns if 'mps' in col.lower()), None)
    if mps_column:        
        # 提取列名中的年份和月份
        year, month = extract_year_and_month(mps_column)
        if year and month:   
            for i in range(4):
                future_year, future_month = add_months(year, month, i)
                material_list['安全库存'] += material_list[f"{future_month}月用料"]

    return material_list

def execute_semi_finished_product_code(material_list, production_planning_df, semi_finished_product_df, current_inventory_df, purchase_order_df, outsourcing_order_df, material_purchase_df, order_time):

    # 获取月份
    production_columns = production_planning_df.columns
    mps_column = next((col for col in production_columns if 'mps' in col.lower()), None)
    if mps_column:        
        # 提取列名中的年份和月份
        year, month = extract_year_and_month(mps_column)
        if year and month:   
            for i in range(4):
                future_year, future_month = add_months(year, month, i)

    # 添加车间库存
    workshop_inventory_df = current_inventory_df[current_inventory_df['仓库名称'].str.contains('车间库')]
    workshop_inventory_df = workshop_inventory_df.groupby('存货编码', as_index=False).sum()

    # 添加原材库存
    raw_material_inventory_df = current_inventory_df[current_inventory_df['仓库名称'].str.contains(r'^附件库$|^原材料库$|^半成品库-2')]
    raw_material_inventory_df = raw_material_inventory_df.groupby('存货编码', as_index=False).sum()  

    # 筛选备注列中开头是 '生产-' 的行
    purchase_order_df['备注'] = purchase_order_df['备注'].fillna('')
    purchase_order_df = purchase_order_df[purchase_order_df['备注'].str.startswith('生产-')]
    purchase_order_df = purchase_order_df[['存货编码', '订单未入库数量']].groupby('存货编码', as_index=False).sum()

    outsourcing_order_df = outsourcing_order_df[['存货编码', '未入库数量']].groupby('存货编码', as_index=False).sum()

    # 初始化半成品物料信息
    semi_finished_product_info = {}  

    # 半成品物料编码
    for i in range(len(material_list)):
        if pd.isna(material_list.loc[i, '子件物料编码']):
            break
        semi_finished_product_row = semi_finished_product_df[['物料编码','子件物料编码','用量2']][semi_finished_product_df['物料编码'] == material_list.loc[i, '子件物料编码']].drop_duplicates()
        if len(semi_finished_product_row) > 0:
            for j in range(len(semi_finished_product_row)):

                sub_material_code = semi_finished_product_row.iloc[j]['子件物料编码']
                material_list.loc[i, f'半成品物料编码_{j+1}'] = sub_material_code
                
                material_list.loc[i, f'半成品物料车间库存_{j+1}'] = 0
                material_list.loc[i, f'半成品物料原材料库存_{j+1}'] = 0
                material_list.loc[i, f'半成品物料采购在途_{j+1}'] = 0
                material_list.loc[i, f'半成品物料结余_{j+1}'] = 0

                # 获取车间库存
                workshop_inventory = workshop_inventory_df[workshop_inventory_df['存货编码'] == sub_material_code]
                if not workshop_inventory.empty:
                    workshop_stock = workshop_inventory.iloc[0]['现存数量']
                else:
                    workshop_stock = 0

                # 获取原材料库存
                raw_material_inventory = raw_material_inventory_df[raw_material_inventory_df['存货编码'] == sub_material_code]
                if not raw_material_inventory.empty:
                    raw_material_stock = raw_material_inventory.iloc[0]['现存数量']
                else:
                    raw_material_stock = 0

                # 获取采购订单
                purchase_order = purchase_order_df[purchase_order_df['存货编码'] == sub_material_code]
                if not purchase_order.empty:
                    purchase_order_stock = purchase_order.iloc[0]['订单未入库数量']
                else:
                    purchase_order_stock = 0

                # 获取委外采购
                outsourcing_order = outsourcing_order_df[outsourcing_order_df['存货编码'] == sub_material_code]
                if not outsourcing_order.empty:
                    outsourcing_order_stock = outsourcing_order.iloc[0]['未入库数量']
                else:
                    outsourcing_order_stock = 0
                
                # 合并采购
                totaled_purchase_stock = purchase_order_stock + outsourcing_order_stock

                material_list.loc[i, f'半成品物料车间库存_{j+1}'] = workshop_stock
                material_list.loc[i, f'半成品物料原材料库存_{j+1}'] = raw_material_stock
                material_list.loc[i, f'半成品物料采购在途_{j+1}'] = totaled_purchase_stock

                # 更新半成品物料信息
                if sub_material_code not in semi_finished_product_info:
                    semi_finished_product_info[sub_material_code] = {
                                                                        '车间库存': workshop_stock, 
                                                                        '原材料库存': raw_material_stock, 
                                                                        '采购在途': totaled_purchase_stock,
                                                                        '需求量': 0}
                semi_finished_product_info[sub_material_code]['需求量'] += material_list.loc[i, f'{future_month}月结余'] * semi_finished_product_row.iloc[j]['用量2']
    
    # 计算结余
    for sub_material_code, info in semi_finished_product_info.items():
        remaining_stock = info['原材料库存'] + info['采购在途'] + info['需求量']
        semi_finished_product_info[sub_material_code]['结余'] = remaining_stock

    # 更新material_list中的结余信息
    order_material_list = []
    for i in range(len(material_list)):
        if pd.isna(material_list.loc[i, '子件物料编码']):
            break
        semi_finished_product_row = semi_finished_product_df[['物料编码','子件物料编码','用量2']][semi_finished_product_df['物料编码'] == material_list.loc[i, '子件物料编码']].drop_duplicates()
        if len(semi_finished_product_row) > 0:
            for j in range(len(semi_finished_product_row)):
                sub_material_code = semi_finished_product_row.iloc[j]['子件物料编码']
                if sub_material_code in semi_finished_product_info:
                    material_list.loc[i, f'半成品物料结余_{j+1}'] = semi_finished_product_info[sub_material_code]['结余']

                # 获取采购方式
                purchase_order_mode = material_purchase_df[material_purchase_df['存货编码'] == sub_material_code]
                if not purchase_order_mode.empty:
                    purchase_order_mode = purchase_order_mode.iloc[0]['自制/采购']
                else:
                    purchase_order_mode = ''

                # 获取最小起订量
                min_order_quantity = material_purchase_df[material_purchase_df['存货编码'] == sub_material_code]
                if not min_order_quantity.empty:
                    min_order_quantity = min_order_quantity.iloc[0]['最小起订量']
                else:
                    min_order_quantity = 1e-10
                
                # 获取阶梯价
                step_price = material_purchase_df[material_purchase_df['存货编码'] == sub_material_code]
                if not step_price.empty:
                    step_price = step_price.iloc[0]['阶梯价']
                else:
                    step_price = ''

                # 获取采购周期
                purchase_cycle = material_purchase_df[material_purchase_df['存货编码'] == sub_material_code]
                if not purchase_cycle.empty:
                    purchase_cycle = purchase_cycle.iloc[0]['采购周期（天）']
                else:
                    purchase_cycle = ''
                    
                material_list.loc[i, f'半成品物料采购方式_{j+1}'] = purchase_order_mode
                material_list.loc[i, f'半成品物料最小起订量_{j+1}'] = min_order_quantity
                material_list.loc[i, f'半成品物料建议下单量_{j+1}'] = np.nan
                material_list.loc[i, f'半成品物料采购周期_{j+1}'] = purchase_cycle

                if sub_material_code not in order_material_list:
                    order_material_list.append(sub_material_code)
                    if material_list.loc[i, f'半成品物料结余_{j+1}'] < 0:
                        if min_order_quantity == 1e-10:
                            material_list.loc[i, f'半成品物料建议下单量_{j+1}'] = -material_list.loc[i, f'半成品物料结余_{j+1}']
                            material_list.loc[i, f'半成品物料最小起订量_{j+1}'] = np.nan
                        else:    
                            material_list.loc[i, f'半成品物料建议下单量_{j+1}'] = np.ceil(-material_list.loc[i, f'半成品物料结余_{j+1}'] / min_order_quantity) * min_order_quantity

                        # 计算到货时间
                        order_date = datetime.strptime(order_time, '%Y-%m-%d')
                        arrival_date = order_date + timedelta(days=purchase_cycle)
                        material_list.loc[i, f'半成品物料到货时间_{j+1}'] = arrival_date.strftime('%Y年%m月%d日')

    return material_list