import matrix
import graph
import itertools as it
import numpy as np


def judge_trivial_graph(g):
    if len(g.nodes) == 1 and len(g.edges) == 0:
        return "是平凡图"
    else:
        return "不是平凡图"


def judge_bipartite_graph(g):
    if g.directional:
        return "无法判断有向图的二分图"
    else:
        # 先去除无边的节点，不用判断，若为零图，直接返回是二分图
        nodes_with_edge = []
        for _node in g.nodes:
            if g.nodes[_node].neighbors:
                nodes_with_edge.append(_node)
        if len(nodes_with_edge) == 0:
            return "是二分图(零图)"
        # 初始化染色图，0代表为染色，1代表染成黑色，-1代表染成白色
        colors = {_node:0 for _node in nodes_with_edge}
        for i, current_node in enumerate(colors.keys()):
            def dfs_dye(_node, _color):
                colors[_node] = _color
                current_neighbors = g.nodes[_node].neighbors
                for _child_node in current_neighbors:
                    if colors[_child_node] == colors[_node]:
                        return False
                    elif colors[_child_node] == 0 and not dfs_dye(_child_node, -colors[_node]):
                        return False
                return True
            if colors[current_node] == 0:
                state = dfs_dye(current_node, 1)
                if not state:
                    return "不是二分图"
        black_list = []
        white_list = []
        for node, col in colors.items():
            if col == 1:
                black_list.append(node)
            if col == -1:
                white_list.append(node)
        return "是二分图"


def judge_euler_graph(g):
    if g.directional:
        # 有向图是否是欧拉通路欧拉回路的判断
        starting_point = []
        for node in g.nodes:
            in_degree = len(g.nodes[node].from_neighbors)
            out_degree = len(g.nodes[node].to_neighbors)
            if out_degree == 0 or in_degree == 0:
                return "不是欧拉通（回）路"
            else:
                if out_degree != in_degree:
                    if out_degree - in_degree == 1 or in_degree - out_degree == 1:
                        starting_point.append(node)
                    else:
                        return "不是欧拉通（回）路"
                    if len(starting_point) > 2:
                        return "不是欧拉通（回）路"
        if len(starting_point) == 0:
            return "是欧拉回路"
        elif len(starting_point) == 1:
            return "不是欧拉通（回）路"
        elif len(starting_point) == 2:
            return "是欧拉通路"
    else:
        # 无向图是否是欧拉通路欧拉回路的判断
        starting_point = []
        for node in g.nodes:
            degrees = len(g.nodes[node].neighbors)
            if degrees == 0:
                return "不是欧拉通（回）路"
            elif degrees % 2 == 1:
                starting_point.append(node)
                if len(starting_point) > 2:
                    return "不是欧拉通（回）路"
            else:
                continue
        if len(starting_point) == 0:
            return "是欧拉回路"
        elif len(starting_point) == 1:
            return "不是欧拉通（回）路"
        elif len(starting_point) == 2:
            return "是欧拉通路"


def judge_tongpei_k5(g):
    graph_k5 = graph.Graph(directional=False)
    graph_k5.add_node('a')
    graph_k5.add_node('b')
    graph_k5.add_node('c')
    graph_k5.add_node('d')
    graph_k5.add_node('e')
    graph_k5.add_relation(('a', 'c'))
    graph_k5.add_relation(('a', 'd'))
    graph_k5.add_relation(('b', 'd'))
    graph_k5.add_relation(('b', 'e'))
    graph_k5.add_relation(('c', 'e'))
    mat_k5 = matrix.adjacency_mat(graph_k5, directional=False)
    mat_g = matrix.adjacency_mat(g, directional=False)
    boolen1 = len(g.nodes) == 5
    boolen2 = len(g.edges) == 5
    if all([boolen1, boolen2]):
        boolen3 = np.sum(mat_g, axis=1) == np.sum(mat_k5, axis=1)
        boolen4 = np.sum(mat_g, axis=0) == np.sum(mat_k5, axis=0)
        boolen31 = all(boolen3.tolist())
        boolen41 = all(boolen4.tolist())
        if all([boolen31, boolen41]):
            return True
        else:
            return False
    else:
        return False


def judge_tongpei_k33(g):
    graph_k33 = graph.Graph(directional=False)
    graph_k33.add_node('a')
    graph_k33.add_node('b')
    graph_k33.add_node('c')
    graph_k33.add_node('d')
    graph_k33.add_node('e')
    graph_k33.add_node('f')
    graph_k33.add_relation(('a', 'd'))
    graph_k33.add_relation(('a', 'e'))
    graph_k33.add_relation(('a', 'f'))
    graph_k33.add_relation(('b', 'd'))
    graph_k33.add_relation(('b', 'e'))
    graph_k33.add_relation(('b', 'f'))
    graph_k33.add_relation(('c', 'd'))
    graph_k33.add_relation(('c', 'e'))
    graph_k33.add_relation(('c', 'f'))
    mat_k33 = matrix.adjacency_mat(graph_k33, directional=False)
    mat_g = matrix.adjacency_mat(g, directional=False)
    boolen1 = len(g.nodes) == 6
    boolen2 = len(g.edges) == 9
    if all([boolen1, boolen2]):
        boolen3 = np.sum(mat_g, axis=1) == np.sum(mat_k33, axis=1)
        boolen4 = np.sum(mat_g, axis=0) == np.sum(mat_k33, axis=0)
        boolen31 = all(boolen3.tolist())
        boolen41 = all(boolen4.tolist())
        if all([boolen31, boolen41]):
            return True
        else:
            return False
    else:
        return False


def judge_planer_graph(g):
    if not g.directional:
        total_node = len(g.nodes)
        if total_node <= 4:
            return "是平面图"
        for n_subnode in range(5, total_node+1):
            for subnodes in it.combinations(g.nodes, n_subnode):
                subnodes = set(subnodes)
                subgraph = g.subgraph(subnodes)
                if n_subnode == 5:
                    if judge_tongpei_k5(subgraph):
                        return "不是平面图"
                else:
                    if judge_tongpei_k33(subgraph):
                        return "不是平面图"
                    if judge_tongpei_k5(subgraph):
                        return "不是平面图"
        return "是平面图"
    else:
        return "无法判断有向图的平面图"
