.. _time:

++++++++++
Time
++++++++++

`Alloy 6 <https://alloytools.org/alloy6.html>`_ added **temporal operators** to Alloy, making it easier to model dynamic systems.

.. _var:

Variables
============

A signature or relation can be declared mutable with the ``var`` keyword:

.. code:: alloy 

  sig Server {}

  var sig Offline in Server {}

  sig Client {
    , var connected_to: lone Server - Offline
  }


The set of servers that are offline is mutable: different servers can be offline in different steps. The ``connected_to`` :ref:`field <signature-relations>` is also mutable and can have different ``Client -> Server`` pairs in different steps.

.. note:: This uses the ``in`` modifier as in the `boolean-subtyping` technique.

The number of steps in a model is specified with the `steps` command.

.. _steps-model:

Temporal Operators
==================

A dynamic model is broken into several `steps`. For each step, all ``var`` signatures and relations may change, depending on the predicates. By default, all predicates and facts only hold for the *initial* step of a variable. Eg

.. code:: alloy

  fact "init" {
    no Offline
    no connected_to
  }

This :ref:`fact <facts>` says that *in the initial step*, there are no offline servers and no connection between clients and servers. There are no constraints, however, on future steps. To place constraints on future steps, put predicates inside a :dfn:`temporal operator`, like ``always`` or ``eventually``.

.. code:: alloy

  pred spec {
    always no Offline
    eventually some connected_to
    
  }

  run {spec}

.. todo::

  .. note:: see TK for how to interpret the evaluated trace.

- ``always no Offline`` means that ``no Offline`` is true now, and in all future steps. 
- ``eventually some connected_to`` means that ``some connected_to`` is true *in at least one step*, now or in the future.

Temporal operators can be combined: ``eventually always some Offline`` means that there's a step where, from that step forward, there is some Offline server. 

To model a "change", we relate the values of a variable between two steps.  If ``connected_to`` is a ``var`` field, then ``connected_to'`` is the value of ``connected_to`` in the *next* step.

.. code:: alloy

  pred connect[c: Client, s: Server] {
    c -> s not in connected_to
    connected_to' = connected_to ++ c -> s
  }

In this example, ``connect`` is true or false in every step. In steps where it is true, the client is not connected to the server *and* in the next step, it is connected to the server. This represents the state of the system changing. 

.. _prime:

``'`` is also called the :dfn:`prime` operator. Combining primed predicates with temporal operators gives us a simple way to model system dynamics.

.. code:: alloy

  pred spec {
    -- all servers always online
    always no Offline

    -- initially no connections
    no connected_to

    -- every step, a client connects to a new server
    always some c: Client, s: Server {
      c.connect[s]
    } 
  }

  run {spec}


.. index:: always, eventually, past, once, after, before, until, since, releases, triggered

List of Operators
-----------------

Alloy operators include both *future* and *past* operators. Operators are true and false for a specific step.

.. list-table:: Future temporal operators
  :header-rows: 1
  
  * - Operator
    - Meaning
  * - always P
    - P is true *and* true in all future steps
  * - eventually P
    - P is true *or* true in at least one future step
  * - after P
    - P is true in the next step
  * - P ; Q
    - Shorthand for ``P && after Q``
  * - Q releases P
    - P is true until Q is true, then P *may* become false
  * - P until Q
    - Equivalent to ``(Q releases P) and eventually Q``

(``P'`` is special: instead of being true or false, it's simply the value of the P in the next step.)

There are also *past* operators corresponding to each future operator. ``once P`` is the past-version of ``eventually P``: P is true *or* true in at least one *previous* step.

.. list-table:: Past temporal operators
  :header-rows: 1
  
  * - Future Operator
    - Past Version
  * - always
    - historically
  * - eventually
    - once
  * - after
    - before
  * - triggered
    - releases
  * - since
    - until

.. todo:: Explain the weirdness of triggered and since


.. todo:: Traces?

.. todo:: 

  Temporal Properties
  .==================

  To test that a property always holds, wrap it in an ``always`` operator. Eg

  .. code:: alloy

    run {spec => always property}

