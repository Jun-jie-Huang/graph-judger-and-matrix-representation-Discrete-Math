import copy
import matrix
import numpy as np


class Node:

    def __init__(self, name, idx):

        self.name = name
        self.idx = idx
        self.neighbors = []
        self.to_neighbors = []
        self.from_neighbors = []

    def add_neighbor(self, neighbor_name):
        self.neighbors.append(neighbor_name)

    def __str__(self):
        return "Node object:" + self.name + ",id:{}".format(self.idx)


class Edge:

    def __init__(self, left_node, right_node, weight=1, directional=False):

        self.left_node = left_node
        self.right_node = right_node
        self.weight = weight
        self.directional = directional

    def set_weight(self, weight):
        self.weight = weight

    def __str__(self):
        return "Edge object: " + str(self.left_node) + ' >> ' + str(self.right_node)

    # def __iter__(self):
    #     return self


class Graph:
    """
        默认节点从左至右，默认创建无向图
    """
    def __init__(self, directional=False):
        self.nodes = dict()
        self.node2idx = dict()
        self.idx2node = dict()
        self.edges = dict()
        self.directional = directional

    def add_node(self, node_name):
        idx = len(self.nodes)
        nodei = Node(node_name, idx)
        self.nodes[node_name] = nodei
        self.node2idx[node_name] = idx
        self.idx2node[idx] = node_name

    def add_edge(self, left_node, right_node, edgename=None, weight=1):
        edgei = Edge(left_node, right_node, weight)
        if not edgename:
            edgename = len(self.edges)
            if len(self.edges) in self.edges:
                edgename = max(self.edges.keys()) + 1
            self.edges[edgename] = edgei
        else:
            self.edges[edgename] = edgei
        self.nodes[left_node].to_neighbors.append(right_node)
        self.nodes[right_node].from_neighbors.append(left_node)
        if left_node != right_node:
            self.nodes[left_node].neighbors.append(right_node)
            self.nodes[right_node].neighbors.append(left_node)
        else:
            self.nodes[left_node].neighbors.append(left_node)

    def add_relation(self, relation_tuple):
        l_node = relation_tuple[0]
        r_node = relation_tuple[1]
        if l_node not in self.nodes:
            self.add_node(l_node)
        if r_node not in self.nodes:
            self.add_node(r_node)
        self.add_edge(l_node, r_node)

    def add_weighted_relation(self):
        pass

    def subgraph(self, nodes_set):
        _subgraph = Graph(directional=False)
        for sub_node in nodes_set:
            _subgraph.add_node(sub_node)
        for edge in self.edges:
            if self.edges[edge].left_node in nodes_set and self.edges[edge].right_node in nodes_set:
                _subgraph.add_relation((self.edges[edge].left_node, self.edges[edge].right_node))
        return _subgraph

    def remove_two_degree_v(self):
        adja_mat = matrix.adjacency_mat(self, directional=self.directional)
        nodeidx2move = np.argwhere(np.sum(adja_mat,axis=1)==2)
        if len(nodeidx2move) == 0:
            # 如果无2度顶点，直接返回原图
            return self
        rm_nodes = [self.idx2node[nodeidx2move[idx][0]] for idx in range(len(nodeidx2move))]
        rm_edges = []
        for node_name in rm_nodes:
            neighbor1 = self.nodes[node_name].neighbors[0]
            neighbor2 = self.nodes[node_name].neighbors[1]
            for edge_id in self.edges:
                boolen1 = neighbor1 == self.edges[edge_id].left_node and node_name == self.edges[edge_id].right_node
                boolen2 = neighbor2 == self.edges[edge_id].left_node and node_name == self.edges[edge_id].right_node
                if boolen1 or boolen2:
                    rm_edges.append(edge_id)
                boolen3 = node_name == self.edges[edge_id].left_node and neighbor1 == self.edges[edge_id].right_node
                boolen4 = node_name == self.edges[edge_id].left_node and neighbor2 == self.edges[edge_id].right_node
                if boolen3 or boolen4:
                    rm_edges.append(edge_id)
            self.edges.pop(rm_edges[0])
            self.edges.pop(rm_edges[1])
            self.add_relation((neighbor1, neighbor2))
            self.nodes.pop(node_name)
            self.idx2node.pop(self.node2idx.pop(node_name))


if __name__ == '__main__':
    graph = Graph(directional=False)
    # graph.add_node('n1')
    # graph.add_node('n2')
    # graph.add_node('n3')

