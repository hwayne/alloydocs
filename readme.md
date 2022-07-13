# Alloydocs

This is the repository for development of the [Alloy](http://www.alloytools.org/) documentation. The documentation is currently hosted [here](https://alloy.readthedocs.io/en/latest/language/index.html). This readme is for people who are interested in building and contributing it.

## Building


The docs currently run on Sphinx. You can install Sphinx with [these instructions](https://www.sphinx-doc.org/en/master/usage/installation.html). You will also need the theme:

```
python -m pip install sphinx-rtd-theme
```

Docs can be built with ``make html``.

## Development

The repo is [standard Sphinx](https://www.sphinx-doc.org/en/master/intro.html), using reStructured Text. Some things might use a bit too much rst as I was getting a feel for what worked and didn't here.

There are two customizations:

### Custom Alloy Domain

Under `utils/alloy.py`. It has roles for functions, predicates, and properly indexes them. Sphinx's standard "this is a function" flag will add parens to docs, while Alloy uses brackets. So we make the brackets part of the function title and then split them off while indexing.

**TODO:** To speed up writing documentation I added an `:also:` param to functions that have "obvious" analogs. For example:

```rst
.. als:predicate:: lt[e1, e2: elem]

  :also: ``gt``, ``lte``, ``gte``

  True iff ``e1 in prevs[e2]``.
```

Functions defined in `:also:` don't have cross-references or indexes. We should change that.

**TODO:** Currently the `alloy.py` is pretty rickety and should be cleaned up/made more idiomatic.

### advanced class

Some sections are marked as "Advanced":

```rst
.. rst-class:: advanced
.. _enums:

Enums
-----
```

Advanced sections have an indicator before them, currently `[⋇] `, that marks them as unnecessary for beginners to learn. I have two **TODOs** I want to add:

1. A tooltip saying "this is an advanced section" so people know what it means without having read the intro
1. A button that toggles whether the advanced sections are visible at all


## Other Misc Tasks

* The reference currently isn't comprehensive.
* Cross references are a bit inconsistent. Some are hyphen-cased, some use spaces. Both are valid, but I'd like to move everything to hyphens for consistency.
* The location of certain topics might move around.
* There are many todos in the docs. These are not visible in the "proper" version, but are there for internal discussion.

## Contributing

TODO
