#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Running Experiment on Facebook Account John Keck
#
# Username: TimElvResearch@gmail.com
# Password: keckW2323#
#
#
# Testing facebook-scraper from pypi
# 03262021
####
import os
import re

import rdflib
from rdflib import URIRef, Literal, BNode
from rdflib import Graph
from rdflib import Namespace
from rdflib.namespace import DCTERMS, FOAF, SKOS, XSD, PROV, PROF, RDF
import entities_to_rdf

import pandas as pd
import nltk
from nltk.sem import relextract

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')


def extract_parts_of_speech(sentence, pos_list = []):
    """
    CC: Coordinating conjunction
    CD: Cardinal number
    DT: Determiner
    EX: Existential there
    FW: Foreign word
    IN: Preposition or subordinating conjunction
    JJ: Adjective
    VP: Verb Phrase
    JJR: Adjective, comparative
    JJS: Adjective, superlative
    LS: List item marker
    MD: Modal
    NN: Noun, singular or mass
    NNS: Noun, plural
    PP: Preposition Phrase
    NNP: Proper noun, singular Phrase
    NNPS: Proper noun, plural
    PDT: Pre determiner
    POS: Possessive ending
    PRP: Personal pronoun Phrase
    PRP: Possessive pronoun Phrase
    RB: Adverb
    RBR: Adverb, comparative
    RBS: Adverb, superlative
    RP: Particle
    S: Simple declarative clause
    SBAR: Clause introduced by a (possibly empty) subordinating conjunction
    SBARQ: Direct question introduced by a wh-word or a wh-phrase.
    SINV: Inverted declarative sentence, i.e. one in which the subject follows the tensed verb or modal.
    SQ: Inverted yes/no question, or main clause of a wh-question, following the wh-phrase in SBARQ.
    SYM: Symbol
    VBD: Verb, past tense
    VBG: Verb, gerund or present participle
    VBN: Verb, past participle
    VBP: Verb, non-3rd person singular present
    VBZ: Verb, 3rd person singular present
    WDT: Wh-determiner
    WP: Wh-pronoun
    WP: Possessive wh-pronoun
    WRB: Wh-adverb
    """
    sent = nltk.word_tokenize(sentence, language = 'english')
    pos_sent = nltk.pos_tag(sent)
    pos_list.append(pos_sent)
    return pos_sent


def extract_entities(tagged_tokens, ent_list = []):
    ent_sent = nltk.ne_chunk(tagged_tokens, binary = True)
    ent_list.append(ent_sent)
    return ent_sent


def extract_relations(sentence):
    classes = ["LOCATION", "ORGANIZATION", "PERSON", "DURATION", "DATE", "CARDINAL", "PERCENT", "MONEY", "MEASURE",
               "FACILITY", "GPE"]
    # sentence = "Mark works in JPMC in London every day"
    pos_tags = nltk.pos_tag(nltk.word_tokenize(sentence))  # POS tagging of the sentence
    ne = nltk.ne_chunk(pos_tags)  # Named Entity Recognition
    
    chunked = nltk.ne_chunk_sents(pos_tags, binary = True)
    
    print(pos_tags)
    
    IN = re.compile(r'.*\bin\b(?!\b.+ing)')
    rtuples = []
    for objclass in classes:
        for rel in nltk.sem.extract_rels('PERSON', objclass, ne, corpus = 'ace', pattern = IN):
            print(nltk.sem.rtuple(rel))
            rtuples.append(nltk.sem.rtuple(rel))
    
    # collect all the tags
    tags = []
    for tag in pos_tags:
        tags.append(tag[1])
        # PRP = possessive pronoun phrase e.g. 'I'
        # VBP = Verb, non-3rd person singular present
        # NN = Noun
    interests = []
    if 'PRP' in tags and 'VBP' in tags and ('NN' in tags or 'NNP'):
        for tag in pos_tags:
            if tag[1] == 'NN' or tag[1] == 'NNP':
                interests.append(tag[0])
    
    return rtuples, interests


def print_analysis_to_console(pos_list, ent_list, rel_list):
    print("Parts of Speech:")
    for pos in pos_list:
        print('\t', pos)
    
    print("Entities:")
    for pos in ent_list:
        if pos:
            print('\t', pos)
        if not pos:
            ent_list.remove(pos)
    
    print("Relationships:")
    print('\tRelations:', rel_list[0])
    print('\tInterests:', rel_list[1])
    print('\n')


def analyze_sentence(post):
    pos = extract_parts_of_speech(post)
    ent = extract_entities(pos)
    rel = extract_relations(post)
    return pos, ent, rel


if __name__ == "__main__":
    test_file = os.path.join(r"C:\Users\David Jefts\Desktop\SemanticSecurity\src\test_posts.txt")
    with open(test_file.__str__()) as file:
        read_data = file.read()
    # print(read_data)
    postsDf = pd.DataFrame(read_data.split("\n\n"))
    
    # move to a method
    # postsDf.info()
    # print(postsDf)
    # print(postsDf['data'])
    
    print(postsDf, '\n\n\n')
    # print(timestampsDf)
    interests_list = []
    for index, post in postsDf.iterrows():
        post = post[0]
        print(post)
        pos, ent, rel = analyze_sentence(post)
        print_analysis_to_console(pos, ent, rel)
        (interests_list.extend(rel[1]) if rel[1] else None)
    print(interests_list)
    
    # subObjList = extractSubsObjects(sentence)
    # relationList = extractRelations(sentence)
    
    # SocialRDF.generateTriples(subObjList, relationList)
    # SocialRDF.additionalTriples(subObjList, ent_list)
