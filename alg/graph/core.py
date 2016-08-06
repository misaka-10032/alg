# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Base classes for graph.
"""

import numpy as np
from collections import deque
from ..core import Node, print_node
from ..heap import MinHeap


class Vertex(Node):
    def __init__(self, key, value=None):
        super(Vertex, self).__init__(key, value)
        self.root = None
        self.level = None
        self.tin = None
        self.tout = None

    def __repr__(self):
        ret = super(Vertex, self).__repr__()
        ret += '\tlevel: %s\n' % self.level
        ret += '\ttin: %s\n' % self.tin
        ret += '\ttout: %s\n' % self.tout
        return ret


class Edge(object):
    def __init__(self, start, end, weight=None):
        """
        :param start: start vertex (u)
        :param end: end vertex (v)
        :param weight: can be anything that impls __cmp__
        """
        self.start = start if isinstance(start, Vertex) else Vertex(start)
        self.end = end if isinstance(end, Vertex) else Vertex(end)
        self.weight = weight or 1

    def __cmp__(self, other):
        if isinstance(other, Edge):
            return cmp((self.start, self.end), (other.start, other.end))
        else:
            return False

    def __repr__(self):
        return '%s\n\tFrom: %s\n\tTo: %s\n\tWeight: %s\n' % \
               (super(Edge, self).__repr__(), self.start, self.end, self.weight)


class Graph(object):
    ORDER_BFS = 'bfs'
    ORDER_DFS = 'dfs'

    def __init__(self, V=None, E=None):
        """ Constructor """
        """ V is dict with both key and val as vertex """
        # It's designed to be dict for fast lookup by key.
        self.V = V or {}
        """ E is dict with vertex as key and list of edges as val. """
        self.E = E or {}

    def clear(self):
        """ Clear the graph """
        self.V = {}
        self.E = {}

    def reset_intermediates(self):
        for node in self.V.itervalues():
            node.root = None
            node.level = None
            node.tin = None
            node.tout = None

    def search_vertex(self, vertex):
        if vertex in self.V:
            return self.V[vertex]
        else:
            return None

    def add_vertex(self, vertex):
        """
        Insert a vertex if not exists. Otherwise return the existing one.
        :param vertex:
        :return:
        """
        if vertex not in self.V:
            vertex = vertex if isinstance(vertex, Vertex) else Vertex(vertex)
            self.V[vertex] = vertex
            self.E[vertex] = []
            return vertex
        else:
            return self.V[vertex]

    def remove_vertex(self, vertex):
        """
        :param vertex: can either be key or vertex, as long as key matches.
        :return: vertex, [edges]
        """
        if vertex in self.V:
            vertex = self.V.pop(vertex)
            return vertex, self.E.pop(vertex)
        else:
            return None, None

    def add_edge(self, edge):
        """
        Insert an edge. Duplicate edge may lead to weird behavior.
        :param edge:
        :type edge: Edge
        :return:
        """
        edge.start = self.add_vertex(edge.start)
        edge.end = self.add_vertex(edge.end)
        self.E[edge.start].append(edge)
        return edge

    def remove_edge(self, edge):
        """
        :param edge:
        :type edge: Edge
        :return:
        """
        i = 0
        found = False
        edges = self.E[edge.start]
        for eit in edges:
            if edge == eit:
                found = True
                break
            i += 1
        return edges.pop(i) if found else None

    def traverse(self, order=ORDER_BFS,
                 func_in=print_node, func_out=None, func_edge=None):
        """
        :param order: either ORDER_BFS or ORDER_DFS
        :param func_in: func_in(Node)
        :param func_out: func_out(Node)
        :param func_edge: func_edge(Edge)
        :return:
        """
        self.reset_intermediates()
        for start in self.V.itervalues():
            if not start.level:
                if order == self.ORDER_BFS:
                    start.root = start
                    start.level = 0
                    self.bfs(start, False, 0, func_in, func_out, func_edge)
                elif order == self.ORDER_DFS:
                    start.root = start
                    start.level = 0
                    self.dfs(start, False, 0, func_in, func_out, func_edge)
                else:
                    raise Exception("Order should be either ORDER_BFS or ORDER_DFS")

    def bfs(self, start, reset=True, timer=0,
            func_in=print_node, func_out=None, func_edge=None):
        """
        Breadth first search
        :param start:
        :param reset:
        :param timer:
        :param func_in:
        :param func_out:
        :param func_edge:
        :return: the updated timer
        """
        start = self.search_vertex(start)
        if reset:
            self.reset_intermediates()
            start.root = start
            start.level = 0
        start.tin = timer
        timer += 1
        if func_in:
            func_in(start)
        queue = deque()
        queue.append(start)
        while queue:
            old = queue.popleft()
            old.tout = timer
            timer += 1
            if func_out:
                func_out(old)
            edges = self.E[old]
            for edge in edges:
                new = edge.end
                if not new.level:
                    if func_edge:
                        func_edge(edge)
                    new.root = old.root
                    new.level = old.level + 1
                    new.tin = timer
                    if func_in:
                        func_in(new)
                    queue.append(new)
                    timer += 1
        return timer

    def dfs(self, start, reset=True, timer=0,
            func_in=print_node, func_out=None, func_edge=None):
        """
        Depth first search
        :param start:
        :param reset:
        :param timer:
        :param func_in:
        :param func_out:
        :param func_edge:
        :return: updated timer
        """
        start = self.search_vertex(start)
        if reset:
            self.reset_intermediates()
            start.root = start
            start.level = 0
        start.tin = timer
        timer += 1
        if func_in:
            func_in(start)
        edges = self.E[start]
        for edge in edges:
            new = edge.end
            if not new.level:
                if func_edge:
                    func_edge(edge)
                new.root = start.root
                new.level = start.level + 1
                timer = self.dfs(new, False, timer,
                                 func_in, func_out, func_edge)
        start.tout = timer
        timer += 1
        if func_out:
            func_out(start)
        return timer

    def cyclic(self, traverse=True):
        if traverse:
            self.traverse(self.ORDER_DFS, func_in=None)
        for edges in self.E.itervalues():
            for edge in edges:
                if edge.start.root != edge.end.root:
                    continue
                if edge.end.tin < edge.start.tin and \
                   edge.end.tout > edge.start.tout:
                    return True
        return False

    def back_edges(self, traverse=True):
        ret = []
        if traverse:
            self.traverse(self.ORDER_DFS, func_in=None)
        for edges in self.E.itervalues():
            for edge in edges:
                if edge.start.root != edge.end.root:
                    continue
                if edge.end.tin < edge.start.tin and \
                   edge.end.tout > edge.start.tout:
                    ret.append(edge)
        return ret

    def sptree(self, order=ORDER_BFS):
        tree = Graph(self.V, {})
        for vertex in tree.V:
            tree.E[vertex] = []
        self.traverse(order=order, func_in=None,
                      func_edge=lambda edge: tree.add_edge(edge))
        return tree

    def topological(self):
        order = []
        self.traverse(order=self.ORDER_DFS, func_in=None,
                      func_out=lambda vertex: order.append(vertex))
        if self.cyclic(traverse=False):
            raise Exception("Graph is cyclic!")
        order.reverse()
        return order

    def _relax(self, d, p, edge):
        if d[edge.start] + edge.weight < d[edge.end]:
            d[edge.end] = d[edge.start] + edge.weight
            p[edge.end] = edge.start
            return True
        else:
            return False

    def dijkstra(self, src):
        """ Returns d[V], p[V], which are distances and predecessors """
        src = self.search_vertex(src)
        # check non-negative weights
        for u, edges in self.E.iteritems():
            for e in edges:
                assert e.weight >= 0
        d, p = {}, {}
        for v in self.V.keys():
            d[v] = np.inf
            p[v] = None
        d[src] = 0
        S = set()

        # maps from vertex to heap_node
        hnodes = {v: Node(d[v], v) for v in self.V.keys()}
        R = MinHeap(hnodes.values(), modifiable=True)
        while R:
            u = R.pop().value
            S.add(u)
            for e in self.E[u]:
                if self._relax(d, p, e):
                    R.update(hnodes[e.end], d[e.end])
        return d, p

    def bellmanford(self, src):
        src = self.search_vertex(src)
        d, p = {}, {}
        for v in self.V.keys():
            d[v] = np.inf
            p[v] = None
        d[src] = 0
        for _ in xrange(len(self.V)-1):
            for edges in self.E.itervalues():
                for e in edges:
                    self._relax(d, p, e)
        for _ in xrange(len(self.V)):
            for edges in self.E.itervalues():
                for e in edges:
                    if self._relax(d, p, e):
                        d[e.end] = -np.inf
        return d, p
