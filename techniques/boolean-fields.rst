
++++++++++++++
Boolean Fields
++++++++++++++

Often software properties are expressed as booleans, either true or false.  But Alloy doesn't have a native boolean type. There are two ways to emulate this.

For this example we want something akin to

.. code::

  sig Account {
    premium: bool -- invalid, not a real type
  }


.. _boolean-subtyping:

Subtyping
=========

Using `in <subtype in>` subtypes is the standard way to model booleans::

  sig Account {}
  sig PremiumAccount in Account {}

Then the boolean can be tested with ``a in PremiumAccount``. This method has a number of advantages:

* ``PremiumAccount`` and ``Account - PremiumAccount`` can be used in the signatures of other fields.

* Premium accounts can have additional fields.

* You can create a custom `theme <themes>` for premium accounts.

* The analyzer will generally be faster.


lone fields
----------------

Booleans can also be represented using ``lone``::

  one sig Premium {}
  sig Account {
    , premium: lone Premium
  }

Then the boolean can be tested with ``some a.premium``, and the set of all premium accounts is ``premium.Premium``.  Using lone is somewhat simpler than using a subtype, but it's less flexible overall, and the boolean cannot be used in the fields of other signatures.



The ``Boolean`` module
---------------------------

If subtyping is insufficient, you can also use the :mod:`boolean` module. This is generlaly not recommended.
