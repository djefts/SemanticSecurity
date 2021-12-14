from rdfpandas.graph import to_dataframe
import pandas as pd
import rdflib
import requests

# for messages
def readfromhub(t="https://raw.githubusercontent.com/djefts/SemanticSecurity/master/src/graph.ttl"):
    r = requests.get(t)
    newfile = open("gitttl.ttl", 'w')
    newfile.write(r.text)
    file = rdflib.Graph()
    file.parse("gitttl.ttl", format="ttl")
    df = to_dataframe(file)
    df.index.name = "message"
    dg = df.iloc[:,0]
    dg.to_csv("test.csv")