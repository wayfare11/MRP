import pulp
import pandas as pd
from .demand_calculation import get_next_month

def is_quarter_end(month):
    """判断给定月份是否为季度末"""
    # 提取月份部分并转换为整数
    month_int = int(month.split('年')[1].replace('月', ''))
    return month_int in [3, 6, 9, 12]

def round_up_to_nearest_x(x, multiple):
    """将数值向上取整到最近的 multiple 的倍数"""
    return max(0, ((x + multiple - 1) // multiple) * multiple)

def calculate_mps(df, n, total_hours, min_productions):
    """计算MPS列和结余列"""
    total_hours_n = 0
    total_hours_n1 = 0
    total_hours_n2 = 0
    total_hours_n3 = 0

    total_production_n = 0
    total_production_n1 = 0
    total_production_n2 = 0
    total_production_n3 = 0

    # 创建问题实例
    prob = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

    # 创建整数变量和二进制变量的字典
    P_vars = {}
    Y_vars = {}

    # 定义 big_number
    big_number = 10**9

    for index, row in df.iterrows():
        stock_code = row['存货编码']  # 获取存货编码
        a = row['月底库存']  # n-1月库存
        b = row[f'{n}需求']  # n月预测订单量
        c = row[f'{get_next_month(n, 1)}预测']  # n+1月预测订单量
        d = row[f'{get_next_month(n, 2)}预测']  # n+2月预测订单量
        e = row[f'{get_next_month(n, 3)}预测']  # n+3月预测订单量
        safety_stock = row['安全库存']  # 安全库存
        loss = row['损耗']  # 损耗
        min_production = row['最小排产量']  # 最小排产量
        standard_hours = row['标准工时']  # 每个产品的标准工时

        if min_production == 0:
            min_production = 1

        # 确保所有值都是数值类型
        a = 0 if pd.isna(a) else a
        b = 0 if pd.isna(b) else b
        c = 0 if pd.isna(c) else c
        d = 0 if pd.isna(d) else d
        e = 0 if pd.isna(e) else e
        loss = 0 if pd.isna(loss) else loss

        # 计算每个月的结余
        balance_n = a - b
        balance_n1 = balance_n - c
        balance_n2 = balance_n1 - d
        balance_n3 = balance_n2 - e

        # 如果库存能满足四个月的需求且季度末结余大于等于安全库存，则不需要生产
        if (balance_n >= 0 and balance_n1 >= 0 and balance_n2 >= 0 and balance_n3 >= 0 and
            ((is_quarter_end(n) and balance_n >= safety_stock) or
             (is_quarter_end(get_next_month(n, 1)) and balance_n1 >= safety_stock) or
             (is_quarter_end(get_next_month(n, 2)) and balance_n2 >= safety_stock) or
             (is_quarter_end(get_next_month(n, 3)) and balance_n3 >= safety_stock))):
            # 输出结果并保存到DataFrame
            df.at[index, f'mps {n}'] = 0
            df.at[index, f'mps {get_next_month(n, 1)}'] = 0
            df.at[index, f'mps {get_next_month(n, 2)}'] = 0
            df.at[index, f'mps {get_next_month(n, 3)}'] = 0

            df.at[index, f'{n}结余'] = balance_n
            df.at[index, f'{get_next_month(n, 1)}结余'] = balance_n1
            df.at[index, f'{get_next_month(n, 2)}结余'] = balance_n2
            df.at[index, f'{get_next_month(n, 3)}结余'] = balance_n3

            continue

        # 创建整数变量和二进制变量
        P_vars[stock_code] = {
            'P6': pulp.LpVariable(f"P6_{stock_code}", lowBound=0, cat='Integer'),
            'P7': pulp.LpVariable(f"P7_{stock_code}", lowBound=0, cat='Integer'),
            'P8': pulp.LpVariable(f"P8_{stock_code}", lowBound=0, cat='Integer'),
            'P9': pulp.LpVariable(f"P9_{stock_code}", lowBound=0, cat='Integer')
        }
        Y_vars[stock_code] = {
            'Y6': pulp.LpVariable(f"Y6_{stock_code}", cat='Binary'),
            'Y7': pulp.LpVariable(f"Y7_{stock_code}", cat='Binary'),
            'Y8': pulp.LpVariable(f"Y8_{stock_code}", cat='Binary'),
            'Y9': pulp.LpVariable(f"Y9_{stock_code}", cat='Binary')
        }

        # 约束条件
        prob += P_vars[stock_code]['P6'] <= big_number * Y_vars[stock_code]['Y6']
        prob += P_vars[stock_code]['P7'] <= big_number * Y_vars[stock_code]['Y7']
        prob += P_vars[stock_code]['P8'] <= big_number * Y_vars[stock_code]['Y8']
        prob += P_vars[stock_code]['P9'] <= big_number * Y_vars[stock_code]['Y9']

        prob += P_vars[stock_code]['P6'] >= 1 * Y_vars[stock_code]['Y6']
        prob += P_vars[stock_code]['P7'] >= 1 * Y_vars[stock_code]['Y7']
        prob += P_vars[stock_code]['P8'] >= 1 * Y_vars[stock_code]['Y8']
        prob += P_vars[stock_code]['P9'] >= 1 * Y_vars[stock_code]['Y9']

        prob += a + P_vars[stock_code]['P6'] >= b + loss * Y_vars[stock_code]['Y6']
        prob += a + P_vars[stock_code]['P6'] - (b + loss * Y_vars[stock_code]['Y6']) + P_vars[stock_code]['P7'] >= c + loss * Y_vars[stock_code]['Y7']
        prob += a + P_vars[stock_code]['P6'] - (b + loss * Y_vars[stock_code]['Y6']) + P_vars[stock_code]['P7'] - (c + loss * Y_vars[stock_code]['Y7']) + P_vars[stock_code]['P8'] >= d + loss * Y_vars[stock_code]['Y8']
        prob += a + P_vars[stock_code]['P6'] - (b + loss * Y_vars[stock_code]['Y6']) + P_vars[stock_code]['P7'] - (c + loss * Y_vars[stock_code]['Y7']) + P_vars[stock_code]['P8'] - (d + loss * Y_vars[stock_code]['Y8']) + P_vars[stock_code]['P9'] >= e + loss * Y_vars[stock_code]['Y9']

        # 确保季度末结余不低于安全库存
        if is_quarter_end(n):
            prob += a + P_vars[stock_code]['P6'] - (b + loss * Y_vars[stock_code]['Y6']) >= safety_stock
        if is_quarter_end(get_next_month(n, 1)):
            prob += a + P_vars[stock_code]['P6'] - (b + loss * Y_vars[stock_code]['Y6']) + P_vars[stock_code]['P7'] - (c + loss * Y_vars[stock_code]['Y7']) >= safety_stock
        if is_quarter_end(get_next_month(n, 2)):
            prob += a + P_vars[stock_code]['P6'] - (b + loss * Y_vars[stock_code]['Y6']) + P_vars[stock_code]['P7'] - (c + loss * Y_vars[stock_code]['Y7']) + P_vars[stock_code]['P8'] - (d + loss * Y_vars[stock_code]['Y8']) >= safety_stock
        if is_quarter_end(get_next_month(n, 3)):
            prob += a + P_vars[stock_code]['P6'] - (b + loss * Y_vars[stock_code]['Y6']) + P_vars[stock_code]['P7'] - (c + loss * Y_vars[stock_code]['Y7']) + P_vars[stock_code]['P8'] - (d + loss * Y_vars[stock_code]['Y8']) + P_vars[stock_code]['P9'] - (e + loss * Y_vars[stock_code]['Y9']) >= safety_stock

        # 添加总工时约束
        total_hours_n += P_vars[stock_code]['P6'] * standard_hours
        total_hours_n1 += P_vars[stock_code]['P7'] * standard_hours
        total_hours_n2 += P_vars[stock_code]['P8'] * standard_hours
        total_hours_n3 += P_vars[stock_code]['P9'] * standard_hours

        # 添加总生产量约束
        total_production_n += P_vars[stock_code]['P6']
        total_production_n1 += P_vars[stock_code]['P7']
        total_production_n2 += P_vars[stock_code]['P8']
        total_production_n3 += P_vars[stock_code]['P9']

    # 添加每个月的总工时约束
    prob += total_hours_n <= total_hours[0]
    prob += total_hours_n1 <= total_hours[1]
    prob += total_hours_n2 <= total_hours[2]
    prob += total_hours_n3 <= total_hours[3]

    # 使用 CBC 求解器并关闭输出
    solver = pulp.PULP_CBC_CMD(msg=False)

    prob.solve(solver)

    # 检查求解状态
    if pulp.LpStatus[prob.status] != 'Optimal':
        return None, f"没有找到可行解: {pulp.LpStatus[prob.status]}，请修改工时、最低生产量或安全库存！"
    else:
        print("Solver found an optimal solution.")

    # 获取求解结果并调整到最小排产量的倍数
    for index, row in df.iterrows():
        stock_code = row['存货编码']
        min_production = row['最小排产量']
        if min_production == 0:
            min_production = 1

        if stock_code in P_vars:
            mps_n = round_up_to_nearest_x(pulp.value(P_vars[stock_code]['P6']) if pulp.value(P_vars[stock_code]['P6']) is not None else 0, min_production)
            mps_n1 = round_up_to_nearest_x(pulp.value(P_vars[stock_code]['P7']) if pulp.value(P_vars[stock_code]['P7']) is not None else 0, min_production)
            mps_n2 = round_up_to_nearest_x(pulp.value(P_vars[stock_code]['P8']) if pulp.value(P_vars[stock_code]['P8']) is not None else 0, min_production)
            mps_n3 = round_up_to_nearest_x(pulp.value(P_vars[stock_code]['P9']) if pulp.value(P_vars[stock_code]['P9']) is not None else 0, min_production)

            # 计算结余
            a = row['月底库存']
            b = row[f'{n}需求']
            c = row[f'{get_next_month(n, 1)}预测']
            d = row[f'{get_next_month(n, 2)}预测']
            e = row[f'{get_next_month(n, 3)}预测']
            loss = row['损耗']

            balance_n = a + mps_n - b - loss * (1 if mps_n > 0 else 0)
            balance_n1 = balance_n + mps_n1 - c - loss * (1 if mps_n1 > 0 else 0)
            balance_n2 = balance_n1 + mps_n2 - d - loss * (1 if mps_n2 > 0 else 0)
            balance_n3 = balance_n2 + mps_n3 - e - loss * (1 if mps_n3 > 0 else 0)
            
            # 输出结果并保存到DataFrame
            df.at[index, f'mps {n}'] = mps_n
            df.at[index, f'mps {get_next_month(n, 1)}'] = mps_n1
            df.at[index, f'mps {get_next_month(n, 2)}'] = mps_n2
            df.at[index, f'mps {get_next_month(n, 3)}'] = mps_n3

            df.at[index, f'{n}结余'] = balance_n
            df.at[index, f'{get_next_month(n, 1)}结余'] = balance_n1
            df.at[index, f'{get_next_month(n, 2)}结余'] = balance_n2
            df.at[index, f'{get_next_month(n, 3)}结余'] = balance_n3

    # 重新计算每个月的生产用时
    total_hours_n = sum(df.at[index, f'mps {n}'] * df.at[index, '标准工时'] for index in df.index)
    total_hours_n1 = sum(df.at[index, f'mps {get_next_month(n, 1)}'] * df.at[index, '标准工时'] for index in df.index)
    total_hours_n2 = sum(df.at[index, f'mps {get_next_month(n, 2)}'] * df.at[index, '标准工时'] for index in df.index)
    total_hours_n3 = sum(df.at[index, f'mps {get_next_month(n, 3)}'] * df.at[index, '标准工时'] for index in df.index)

    # 打印每个月的生产用时
    print(f"Total production hours for month {n}: {total_hours_n}")
    print(f"Total production hours for month {get_next_month(n, 1)}: {total_hours_n1}")
    print(f"Total production hours for month {get_next_month(n, 2)}: {total_hours_n2}")
    print(f"Total production hours for month {get_next_month(n, 3)}: {total_hours_n3}")

    # 检查并调整每个月的生产量
    for i, min_production in enumerate(min_productions):
        month = get_next_month(n, i)
        total_production = sum(df.at[index, f'mps {month}'] for index in df.index)
        if total_production < min_production:
            # 计算需要增加的生产量
            additional_production = min_production - total_production
            remaining_hours = total_hours[i] - sum(df.at[index, f'mps {month}'] * df.at[index, '标准工时'] for index in df.index)
            
            # 按比例分配增加的生产量
            for index, row in df.iterrows():
                if additional_production <= 0 or remaining_hours <= 0:
                    break
                stock_code = row['存货编码']
                min_production = row['最小排产量']
                if min_production == 0:
                    min_production = 1
                safety_stock = row['安全库存']
                current_production = df.at[index, f'mps {month}']
                additional_units = round_up_to_nearest_x(min(additional_production, remaining_hours // row['标准工时']), min_production)
                
                # 计算每个物料的分配比例
                total_safety_stock = sum(df.at[idx, '安全库存'] for idx in df.index if df.at[idx, f'mps {month}'] > 0)
                if total_safety_stock > 0:
                    # proportion = (safety_stock / total_safety_stock) * 5
                    proportion = (safety_stock / total_safety_stock)
                    additional_units = round_up_to_nearest_x(proportion * additional_production, min_production)
                
                if additional_units > 0:
                    df.at[index, f'mps {month}'] += additional_units
                    additional_production -= additional_units
                    remaining_hours -= additional_units * row['标准工时']

    # 重新计算并打印每个月的生产用时
    total_hours_n = sum(df.at[index, f'mps {n}'] * df.at[index, '标准工时'] for index in df.index)
    total_hours_n1 = sum(df.at[index, f'mps {get_next_month(n, 1)}'] * df.at[index, '标准工时'] for index in df.index)
    total_hours_n2 = sum(df.at[index, f'mps {get_next_month(n, 2)}'] * df.at[index, '标准工时'] for index in df.index)
    total_hours_n3 = sum(df.at[index, f'mps {get_next_month(n, 3)}'] * df.at[index, '标准工时'] for index in df.index)

    print("After adjustment:")
    print(f"Total production hours for month {n}: {total_hours_n}")
    print(f"Total production hours for month {get_next_month(n, 1)}: {total_hours_n1}")
    print(f"Total production hours for month {get_next_month(n, 2)}: {total_hours_n2}")
    print(f"Total production hours for month {get_next_month(n, 3)}: {total_hours_n3}")

    # 再次计算每个月的结余
    for index, row in df.iterrows():
        a = row['月底库存']
        b = row[f'{n}需求']
        c = row[f'{get_next_month(n, 1)}预测']
        d = row[f'{get_next_month(n, 2)}预测']
        e = row[f'{get_next_month(n, 3)}预测']
        loss = row['损耗']

        mps_n = df.at[index, f'mps {n}']
        mps_n1 = df.at[index, f'mps {get_next_month(n, 1)}']
        mps_n2 = df.at[index, f'mps {get_next_month(n, 2)}']
        mps_n3 = df.at[index, f'mps {get_next_month(n, 3)}']

        balance_n = a + mps_n - b - loss * (1 if mps_n > 0 else 0)
        balance_n1 = balance_n + mps_n1 - c - loss * (1 if mps_n1 > 0 else 0)
        balance_n2 = balance_n1 + mps_n2 - d - loss * (1 if mps_n2 > 0 else 0)
        balance_n3 = balance_n2 + mps_n3 - e - loss * (1 if mps_n3 > 0 else 0)

        # 输出结果并保存到DataFrame
        df.at[index, f'{n}结余'] = balance_n
        df.at[index, f'{get_next_month(n, 1)}结余'] = balance_n1
        df.at[index, f'{get_next_month(n, 2)}结余'] = balance_n2
        df.at[index, f'{get_next_month(n, 3)}结余'] = balance_n3

    return df, None


