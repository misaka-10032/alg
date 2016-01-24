# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Tests for graph.
"""
__author__ = 'misaka-10032'

from . import Graph, Edge


def test_traverse():
    g = Graph()
    g.insert_edge(Edge(1, 2))
    g.insert_edge(Edge(1, 3))
    g.insert_edge(Edge(2, 4))
    g.insert_edge(Edge(2, 5))
    g.insert_edge(Edge(5, 3))
    g.insert_vertex(6)
    """ Test bfs """
    trace = []
    g.bfs(1, func_in=lambda vertex: trace.append(vertex))
    assert trace == [1, 2, 3, 4, 5]
    """ Test dfs """
    trace = []
    g.dfs(1, func_in=lambda vertex: trace.append(vertex))
    assert trace == [1, 2, 4, 5, 3]
    """ Test traverse """
    trace = []
    g.traverse(order=g.ORDER_BFS, func_in=lambda vertex: trace.append(vertex))
    assert trace == [1, 2, 3, 4, 5, 6]
    """ Test cyclic """
    g.insert_edge(Edge(3, 2))
    assert g.cyclic()
    """ Test acyclic """
    g.remove_edge(Edge(3, 2))
    assert not g.cyclic()
    """ Test topological sort """
    assert g.topological() == [6, 1, 2, 5, 3, 4]
    # TODO: test sptree
