import os
import pandas as pd

# 获取当前执行路径的上一层目录
current_dir = os.path.dirname(os.path.abspath(__file__))  # 当前脚本的目录
parent_dir = os.path.dirname(current_dir)  # 上一层目录

# 定义evaluation文件夹路径
evaluation_folder = os.path.join(parent_dir, 'evaluation')

# 采样数据量列表
sample_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# 定义列的顺序
column_order = [
    'sample_size', 'n', 'k', 'r', 'source_sink_from_different_branches',
    'uf_build_time', 'uf_connected', 'uf_connected_time',
    'dfs_connected', 'dfs_path_length', 'dfs_time',
    'bfs_connected', 'bfs_path_length', 'bfs_time',
    'fffp_connected', 'fffp_path_length', 'fffp_time'
]

# 遍历 evaluation 文件夹下的所有文件
for filename in os.listdir(evaluation_folder):
    if filename.endswith('False.csv'):
        file_path = os.path.join(evaluation_folder, filename)

        # 读取 CSV 文件
        df = pd.read_csv(file_path)

        # 提取固定列（第一行的基本信息）
        fixed_columns = df[['n', 'k', 'r', 'source_sink_from_different_branches',
                            'uf_connected', 'dfs_connected', 'bfs_connected', 'fffp_connected']].iloc[0]

        # 初始化存储不同 sample_size 计算结果的 DataFrame
        results = pd.DataFrame(columns=column_order)

        # 计算不同 sample_size 的均值
        for size in sample_sizes:
            sampled_df = df.iloc[:size]  # 选取前 size 个数据

            # 计算均值（保留 6 位小数）
            avg_columns = sampled_df[['uf_build_time', 'uf_connected_time', 'dfs_path_length',
                                      'dfs_time', 'bfs_path_length', 'bfs_time', 'fffp_path_length', 'fffp_time']].mean().round(6)

            # 组合新行
            new_row = pd.concat([pd.Series({'sample_size': size}), fixed_columns, avg_columns])

            # 添加到结果 DataFrame
            results = pd.concat([results, pd.DataFrame([new_row], columns=column_order)], ignore_index=True)

        # 生成新的文件名
        new_filename = filename.replace('.csv', '-average.csv')
        output_path = os.path.join(evaluation_folder, new_filename)

        # 保存结果到新的 CSV 文件
        results.to_csv(output_path, index=False)

        print(f"处理完成，结果已保存到 {new_filename}")
