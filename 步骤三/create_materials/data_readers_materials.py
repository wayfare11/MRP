import pandas as pd

def read_production_planning(file_path):
    """读取排产计划.xlsx"""
    return pd.read_excel(file_path, dtype={'存货编码': str})


def read_material_analysis(file_path):
    """读取生产用料分析.xlsx"""
    return pd.read_excel(file_path, dtype={'物料编码': str, '子件物料编码': str})

def read_in_transit_materials(file_path):
    """读取在途物料.xlsx"""
    return pd.read_excel(file_path, dtype={'子件编码': str})

def read_stock_inquiry(file_path):
    """读取现存量查询.xlsx"""
    return pd.read_excel(file_path, dtype={'存货编码': str})

def read_production_order_list(file_path):
    """读取生产订单清单.xlsx"""
    return pd.read_excel(file_path, dtype={'物料编码': str})

def read_purchase_order_execution_statistics(file_path):
    """读取采购订单执行统计.xlsx"""
    return pd.read_excel(file_path, dtype={'存货编码': str})

def read_outsourcing_order_execution_statistics(file_path):
    """读取委外订单执行统计.xlsx"""
    return pd.read_excel(file_path, dtype={'存货编码': str})

def read_material_purchase_information(file_path):
    """读取物料采购信息.xlsx"""
    return pd.read_excel(file_path, dtype={'存货编码': str})

def read_semi_finished_product_comparison(file_path):
    """读取半成品对比.xlsx"""
    return pd.read_excel(file_path, dtype={'物料编码': str, '子件物料编码': str})