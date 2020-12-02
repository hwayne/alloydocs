.. module:: naturals


+++++++++++++++
naturals
+++++++++++++++

Emulates natural (non-negative) numbers.

.. code:: alloy
  open util/natural
  
  fun sum[a: Natural, b: Natural]: Natural {
    {x:Natural | x = natural/add[a,b]}
  }
  
  run show for 3

In Alloy's evaluator you may type the following:

.. code:: alloy
  sum [natural/Natural1, natural/Natural1]
    {natural/Natural$2}

  sum [natural/Natural1, natural/Natural2]
    {}


Functions
==========

.. code:: alloy
  fun inc [n: Natural] : lone Natural { ord/next[n] }
  fun dec [n: Natural] : lone Natural { ord/prev[n] } // returns n – 1 
  
  fun add [n1, n2: Natural] : lone Natural { // returns n1 + n2
    {n: Natural | #ord/prevs[n] = #ord/prevs[n1] + #ord/prevs[n2]} 
  }
  fun sub [n1, n2: Natural] : lone Natural { // returns n1 - n2
    {n: Natural | #ord/prevs[n1] = #ord/prevs[n2] + #ord/prevs[n]}
  }
  fun mul [n1, n2: Natural] : lone Natural { // returns n1 * n2
    {n: Natural | #ord/prevs[n] = #(ord/prevs[n1]->ord/prevs[n2])} 
  }
  fun div [n1, n2: Natural] : lone Natural { // returns n1 / n2
    {n: Natural | #ord/prevs[n1] = #(ord/prevs[n2]->ord/prevs[n])}
  }
  
  pred gt [n1, n2: Natural] { ord/gt [n1, n2] } // greater than
  pred lt [n1, n2: Natural] { ord/lt [n1, n2] } // less than
  pred gte [n1, n2: Natural] { ord/gte[n1, n2] } // greater than or equal to
  pred lte [n1, n2: Natural] { ord/lte[n1, n2] } // less than or equal to
  fun max [ns: set Natural] : lone Natural { ord/max[ns] } //returns the maximum integer in ns 
  fun min [ns: set Natural] : lone Natural { ord/min[ns] } // returns the minimum integer in ns



