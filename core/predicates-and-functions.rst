++++++++++++++++++++++++
Predicates and Functions
++++++++++++++++++++++++

.. I'm intentionally leaving out qualified predicates because they don't provide any benefits and add syntax.

.. _predicates:

Predicates
==========

A predicate is like a programming function that returns a
`boolean <constraints>`. While they are a special case of Alloy
functions, they are more fundamental to modeling and addressed first.

Predicates take the form

.. code:: alloy

   pred name {
	  constraint
   }

Once defined, predicates can be used as part of boolean expressions. The
following is a valid spec:

.. code:: alloy

   sig A {}

   pred at_least_one_a {
     some A
   }

   pred more_than_one_a {
     at_least_one_a and not one A
   }

   run more_than_one_a

.. warning:: Predicates and functions **cannot**, in the general case, be recursive. 
    Limited recursion is possible, see 
    :ref:`here <recursion>` for more info.

.. _parameters:

Parameters
----------

Predicates can also take arguments.

.. code:: alloy

   pred foo[a: Set1, b: Set2...] {
     expr
   }

The predicate is called with ``foo[x, y]``, **using brackets, not
parens**. In the body of the predicate, ``a`` and ``b`` would have the
corresponding values.

.. _receiver-syntax:

Receiver Syntax
~~~~~~~~~~~~~~~~~~~

The initial argument to a predicate can be passed in via a ``.`` join.
The following two are equivalent:

.. code:: alloy

   pred[x, y, z]
   x.pred[y, z]




.. _functions: 

Functions
=============

Alloy functions are equivalent to programming functions. They have the
same structure as predicates, but also return a value:

.. code:: alloy

   fun name[a: Set1, b: Set2]: output_type {
     expression
   }

.. tip:: if a function is constant (does not take any parameters), the
    analyzer casts it to a constant set. This means if we have a function of parameter

    .. code:: alloy

        fun foo: A -> B {
            expression
        }

    Then ``^foo`` is a valid expression.

.. rst-class:: advanced

.. _overloading:

Overloading
------------------

Predicates and functions may be overloaded, as long as it's unambiguous which function applies. The following is valid:

.. code:: alloy

  sig A {}

  sig B {}

  pred foo[a: A] { --1
    a in A
  }

  pred foo[b: B] { --2
    b in B
  }

  run {some a: A | foo[a]}

As when ``foo`` is called, it's unambiguous whether it means (1) or (2). If we instead replaced ``sig B`` with ``sig B extends A``, then it's ambiguous and the call is invalid.

Overloading can happen if you import the same parameterized module twice.For example, given the following:

::

  
  open util/ordering[A]
  open util/ordering[B]

  sig A, B {}
  run {some first}

It is unclear whether ``first`` applies to ``A`` or ``B``. To fix this, use `Namespaced imports <namespaces>`::

  open util/ordering[A] as u1
  open util/ordering[B] as u2

  sig A, B {}
  run {some u2/first}


.. rst-class:: advanced
.. _@:

Parameter Overrides
-----------------------


The parameters of a function (or predicate) can shadow a global value.
In this case, you can retrieve the original global value by using
``@val``.

.. code:: alloy
    
  sig A {}

  pred f[A: univ, b: univ] {
    b in A  -- function param
    b in @A -- global signature
  }


.. _facts:

Facts
=====

A fact has the same form as a global predicate:

.. code:: alloy

   fact name {
     constraint
   }

A fact is *always* considered true by the Analyzer. Any models that
would violate the fact are discarded instead of checked. This means that
if a potential model both violates an assertion and a fact, it is not
considered a counterexample.

.. code:: alloy

   sig A {}

   -- This has a counterexample
   check {no A}

   -- Unless we add this fact
   fact {no A}

.. tip:: For facts, the name is optional. In addition, the name can be a string. So this is a valid fact:

    .. code::
      
      fact "no cycles" {
        all n: Node | n not in n.^edge
      }

.. rst-class:: advanced
.. _implicit facts:

Implicit Facts
------------------



You can write a fact as part of a signature. The implicit fact goes
after the signature definition and relations. Inside of an implicit fact,
you can get the current atom with ``this``. Fields are automatically expanded in the implicit fact to ``this.field``. 

::

  sig Node {
    edge: set Node
  } {
    this not in edge
  }

This means you cannot apply the relation to another atom
of the same signature inside the implicit fact. You can access the
original relation by using the ``@`` operator:

::

  -- undirected graphs only
  sig Node {
    , edge: set Node
  } 
  {
    all link: edge | this in link.edge -- invalid
    all link: edge | this in link.@edge -- valid
  } 


.. rst-class:: advanced
.. _macros:

Macros
========

A macro is a similar to a predicate or function, except it is expanded before runtime. For this reason, macros can be used as part of signature fields. Parameters to macros also don't need to be given types, so can accept arbitrary signatures and even boolean constraints. Macros are defined with ``let`` in the top scope.


.. code:: alloy
  
  let selfrel[Sig] = { Sig -> Sig }
  let many[Sig] = { some Sig and not one Sig }

  sig A {
    rel: selfrel[A]
  }

  run {many[A]}

See `here <http://alloytools.org/quickguide/macro.html>`__ for more information.
