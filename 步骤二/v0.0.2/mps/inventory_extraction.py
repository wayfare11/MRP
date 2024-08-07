import pandas as pd

def extract_inventory_data(df_inventory, stock_code):
    try:
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
    except KeyError as e:
        # print(f"Key error: {e}")
        return 0, 0, 0, 0

def extract_in_transit_quantity(df_production_orders, stock_code):
    try:
        """提取特定物料编码的在途数量"""
        stock_code = str(stock_code)
        df_filtered = df_production_orders[df_production_orders['物料编码'] == stock_code]
        in_transit_quantity = df_filtered['未完成数量'].sum()
        return in_transit_quantity
    except KeyError as e:
        # print(f"Key error: {e}")
        return 0
