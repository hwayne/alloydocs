.. _modules:

++++++++++++
Modules
++++++++++++

Alloy **modules** are similar to programming languages and act as the namespaces. Alloy comes with a standard library of :ref:`utility modules <utils>`.


.. _simple-modules:

Simple Modules
====================

::

  open util/relation as r

Imports must be at the top of the file. Modules may import new signatures into the spec.

Modules can be imported multiple times under different namespaces.

.. _namespaces:

Namespaces
-----------------

A module can be namespaced by importing ``as`` a name. Namespaces are accessed with ``/``. This is also called a **qualified** import.

.. code:: 

  open util/relation as r

  -- later

  r/dom

.. _parameterized-modules:

Parameterized Modules
=========================

A parameterized module is "generic": its functions and predicates are defined for some arbitrary signature. When you import a parameterized module, you must pass in a signature. Its functions and predicates are then specialized to be defined for that signature.

.. code:: alloy

  open util/ordering[A]

  sig A {}

  run {some first} -- returns an A atom

Normally `ord/first <first>` returns an abstract ``elem``. By parameterizing the module with ``A``, the function now returns an ``A`` atom. 

The input must be a full signature and not a subset of one.

A parameterized module can be imported multiple times using `namespaces`.

.. note::

  The following built-in modules are parameterized: `ordering`, :mod:`time`, `graph`, and `sequence`.

Creating Modules
========================

The syntax for a module is

::

  module name

At the beginning of the file.

.. _private:

Private 
------------------

Any module predicate, function, and signature can be preceded by ``private``, which means it will not be imported into other modules.

::

  module name

  private sig A {}

.. todo:: exactly in module names. Not MVP, but should probably be brought up briefly

Creating Parameterized Modules
------------------------------------

::

  module name[sig]

  -- predicates and functions should use sig

