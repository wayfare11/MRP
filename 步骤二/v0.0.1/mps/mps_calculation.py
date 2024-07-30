import pulp
import pandas as pd
from .demand_calculation import get_next_month

def calculate_mps(df, n):
    """计算MPS列和结余列"""
    for index, row in df.iterrows():
        a = row['月底库存']  # n-1月库存
        b = row[f'{n}需求']  # n月预测订单量
        c = row[f'{get_next_month(n, 1)}预测']  # n+1月预测订单量
        d = row[f'{get_next_month(n, 2)}预测']  # n+2月预测订单量
        e = row[f'{get_next_month(n, 3)}预测']  # n+3月预测订单量
        x = 1000  # n+3月后至少库存 (假设固定值)

        # 确保所有值都是数值类型
        a = 0 if pd.isna(a) else a
        b = 0 if pd.isna(b) else b
        c = 0 if pd.isna(c) else c
        d = 0 if pd.isna(d) else d
        e = 0 if pd.isna(e) else e

        # 创建问题实例
        prob = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

        # 创建整数变量
        P6 = pulp.LpVariable("P6", lowBound=0, cat='Integer')
        P7 = pulp.LpVariable("P7", lowBound=0, cat='Integer')
        P8 = pulp.LpVariable("P8", lowBound=0, cat='Integer')
        P9 = pulp.LpVariable("P9", lowBound=0, cat='Integer')
        M = pulp.LpVariable("M", lowBound=0)
        m = pulp.LpVariable("m", lowBound=0)

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

        prob += a + P6 >= b
        prob += a + P6 - b + P7 >= c
        prob += a + P6 - b + P7 - c + P8 >= d
        prob += a + P6 - b + P7 - c + P8 - d + P9 >= e
        prob += a + P6 - b + P7 - c + P8 - d + P9 - e >= x

        # 求解
        prob.solve()

        # 获取求解结果
        mps_n = pulp.value(P6)
        mps_n1 = pulp.value(P7)
        mps_n2 = pulp.value(P8)
        mps_n3 = pulp.value(P9)

        # 计算结余
        balance_n = a + mps_n - b
        balance_n1 = balance_n + mps_n1 - c
        balance_n2 = balance_n1 + mps_n2 - d
        balance_n3 = balance_n2 + mps_n3 - e

        # 输出结果并保存到DataFrame
        df.at[index, f'mps {n}'] = mps_n
        df.at[index, f'mps {get_next_month(n, 1)}'] = mps_n1
        df.at[index, f'mps {get_next_month(n, 2)}'] = mps_n2
        df.at[index, f'mps {get_next_month(n, 3)}'] = mps_n3

        df.at[index, f'{n}结余'] = balance_n
        df.at[index, f'{get_next_month(n, 1)}结余'] = balance_n1
        df.at[index, f'{get_next_month(n, 2)}结余'] = balance_n2
        df.at[index, f'{get_next_month(n, 3)}结余'] = balance_n3
