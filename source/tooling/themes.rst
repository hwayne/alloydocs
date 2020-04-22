.. |dt| replace:: Default True.
.. |df| replace:: Default False.

.. _themes:

++++++
Themes
++++++

Diagrams produced in the :doc:`visualizer` can be **themed**. Options are:

.. note:: All options will not be changed until you click the “Apply” button.

.. todo:: I'd love to have before and after screenshots for every one of these options, but the tooling doesn't make that automatically generatable.

General Graph Settings
===========================

.. todo:: Explain what meta does

- **Use Original Atom Names**: Instead of showing atoms as ``Atom¹``, the visualizer will show them as ``Atom$1``. Default False.
- **Hide Private Sigs/Relations**: Hides signatures and relations that are internal to an imported module. Default True.
- **Hide Meta Sigs/Relations**: ???


Types and Sets
===================

In this case, "set" refers to any nodes that are important to the visualizer, such as the results of `commands`. All settings are hierarchical: any setting labelled ``inherit`` will use the same setting as the parent type/set. Settings for sets override settings for signatures.

The following settings are universal to all nodes:

- **Color**, **Shape**, and **Border**.
- **Name** (to the left of color): What to call the nodes. This does not effect the evaluator or tree, text, and table views.
- **Show**: Whether or not the node is visible in the visualization at all. Default True.
- **Hide Unconnected Nodes**: If a node doesn't have any relation to any other node, hide the node. Default True.


The following are specific to signatures:

- **Number Nodes**: Nodes with the same name and same type are suffixed with a number.
- **Project over this Sig**: See `projections`.

The following are specific to sets:

- **Show as Labels:** Set membership is shown as a text label on the matching atoms.
- **Show in Relation Attributes**: If the element of the set appears in another node's textual attributes, also list that it belongs to the set.

.. todo:: That one NEEDS a before/after visualization.

Relations
=================

For all of these options, we assume the relation is ``rel: A -> B``

- **Show as Arcs**: Represent the relationship as an arrow from A to B. |dt|
- **Show as Attributes**: Represents the relationship as the label ``rel: B`` on node A. A relationship can be shown as both arcs and attributes at the same time. |df|
- **Influence Layout**: If True, the visualizer will try to account for the arrows when laying out the node graph. If False, the visualizer will first lay out the graph, and then draw the relation. |dt|
- **Weight**: The visualizer will try to minimize the weights of the larger arrows first.
- **Layout Backwards**: Layout the graph as if the relation was ``B -> A``. The final layout will still show the arrow as ``A -> B``. |df|
- **Merge Arrows**: If True, the relationship ``A -> B + B -> A`` with be represented as a single double-sided arrow. If false, the relationship is represented as two single-sided arrows. |dt|

.. _reusing-themes:

Reusing Themes
+++++++++++++++

Themes can be saved and loaded under the ``theme`` top menu bar. Themes can also be reset here.
