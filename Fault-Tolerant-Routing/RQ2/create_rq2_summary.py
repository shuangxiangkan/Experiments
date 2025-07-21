#!/usr/bin/env python3
"""
创建RQ2实验结果的汇总表格和Excel文件
"""

import csv

def create_rq2_summary():
    """
    创建RQ2实验结果的汇总
    """
    print("=== 创建RQ2实验结果汇总 ===")
    
    # 读取分析结果
    analysis_data = []
    try:
        with open('rq2_analysis_results.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                analysis_data.append({
                    'No': int(row['No']),
                    'n': int(row['n']),
                    'k': int(row['k']),
                    'r': int(row['r']),
                    'h': int(row['h']),
                    'astar_time_ms': float(row['astar_avg_time_ms']),
                    'astar_path_length': float(row['astar_avg_path_length']),
                    'bidirectional_time_ms': float(row['bidirectional_avg_time_ms']),
                    'bidirectional_path_length': float(row['bidirectional_avg_path_length']),
                    'astar_success_rate': float(row['astar_success_rate']),
                    'bidirectional_success_rate': float(row['bidirectional_success_rate'])
                })
    except FileNotFoundError:
        print("错误: 找不到 rq2_analysis_results.csv 文件")
        return
    
    if not analysis_data:
        print("没有找到分析数据")
        return
    
    # 计算平均值
    avg_astar_time = sum(row['astar_time_ms'] for row in analysis_data) / len(analysis_data)
    avg_astar_path = sum(row['astar_path_length'] for row in analysis_data) / len(analysis_data)
    avg_bidirectional_time = sum(row['bidirectional_time_ms'] for row in analysis_data) / len(analysis_data)
    avg_bidirectional_path = sum(row['bidirectional_path_length'] for row in analysis_data) / len(analysis_data)
    avg_astar_success = sum(row['astar_success_rate'] for row in analysis_data) / len(analysis_data)
    avg_bidirectional_success = sum(row['bidirectional_success_rate'] for row in analysis_data) / len(analysis_data)
    
    # 创建汇总CSV
    summary_data = analysis_data.copy()
    summary_data.append({
        'No': "Avg",
        'n': "-",
        'k': "-", 
        'r': "-",
        'h': "-",
        'astar_time_ms': avg_astar_time,
        'astar_path_length': avg_astar_path,
        'bidirectional_time_ms': avg_bidirectional_time,
        'bidirectional_path_length': avg_bidirectional_path,
        'astar_success_rate': avg_astar_success,
        'bidirectional_success_rate': avg_bidirectional_success
    })
    
    # 保存汇总CSV
    with open('rq2_summary.csv', 'w', newline='') as csvfile:
        fieldnames = ['No', 'n', 'k', 'r', 'h', 'astar_time_ms', 'astar_path_length', 
                     'bidirectional_time_ms', 'bidirectional_path_length', 
                     'astar_success_rate', 'bidirectional_success_rate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(summary_data)
    
    print("汇总CSV已保存到: rq2_summary.csv")
    
    # 打印表格
    print("\n=== RQ2实验结果汇总表格 ===")
    print("No. | n | k | r | h | A* Time(ms) | A* Path | BBFS Time(ms) | BBFS Path | Success Rate")
    print("----|---|---|---|---|-------------|---------|---------------|-----------|-------------")
    
    for row in summary_data:
        if row['No'] == "Avg":
            print(f"Avg | - | - | - | - | {row['astar_time_ms']:9.3f}   | {row['astar_path_length']:5.2f}   | "
                  f"{row['bidirectional_time_ms']:11.3f}   | {row['bidirectional_path_length']:7.2f}   | "
                  f"{row['astar_success_rate']:6.1f}% / {row['bidirectional_success_rate']:5.1f}%")
        else:
            print(f"{row['No']:2d}  | {row['n']} | {row['k']} | {row['r']} | {row['h']} | "
                  f"{row['astar_time_ms']:9.3f}   | {row['astar_path_length']:5.2f}   | "
                  f"{row['bidirectional_time_ms']:11.3f}   | {row['bidirectional_path_length']:7.2f}   | "
                  f"{row['astar_success_rate']:6.1f}% / {row['bidirectional_success_rate']:5.1f}%")
    
    # 创建LaTeX表格
    print("\n=== LaTeX表格 ===")
    print("\\begin{table}")
    print("\\centering")
    print("\\caption{RQ2: Time (ms) and Path Length Performance of A* and Bidirectional BFS with Source and Target from Same Component}")
    print("\\label{tab:rq2_astar_bidirectional}")
    print("\\begin{tabular}{c|c|c|c|c|c|c|c|c}")
    print("\\hline")
    print("\\multirow{2}{*}{\\textbf{No}} & \\multirow{2}{*}{\\textbf{n}} & \\multirow{2}{*}{\\textbf{k}} & \\multirow{2}{*}{\\textbf{r}} & \\multirow{2}{*}{\\textbf{h}} & \\multicolumn{2}{c|}{\\textbf{A*}} & \\multicolumn{2}{c}{\\textbf{Bidirectional BFS}} \\\\")
    print("\\cline{6-9}")
    print(" & & & & & \\textbf{Time(ms)} & \\textbf{Path} & \\textbf{Time(ms)} & \\textbf{Path} \\\\")
    print("\\hline")
    
    for row in summary_data:
        if row['No'] == "Avg":
            print("\\hline")
            print(f"\\textbf{{Avg}} & - & - & - & - & \\textbf{{{row['astar_time_ms']:.3f}}} & \\textbf{{{row['astar_path_length']:.2f}}} & \\textbf{{{row['bidirectional_time_ms']:.3f}}} & \\textbf{{{row['bidirectional_path_length']:.2f}}} \\\\")
        else:
            print(f"\\textbf{{{row['No']}}} & {row['n']} & {row['k']} & {row['r']} & {row['h']} & {row['astar_time_ms']:.3f} & {row['astar_path_length']:.2f} & {row['bidirectional_time_ms']:.3f} & {row['bidirectional_path_length']:.2f} \\\\")
    
    print("\\hline")
    print("\\end{tabular}")
    print("\\end{table}")
    
    # 性能分析
    print("\n=== 性能分析 ===")
    print(f"A*平均时间: {avg_astar_time:.3f} ms")
    print(f"双向BFS平均时间: {avg_bidirectional_time:.3f} ms")
    print(f"A*平均路径长度: {avg_astar_path:.2f}")
    print(f"双向BFS平均路径长度: {avg_bidirectional_path:.2f}")
    print(f"A*成功率: {avg_astar_success:.1f}%")
    print(f"双向BFS成功率: {avg_bidirectional_success:.1f}%")
    
    print(f"\n性能比较:")
    print(f"A* vs 双向BFS 时间比: {avg_astar_time/avg_bidirectional_time:.2f}x")
    print(f"A* vs 双向BFS 路径比: {avg_astar_path/avg_bidirectional_path:.2f}x")
    
    # 按网络规模分析
    print(f"\n=== 按网络规模分析 ===")
    
    # n=4的配置
    n4_data = [row for row in analysis_data if row['n'] == 4]
    if n4_data:
        n4_astar_time = sum(row['astar_time_ms'] for row in n4_data) / len(n4_data)
        n4_bidirectional_time = sum(row['bidirectional_time_ms'] for row in n4_data) / len(n4_data)
        n4_astar_path = sum(row['astar_path_length'] for row in n4_data) / len(n4_data)
        n4_bidirectional_path = sum(row['bidirectional_path_length'] for row in n4_data) / len(n4_data)
        print(f"n=4: A*时间={n4_astar_time:.3f}ms, 双向BFS时间={n4_bidirectional_time:.3f}ms")
        print(f"     A*路径={n4_astar_path:.2f}, 双向BFS路径={n4_bidirectional_path:.2f}")
    
    # n=5的配置
    n5_data = [row for row in analysis_data if row['n'] == 5]
    if n5_data:
        n5_astar_time = sum(row['astar_time_ms'] for row in n5_data) / len(n5_data)
        n5_bidirectional_time = sum(row['bidirectional_time_ms'] for row in n5_data) / len(n5_data)
        n5_astar_path = sum(row['astar_path_length'] for row in n5_data) / len(n5_data)
        n5_bidirectional_path = sum(row['bidirectional_path_length'] for row in n5_data) / len(n5_data)
        print(f"n=5: A*时间={n5_astar_time:.3f}ms, 双向BFS时间={n5_bidirectional_time:.3f}ms")
        print(f"     A*路径={n5_astar_path:.2f}, 双向BFS路径={n5_bidirectional_path:.2f}")
    
    # n=6的配置
    n6_data = [row for row in analysis_data if row['n'] == 6]
    if n6_data:
        n6_astar_time = sum(row['astar_time_ms'] for row in n6_data) / len(n6_data)
        n6_bidirectional_time = sum(row['bidirectional_time_ms'] for row in n6_data) / len(n6_data)
        n6_astar_path = sum(row['astar_path_length'] for row in n6_data) / len(n6_data)
        n6_bidirectional_path = sum(row['bidirectional_path_length'] for row in n6_data) / len(n6_data)
        print(f"n=6: A*时间={n6_astar_time:.3f}ms, 双向BFS时间={n6_bidirectional_time:.3f}ms")
        print(f"     A*路径={n6_astar_path:.2f}, 双向BFS路径={n6_bidirectional_path:.2f}")

if __name__ == "__main__":
    create_rq2_summary()
