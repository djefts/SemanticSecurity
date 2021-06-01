#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Running Experiment on Facebook Account John Keck
#
#Username: TimElvResearch@gmail.com
#Password: keckW2323#
#
#
#Testing facebook-scraper from pypi
#03262021
####
import rdflib
from rdflib import URIRef, Literal, BNode
from rdflib import Graph
from rdflib import Namespace
from rdflib.namespace import DCTERMS, FOAF, SKOS, XSD, PROV, PROF, RDF

import import_ipynb

import pandas as pd
import Dissector
import EntitiesToRDF

def mung(post):
	listMung = (post['data'])
	dictMung = listMung[0]
	sent = dictMung["post"]
	return sent

def cleanDataframe(dataframe):
	postsDf = dataframe.drop(columns = ['title'])
	timestampsDf = dataframe['timestamp'].copy()
	postsDf = dataframe.drop(columns = ['timestamp'])
	return postsDf

def extractPartsOfSpeech(sent, posList):
	posSent = Dissector.posExtraction(sent)
	posList.append(posSent)
	return posSent

def extractEntities(sent, entList):
	entSent = Dissector.entityExtraction(sent)
	entList.append(entSent)

def printAnalysisToConsole(posList, entList):
	print("Parts of Speech:")
	for list in posList:
		print(list)
	print('\n\n\n')

	print("Entities:")
	for list in entList:
		if list:
			print(list)
		if not list:
			entList.remove(list)
	print('\n')


if __name__ == "__main__":

	postsDf = pd.read_json(r'C:/ERAU Juancho/Spring 2021/Omar/your_posts_1.json')

	##move to a method
	##postsDf.info()
	##print(postsDf)
	##print(postsDf['data'])

	##print(postsDf)
	##print(timestampsDf)
	postsDf = cleanDataframe(postsDf)

	posList = []
	entList = []
    
	for index, post in postsDf.iterrows():
		sentence = mung(post)
		pos_tag = extractPartsOfSpeech(sentence,posList)
		extractEntities(pos_tag, entList)

		#subObjList = extractSubsObjects(sentence)
		#relationList = extractRelations(sentence)

	#SocialRDF.generateTriples(subObjList, relationList)
	#SocialRDF.additionalTriples(subObjList, entList)

	printAnalysisToConsole(posList, entList)


else:
	print('you cant import a main, tim')


# In[ ]:





# In[ ]:





# In[ ]:




