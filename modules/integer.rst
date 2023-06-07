.. als:module:: integer


+++++++++++++++
integer
+++++++++++++++

Emulates integers.

A collection of utility functions for using Integers in Alloy. Note that integer 
overflows are silently truncated to the current bitwidth using the 2's complement 
arithmetic, unless the ''forbid overflows'' option is turned on, in which case only
models that do not have any overflows are analyzed. 

.. warning::
  
  The main challenge with this module is the distinction between ``Int`` and ``int``. ``Int`` is the set of integers that have been instantiated, whereas ``int`` returns the value of an ``Int``. You have to explicitly write ``int i`` to be able to add, subtract, and compare ``Ints``.


.. code:: alloy

  open util/integer
  
  fact ThreeExists { // there is some integer whose value is 3
    some x: Int | int x = 3
  }

  fun add[a, b: Int]: Int {
    {i: Int | int i = int a + int b}
  }
  
  run add for 10 but 3 int expect 1

To try this module out, in Alloy Analyzer's evaluator, you may also issue the 
following commands (suppose that allow generated a set with numbers ranging 
from ``-8`` to ``7``):

.. code:: alloy

  1 + 3
    4

  7 + 1
    -8


Functions
==========

.. als:function:: add [n1, n2: Int]

  :rtype: ``one Int``

  Returns ``n1 + n2``.

.. als:function:: plus [n1, n2: Int]

  :rtype: ``one Int``

  Returns ``n1 + n2``.

.. als:function:: sub [n1, n2: Int]

  :rtype: ``one Int``

  Returns ``n1 - n2``.

.. als:function:: minus [n1, n2: Int]

  :rtype: ``one Int``

  Returns ``n1 - n2``.

.. als:function:: mul [n1, n2: Int]

  :rtype: ``one Int``

  Returns ``n1 * n2``.

.. als:function:: div [n1, n2: Int]

  :rtype: ``one Int``

  Returns the division with ''round to zero'' semantics, except the following 
  3 cases:

  * if a is 0, then it returns 0

  * else if b is 0, then it returns 1 if a is negative and -1 if a is positive

  * else if a is the smallest negative integer, and b is -1, then it returns a
  
.. als:function:: rem [n1, n2: Int]

  :rtype: ``one Int``

  Returns the unique integer that satisfies ``a = ((a/b)*b) + remainder``.

.. als:function:: negate [n: Int]

  :rtype: ``one Int``

  Returns the negation of n.

.. als:function:: signum [n: Int]

  :rtype: ``one Int``

  Returns the signum of n (aka sign or sgn). In particular, 
  ``n < 0 => ( 0 - 1 ) else ( n > 0 => 1 else 0 )``.

.. als:function:: int2elem [i: Int, next: univ->univ, s: set univ]

  :rtype: ``lone s``

  Returns the ith element (zero-based) from the ``set s``
  in the ordering of ``next``, which is a linear ordering
  relation like that provided by :als:mod:`ordering`.

.. als:function:: elem2int [e: univ, next: univ->univ]

  :rtype: ``lone Int``

  Returns the index of the element (zero-based) in the
  ordering of next, which is a linear ordering relation
  like that provided by :als:mod:`ordering`.

.. als:function:: max

  :rtype: ``one Int``

  Returns the largest integer in the current bitwidth.

.. als:function:: min

  :rtype: ``one Int``

  Returns the smallest integer in the current bitwidth.

.. als:function:: next

  :rtype: ``Int -> Int``

  Maps each integer (except max) to the integer after it.

.. als:function:: prev

  :rtype: ``Int -> Int``

  Maps each integer (except min) to the integer before it.

.. als:function:: max [es: set Int]

  :rtype: ``lone Int``

  Given a set of integers, return the largest element.

.. als:function:: min [es: set Int]

  :rtype: ``lone Int``

  Given a set of integers, return the smallest element.

.. als:function:: prevs [e: Int]

  :rtype: ``set Int``

  Given an integer, return all integers prior to it.

.. als:function:: nexts [e: Int]

  :rtype: ``set Int``

  Given an integer, return all integers following it.

.. als:function:: larger [e1, e2: Int]

  :rtype: ``Int``

  Returns the larger of the two integers.

.. als:function:: smaller [e1, e2: Int]

  :rtype: ``Int``

  Returns the smaller of the two integers.

Predicates
==========

.. als:predicate:: eq [n1, n2: Int]
  
  ``True`` iff n1 is equal to n2.

.. als:predicate:: gt [n1, n2: Int]
  
  ``True`` iff n1 is greater than n2.

.. als:predicate:: gte [n1, n2: Int]
  
  ``True`` iff n1 is greater than or equal to n2.

.. als:predicate:: lt [n1, n2: Int]
  
  ``True`` iff n1 is less than n2.

.. als:predicate:: lte [n1, n2: Int]
  
  ``True`` iff n1 is less than or equal to n2.

.. als:predicate:: zero [n: Int]
  
  ``True`` iff n is equal to ``0``.

.. als:predicate:: pos [n: Int]
  
  ``True`` iff n is positive.

.. als:predicate:: neg [n: Int]
  
  ``True`` iff n is negative.

.. als:predicate:: nonpos [n: Int]
  
  ``True`` iff n is non-positive.

.. als:predicate:: nonneg [n: Int]
  
  ``True`` iff n is non-negative.
