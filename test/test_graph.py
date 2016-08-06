# encoding: utf-8
"""
Created by misaka-10032 (longqic@andrew.cmu.edu).
All rights reserved.

Tests for graph.
"""

import numpy as np
from alg.graph import Graph, Edge


def test_traverse():
    g = Graph()
    g.add_edge(Edge(1, 2))
    g.add_edge(Edge(1, 3))
    g.add_edge(Edge(2, 4))
    g.add_edge(Edge(2, 5))
    g.add_edge(Edge(5, 3))
    g.add_vertex(6)
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
    g.add_edge(Edge(3, 2))
    assert g.cyclic()
    """ Test acyclic """
    g.remove_edge(Edge(3, 2))
    assert not g.cyclic()
    """ Test topological sort """
    assert g.topological() == [6, 1, 2, 5, 3, 4]
    """ Test sptree """
    assert not g.sptree().cyclic()


def test_sssp():
    # sssp = single source shortest path
    # CLRS(2009) p659
    g = Graph()
    g.add_edge(Edge('s', 't', 10))
    g.add_edge(Edge('s', 'y', 5))
    g.add_edge(Edge('t', 'y', 2))
    g.add_edge(Edge('t', 'x', 1))
    g.add_edge(Edge('x', 'z', 4))
    g.add_edge(Edge('z', 'x', 6))
    g.add_edge(Edge('z', 's', 7))
    g.add_edge(Edge('y', 't', 3))
    g.add_edge(Edge('y', 'x', 9))
    g.add_edge(Edge('y', 'z', 2))
    d, p = g.dijkstra('s')
    assert d['s'] == 0 and p['s'] is None
    assert d['t'] == 8 and p['t'] == 'y'
    assert d['x'] == 9 and p['x'] == 't'
    assert d['z'] == 7 and p['z'] == 'y'
    assert d['y'] == 5 and p['y'] == 's'
    d, p = g.bellmanford('s')
    assert d['s'] == 0 and p['s'] is None
    assert d['t'] == 8 and p['t'] == 'y'
    assert d['x'] == 9 and p['x'] == 't'
    assert d['z'] == 7 and p['z'] == 'y'
    assert d['y'] == 5 and p['y'] == 's'


def test_bellmanford():
    g = Graph()
    g.add_edge(Edge('a', 'x', 1))
    g.add_edge(Edge('x', 'y', -1))
    g.add_edge(Edge('y', 'z', -1))
    g.add_edge(Edge('z', 'x', -1))
    d, p = g.bellmanford('a')
    assert d['a'] == 0 and p['a'] is None
    assert d['x'] == -np.inf and p['x'] == 'z'
    assert d['y'] == -np.inf and p['y'] == 'x'
    assert d['z'] == -np.inf and p['z'] == 'y'
