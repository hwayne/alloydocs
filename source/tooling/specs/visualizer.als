abstract sig Object {}

sig File extends Object {}

sig Dir extends Object {contents: set Object}
one sig Root extends Dir { }


fact {
 Object in Root.*contents
}

assert RootTop {
 no o: Object | Root in o.contents
}
check RootTop // This assertion should produce a counterexample

