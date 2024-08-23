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

def calculate_mps(df, n, total_hours):
    """计算MPS列和结余列"""
    unoptimized_stock_codes = []  # 存储没有找到合适解的存货编码
    total_hours_n = 0
    total_hours_n1 = 0
    total_hours_n2 = 0
    total_hours_n3 = 0

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

        # 创建问题实例
        prob = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

        # 创建整数变量
        P6 = pulp.LpVariable("P6", lowBound=0, cat='Integer')
        P7 = pulp.LpVariable("P7", lowBound=0, cat='Integer')
        P8 = pulp.LpVariable("P8", lowBound=0, cat='Integer')
        P9 = pulp.LpVariable("P9", lowBound=0, cat='Integer')
        M = pulp.LpVariable("M", lowBound=0)
        m = pulp.LpVariable("m", lowBound=0)

        # 创建二进制变量表示是否有生产
        Y6 = pulp.LpVariable("Y6", cat='Binary')
        Y7 = pulp.LpVariable("Y7", cat='Binary')
        Y8 = pulp.LpVariable("Y8", cat='Binary')
        Y9 = pulp.LpVariable("Y9", cat='Binary')

        # 目标函数
        prob += M - m

        # 约束条件
        prob += P6 <= M
        prob += P7 <= M
        prob += P8 <= M
        prob += P9 <= M
        prob += P6 >= m
        prob += P7 >= m
        prob += P8 >= m
        prob += P9 >= m

        # 确保 P 变量和 Y 变量的关系
        prob += P6 >= 1 * Y6
        prob += P7 >= 1 * Y7
        prob += P8 >= 1 * Y8
        prob += P9 >= 1 * Y9

        # 确保当 P 变量大于 0 时，Y 变量必须为 1
        big_number = 10**9
        prob += P6 <= big_number * Y6
        prob += P7 <= big_number * Y7
        prob += P8 <= big_number * Y8
        prob += P9 <= big_number * Y9

        # 在设置约束条件时，若对应月份有生产，则将需求量加上损耗
        prob += a + P6 >= b + loss * Y6
        prob += a + P6 - (b + loss * Y6) + P7 >= c + loss * Y7
        prob += a + P6 - (b + loss * Y6) + P7 - (c + loss * Y7) + P8 >= d + loss * Y8
        prob += a + P6 - (b + loss * Y6) + P7 - (c + loss * Y7) + P8 - (d + loss * Y8) + P9 >= e + loss * Y9

        # 确保季度末结余不低于安全库存
        if is_quarter_end(n):
            prob += a + P6 - (b + loss * Y6) >= safety_stock
        if is_quarter_end(get_next_month(n, 1)):
            prob += a + P6 - (b + loss * Y6) + P7 - (c + loss * Y7) >= safety_stock
        if is_quarter_end(get_next_month(n, 2)):
            prob += a + P6 - (b + loss * Y6) + P7 - (c + loss * Y7) + P8 - (d + loss * Y8) >= safety_stock
        if is_quarter_end(get_next_month(n, 3)):
            prob += a + P6 - (b + loss * Y6) + P7 - (c + loss * Y7) + P8 - (d + loss * Y8) + P9 - (e + loss * Y9) >= safety_stock

        # 确保每个月的结余不超过安全库存太多（如果安全库存大于0）
        if safety_stock > 0:
            max_excess_stock = safety_stock * 1.5  # 允许超出安全库存的最大值
            prob += a + P6 - (b + loss * Y6) <= max_excess_stock
            prob += a + P6 - (b + loss * Y6) + P7 - (c + loss * Y7) <= max_excess_stock
            prob += a + P6 - (b + loss * Y6) + P7 - (c + loss * Y7) + P8 - (d + loss * Y8) <= max_excess_stock
            prob += a + P6 - (b + loss * Y6) + P7 - (c + loss * Y7) + P8 - (d + loss * Y8) + P9 - (e + loss * Y9) <= max_excess_stock

        # 确保每个月的结余大于等于0
        prob += a + P6 - (b + loss * Y6) >= 0
        prob += a + P6 - (b + loss * Y6) + P7 - (c + loss * Y7) >= 0
        prob += a + P6 - (b + loss * Y6) + P7 - (c + loss * Y7) + P8 - (d + loss * Y8) >= 0
        prob += a + P6 - (b + loss * Y6) + P7 - (c + loss * Y7) + P8 - (d + loss * Y8) + P9 - (e + loss * Y9) >= 0

        # 使用 CBC 求解器并关闭输出
        solver = pulp.PULP_CBC_CMD(msg=False, options=['-log', '0', '-printingOptions', 'none'])
        prob.solve(solver)

        # 检查求解状态
        if pulp.LpStatus[prob.status] != 'Optimal':
            print(f"Solver did not find an optimal solution for stock code {stock_code}: {pulp.LpStatus[prob.status]}")
            unoptimized_stock_codes.append(stock_code)
        else:
            print("Solver found an optimal solution.")

        # 获取求解结果并调整到最小排产量的倍数
        mps_n = round_up_to_nearest_x(pulp.value(P6) if pulp.value(P6) is not None else 0, min_production)
        mps_n1 = round_up_to_nearest_x(pulp.value(P7) if pulp.value(P7) is not None else 0, min_production)
        mps_n2 = round_up_to_nearest_x(pulp.value(P8) if pulp.value(P8) is not None else 0, min_production)
        mps_n3 = round_up_to_nearest_x(pulp.value(P9) if pulp.value(P9) is not None else 0, min_production)

        # 计算结余
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

        # 计算每个月的总工时
        total_hours_n += mps_n * standard_hours
        total_hours_n1 += mps_n1 * standard_hours
        total_hours_n2 += mps_n2 * standard_hours
        total_hours_n3 += mps_n3 * standard_hours
    
    # 打印没有找到合适解的存货编码
    if unoptimized_stock_codes:
        print("Stock codes without optimal solutions:", ", ".join(unoptimized_stock_codes))
    
    # 打印每个月的总工时和total_hours的比较结果
    print(f"Total hours for {n}: {total_hours_n} (Limit: {total_hours[0]})")
    print(f"Total hours for {get_next_month(n, 1)}: {total_hours_n1} (Limit: {total_hours[1]})")
    print(f"Total hours for {get_next_month(n, 2)}: {total_hours_n2} (Limit: {total_hours[2]})")
    print(f"Total hours for {get_next_month(n, 3)}: {total_hours_n3} (Limit: {total_hours[3]})")

    return df
