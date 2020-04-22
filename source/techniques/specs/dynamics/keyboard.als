open util/ordering[Time]

sig Time {}

sig Key {
  pressed: set Time
}

pred press[k: Key, t: Time] {
  t not in k.pressed
  t.next in k.pressed
}

pred release[k: Key, t: Time] {
  t in k.pressed
  t.next not in k.pressed
}

pred changed[k: Key, t: Time] {
  press[k, t] or release[k, t]
}

fact Trace {
  no first.~pressed
  all t: Time - last |
    some k: Key {
      changed[k, t]
      all k': Key - k |
        not changed[k, t]
    }
}
