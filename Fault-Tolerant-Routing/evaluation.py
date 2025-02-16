import time
import csv

from AugmentedKAryNCube import AugmentedKAryNCube

def run_experiment(n, k, r, h, source_sink_from_different_branches, iterations=20):
    """
    运行实验，记录 100 次连通性检查数据，并存入 CSV 文件
    """
    # 创建 Augmented k-ary n-cube
    aq = AugmentedKAryNCube(n, k, r, h)

    # 记录实验结果
    results = []

    for _ in range(iterations):

        # 选择 source 和 sink
        if source_sink_from_different_branches:
            source, sink = aq.get_source_sink_different_branches()
            # aq.print_node_states()
        else:
            source, sink = aq.get_source_sink_largest_branch()

        # 获取并查集构建时间
        uf_build_time = format(aq.uf_build_time, ".6f")

        # 计算并查集连通性检查时间
        start_time = time.time()
        uf_connected = aq.are_connected(source, sink)
        uf_connected_time = format(time.time() - start_time, ".6f")

        # 1. DFS
        # dfs_start = time.time()
        dfs_connected, dfs_path, dfs_time = aq.dfs(source, sink)
        dfs_path_length = len(dfs_path) if dfs_connected else -1
        dfs_time = format(dfs_time, ".6f")

        # 2. BFS
        # bfs_start = time.time()
        bfs_connected, bfs_path, bfs_time = aq.bfs(source, sink)
        bfs_path_length = len(bfs_path) if bfs_connected else -1
        bfs_time = format(bfs_time, ".6f")

        # 3. Find Fault-Free Path (FFFP)
        # fffp_start = time.time()
        fffp_connected, fffp_path, fffp_time, used_bfs = aq.find_fault_free_path(source, sink)
        fffp_path_length = len(fffp_path) if fffp_connected else -1
        fffp_time = format(fffp_time, ".6f")

        # 记录实验数据
        results.append([
            n, k, r, source_sink_from_different_branches, uf_build_time, uf_connected, uf_connected_time,
            dfs_connected, dfs_path_length, dfs_time,
            bfs_connected, bfs_path_length, bfs_time,
            fffp_connected, fffp_path_length, fffp_time, used_bfs
        ])

    # 生成 CSV 文件名
    output_file = f"./evaluation-test/fault_tolerant_results_n{n}_k{k}_r{r}_h{h}_source_sink_from_different_branches{source_sink_from_different_branches}.csv"

    # 写入 CSV 文件
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "n", "k", "r", "source_sink_from_different_branches", "uf_build_time", "uf_connected", "uf_connected_time",
            "dfs_connected", "dfs_path_length", "dfs_time",
            "bfs_connected", "bfs_path_length", "bfs_time",
            "fffp_connected", "fffp_path_length", "fffp_time", "used_bfs"
        ])
        writer.writerows(results)

    print(f"实验完成，结果已保存到 {output_file}")


# 运行实验示例
if __name__ == "__main__":

    # n >=4, k >=4, 2 <= r <=n, h = 0或1

    # run_experiment(n=4, k=4, r=2, h = 0, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=4, r=2, h = 0, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=4, r=2, h = 1, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=4, r=2, h = 1, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=4, r=3, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=4, r=3, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=4, r=3, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=4, r=3, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=4, r=4, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=4, r=4, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=4, r=4, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=4, r=4, h=1, source_sink_from_different_branches=False)
    #
    # run_experiment(n=4, k=5, r=2, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=5, r=2, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=5, r=2, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=5, r=2, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=5, r=3, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=5, r=3, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=5, r=3, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=5, r=3, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=5, r=4, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=5, r=4, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=5, r=4, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=5, r=4, h=1, source_sink_from_different_branches=False)
    #
    # run_experiment(n=4, k=6, r=2, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=6, r=2, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=6, r=2, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=6, r=2, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=6, r=3, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=6, r=3, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=6, r=3, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=6, r=3, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=6, r=4, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=6, r=4, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=6, r=4, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=6, r=4, h=1, source_sink_from_different_branches=False)
    #
    # run_experiment(n=5, k=4, r=2, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=4, r=2, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=4, r=2, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=4, r=2, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=4, r=3, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=4, r=3, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=4, r=3, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=4, r=3, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=4, r=4, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=4, r=4, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=4, r=4, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=4, r=4, h=1, source_sink_from_different_branches=False)
    #
    # run_experiment(n=5, k=5, r=2, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=5, r=2, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=5, r=2, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=5, r=2, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=5, r=3, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=5, r=3, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=5, r=3, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=5, r=3, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=5, r=4, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=5, r=4, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=5, r=4, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=5, r=4, h=1, source_sink_from_different_branches=False)
    #
    # run_experiment(n=5, k=6, r=2, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=6, r=2, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=6, r=2, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=6, r=2, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=6, r=3, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=6, r=3, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=6, r=3, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=6, r=3, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=6, r=4, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=6, r=4, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=5, k=6, r=4, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=6, r=4, h=1, source_sink_from_different_branches=False)
    #
    # run_experiment(n=6, k=4, r=2, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=4, r=2, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=4, r=2, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=4, r=2, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=4, r=3, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=4, r=3, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=4, r=3, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=4, r=3, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=4, r=4, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=4, r=4, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=4, r=4, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=4, r=4, h=1, source_sink_from_different_branches=False)
    #
    # run_experiment(n=6, k=5, r=2, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=5, r=2, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=5, r=2, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=5, r=2, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=5, r=3, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=5, r=3, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=5, r=3, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=5, r=3, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=5, r=4, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=5, r=4, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=5, r=4, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=5, r=4, h=1, source_sink_from_different_branches=False)

    run_experiment(n=6, k=6, r=2, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=6, r=2, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=6, r=2, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=6, r=2, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=6, r=3, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=6, r=3, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=6, r=3, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=6, r=3, h=1, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=6, r=4, h=0, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=6, r=4, h=0, source_sink_from_different_branches=False)
    # run_experiment(n=6, k=6, r=4, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=6, r=4, h=1, source_sink_from_different_branches=False)

    # run_experiment(n=4, k=5, r=3, h = 0, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=5, r=3, h = 0, source_sink_from_different_branches=False)
    # run_experiment(n=4, k=5, r=3, h=1, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=5, r=3, h=1, source_sink_from_different_branches=False)
    #
    # run_experiment(n=4, k=4, r=3, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=4, r=3, source_sink_from_different_branches=False)
    #
    # run_experiment(n=5, k=4, r=3, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=4, r=3, source_sink_from_different_branches=False)
    #
    # run_experiment(n=5, k=5, r=4, source_sink_from_different_branches=True)
    # run_experiment(n=5, k=5, r=4, source_sink_from_different_branches=False)
    #
    # run_experiment(n=6, k=3, r=5, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=3, r=5, source_sink_from_different_branches=False)
    #
    # run_experiment(n=6, k=4, r=3, source_sink_from_different_branches=True)
    # run_experiment(n=6, k=4, r=3, source_sink_from_different_branches=False)
    #
    # run_experiment(n=7, k=2, r=2, source_sink_from_different_branches=True)
    # run_experiment(n=7, k=2, r=2, source_sink_from_different_branches=False)
    #
    # run_experiment(n=7, k=3, r=5, source_sink_from_different_branches=True)
    # run_experiment(n=7, k=3, r=5, source_sink_from_different_branches=False)
    # #
    # run_experiment(n=4, k=7, r=3, source_sink_from_different_branches=True)
    # run_experiment(n=4, k=7, r=3, source_sink_from_different_branches=False)
