import os
import pandas as pd

# 获取当前执行路径的上一层目录
current_dir = os.path.dirname(os.path.abspath(__file__))  # 当前脚本的目录
parent_dir = os.path.dirname(current_dir)  # 上一层目录

# 定义evaluation文件夹路径
evaluation_folder = os.path.join(parent_dir, 'evaluation')
output_file = 'used_bfs_statistics.csv'

# 初始化一个空的DataFrame来存储结果
results = pd.DataFrame(
    columns=['n', 'k', 'r', 'source_sink_from_different_branches', 'used_bfs_true', 'used_bfs_false'])

# 遍历evaluation文件夹下的所有文件
for filename in os.listdir(evaluation_folder):
    if filename.endswith('False.csv'):
        file_path = os.path.join(evaluation_folder, filename)

        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 统计used_bfs列中True和False的数量
        used_bfs_true = df['used_bfs'].sum()  # True的数量
        used_bfs_false = len(df) - used_bfs_true  # False的数量

        # 提取所需的列
        extracted_data = df[['n', 'k', 'r', 'source_sink_from_different_branches']].iloc[0]

        # 创建一个新的Series来存储统计结果
        stats = pd.Series({'used_bfs_true': used_bfs_true, 'used_bfs_false': used_bfs_false})

        # 将提取的列和统计结果合并为一个新的行
        new_row = pd.concat([extracted_data, stats])

        # 将新行添加到结果DataFrame中
        results = pd.concat([results, new_row.to_frame().T], ignore_index=True)

# 将结果保存到新的CSV文件中
results.to_csv(output_file, index=False)

print(f"处理完成，结果已保存到 {output_file}")