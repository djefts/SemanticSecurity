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
    #     semantic_social_graph.interest_to_rdf(hobby)
    
    # TODO Add rest of basic user information
    
    """##### NLP/NLTK #####"""
    pos_list = []
    ent_list = []
    int_list = []
    # Add posts and comments to graph
    # loop through Facebook posts
    for post in online_user.fb_posts:
        semantic_social_graph.post_to_rdf(post, semantic_social_graph.socmed_sites['facebook'])
        print(post)
        
        pos_list, ent_list, rel_list = rdf_main.analyze_sentence(post.text)
        rdf_main.print_analysis_to_console(pos_list, ent_list, rel_list)
        
        (int_list.extend(rel_list[1]) if rel_list[1] else None)
    
    int_list.extend(online_user.hobbies)
    print("INTERESTS:", int_list)
    for interest in int_list:
        interest = interest.replace(' ', '_')
        semantic_social_graph.interest_to_rdf(interest)
    
    # TODO Relationship Extraction
    
    semantic_social_graph.save()
