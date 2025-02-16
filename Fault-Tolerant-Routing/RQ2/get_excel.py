import pandas as pd
import numpy as np

# 定义输入和输出文件路径
input_csv = 'average_true_results.csv'
output_excel = 'average_true_results.xlsx'

# 读取CSV文件
df = pd.read_csv(input_csv)

# 删除不需要的列
columns_to_drop = [
    'source_sink_from_different_branches',
    'uf_connected',
    'dfs_connected',
    'bfs_connected',
    'fffp_connected',
    'dfs_path_length',
    'bfs_path_length',
    'fffp_path_length'
]
df = df.drop(columns=columns_to_drop)

# 添加序号列
df.insert(0, 'No.', range(1, len(df) + 1))

# 统一格式，确保所有数值都是科学计数法
def to_scientific_notation(x):
    return f"{float(x):.3e}"  # 保留3位小数，确保所有数值格式统一

# 需要格式化的列
time_columns = ['uf_build_time', 'uf_connected_time', 'dfs_time', 'bfs_time', 'fffp_time']

# 统一数值格式
for col in time_columns:
    df[col] = df[col].apply(to_scientific_notation)

# 计算平均值
df_calc = df.copy()
for col in time_columns:
    df_calc[col] = pd.to_numeric(df_calc[col], errors='coerce')

means = df_calc.mean(numeric_only=True)
means['No.'] = 'Average'

# 统一平均值格式
for col in time_columns:
    means[col] = to_scientific_notation(means[col])

# 添加平均值行
df_with_means = pd.concat([df, pd.DataFrame([means])], ignore_index=True)

# 将结果保存为Excel文件
df_with_means.to_excel(output_excel, index=False, engine='openpyxl')

print(f"处理完成，结果已保存到 {output_excel}")
