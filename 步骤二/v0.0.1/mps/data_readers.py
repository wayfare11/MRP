import pandas as pd

def read_sales_forecast(file_path):
    """读取排产流程0613.xlsx的销售预测页"""
    sheet_name = '消融针&消融线&仪器'
    return pd.read_excel(file_path, sheet_name=sheet_name, dtype={'存货编码': str})

def read_inventory(file_path):
    """读取现存量查询.xlsx"""
    return pd.read_excel(file_path, dtype={'存货编码': str})

def read_production_orders(file_path):
    """读取生产订单列表0630.xlsx"""
    return pd.read_excel(file_path, dtype={'物料编码': str})
