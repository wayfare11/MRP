import re
import pandas as pd

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

    # 返回实际存在需求的月份列表
    return [year_month for year_month, cols in orders_forecasts.items() if cols['订单'] and cols['预测']]

def get_next_month(year_month, n):
    """获取指定月数后的月份字符串表示"""
    date = pd.to_datetime(year_month, format='%Y年%m月')
    next_month = date + pd.DateOffset(months=n)
    return f"{next_month.year}年{next_month.month}月"
