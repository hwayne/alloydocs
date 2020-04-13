.. _dynamics:

++++++++++++++
Dynamic Models
++++++++++++++

A **dynamic model** represents something changing over time. Alloy does not have a first-class notion of time, and dynamics must be encoded as part of the relationships. This is normally done by placing an `ordering` on some signature, which then used to emulate time. There are several common ways of doing this.

.. seealso::

  :mod:`time`

    A module with some utility macros to better model time.


Changing Object Signature
============================

When only one entity is changing and there is only one instance of the signature to consider, we can place the ordering on the signature itself. Then each atom of that signature represents the state of the entity at a different point in time.

.. literalinclude:: specs/dynamics/light.als
  :caption: Full spec downloadable :download:`here <specs/dynamics/light.als>`
  :lines: 1-9

While there are multiple ``Light`` atoms, they all represent the same physical "traffic light", just at different points in time.

The dynamic model is modeled by a state change predicate, which relates each light to the next light in the sequence.


.. literalinclude:: specs/dynamics/light.als
  :caption: Full spec downloadable :download:`here <specs/dynamics/light.als>`
  :lines: 10-18

Conventionally `ordering` is *not* namespaced. We do it here to make the imported functions clearer. 

.. _trace:

Traces
--------------

A :dfn:`trace` is a `fact <facts>` that describes how the system will evolve, by constraining "valid models" to ones where the system evolves properly.

.. trace

.. literalinclude:: specs/dynamics/light.als
  :caption: Full spec downloadable :download:`here <specs/dynamics/light.als>`
  :lines: 20-25

`first` and ``last`` are from the `ordering` module. This sets the first light to red and every subsequent light to the next color in the chain.


.. note:: We write ``Light - last`` because ``no last.next``, so the predicate would be false.

Time Signatures
======================

For more complex specifications we use a ``Time`` signature. This is useful if we have multiple things that are changing or multiple properties that can change. The ordering is placed on ``Time`` and the signature fields are all related to that time.

.. literalinclude:: specs/dynamics/keyboard.als
  :caption: Full spec downloadable :download:`here <specs/dynamics/keyboard.als>`
  :lines: 1-3

.. _dynamic-booleans:

Representing Boolean Properties
---------------------------------

If the changing value is a boolean, the best way to represent that is to have a field that is ``set Time``, which represents the times where that field is true:

.. literalinclude:: specs/dynamics/keyboard.als
  :caption: Full spec downloadable :download:`here <specs/dynamics/keyboard.als>`
  :lines: 5-21

We will assume that only one key can be pressed or released at a given time. This means that the trace must specify that some key changes *and also* that no other key changes.

.. literalinclude:: specs/dynamics/keyboard.als
  :caption: Full spec downloadable :download:`here <specs/dynamics/keyboard.als>`
  :lines: 22-

.. note:: We could have instead written it this way, using ``one`` instad of ``some``: 

  .. code:: alloy

    all t: Time - last |
      one k: Key |
        changed[k, t]

  Which would have enforced that no other keys changed by default. Using ``one`` in these contexts can be error-prone, so it's avoided for the purposes of this page.

Conventionally, state-change predicates are written to take two time parameters, where the trace then passes in both ``t`` and ``t.next``.

::

  pred release[k: Key, t, t': Time] {
    t in k.pressed
    t' not in k.pressed
  }


Representing Arbitrary Properties
---------------------------------

Information beyond booleans can be encoded with `multirelations`.

.. todo:: break this up and explain what's going on

.. literalinclude:: specs/dynamics/browsing.als
  :caption: Full spec downloadable :download:`here <specs/dynamics/browsing.als>`
  :lines: 1-12

Writing ``Page one -> Time`` indicates that for every Person and Time, there is exactly one page. Writing ``Page -> Time`` also any number of pages per person/time.

.. note:: There's no innate reason why we use ``Page -> Time`` instead of ``Time -> Page``. However, making Time the end of the multirelation is conventional.


.. literalinclude:: specs/dynamics/browsing.als
  :caption: Full spec downloadable :download:`here <specs/dynamics/browsing.als>`
  :lines: 13-28

When using multirelations of form ``rel = A -> B -> Time``, we get the value of ``b`` at time ``t`` with ``a.rel.t``

.. literalinclude:: specs/dynamics/browsing.als
  :caption: Full spec downloadable :download:`here <specs/dynamics/browsing.als>`
  :lines: 29-33

``stay`` is a "stuttering" predicate which makes it valid for a user to not change at the next time step. Without it ``goto`` would have to be true for every single user at every time in the trace.

.. literalinclude:: specs/dynamics/browsing.als
  :caption: Full spec downloadable :download:`here <specs/dynamics/browsing.als>`
  :lines: 34-


Common Issues
======================


Incomplete Trace
--------------------------------

The trace must fully cover what happens to all dynamic signatures. If not, weird things happen. Consider the following alternate trace for the browsing model:

::

  fact Trace {
    at.first = history.first -- everybody starts with their initial page in history
    all t: Time - last |
      let t' = t.next {
        one u: User |
          u.stay[t, t'] or
          some p: Page | u.goto[p, t, t']
      }
  }

This is true iff *exactly one* User either stays or goes to a valid page. This allows them to do anything that's not covered by the two predicates. A user may go to an unlinked page, or stay on the same page but change their history to include a page they never visited. 

"No Models Found"
--------------------------------


``ordering`` implicity makes the ordered signature `exact <exactly>` and this cannot be overridden. If a dynamic spec does not exist, it's likely due to this.

::

  open util/ordering[State]

  sig State {}

  run {#State = 2} -- no models


.. todo:: 
  1. Cases where multiple things relating to each other interact, like the ring election spec. So the predicates step on each others toes.
  2. Writing temporal assertions

Limitations
======================

There are some limitations to what we can model in a dynamic system. 

* Alloy cannot tell if a system has **deadlocked**. A deadlock is when there is no valid next state as part of the trace. If the trace is encoded as a fact, then the entire model is discarded. If the trace is encoded as a predicate, Alloy will provide any model that doesn't match the trace as a counterexample.
* Alloy cannot test that some property is guaranteed to happen in infinite time, aka **liveness**.
* Alloy cannot emulate **fair** dynamic systems.



.. todo:: representing with a Seq
