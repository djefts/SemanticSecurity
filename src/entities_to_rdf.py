#!/usr/bin/env python
# coding: utf-8

"""
GeoNames Account Information:
username:   semsec_erau
email:      TimElvResearch@gmail.com
password:   keckW2323#
"""

import json
from datetime import datetime
from datetime import date
import geonames.adapters.search
from rdflib import Graph, RDF, URIRef, Literal
from rdflib import Namespace


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


class SocialMediaSite:
    def __init__(self, name, link, uri):
        self.name = name
        self.link = link
        self.uri = uri


class SocialSemanticWeb(Graph):
    # URL is at [0] and the graph URI is at [1]
    socmed_sites = {'facebook': SocialMediaSite('facebook', 'https://facebook.com/', None),
                    'instagram': SocialMediaSite('instagram', 'https://instagram.com/', None)
                    }
    
    # establish the namespaces -- A.K.A import the Ontologies
    SSO = Namespace('http://david.jefts/sso/')
    FOAF = Namespace('http://xmlns.com/foaf/0.1/')
    SIOC = Namespace('http://rdfs.org/sioc/ns#')
    EDU = Namespace('https://schema.org/EducationalOccupationalCredential')
    DCTERMS = Namespace('http://purl.org/dc/terms/')
    RDFS = Namespace('http://www.w3.org/2000/01/rdf-schema#')
    
    def __init__(self, user, fb_information):
        super(SocialSemanticWeb, self).__init__()
        self.bind('sso', self.SSO)
        self.bind('foaf', self.FOAF)
        self.bind('sioc', self.SIOC)
        self.bind('dcterms', self.DCTERMS)
        self.bind('rdfs', self.RDFS)
        self.namespace_manager = self.namespace_manager
        
        # add social medias to graph
        for site in self.socmed_sites:
            self.socmed_sites[site].uri = self.social_service_to_rdf(self.socmed_sites[site].link)
        
        # user node instantiation
        self.user_uri = URIRef(self.SSO + user.name.replace(' ', '-'))
        print(self.user_uri)  # = rdflib.term.URIRef(u'http://david.jefts/sso/John-Keck')
        self.add((self.user_uri, RDF.type, self.FOAF.Person))
        
        # user's basic info
        self.add((self.user_uri, self.FOAF.name, Literal(user.name)))
        self.add((self.user_uri, self.FOAF.gender, Literal(user.gender.lower())))  # FOAF docs specify lowercase
        self.add((self.user_uri, self.FOAF.birthday, Literal(user.birthday[0:5])))  # birthday = 'MM-DD-YYYY'
        today = date.today()
        born = datetime.strptime(user.birthday, '%m-%d-%Y')
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        self.add((self.user_uri, self.FOAF.age, Literal(age)))
        
        # user accounts initialization
        # Facebook Account:
        self.fb_uri = self.online_account_to_rdf(self.user_uri, fb_information['permalink'],
                                                 user.fb_username, self.socmed_sites['facebook'].uri)
        
        # initial SIOC information
        self.add((self.fb_uri, self.SIOC.email, Literal(user.fb_email)))
        self.add((self.fb_uri, self.SIOC.name, Literal(user.fb_username)))
    
    def social_service_to_rdf(self, social_media):
        site_uri = URIRef(social_media)
        self.add((site_uri, RDF.type, self.FOAF.Document))
        self.add((site_uri, RDF.type, self.SIOC.Site))
        return site_uri
    
    def online_account_to_rdf(self, user_uri, user_homepage, account_username, service_uri):
        account_uri = URIRef(user_homepage)
        # SIOC:UserAccount is a subclass of FOAF:OnlineAccount
        self.add((account_uri, RDF.type, self.SIOC.UserAccount))
        self.add((account_uri, self.FOAF.accountName, Literal(account_username)))
        self.add((account_uri, self.FOAF.accountServiceHomepage, service_uri))
        self.add((user_uri, self.FOAF.account, account_uri))
        self.add((account_uri, self.SIOC.account_of, user_uri))
        return account_uri
    
    def online_friend_to_rdf(self, user_uri, friend_uri, friend_name, account_link, friend_username, service_uri):
        # TODO: ensure friend doesn't exist in graph already
        # user node instantiation
        self.add((friend_uri, RDF.type, self.FOAF.Person))
        
        # Friend's FB Account:
        self.online_account_to_rdf(friend_uri, account_link, friend_username, service_uri)
        
        # connect friend to user
        self.add((friend_uri, RDF.type, self.FOAF.Person))
        self.add((friend_uri, self.FOAF.name, Literal(friend_name)))
        self.add((user_uri, self.FOAF.knows, friend_uri))
        self.add((friend_uri, self.FOAF.knows, user_uri))
        self.add((user_uri, self.SIOC.follows, friend_uri))
        return friend_uri
    
    def facebook_friend_to_rdf(self, user_uri, friend_uri, friend_name, account_link, friend_username):
        return self.online_friend_to_rdf(user_uri, friend_uri, friend_name, account_link, friend_username,
                                         self.socmed_sites['facebook'].uri)
    
    def post_to_rdf(self, post, site):
        post_uri = URIRef(post.link)
        self.add((post_uri, RDF.type, self.SIOC.Post))
        self.add((post_uri, RDF.type, self.FOAF.Document))
        
        published = ''
        for fmt in ('%B %d %I:%M %p', '%B %d', '%B %d, %Y'):
            # December 2 at 2:57 PM --> %B %d %I:%M %p
            # December 2            --> %B %d
            # December 5, 2020      --> %B %d, %Y
            if not post.published:
                continue
            if 'at ' in post.published:
                post.published = post.published.replace('at ', '')
            try:
                published = datetime.strptime(post.published, fmt)
                if published.year == 1900:
                    # no year in date string
                    published = published.replace(year = datetime.now().year)
            except ValueError:
                pass
        
        self.add((post_uri, self.DCTERMS.created, Literal(published)))
        self.add((post_uri, self.SIOC.has_space, site.uri))
        self.add((post_uri, self.SIOC.has_creator, self.user_uri))
        self.add((post_uri, self.RDFS.comment, Literal(post.text)))
        self.add((self.user_uri, self.SIOC.creator_of, post_uri))
    
    def diploma_to_rdf(self, degree, school):
        degree_uri = URIRef(degree + ' - ' + school)
        school_uri = URIRef(school)
        self.add((degree_uri, RDF.type, self.EDU))
        self.add((school_uri, RDF.type,))
        self.add((degree_uri, self.EDU.recognizedBy, school_uri))
        self.add((self.user_uri, self.FOAF.hasCredential,))
    
    def interest_to_rdf(self, interest):
        interest_uri = URIRef(self.SSO + interest)
        self.add((interest_uri, RDF.type, self.FOAF.Document))
        self.add((interest_uri, self.FOAF.topic, Literal(interest)))
        self.add((self.user_uri, self.FOAF.interest, interest_uri))
        self.add((self.user_uri, self.FOAF.knowsAbout, interest_uri))
        self.add((self.user_uri, self.SIOC.likes, interest_uri))
    
    def get_namespaces(self):
        namespaces = {}
        for prefix, namespace in self.namespace_manager.namespaces():
            namespaces[prefix] = namespace
        return namespaces
    
    def print_namespaces(self):
        return json.dumps(self.get_namespaces(), indent = 2)
    
    def save(self):
        """
        Saves the graph to "SemanticSecurity/src/graph.ttl"
        """
        self.serialize(destination = "graph.ttl", format = 'turtle', encoding = 'utf-8')
    
    def __str__(self):
        """
        Serializes the graph using RDF Turtle Format
        :return: string representation of the knowledge graph
        """
        out = "--- Knowledge Graph ---\n"
        # Format support can be extended with plugins,
        #    but "xml", "n3", "turtle", "nt", "pretty-xml", "trix", "trig" and "nquads" are built in."""
        out += self.serialize(format = 'turtle', encoding = 'utf-8').decode("utf-8")
        return out


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
