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
    online_user = scraper_main.fb_scraper_main(fb_user_information)
    
    # Knowledge Graph
    semantic_social_graph = entities_to_rdf.SocialSemanticWeb(online_user, fb_user_information)
    semantic_social_graph.print_namespaces()
    
    # Add Friends to graph
    for friend in online_user.friends:
        name = friend[0]
        link = friend[1]
        username = link.split('/')[-1]
        friend_uri = URIRef(semantic_social_graph.SSO + name.replace(' ', '-'))
        semantic_social_graph.facebook_friend_to_rdf(semantic_social_graph.user_uri, friend_uri, name, link, username)
    
    # TODO Add hobbies graph
    # for hobby in user.hobbies:
    #     hobby_text = hobby.replace(' ', '_')
    #     hobby_uri = URIRef('https://en.wikipedia.org/wiki/' + hobby_text)
    #     knowledge_graph.add((hobby_uri, RDF.type,))
    #     knowledge_graph.add((user_fb_uri, SIOC.likes, hobby_uri))
    #     knowledge_graph.add((user_fb_uri, FOAF.knowsAbout, hobby_uri))
    
    # TODO Relationship Extraction
    
    # NLP/NLTK
    posList = []
    entList = []
    for post in online_user.posts:
        posList, entList = rdf_main.analyze_post(post)
        rdf_main.print_analysis_to_console(posList, entList)
    
    # TODO Add rest of basic user information
    
    semantic_social_graph.save()
