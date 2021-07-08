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
    
    # establish the namespaces
    FOAF = Namespace('http://xmlns.com/foaf/0.1/')
    knowledge_graph.bind('foaf', FOAF)
    SIOC = Namespace('http://rdfs.org/sioc/ns#')
    knowledge_graph.bind('sioc', SIOC)
    EDU = Namespace('https://schema.org/EducationalOccupationalCredential')  # education credentials namespace
    knowledge_graph.bind('edu', EDU)
    
    # user node instantiation
    user_fb_uri = URIRef(fb_user_information['permalink'])
    user_name = Literal(fb_user_information['name'])
    knowledge_graph.add((user_fb_uri, RDF.type, FOAF.Person))
    knowledge_graph.add((user_fb_uri, FOAF.name, user_name))
    
    # TODO User's other accounts:
    # knowledge_graph.add((user_fb_uri, FOAF.sameAs, instagram))
    # knowledge_graph.add((user_fb_uri, FOAF.sameAs, linkedin))
    
    # Add Friends to graph
    for friend in user.friends:
        name = friend[0]
        link = friend[1]
        entities_to_rdf.add_friend(knowledge_graph, FOAF, user_fb_uri, name, link)
    
    # TODO Add hobbies graph
    # for hobby in user.hobbies:
    #     hobby_text = hobby.replace(' ', '_')
    #     hobby_uri = URIRef('https://en.wikipedia.org/wiki/' + hobby_text)
    #     knowledge_graph.add((hobby_uri, RDF.type,))
    #     knowledge_graph.add((user_fb_uri, SIOC.likes, hobby_uri))
    #     knowledge_graph.add((user_fb_uri, FOAF.knowsAbout, hobby_uri))
    
    # TODO Add rest of basic user information
    # for i in range(user.degrees):
    #     degree = user.degrees[i]
    #     school = user.schools[i]
    #     entities_to_rdf.add_diploma(knowledge_graph, degree, school)
    
    # print all the data
    print("--- Knowledge Graph ---")
    """ Format support can be extended with plugins,
        but "xml", "n3", "turtle", "nt", "pretty-xml", "trix", "trig" and "nquads" are built in."""
    print(knowledge_graph.serialize(format = 'turtle', encoding = 'utf-8').decode("utf-8"))
    
    # save the graph
    knowledge_graph.serialize(destination = "graph.ttl", format = 'turtle', encoding = 'utf-8')
