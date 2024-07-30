import pulp

# 参数
a = 3700  # 5月库存
b = 6100  # 6月预测订单量
c = 1112  # 7月预测订单量
d = 1022  # 8月预测订单量
e = 6000  # 9月预测订单量
x = 2466   # 9月后至少库存

# 创建问题实例
prob = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

# 创建变量
P6 = pulp.LpVariable("P6", lowBound=0)
P7 = pulp.LpVariable("P7", lowBound=0)
P8 = pulp.LpVariable("P8", lowBound=0)
P9 = pulp.LpVariable("P9", lowBound=0)
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

# 输出结果
print(f"P6: {pulp.value(P6)}")
print(f"P7: {pulp.value(P7)}")
print(f"P8: {pulp.value(P8)}")
print(f"P9: {pulp.value(P9)}")