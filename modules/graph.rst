.. module:: graph

++++++++++++++
graph
++++++++++++++

Graph provides predicates on relations over a parameterized signature.

::

  open util/graph[Node]

  sig Node {
    edge: set Node
  }

  run {
    dag[edge]
  }

Notice that graph is parameterized on the **signature**, but the predicate takes in a **relation**. This is so that you can apply multiple predicates to multiple different relations, or different subsets of the same relation. The graph module uses some specific terminology:

This means that in a completely unconnected graph, every node is both a root and a leaf.

Functions
---------


.. als:function:: roots[r: node-> node]

  :rtype: ``set Node``

  Returns the set of nodes that *are not connected to* by any other node.

  .. warning:: this is *not* the same meaning of *root* as in the `rootedAt` predicate! For the predicate, a *root* is a node that transitively covers the whole graph. Interally, ``util/graph`` uses ``rootedAt`` and not ``roots``.

.. als:function:: leaves[r: node-> node]

  :rtype: ``set Node``

  Returns the set of nodes that *do not connect to* any other node.

  .. note:: If ``r`` is empty, ``roots[r] = leaves[r] = Node``. If ``r`` is undirected or contains enough self loops, ``roots[r] = leaves[r] =``  `none`.


.. als:function:: innerNodes[r: node-> node]

  :return: All nodes that aren't leaves
  :rtype: ``set Node``


Predicates
------------

.. als:predicate:: undirected [r: node->node]
  
  ``r`` is :als:pred:`symmetric`.

.. als:predicate:: noSelfLoops[r: node->node]

  ``r`` is :als:pred:`irreflexive`.

.. als:predicate:: weaklyConnected[r: node->node]

  For any two nodes A and B, there is a path from A to B or a path from B to A. The path may not necessarily be bidirectional.

.. als:predicate:: stronglyConnected[r: node->node]

  For any two nodes A and B, there is a path from A to B *and* a path from B to A.

.. als:predicate:: rootedAt[r: node->node, root: node]

  All nodes are reachable from ``root``.

  .. warning:: this is *not* the same meaning of *root* as in the `roots` function! For the function, a *root* is a node no node connects to. Interally, ``util/graph`` uses ``rootedAt`` and not ``roots``.

.. als:predicate:: ring [r: node->node]

  ``r`` forms a single cycle.

.. als:predicate:: dag [r: node->node]

  ``r`` is a :abbr:`dag (directed acyclic graph)`: there are no self-loops in the transitive closure.

.. als:predicate:: forest [r: node->node]

  ``r`` is a dag and every node has at most one parent.

.. als:predicate:: tree [r: node->node]

  ``r`` is a forest with a single root node.

.. als:predicate:: treeRootedAt[r: node->node, root: node]

  ``r`` is a tree with node ``root``.
