open util/ordering[Time]

sig Time {
  pressed: set Key
}

sig Key {
}

pred press[k: Key, t: Time] {
  k not in t.pressed
  k in t.next.pressed
}

pred release[k: Key, t: Time] {
  k in t.pressed
  k not in t.next.pressed
}

pred changed[k: Key, t: Time] {
  press[k, t] or release[k, t]
}

face Trace {
  no first.pressed
  all t: Time - last |
    some k: Key {
      changed[k, t]
      all k': Key - k |
        not changed[k, t]
    }
}
