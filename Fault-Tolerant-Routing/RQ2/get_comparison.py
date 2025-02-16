import os
import pandas as pd
import matplotlib.pyplot as plt

# 目标文件夹
uf_folder = "uf"
comparison_folder = os.path.join(uf_folder, "comparison")
os.makedirs(comparison_folder, exist_ok=True)

# 需要提取的 sample_size
selected_sizes = [10, 20, 50, 70, 100]

# 遍历 uf 文件夹下的所有 csv 文件
for filename in os.listdir(uf_folder):
    if filename.endswith("False-average.csv"):  # 确保匹配目标文件名格式
        file_path = os.path.join(uf_folder, filename)
        df = pd.read_csv(file_path)

        # 只提取指定的 sample_size 数据
        df_filtered = df[df['sample_size'].isin(selected_sizes)]

        # 计算搜索时间
        df_filtered["dfs_search_time"] = df_filtered["sample_size"] * df_filtered["dfs_time"]
        df_filtered["bfs_search_time"] = df_filtered["sample_size"] * df_filtered["bfs_time"]
        df_filtered["fffp_search_time"] = df_filtered["sample_size"] * (
                    df_filtered["fffp_time"] + df_filtered["uf_connected_time"]) + df_filtered["uf_build_time"]

        # 提取 n, k, r 值用于标题
        n_value = df_filtered["n"].iloc[0]
        k_value = df_filtered["k"].iloc[0]
        r_value = df_filtered["r"].iloc[0]

        # 提取数据
        x_labels = df_filtered["sample_size"].tolist()
        dfs_search_time = df_filtered["dfs_search_time"].tolist()
        bfs_search_time = df_filtered["bfs_search_time"].tolist()
        fffp_search_time = df_filtered["fffp_search_time"].tolist()

        # 画图
        fig, ax = plt.subplots(figsize=(8, 5))
        width = 0.2  # 增大柱状宽度
        x_indexes = range(len(x_labels))

        ax.bar([x - width for x in x_indexes], dfs_search_time, width=width, label="DFS Search Time")
        ax.bar(x_indexes, bfs_search_time, width=width, label="BFS Search Time")
        ax.bar([x + width for x in x_indexes], fffp_search_time, width=width, label="FFFP Search Time")

        ax.set_xticks(x_indexes)
        ax.set_xticklabels(x_labels)
        ax.set_xlabel("Sample Size")
        ax.set_ylabel("Time (s)")
        ax.set_title(f"Search Time Comparison (n={n_value}, k={k_value}, r={r_value})")
        ax.legend()

        # 生成 PDF 文件名
        pdf_filename = filename.split("_source")[0] + ".pdf"
        pdf_path = os.path.join(comparison_folder, pdf_filename)

        # 保存并显示
        plt.savefig(pdf_path, format="pdf")
        plt.show()

        print(f"图表已保存: {pdf_path}")
