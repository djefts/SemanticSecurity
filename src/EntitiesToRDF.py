#!/usr/bin/env python
# coding: utf-8

# In[14]:


import rdflib
from rdflib import Graph, RDF, URIRef, Literal, BNode
from rdflib.namespace import FOAF, XSD
from rdflib import Namespace
from rdflib.namespace import DCTERMS, SKOS, PROV, PROF


def get_uri(entity):
    pass


def add_friend(k_graph, user_uri, friend_name, link):
    friend_uri = URIRef(link)
    k_graph.add((friend_uri, RDF.type, FOAF.Person))
    k_graph.add((friend_uri, FOAF.name, Literal(friend_name)))
    k_graph.add((user_uri, FOAF.knows, friend_uri))


if __name__ == "__main__":
    g = Graph()
    g.bind("foaf", FOAF)
    
    JKeck = URIRef('https://www.facebook.com/john.keck.125')
    DJefts = URIRef('https://www.facebook.com/david.jefts')
    demonSlayer = URIRef('https://www.imdb.com/title/tt9335498/')
    JOrtiz = URIRef('https://www.facebook.com/juan.ortizcouder')
    siocNamespace = Namespace('http://rdfs.org/sioc/ns#')
    
    JKeckName = Literal('John W Keck')
    DJeftsName = Literal('David Jefts')
    JOrtizName = Literal("Juan Ortiz")
    DSname = Literal('Demon Slayer')
    age = Literal(56)
    
    g.add((JOrtiz, RDF.type, FOAF.Person))
    g.add((JOrtiz, FOAF.name, JOrtizName))
    g.add((JOrtiz, FOAF.knows, DJefts))
    g.add((JOrtiz, FOAF.knows, JKeck))
    
    g.add((JKeck, RDF.type, FOAF.Person))
    g.add((JKeck, FOAF.name, JKeckName))
    g.add((JKeck, FOAF.knows, DJefts))
    g.add((JKeck, FOAF.knows, JOrtiz))
    
    g.add((DJefts, RDF.type, FOAF.Person))
    g.add((DJefts, FOAF.name, DJeftsName))
    g.add((DJefts, FOAF.knows, JKeck))
    g.add((DJefts, FOAF.knows, JOrtiz))
    
    g.add((JKeck, siocNamespace.likes, demonSlayer))
    g.add((demonSlayer, FOAF.name, DSname))
    
    # print(g.serialize(format="turtle").decode("utf-8"))
    
    # print("--- printing raw triples ---")
    # for s, p, o in g:
    #    print((s, p, o))
    
    # print all the data in the Notation3 format
    print("--- printing mboxes ---")
    print(g.serialize(format = 'n3').decode("utf-8"))
