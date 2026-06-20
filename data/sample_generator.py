import numpy as np
import pandas as pd


def generate_sales_data(periods=120):
    """生成示例销售数据"""
    dates = pd.date_range(start="2024-01-01", periods=periods, freq="D")
    regions = ["华北", "华东", "华南", "西南", "西北"]
    products = ["电子产品", "服装", "食品", "家居", "运动"]

    data = []
    for date in dates:
        for region in regions:
            for product in products:
                sales = np.random.randint(100, 5000)
                profit = sales * np.random.uniform(0.1, 0.3)
                cost = sales * np.random.uniform(0.5, 0.8)
                data.append([date, region, product, sales, profit, cost])

    df = pd.DataFrame(data, columns=["日期", "地区", "产品类别", "销售额", "利润", "成本"])
    return df


def generate_student_data(periods=50):
    """生成示例学生成绩数据"""
    names = [f"学生{i}" for i in range(1, periods + 1)]
    classes = ["一班", "二班", "三班"]
    subjects = ["语文", "数学", "英语", "科学"]

    data = []
    for name in names:
        cls = np.random.choice(classes)
        for subject in subjects:
            score = np.random.randint(40, 100)
            data.append({"姓名": name, "班级": cls, "科目": subject, "成绩": score})

    df = pd.DataFrame(data)
    return df


def generate_inventory_data(periods=80):
    """生成示例库存数据"""
    products = ["笔记本电脑", "手机", "平板", "耳机", "键盘", "鼠标"]
    warehouses = ["北京仓", "上海仓", "广州仓", "成都仓"]
    suppliers = ["供应商A", "供应商B", "供应商C"]

    dates = pd.date_range(start="2024-01-01", periods=periods, freq="D")
    data = []
    for date in dates:
        for _ in range(np.random.randint(3, 8)):
            product = np.random.choice(products)
            warehouse = np.random.choice(warehouses)
            supplier = np.random.choice(suppliers)
            qty = np.random.randint(10, 500)
            unit_price = np.random.uniform(50, 8000)
            total_value = qty * unit_price
            data.append([
                date, product, warehouse, supplier,
                qty, round(unit_price, 2), round(total_value, 2)
            ])

    df = pd.DataFrame(data, columns=[
        "日期", "产品名称", "仓库", "供应商",
        "库存数量", "单价", "库存价值"
    ])
    return df


SAMPLE_DATASETS = {
    "销售数据": {
        "generator": generate_sales_data,
        "description": "包含地区、产品类别的销售、利润、成本数据",
        "columns": ["日期", "地区", "产品类别", "销售额", "利润", "成本"]
    },
    "学生成绩": {
        "generator": generate_student_data,
        "description": "包含班级、科目维度的学生成绩数据",
        "columns": ["姓名", "班级", "科目", "成绩"]
    },
    "库存管理": {
        "generator": generate_inventory_data,
        "description": "包含仓库、供应商维度的库存数据",
        "columns": ["日期", "产品名称", "仓库", "供应商", "库存数量", "单价", "库存价值"]
    }
}