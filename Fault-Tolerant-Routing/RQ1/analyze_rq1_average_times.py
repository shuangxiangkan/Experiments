#!/usr/bin/env python3
"""
分析RQ1实验结果：计算A*和双向BFS在每种网络结构下的平均时间
"""

import csv
import glob
import os

def analyze_average_times():
    """
    分析每种网络配置下A*和双向BFS的平均时间
    """
    print("=== 分析RQ1实验平均时间 ===")
    
    # 18种网络配置
    configurations = [
        (4, 4, 2, 0),  # No.1
        (4, 4, 2, 1),  # No.2
        (4, 4, 3, 0),  # No.3
        (4, 4, 3, 1),  # No.4
        (4, 4, 4, 0),  # No.5
        (4, 4, 4, 1),  # No.6
        (5, 4, 2, 0),  # No.7
        (5, 4, 2, 1),  # No.8
        (5, 4, 3, 0),  # No.9
        (5, 4, 3, 1),  # No.10
        (5, 4, 4, 0),  # No.11
        (5, 4, 4, 1),  # No.12
        (6, 4, 2, 0),  # No.13
        (6, 4, 2, 1),  # No.14
        (6, 4, 3, 0),  # No.15
        (6, 4, 3, 1),  # No.16
        (6, 4, 4, 0),  # No.17
        (6, 4, 4, 1),  # No.18
    ]
    
    results = []
    
    for i, (n, k, r, h) in enumerate(configurations, 1):
        filename = f"rq1_results_n{n}_k{k}_r{r}_h{h}.csv"
        
        if not os.path.exists(filename):
            print(f"文件不存在: {filename}")
            continue
        
        print(f"处理配置 {i}: n={n}, k={k}, r={r}, h={h}")
        
        astar_times = []
        bidirectional_times = []
        total_records = 0
        
        try:
            with open(filename, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    total_records += 1
                    
                    # 读取A*时间（无论是否连接成功都记录时间）
                    astar_time = float(row['astar_time'])
                    astar_times.append(astar_time)
                    
                    # 读取双向BFS时间（无论是否连接成功都记录时间）
                    bidirectional_time = float(row['bidirectional_bfs_time'])
                    bidirectional_times.append(bidirectional_time)
            
            # 计算平均时间
            avg_astar_time = sum(astar_times) / len(astar_times) if astar_times else 0
            avg_bidirectional_time = sum(bidirectional_times) / len(bidirectional_times) if bidirectional_times else 0
            
            # 转换为毫秒
            avg_astar_time_ms = avg_astar_time * 1000
            avg_bidirectional_time_ms = avg_bidirectional_time * 1000
            
            print(f"  记录数: {total_records}")
            print(f"  A*平均时间: {avg_astar_time_ms:.3f} ms")
            print(f"  双向BFS平均时间: {avg_bidirectional_time_ms:.3f} ms")
            
            results.append({
                'No': i,
                'n': n,
                'k': k,
                'r': r,
                'h': h,
                'astar_avg_time_ms': avg_astar_time_ms,
                'bidirectional_bfs_avg_time_ms': avg_bidirectional_time_ms,
                'records_count': total_records
            })
            
        except Exception as e:
            print(f"  处理文件 {filename} 时出错: {e}")
            continue
    
    # 保存结果到CSV文件
    output_filename = "rq1_average_times_analysis.csv"
    with open(output_filename, 'w', newline='') as csvfile:
        fieldnames = ['No', 'n', 'k', 'r', 'h', 'astar_avg_time_ms', 'bidirectional_bfs_avg_time_ms', 'records_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(results)
    
    print(f"\n结果已保存到: {output_filename}")
    
    # 打印汇总表格
    print("\n=== 汇总结果表格 ===")
    print("No. | n | k | r | h | A* (ms)    | Bidirectional BFS (ms) | Records")
    print("----|---|---|---|---|------------|------------------------|--------")
    
    for result in results:
        print(f"{result['No']:2d}  | {result['n']} | {result['k']} | {result['r']} | {result['h']} | "
              f"{result['astar_avg_time_ms']:8.3f}   | {result['bidirectional_bfs_avg_time_ms']:20.3f}   | {result['records_count']:6d}")
    
    # 计算总体平均值
    if results:
        total_astar_avg = sum(r['astar_avg_time_ms'] for r in results) / len(results)
        total_bidirectional_avg = sum(r['bidirectional_bfs_avg_time_ms'] for r in results) / len(results)
        
        print("----|---|---|---|---|------------|------------------------|--------")
        print(f"Avg | - | - | - | - | {total_astar_avg:8.3f}   | {total_bidirectional_avg:20.3f}   | -")
    
    return results

def create_latex_table(results):
    """
    创建LaTeX表格格式的输出
    """
    print("\n=== LaTeX表格格式 ===")
    print("\\begin{table}")
    print("\\centering")
    print("\\caption{Average Time (ms) Performance of A* and Bidirectional BFS}")
    print("\\label{tab:rq1_astar_bidirectional}")
    print("\\begin{tabular}{c|c|c|c|c|c|c}")
    print("\\hline")
    print("\\textbf{No} & \\textbf{n} & \\textbf{k} & \\textbf{r} & \\textbf{h} & \\textbf{A*} & \\textbf{Bidirectional BFS} \\\\")
    print("\\hline")
    
    for result in results:
        print(f"\\textbf{{{result['No']}}} & {result['n']} & {result['k']} & {result['r']} & {result['h']} & "
              f"{result['astar_avg_time_ms']:.3f} & {result['bidirectional_bfs_avg_time_ms']:.3f} \\\\")
    
    # 计算总体平均值
    if results:
        total_astar_avg = sum(r['astar_avg_time_ms'] for r in results) / len(results)
        total_bidirectional_avg = sum(r['bidirectional_bfs_avg_time_ms'] for r in results) / len(results)
        
        print("\\hline")
        print(f"\\textbf{{Avg}} & - & - & - & - & \\textbf{{{total_astar_avg:.3f}}} & \\textbf{{{total_bidirectional_avg:.3f}}} \\\\")
    
    print("\\hline")
    print("\\end{tabular}")
    print("\\end{table}")

if __name__ == "__main__":
    results = analyze_average_times()
    
    if results:
        create_latex_table(results)
    else:
        print("没有找到有效的结果数据")
