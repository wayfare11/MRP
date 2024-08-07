import pulp

def is_quarter_end(month):
    """判断给定月份是否为季度末"""
    # 提取月份部分并转换为整数
    month_int = int(month.split('年')[1].replace('月', ''))
    return month_int in [3, 6, 9, 12]

def calculate_mps_for_item(a, b, c, d, e, safety_stock, n, get_next_month):
    """计算单个物品的MPS和结余"""
    
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

    # 确保季度末结余不低于安全库存
    if is_quarter_end(n):
        prob += a + P6 - b >= safety_stock
    if is_quarter_end(get_next_month(n, 1)):
        prob += a + P6 - b + P7 - c >= safety_stock
    if is_quarter_end(get_next_month(n, 2)):
        prob += a + P6 - b + P7 - c + P8 - d >= safety_stock
    if is_quarter_end(get_next_month(n, 3)):
        prob += a + P6 - b + P7 - c + P8 - d + P9 - e >= safety_stock

    # 确保每个月的结余不超过安全库存太多
    max_excess_stock = safety_stock * 1.5  # 允许超出安全库存的最大值
    prob += a + P6 - b <= max_excess_stock
    prob += a + P6 - b + P7 - c <= max_excess_stock
    prob += a + P6 - b + P7 - c + P8 - d <= max_excess_stock
    prob += a + P6 - b + P7 - c + P8 - d + P9 - e <= max_excess_stock

    # 求解
    prob.solve()

    # 获取求解结果
    mps_n = pulp.value(P6) if pulp.value(P6) is not None else 0
    mps_n1 = pulp.value(P7) if pulp.value(P7) is not None else 0
    mps_n2 = pulp.value(P8) if pulp.value(P8) is not None else 0
    mps_n3 = pulp.value(P9) if pulp.value(P9) is not None else 0

    # 计算结余
    balance_n = a + mps_n - b
    balance_n1 = balance_n + mps_n1 - c
    balance_n2 = balance_n1 + mps_n2 - d
    balance_n3 = balance_n2 + mps_n3 - e

    return mps_n, mps_n1, mps_n2, mps_n3, balance_n, balance_n1, balance_n2, balance_n3

# 测试函数
def test_calculate_mps():
    def get_next_month_stub(n, offset):
        months = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
        current_year = n.split('年')[0]
        current_month = n.split('年')[1]
        current_index = months.index(current_month)
        next_month = months[(current_index + offset) % 12]
        next_year = int(current_year) + ((current_index + offset) // 12)
        return f"{next_year}年{next_month}"

    a = 100  # n-1月库存
    b = 150  # n月预测订单量
    c = 200  # n+1月预测订单量
    d = 250  # n+2月预测订单量
    e = 300  # n+3月预测订单量
    safety_stock = 50  # 安全库存
    n = "2023年6月"  # 当前月份

    results = calculate_mps_for_item(a, b, c, d, e, safety_stock, n, get_next_month_stub)
    
    # 打印每个月的生产量和结余
    months = [n, get_next_month_stub(n, 1), get_next_month_stub(n, 2), get_next_month_stub(n, 3)]
    production_quantities = results[:4]
    balances = results[4:]
    
    # for month, production, balance in zip(months, production_quantities, balances):
    #     print(f"{month}: 生产量 = {production}, 结余 = {balance}")

# 运行测试
test_calculate_mps()
