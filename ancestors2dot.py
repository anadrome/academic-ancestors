#!/usr/bin/env python3

# Generate a graphviz graph of someone's academic ancestors,
# according to Wikidata.
# Mark J. Nelson, 2021

import sys
import requests
import graphviz

def get_ancestor_pairs(wikidata_id):
  query = """
SELECT ?ancestor1Label ?ancestor2Label WHERE {
  wd:""" + wikidata_id + """ wdt:P184* ?ancestor1.
  ?ancestor1 wdt:P184 ?ancestor2.
  ?ancestor1 wdt:P31 wd:Q5.
  ?ancestor2 wdt:P31 wd:Q5.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
"""
  result = requests.get("https://query.wikidata.org/sparql", params = {'format': 'json', 'query': query}).json()

  # turn the JSON SPARQL result into tuples of (advisor, advisee)
  return [(link['ancestor2Label']['value'], link['ancestor1Label']['value']) for link in result['results']['bindings']]

def make_dot(ancestor_pairs):
  graph = graphviz.Digraph()
  graph.edges(ancestor_pairs)
  return graph.source

if __name__ == "__main__":
  if (len(sys.argv) != 2 and len(sys.argv) != 3):
    print(f"Usage: {sys.argv[0]} Qxxxxx [outfile.dot]\n  Qxxxxx: a researcher's Wikidata ID\n  outfile.dot: file to write to if supplied; otherwise write to stdout", file=sys.stderr)
  else:
    dot = make_dot(get_ancestor_pairs(sys.argv[1]))

    f = open(sys.argv[2], 'w') if len(sys.argv) == 3 else sys.stdout
    print(dot, file=f)
