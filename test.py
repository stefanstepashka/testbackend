import numpy as np
import pandas as pd
import json

with open("trial_task.json", "r", encoding='utf-8') as read_file:
    data = json.load(read_file)

products = pd.json_normalize(data, record_path='products', meta=['order_id', 'warehouse_name', 'highway_cost'])

products['total_quantity'] = products.groupby('order_id')['quantity'].transform('sum')
products['tariff'] = abs(products['highway_cost'] / products['total_quantity'])

# Группировка по складам и расчет среднего тарифа
tariff_per_warehouse = products.groupby('warehouse_name')['tariff'].mean().reset_index()
print(tariff_per_warehouse)


#Расчет доходов, расходов и прибыли
products['income'] = products['price'] * products['quantity']
products['expenses'] = products['tariff'] * products['quantity']
products['profit'] = products['income'] - products['expenses']


# ....................................2 ЗАДАНИЕ........................................
# Группировка по продуктам и расчет суммарного количества, дохода, и т.д.
summary = products.groupby('product').agg({
    'quantity': 'sum',
    'income': 'sum',
    'expenses': 'sum',
    'profit': 'sum'
}).reset_index()


print(summary)




# ....................................3 ЗАДАНИЕ........................................
#Составить табличку со столбцами 'order_id' (id заказа)
# и 'order_profit' (прибыль полученная с заказа). А также вывести среднюю прибыль заказов.

order_summary = products.groupby('order_id').agg({
    'income': 'sum',
    'expenses': 'sum',
    'profit': 'sum'
}).reset_index()

order_summary.rename(columns={'profit': 'order_profit'}, inplace=True)

print(order_summary[['order_id', 'order_profit']])

#  средняя прибыль
mean_profit = order_summary['order_profit'].mean()

print("Средняя прибыль заказов: ", mean_profit)


# ....................................4.  ЗАДАНИЕ.................................
grouped = products.groupby(['warehouse_name', 'product']).agg({'quantity': 'sum', 'profit': 'sum'}).reset_index()

# Вычисление общей прибыли для каждого склада
total_profit_per_warehouse = products.groupby('warehouse_name')['profit'].sum()

# Вычисление процентной прибыли продукта от прибыли этого склада
grouped['percent_profit_product_of_warehouse'] = grouped.apply(
    lambda row: (row['profit'] / total_profit_per_warehouse[row['warehouse_name']]) * 100, axis=1)

# ......................................5 задание.................................
# Сортировка 'percent_profit_product_of_warehouse' по убыванию и подсчет накопленного процента
grouped = grouped.sort_values(by='percent_profit_product_of_warehouse', ascending=False)
grouped['accumulated_percent_profit_product_of_warehouse'] = grouped['percent_profit_product_of_warehouse'].cumsum()

# .....................................6 Задание......................................
# Присвоение категорий A, B, C на основании значения накопленного процента
bins = [0, 70, 90, np.inf]
labels = ['A', 'B', 'C']

grouped['category'] = pd.cut(grouped['accumulated_percent_profit_product_of_warehouse'], bins=bins, labels=labels)


# pd.set_option('display.max_rows', None)
# pd.set_option('display.max_columns', None)

print(grouped)

