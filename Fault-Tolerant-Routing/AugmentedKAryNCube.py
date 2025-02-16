import csv
import itertools
import math
import time
from itertools import product
import random
from collections import deque

import networkx as nx
from matplotlib import pyplot as plt


class UnionFind:
    def __init__(self, nodes):
        """
        初始化并查集
        只初始化无故障节点
        """
        self.parent = {}
        self.rank = {}
        for node in nodes:
            self.parent[node] = node
            self.rank[node] = 0

    def find(self, node):
        """
        查找节点所属的集合（带路径压缩）
        """
        if node not in self.parent:
            return None
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node1, node2):
        """
        合并两个节点所属的集合（按秩合并）
        """
        if node1 not in self.parent or node2 not in self.parent:
            return

        root1 = self.find(node1)
        root2 = self.find(node2)

        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1

    def connected(self, node1, node2):
        """
        检查两个节点是否连通
        """
        if node1 not in self.parent or node2 not in self.parent:
            return False
        return self.find(node1) == self.find(node2)

    def get_connected_components(self):
        """
        获取所有连通分支
        """
        components = {}
        for node in self.parent:
            root = self.find(node)
            if root not in components:
                components[root] = []
            components[root].append(node)
        return components


class AugmentedKAryNCube:
    def __init__(self, n, k, r, h = 0):
        """
        初始化 Augmented k-ary n-cube

        :param n: 维度
        :param k: 基数
        :param r: 分支个数
        :param h: 分支中包含的最少节点数
        """
        self.n = n
        self.k = k
        self.r = r
        self.h = h
        self.nodes = list(product(range(k), repeat=n))  # 所有节点
        self.edges = self._generate_edges()  # 所有边
        self.node_states = {}  # 节点状态：fault-free 或 faulty

        self.set_node_states()
        self._build_union_find()

    def _generate_edges(self):
        """
        生成所有边
        """
        edges = set()
        for node in self.nodes:
            for i in range(self.n):
                # (i, ±1)-边
                neighbor_plus = self._get_neighbor(node, i, +1)
                neighbor_minus = self._get_neighbor(node, i, -1)
                if neighbor_plus:
                    edges.add(tuple(sorted([node, neighbor_plus])))
                if neighbor_minus:
                    edges.add(tuple(sorted([node, neighbor_minus])))
            for i in range(1, self.n):
                # (≤i, ±1)-边
                neighbor_plus = self._get_cascading_neighbor(node, i, +1)
                neighbor_minus = self._get_cascading_neighbor(node, i, -1)
                if neighbor_plus:
                    edges.add(tuple(sorted([node, neighbor_plus])))
                if neighbor_minus:
                    edges.add(tuple(sorted([node, neighbor_minus])))
        return list(edges)

    def _get_neighbor(self, node, i, direction):
        """
        获取 (i, ±1) 邻居
        """
        new_node = list(node)
        new_node[i] = (new_node[i] + direction) % self.k
        return tuple(new_node)

    def _get_cascading_neighbor(self, node, i, direction):
        """
        获取 (≤i, ±1) 邻居
        """
        new_node = list(node)
        for j in range(i + 1):
            new_node[j] = (new_node[j] + direction) % self.k
        return tuple(new_node)

    def set_node_states(self):
        """
        生成r-1个独立分支，每个分支包含h+1个无故障节点，
        并将这些节点的所有邻居设为故障节点
        """
        # 初始化所有节点为无故障
        for node in self.nodes:
            self.node_states[node] = "fault-free"

        # 存储已使用的核心节点
        used_cores = set()
        generated_branches = 0

        # 生成r-1个分支
        for _ in range(self.r - 1):
            # 获取可用无故障节点（排除已用核心节点）
            available_nodes = [n for n in self.nodes
                               if self.node_states[n] == "fault-free"
                               and n not in used_cores]

            # 终止条件检查
            if len(available_nodes) < self.h + 1:
                break

            # 随机选择种子节点
            start_node = random.choice(available_nodes)

            # BFS收集连通节点形成核心
            core = []
            queue = deque([start_node])
            visited = set()

            while queue and len(core) < self.h + 1:
                current = queue.popleft()
                if current in visited:
                    continue
                visited.add(current)
                core.append(current)
                used_cores.add(current)

                # 获取有效邻居
                neighbors = []
                # 单维邻居
                for i in range(self.n):
                    for d in [-1, 1]:
                        neighbor = self._get_neighbor(current, i, d)
                        if (self.node_states[neighbor] == "fault-free" and
                                neighbor not in used_cores):
                            neighbors.append(neighbor)
                # 多维邻居
                for i in range(1, self.n):
                    for d in [-1, 1]:
                        neighbor = self._get_cascading_neighbor(current, i, d)
                        if (self.node_states[neighbor] == "fault-free" and
                                neighbor not in used_cores):
                            neighbors.append(neighbor)

                # 添加未访问邻居到队列
                queue.extend([n for n in neighbors if n not in visited])

            # 有效性检查
            if len(core) < self.h + 1:
                # 回滚已标记的核心节点
                for n in core:
                    used_cores.remove(n)
                continue

            # 标记边界节点为故障
            fault_candidates = set()
            for node in core:
                # 单维边界
                for i in range(self.n):
                    for d in [-1, 1]:
                        neighbor = self._get_neighbor(node, i, d)
                        if neighbor not in core:
                            fault_candidates.add(neighbor)
                # 多维边界
                for i in range(1, self.n):
                    for d in [-1, 1]:
                        neighbor = self._get_cascading_neighbor(node, i, d)
                        if neighbor not in core:
                            fault_candidates.add(neighbor)

            # 设置故障状态
            for n in fault_candidates:
                if self.node_states[n] == "fault-free":
                    self.node_states[n] = "faulty"

            generated_branches += 1

        # 最终有效性验证
        if generated_branches < self.r - 1:
            print(f"警告：仅生成{generated_branches}个分支，目标{self.r - 1}个")

    def _build_union_find(self):
        """
        构建并查集
        只考虑无故障节点
        """
        start_time = time.time()  # 记录开始时间
        fault_free_nodes = [node for node, state in self.node_states.items()
                            if state == "fault-free"]
        self.uf = UnionFind(fault_free_nodes)

        for node1, node2 in self.edges:
            if (self.node_states[node1] == "fault-free" and
                    self.node_states[node2] == "fault-free"):
                self.uf.union(node1, node2)
        end_time = time.time()  # 记录结束时间
        self.uf_build_time = end_time - start_time  # 计算构建时间

    def print_branches(self):
        """
        打印所有连通分支
        """
        components = self.uf.get_connected_components()
        print("\n连通分支:")
        for root, nodes in components.items():
            print(f"分支 {root}: {nodes}")

    def are_connected(self, node1, node2):
        """
        检查两个节点是否连通（使用并查集）
        """
        if (self.node_states.get(node1) == "faulty" or
                self.node_states.get(node2) == "faulty"):
            return False
        return self.uf.connected(node1, node2)

    def get_source_sink_different_branches(self):
        """
        从不同的连通分支中选择 source 和 sink，
        source 来自最大的分支，sink 从剩余的分支中随机选择
        """
        components = self.uf.get_connected_components()
        branches = list(components.values())

        if len(branches) < 2:
            raise ValueError("无法从不同的分支中选择 source 和 sink")

        # 按照分支大小排序，选择最大的分支
        branches.sort(key=len, reverse=True)
        largest_branch = branches[0]  # 最大的分支
        other_branches = branches[1:]  # 其余分支

        # 选择 source
        source = random.choice(largest_branch)

        # 从剩余分支中选择一个分支，再选一个 sink
        chosen_branch = random.choice(other_branches)
        sink = random.choice(chosen_branch)

        return source, sink

    def get_source_sink_largest_branch(self):
        """
        从最大的连通分支中随机选择 source 和 sink，确保它们的坐标差异尽可能大
        """
        components = self.uf.get_connected_components()
        largest_branch = max(components.values(), key=len)

        if len(largest_branch) < 2:
            raise ValueError("最大分支节点数不足，无法选择两个不同的点")

        # 随机选取两个点
        candidates = random.sample(largest_branch, min(10, len(largest_branch)))  # 选取最多 10 个点进行比较
        best_pair = max(itertools.combinations(candidates, 2),
                        key=lambda pair: sum(abs(a - b) for a, b in zip(pair[0], pair[1])))

        return best_pair

    def find_fault_free_path(self, start, end):
        """
        结合改进的贪心策略和 BFS，在 AQn,k 拓扑中查找无故障路径
        (修正版本，符合HGBRouting算法描述)
        """
        if (self.node_states.get(start) == "faulty" or
                self.node_states.get(end) == "faulty"):
            return False, [], 0, False

        if not self.are_connected(start, end):  # 快速连通性检查
            return False, [], 0, False

        start_time = time.time()
        path = [start]
        current = start

        # 贪心阶段：优先使用多维度跳转
        while current != end:
            # 计算差异维度并降序排序
            diff_dims = [i for i in range(self.n) if current[i] != end[i]]
            diff_dims.sort(reverse=True)  # 按维度降序

            found_next = False

            # 遍历所有差异维度
            for i in diff_dims:
                # 计算最佳方向
                delta = (end[i] - current[i]) % self.k
                direction = +1 if delta <= self.k // 2 else -1

                # 生成两种候选邻居
                single_neighbor = self._get_neighbor(current, i, direction)
                multi_neighbor = self._get_cascading_neighbor(current, i, direction)

                # 筛选有效邻居并计算距离
                valid_neighbors = []

                # 检查单维度邻居
                if (single_neighbor in self.node_states and
                        self.node_states[single_neighbor] == "fault-free"):
                    single_diff = sum(
                        min(abs(single_neighbor[d] - end[d]),
                            self.k - abs(single_neighbor[d] - end[d]))
                        for d in range(self.n))
                    valid_neighbors.append((single_diff, False, single_neighbor))

                # 检查多维度邻居
                if (multi_neighbor in self.node_states and
                        self.node_states[multi_neighbor] == "fault-free"):
                    multi_diff = sum(
                        min(abs(multi_neighbor[d] - end[d]),
                            self.k - abs(multi_neighbor[d] - end[d]))
                        for d in range(self.n))
                    valid_neighbors.append((multi_diff, True, multi_neighbor))

                if not valid_neighbors:
                    continue

                # 排序规则：优先距离小，距离相同则多维度优先
                valid_neighbors.sort(key=lambda x: (x[0], not x[1]))

                # 选择最优邻居
                best_diff, is_multi, best_neighbor = valid_neighbors[0]
                path.append(best_neighbor)
                current = best_neighbor
                found_next = True
                break  # 处理下一个节点

            if not found_next:
                break  # 贪心策略失败

        # 检查是否成功到达
        if current == end:
            return True, path, time.time() - start_time, False

        # BFS阶段：完成剩余路径
        bfs_success, bfs_path, bfs_time = self.bfs(current, end)

        if bfs_success:
            path += bfs_path[1:]  # 去掉重复的当前节点
            return True, path, time.time() - start_time, True

        return False, [], time.time() - start_time, False

    def dfs_recursive(self, start, end):
        """
        使用DFS查找两个无故障节点之间是否存在无故障路径

        :param start: 起始节点
        :param end: 目标节点
        :return: (是否存在路径, 路径列表, 搜索时间)
        """
        if (self.node_states.get(start) == "faulty" or
                self.node_states.get(end) == "faulty"):
            return False, [], 0

        start_time = time.time()
        visited = set()
        path = []

        def dfs_helper(current, target, current_path):
            if current == target:
                path.extend(current_path)
                return True

            visited.add(current)

            # 获取所有无故障邻居节点
            for i in range(self.n):
                for direction in [-1, 1]:
                    neighbor = self._get_neighbor(current, i, direction)
                    if (neighbor not in visited and
                            self.node_states.get(neighbor) == "fault-free"):
                        if dfs_helper(neighbor, target, current_path + [neighbor]):
                            return True
            for i in range(1, self.n):
                for direction in [-1, 1]:
                    neighbor = self._get_cascading_neighbor(current, i, direction)
                    if (neighbor not in visited and
                            self.node_states.get(neighbor) == "fault-free"):
                        if dfs_helper(neighbor, target, current_path + [neighbor]):
                            return True

            return False

        found = dfs_helper(start, end, [start])
        end_time = time.time()
        search_time = end_time - start_time

        return found, path, search_time

    def dfs(self, start, end):
        """
        使用非递归 DFS 查找两个无故障节点之间是否存在无故障路径

        :param start: 起始节点
        :param end: 目标节点
        :return: (是否存在路径, 路径列表, 搜索时间)
        """
        if (self.node_states.get(start) == "faulty" or
                self.node_states.get(end) == "faulty"):
            return False, [], 0

        start_time = time.time()
        stack = [(start, [start])]  # 栈中存储 (当前节点, 当前路径)
        visited = set()

        while stack:
            current, path = stack.pop()
            if current in visited:
                continue
            visited.add(current)

            if current == end:
                return True, path, round(time.time() - start_time, 6)

            # 获取所有无故障邻居节点（优先入栈的会后出，模拟递归的搜索顺序）
            neighbors = []
            for i in range(self.n):
                for direction in [-1, 1]:
                    neighbor = self._get_neighbor(current, i, direction)
                    if neighbor not in visited and self.node_states.get(neighbor) == "fault-free":
                        neighbors.append((neighbor, path + [neighbor]))

            for i in range(1, self.n):
                for direction in [-1, 1]:
                    neighbor = self._get_cascading_neighbor(current, i, direction)
                    if neighbor not in visited and self.node_states.get(neighbor) == "fault-free":
                        neighbors.append((neighbor, path + [neighbor]))

            # 逆序入栈，确保搜索顺序和递归一致
            stack.extend(reversed(neighbors))

        return False, [], round(time.time() - start_time, 6)

    def bfs(self, start, end):
        """
        使用BFS查找两个无故障节点之间是否存在无故障路径

        :param start: 起始节点
        :param end: 目标节点
        :return: (是否存在路径, 路径列表, 搜索时间)
        """
        if (self.node_states.get(start) == "faulty" or
                self.node_states.get(end) == "faulty"):
            return False, [], 0

        start_time = time.time()

        visited = {start}
        queue = deque([(start, [start])])

        while queue:
            current, path = queue.popleft()

            if current == end:
                end_time = time.time()
                search_time = end_time - start_time
                return True, path, search_time

            # 获取所有无故障邻居节点
            for i in range(self.n):
                for direction in [-1, 1]:
                    neighbor = self._get_neighbor(current, i, direction)
                    if (neighbor not in visited and
                            self.node_states.get(neighbor) == "fault-free"):
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))
            for i in range(1, self.n):
                for direction in [-1, 1]:
                    neighbor = self._get_cascading_neighbor(current, i, direction)
                    if (neighbor not in visited and
                            self.node_states.get(neighbor) == "fault-free"):
                        visited.add(neighbor)
                        queue.append((neighbor, path + [neighbor]))

        end_time = time.time()
        search_time = end_time - start_time
        return False, [], search_time

    def test_connectivity_methods(self, node1, node2):
        """
        测试并比较三种连通性检查方法
        """
        # 1. 测试并查集方法
        start_time = time.time()
        uf_connected = self.are_connected(node1, node2)
        uf_time = time.time() - start_time

        # 2. 测试DFS
        dfs_connected, dfs_path, dfs_time = self.dfs(node1, node2)

        # 3. 测试BFS
        bfs_connected, bfs_path, bfs_time = self.bfs(node1, node2)

        # 4. 测试 find_fault_free_path
        fffp_connected, fffp_path, fffp_time, used_bfs = self.find_fault_free_path(node1, node2)

        # 打印结果
        print(f"\n测试节点 {node1} 到 {node2} 的连通性:")
        print(f"并查集结果: {'连通' if uf_connected else '不连通'}, 耗时: {uf_time:.6f}秒")
        print(f"DFS结果: {'连通' if dfs_connected else '不连通'}, 耗时: {dfs_time:.6f}秒")
        if dfs_connected:
            print(f"DFS路径: {' -> '.join(map(str, dfs_path))}")
        print(f"BFS结果: {'连通' if bfs_connected else '不连通'}, 耗时: {bfs_time:.6f}秒")
        if bfs_connected:
            print(f"BFS路径: {' -> '.join(map(str, bfs_path))}")
        print(f"FFFP结果: {'连通' if fffp_connected else '不连通'}, 耗时: {fffp_time:.6f}秒")
        if fffp_connected:
            print(f"FFFP路径: {' -> '.join(map(str, fffp_path))} "
                  f"{'(BFS used)' if used_bfs else '(Greedy used)'}")

    def print_node_states(self):
        """
        打印无故障顶点和故障顶点
        """
        fault_free_nodes = [node for node, state in self.node_states.items()
                            if state == "fault-free"]
        faulty_nodes = [node for node, state in self.node_states.items()
                        if state == "faulty"]

        print("无故障顶点:")
        print(fault_free_nodes)
        print("故障顶点:")
        print(faulty_nodes)

    def visualize(self, layout="circular", figsize=(10, 10), node_size=200, font_size=8):
        """
        可视化Augmented k-ary n-cube

        :param layout: 布局类型，可选 "spring", "spectral", "kamada_kawai", "fruchterman_reingold", "circular"
        :param figsize: 图像大小
        :param node_size: 节点大小
        :param font_size: 节点标签字体大小
        """
        # 创建NetworkX图
        G = nx.Graph()
        G.add_nodes_from(self.nodes)
        G.add_edges_from(self.edges)

        # 选择布局
        if layout == "circular":
            pos = nx.circular_layout(G)
        elif layout == "spring":
            pos = nx.spring_layout(G)
        elif layout == "spectral":
            pos = nx.spectral_layout(G)
        elif layout == "kamada_kawai":
            pos = nx.kamada_kawai_layout(G)
        elif layout == "fruchterman_reingold":
            pos = nx.fruchterman_reingold_layout(G)
        else:
            raise ValueError(f"未知布局类型: {layout}")

        # 绘制图
        plt.figure(figsize=figsize)

        normal_nodes = set(node for node, state in self.node_states.items() if state == "fault-free")
        fault_nodes = set(node for node, state in self.node_states.items() if state == "faulty")

        # 绘制正常顶点
        nx.draw_networkx_nodes(G, pos, nodelist=normal_nodes, node_size=node_size, node_color="lightblue")
        # 绘制故障顶点
        nx.draw_networkx_nodes(G, pos, nodelist=fault_nodes, node_size=node_size, node_color="red")
        # 绘制边
        nx.draw_networkx_edges(G, pos, edge_color="gray")
        # 绘制节点标签
        nx.draw_networkx_labels(G, pos, font_size=font_size)

        plt.title(f"Augmented {self.k}-ary {self.n}-cube ({layout} layout)")
        plt.show()

# if __name__ == "__main__":
#     run_experiment(n=2, k=4, r=2, source_sink_from_different_branches=True)