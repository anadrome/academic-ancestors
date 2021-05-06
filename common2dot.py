#!/usr/bin/env python3

# Generate a graphviz graph of the path to two researchers' common academic
# ancestor, if there is one, according to Wikidata.
# Mark J. Nelson, 2021

import sys
import requests
import graphviz

def get_common_ancestor_pairs(personA, personB):
  query = """
SELECT ?ancestor1aLabel ?ancestor2aLabel ?ancestor1bLabel ?ancestor2bLabel WHERE {
  # ancestors of the first person leading to a common ancestor (or ancestors)
  wd:""" + personA + """ wdt:P184* ?ancestor1a.
  ?ancestor1a wdt:P184 ?ancestor2a.
  ?ancestor2a wdt:P184* ?common_ancestor.
  # ancestors of the second person leading to a common ancestor (or ancestors)
  wd:""" + personB + """ wdt:P184* ?ancestor1b.
  ?ancestor1b wdt:P184 ?ancestor2b.
  ?ancestor2b wdt:P184* ?common_ancestor.
  # stop at the common ancestor(s) rather than retrieving their own ancestors
  FILTER NOT EXISTS {
    wd:""" + personA + """ wdt:P184* ?intermediate_ancestor.
    wd:""" + personB + """ wdt:P184* ?intermediate_ancestor.
    ?intermediate_ancestor wdt:P184 ?common_ancestor.
  }
  ?ancestor1a wdt:P31 wd:Q5.
  ?ancestor2a wdt:P31 wd:Q5.
  ?ancestor1b wdt:P31 wd:Q5.
  ?ancestor2b wdt:P31 wd:Q5.
  ?common_ancestor wdt:P31 wd:Q5.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}"""
  result = requests.get("https://query.wikidata.org/sparql", params = {'format': 'json', 'query': query}).json()
  linksA = [(link['ancestor2aLabel']['value'], link['ancestor1aLabel']['value']) for link in result['results']['bindings']]
  linksB = [(link['ancestor2bLabel']['value'], link['ancestor1bLabel']['value']) for link in result['results']['bindings']]
  return list(set(linksA + linksB)) # remove duplicates, since the query will return various permutations

def make_dot(ancestor_pairs):
  graph = graphviz.Digraph()
  graph.edges(ancestor_pairs)
  return graph.source

if __name__ == "__main__":
  if (len(sys.argv) != 3 and len(sys.argv) != 4):
    print(f"Usage: {sys.argv[0]} Q1xxxx Q2xxxx [outfile.dot]\n  Qxxxxx: two researchers' Wikidata IDs\n  outfile.dot: file to write to if supplied; otherwise write to stdout", file=sys.stderr)
  else:
    dot = make_dot(get_common_ancestor_pairs(sys.argv[1], sys.argv[2]))

    f = open(sys.argv[3], 'w') if len(sys.argv) == 4 else sys.stdout
    print(dot, file=f)
