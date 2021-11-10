.. module:: naturals


+++++++++++++++
naturals
+++++++++++++++

Emulates natural (non-negative) numbers.

This is an utility with functions and predicates for using the set of
nonnegative integers (``0, 1, 2, . . .``). The number of naturals present 
in an analysis will be equal to the scope on Natural. Specifically, if 
the scope on Natural is ``N``, then the naturals ``0`` through ``N-1`` will 
be present.

.. code:: alloy

  open util/natural
  
  fun sum[a: Natural, b: Natural]: Natural {
    {x:Natural | x = natural/add[a,b]}
  }
  
  run show for 3

To try this module out, in Alloy Analyzer's evaluator, you may invoke the 
function defined above as follows:

.. code:: alloy

  sum [natural/Natural1, natural/Natural1]
    {natural/Natural$2}

  sum [natural/Natural1, natural/Natural2]
    {}


Functions
==========

.. als:function:: inc [n: Natural]

  :rtype: ``one Natural``

  Returns ``n + 1``.

.. als:function:: dec [n: Natural]

  :rtype: ``one Natural``

  Returns ``n - 1``.


.. als:function:: add [n1, n2: Natural]

  :rtype: ``one Natural``

  Returns ``n1 + n2``.

.. als:function:: sub [n1, n2: Natural]

  :rtype: ``one Natural``

  Returns ``n1 - n2``.

.. als:function:: mul [n1, n2: Natural]

  :rtype: ``one Natural``

  Returns ``n1 * n2``.

.. als:function:: div [n1, n2: Natural]

  :rtype: ``one Natural``

  Returns ``n1 / n2``.
  
.. als:function:: max [ns: set Natural]

  :rtype: ``one Natural``

  Returns the maximum integer in ns.

.. als:function:: min [ns: set Natural]

  :rtype: ``one Natural``

  Returns the minimum integer in ns.


Predicates
==========

.. als:predicate:: gt [n1, n2: Natural]
  
  ``True`` iff n1 is greater than n2.

.. als:predicate:: gte [n1, n2: Natural]
  
  ``True`` iff n1 is greater than or equal to n2.

.. als:predicate:: lt [n1, n2: Natural]
  
  ``True`` iff n1 is less than n2.

.. als:predicate:: lte [n1, n2: Natural]
  
  ``True`` iff n1 is less than or equal to n2.

