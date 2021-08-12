import datetime
import json
from datetime import date

import pandas as pd

import scraper_main
import rdf_main
import entities_to_rdf
from rdflib import Graph, RDF, URIRef, Literal, BNode, Namespace

if __name__ == "__main__":
    # Facebook Scraper
    fb_user_information = {'email': 'TimElvResearch@gmail.com',
                           'password': 'keckW2323#',
                           'name': 'John Keck',
                           'username': 'john.keck.125',
                           'permalink': 'https://www.facebook.com/john.keck.125'}
    user = scraper_main.fb_scraper_main(fb_user_information)
    
    # NLP/NLTK
    posList = []
    entList = []
    for post in user.posts:
        posList, entList = rdf_main.analyze_post(post)
    rdf_main.print_analysis_to_console(posList, entList)
    
    # TODO Relationship Extraction
    
    # Knowledge Graph
    knowledge_graph = Graph()
    
    # establish the namespaces -- A.K.A import the Ontologies
    SSO = Namespace('http://david.jefts/sso/')
    knowledge_graph.bind('sso', SSO)
    FOAF = Namespace('http://xmlns.com/foaf/0.1/')
    knowledge_graph.bind('foaf', FOAF)
    SIOC = Namespace('http://rdfs.org/sioc/ns#')
    knowledge_graph.bind('sioc', SIOC)
    
    # print out the namespaces with formatting
    namespaces = entities_to_rdf.get_namespaces(knowledge_graph)
    json.dumps(namespaces, indent = 2)
    
    # user node instantiation
    user_uri = URIRef(SSO + user.name.replace(' ', '-'))
    print(user_uri)  # = rdflib.term.URIRef(u'http://david.jefts/sso/John-Keck')
    knowledge_graph.add((user_uri, RDF.type, FOAF.Person))
    
    socmed_sites = {'facebook': 'https://facebook.com/',
                    'instagram': 'https://instagram.com/',
                    }
    socmed_nodes = entities_to_rdf.init_social_media(knowledge_graph, socmed_sites.values())
    
    # Facebook Account:
    entities_to_rdf.add_online_account(knowledge_graph, user_uri, fb_user_information['permalink'], user.fb_username,
                                       socmed_nodes[socmed_sites['facebook']])
    
    # TODO Add rest of basic user information
    knowledge_graph.add((user_uri, FOAF.gender, Literal(user.gender.lower())))  # FOAF docs specify lowercase
    knowledge_graph.add((user_uri, FOAF.birthday, Literal(user.birthday[0:5])))  # birthday = 'MM-DD-YYYY'
    today = date.today()
    born = datetime.datetime.strptime(user.birthday, '%m-%d-%Y')
    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    knowledge_graph.add((user_uri, FOAF.age, Literal(age)))
    
    # Add Friends to graph
    for friend in user.friends:
        name = friend[0]
        link = friend[1]
        username = link.split('/')[-1]
        friend_uri = URIRef(SSO + name.replace(' ', '-'))
        #               add_facebook_friend(k_graph, user_uri, friend_uri, friend_name, account_link, friend_username):
        entities_to_rdf.add_online_friend(knowledge_graph, user_uri, friend_uri, name, link, username,
                                          socmed_nodes[socmed_sites['facebook']])
    
    # TODO Add hobbies graph
    # for hobby in user.hobbies:
    #     hobby_text = hobby.replace(' ', '_')
    #     hobby_uri = URIRef('https://en.wikipedia.org/wiki/' + hobby_text)
    #     knowledge_graph.add((hobby_uri, RDF.type,))
    #     knowledge_graph.add((user_fb_uri, SIOC.likes, hobby_uri))
    #     knowledge_graph.add((user_fb_uri, FOAF.knowsAbout, hobby_uri))
    
    # print all the data
    print("--- Knowledge Graph ---")
    """ Format support can be extended with plugins,
        but "xml", "n3", "turtle", "nt", "pretty-xml", "trix", "trig" and "nquads" are built in."""
    print(knowledge_graph.serialize(format = 'turtle', encoding = 'utf-8').decode("utf-8"))
    
    # save the graph
    knowledge_graph.serialize(destination = "graph.ttl", format = 'turtle', encoding = 'utf-8')
