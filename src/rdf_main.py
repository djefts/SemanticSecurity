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
import rdflib
from rdflib import URIRef, Literal, BNode
from rdflib import Graph
from rdflib import Namespace
from rdflib.namespace import DCTERMS, FOAF, SKOS, XSD, PROV, PROF, RDF

import pandas as pd
import Dissector
import entities_to_rdf


def mung(post):
    list_mung = (post['data'])
    dict_mung = list_mung[0]
    sent = dict_mung["post"]
    return sent


def clean_dataframe(dataframe):
    posts_df = dataframe.drop(columns = ['title'])
    timestamps_df = dataframe['timestamp'].copy()
    posts_df = dataframe.drop(columns = ['timestamp'])
    return posts_df


def extract_parts_of_speech(sent, pos_list):
    pos_sent = Dissector.pos_extraction(sent)
    pos_list.append(pos_sent)
    return pos_sent


def extract_entities(sent, ent_list):
    ent_sent = Dissector.entity_extraction(sent)
    ent_list.append(ent_sent)
    return ent_sent


def print_analysis_to_console(pos_list, ent_list):
    print("\nParts of Speech:")
    for pos in pos_list:
        print(pos)
    print('\n\n\n')
    
    print("Entities:")
    for pos in ent_list:
        if pos:
            print(pos)
        if not pos:
            ent_list.remove(pos)
    print('\n')
    

def analyze_post(post):
    pos = extract_parts_of_speech(post, [])
    ent = extract_entities(pos, [])
    return pos, ent


if __name__ == "__main__":
    postsDf = pd.read_json(r'C:\Users\David Jefts\Desktop\SemanticSecurity\src\your_posts_1.json')
    
    # move to a method
    # postsDf.info()
    # print(postsDf)
    # print(postsDf['data'])
    
    print(postsDf)
    # print(timestampsDf)
    postsDf = clean_dataframe(postsDf)
    
    posList = []
    entList = []
    
    for index, post in postsDf.iterrows():
        sentence = mung(post)
        pos_tag = extract_parts_of_speech(sentence, posList)
        extract_entities(pos_tag, entList)
    
    # subObjList = extractSubsObjects(sentence)
    # relationList = extractRelations(sentence)
    
    # SocialRDF.generateTriples(subObjList, relationList)
    # SocialRDF.additionalTriples(subObjList, ent_list)
    
    print_analysis_to_console(posList, entList)
