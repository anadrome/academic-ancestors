Academic ancestors from Wikidata
===

A few Python scripts that construct academic ancestor graphs (i.e. chains of
Ph.D. students and their Ph.D. advisors). This is done by sending SPARQL
queries to [Wikidata](https://www.wikidata.org/) that follow the [doctoral
advisor (P184)](https://www.wikidata.org/wiki/Property:P184) relations.
See [this blog
post](https://www.kmjn.org/notes/academic_ancestors_wikidata.html) for an
explanation and examples.

Required Python packages: requests, graphviz

There are currently two scripts:

ancestors2dot
---

Grab the complete ancestor tree of a specific researcher, and output it in
[graphviz](https://graphviz.org/) DOT format.

Usage:

    ./ancestors2dot.py Qxxxxx [outfile.dot]

    Qxxxxx: a researcher's Wikidata ID
    outfile.dot: file to write to if supplied; otherwise write to stdout

You will need to have graphviz installed to actually graph the resulting DOT
file, by doing something like:

    dot -Tpng personA.dot > personA.png

common2dot
---

Given two researchers, graph the path to their most recent common ancestor, if
any.

Usage:

    ./common2dot.py Q1xxxx Q2xxxx [outfile.dot]

    Qxxxxx: two researchers' Wikidata IDs
    outfile.dot: file to write to if supplied; otherwise write to stdout

Note that if the two researchers do not have any common ancestors *and* have
large ancestor trees, the query may time out.
