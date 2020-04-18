.. module:: relation

===========
relation
===========

All functions and predicates in this module apply to any binary relation. `univ <univ>` is the set of all atoms in the model.

Functions
---------

.. als:function:: dom[r: univ->univ]

  :rtype: ``set univ``

  Returns the domain of ``r``. Equivalent to ``univ.~r``.

.. als:function:: ran[r: univ->univ]

  :rtype: ``set univ``

  Returns the range of ``r``. Equivalent to ``univ.r``.


Predicates
----------

.. als:predicate:: total[r: univ->univ, s: set]

  True iff every element of ``s`` appears in ``dom[r]``.

.. als:predicate:: functional[r: univ->univ, s: set univ]

  True iff every element of ``s`` appears *at most once* in the left-relations of ``r``.

.. als:predicate:: function[r: univ->univ, s: set univ]

  True iff every element of ``s`` appears *exactly once* in the left-relations of ``r``.

.. als:predicate:: surjective[r: univ->univ, s: set univ]

  True iff ``s in ran[r]``.

.. als:predicate:: injective[r: univ->univ, s: set univ]

  True iff no two elements of ``dom[r]`` map to the same element in ``s``.

.. als:predicate:: bijective[r: univ->univ, s: set univ]

  True iff every element of ``s`` is mapped to by *exactly one* relation in ``r``. This is equivalent to being both injective and surjective. There may be relations that map to elements outside of ``s``.

.. als:predicate:: bijection[r: univ->univ, d, c: set univ]

  True iff exactly ``r`` bijects ``d`` to ``c``.

  .. todo:: I think the definition is actually wrong. It's either too strict or too loose. Both of these asserts fail

    .. code:: alloy 

      open util/relation

      sig B {}
      sig C {}
      sig A {
        rel: set B + C
      }

      assert {
        bijection[rel, A, B] => #A = #B
      }

      assert {
        bijective[rel :> B, B] => bijection[rel, A, B]
      }

.. als:predicate:: reflexive[r: univ -> univ, s: set univ]

  ``r`` maps every element of ``s`` to itself.

.. als:predicate:: irreflexive[r: univ -> univ]

  ``r`` does not map any element to itself.

.. als:predicate:: symmetric[r: univ -> univ]
  
  ``A -> B in r implies B -> A in r``

.. als:predicate:: antisymmetric[r: univ -> univ]

  ``A -> B in r implies B -> A notin r``. This is stronger than ``not symmetric``: *no* subset of ``r`` can be symmetric either.

.. als:predicate:: transitive[r: univ -> univ]

  ``A -> B in r and B - > C in r implies A -> C in r``

.. als:predicate:: acyclic[r: univ->univ, s: set univ]

  ``r`` has no cycles that have elements of ``s``.


.. als:predicate:: complete[r: univ->univ, s: univ]

  ``all x,y:s | (x!=y => x->y in (r + ~r))``

.. als:predicate:: preorder[r: univ -> univ, s: set univ]

  ``reflexive[r, s] and transitive[r]``

  .. todo:: this might also be wrong, shouldn't it only be if r is transitive over s?

.. als:predicate:: equivalence[r: univ->univ, s: set univ]

  ``r`` is reflexive, transitive, and symmetric over s.

.. als:predicate:: partialOrder[r: univ -> univ, s: set univ]

  ``r`` is a partial order over the set ``s``.

.. als:predicate:: totalOrder[r: univ -> univ, s: set univ]

  ``r`` is a total order over the set ``s``.
