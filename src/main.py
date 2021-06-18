import pandas as pd

import scraper_main
import rdf_main
import EntitiesToRDF
from rdflib import Graph, RDF, URIRef, Literal, BNode, FOAF, Namespace

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
    knowledge_graph.bind("foaf", FOAF)
    SIOC = Namespace('http://rdfs.org/sioc/ns#')
    
    user_uri = URIRef(fb_user_information['permalink'])
    user_name = Literal(fb_user_information['name'])
    knowledge_graph.add((user_uri, RDF.type, FOAF.Person))
    
    # Add Friends to graph
    for friend in user.friends:
        name = friend[0]
        link = friend[1]
        EntitiesToRDF.add_friend(knowledge_graph, user_uri, name, link)
    
    # TODO Add hobbies graph
    for hobby in user.hobbies:
        hobby_uri = URIRef('https://en.wikipedia.org/wiki/' + hobby)
        knowledge_graph.add((user_uri, SIOC.likes, hobby_uri))
    
    # TODO Add rest of basic user information
    
    # print all the data
    print("--- Knowledge Graph ---")
    print(knowledge_graph.serialize(format = 'turtle').decode("utf-8"))
