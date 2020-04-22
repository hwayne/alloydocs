.. _analyzer:

++++++++
Analyzer
++++++++

The **Alloy Analyzer** is the tool that actually checks your spec.

Configuring the Analyzer
=====================================

.. todo:: make a link to SAT, explain what Kodkod is

The analyzer converts the model into a SAT expression to solve. Some of the options are configurable. By default you should not need to change any of these- most performance issues are better solved by improving the spec itself. The following all affect the runtime of the analyzer. All of these are under the “Options” toolbar of the IDE:

.. todo:: maximum stack

-  **Allow Warnings:** When “no”, the analyzer will halt if the model has any warnings. Warnings usually, but not always, correspond to errors in the spec.
-  **Maximum Memory:** How much RAM the analyzer is allowed to use when solving.
-  **Solver:** The SAT solver to use for finding the model. Different solvers may have different performance on different specs. The SAT model and Kodkod model can also be output to a temporary file here.  There are additional special options for MiniSat with `Unsat Core <unsat-core>`, below.
-  **Skolem Depth:** see below
-  **Recursion Depth:** see below
-  **Record the Kodkod input/output:** when ``true``, the Kodkod output for the run can be seen by clicking the *Predicate* link in the output.

.. image:: img/kodkod.png

-  **Prevent Overflows:** If an `arithmetic operation <integers>` would overflow the model, the predicate is treated as false.


.. todo::

   1. 
     figure out who knows Skolem Depth. From `here <http://alloytools.org/quickguide/gui.html>`__:

      > Skolem Depth: This controls the maximum depth of alternating
      universal-vs-existential quantifier that we will permit when
      generating a skolem function. If a formula exceeds this depth, we
      will not generate a skolem function for it.

     but that doesn’t explain it in a way that’s useful for most readers

   2. Figure out who knows what "Infer partial instances". does.

     [We might just leave it out of this version]


.. rst-class:: advanced
.. _recursion:

Recursion Depth
-------------------


Predicates and functions are normally not recursive- they may not call
themselves. The following is an invalid predicate:

.. code:: alloy

   sig Node {
       edge: set Node
   }

   fact {no iden & ^edge}

   pred binary_tree[n: Node] {
       #n.edge <= 2
       all child: n.edge |
       // recursive call
           binary_tree[child]
   }

   run {some n: Node | binary_tree[n]}

This is invalid because all Alloy models must be bound, and recursive
calls can lead to an unbound model. Normally you should restructure your
model to not need a recursive call. If you *must* have a recursive
predicate or function, you can set the ``recursion depth`` to a maximum
of 3.

The recursion depth is treated as a “fact”: the analyzer will not look
for models with a greater recursion depth, even if it would lead to a
valid example or counterexample.

.. WARNING:: Increasing the recursion depth will slow down your spec.






.. rst-class:: advanced

.. _unsat-core:

Unsat Core
--------------

By default Alloy is packaged with `Minisat <http://minisat.se/>`__,
which also has an *Unsat Core*. When “MiniSat with Unsat Core” is
selected as the solver, the analyzer can isolate which constraints
prevent the analyzer from finding a counter/example. See
`here <http://alloytools.org/quickguide/unsat.html>`__ for more
information.

.. NOTE:: By default, the Windows version of Alloy does not come with MiniSAT.

.. WARNING:: The “Core Granularity” option is not strictly increasing in terms of information: a slower setting might, in some circumstances, lead to the core providing *less* information. Given the following model:

  .. code:: alloy

     sig Node {
         edge: some Node
     }

     fact {some Node}

     run {no edge}

  All granularity settings will highlight three formulas *except* for
  “expand quantifiers”, which will only highlight two. However, all three
  constraints are required to make the predicate inconsistent.
