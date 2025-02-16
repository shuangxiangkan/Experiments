import os
import pandas as pd

# 获取当前执行路径的上一层目录
current_dir = os.path.dirname(os.path.abspath(__file__))  # 当前脚本的目录
parent_dir = os.path.dirname(current_dir)  # 上一层目录

# 定义evaluation文件夹路径
evaluation_folder = os.path.join(parent_dir, 'evaluation')
# source and sink from different components
output_file = 'average_false_results.csv'

# 定义列的顺序
column_order = [
    'n', 'k', 'r', 'source_sink_from_different_branches',
    'uf_build_time', 'uf_connected', 'uf_connected_time',
    'dfs_connected', 'dfs_path_length', 'dfs_time',
    'bfs_connected', 'bfs_path_length', 'bfs_time',
    'fffp_connected', 'fffp_path_length', 'fffp_time'
]

# 初始化一个空的DataFrame来存储结果
results = pd.DataFrame(columns=column_order)

# 遍历evaluation文件夹下的所有文件
for filename in os.listdir(evaluation_folder):
    if filename.endswith('False.csv'):
        file_path = os.path.join(evaluation_folder, filename)

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 提取固定列
        fixed_columns = df[['n', 'k', 'r', 'source_sink_from_different_branches', 'uf_connected', 'dfs_connected', 'bfs_connected', 'fffp_connected']].iloc[0]

        # 计算需要平均的列的平均值，保留6位小数
        avg_columns = df[['uf_build_time', 'uf_connected_time', 'dfs_path_length', 'dfs_time', 'bfs_path_length', 'bfs_time', 'fffp_path_length', 'fffp_time']].mean().round(6)

        # 将固定列和平均值列合并为一个新的Series
        new_row = pd.concat([fixed_columns, avg_columns])

        # 将新行转换为DataFrame并调整列顺序
        new_row_df = pd.DataFrame([new_row], columns=column_order)

        # 将新行添加到结果DataFrame中
        results = pd.concat([results, new_row_df], ignore_index=True)

# 将结果保存到新的CSV文件中
results.to_csv(output_file, index=False)

print(f"处理完成，结果已保存到 {output_file}")