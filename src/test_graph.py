import rdflib
from SPARQLWrapper import SPARQLWrapper, SPARQLWrapper2
from SPARQLWrapper import JSON, TURTLE, XML, CSV
import json

repo_link = "http://98.156.138.188:7200/repositories/SemSec"


def sparqlwrapper_example(query = "SELECT * WHERE { ?s ?p ?o. }"):
    """
    See https://github.com/RDFLib/sparqlwrapper for more information
    """
    
    sparql = SPARQLWrapper(repo_link)
    sparql.setOnlyConneg(True)  # GraphDB uses only content negotiation, and no URL parameters
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.queryAndConvert()
    
    return results


def print_select_results(results):
    # for result in results["results"]["bindings"]:
    #     print(result["label"]["value"])
    for binding in results['results']['bindings']:
        x = 0
        for var in results['head']['vars']:
            # each binding is a dictionary. Let us just print the results
            print('\t' * x + "%s: %s (of type %s)" % (var, binding[var]['value'], binding[var]['type']))
            x += 1


# rdflib_example()lconv
ret = sparqlwrapper_example()
print(json.dumps(ret, indent = 2))
print('\n-----------------------------------\n')
print_select_results(ret)
