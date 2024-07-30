import pandas as pd
import re
import pulp

def read_sales_forecast(file_path):
    """读取排产流程0613.xlsx的销售预测页"""
    sheet_name = '销售预测'
    return pd.read_excel(file_path, sheet_name=sheet_name, dtype={'存货编码': str})

def read_inventory(file_path):
    """读取现存量查询.xlsx"""
    return pd.read_excel(file_path, dtype={'存货编码': str})

def read_production_orders(file_path):
    """读取生产订单列表0630.xlsx"""
    return pd.read_excel(file_path, dtype={'物料编码': str})

def read_forecast(file_path):
    """读取2024年7-10月消融针&消融仪&消融线附件预测6.28.xlsx"""
    return pd.read_excel(file_path, dtype={'存货编码': str})

def extract_inventory_data(df_inventory, stock_code):
    """提取特定存货编码的现存量数据"""
    stock_code = str(stock_code)
    df_filtered = df_inventory[df_inventory['存货编码'] == stock_code]

    if df_filtered.empty:
        return 0.0, 0.0, 0.0, 0.0

    finished_goods_stock = df_filtered[df_filtered['仓库名称'].isin(['成品库', '附件库'])]['现存数量'].sum()
    parsing_stock = df_filtered[df_filtered['仓库名称'].isin(['半成品2(车间)', '周转库'])]['现存数量'].sum()
    research_stock = df_filtered[df_filtered['仓库名称'] == '研发成品库']['现存数量'].sum()
    return_stock = df_filtered[df_filtered['仓库名称'] == '退货库']['现存数量'].sum()

    return finished_goods_stock, parsing_stock, research_stock, return_stock

def extract_in_transit_quantity(df_production_orders, stock_code):
    """提取特定物料编码的在途数量"""
    stock_code = str(stock_code)
    df_filtered = df_production_orders[df_production_orders['物料编码'] == stock_code]
    in_transit_quantity = df_filtered['未完成数量'].sum()
    return in_transit_quantity

def calculate_monthly_demand(df):
    """计算每个月的需求（订单 + 预测），并返回月份列表"""
    pattern = re.compile(r'(\d{4}年\d{1,2}月)(订单|预测)')
    columns = df.columns

    # 查找所有符合模式的列
    orders_forecasts = {}
    for col in columns:
        match = pattern.match(col)
        if match:
            year_month, type_ = match.groups()
            if year_month not in orders_forecasts:
                orders_forecasts[year_month] = {'订单': None, '预测': None}
            orders_forecasts[year_month][type_] = col

    # 计算需求
    for year_month, cols in orders_forecasts.items():
        if cols['订单'] and cols['预测']:
            order_col = cols['订单']
            forecast_col = cols['预测']
            demand_col = f'{year_month}需求'

            df[order_col] = df[order_col].fillna(0)
            df[forecast_col] = df[forecast_col].fillna(0)
            df[demand_col] = df[order_col] + df[forecast_col]

    # 返回月份列表
    return list(orders_forecasts.keys())

def get_next_month(year_month, n):
    """获取指定月数后的月份字符串表示"""
    date = pd.to_datetime(year_month, format='%Y年%m月')
    next_month = date + pd.DateOffset(months=n)
    return f"{next_month.year}年{next_month.month}月"

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

def main():
    # 文件路径
    sales_forecast_file = '排产流程0613.xlsx'
    inventory_file = '现存量查询.xlsx'
    production_orders_file = '生产订单列表0630.xlsx'
    forecast_file = '2024年7-10月消融针&消融仪&消融线附件预测6.28.xlsx'
    output_file = '预排计划.xlsx'

    # 读取数据
    df_sales_forecast = read_sales_forecast(sales_forecast_file)
    df_inventory = read_inventory(inventory_file)
    df_production_orders = read_production_orders(production_orders_file)
    df_forecast = read_forecast(forecast_file)

    # 确保存货编码为字符串类型
    df_sales_forecast['存货编码'] = df_sales_forecast['存货编码'].astype(str)
    df_inventory['存货编码'] = df_inventory['存货编码'].astype(str)
    df_production_orders['物料编码'] = df_production_orders['物料编码'].astype(str)

    # 将所有空值替换为0
    df_sales_forecast.fillna(0, inplace=True)
    df_inventory.fillna(0, inplace=True)
    df_production_orders.fillna(0, inplace=True)
    df_forecast.fillna(0, inplace=True)

    # 初始化新的列
    df_sales_forecast['成品库存(现存量查询)'] = 0
    df_sales_forecast['解析库存(现存量查询)'] = 0
    df_sales_forecast['研发库存(现存量查询)'] = 0
    df_sales_forecast['退货待返工'] = 0
    df_sales_forecast['在途(生产订单列表)'] = 0
    df_sales_forecast['月底库存'] = 0

    # 根据存货编码匹配并提取库存数据和在途数量
    for index, row in df_sales_forecast.iterrows():
        stock_code = row['存货编码']
        finished_goods_stock, parsing_stock, research_stock, return_stock = extract_inventory_data(df_inventory, stock_code)
        in_transit_quantity = extract_in_transit_quantity(df_production_orders, stock_code)
        
        df_sales_forecast.at[index, '成品库存(现存量查询)'] = finished_goods_stock
        df_sales_forecast.at[index, '解析库存(现存量查询)'] = parsing_stock
        df_sales_forecast.at[index, '研发库存(现存量查询)'] = research_stock
        df_sales_forecast.at[index, '退货待返工(现存量查询)'] = return_stock
        df_sales_forecast.at[index, '在途(生产订单列表)'] = in_transit_quantity

        # 获取未发货订单，如果为空则处理为0
        unshipped_orders = row['未发货订单'] if pd.notna(row['未发货订单']) else 0

        # 计算月底库存
        end_of_month_stock = finished_goods_stock + parsing_stock + in_transit_quantity + return_stock - unshipped_orders
        df_sales_forecast.at[index, '月底库存'] = end_of_month_stock

    # 计算每个月的需求，并返回月份列表
    months = calculate_monthly_demand(df_sales_forecast)

    # 假设我们要计算第一个月份的 MPS
    if months:
        n = months[0]

        # 计算MPS列和结余列
        calculate_mps(df_sales_forecast, n)

    # 创建一个新的Excel writer对象
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # 将销售预测数据和现存量数据写入新的Excel文件的预排计划工作表中
        df_sales_forecast.to_excel(writer, sheet_name='预排计划', index=False)

        # 将其他表格数据写入同一个Excel文件中
        df_inventory.to_excel(writer, sheet_name='现存量查询', index=False)
        df_production_orders.to_excel(writer, sheet_name='生产订单列表', index=False)
        df_forecast.to_excel(writer, sheet_name='附件预测', index=False)

    print(f'数据已成功写入 {output_file} 文件中')

if __name__ == "__main__":
    main()