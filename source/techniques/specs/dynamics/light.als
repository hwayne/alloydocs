open util/ordering[Light] as ord

abstract sig Color {}
one sig Red, Yellow, Green extends Color {}

sig Light {
  color: Color
}

pred change_light[l: Light] {

  let l' = l.(ord/next) {
    l.color = Red => l'.color = Green
    l.color = Green => l'.color = Yellow
    l.color = Yellow => l'.color = Red
  }

}

fact Trace {
  ord/first.color = Red

  all l: Light - ord/last |
    change_light[l]
}
