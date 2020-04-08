.. module:: ternary

+++++++
ternary
+++++++

``util/ternary`` provides utility functions for working with 3-arity `multirelations`. All functions return either an element in the relation or a new transformed relation.

.. list-table:: ``util/ternary``
  :header-rows: 1

  * - ``f``
    - ``f[a -> b -> c]``
  * - ``dom``
    - ``a``
  * - ``mid``
    - ``b``
  * - ``ran``
    - ``c``
  * - ``select12``
    - ``a -> b``
  * - ``select13``
    - ``a -> c``
  * - ``select23``
    - ``b -> c``
  * - ``flip12`` 
    - ``b -> a -> c``
  * - ``flip13``
    - ``c -> b -> a``
  * - ``flip23``
    - ``a -> c -> b``

