.. _markdown:

++++++++
Markdown
++++++++

Thanks to Peter Kriens, Alloy supports Markdown syntax. Files written in Alloy Markdown have an ``.md`` extension, just like regular Markdown files. The Alloy Analyzer can read in Markdown files the same way it reads in ``.als`` files.

For an example of an Alloy Markdown file, see Peter Kriens's `Dining Philosophers`_.

.. _Dining Philosophers: https://github.com/pkriens/pkriens.github.io/blob/master/philosophers.md

Header
======

A Markdown Alloy file must start with a YAML header: three dashes on the first line, followed by fields and values in YAML format, followed by three more dashes. For example:

  .. code:: yaml

      ---
      title: Dining Philosophers
      ---


Alloy sections
==============

After the YAML header, the Alloy parser interprets all text as Markdown. To start an Alloy section, use `fenced code blocks`_ with ``alloy`` as the language identifier. For example:

.. _fenced code blocks: https://help.github.com/en/github/writing-on-github/creating-and-highlighting-code-blocks#fenced-code-blocks

  .. code::

      # Literate Programming 

      Let us change our traditional attitude to the construction of programs: Instead 
      of imagining that our main task is to instruct a computer what to do, let us 
      concentrate rather on explaining to human beings **what** we want a computer to do.

      ```alloy
      sig Foo {} // this is Alloy syntax
      ```

      If you find that you're spending almost _all_ your time on theory, start turning 
      _some_ attention to practical things; it will improve your theories. If you find 
      that you're spending almost all your time on practice, start turning some attention 
      to theoretical things; it will improve your practice.


GitHub Pages support
====================

The YAML header can be used in conjunction with `GitHub Pages`_. GitHub Pages allow you to maintain a website via Github, the YAML header is then used to encode metadata information such as title and layout. This `example website`_ shows the dining philosophers example rendered using Jekyll_ and served from GitHub Pages.

.. _Github Pages: https://pages.github.com/
.. _example website: https://www.aqute.biz/philosophers.html
.. _Jekyll: https://jekyllrb.com/docs/github-pages/

