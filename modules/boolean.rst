.. module:: boolean


+++++++++++++++
boolean
+++++++++++++++

Emulates boolean variables by creating ``True`` and ``False`` atoms. 

.. code:: alloy

  -- module definition
  module util/boolean

  abstract sig Bool {}
  one sig True, False extends Bool {}

  pred isTrue[b: Bool] { b in True }

  pred isFalse[b: Bool] { b in False }

In our code:

.. code:: alloy

  -- our code
  open util/boolean

  sig Account {
    premium: Bool
  }

Booleans created in this matter are not "true" booleans and cannot be used as part of regular `constraints`, IE you cannot do ``bool1 && bool2``. Instead you must use the dedicated boolean predicates, below. As such, ``boolean`` should be considered a proof-of-concept and is generally **not recommended** for use in production specs. You should instead represent booleans using `subtyping <boolean-subtyping>`.

Functions
==========

All of the following have expected logic, but return ``Bool`` atoms:

* ``Not``
* ``And``
* ``Or``
* ``Xor``
* ``Nand``
* ``Nor``  

So to emulate ``bool1 && bool2``, write ``bool1.And[bool2].isTrue``.
