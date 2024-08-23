import re

def extract_year_and_month(column_name):
    # 使用正则表达式匹配 "YYYY年MM月" 格式
    match = re.search(r'(\d{4})年(\d{1,2})月', column_name)
    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        return year, month
    else:
        return None, None

def add_months(year, month, months):
    month += months
    while month > 12:
        year += 1
        month -= 12
    return year, month