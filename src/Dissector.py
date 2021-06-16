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

import nltk
import pandas as pd

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')


def mung(post):
    list_mung = (post['data'])
    dict_mung = list_mung[0]
    sent = dict_mung["post"]
    return sent


def pos_extraction(sentence):
    sent = nltk.word_tokenize(sentence)
    pos_tag = nltk.pos_tag(sent)
    return pos_tag


def entity_extraction(sentence):
    ent = nltk.ne_chunk(sentence, binary = True)
    return ent


# def extractSubsAndObs(sent):
# this is just advanced string munging (enter patrick star meme of flashlight)

# def relationExtraction(sent):
postsDf = pd.read_json(r'C:/ERAU Juancho/Spring 2021/Omar/your_posts_1.json')
posList = []
entList = []

test = 'John Keck has $51 Billion dollars worth of Bitcoin given to him from Trump and Elon Musk lawsuit.'
tokens = nltk.word_tokenize(test)
pos_tag = nltk.pos_tag(tokens)
print(pos_tag)
print(nltk.ne_chunk(pos_tag, binary = True))

