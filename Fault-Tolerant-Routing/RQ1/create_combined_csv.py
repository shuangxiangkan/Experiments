#!/usr/bin/env python3
"""
创建合并的CSV文件，包含所有算法的性能数据（不依赖pandas）
"""

import csv

def create_combined_csv():
    """
    创建包含所有算法性能数据的CSV文件
    """
    print("=== 创建合并的CSV文件 ===")
    
    # 原始表格数据 (DFS, BFS, HGBPC)
    original_data = [
        [1, 4, 4, 2, 0, 1.465, 0.817, 1.480, 0.001],
        [2, 4, 4, 2, 1, 1.413, 0.800, 1.554, 0.001],
        [3, 4, 4, 3, 0, 1.321, 0.763, 1.299, 0.001],
        [4, 4, 4, 3, 1, 1.155, 0.701, 1.100, 0.001],
        [5, 4, 4, 4, 0, 1.194, 0.715, 1.190, 0.001],
        [6, 4, 4, 4, 1, 1.032, 0.656, 0.973, 0.001],
        [7, 5, 4, 2, 0, 32.816, 4.538, 10.100, 0.001],
        [8, 5, 4, 2, 1, 30.757, 4.467, 8.330, 0.001],
        [9, 5, 4, 3, 0, 28.234, 4.442, 8.000, 0.001],
        [10, 5, 4, 3, 1, 26.687, 4.281, 7.597, 0.001],
        [11, 5, 4, 4, 0, 27.444, 4.355, 7.695, 0.001],
        [12, 5, 4, 4, 1, 22.959, 4.155, 7.150, 0.001],
        [13, 6, 4, 2, 0, 805.379, 23.437, 47.341, 0.001],
        [14, 6, 4, 2, 1, 775.239, 23.530, 44.858, 0.001],
        [15, 6, 4, 3, 0, 776.429, 23.778, 43.548, 0.001],
        [16, 6, 4, 3, 1, 747.787, 23.069, 42.574, 0.001],
        [17, 6, 4, 4, 0, 756.214, 23.210, 44.042, 0.001],
        [18, 6, 4, 4, 1, 8347.513, 23.786, 42.039, 0.001],
    ]
    
    # 读取A*和双向BFS数据
    astar_bidirectional_data = {}
    try:
        with open('rq1_average_times_analysis.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                no = int(row['No'])
                astar_time = float(row['astar_avg_time_ms'])
                bidirectional_time = float(row['bidirectional_bfs_avg_time_ms'])
                astar_bidirectional_data[no] = (astar_time, bidirectional_time)
    except FileNotFoundError:
        print("错误: 找不到 rq1_average_times_analysis.csv 文件")
        return
    
    # 合并数据
    combined_data = []
    for row in original_data:
        no = row[0]
        n, k, r, h = row[1:5]
        dfs_time, bfs_time, hgbpc_uf_build, hgbpc_uf_query = row[5:9]
        
        # 获取A*和双向BFS数据
        if no in astar_bidirectional_data:
            astar_time, bidirectional_time = astar_bidirectional_data[no]
        else:
            astar_time, bidirectional_time = 0, 0
            print(f"警告: 配置 {no} 的A*和双向BFS数据缺失")
        
        combined_data.append([
            no, n, k, r, h,
            dfs_time, bfs_time, astar_time, bidirectional_time,
            hgbpc_uf_build, hgbpc_uf_query
        ])
    
    # 计算平均值
    avg_dfs = sum(row[5] for row in combined_data) / len(combined_data)
    avg_bfs = sum(row[6] for row in combined_data) / len(combined_data)
    avg_astar = sum(row[7] for row in combined_data) / len(combined_data)
    avg_bidirectional = sum(row[8] for row in combined_data) / len(combined_data)
    avg_hgbpc_build = sum(row[9] for row in combined_data) / len(combined_data)
    avg_hgbpc_query = sum(row[10] for row in combined_data) / len(combined_data)
    
    # 添加平均值行
    combined_data.append([
        "Avg", "-", "-", "-", "-",
        avg_dfs, avg_bfs, avg_astar, avg_bidirectional,
        avg_hgbpc_build, avg_hgbpc_query
    ])
    
    # 保存为CSV文件
    csv_filename = 'combined_algorithm_performance.csv'
    
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # 写入表头
        headers = [
            'No', 'n', 'k', 'r', 'h',
            'DFS_search_time_ms', 'BFS_search_time_ms', 'A*_search_time_ms', 'Bidirectional_BFS_search_time_ms',
            'HGBPC_uf_build_time_ms', 'HGBPC_uf_query_time_ms'
        ]
        writer.writerow(headers)
        
        # 写入数据
        writer.writerows(combined_data)
    
    print(f"CSV文件已创建: {csv_filename}")
    
    # 打印汇总信息
    print("\n=== 数据汇总 ===")
    print(f"总配置数: {len(combined_data) - 1}")  # 减去平均值行
    print(f"DFS平均时间: {avg_dfs:.3f} ms")
    print(f"BFS平均时间: {avg_bfs:.3f} ms")
    print(f"A*平均时间: {avg_astar:.3f} ms")
    print(f"双向BFS平均时间: {avg_bidirectional:.3f} ms")
    print(f"HGBPC构建时间: {avg_hgbpc_build:.3f} ms")
    print(f"HGBPC查询时间: {avg_hgbpc_query:.3f} ms")
    
    # 性能比较
    print("\n=== 性能比较 ===")
    print(f"双向BFS vs BFS: {avg_bidirectional/avg_bfs:.2f}x")
    print(f"A* vs BFS: {avg_astar/avg_bfs:.2f}x")
    print(f"双向BFS vs A*: {avg_bidirectional/avg_astar:.2f}x")
    
    # 打印表格格式
    print("\n=== 表格数据 ===")
    print("No. | n | k | r | h | DFS    | BFS   | A*     | BBFS   | HGBPC_build | HGBPC_query")
    print("----|---|---|---|---|--------|-------|--------|--------|-------------|------------")
    
    for row in combined_data:
        if row[0] == "Avg":
            print(f"Avg | - | - | - | - | {row[5]:6.3f} | {row[6]:5.3f} | {row[7]:6.3f} | {row[8]:6.3f} | {row[9]:11.3f} | {row[10]:11.3f}")
        else:
            print(f"{row[0]:2d}  | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]:6.3f} | {row[6]:5.3f} | {row[7]:6.3f} | {row[8]:6.3f} | {row[9]:11.3f} | {row[10]:11.3f}")
    
    return combined_data

if __name__ == "__main__":
    create_combined_csv()
