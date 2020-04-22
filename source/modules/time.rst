.. module:: time

++++
time
++++

Automatically imports an ordered ``Time`` signature to your spec.

.. warning::

  ``Time`` internally uses the :mod:`ordering` module. This means that the signature is forced to be exact.

.. seealso::

  Module :mod:`ordering`

Macros
----------

.. als:macro:: dynamic[x]

  :arg sig x: any signature.
  :expansion: ``x one -> Time``

  ``dynamic`` can be used as part of a signature definition::

    open util/time

    abstract sig Color {}
		one sig Red, Green, Yellow extends Color {}

    sig Light {
      , state: dynamic[Color]
    }

  At every ``Time``, every ``Light`` will have exactly one color.



.. als:macro:: dynamicSet[x]

  :arg sig x: any signature.
  :expansion: ``x -> Time``

  Equivalent to ``dynamic``, except that any number of elements can belong to any given time::

    open util/time

    sig Keys {}

    one sig Keyboard {
      pressed: dynamicSet[Keys]
    }
  


..
  .. rst-class:: advanced

  Then
  --------------

  .. todo:: Define step predicates first (in techniques, maybe?) (Call them actions)
  .. als:macro:: then[a, b, start, finish]
    
    :arg pred[Time,Time] a: the initial event
    :arg pred[Time,Time] b: the subsequent event
    :arg Time start:
    :arg Time finish:
    :expansion: ``some x:Time | a[start,x] && b[x,finish]``

  Permits the "chaining" of time steps.  ``then`` is intended to be used as part of receiver syntax:

  ::
    fun cycle: set Color -> Color {
      (Red -> Green) + (Green -> Yellow) + (Yellow -> Red)
    }

    pred change[t, t': Time] {
     Light.state.t' = (Light.state.t).cycle
     t' = t.next
    }

    pred break[t, t': Time] {
     Light.state.t' = Red
     t' = t.next
    }

    run {
      some t: Time | change.then[break] [first, t]
    }



  let while = while3

  Equivalent to ``body.then[body].then[body]...`` up to three times or until ``cond[t]`` is true. Recall that every ``body`` should have ``t' = t.next``.
  let while1 [cond, body, t, t'] {
      some x:Time | (cond[t] => body[t,x] else t=x) && while0[cond,body,x,t']
  }

  let while0 [cond, body, t, t'] {
      !cond[t] && t=t'
  }

  ::

    open util/ordering[Time]
    sig Time { }
    let then [a, b, t, t']    {  some x:Time | a[t,x]&&  b[x,t']  }

    one sig Light { brightness: Int one->  Time }

    pred brighter [t, t': Time] {
        Light.brightness.t' = Light.brightness.t.plus[1]
        t' = t.next
    }

    pred dimmer [t, t': Time] {
        Light.brightness.t' = Light.brightness.t.minus[1]
        t' = t.next
    }

    run {
        some t:Time | brighter.then[dimmer].then[dimmer] [first, t]
    } for 4 Time

  While
  ---------
