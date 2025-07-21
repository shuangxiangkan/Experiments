#!/usr/bin/env python3
"""
RQ2实验：A*和双向BFS算法性能评估（同一分支内的源节点和目标节点）
专门针对18种网络配置进行A*和双向BFS算法的路径长度和时间测试
source_sink_from_different_branches = False
"""

import sys
import os
sys.path.append('..')

from AugmentedKAryNCube import AugmentedKAryNCube
import csv
import random
import time

def run_rq2_experiment(n, k, r, h, iterations=10):
    """
    运行RQ2实验：只测试A*和双向BFS算法，源节点和目标节点来自同一分支
    
    :param n: 网络维度
    :param k: 基数
    :param r: 分支数量
    :param h: 分支最小节点数
    :param iterations: 迭代次数
    """
    print(f"开始RQ2实验: n={n}, k={k}, r={r}, h={h}")
    
    results = []
    
    for i in range(iterations):
        print(f"  迭代 {i+1}/{iterations}")
        
        # 创建增强k元n立方体
        aq = AugmentedKAryNCube(n, k, r, h)
        
        # 获取连通分支
        components = aq.uf.get_connected_components()
        
        # 选择源节点和目标节点（从同一分支中选择）
        largest_branch = max(components.values(), key=len)
        if len(largest_branch) >= 2:
            source, sink = random.sample(largest_branch, 2)
            source_sink_from_different_branches = False
        else:
            print(f"    跳过迭代 {i+1}: 最大分支节点数不足 ({len(largest_branch)})")
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
    output_file = f"rq2_results_n{n}_k{k}_r{r}_h{h}.csv"
    
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

def run_all_rq2_experiments():
    """
    运行所有18种网络配置的RQ2实验
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
    
    print("开始运行所有RQ2实验配置...")
    print(f"总共 {len(configurations)} 种配置")
    print("注意: source_sink_from_different_branches = False (同一分支内选择)")
    
    start_time = time.time()
    completed = 0
    
    for i, (n, k, r, h) in enumerate(configurations, 1):
        try:
            print(f"\n=== 配置 {i}/18 ===")
            run_rq2_experiment(n, k, r, h, iterations=10)
            completed += 1
        except Exception as e:
            print(f"配置 {i} 失败: {e}")
            continue
    
    total_time = time.time() - start_time
    print(f"\n=== RQ2实验完成 ===")
    print(f"成功完成: {completed}/{len(configurations)} 个配置")
    print(f"总耗时: {total_time:.2f}秒")
    print(f"平均每个配置: {total_time/completed:.2f}秒" if completed > 0 else "无成功配置")

def analyze_rq2_results():
    """
    分析RQ2实验结果：统计路径长度和平均时间
    """
    import glob
    
    print("\n=== 分析RQ2实验结果 ===")
    
    # 加载所有RQ2结果文件
    csv_files = glob.glob("rq2_results_*.csv")
    print(f"找到 {len(csv_files)} 个结果文件")
    
    if not csv_files:
        print("没有找到结果文件")
        return
    
    # 18种网络配置
    configurations = [
        (4, 4, 2, 0), (4, 4, 2, 1), (4, 4, 3, 0), (4, 4, 3, 1), (4, 4, 4, 0), (4, 4, 4, 1),
        (5, 4, 2, 0), (5, 4, 2, 1), (5, 4, 3, 0), (5, 4, 3, 1), (5, 4, 4, 0), (5, 4, 4, 1),
        (6, 4, 2, 0), (6, 4, 2, 1), (6, 4, 3, 0), (6, 4, 3, 1), (6, 4, 4, 0), (6, 4, 4, 1),
    ]
    
    analysis_results = []
    
    for i, (n, k, r, h) in enumerate(configurations, 1):
        filename = f"rq2_results_n{n}_k{k}_r{r}_h{h}.csv"
        
        if not os.path.exists(filename):
            print(f"文件不存在: {filename}")
            continue
        
        print(f"分析配置 {i}: n={n}, k={k}, r={r}, h={h}")
        
        astar_times = []
        astar_path_lengths = []
        bidirectional_times = []
        bidirectional_path_lengths = []
        total_records = 0
        successful_astar = 0
        successful_bidirectional = 0
        
        try:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    total_records += 1
                    
                    # A*数据
                    astar_time = float(row['astar_time'])
                    astar_times.append(astar_time)
                    
                    if row['astar_connected'] == 'True':
                        successful_astar += 1
                        astar_path_length = int(row['astar_path_length'])
                        astar_path_lengths.append(astar_path_length)
                    
                    # 双向BFS数据
                    bidirectional_time = float(row['bidirectional_bfs_time'])
                    bidirectional_times.append(bidirectional_time)
                    
                    if row['bidirectional_bfs_connected'] == 'True':
                        successful_bidirectional += 1
                        bidirectional_path_length = int(row['bidirectional_bfs_path_length'])
                        bidirectional_path_lengths.append(bidirectional_path_length)
            
            # 计算统计数据
            avg_astar_time = sum(astar_times) / len(astar_times) if astar_times else 0
            avg_astar_path_length = sum(astar_path_lengths) / len(astar_path_lengths) if astar_path_lengths else 0
            
            avg_bidirectional_time = sum(bidirectional_times) / len(bidirectional_times) if bidirectional_times else 0
            avg_bidirectional_path_length = sum(bidirectional_path_lengths) / len(bidirectional_path_lengths) if bidirectional_path_lengths else 0
            
            # 转换为毫秒
            avg_astar_time_ms = avg_astar_time * 1000
            avg_bidirectional_time_ms = avg_bidirectional_time * 1000
            
            print(f"  记录数: {total_records}")
            print(f"  A*成功率: {successful_astar}/{total_records} ({successful_astar/total_records*100:.1f}%)")
            print(f"  A*平均时间: {avg_astar_time_ms:.3f} ms")
            print(f"  A*平均路径长度: {avg_astar_path_length:.2f}")
            print(f"  双向BFS成功率: {successful_bidirectional}/{total_records} ({successful_bidirectional/total_records*100:.1f}%)")
            print(f"  双向BFS平均时间: {avg_bidirectional_time_ms:.3f} ms")
            print(f"  双向BFS平均路径长度: {avg_bidirectional_path_length:.2f}")
            
            analysis_results.append({
                'No': i,
                'n': n,
                'k': k,
                'r': r,
                'h': h,
                'astar_success_rate': successful_astar/total_records*100,
                'astar_avg_time_ms': avg_astar_time_ms,
                'astar_avg_path_length': avg_astar_path_length,
                'bidirectional_success_rate': successful_bidirectional/total_records*100,
                'bidirectional_avg_time_ms': avg_bidirectional_time_ms,
                'bidirectional_avg_path_length': avg_bidirectional_path_length,
                'total_records': total_records
            })
            
        except Exception as e:
            print(f"  处理文件 {filename} 时出错: {e}")
            continue
    
    # 保存分析结果
    if analysis_results:
        output_filename = "rq2_analysis_results.csv"
        with open(output_filename, 'w', newline='') as csvfile:
            fieldnames = ['No', 'n', 'k', 'r', 'h', 
                         'astar_success_rate', 'astar_avg_time_ms', 'astar_avg_path_length',
                         'bidirectional_success_rate', 'bidirectional_avg_time_ms', 'bidirectional_avg_path_length',
                         'total_records']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            writer.writerows(analysis_results)
        
        print(f"\n分析结果已保存到: {output_filename}")
        
        # 打印汇总表格
        print("\n=== RQ2汇总结果表格 ===")
        print("No. | n | k | r | h | A* Time(ms) | A* Path | BBFS Time(ms) | BBFS Path | A* Success | BBFS Success")
        print("----|---|---|---|---|-------------|---------|---------------|-----------|------------|-------------")
        
        for result in analysis_results:
            print(f"{result['No']:2d}  | {result['n']} | {result['k']} | {result['r']} | {result['h']} | "
                  f"{result['astar_avg_time_ms']:9.3f}   | {result['astar_avg_path_length']:5.2f}   | "
                  f"{result['bidirectional_avg_time_ms']:11.3f}   | {result['bidirectional_avg_path_length']:7.2f}   | "
                  f"{result['astar_success_rate']:8.1f}%  | {result['bidirectional_success_rate']:10.1f}%")
        
        # 计算总体平均值
        total_astar_time = sum(r['astar_avg_time_ms'] for r in analysis_results) / len(analysis_results)
        total_astar_path = sum(r['astar_avg_path_length'] for r in analysis_results if r['astar_avg_path_length'] > 0)
        total_astar_path = total_astar_path / len([r for r in analysis_results if r['astar_avg_path_length'] > 0]) if total_astar_path > 0 else 0
        
        total_bidirectional_time = sum(r['bidirectional_avg_time_ms'] for r in analysis_results) / len(analysis_results)
        total_bidirectional_path = sum(r['bidirectional_avg_path_length'] for r in analysis_results if r['bidirectional_avg_path_length'] > 0)
        total_bidirectional_path = total_bidirectional_path / len([r for r in analysis_results if r['bidirectional_avg_path_length'] > 0]) if total_bidirectional_path > 0 else 0
        
        total_astar_success = sum(r['astar_success_rate'] for r in analysis_results) / len(analysis_results)
        total_bidirectional_success = sum(r['bidirectional_success_rate'] for r in analysis_results) / len(analysis_results)
        
        print("----|---|---|---|---|-------------|---------|---------------|-----------|------------|-------------")
        print(f"Avg | - | - | - | - | {total_astar_time:9.3f}   | {total_astar_path:5.2f}   | "
              f"{total_bidirectional_time:11.3f}   | {total_bidirectional_path:7.2f}   | "
              f"{total_astar_success:8.1f}%  | {total_bidirectional_success:10.1f}%")

if __name__ == "__main__":
    # 设置随机种子以获得可重复的结果
    random.seed(42)
    
    # 运行所有RQ2实验
    run_all_rq2_experiments()
    
    # 分析结果
    try:
        analyze_rq2_results()
    except Exception as e:
        print(f"结果分析失败: {e}")
