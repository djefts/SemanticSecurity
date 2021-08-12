#!/usr/bin/env python
# coding: utf-8

"""
GeoNames Account Information:
username:   semsec_erau
email:      TimElvResearch@gmail.com
password:   keckW2323#
"""


import rdflib
from rdflib import Graph, RDF, URIRef, Literal, BNode
from rdflib.namespace import FOAF
from rdflib import Namespace
from rdflib.namespace import DCTERMS, SKOS, PROV, PROF
import geonames.adapters.search


def geo_search(city_name, state_name):
    """
    Method to access the GeoNames database
    :param city_name:
    :param state_name:
    :return: RDF node representing the city matching `city_name`
    """
    _USERNAME = 'semsec_erau'
    sa = geonames.adapters.search.Search(_USERNAME)
    
    result = sa.query('detroit').country('us').max_rows(5).execute()
    for id_, name in result.get_flat_results():
        # make_unicode() is only used here for Python version-compatibility.
        return geonames.compat.make_unicode("[{0}]: [{1}]").format(id_, name)


def init_social_media(k_graph, homepages):
    sites_uris = {}
    for social_media in homepages:
        site_uri = URIRef(social_media)
        k_graph.add((site_uri, RDF.type, FOAF.Document))
        sites_uris[social_media] = site_uri
    return sites_uris


def get_namespaces(k_graph):
    namespaces = {}
    for prefix, namespace in k_graph.namespace_manager.namespaces():
        namespaces[prefix] = namespace
    return namespaces


def add_online_account(k_graph, user_uri, user_homepage, account_username, service_uri):
    account_uri = URIRef(user_homepage)
    k_graph.add((account_uri, RDF.type, FOAF.OnlineAccount))
    k_graph.add((account_uri, FOAF.accountName, Literal(account_username)))
    k_graph.add((account_uri, FOAF.accountServiceHomepage, service_uri))
    k_graph.add((user_uri, FOAF.account, account_uri))
    return account_uri


def add_online_friend(k_graph, user_uri, friend_uri, friend_name, account_link, friend_username, service_uri):
    # TODO: ensure friend doesn't exist in graph already
    # user node instantiation
    k_graph.add((friend_uri, RDF.type, FOAF.Person))
    
    # Friend's FB Account:
    add_online_account(k_graph, friend_uri, account_link, friend_username, service_uri)
    
    # connect friend to user
    k_graph.add((friend_uri, RDF.type, FOAF.Person))
    k_graph.add((friend_uri, FOAF.name, Literal(friend_name)))
    k_graph.add((user_uri, FOAF.knows, friend_uri))
    k_graph.add((friend_uri, FOAF.knows, user_uri))
    return friend_uri


def add_diploma(k_graph, degree, school):
    degree_uri = URIRef(degree + ' - ' + school)
    school_uri = URIRef(school)
    k_graph.add((degree_uri, RDF.type, EDU))
    k_graph.add((school_uri, RDF.type,))
    k_graph.add((degree_uri, EDU.recognizedBy, school_uri))
    k_graph.add((user_fb_uri, FOAF.hasCredential,))


if __name__ == "__main__":
    # g = Graph()
    # g.bind("foaf", FOAF)
    #
    # JKeck = URIRef('https://www.facebook.com/john.keck.125')
    # DJefts = URIRef('https://www.facebook.com/david.jefts')
    # demonSlayer = URIRef('https://www.imdb.com/title/tt9335498/')
    # JOrtiz = URIRef('https://www.facebook.com/juan.ortizcouder')
    # siocNamespace = Namespace('http://rdfs.org/sioc/ns#')
    #
    # JKeckName = Literal('John W Keck')
    # DJeftsName = Literal('David Jefts')
    # JOrtizName = Literal("Juan Ortiz")
    # DSname = Literal('Demon Slayer')
    # age = Literal(56)
    #
    # g.add((JOrtiz, RDF.type, FOAF.Person))
    # g.add((JOrtiz, FOAF.name, JOrtizName))
    # g.add((JOrtiz, FOAF.knows, DJefts))
    # g.add((JOrtiz, FOAF.knows, JKeck))
    #
    # g.add((JKeck, RDF.type, FOAF.Person))
    # g.add((JKeck, FOAF.name, JKeckName))
    # g.add((JKeck, FOAF.knows, DJefts))
    # g.add((JKeck, FOAF.knows, JOrtiz))
    #
    # g.add((DJefts, RDF.type, FOAF.Person))
    # g.add((DJefts, FOAF.name, DJeftsName))
    # g.add((DJefts, FOAF.knows, JKeck))
    # g.add((DJefts, FOAF.knows, JOrtiz))
    #
    # g.add((JKeck, siocNamespace.likes, demonSlayer))
    # g.add((demonSlayer, FOAF.name, DSname))
    #
    # # print(g.serialize(format="turtle").decode("utf-8"))
    #
    # # print("--- printing raw triples ---")
    # # for s, p, o in g:
    # #    print((s, p, o))
    #
    # # print all the data in the Notation3 format
    # print("--- printing mboxes ---")
    # print(g.serialize(format = 'n3').decode("utf-8"))
    
    rdf_term = geo_search('detroit', 'michigan')
    print(rdf_term)
