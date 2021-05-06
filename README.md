Academic ancestors from Wikidata
===

A few Python scripts that construct academic ancestor graphs (i.e. chains of
Ph.D. students and their Ph.D. advisors). This is done by sending SPARQL
queries to [https://www.wikidata.org/](Wikidata) that follow the [doctoral
advisor (P184)](https://www.wikidata.org/wiki/Property:P184) relations.

Required packages: requests, graphviz

Usage:

    ./ancestors2dot.py Qxxxxx [outfile.dot]

    Qxxxxx: a researcher's Wikidata ID
    outfile.dot: file to write to if supplied; otherwise write to stdout
