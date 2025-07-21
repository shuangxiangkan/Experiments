#!/usr/bin/env python3
"""
创建RQ2合并的Excel文件，包含所有算法的性能数据
"""

import csv

def create_rq2_combined_excel():
    """
    创建包含所有算法性能数据的Excel文件
    """
    print("=== 创建RQ2合并的Excel文件 ===")
    
    # 原始表格数据 (DFS, BFS, HGBPC) - 路径长度和时间
    original_data = [
        [1, 4, 4, 2, 0, 142.64, 0.7, 3.99, 0.486, 1.386, 0.001, 4.16, 0.013],
        [2, 4, 4, 2, 1, 129.12, 0.65, 4.02, 0.469, 1.352, 0.001, 4.19, 0.011],
        [3, 4, 4, 3, 0, 147.13, 0.708, 4.09, 0.454, 1.246, 0.001, 4.37, 0.013],
        [4, 4, 4, 3, 1, 120.06, 0.573, 3.89, 0.396, 1.188, 0.001, 4.00, 0.007],
        [5, 4, 4, 4, 0, 125.07, 0.59, 4.07, 0.437, 1.176, 0.001, 4.44, 0.009],
        [6, 4, 4, 4, 1, 110.22, 0.529, 3.93, 0.368, 1.051, 0.001, 4.25, 0.015],
        [7, 5, 4, 2, 0, 588.89, 12.402, 4.76, 2.676, 8.226, 0.001, 4.85, 0.016],
        [8, 5, 4, 2, 1, 621.01, 12.988, 4.38, 2.105, 7.995, 0.001, 4.57, 0.013],
        [9, 5, 4, 3, 0, 581.18, 11.908, 4.61, 2.426, 7.878, 0.001, 4.86, 0.015],
        [10, 5, 4, 3, 1, 510.91, 9.694, 4.58, 2.255, 7.509, 0.001, 4.81, 0.013],
        [11, 5, 4, 4, 0, 578.61, 12.094, 4.57, 2.285, 7.85, 0.001, 4.89, 0.015],
        [12, 5, 4, 4, 1, 495.39, 8.793, 4.62, 2.241, 7.688, 0.001, 4.91, 0.018],
        [13, 6, 4, 2, 0, 2317.27, 279.004, 5.25, 12.693, 43.664, 0.001, 5.63, 0.023],
        [14, 6, 4, 2, 1, 2515.94, 314.675, 5.27, 12.7, 43.624, 0.001, 5.48, 0.023],
        [15, 6, 4, 3, 0, 2428.46, 301.32, 5.22, 12.697, 45.444, 0.001, 5.41, 0.022],
        [16, 6, 4, 3, 1, 2298.59, 259.599, 5.31, 12.5, 43.15, 0.001, 5.52, 0.022],
        [17, 6, 4, 4, 0, 2373.94, 296.254, 5.43, 14.333, 48.327, 0.002, 5.69, 0.026],
        [18, 6, 4, 4, 1, 2561.98, 326.241, 5.15, 11.736, 44.329, 0.001, 5.48, 0.022],
    ]
    
    # 读取A*和双向BFS数据
    astar_bidirectional_data = {}
    try:
        with open('rq2_summary.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['No'] != 'Avg':  # 跳过平均值行
                    no = int(row['No'])
                    astar_time = float(row['astar_time_ms'])
                    astar_path = float(row['astar_path_length'])
                    bidirectional_time = float(row['bidirectional_time_ms'])
                    bidirectional_path = float(row['bidirectional_path_length'])
                    astar_bidirectional_data[no] = (astar_time, astar_path, bidirectional_time, bidirectional_path)
    except FileNotFoundError:
        print("错误: 找不到 rq2_summary.csv 文件")
        return
    
    # 合并数据
    combined_data = []
    for row in original_data:
        no = row[0]
        n, k, r, h = row[1:5]
        dfs_path_length, dfs_path_time = row[5:7]
        bfs_path_length, bfs_path_time = row[7:9]
        hgbpc_uf_build_time, hgbpc_uf_query_time, hgbpc_path_length, hgbpc_path_time = row[9:13]
        
        # 获取A*和双向BFS数据
        if no in astar_bidirectional_data:
            astar_time, astar_path, bidirectional_time, bidirectional_path = astar_bidirectional_data[no]
        else:
            astar_time, astar_path, bidirectional_time, bidirectional_path = 0, 0, 0, 0
            print(f"警告: 配置 {no} 的A*和双向BFS数据缺失")
        
        combined_data.append([
            no, n, k, r, h,
            dfs_path_length, dfs_path_time,
            bfs_path_length, bfs_path_time,
            astar_path, astar_time,
            bidirectional_path, bidirectional_time,
            hgbpc_uf_build_time, hgbpc_uf_query_time, hgbpc_path_length, hgbpc_path_time
        ])
    
    # 计算平均值
    avg_dfs_path = sum(row[5] for row in combined_data) / len(combined_data)
    avg_dfs_time = sum(row[6] for row in combined_data) / len(combined_data)
    avg_bfs_path = sum(row[7] for row in combined_data) / len(combined_data)
    avg_bfs_time = sum(row[8] for row in combined_data) / len(combined_data)
    avg_astar_path = sum(row[9] for row in combined_data) / len(combined_data)
    avg_astar_time = sum(row[10] for row in combined_data) / len(combined_data)
    avg_bidirectional_path = sum(row[11] for row in combined_data) / len(combined_data)
    avg_bidirectional_time = sum(row[12] for row in combined_data) / len(combined_data)
    avg_hgbpc_uf_build = sum(row[13] for row in combined_data) / len(combined_data)
    avg_hgbpc_uf_query = sum(row[14] for row in combined_data) / len(combined_data)
    avg_hgbpc_path = sum(row[15] for row in combined_data) / len(combined_data)
    avg_hgbpc_time = sum(row[16] for row in combined_data) / len(combined_data)
    
    # 添加平均值行
    combined_data.append([
        "Avg", "-", "-", "-", "-",
        avg_dfs_path, avg_dfs_time,
        avg_bfs_path, avg_bfs_time,
        avg_astar_path, avg_astar_time,
        avg_bidirectional_path, avg_bidirectional_time,
        avg_hgbpc_uf_build, avg_hgbpc_uf_query, avg_hgbpc_path, avg_hgbpc_time
    ])
    
    # 保存为CSV文件
    csv_filename = 'rq2_combined_algorithm_performance.csv'
    
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # 写入表头
        headers = [
            'No', 'n', 'k', 'r', 'h',
            'DFS_path_length', 'DFS_path_time_ms',
            'BFS_path_length', 'BFS_path_time_ms',
            'A*_path_length', 'A*_path_time_ms',
            'Bidirectional_BFS_path_length', 'Bidirectional_BFS_path_time_ms',
            'HGBPC_uf_build_time_ms', 'HGBPC_uf_query_time_ms', 'HGBPC_path_length', 'HGBPC_path_time_ms'
        ]
        writer.writerow(headers)
        
        # 写入数据
        writer.writerows(combined_data)
    
    print(f"CSV文件已创建: {csv_filename}")
    
    # 打印汇总信息
    print("\n=== RQ2数据汇总 ===")
    print(f"总配置数: {len(combined_data) - 1}")  # 减去平均值行
    print(f"DFS平均路径长度: {avg_dfs_path:.2f}, 平均时间: {avg_dfs_time:.3f} ms")
    print(f"BFS平均路径长度: {avg_bfs_path:.2f}, 平均时间: {avg_bfs_time:.3f} ms")
    print(f"A*平均路径长度: {avg_astar_path:.2f}, 平均时间: {avg_astar_time:.3f} ms")
    print(f"双向BFS平均路径长度: {avg_bidirectional_path:.2f}, 平均时间: {avg_bidirectional_time:.3f} ms")
    print(f"HGBPC平均路径长度: {avg_hgbpc_path:.2f}, 平均时间: {avg_hgbpc_time:.3f} ms")
    
    # 性能比较
    print("\n=== 性能比较 ===")
    print(f"A* vs BFS 时间比: {avg_astar_time/avg_bfs_time:.2f}x")
    print(f"双向BFS vs BFS 时间比: {avg_bidirectional_time/avg_bfs_time:.2f}x")
    print(f"A* vs 双向BFS 时间比: {avg_astar_time/avg_bidirectional_time:.2f}x")
    print(f"A* vs BFS 路径比: {avg_astar_path/avg_bfs_path:.2f}x")
    print(f"双向BFS vs BFS 路径比: {avg_bidirectional_path/avg_bfs_path:.2f}x")
    
    # 打印表格格式
    print("\n=== 表格数据 ===")
    print("No. | n | k | r | h | DFS_Path | DFS_Time | BFS_Path | BFS_Time | A*_Path | A*_Time | BBFS_Path | BBFS_Time | HGBPC_Path | HGBPC_Time")
    print("----|---|---|---|---|----------|----------|----------|----------|---------|---------|-----------|-----------|------------|------------")
    
    for row in combined_data:
        if row[0] == "Avg":
            print(f"Avg | - | - | - | - | {row[5]:8.2f} | {row[6]:8.3f} | {row[7]:8.2f} | {row[8]:8.3f} | {row[9]:7.2f} | {row[10]:7.3f} | {row[11]:9.2f} | {row[12]:9.3f} | {row[15]:10.2f} | {row[16]:10.3f}")
        else:
            print(f"{row[0]:2d}  | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]:8.2f} | {row[6]:8.3f} | {row[7]:8.2f} | {row[8]:8.3f} | {row[9]:7.2f} | {row[10]:7.3f} | {row[11]:9.2f} | {row[12]:9.3f} | {row[15]:10.2f} | {row[16]:10.3f}")
    
    return combined_data

def create_latex_table(combined_data):
    """
    创建完整的LaTeX表格
    """
    print("\n=== 完整LaTeX表格 ===")
    print("\\begin{table*}")
    print("\\centering")
    print("\\caption{Performance of BFS, DFS, A*, BBFS, and HGBPC with Source and End Fault-free Nodes from the Same Component}")
    print("\\label{tab:rq2_combined_algorithm_performance}")
    print("\\begin{tabular}{c|c|c|c|c|cc|cc|cc|cc|cccc}")
    print("\\hline\\hline")
    print("\\multirow{2}{*}{\\textbf{No}} & \\multirow{2}{*}{\\textbf{n}} & \\multirow{2}{*}{\\textbf{k}} & \\multirow{2}{*}{\\textbf{r}} & \\multirow{2}{*}{\\textbf{h}} & \\multicolumn{2}{c|}{\\textbf{DFS}} & \\multicolumn{2}{c|}{\\textbf{BFS}} & \\multicolumn{2}{c|}{\\textbf{A*}} & \\multicolumn{2}{c|}{\\textbf{BBFS}} & \\multicolumn{4}{c}{\\textbf{HGBPC}} \\\\")
    print("\\cline{6-17}")
    print(" & & & & & \\textbf{path\\_length} & \\textbf{path\\_time} & \\textbf{path\\_length} & \\textbf{path\\_time} & \\textbf{path\\_length} & \\textbf{path\\_time} & \\textbf{path\\_length} & \\textbf{path\\_time} & \\textbf{uf\\_build\\_time} & \\textbf{uf\\_query\\_time} & \\textbf{path\\_length} & \\textbf{path\\_time} \\\\")
    print("\\hline")
    
    for row in combined_data:
        if row[0] == "Avg":
            print("\\hline")
            print(f"\\textbf{{Avg}} & \\textbf{{-}} & \\textbf{{-}} & \\textbf{{-}} & \\textbf{{-}} & \\textbf{{{row[5]:.2f}}} & \\textbf{{{row[6]:.3f}}} & \\textbf{{{row[7]:.2f}}} & \\textbf{{{row[8]:.3f}}} & \\textbf{{{row[9]:.2f}}} & \\textbf{{{row[10]:.3f}}} & \\textbf{{{row[11]:.2f}}} & \\textbf{{{row[12]:.3f}}} & \\textbf{{{row[13]:.3f}}} & \\textbf{{{row[14]:.3f}}} & \\textbf{{{row[15]:.2f}}} & \\textbf{{{row[16]:.3f}}} \\\\")
        else:
            print(f"\\textbf{{{int(row[0])}}} & {int(row[1])} & {int(row[2])} & {int(row[3])} & {int(row[4])} & {row[5]:.2f} & {row[6]:.3f} & {row[7]:.2f} & {row[8]:.3f} & {row[9]:.2f} & {row[10]:.3f} & {row[11]:.2f} & {row[12]:.3f} & {row[13]:.3f} & {row[14]:.3f} & {row[15]:.2f} & {row[16]:.3f} \\\\")
    
    print("\\hline\\hline")
    print("\\end{tabular}")
    print("\\end{table*}")

if __name__ == "__main__":
    combined_data = create_rq2_combined_excel()
    if combined_data:
        create_latex_table(combined_data)
