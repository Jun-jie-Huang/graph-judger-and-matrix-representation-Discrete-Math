import numpy as np
import graph as g


def incidence_mat(graph, directional=False):
    n = len(graph.nodes)
    m = len(graph.edges)
    i_mat = np.zeros([n, m], dtype=np.int32)
    if not directional:
        # 获得无向图的关联矩阵
        for node in graph.nodes:
            for edge_id in graph.edges:
                i = graph.node2idx[node]
                j = edge_id
                if node == graph.edges[edge_id].left_node or node == graph.edges[edge_id].right_node:
                    if graph.edges[edge_id].left_node != graph.edges[edge_id].right_node:
                        i_mat[i][j] = 1
                    else:
                        i_mat[i][j] = 2
        assert(np.sum(np.sum(i_mat, axis=1), axis=0) == 2*m)
    else:
        # 获得有向无环图的关联矩阵
        for node in graph.nodes:
            for edge_id in graph.edges:
                i = graph.node2idx[node]
                j = edge_id
                if node == graph.edges[edge_id].left_node or node == graph.edges[edge_id].right_node:
                    if graph.edges[edge_id].left_node == node:
                        i_mat[i][j] = 1
                    elif graph.edges[edge_id].right_node == node:
                        i_mat[i][j] = -1
        assert(np.sum(np.sum(i_mat, axis=1), axis=0) == 0)
    return i_mat


def adjacency_mat(graph, directional=True):
    n = len(graph.nodes)
    a_mat = np.zeros([n, n], dtype=np.int32)
    if directional:
        # 获的有向图的邻接矩阵
        for vi in graph.nodes:
            for vj in graph.nodes:
                i = graph.node2idx[vi]
                j = graph.node2idx[vj]
                for edge_id in graph.edges:
                    if vi == graph.edges[edge_id].left_node and vj == graph.edges[edge_id].right_node:
                        a_mat[i][j] += 1
    else:
        # 无向图的相邻矩阵
        for i, vi in enumerate(graph.nodes.keys()):
            for j, vj in enumerate(graph.nodes.keys()):
                for edge_id in graph.edges:
                    if vi != vj:
                        if vi == graph.edges[edge_id].left_node and vj == graph.edges[edge_id].right_node:
                            a_mat[i][j] = 1
                            a_mat[j][i] = 1
    return a_mat


def reacheable_mat(graph, directional=True):
    n = len(graph.nodes)
    r_mat = np.eye(n, dtype=np.int32)
    b_mat = np.zeros([n, n], dtype=np.int32)

    # 用定理6.18计算矩阵B = A^1 + A^2 + A^3 + ......
    # 有向图的可达矩阵和无向图的连通矩阵算法相同
    A = adjacency_mat(graph, directional)
    A_list = [A]
    for i in range(n-2):
        A_list.append(np.dot(A_list[i], A))
    for _A in A_list:
        b_mat += _A
    r_mat += b_mat
    for i in range(n):
        for j in range(n):
            if r_mat[i][j] != 0:
                r_mat[i][j] = 1
    return r_mat


def mat2str(matrix):
    m, n = matrix.shape
    string = " "
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == -1:
                string = string[:-1] + str(matrix[i][j]) + '   '
            else:
                string += (str(matrix[i][j]) + '   ')
        string+='\n '
    return string

