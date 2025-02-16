import pandas as pd
import matplotlib.pyplot as plt

# 读取生成的CSV文件
input_file = 'used_bfs_statistics.csv'
df = pd.read_csv(input_file)

# 提取最后两列并计算总和
used_bfs_true_total = df['used_bfs_true'].sum()
used_bfs_false_total = df['used_bfs_false'].sum()

# 打印总和
print(f"used_bfs_true (BFS) Total: {used_bfs_true_total}")
print(f"used_bfs_false (Greedy) Total: {used_bfs_false_total}")

# 数据准备
labels = ['BFS_HGBR', 'Greedy_HGBR']
sizes = [used_bfs_true_total, used_bfs_false_total]
colors = ['#4C72B0', '#55A868']  # 更学术化的颜色
explode = (0.1, 0)  # 突出显示BFS部分

# 绘制饼图
plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, shadow=True, textprops={'fontsize': 14})

# 设置标题
plt.title('Proportion of BFS vs Greedy', fontsize=16, pad=20)

# 显示比例和数量
plt.legend([f'BFS_HGBR: {used_bfs_true_total}', f'Greedy_HGBR: {used_bfs_false_total}'], loc='best', fontsize=12)

# 保证饼图是圆形
plt.axis('equal')

# 保存为PDF
output_pdf = 'bfs_vs_greedy_proportion.pdf'
plt.savefig(output_pdf, format='pdf', bbox_inches='tight')

# 显示饼图
plt.show()

print(f"饼图已保存为 {output_pdf}")