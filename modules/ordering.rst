.. module:: ordering

++++++++
ordering
++++++++

  Ordering places an ordering on the parameterized signature.

::

  open util/ordering[A]

  sig A {}

  run {
    some first -- first in ordering
    some last  -- last in ordering
    first.lt[last]
  }


``ordering`` can only be instantiated once per signature. You can, however, call it for two different signatures::

  open util/module[Thing1] as u1
  open util/module[Thing2] as u2

  sig Thing1 {}
  sig Thing2 {}
  

.. warning::

  ``ordering`` forces the signature to be `exact <scopes>`. This means that the following model has no instances::

    open util/ordering[S]

    sig S {}

    run {#S = 2} for 3

  In particular, be careful when using ``ordering`` as part of an assertion: the assertion may pass because of the implicit constraint!

.. seealso::

  Module :mod:`time`

    Adds additional convenience macros for the most common use case of ordering.

  `Sequences <seq>`

    For writing ordered relations vs placing top-level ordering on signatures.

Functions
---------

.. als:function:: first

  :return: The first element of the ordering
  :rtype: ``elem``
  :also: ``last``

.. als:function:: prev

  :rtype: ``elem -> elem``
  :also: ``next``

  Returns the relation mapping each element to its previous element. This means it can be used as any other kind of relation::

    fun is_first[e: elem] {
      no e.prev
    }

  
.. als:function:: prevs[e]

  :return: All elements before ``e``, excluding ``e``.
  :rtype: ``elem``
  :also: ``nexts``


.. als:function:: smaller[e1, e2: elem]

  :return: the element that comes first in the ordering
  :also: larger

.. als:function:: min[es: set elem]

  :return: The smallest element in ``es``, or the empty set if ``es`` is empty
  :rtype: ``lone elem``
  :also: max


Predicates
-------------


.. als:predicate:: lt[e1, e2: elem]

  :also: ``gt``, ``lte``, ``gte``

  True iff ``e1 in prevs[e2]``.

