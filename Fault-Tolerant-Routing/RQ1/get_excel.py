import pandas as pd
import numpy as np

# 定义输入和输出文件路径
input_csv = 'average_false_results.csv'
output_excel = 'average_false_results.xlsx'

# 读取CSV文件
df = pd.read_csv(input_csv)

# 删除不需要的列
columns_to_drop = [
    'source_sink_from_different_branches',
    'uf_connected',
    'dfs_connected',
    'bfs_connected',
    'fffp_connected'
]
df = df.drop(columns=columns_to_drop)

# 添加序号列
df.insert(0, '序号', range(1, len(df) + 1))

# 格式化小数位数
df['dfs_path_length'] = df['dfs_path_length'].round(2)
df['bfs_path_length'] = df['bfs_path_length'].round(2)
df['fffp_path_length'] = df['fffp_path_length'].round(2)

# 修改后的科学计数法格式化函数
def to_scientific_notation(x):
    return f"{x:.2g}"

# 应用科学计数法格式化
time_columns = ['uf_build_time', 'uf_connected_time', 'dfs_time', 'bfs_time', 'fffp_time']
for col in time_columns:
    df[col] = df[col].apply(to_scientific_notation)

# 计算平均值行
# 首先转换时间列回浮点数以便计算平均值
df_calc = df.copy()
for col in time_columns:
    df_calc[col] = pd.to_numeric(df_calc[col], errors='coerce')

# 计算平均值
means = df_calc.mean(numeric_only=True)
means['序号'] = 'Average'  # 序号列显示"Average"

# 将平均值也格式化
for col in time_columns:
    means[col] = to_scientific_notation(means[col])

# 添加平均值行
df_with_means = pd.concat([df, pd.DataFrame([means])], ignore_index=True)

# 将结果保存为Excel文件
df_with_means.to_excel(output_excel, index=False, engine='openpyxl')

print(f"处理完成，结果已保存到 {output_excel}")