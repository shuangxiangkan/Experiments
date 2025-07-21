#!/usr/bin/env python3
"""
RQ1实验：A*和双向BFS算法性能评估
专门针对18种网络配置进行A*和双向BFS算法的性能测试
"""

import sys
import os
sys.path.append('..')

from AugmentedKAryNCube import AugmentedKAryNCube
import csv
import random
import time

def run_rq1_experiment(n, k, r, h, iterations=10):
    """
    运行RQ1实验：只测试A*和双向BFS算法
    
    :param n: 网络维度
    :param k: 基数
    :param r: 分支数量
    :param h: 分支最小节点数
    :param iterations: 迭代次数
    """
    print(f"开始RQ1实验: n={n}, k={k}, r={r}, h={h}")
    
    results = []
    
    for i in range(iterations):
        print(f"  迭代 {i+1}/{iterations}")
        
        # 创建增强k元n立方体
        aq = AugmentedKAryNCube(n, k, r, h)
        
        # 获取连通分支
        components = aq.uf.get_connected_components()
        
        # 选择源节点和目标节点（从不同分支中选择）
        if len(components) >= 2:
            # 从不同分支选择
            branch_sizes = [(branch_id, len(nodes)) for branch_id, nodes in components.items()]
            branch_sizes.sort(key=lambda x: x[1], reverse=True)  # 按大小排序
            
            # 选择两个最大的分支
            branch1_nodes = list(components[branch_sizes[0][0]])
            branch2_nodes = list(components[branch_sizes[1][0]])
            
            source = random.choice(branch1_nodes)
            sink = random.choice(branch2_nodes)
            source_sink_from_different_branches = True
        else:
            # 如果只有一个分支，从同一分支选择
            largest_branch = max(components.values(), key=len)
            if len(largest_branch) >= 2:
                source, sink = random.sample(largest_branch, 2)
                source_sink_from_different_branches = False
            else:
                print(f"    跳过迭代 {i+1}: 无足够节点")
                continue
        
        # 1. A*算法
        astar_connected, astar_path, astar_time = aq.astar(source, sink)
        astar_path_length = len(astar_path) if astar_connected else -1
        astar_time = format(astar_time, ".6f")
        
        # 2. 双向BFS算法
        bidirectional_bfs_connected, bidirectional_bfs_path, bidirectional_bfs_time = aq.bidirectional_bfs(source, sink)
        bidirectional_bfs_path_length = len(bidirectional_bfs_path) if bidirectional_bfs_connected else -1
        bidirectional_bfs_time = format(bidirectional_bfs_time, ".6f")
        
        # 记录实验数据
        results.append([
            n, k, r, h, source_sink_from_different_branches,
            astar_connected, astar_path_length, astar_time,
            bidirectional_bfs_connected, bidirectional_bfs_path_length, bidirectional_bfs_time
        ])
    
    # 生成CSV文件名
    output_file = f"rq1_results_n{n}_k{k}_r{r}_h{h}.csv"
    
    # 保存结果到CSV文件
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # 写入表头
        writer.writerow([
            "n", "k", "r", "h", "source_sink_from_different_branches",
            "astar_connected", "astar_path_length", "astar_time",
            "bidirectional_bfs_connected", "bidirectional_bfs_path_length", "bidirectional_bfs_time"
        ])
        
        # 写入数据
        writer.writerows(results)
    
    print(f"实验完成，结果已保存到 {output_file}")

def run_all_rq1_experiments():
    """
    运行所有18种网络配置的RQ1实验
    """
    # 18种网络配置
    configurations = [
        # No.1-6: n=4, k=4
        (4, 4, 2, 0),  # No.1
        (4, 4, 2, 1),  # No.2
        (4, 4, 3, 0),  # No.3
        (4, 4, 3, 1),  # No.4
        (4, 4, 4, 0),  # No.5
        (4, 4, 4, 1),  # No.6
        
        # No.7-12: n=5, k=4
        (5, 4, 2, 0),  # No.7
        (5, 4, 2, 1),  # No.8
        (5, 4, 3, 0),  # No.9
        (5, 4, 3, 1),  # No.10
        (5, 4, 4, 0),  # No.11
        (5, 4, 4, 1),  # No.12
        
        # No.13-18: n=6, k=4
        (6, 4, 2, 0),  # No.13
        (6, 4, 2, 1),  # No.14
        (6, 4, 3, 0),  # No.15
        (6, 4, 3, 1),  # No.16
        (6, 4, 4, 0),  # No.17
        (6, 4, 4, 1),  # No.18
    ]
    
    print("开始运行所有RQ1实验配置...")
    print(f"总共 {len(configurations)} 种配置")
    
    start_time = time.time()
    completed = 0
    
    for i, (n, k, r, h) in enumerate(configurations, 1):
        try:
            print(f"\n=== 配置 {i}/18 ===")
            run_rq1_experiment(n, k, r, h, iterations=10)
            completed += 1
        except Exception as e:
            print(f"配置 {i} 失败: {e}")
            continue
    
    total_time = time.time() - start_time
    print(f"\n=== RQ1实验完成 ===")
    print(f"成功完成: {completed}/{len(configurations)} 个配置")
    print(f"总耗时: {total_time:.2f}秒")
    print(f"平均每个配置: {total_time/completed:.2f}秒" if completed > 0 else "无成功配置")

def analyze_rq1_results():
    """
    分析RQ1实验结果
    """
    import glob
    import pandas as pd
    
    print("\n=== 分析RQ1实验结果 ===")
    
    # 加载所有RQ1结果文件
    csv_files = glob.glob("rq1_results_*.csv")
    print(f"找到 {len(csv_files)} 个结果文件")
    
    if not csv_files:
        print("没有找到结果文件")
        return
    
    all_data = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            all_data.append(df)
        except Exception as e:
            print(f"读取文件 {file} 失败: {e}")
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        print(f"总记录数: {len(combined_df)}")
        
        # 分析A*算法性能
        astar_successful = combined_df[combined_df['astar_connected'] == True]
        if len(astar_successful) > 0:
            avg_astar_time = astar_successful['astar_time'].astype(float).mean()
            avg_astar_length = astar_successful['astar_path_length'].mean()
            print(f"A*算法 - 成功率: {len(astar_successful)/len(combined_df)*100:.1f}%")
            print(f"A*算法 - 平均时间: {avg_astar_time:.6f}秒")
            print(f"A*算法 - 平均路径长度: {avg_astar_length:.2f}")
        
        # 分析双向BFS算法性能
        bidirectional_successful = combined_df[combined_df['bidirectional_bfs_connected'] == True]
        if len(bidirectional_successful) > 0:
            avg_bidirectional_time = bidirectional_successful['bidirectional_bfs_time'].astype(float).mean()
            avg_bidirectional_length = bidirectional_successful['bidirectional_bfs_path_length'].mean()
            print(f"双向BFS算法 - 成功率: {len(bidirectional_successful)/len(combined_df)*100:.1f}%")
            print(f"双向BFS算法 - 平均时间: {avg_bidirectional_time:.6f}秒")
            print(f"双向BFS算法 - 平均路径长度: {avg_bidirectional_length:.2f}")
        
        # 保存合并结果
        combined_df.to_csv("rq1_combined_results.csv", index=False)
        print("合并结果已保存到: rq1_combined_results.csv")

if __name__ == "__main__":
    # 设置随机种子以获得可重复的结果
    random.seed(42)
    
    # 运行所有RQ1实验
    run_all_rq1_experiments()
    
    # 分析结果
    try:
        analyze_rq1_results()
    except ImportError:
        print("pandas未安装，跳过结果分析")
    except Exception as e:
        print(f"结果分析失败: {e}")
